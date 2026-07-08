"""Tests for Finitexo Code Matrix v0.6.0 controlled run n=30."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from benchmarks.finitexo_code_matrix_v0_6.real_provider_controlled_run import (
    BLOCKED_BUDGET,
    BLOCKED_PREFLIGHT,
    COMPLETED,
    ControlledProviderSpec,
    ControlledRunConfig,
    PARTIAL,
    ProviderAggregate,
    ScoredRecord,
    aggregate_by_provider,
    build_controlled_run_report,
    compute_overall_mean,
    evaluate_controlled_run_preflight,
    score_provider_responses,
    score_response,
    validate_run_id_suffix,
    write_controlled_run_artifacts,
    run_controlled_provider_benchmark,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def _dataset(tmp_path: Path, count: int = 30,
             dataset_hash: str = "ds-hash", manifest_hash: str = "mf-hash") -> Path:
    root = tmp_path / "dataset"
    _write_json(root / "dataset_hashes.json", {"dataset_hash": dataset_hash, "manifest_hash": manifest_hash})
    _write_json(root / "dataset_manifest.json", {"dataset_name": "test_n30", "dataset_version": "0.6.0"})
    for i in range(1, count + 1):
        _write_json(
            root / "tasks" / f"task_{i:03d}.json",
            {
                "task_id": f"t{i:03d}",
                "task_version": "0.6.0",
                "content_hash": f"ch{i:03d}",
                "prompt": "Return a diagnostic answer.",
            },
        )
    return root


def _ready(tmp_path: Path, ready: bool = True) -> Path:
    p = tmp_path / "v057.json"
    _write_json(p, {
        "final_decision": "REAL_PROVIDER_REPORT_ADMISSIBILITY_APPROVED_DIAGNOSTIC_ONLY" if ready else "BLOCKED",
        "ready_for_v0_6_0_controlled_run": ready,
    })
    return p


def _config(tmp_path: Path, task_count: int = 30, ready: bool = True,
            budget: float = 0.50, overwrite: bool = True) -> ControlledRunConfig:
    return ControlledRunConfig(
        dataset_path=_dataset(tmp_path, count=task_count),
        readiness_summary_path=_ready(tmp_path, ready=ready),
        output_dir=tmp_path / "out",
        providers=(
            ControlledProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, "unused"),
            ControlledProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, "unused"),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        budget_cap_usd=budget,
        allow_overwrite=overwrite,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )


class _StubResult:
    def __init__(self, task, provider):
        self.raw_response_text = f"{task['task_id']} diagnostic response preserves contract."
        self.normalized_response_text = self.raw_response_text
        self.estimated_cost_usd = provider.estimated_cost_per_task_usd
        self.provider_reported_model = provider.model_name
        self.prompt_tokens = 10
        self.completion_tokens = 20
        self.total_tokens = 30


def _stub_adapter(provider, task, config):
    return _StubResult(task, provider)


# ---------------------------------------------------------------------------
# Config defaults
# ---------------------------------------------------------------------------

def test_config_defaults():
    config = ControlledRunConfig()
    assert config.run_id == "finitexo_v0_6_0_real_provider_controlled_run_n30"
    assert config.provider_mode == "real"
    assert config.budget_cap_usd == 0.50
    assert config.expected_task_count == 30
    assert config.allow_mock_fallback is False
    assert config.temperature == 0.0
    assert len(config.providers) == 2


def test_config_dataset_path_points_to_v0_6_n30():
    config = ControlledRunConfig()
    assert "v0_6" in str(config.dataset_path)
    assert "controlled_run_n30" in str(config.dataset_path)
    assert "v0_4_3" not in str(config.dataset_path)


def test_config_has_v0_6_0_dataset_hashes():
    config = ControlledRunConfig()
    assert config.expected_dataset_hash == "04758231d91333a3785693b05587740f27fa7b05a2d3e77c42a73fbd3184f010"
    assert config.expected_manifest_hash == "073d3982c2fe79fdf59822e6c75585d61f6274b684396d67dfcaa94b159b8519"


def test_config_expected_task_count_and_attempts():
    config = ControlledRunConfig()
    assert config.expected_task_count == 30
    assert len(config.providers) == 2
    expected_attempts = config.expected_task_count * len(config.providers)
    assert expected_attempts == 60


# ---------------------------------------------------------------------------
# Preflight gate
# ---------------------------------------------------------------------------

def test_preflight_blocks_if_readiness_summary_missing(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, readiness_summary_path=tmp_path / "missing.json")
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "missing_v0_5_7_readiness_summary" in pf.blockers


def test_preflight_blocks_if_readiness_not_ready(tmp_path):
    cfg = _config(tmp_path, ready=False)
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "v0_5_7_not_ready_for_v0_6_0" in pf.blockers


def test_preflight_blocks_if_confirmation_missing(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"})
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "missing_explicit_execution_confirmation" in pf.blockers


def test_preflight_blocks_if_api_key_missing(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert any("missing_provider_key" in b for b in pf.blockers)


def test_preflight_blocks_dataset_count_mismatch(tmp_path):
    cfg = _config(tmp_path, task_count=10)
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 10)
    assert pf.can_execute is False
    assert "insufficient_tasks" in pf.blockers


def test_preflight_blocks_output_dir_not_empty(tmp_path):
    cfg = _config(tmp_path, overwrite=False)
    (tmp_path / "out").mkdir(parents=True, exist_ok=True)
    (tmp_path / "out" / "stale.txt").write_text("stale", encoding="utf-8")
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


def test_preflight_blocks_if_mode_not_real(tmp_path):
    cfg = replace(_config(tmp_path), provider_mode="mock")
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "provider_mode_not_real" in pf.blockers


def test_preflight_passes_with_all_conditions(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is True
    assert pf.decision == "CONTROLLED_RUN_PREFLIGHT_READY"
    assert pf.task_attempts_expected == 60
    assert pf.task_count == 30


def test_preflight_blocks_task_count_10_regression(tmp_path):
    """Regression: v0.6.0 must reject n=10 (the v0.4.3 size)."""
    cfg = _config(tmp_path, task_count=10)
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 10)
    assert pf.can_execute is False
    assert "insufficient_tasks" in pf.blockers
    assert pf.task_count == 10


def test_preflight_reports_v0_6_0_dataset_hash_when_mismatched(tmp_path):
    """Preflight should detect when dataset hash doesn't match v0.6.0 expected hash."""
    cfg = _config(tmp_path, task_count=30)
    pf = evaluate_controlled_run_preflight(cfg, "WRONG-HASH", "mf-hash", 30)
    assert pf.can_execute is False
    assert "dataset_hash_mismatch" in pf.blockers


