from __future__ import annotations

import json
import os
import sys
from unittest.mock import patch

import pytest

from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkConfig, TaskResult
from xendris.benchmarking.agentic_programming.runner import run_benchmark, _check_forbidden_files, _run_single_task
from xendris.benchmarking.agentic_programming.scorer import compute_scores, compute_score_for_results
from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate
from xendris.benchmarking.agentic_programming.dataset import load_dataset


CONTROLS_PATH = os.path.join("runs", "agentic_programming_v0_1_deterministic_controls", "summary.json")
DRY_RUN_PATH = os.path.join("runs", "agentic_programming_v0_1_dry_run", "summary.json")


MOCK_API_RESPONSE = json.dumps({
    "choices": [{"message": {"content": '{"src/solver.py": "def solve():\\n    return 42\\n"}'}}],
    "usage": {"prompt_tokens": 500, "completion_tokens": 50},
})

MOCK_DEEPSEEK_PATCH = '{"src/solver.py": "def solve():\\n    return 42\\n"}'


@pytest.fixture
def mock_deepseek_call():
    with patch("xendris.benchmarking.agentic_programming.agents.deepseek_provider.call_deepseek") as mock:
        mock.return_value = (MOCK_DEEPSEEK_PATCH, 1500.0, 0.0015, "deepseek-v4-flash", None)
        yield mock


@pytest.fixture
def mock_no_api_key():
    with patch("xendris.benchmarking.agentic_programming.agents.deepseek_provider.get_deepseek_api_key") as mock:
        mock.return_value = None
        yield mock


