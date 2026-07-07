from __future__ import annotations

import json
import os
from unittest.mock import patch

from scripts.run_agentic_programming_benchmark import (
    EvidenceContract,
    ExecutionIdentity,
    InterpretationAdmissibility,
    ModelSpec,
    _build_canonical_summary,
    _build_execution_provenance,
    _get_providers_from_variants,
    build_evidence_contract,
    build_evidence_report_markdown,
    evaluate_interpretation_admissibility,
    load_openai_api_key_from_env_files,
    resolve_execution_identity,
    resolve_model_spec,
)
from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate
from xendris.benchmarking.agentic_programming.scorer import compute_scores
from xendris.benchmarking.agentic_programming.types import AgentVariant, BenchmarkConfig, TaskResult


def test_openai_process_environment_has_priority(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "process-secret")
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend" / ".env.local").write_text("OPENAI_API_KEY=file-secret\n", encoding="utf-8")

    meta = load_openai_api_key_from_env_files(str(tmp_path))

    assert meta["detected"] is True
    assert meta["source"] == "process_env"
    assert meta["credential_source"] == "env:OPENAI_API_KEY"
    assert os.environ["OPENAI_API_KEY"] == "process-secret"


def test_openai_frontend_env_local_fallback(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    (tmp_path / "frontend").mkdir()
    (tmp_path / "frontend" / ".env.local").write_text("OPENAI_API_KEY=file-secret\n", encoding="utf-8")

    meta = load_openai_api_key_from_env_files(str(tmp_path))

    assert meta["detected"] is True
    assert meta["source"] == "frontend/.env.local"
    assert meta["credential_source"] == "dotenv:frontend/.env.local/OPENAI_API_KEY"
    assert os.environ["OPENAI_API_KEY"] == "file-secret"


def test_openai_missing_key_fails_preflight_safely(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", "ignored-openrouter-secret")

    meta = load_openai_api_key_from_env_files(str(tmp_path))

    assert meta["detected"] is False
    assert meta["source"] == "missing"
    assert meta["credential_source"] == "missing"
    assert "OPENAI_API_KEY" not in os.environ


def test_openai_provider_cost_estimation_known_and_unknown_pricing():
    from xendris.benchmarking.agentic_programming.agents.openai_provider import estimate_openai_cost

    cost, quality = estimate_openai_cost(1000, 1000, "gpt-4.1-mini")
    fallback_cost, fallback_quality = estimate_openai_cost(1000, 1000, "future-model")

    assert cost == 0.002
    assert quality == "known_pricing"
    assert fallback_cost == 0.003
    assert fallback_quality == "unknown_pricing_fallback"


def test_openai_summary_is_secret_safe(tmp_path):
    secret = "unit-test-openai-secret"
    result = TaskResult(
        sample_id="AP-001",
        agent_variant="openai_base_agent",
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
        provider="openai",
        model="gpt-4.1-mini",
        provider_reported_model="gpt-4.1-mini",
        transport="direct",
        latency_ms=100.0,
        cost_estimate=0.001,
        cost_estimate_quality="known_pricing",
    )
    config = BenchmarkConfig(
        dataset_path="benchmarks/agentic_programming/v0_1",
        agent_variants=(AgentVariant.OPENAI_BASE_AGENT,),
        execution_mode="live",
        output_dir=str(tmp_path),
        agent_module="xendris.benchmarking.agentic_programming.agents",
        max_concurrent=1,
        seed=42,
        provider="openai",
        transport="direct",
        credential_sources_by_provider={"openai": "dotenv:frontend/.env.local/OPENAI_API_KEY"},
        model_map={"openai": "gpt-4.1-mini"},
    )

    summary = _build_canonical_summary([result], config, compute_scores([result]), evaluate_excellence_gate(compute_scores([result])), comparison_mode=True)
    summary_text = json.dumps(summary)

    assert secret not in summary_text
    assert "Authorization:" not in summary_text
    assert "Bearer" not in summary_text
    assert summary["providers"] == ["openai"]
    assert summary["models_by_variant"]["openai_base_agent"] == "gpt-4.1-mini"


def test_openai_live_variant_uses_mocked_provider_call(monkeypatch):
    from xendris.benchmarking.agentic_programming.runner import run_benchmark

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    with patch("xendris.benchmarking.agentic_programming.agents.openai_provider.call_openai") as mock_call:
        mock_call.return_value = (
            '{"src/solver.py": "def solve():\\n    return 42\\n"}',
            123.0,
            0.001,
            "gpt-4.1-mini",
            None,
        )
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(AgentVariant.OPENAI_BASE_AGENT,),
            execution_mode="live",
            output_dir="/tmp/openai-pilot",
            agent_module="xendris.benchmarking.agentic_programming.agents",
            max_concurrent=1,
            seed=42,
            transport="direct",
            model_map={"openai": "gpt-4.1-mini"},
        )

        results = run_benchmark(config)

    assert results
    assert all(r.provider == "openai" for r in results)
    assert all(r.model == "gpt-4.1-mini" for r in results)
    assert all(r.transport == "direct" for r in results)


class TestPreflightProvider:
    """Tests for --preflight-only with explicit --provider and --model."""

    def test_preflight_openai_with_explicit_model(self, monkeypatch, tmp_path):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "")
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        from scripts.run_agentic_programming_benchmark import main as cli_main
        import sys
        test_args = [
            "run_agentic_programming_benchmark.py",
            "--preflight-only",
            "--provider", "openai",
            "--model", "gpt-5.5",
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        try:
            cli_main()
        except SystemExit as e:
            assert e.code == 0

    def test_preflight_deepseek_with_explicit_model(self, monkeypatch, tmp_path):
        monkeypatch.setenv("DEEPSEEK_API_KEY", "test-deepseek-key")
        monkeypatch.setenv("OPENAI_API_KEY", "")
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        from scripts.run_agentic_programming_benchmark import main as cli_main
        import sys
        test_args = [
            "run_agentic_programming_benchmark.py",
            "--preflight-only",
            "--provider", "deepseek",
            "--model", "deepseek-v4-flash",
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        try:
            cli_main()
        except SystemExit as e:
            assert e.code == 0

    def test_preflight_openai_with_task_suite(self, monkeypatch, tmp_path):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key")
        from scripts.run_agentic_programming_benchmark import main as cli_main
        import sys
        test_args = [
            "run_agentic_programming_benchmark.py",
            "--task-suite", "real_world_v0_2",
            "--preflight-only",
            "--provider", "openai",
            "--model", "gpt-5.5",
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        try:
            cli_main()
        except SystemExit as e:
            assert e.code == 0

    def test_preflight_openai_missing_key_reports_false(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
        from scripts.run_agentic_programming_benchmark import main as cli_main
        import sys
        test_args = [
            "run_agentic_programming_benchmark.py",
            "--preflight-only",
            "--provider", "openai",
            "--model", "gpt-5.5",
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        try:
            cli_main()
        except SystemExit as e:
            assert e.code == 1

    def test_preflight_no_secrets_in_output(self, monkeypatch, capsys):
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test-secret-value-12345")
        from scripts.run_agentic_programming_benchmark import main as cli_main
        import sys
        test_args = [
            "run_agentic_programming_benchmark.py",
            "--preflight-only",
            "--provider", "openai",
            "--model", "gpt-5.5",
        ]
        monkeypatch.setattr(sys, "argv", test_args)
        try:
            cli_main()
        except SystemExit:
            pass
        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "sk-test-secret-value" not in output
        assert "Authorization:" not in output
        assert "Bearer" not in output


class TestSummaryProviderTransport:
    """Summary aggregates provider and transport from results/config."""

    def test_providers_from_variant_names(self):
        agents = ["openai_base_agent", "deepseek_base_agent"]
        result = _get_providers_from_variants(agents)
        assert result == ["deepseek", "openai"]

    def test_providers_fallback_to_config(self):
        agents = ["base_agent"]
        from xendris.benchmarking.agentic_programming.types import BenchmarkConfig
        config = BenchmarkConfig(
            dataset_path="",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai",
            transport="direct",
        )
        result = _get_providers_from_variants(agents, config=config)
        assert result == ["openai"]

    def test_providers_fallback_to_results(self):
        agents = ["base_agent"]
        from xendris.benchmarking.agentic_programming.types import TaskResult
        results = [
            TaskResult(
                sample_id="T1", agent_variant="base_agent",
                patch_applied=True, visible_tests_passed=False,
                hidden_tests_passed=None, api_contract_preserved=True,
                no_forbidden_files_touched=True, no_false_success_claim=True,
                minimal_patch=None, security_clean=True, iterations_used=1,
                error_message=None, patch_content="",
                provider="openai", model="gpt-5.5", transport="direct",
            ),
        ]
        result = _get_providers_from_variants(agents, results=results)
        assert result == ["openai"]

    def test_live_summary_includes_providers_and_transport(self):
        from xendris.benchmarking.agentic_programming.types import TaskResult, BenchmarkConfig
        from xendris.benchmarking.agentic_programming.scorer import compute_scores
        from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate

        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", model="gpt-5.5", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", model="gpt-5.5", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert summary["providers"] == ["openai"]
        assert summary["transport"] == "direct"
        assert summary["transports"] == ["direct"]

    def test_live_summary_with_non_openai_variant_names(self):
        """Non-live variant names (base_agent) still yield openai provider in summary."""
        from xendris.benchmarking.agentic_programming.types import TaskResult, BenchmarkConfig
        from xendris.benchmarking.agentic_programming.scorer import compute_scores
        from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate

        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", model="gpt-5.5", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", model="gpt-5.5", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert summary["provider"] == "openai"
        assert summary["providers"] == ["openai"]
        assert summary["transport"] == "direct"


class TestProvenance:
    """execution_provenance block tracks provider/transport inference chain."""

    def test_provenance_variant_prefix(self):
        agents = ["openai_base_agent"]
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None, transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="openai_base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", transport="direct",
        )
        prov = _build_execution_provenance(agents, config, [result], ["openai"], "direct")
        assert prov["execution_provenance"]["provider_source"] == "variant_name_prefix"
        assert prov["execution_provenance"]["variant_provider_inference"] is True
        assert prov["execution_provenance"]["config_provider_fallback_used"] is False

    def test_provenance_config_provider(self):
        agents = ["base_agent"]
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        prov = _build_execution_provenance(agents, config, [result], ["openai"], "direct")
        assert prov["execution_provenance"]["provider_source"] == "config.provider"
        assert prov["execution_provenance"]["config_provider_fallback_used"] is True
        assert prov["execution_provenance"]["variant_provider_inference"] is False

    def test_provenance_result_provider(self):
        agents = ["base_agent"]
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None, transport=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai",
        )
        prov = _build_execution_provenance(agents, config, [result], ["openai"], None)
        assert prov["execution_provenance"]["provider_source"] == "result.provider"
        assert prov["execution_provenance"]["result_provider_fallback_used"] is True
        assert prov["execution_provenance"]["variant_provider_inference"] is False
        assert prov["execution_provenance"]["config_provider_fallback_used"] is False

    def test_provenance_explicit_provider_transport(self):
        agents = ["base_agent"]
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", transport="direct",
        )
        prov = _build_execution_provenance(agents, config, [result], ["openai"], "direct")
        assert prov["execution_provenance"]["transport_source"] == "explicit_provider_default"

    def test_provenance_result_transport_fallback(self):
        agents = ["base_agent"]
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", transport="direct",
        )
        prov = _build_execution_provenance(agents, config, [result], ["openai"], "direct")
        assert prov["execution_provenance"]["transport_source"] == "result.transport"
        assert prov["execution_provenance"]["result_transport_fallback_used"] is True

    def test_provenance_none(self):
        agents = ["base_agent"]
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="dry-run", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None, transport=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        prov = _build_execution_provenance(agents, config, [result], [], None)
        assert prov["execution_provenance"]["provider_source"] == "none"
        assert prov["execution_provenance"]["transport_source"] == "none"
        assert prov["execution_provenance"]["variant_provider_inference"] is False
        assert prov["execution_provenance"]["config_provider_fallback_used"] is False
        assert prov["execution_provenance"]["result_provider_fallback_used"] is False
        assert prov["execution_provenance"]["result_transport_fallback_used"] is False

    def test_provenance_appears_in_full_summary(self):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", model="gpt-5.5", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", model="gpt-5.5", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert "execution_provenance" in summary
        ep = summary["execution_provenance"]
        assert ep["provider_source"] == "config.provider"
        assert ep["transport_source"] == "explicit_provider_default"
        assert ep["config_provider_fallback_used"] is True


class TestExecutionIdentity:
    """Canonical resolver tests for execution identity."""

    def test_provider_from_variant_prefix(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None, transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="deepseek_base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="deepseek", transport="direct",
        )
        identity = resolve_execution_identity(["deepseek_base_agent"], config, [result])
        assert identity.providers == ["deepseek"]
        assert identity.execution_provenance["provider_source"] == "variant_name_prefix"
        assert identity.execution_provenance["variant_provider_inference"] is True

    def test_provider_from_config(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        assert identity.providers == ["openai"]
        assert identity.execution_provenance["provider_source"] == "config.provider"
        assert identity.execution_provenance["config_provider_fallback_used"] is True

    def test_provider_from_result(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="deepseek",
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        assert identity.providers == ["deepseek"]
        assert identity.execution_provenance["provider_source"] == "result.provider"
        assert identity.execution_provenance["result_provider_fallback_used"] is True

    def test_transport_from_explicit_provider_default(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", transport="direct",
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        assert identity.transport == "direct"
        assert identity.transports == ["direct"]
        assert identity.execution_provenance["transport_source"] == "explicit_provider_default"

    def test_transport_from_result_fallback(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", transport="direct",
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        assert identity.transport == "direct"
        assert identity.transports == ["direct"]
        assert identity.execution_provenance["transport_source"] == "result.transport"
        assert identity.execution_provenance["result_transport_fallback_used"] is True

    def test_no_provider_no_transport_dry_run(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="dry-run", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None, transport=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        assert identity.providers == []
        assert identity.transports == []
        assert identity.transport is None
        assert identity.execution_provenance["provider_source"] == "none"
        assert identity.execution_provenance["transport_source"] == "none"

    def test_consistency_variant_prefix_nonempty_providers(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="openai_base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai",
        )
        identity = resolve_execution_identity(["openai_base_agent"], config, [result])
        assert identity.providers != []
        assert identity.execution_provenance["provider_source"] != "none"

    def test_consistency_empty_providers_source_none(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="dry-run", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        assert identity.providers == []
        assert identity.execution_provenance["provider_source"] == "none"

    def test_consistency_none_transport_source_none(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="dry-run", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
        )
        identity = resolve_execution_identity(["base_agent"], config, [])
        assert identity.transport is None
        assert identity.execution_provenance["transport_source"] == "none"

    def test_consistency_non_none_source_nonempty_providers(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai",
        )
        identity = resolve_execution_identity(["base_agent"], config, [])
        assert identity.providers != []
        assert identity.execution_provenance["provider_source"] != "none"

    def test_consistency_non_none_transport_source_non_none_transport(self):
        config = BenchmarkConfig(
            dataset_path="", agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport="direct",
        )
        identity = resolve_execution_identity(["base_agent"], config, [])
        assert identity.transport is not None
        assert identity.execution_provenance["transport_source"] != "none"

    def test_canonical_summary_consumes_identity(self):
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert summary["providers"] == identity.providers
        assert summary["transport"] == identity.transport
        assert summary["transports"] == identity.transports
        assert summary["execution_provenance"] == identity.execution_provenance


class TestModelRegistry:
    """ModelSpec registry resolves model identity deterministically."""

    def test_known_openai_model_resolves(self):
        spec = resolve_model_spec("openai", "gpt-4.1-mini")
        assert spec is not None
        assert spec.alias == "gpt-4.1-mini"
        assert spec.provider == "openai"
        assert spec.model_id == "gpt-4.1-mini"
        assert spec.api_surface == "chat_completions"
        assert spec.default_transport == "direct"
        assert spec.supports_structured_output is True

    def test_known_openai_gpt5_resolves(self):
        spec = resolve_model_spec("openai", "gpt-5.5")
        assert spec is not None
        assert spec.alias == "gpt-5.5"
        assert spec.provider == "openai"
        assert spec.model_id == "gpt-5.5"
        assert spec.api_surface == "responses"
        assert spec.supports_reasoning is True

    def test_known_deepseek_model_resolves(self):
        spec = resolve_model_spec("deepseek", "deepseek-v4-flash")
        assert spec is not None
        assert spec.alias == "deepseek-v4-flash"
        assert spec.provider == "deepseek"
        assert spec.model_id == "deepseek-v4-flash"
        assert spec.api_surface == "chat_completions"

    def test_unknown_model_alias_returns_none(self):
        spec = resolve_model_spec("openai", "gpt-7-reasoning")
        assert spec is None

    def test_unknown_provider_returns_none(self):
        spec = resolve_model_spec("anthropic", "claude-4")
        assert spec is None

    def test_none_provider_returns_none(self):
        spec = resolve_model_spec(None, "gpt-5.5")
        assert spec is None

    def test_none_model_alias_returns_none(self):
        spec = resolve_model_spec("openai", None)
        assert spec is None

    def test_summary_includes_model_identity_when_resolvable(self):
        from xendris.benchmarking.agentic_programming.scorer import compute_scores
        from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate

        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert "model_identity" in summary
        mi = summary["model_identity"]
        assert mi["resolved"] is True
        assert mi["model_alias"] == "gpt-4.1-mini"
        assert mi["provider"] == "openai"
        assert mi["api_surface"] == "chat_completions"
        assert mi["supports_reasoning"] is False

    def test_summary_model_identity_unresolved_when_unknown_model(self):
        from xendris.benchmarking.agentic_programming.scorer import compute_scores
        from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate

        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", model="unknown-future-model", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", model="unknown-future-model", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert "model_identity" in summary
        mi = summary["model_identity"]
        assert mi["resolved"] is False
        assert mi["model_alias"] == "unknown-future-model"
        assert mi["provider"] == "openai"

    def test_summary_model_identity_unresolved_when_no_provider(self):
        from xendris.benchmarking.agentic_programming.scorer import compute_scores
        from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate

        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="dry-run", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider=None, model=None,
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert "model_identity" in summary
        mi = summary["model_identity"]
        assert mi["resolved"] is False

    def test_model_identity_no_provider_transport_behavior_change(self):
        """Existing ExecutionIdentity tests must still pass unchanged."""
        from xendris.benchmarking.agentic_programming.scorer import compute_scores
        from xendris.benchmarking.agentic_programming.excellence_gate import evaluate_excellence_gate

        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live", output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            provider="openai", model="gpt-5.5", transport="direct",
        )
        result = TaskResult(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
            provider="openai", model="gpt-5.5", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        identity = resolve_execution_identity(["base_agent"], config, [result])
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert summary["providers"] == identity.providers
        assert summary["transport"] == identity.transport
        assert summary["transports"] == identity.transports
        assert summary["execution_provenance"] == identity.execution_provenance
        assert "model_identity" in summary


class TestInterpretationAdmissibility:
    """Interpretation admissibility separates identity resolution from evidence strength."""

    def _make_config(self, **overrides: Any) -> BenchmarkConfig:
        base = dict(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
        )
        base.update(overrides)
        return BenchmarkConfig(**base)

    def _make_result(self, **overrides: Any) -> TaskResult:
        base = dict(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        base.update(overrides)
        return TaskResult(**base)

    def test_explicit_config_provider_direct_transport_admissible(self):
        config = self._make_config(provider="openai", model="gpt-4.1-mini", transport="direct")
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["provider_metadata_sufficient"] is True
        assert ia["transport_metadata_sufficient"] is True
        assert ia["admissible"] is True
        assert ia["limitations"] == []

    def test_variant_prefix_provider_admissible(self):
        config = self._make_config(transport="direct")
        result = self._make_result(
            agent_variant="openai_base_agent",
            provider="openai", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["provider_metadata_sufficient"] is True
        assert ia["transport_metadata_sufficient"] is True
        assert ia["admissible"] is True

    def test_result_level_provider_fallback_not_fully_admissible(self):
        config = self._make_config(transport="direct")
        result = self._make_result(
            provider="openai", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["provider_metadata_sufficient"] is False
        assert ia["admissible"] is False
        assert "provider_metadata_only_resolved_from_result_level" in ia["limitations"]

    def test_result_level_transport_fallback_not_fully_admissible(self):
        config = self._make_config(provider="openai", model="gpt-4.1-mini")
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["transport_metadata_sufficient"] is False
        assert ia["admissible"] is False
        assert "transport_metadata_only_resolved_from_result_level" in ia["limitations"]

    def test_no_provider_no_transport_inadmissible(self):
        config = self._make_config(execution_mode="dry-run")
        result = self._make_result()
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["provider_metadata_sufficient"] is False
        assert ia["transport_metadata_sufficient"] is False
        assert ia["admissible"] is False

    def test_unresolved_model_identity_marks_metadata_sufficient_false(self):
        config = self._make_config(
            provider="openai", model="unknown-future-model", transport="direct",
        )
        result = self._make_result(
            provider="openai", model="unknown-future-model", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["model_metadata_sufficient"] is False
        assert "model_identity_not_resolved" in ia["limitations"]

    def test_resolved_model_identity_marks_metadata_sufficient_true(self):
        config = self._make_config(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["model_metadata_sufficient"] is True

    def test_missing_provider_metadata_blocks_interpretation_admissibility(self):
        """Replaces pre-existing test that relied on transport==None blocking."""
        result = self._make_result(
            agent_variant="openai_base_agent",
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        config = BenchmarkConfig(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
            transport=None,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia = summary["interpretation_admissibility"]
        assert ia["admissible"] is False


class TestEvidenceContract:
    """evidence_contract consolidates all metadata layers into one decision."""

    def _make_config(self, **overrides: Any) -> BenchmarkConfig:
        base = dict(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
        )
        base.update(overrides)
        return BenchmarkConfig(**base)

    def _make_result(self, **overrides: Any) -> TaskResult:
        base = dict(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        base.update(overrides)
        return TaskResult(**base)

    def test_fully_resolved_interpretable(self):
        config = self._make_config(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ec = summary["evidence_contract"]
        assert ec["decision"] == "INTERPRETABLE"
        assert ec["identity_resolved"] is True
        assert ec["provenance_recorded"] is True
        assert ec["model_identity_resolved"] is True
        assert ec["interpretation_admissible"] is True
        assert ec["scoring_complete"] is True

    def test_inadmissible_blocks(self):
        config = self._make_config(execution_mode="dry-run")
        result = self._make_result()
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ec = summary["evidence_contract"]
        assert ec["decision"] == "BLOCKED"
        assert ec["interpretation_admissible"] is False

    def test_result_level_transport_fallback_blocks(self):
        config = self._make_config(provider="openai", model="gpt-4.1-mini")
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ec = summary["evidence_contract"]
        assert ec["decision"] == "BLOCKED"
        assert any("transport" in lim for lim in ec["limitations"])

    def test_unresolved_model_identity_with_admissible_metadata(self):
        config = self._make_config(
            provider="openai", model="unknown-future-model", transport="direct",
        )
        result = self._make_result(
            provider="openai", model="unknown-future-model", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ec = summary["evidence_contract"]
        assert ec["decision"] == "INTERPRETABLE_WITH_LIMITATIONS"
        assert ec["model_identity_resolved"] is False
        assert ec["interpretation_admissible"] is True
        assert any("model_identity" in lim for lim in ec["limitations"])

    def test_missing_scoring_produces_limitation(self):
        config = self._make_config(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ec = summary["evidence_contract"]
        assert ec["scoring_complete"] is True

    def test_evidence_contract_in_summary(self):
        config = self._make_config(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        result = self._make_result(
            provider="openai", model="gpt-4.1-mini", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        assert "evidence_contract" in summary
        assert summary["evidence_contract"]["contract_version"] == "0.1"

    def test_limitations_from_interpretation_admissibility_preserved(self):
        config = self._make_config(provider="openai", model="unknown-future-model")
        result = self._make_result(
            provider="openai", model="unknown-future-model", transport="direct",
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        summary = _build_canonical_summary([result], config, scores, decisions)
        ia_lims = summary["interpretation_admissibility"]["limitations"]
        ec_lims = summary["evidence_contract"]["limitations"]
        for lim in ia_lims:
            assert lim in ec_lims


class TestEvidenceReport:
    """Markdown evidence report converts summary.json into human-readable audit artifact."""

    def _make_config(self, **overrides: Any) -> BenchmarkConfig:
        base = dict(
            dataset_path="benchmarks/agentic_programming/v0_1",
            agent_variants=(),
            execution_mode="live",
            output_dir="/tmp",
            agent_module="", max_concurrent=1, seed=42,
        )
        base.update(overrides)
        return BenchmarkConfig(**base)

    def _make_result(self, **overrides: Any) -> TaskResult:
        base = dict(
            sample_id="T1", agent_variant="base_agent",
            patch_applied=True, visible_tests_passed=False,
            hidden_tests_passed=None, api_contract_preserved=True,
            no_forbidden_files_touched=True, no_false_success_claim=True,
            minimal_patch=None, security_clean=True, iterations_used=1,
            error_message=None, patch_content="",
        )
        base.update(overrides)
        return TaskResult(**base)

    def _build_summary(self, **config_overrides: Any) -> dict:
        config = self._make_config(**config_overrides)
        result = self._make_result(
            provider=config_overrides.get("provider", "openai"),
            model=config_overrides.get("model", "gpt-4.1-mini"),
            transport=config_overrides.get("transport", "direct"),
            latency_ms=100.0, cost_estimate=0.001,
            input_tokens=50, output_tokens=20, total_tokens=70,
            provider_call_attempted=True, provider_call_succeeded=True,
        )
        scores = compute_scores([result])
        decisions = evaluate_excellence_gate(scores)
        return _build_canonical_summary([result], config, scores, decisions)

    def test_interpretable_report_allows_evidence(self):
        summary = self._build_summary(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        report = build_evidence_report_markdown(summary)
        assert "Decision: INTERPRETABLE" in report
        assert "interpretable as evidence" in report

    def test_interpretable_with_limitations_report_warns_disclosure(self):
        summary = self._build_summary(
            provider="openai", model="unknown-future-model", transport="direct",
        )
        report = build_evidence_report_markdown(summary)
        assert "Decision: INTERPRETABLE_WITH_LIMITATIONS" in report
        assert "interpreted with limitations" in report
        assert "must be disclosed" in report

    def test_blocked_report_rejects_evidence(self):
        summary = self._build_summary(execution_mode="dry-run")
        report = build_evidence_report_markdown(summary)
        assert "Decision: BLOCKED" in report
        assert "should not be used as evidence" in report

    def test_report_includes_provider_and_transport_source(self):
        summary = self._build_summary(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        report = build_evidence_report_markdown(summary)
        assert "Provider source: config.provider" in report
        assert "Transport source: explicit_provider_default" in report

    def test_report_includes_model_identity_fields(self):
        summary = self._build_summary(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        report = build_evidence_report_markdown(summary)
        assert "Model ID: gpt-4.1-mini" in report
        assert "API surface: chat_completions" in report

    def test_report_includes_scores_by_variant(self):
        summary = self._build_summary(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        report = build_evidence_report_markdown(summary)
        assert "total_score=" in report
        assert "pass_rate=" in report
        assert "base_agent" in report

    def test_report_is_deterministic(self):
        summary = self._build_summary(
            provider="openai", model="gpt-4.1-mini", transport="direct",
        )
        report1 = build_evidence_report_markdown(summary)
        report2 = build_evidence_report_markdown(summary)
        assert report1 == report2