def test_preflight_reports_correct_v0_6_hash_when_passing(tmp_path):
    """When preflight passes, verify the reported hash values are v0.6.0-compatible."""
    cfg = _config(tmp_path, task_count=30)
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is True
    assert pf.dataset_hash == "ds-hash"
    assert pf.manifest_hash == "mf-hash"


def test_preflight_blocks_hash_mismatch_with_default_config(tmp_path):
    """With real v0.6.0 config defaults, wrong hash blocks preflight."""
    ds = _dataset(tmp_path, count=30, dataset_hash="WRONG", manifest_hash="mf-hash")
    ready = _ready(tmp_path)
    cfg = ControlledRunConfig(
        dataset_path=ds,
        readiness_summary_path=ready,
        output_dir=tmp_path / "out_hash",
        expected_dataset_hash="04758231d91333a3785693b05587740f27fa7b05a2d3e77c42a73fbd3184f010",
        expected_manifest_hash="073d3982c2fe79fdf59822e6c75585d61f6274b684396d67dfcaa94b159b8519",
        allow_overwrite=True,
        environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true", "DEEPSEEK_API_KEY": "x", "OPENAI_API_KEY": "x"},
    )
    pf = evaluate_controlled_run_preflight(cfg, "WRONG", "mf-hash", 30)
    assert pf.can_execute is False
    assert "dataset_hash_mismatch" in pf.blockers


# ---------------------------------------------------------------------------
# Run ID suffix — validate_run_id_suffix
# ---------------------------------------------------------------------------