class TestProviderConfig:
    def test_provider_key_not_hardcoded(self):
        from xendris.benchmarking.agentic_programming.agents.deepseek_provider import get_deepseek_api_key
        key = get_deepseek_api_key()
        assert key is None or len(key) > 0
        source_path = os.path.join(
            "xendris", "benchmarking", "agentic_programming",
            "agents", "deepseek_provider.py"
        )
        with open(source_path) as f:
            content = f.read()
        assert "DEEPSEEK_API_KEY = " not in content
        assert "OPENAI_API_KEY = " not in content

    def test_live_mode_requires_deepseek_variant_to_error_in_dry_run(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="dry-run",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        for r in results:
            assert r.patch_applied is False
            assert "live" in (r.error_message or "").lower()

    def test_output_path_is_separate(self):
        assert "deepseek_pilot" not in DRY_RUN_PATH
        assert "deepseek_pilot" not in CONTROLS_PATH

    def test_historical_artifacts_not_overwritten_by_pilot(self):
        assert os.path.isfile(DRY_RUN_PATH), "Dry-run summary should still exist"
        assert os.path.isfile(CONTROLS_PATH), "Controls summary should still exist"


class TestSafeDotenvLoading:
    def test_process_environment_has_priority(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.setenv("DEEPSEEK_API_KEY", "process-secret")
        (tmp_path / ".env.local").write_text("DEEPSEEK_API_KEY=file-secret\n", encoding="utf-8")

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["detected"] is True
        assert meta["source"] == "process_env"
        assert meta["credential_source"] == "env:DEEPSEEK_API_KEY"
        assert os.environ["DEEPSEEK_API_KEY"] == "process-secret"

    def test_root_env_local_has_priority_over_frontend_env_local(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        (tmp_path / "frontend").mkdir()
        (tmp_path / ".env.local").write_text("DEEPSEEK_API_KEY=root-local-secret\n", encoding="utf-8")
        (tmp_path / "frontend" / ".env.local").write_text("DEEPSEEK_API_KEY=frontend-local-secret\n", encoding="utf-8")

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["source"] == ".env.local"
        assert meta["credential_source"] == "dotenv:.env.local/DEEPSEEK_API_KEY"
        assert os.environ["DEEPSEEK_API_KEY"] == "root-local-secret"

    def test_root_env_has_priority_over_frontend_env_local(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        (tmp_path / "frontend").mkdir()
        (tmp_path / ".env").write_text("DEEPSEEK_API_KEY=root-env-secret\n", encoding="utf-8")
        (tmp_path / "frontend" / ".env.local").write_text("DEEPSEEK_API_KEY=frontend-local-secret\n", encoding="utf-8")

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["source"] == ".env"
        assert meta["credential_source"] == "dotenv:.env/DEEPSEEK_API_KEY"
        assert os.environ["DEEPSEEK_API_KEY"] == "root-env-secret"

    def test_frontend_env_local_is_loaded_as_fallback(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        (tmp_path / "frontend").mkdir()
        (tmp_path / "frontend" / ".env.local").write_text("DEEPSEEK_API_KEY=frontend-local-secret\n", encoding="utf-8")

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["detected"] is True
        assert meta["source"] == "frontend/.env.local"
        assert meta["credential_source"] == "dotenv:frontend/.env.local/DEEPSEEK_API_KEY"
        assert os.environ["DEEPSEEK_API_KEY"] == "frontend-local-secret"

    def test_frontend_env_is_loaded_when_frontend_env_local_is_absent(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        (tmp_path / "frontend").mkdir()
        (tmp_path / "frontend" / ".env").write_text("DEEPSEEK_API_KEY=frontend-env-secret\n", encoding="utf-8")

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["source"] == "frontend/.env"
        assert meta["credential_source"] == "dotenv:frontend/.env/DEEPSEEK_API_KEY"
        assert os.environ["DEEPSEEK_API_KEY"] == "frontend-env-secret"

    def test_missing_all_env_sources_fails_safely(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        monkeypatch.setenv("OPENROUTER_API_KEY", "ignored-openrouter-secret")

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["detected"] is False
        assert meta["source"] == "missing"
        assert meta["credential_source"] == "missing"
        assert "DEEPSEEK_API_KEY" not in os.environ

    def test_quoted_values_comments_and_blank_lines_are_supported(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import load_deepseek_api_key_from_env_files

        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        (tmp_path / ".env.local").write_text(
            "\n# comment\nOTHER_KEY=ignored\nDEEPSEEK_API_KEY='quoted-secret'\n",
            encoding="utf-8",
        )

        meta = load_deepseek_api_key_from_env_files(str(tmp_path))

        assert meta["source"] == ".env.local"
        assert os.environ["DEEPSEEK_API_KEY"] == "quoted-secret"

    def test_credential_source_is_safe_and_secret_not_in_summary_or_report(self, tmp_path, monkeypatch):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary
        from xendris.benchmarking.agentic_programming.report import generate_markdown_report

        secret = "unit-test-secret-that-must-not-leak"
        monkeypatch.setenv("DEEPSEEK_API_KEY", secret)
        result = TaskResult(
            sample_id="AP-001",
            agent_variant="deepseek_base_agent",
            patch_applied=True,
            visible_tests_passed=True,
            hidden_tests_passed=True,
            api_contract_preserved=True,
            no_forbidden_files_touched=True,
            no_false_success_claim=True,
            minimal_patch=True,
            security_clean=True,
            iterations_used=1,
            error_message=None,
            patch_content="",
            provider="deepseek",
            model="deepseek-v4-flash",
            transport="direct",
            latency_ms=100.0,
            cost_estimate=0.001,
        )
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir=str(tmp_path),
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            provider="deepseek",
            model="deepseek-v4-flash",
            transport="direct",
            credential_source="dotenv:frontend/.env.local/DEEPSEEK_API_KEY",
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        report_path = tmp_path / "report.md"
        generate_markdown_report(scores, summary, decisions, str(report_path))

        summary_text = json.dumps(summary)
        report_text = report_path.read_text(encoding="utf-8")

        assert summary["credential_source"] == "dotenv:frontend/.env.local/DEEPSEEK_API_KEY"
        assert secret not in summary_text
        assert secret not in report_text
        assert "OPENROUTER_API_KEY" not in summary_text
        assert "deepseek/deepseek" not in summary_text


class TestSummarySchema:
    def test_summary_includes_provider_model_transport(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            provider="deepseek",
            model="deepseek-v4-flash",
            transport="direct",
        )
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary
        results = run_benchmark(config)
        scores = compute_scores(results)
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, config, scores, decisions)
        assert summary.get("execution_mode") == "live"
        assert summary.get("provider_mode") == "real"
        assert summary.get("provider") == "deepseek"
        assert summary.get("transport") == "direct"
        assert summary.get("model") == "deepseek-v4-flash"
        assert summary.get("credential_source") == "env:DEEPSEEK_API_KEY"
        assert summary.get("no_openrouter_used") is True

    def test_cost_and_latency_fields_exist(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        scores = compute_scores(results)
        decisions = evaluate_excellence_gate(scores)
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary, _compute_commercial_metrics
        commercial = _compute_commercial_metrics(results)
        assert "average_latency_ms" in commercial
        assert "estimated_cost_total" in commercial
        assert "cost_per_verified_successful_task" in commercial


class TestComparisonMode:
    def _synthetic_results(self) -> list[TaskResult]:
        return [
            TaskResult(
                sample_id="AP-001",
                agent_variant="deepseek_base_agent",
                patch_applied=True,
                visible_tests_passed=True,
                hidden_tests_passed=False,
                api_contract_preserved=True,
                no_forbidden_files_touched=True,
                no_false_success_claim=True,
                minimal_patch=True,
                security_clean=True,
                iterations_used=1,
                error_message=None,
                patch_content="",
                provider="deepseek",
                model="deepseek-v4-flash",
                transport="direct",
                latency_ms=100.0,
                cost_estimate=0.001,
            ),
            TaskResult(
                sample_id="AP-001",
                agent_variant="deepseek_xendris_agent",
                patch_applied=True,
                visible_tests_passed=True,
                hidden_tests_passed=True,
                api_contract_preserved=True,
                no_forbidden_files_touched=True,
                no_false_success_claim=True,
                minimal_patch=True,
                security_clean=True,
                iterations_used=1,
                error_message=None,
                patch_content="",
                provider="deepseek",
                model="deepseek-v4-flash",
                transport="direct",
                latency_ms=100.0,
                cost_estimate=0.001,
            ),
        ]

    def _config(self, **overrides) -> BenchmarkConfig:
        data = {
            "dataset_path": "benchmarks/agentic_programming/v0_1",
            "agent_variants": (AgentVariant.DEEPSEEK_BASE_AGENT, AgentVariant.DEEPSEEK_XENDRIS_AGENT),
            "execution_mode": "live",
            "output_dir": "/tmp/test_pilot_out",
            "agent_module": "xendris.benchmarking.agentic_programming.agents",
            "max_concurrent": 1,
            "seed": 42,
            "provider": "deepseek",
            "model": "deepseek-v4-flash",
            "transport": "direct",
            "max_samples": 1,
            "credential_source": "dotenv:frontend/.env.local/DEEPSEEK_API_KEY",
        }
        data.update(overrides)
        return BenchmarkConfig(**data)

    def test_comparison_mode_warns_instead_of_blocking_for_blocked_baseline(self):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary

        results = self._synthetic_results()
        scores = {
            "deepseek_base_agent": {"total_score": 0.5, "tasks_passed": 0, "tasks_total": 1, "pass_rate": 0.0},
            "deepseek_xendris_agent": {"total_score": 1.0, "tasks_passed": 1, "tasks_total": 1, "pass_rate": 1.0},
        }
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, self._config(), scores, decisions, comparison_mode=True)

        assert summary["benchmark_level_decision"] == "WARNINGS_PRESENT"
        assert summary["variant_gate_decisions"]["deepseek_base_agent"] == "BLOCKED_FOR_INTERPRETATION"
        assert summary["variant_gate_decisions"]["deepseek_xendris_agent"] == "READY_FOR_INTERPRETATION"
        assert summary["blocked_variants"] == ["deepseek_base_agent"]
        assert "not admitted as positive evidence" in summary["comparison_interpretation_scope"]
        assert "not evidence of general coding superiority" in summary["no_general_coding_superiority_warning"]

    def test_comparison_mode_allows_warning_baseline_without_benchmark_warning(self):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary

        results = self._synthetic_results()
        scores = {
            "deepseek_base_agent": {"total_score": 0.50, "tasks_passed": 1, "tasks_total": 5, "pass_rate": 0.20},
            "deepseek_xendris_agent": {"total_score": 1.0, "tasks_passed": 5, "tasks_total": 5, "pass_rate": 1.0},
        }
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, self._config(), scores, decisions, comparison_mode=True)

        assert summary["variant_gate_decisions"]["deepseek_base_agent"] == "WARNINGS_PRESENT"
        assert summary["blocked_variants"] == []
        assert summary["benchmark_level_decision"] == "READY_FOR_INTERPRETATION"

    def test_strict_mode_blocks_when_any_variant_is_blocked(self):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary

        results = self._synthetic_results()
        scores = {
            "deepseek_base_agent": {"total_score": 0.5, "tasks_passed": 0, "tasks_total": 1, "pass_rate": 0.0},
            "deepseek_xendris_agent": {"total_score": 1.0, "tasks_passed": 1, "tasks_total": 1, "pass_rate": 1.0},
        }
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, self._config(), scores, decisions, comparison_mode=False)

        assert summary["benchmark_level_decision"] == "BLOCKED_FOR_INTERPRETATION"

    def test_benchmark_level_blocks_if_provider_disclosure_missing(self):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary

        results = [
            TaskResult(
                sample_id="AP-001",
                agent_variant="base_agent",
                patch_applied=True,
                visible_tests_passed=True,
                hidden_tests_passed=False,
                api_contract_preserved=True,
                no_forbidden_files_touched=True,
                no_false_success_claim=True,
                minimal_patch=True,
                security_clean=True,
                iterations_used=1,
                error_message=None,
                patch_content="",
            ),
        ]
        scores = {
            "base_agent": {"total_score": 0.5, "tasks_passed": 0, "tasks_total": 1, "pass_rate": 0.0},
        }
        decisions = evaluate_excellence_gate(scores)
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.BASE_AGENT,),
            execution_mode="dry-run",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            provider=None,
        )
        summary = _build_canonical_summary(results, config, scores, decisions, comparison_mode=True)

        assert summary["benchmark_level_decision"] == "BLOCKED_FOR_INTERPRETATION"

    def test_report_discloses_blocked_baseline_and_forbidden_interpretations(self, tmp_path):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary
        from xendris.benchmarking.agentic_programming.report import generate_markdown_report

        results = self._synthetic_results()
        scores = {
            "deepseek_base_agent": {"total_score": 0.5, "tasks_passed": 0, "tasks_total": 1, "pass_rate": 0.0},
            "deepseek_xendris_agent": {"total_score": 1.0, "tasks_passed": 1, "tasks_total": 1, "pass_rate": 1.0},
        }
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, self._config(), scores, decisions, comparison_mode=True)
        report_path = tmp_path / "report.md"

        generate_markdown_report(scores, summary, decisions, str(report_path))
        report = report_path.read_text(encoding="utf-8")

        assert "Blocked variants are included for comparison only" in report
        assert "blocked baseline" in report.lower()
        assert "must not be treated as admitted positive evidence" in report
        assert "Universal superiority" in report
        assert "General coding superiority" in report
        assert "No General Coding Superiority Claim" in report

    def test_ready_for_interpretation_when_no_variant_blocked(self):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary

        results = self._synthetic_results()
        scores = {
            "deepseek_xendris_agent": {"total_score": 1.0, "tasks_passed": 1, "tasks_total": 1, "pass_rate": 1.0},
        }
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, self._config(), scores, decisions, comparison_mode=True)

        assert summary["variant_gate_decisions"]["deepseek_xendris_agent"] == "READY_FOR_INTERPRETATION"
        assert summary["benchmark_level_decision"] == "READY_FOR_INTERPRETATION"


class TestAuditFields:
    def test_xendris_variant_includes_audit_fields(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_XENDRIS_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        for r in results:
            if r.patch_applied:
                assert r.xendris_audit is not None
                assert r.xendris_audit.get("allowed_files_enforced") is True
                assert r.xendris_audit.get("forbidden_files_checked") is True
                assert r.xendris_audit.get("test_evidence_required") is True

    def test_calibrated_variant_includes_calibration_fields(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_XENDRIS_CALIBRATED_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        for r in results:
            if r.patch_applied:
                assert r.calibration_audit is not None
                assert r.calibration_audit.get("intervention_policy") == "ProgrammingInterventionPolicy"
                assert r.calibration_audit.get("mode") == "CODE_SANDBOX"

    def test_deepseek_base_agent_no_audit_fields(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        for r in results:
            assert r.xendris_audit is None
            assert r.calibration_audit is None


class TestDeltas:
    def test_distance_to_oracle_computed(self):
        from scripts.run_agentic_programming_benchmark import _compute_deltas
        scores = {
            "deepseek_base_agent": {"total_score": 0.5, "pass_rate": 0.5},
            "deepseek_xendris_agent": {"total_score": 0.6, "pass_rate": 0.6},
        }
        deltas = _compute_deltas(scores)
        assert deltas["deepseek_base_agent"]["distance_to_oracle"] == 0.5
        assert deltas["deepseek_xendris_agent"]["distance_to_oracle"] == 0.4
        assert deltas["deepseek_xendris_agent"]["delta_vs_deepseek_base"] == 0.1
        assert deltas["deepseek_base_agent"]["delta_vs_deepseek_base"] == 0.0


class TestExcellenceGate:
    def test_gate_blocks_missing_provider_disclosure(self, mock_deepseek_call):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
        )
        results = run_benchmark(config)
        scores = compute_scores(results)
        decisions = evaluate_excellence_gate(scores)
        has_blocked = any(d == "BLOCKED_FOR_INTERPRETATION" for d in decisions.values())
        assert has_blocked

    def test_gate_blocks_universal_superiority_wording(self):
        from scripts.run_agentic_programming_benchmark import _build_canonical_summary
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/test_pilot_out",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            provider="deepseek",
            model="deepseek-v4-flash",
        )
        results = [TaskResult(
            sample_id="AP-001",
            agent_variant="deepseek_base_agent",
            patch_applied=True,
            visible_tests_passed=False,
            hidden_tests_passed=False,
            api_contract_preserved=True,
            no_forbidden_files_touched=True,
            no_false_success_claim=True,
            minimal_patch=True,
            security_clean=True,
            iterations_used=1,
            error_message=None,
            patch_content="",
        )]
        scores = compute_scores(results)
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary(results, config, scores, decisions)
        warning = summary.get("no_universal_superiority_warning", "")
        assert "not" in warning.lower() or "no" in warning.lower()


class TestDeterministicControls:
    def test_controls_not_confused_with_real_evidence(self):
        with open(CONTROLS_PATH) as f:
            controls = json.load(f)
        interpretation = controls.get("evidence_interpretation", "")
        assert "not admissible as evidence" in interpretation.lower()


class TestBedrockIntegrity:
    def test_taskresult_has_provider_fields(self):
        r = TaskResult(
            sample_id="AP-TEST",
            agent_variant="deepseek_base_agent",
            patch_applied=True,
            visible_tests_passed=True,
            hidden_tests_passed=True,
            api_contract_preserved=True,
            no_forbidden_files_touched=True,
            no_false_success_claim=True,
            minimal_patch=True,
            security_clean=True,
            iterations_used=1,
            error_message=None,
            patch_content="",
            provider="deepseek",
            model="deepseek-v4-flash",
            transport="direct",
            latency_ms=1500.0,
            cost_estimate=0.0015,
        )
        d = r.to_dict()
        assert d.get("provider") == "deepseek"
        assert d.get("model") == "deepseek-v4-flash"
        assert d.get("transport") == "direct"
        assert d.get("latency_ms") == 1500.0
        assert d.get("cost_estimate") == 0.0015

    def test_benchmark_config_has_provider_fields(self):
        c = BenchmarkConfig(
            dataset_path="test",
            agent_variants=(AgentVariant.DEEPSEEK_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="test",
            max_concurrent=1,
            seed=42,
            provider="deepseek",
            model="deepseek-v4-flash",
            transport="direct",
            budget_usd=1.0,
            max_samples=5,
            max_iterations=2,
        )
        d = c.to_dict()
        assert d.get("provider") == "deepseek"
        assert d.get("model") == "deepseek-v4-flash"
        assert d.get("transport") == "direct"
        assert d.get("budget_usd") == 1.0
        assert d.get("max_samples") == 5
        assert d.get("max_iterations") == 2

    def test_deepseek_variants_defined(self):
        assert AgentVariant.DEEPSEEK_BASE_AGENT is not None
        assert AgentVariant.DEEPSEEK_XENDRIS_AGENT is not None
        assert AgentVariant.DEEPSEEK_XENDRIS_CALIBRATED_AGENT is not None
        assert AgentVariant.is_deepseek_variant(AgentVariant.DEEPSEEK_BASE_AGENT)
        assert AgentVariant.is_deepseek_variant(AgentVariant.DEEPSEEK_XENDRIS_AGENT)
        assert not AgentVariant.is_deepseek_variant(AgentVariant.ORACLE_AGENT)


class TestPatchApplication:
    def test_deepseek_patch_applies_to_working_dir(self, mock_deepseek_call):
        from xendris.benchmarking.agentic_programming.patcher import apply_patch
        import tempfile, os
        with tempfile.TemporaryDirectory() as tmp:
            result = apply_patch(tmp, MOCK_DEEPSEEK_PATCH)
            assert result is True
            solver_path = os.path.join(tmp, "src", "solver.py")
            assert os.path.isfile(solver_path)
            with open(solver_path) as f:
                assert "return 42" in f.read()


class TestForbiddenFileCheck:
    def test_forbidden_file_check_blocks_bad_agent(self):
        bad_files = ["tests/test_deleted.py", "tests/test_some.py"]
        assert _check_forbidden_files(bad_files, ("tests/",)) is False

    def test_forbidden_file_check_allows_src_only(self):
        good_files = ["src/solver.py"]
        assert _check_forbidden_files(good_files, ("tests/",)) is True