def test_suffix_accepts_valid_strings():
    assert validate_run_id_suffix("live_20260708_01") == "live_20260708_01"
    assert validate_run_id_suffix("test-run-42") == "test-run-42"
    assert validate_run_id_suffix("A_B_C") == "A_B_C"


def test_suffix_rejects_slash():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_run_id_suffix("live/2026")


def test_suffix_rejects_backslash():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_run_id_suffix("live\\2026")


def test_suffix_rejects_dot_dot():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_run_id_suffix("..")


def test_suffix_rejects_whitespace():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_run_id_suffix("live 2026")


def test_suffix_rejects_empty_string():
    with pytest.raises(ValueError, match="must not be empty"):
        validate_run_id_suffix("")


# ---------------------------------------------------------------------------
# Run ID suffix — with_run_id_suffix
# ---------------------------------------------------------------------------

def test_default_config_uses_canonical_output_dir():
    config = ControlledRunConfig()
    assert config.run_id == "finitexo_v0_6_0_real_provider_controlled_run_n30"
    assert "finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30" in str(config.output_dir)


def test_suffix_config_uses_different_output_dir():
    config = ControlledRunConfig()
    suffixed = config.with_run_id_suffix("live_20260708_01")
    assert suffixed.output_dir != config.output_dir
    assert "live_20260708_01" in str(suffixed.output_dir)
    assert suffixed.output_dir.name == config.output_dir.name + "_live_20260708_01"


def test_suffix_config_run_id_includes_suffix():
    config = ControlledRunConfig()
    suffixed = config.with_run_id_suffix("live_20260708_01")
    assert suffixed.run_id == "finitexo_v0_6_0_real_provider_controlled_run_n30_live_20260708_01"


def test_suffix_does_not_mutate_original_config():
    config = ControlledRunConfig()
    original_run_id = config.run_id
    original_dir = config.output_dir
    _ = config.with_run_id_suffix("some_suffix")
    assert config.run_id == original_run_id
    assert config.output_dir == original_dir


# ---------------------------------------------------------------------------
# Run ID suffix — preflight blocks canonical dir when non-empty
# ---------------------------------------------------------------------------

def test_preflight_blocks_canonical_dir_when_non_empty(tmp_path):
    """Simulate the real situation: canonical output dir exists and is non-empty."""
    canonical = tmp_path / "canonical_out"
    canonical.mkdir(parents=True, exist_ok=True)
    (canonical / "historical_artifact.json").write_text("{}", encoding="utf-8")
    cfg = _config(tmp_path, overwrite=False)
    cfg = replace(cfg, output_dir=canonical)
    pf = evaluate_controlled_run_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


def test_suffix_output_dir_avoids_collision(tmp_path):
    """With a suffix, output_dir is unique and preflight passes."""
    canonical = tmp_path / "canonical_out"
    canonical.mkdir(parents=True, exist_ok=True)
    (canonical / "historical_artifact.json").write_text("{}", encoding="utf-8")
    config = ControlledRunConfig(
        dataset_path=_dataset(tmp_path, count=30),
        readiness_summary_path=_ready(tmp_path),
        output_dir=canonical,
        providers=(
            ControlledProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, "unused"),
            ControlledProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, "unused"),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        allow_overwrite=False,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    suffixed = config.with_run_id_suffix("live_test")
    pf = evaluate_controlled_run_preflight(suffixed, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is True
    assert pf.decision == "CONTROLLED_RUN_PREFLIGHT_READY"


# ---------------------------------------------------------------------------
# Scorer — range 0..1
# ---------------------------------------------------------------------------

def test_scorer_range():
    r = score_response("")
    assert 0.0 <= r.score_total <= 1.0
    r = score_response("A" * 5000)
    assert 0.0 <= r.score_total <= 1.0
    r = score_response("normal response with contract mention" * 20)
    assert 0.0 <= r.score_total <= 1.0


def test_scorer_empty_response():
    r = score_response("")
    assert r.score_components["response_present"] == 0.0
    assert r.verified_success is False


def test_scorer_full_response():
    r = score_response("Fix helper. Returns normalized string. API contract preserved. No secrets. No errors. Limitations: diagnostic only.")
    assert r.score_components["response_present"] == 1.0
    assert r.score_components["no_secret_exposure"] == 1.0
    assert r.score_components["security_clean"] == 1.0
    assert r.verified_success is True


def test_scorer_secret_exposure():
    r = score_response("sk-proj-fake")
    assert r.score_components["no_secret_exposure"] == 0.0
    assert r.verified_success is False


def test_scorer_false_success_claim():
    r = score_response("all tests pass perfectly")
    assert r.score_components["no_false_success_claim"] == 0.0


def test_scorer_all_components_present():
    r = score_response("Fix helper. Returns normalized string. API contract preserved. No secrets. No errors. Limitations: diagnostic only.")
    for comp in ["response_present", "no_secret_exposure", "security_clean",
                  "no_runtime_error", "no_false_success_claim", "no_refusal_without_reason"]:
        assert r.score_components.get(comp, -1) >= 0, f"{comp} failed"


# ---------------------------------------------------------------------------
# Scorer — provider symmetry
# ---------------------------------------------------------------------------

def test_scorer_provider_independent():
    r1 = score_response("diagnostic response for deepseek")
    r2 = score_response("diagnostic response for openai")
    assert r1.score_total == r2.score_total


# ---------------------------------------------------------------------------
# score_provider_responses
# ---------------------------------------------------------------------------

def test_score_provider_responses():
    records = [
        {"provider_name": "deepseek", "model_name": "m", "task_id": "t1",
         "response_text": "diagnostic answer preserves contract."},
        {"provider_name": "openai", "model_name": "m", "task_id": "t1",
         "response_text": "diagnostic answer preserves contract."},
    ]
    scored = score_provider_responses(records)
    assert len(scored) == 2
    for s in scored:
        assert 0.0 <= s.score_total <= 1.0
        assert s.provider_name in ("deepseek", "openai")


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def test_aggregate_by_provider():
    recs = [
        ScoredRecord("deepseek", "m", "t1", 0.8, {"a": 0.8}, True, None, None),
        ScoredRecord("deepseek", "m", "t2", 0.9, {"a": 0.9}, True, None, None),
        ScoredRecord("openai", "m", "t1", 0.7, {"a": 0.7}, True, None, None),
    ]
    aggs = aggregate_by_provider(recs)
    assert len(aggs) == 2
    ds = [a for a in aggs if a.provider_name == "deepseek"][0]
    assert ds.mean_score == 0.85
    assert ds.task_count == 2


def test_overall_mean():
    aggs = [
        ProviderAggregate("deepseek", 10, 0.8, {"a": 0.8}, 0.7, 0.9, 8),
        ProviderAggregate("openai", 10, 0.7, {"a": 0.7}, 0.6, 0.8, 7),
    ]
    m = compute_overall_mean(aggs)
    assert m == 0.75


def test_aggregate_verified_count():
    recs = [
        ScoredRecord("deepseek", "m", "t1", 0.9, {"a": 0.9}, True, None, None),
        ScoredRecord("deepseek", "m", "t2", 0.3, {"a": 0.3}, False, None, None),
    ]
    aggs = aggregate_by_provider(recs)
    ds = [a for a in aggs if a.provider_name == "deepseek"][0]
    assert ds.verified_count == 1


# ---------------------------------------------------------------------------
# Report — contains prohibited-claim guardrails
# ---------------------------------------------------------------------------

def test_report_contains_prohibited_claims(tmp_path):
    cfg = _config(tmp_path)
    result = run_controlled_provider_benchmark(cfg, adapter=_stub_adapter, skip_dataset_load=True,
                                                preloaded_dataset={
                                                    "dataset_name": "t", "dataset_version": "1",
                                                    "dataset_hash": "ds-hash", "manifest_hash": "mf-hash",
                                                    "tasks": [{"task_id": f"t{i:03d}", "task_version": "1",
                                                               "content_hash": f"ch{i:03d}", "prompt": "test"}
                                                              for i in range(1, 31)],
                                                })
    summary = write_controlled_run_artifacts(result)
    report = (cfg.output_dir / "report.md").read_text(encoding="utf-8")
    assert "does not prove model superiority" in report.lower()
    assert "no statistical" in report.lower()
    assert "no superiority claim" in report.lower()


# ---------------------------------------------------------------------------
# Summary — contains authorized_claims and prohibited_claims
# ---------------------------------------------------------------------------

def test_summary_contains_authorized_prohibited_claims(tmp_path):
    cfg = _config(tmp_path)
    result = run_controlled_provider_benchmark(cfg, adapter=_stub_adapter, skip_dataset_load=True,
                                                preloaded_dataset={
                                                    "dataset_name": "t", "dataset_version": "1",
                                                    "dataset_hash": "ds-hash", "manifest_hash": "mf-hash",
                                                    "tasks": [{"task_id": f"t{i:03d}", "task_version": "1",
                                                               "content_hash": f"ch{i:03d}", "prompt": "test"}
                                                              for i in range(1, 31)],
                                                })
    summary = write_controlled_run_artifacts(result)
    assert "authorized_claims" in summary
    assert "prohibited_claims" in summary
    assert len(summary["authorized_claims"]) > 0
    assert len(summary["prohibited_claims"]) > 0
    assert any("broad superiority" in c for c in summary["authorized_claims"])
    assert any("model superiority" in c.lower() for c in summary["prohibited_claims"])


# ---------------------------------------------------------------------------
# Budget block behavior
# ---------------------------------------------------------------------------

def test_budget_block_when_exceeded(tmp_path):
    cfg = _config(tmp_path, budget=0.00001)
    result = run_controlled_provider_benchmark(cfg, adapter=_stub_adapter, skip_dataset_load=True,
                                                preloaded_dataset={
                                                    "dataset_name": "t", "dataset_version": "1",
                                                    "dataset_hash": "ds-hash", "manifest_hash": "mf-hash",
                                                    "tasks": [{"task_id": f"t{i:03d}", "task_version": "1",
                                                               "content_hash": f"ch{i:03d}", "prompt": "test"}
                                                              for i in range(1, 31)],
                                                })
    assert result["summary"]["final_decision"] in (BLOCKED_BUDGET, PARTIAL)
    assert result["summary"]["budget_decision"] in ("BUDGET_EXHAUSTED", "BLOCKED")


# ---------------------------------------------------------------------------
# Artifact path creation
# ---------------------------------------------------------------------------

def test_artifacts_created(tmp_path):
    cfg = _config(tmp_path)
    result = run_controlled_provider_benchmark(cfg, adapter=_stub_adapter, skip_dataset_load=True,
                                                preloaded_dataset={
                                                    "dataset_name": "t", "dataset_version": "1",
                                                    "dataset_hash": "ds-hash", "manifest_hash": "mf-hash",
                                                    "tasks": [{"task_id": f"t{i:03d}", "task_version": "1",
                                                               "content_hash": f"ch{i:03d}", "prompt": "test"}
                                                              for i in range(1, 31)],
                                                })
    summary = write_controlled_run_artifacts(result)
    out = cfg.output_dir
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()
    assert (out / "responses.jsonl").exists()
    assert (out / "scores.jsonl").exists()
    assert (out / "costs.json").exists()
    assert (out / "errors.jsonl").exists()
    assert (out / "metadata.jsonl").exists()
    assert (out / "preflight.json").exists()
    assert (out / "gate.json").exists()


# ---------------------------------------------------------------------------
# Runner — full path with real dataset
# ---------------------------------------------------------------------------

def test_runner_completes_with_real_dataset(tmp_path):
    ds = _dataset(tmp_path, count=30, dataset_hash="ds-hash", manifest_hash="mf-hash")
    ready = _ready(tmp_path)
    cfg = ControlledRunConfig(
        dataset_path=ds,
        readiness_summary_path=ready,
        output_dir=tmp_path / "out2",
        providers=(
            ControlledProviderSpec("deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, "unused"),
            ControlledProviderSpec("openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, "unused"),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
    )
    result = run_controlled_provider_benchmark(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] == COMPLETED
    assert result["summary"]["total_expected"] == 60
    assert result["summary"]["total_completed"] == 60
    assert result["summary"]["total_cost_usd"] > 0
    assert result["summary"]["mean_score_overall"] > 0
    summary = write_controlled_run_artifacts(result)
    assert summary["final_decision"] == COMPLETED
    assert len(summary["aggregates"]) == 2
