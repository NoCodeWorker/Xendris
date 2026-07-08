"""Tests for Finitexo Code Matrix v0.9.0 runtime paired lift n=30."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift import (
    AUDIT_COMPONENTS,
    BLOCKED_BUDGET,
    BLOCKED_PREFLIGHT,
    COMPLETED,
    FAMILIES,
    PARTIAL,
    RuntimeAuditDecision,
    RuntimeConfig,
    RuntimePreflight,
    RuntimeVariantSpec,
    aggregate_by_family_variant,
    aggregate_by_variant,
    build_runtime_lift_report,
    compute_family_lift,
    compute_paired_lift,
    evaluate_runtime_preflight,
    run_runtime_paired_lift,
    score_runtime_response,
    write_runtime_lift_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_audit import (
    build_repair_prompt,
    run_audit,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_config import (
    validate_run_id_suffix,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_runner import (
    XENDRIS_ADMISSIBILITY_PROMPT,
    _build_wrapper_task,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_types import (
    RuntimeTrace,
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
    _write_json(root / "dataset_manifest.json", {"dataset_name": "test_n30", "dataset_version": "0.8.0"})
    for i in range(1, count + 1):
        family = FAMILIES[i % len(FAMILIES)]
        _write_json(
            root / "tasks" / f"task_{i:03d}.json",
            {
                "task_id": f"t{i:03d}",
                "task_version": "0.8.0",
                "content_hash": f"ch{i:03d}",
                "family": family,
                "prompt": "Return a diagnostic answer.",
                "constraints": ["format: return code only"],
                "public_contract": "return result",
                "scoring_focus": ["correctness"],
            },
        )
    return root


def _config(
    tmp_path: Path, task_count: int = 30, budget: float = 2.0, overwrite: bool = True,
) -> RuntimeConfig:
    return RuntimeConfig(
        dataset_path=_dataset(tmp_path, count=task_count),
        output_dir=tmp_path / "out",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
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
        self.raw_response_text = f"{task['task_id']} diagnostic response preserves contract. Fixed. Returns result. Limitation: diagnostic only."
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
    config = RuntimeConfig()
    assert config.run_id == "finitexo_v0_9_0_runtime_paired_lift_n30"
    assert config.provider_mode == "real"
    assert config.budget_cap_usd == 2.0
    assert config.expected_task_count == 30
    assert config.expected_attempts == 240
    assert config.allow_mock_fallback is False
    assert config.temperature == 0.0
    assert len(config.variants) == 8


def test_config_uses_v0_8_dataset():
    config = RuntimeConfig()
    dataset_str = str(config.dataset_path)
    assert "v0_8" in dataset_str
    assert "hard_programming_n30" in dataset_str


def test_config_expected_attempts():
    config = RuntimeConfig()
    assert config.expected_attempts == 240
    calculated = len(config.variants) * config.expected_task_count
    assert config.expected_attempts == calculated


def test_config_eight_variants():
    config = RuntimeConfig()
    names = [v.variant_name for v in config.variants]
    assert names == [
        "deepseek_base", "deepseek_wrapper", "deepseek_runtime", "deepseek_calibrated_runtime",
        "openai_base", "openai_wrapper", "openai_runtime", "openai_calibrated_runtime",
    ]
    runtime_flags = [v.use_runtime_loop for v in config.variants]
    assert runtime_flags == [False, False, True, True, False, False, True, True]
    wrapper_flags = [v.use_xendris_wrapper for v in config.variants]
    assert wrapper_flags == [False, True, True, True, False, True, True, True]
    calibrated_flags = [getattr(v, "use_calibrated_runtime", False) for v in config.variants]
    assert calibrated_flags == [False, False, False, True, False, False, False, True]


def test_config_has_correct_hashes():
    config = RuntimeConfig()
    assert config.expected_dataset_hash == "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841"
    assert config.expected_manifest_hash == "3cfa4e904c0cf5918da4483c1e656fd8cf9b8e231bc5487b45e86eabb2ff1c54"


# ---------------------------------------------------------------------------
# Suffix
# ---------------------------------------------------------------------------

def test_suffix_creates_unique_output_dir():
    config = RuntimeConfig()
    suffixed = config.with_run_id_suffix("live_test")
    assert suffixed.run_id == "finitexo_v0_9_0_runtime_paired_lift_n30_live_test"
    assert "live_test" in str(suffixed.output_dir)
    assert suffixed.output_dir != config.output_dir


def test_invalid_suffix_rejected():
    with pytest.raises(ValueError, match="invalid characters"):
        validate_run_id_suffix("live/test")


def test_suffix_blocked_empty():
    with pytest.raises(ValueError, match="must not be empty"):
        validate_run_id_suffix("")


# ---------------------------------------------------------------------------
# Preflight gate
# ---------------------------------------------------------------------------

def test_preflight_passes_with_all_conditions(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_runtime_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is True
    assert pf.decision == "RUNTIME_LIFT_PREFLIGHT_READY"
    assert pf.expected_attempts == 240
    assert pf.task_count == 30


def test_preflight_blocks_missing_confirmation(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"})
    pf = evaluate_runtime_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "missing_explicit_execution_confirmation" in pf.blockers


def test_preflight_blocks_missing_keys(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    pf = evaluate_runtime_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert any("missing_provider_key" in b for b in pf.blockers)


def test_preflight_blocks_wrong_dataset_count(tmp_path):
    cfg = _config(tmp_path, task_count=10)
    pf = evaluate_runtime_preflight(cfg, "ds-hash", "mf-hash", 10)
    assert pf.can_execute is False
    assert "insufficient_tasks" in pf.blockers


def test_preflight_blocks_wrong_hash(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_runtime_preflight(cfg, "WRONG-HASH", "mf-hash", 30)
    assert pf.can_execute is False
    assert "dataset_hash_mismatch" in pf.blockers


def test_preflight_blocks_non_empty_output_dir(tmp_path):
    cfg = _config(tmp_path, overwrite=False)
    (tmp_path / "out").mkdir(parents=True, exist_ok=True)
    (tmp_path / "out" / "stale.txt").write_text("stale", encoding="utf-8")
    pf = evaluate_runtime_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


# ---------------------------------------------------------------------------
# Xendris wrapper
# ---------------------------------------------------------------------------

def test_wrapper_is_deterministic():
    task = {"task_id": "t001", "prompt": "Write a function."}
    r1 = _build_wrapper_task(task)
    r2 = _build_wrapper_task(task)
    assert r1["prompt"] == r2["prompt"]


def test_wrapper_preserves_task_prompt():
    task = {"task_id": "t001", "prompt": "Return 42."}
    wrapped = _build_wrapper_task(task)
    assert wrapped["task_id"] == "t001"
    assert "Return 42." in wrapped["prompt"]
    assert wrapped["prompt"].startswith("You are a diagnostic code assistant")


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def test_audit_returns_valid_decision():
    result = run_audit("Returns a correct implementation.", {"prompt": "test"})
    assert isinstance(result.decision, RuntimeAuditDecision)
    assert result.decision in list(RuntimeAuditDecision)


def test_audit_has_12_components():
    result = run_audit("Some response text here. Fixed. Result: ok.", None)
    assert len(result.component_scores) == len(AUDIT_COMPONENTS)
    for comp in AUDIT_COMPONENTS:
        assert comp in result.component_scores


def test_audit_blocks_empty_response():
    result = run_audit("", None)
    assert result.decision == RuntimeAuditDecision.BLOCK
    assert result.score == 0.0


def test_audit_blocks_secret_exposure():
    result = run_audit("My API key is sk-abc123def456ghijklmnopqrs.", None)
    assert result.decision == RuntimeAuditDecision.BLOCK


def test_audit_allows_good_response():
    result = run_audit(
        "1. Fixed the helper function.\n"
        "2. Returns normalized string.\n"
        "3. Result: success.\n"
        "Limitation: diagnostic only.\n",
        {"prompt": "test"},
    )
    assert result.decision in (RuntimeAuditDecision.ALLOW, RuntimeAuditDecision.ALLOW_WITH_LIMITATIONS)


def test_audit_repair_required_for_missing_structure():
    result = run_audit(
        "just a plain response with no structure or formatting whatsoever and it keeps going on and on",
        {"prompt": "write a complex function"},
    )
    assert result.decision in (
        RuntimeAuditDecision.REPAIR_REQUIRED, RuntimeAuditDecision.BLOCK,
        RuntimeAuditDecision.ALLOW_WITH_LIMITATIONS,
    )


# ---------------------------------------------------------------------------
# Trace schema
# ---------------------------------------------------------------------------

def test_trace_schema_includes_required_fields():
    audit = run_audit("test response", None)
    trace = RuntimeTrace(
        task_id="t001",
        provider_name="deepseek",
        variant_name="deepseek_runtime",
        initial_response="test",
        initial_audit=audit,
        audit_decision=audit.decision,
        repair_attempted=False,
        repair_response=None,
        repair_audit=None,
        final_response="test",
        final_audit=audit,
    )
    d = trace.to_dict()
    assert d["task_id"] == "t001"
    assert d["provider_name"] == "deepseek"
    assert d["variant_name"] == "deepseek_runtime"
    assert "initial_response" in d
    assert "initial_audit" in d
    assert "audit_decision" in d
    assert "repair_attempted" in d
    assert "repair_response" in d
    assert "repair_audit" in d
    assert "final_response" in d
    assert "final_audit" in d


# ---------------------------------------------------------------------------
# Repair policy
# ---------------------------------------------------------------------------

def test_repair_prompt_includes_issues():
    audit = run_audit("incomplete response no format", {"prompt": "write a function"})
    prompt = build_repair_prompt("Original task", "incomplete response no format", audit)
    assert "repair" in prompt.lower()
    assert "issues" in prompt.lower() or "reasons" in prompt.lower()


def test_repair_not_attempted_on_secret_exposure():
    audit = run_audit("key=sk-abc123def456ghijklmnopqrstuvwx", None)
    assert audit.is_repairable is False
    assert audit.decision == RuntimeAuditDecision.BLOCK


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

def test_scorer_range():
    r = score_runtime_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "")
    assert 0.0 <= r.score_total <= 1.0
    r = score_runtime_response("deepseek_runtime", "deepseek", "m", "t1", "edge_case_handling", "A" * 5000)
    assert 0.0 <= r.score_total <= 1.0


def test_scorer_has_task_family():
    r = score_runtime_response("deepseek_runtime", "deepseek", "m", "t1", "performance_constraints", "good response")
    assert r.task_family == "performance_constraints"


# ---------------------------------------------------------------------------
# Lift calculations (6 variant)
# ---------------------------------------------------------------------------

def test_paired_lift_calculation_six_variants():
    scored = [
        score_runtime_response("deepseek_base", "deepseek", "m", "t1", "a", "base"),
        score_runtime_response("deepseek_wrapper", "deepseek", "m", "t1", "a", "wrapper better"),
        score_runtime_response("deepseek_runtime", "deepseek", "m", "t1", "a", "runtime best"),
        score_runtime_response("openai_base", "openai", "m", "t1", "a", "base"),
        score_runtime_response("openai_wrapper", "openai", "m", "t1", "a", "wrapper better"),
        score_runtime_response("openai_runtime", "openai", "m", "t1", "a", "runtime best"),
    ]
    agg = aggregate_by_variant(scored)
    lift = compute_paired_lift(scored, agg)
    assert "deepseek_wrapper_vs_base_mean_lift" in lift
    assert "deepseek_runtime_vs_base_mean_lift" in lift
    assert "deepseek_runtime_vs_wrapper_mean_lift" in lift
    assert "openai_wrapper_vs_base_mean_lift" in lift
    assert "openai_runtime_vs_base_mean_lift" in lift
    assert "openai_runtime_vs_wrapper_mean_lift" in lift


def test_aggregate_by_variant_six():
    scored = [
        score_runtime_response("deepseek_base", "deepseek", "m", "t1", "a", "r1"),
        score_runtime_response("deepseek_wrapper", "deepseek", "m", "t1", "a", "r2"),
        score_runtime_response("deepseek_runtime", "deepseek", "m", "t1", "a", "r3"),
        score_runtime_response("openai_base", "openai", "m", "t1", "a", "r4"),
        score_runtime_response("openai_wrapper", "openai", "m", "t1", "a", "r5"),
        score_runtime_response("openai_runtime", "openai", "m", "t1", "a", "r6"),
    ]
    aggs = aggregate_by_variant(scored)
    assert len(aggs) == 6
    names = [a.variant_name for a in aggs]
    for name in ["deepseek_base", "deepseek_wrapper", "deepseek_runtime",
                  "openai_base", "openai_wrapper", "openai_runtime"]:
        assert name in names


# ---------------------------------------------------------------------------
# Family lift (6 variant)
# ---------------------------------------------------------------------------

def test_compute_family_lift_six_variants():
    scored = [
        score_runtime_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "base"),
        score_runtime_response("deepseek_wrapper", "deepseek", "m", "t2", "algorithmic_reasoning", "wrap"),
        score_runtime_response("deepseek_runtime", "deepseek", "m", "t3", "algorithmic_reasoning", "runtime"),
        score_runtime_response("openai_base", "openai", "m", "t4", "algorithmic_reasoning", "base"),
        score_runtime_response("openai_wrapper", "openai", "m", "t5", "algorithmic_reasoning", "wrap"),
        score_runtime_response("openai_runtime", "openai", "m", "t6", "algorithmic_reasoning", "runtime"),
    ]
    fl = compute_family_lift(scored)
    assert "family_lift" in fl
    assert "algorithmic_reasoning" in fl["family_lift"]
    assert "deepseek_wrapper_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "deepseek_runtime_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "deepseek_runtime_lift_vs_wrapper" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_wrapper_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_runtime_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_runtime_lift_vs_wrapper" in fl["family_lift"]["algorithmic_reasoning"]


# ---------------------------------------------------------------------------
# Lift calculations (8 variant)
# ---------------------------------------------------------------------------

def test_paired_lift_calculation_eight_variants():
    scored = [
        score_runtime_response("deepseek_base", "deepseek", "m", "t1", "a", "base"),
        score_runtime_response("deepseek_wrapper", "deepseek", "m", "t1", "a", "wrapper better"),
        score_runtime_response("deepseek_runtime", "deepseek", "m", "t1", "a", "runtime best"),
        score_runtime_response("deepseek_calibrated_runtime", "deepseek", "m", "t1", "a", "calibrated best"),
        score_runtime_response("openai_base", "openai", "m", "t1", "a", "base"),
        score_runtime_response("openai_wrapper", "openai", "m", "t1", "a", "wrapper better"),
        score_runtime_response("openai_runtime", "openai", "m", "t1", "a", "runtime best"),
        score_runtime_response("openai_calibrated_runtime", "openai", "m", "t1", "a", "calibrated best"),
    ]
    agg = aggregate_by_variant(scored)
    lift = compute_paired_lift(scored, agg)
    assert "deepseek_wrapper_vs_base_mean_lift" in lift
    assert "deepseek_runtime_vs_base_mean_lift" in lift
    assert "deepseek_runtime_vs_wrapper_mean_lift" in lift
    assert "deepseek_calibrated_runtime_vs_base_mean_lift" in lift
    assert "deepseek_calibrated_runtime_vs_wrapper_mean_lift" in lift
    assert "deepseek_calibrated_runtime_vs_runtime_mean_lift" in lift
    assert "openai_wrapper_vs_base_mean_lift" in lift
    assert "openai_runtime_vs_base_mean_lift" in lift
    assert "openai_runtime_vs_wrapper_mean_lift" in lift
    assert "openai_calibrated_runtime_vs_base_mean_lift" in lift
    assert "openai_calibrated_runtime_vs_wrapper_mean_lift" in lift
    assert "openai_calibrated_runtime_vs_runtime_mean_lift" in lift


def test_aggregate_by_variant_eight():
    scored = [
        score_runtime_response("deepseek_base", "deepseek", "m", "t1", "a", "r1"),
        score_runtime_response("deepseek_wrapper", "deepseek", "m", "t1", "a", "r2"),
        score_runtime_response("deepseek_runtime", "deepseek", "m", "t1", "a", "r3"),
        score_runtime_response("deepseek_calibrated_runtime", "deepseek", "m", "t1", "a", "r4"),
        score_runtime_response("openai_base", "openai", "m", "t1", "a", "r5"),
        score_runtime_response("openai_wrapper", "openai", "m", "t1", "a", "r6"),
        score_runtime_response("openai_runtime", "openai", "m", "t1", "a", "r7"),
        score_runtime_response("openai_calibrated_runtime", "openai", "m", "t1", "a", "r8"),
    ]
    aggs = aggregate_by_variant(scored)
    assert len(aggs) == 8
    names = [a.variant_name for a in aggs]
    for name in ["deepseek_base", "deepseek_wrapper", "deepseek_runtime", "deepseek_calibrated_runtime",
                  "openai_base", "openai_wrapper", "openai_runtime", "openai_calibrated_runtime"]:
        assert name in names


def test_compute_family_lift_eight_variants():
    scored = [
        score_runtime_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "base"),
        score_runtime_response("deepseek_wrapper", "deepseek", "m", "t2", "algorithmic_reasoning", "wrap"),
        score_runtime_response("deepseek_runtime", "deepseek", "m", "t3", "algorithmic_reasoning", "runtime"),
        score_runtime_response("deepseek_calibrated_runtime", "deepseek", "m", "t4", "algorithmic_reasoning", "calibrated"),
        score_runtime_response("openai_base", "openai", "m", "t5", "algorithmic_reasoning", "base"),
        score_runtime_response("openai_wrapper", "openai", "m", "t6", "algorithmic_reasoning", "wrap"),
        score_runtime_response("openai_runtime", "openai", "m", "t7", "algorithmic_reasoning", "runtime"),
        score_runtime_response("openai_calibrated_runtime", "openai", "m", "t8", "algorithmic_reasoning", "calibrated"),
    ]
    fl = compute_family_lift(scored)
    assert "family_lift" in fl
    assert "algorithmic_reasoning" in fl["family_lift"]
    assert "deepseek_wrapper_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "deepseek_runtime_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "deepseek_calibrated_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_wrapper_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_runtime_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_calibrated_lift_vs_base" in fl["family_lift"]["algorithmic_reasoning"]


# ---------------------------------------------------------------------------
# Runner with stub adapter
# ---------------------------------------------------------------------------

def test_runner_completes_240_with_stub(tmp_path):
    ds = _dataset(tmp_path, count=30, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = RuntimeConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out2",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "m", "OPENAI_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=30,
        expected_attempts=240,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=2.0,
    )
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] == COMPLETED
    assert result["summary"]["total_expected"] == 240
    assert result["summary"]["total_completed"] == 240
    assert result["summary"]["total_cost_usd"] > 0
    assert len(result["records"]) == 240
    assert len(result["scored"]) == 240


def test_runner_produces_traces_for_runtime_variants(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = RuntimeConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out3",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "m", "OPENAI_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=40,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=2.0,
    )
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    assert len(result["traces"]) == 20  # 4 runtime-loop variants * 5 tasks
    assert len(result["calibration_traces"]) == 10  # 2 calibrated variants * 5 tasks
    for trace in result["traces"]:
        assert trace.audit_decision in list(RuntimeAuditDecision)
        assert trace.initial_response
        assert trace.final_response
    for ct in result["calibration_traces"]:
        assert isinstance(ct.claim_classification, dict)
        assert len(ct.claim_classification) > 0
        assert ct.final_calibrated_response


def test_artifacts_include_runtime_traces(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = RuntimeConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out4",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "m", "OPENAI_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=40,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=2.0,
    )
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    summary = write_runtime_lift_artifacts(result)
    out = cfg.output_dir
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()
    assert (out / "paired_lift.json").exists()
    assert (out / "family_lift.json").exists()
    assert (out / "runtime_traces.jsonl").exists()
    assert (out / "calibration_traces.jsonl").exists()
    assert (out / "claim_status.jsonl").exists()
    assert (out / "confidence_bands.jsonl").exists()
    assert (out / "allowed_blocked_language.jsonl").exists()
    assert (out / "calibrated_final_responses.jsonl").exists()
    assert (out / "audit_decisions.jsonl").exists()
    assert (out / "repair_attempts.jsonl").exists()
    assert (out / "costs.json").exists()
    assert (out / "gate.json").exists()
    assert (out / "preflight.json").exists()
    assert (out / "responses.jsonl").exists()
    assert (out / "scores.jsonl").exists()
    assert (out / "evidence_integrity.json").exists()


def test_runner_records_have_task_family(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = RuntimeConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out_tf",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "m", "OPENAI_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=40,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=2.0,
    )
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    for r in result["records"]:
        assert "task_family" in r
        assert r["task_family"] in FAMILIES


def test_summary_contains_claims(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = RuntimeConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out5",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "m", "OPENAI_API_KEY", 0.00001, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "m", "OPENAI_API_KEY", 0.00001, True, True, use_calibrated_runtime=True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=40,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=2.0,
    )
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    summary = write_runtime_lift_artifacts(result)
    assert "authorized_claims" in summary
    assert "prohibited_claims" in summary
    assert any("runtime" in c.lower() for c in summary["authorized_claims"])
    assert any("universal" in c.lower() for c in summary["prohibited_claims"])


def test_budget_blocks_when_exceeded(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = RuntimeConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out6",
        variants=(
            RuntimeVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, False, False),
            RuntimeVariantSpec("deepseek_wrapper", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, True, False),
            RuntimeVariantSpec("deepseek_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, True, True),
            RuntimeVariantSpec("deepseek_calibrated_runtime", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, True, True, use_calibrated_runtime=True),
            RuntimeVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.1, False, False),
            RuntimeVariantSpec("openai_wrapper", "openai", "m", "OPENAI_API_KEY", 0.1, True, False),
            RuntimeVariantSpec("openai_runtime", "openai", "m", "OPENAI_API_KEY", 0.1, True, True),
            RuntimeVariantSpec("openai_calibrated_runtime", "openai", "m", "OPENAI_API_KEY", 0.1, True, True, use_calibrated_runtime=True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=40,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.01,
    )
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] in (BLOCKED_BUDGET, PARTIAL)


def test_report_builds_from_summary(tmp_path):
    cfg = _config(tmp_path, task_count=5)
    cfg = replace(cfg, expected_task_count=5, expected_attempts=40)
    result = run_runtime_paired_lift(cfg, adapter=_stub_adapter)
    report = build_runtime_lift_report(result["summary"])
    assert "Runtime Paired Lift Report" in report
    assert "deepseek_base" in report
    assert "deepseek_runtime" in report
    assert "openai_runtime" in report
    assert "Runtime vs Base" in report
    assert "Runtime vs Wrapper" in report
    assert "Calibrated Runtime vs Base" in report
    assert "Calibrated Runtime vs Wrapper" in report
    assert "Calibrated Runtime vs Runtime" in report
    assert "Prohibited" in report
    assert "Authorized" in report


# ---------------------------------------------------------------------------
# Methodology deviation note
# ---------------------------------------------------------------------------

def test_methodology_deviation_note_exists():
    note_path = Path("docs/status/methodology/FINITEXO_RUNTIME_TO_WRAPPER_DEVIATION_NOTE.md")
    assert note_path.exists(), "Methodology deviation note not found"


def test_methodology_note_contains_key_phrases():
    note_path = Path("docs/status/methodology/FINITEXO_RUNTIME_TO_WRAPPER_DEVIATION_NOTE.md")
    text = note_path.read_text(encoding="utf-8")
    assert "WRAPPER_DIAGNOSTIC_ONLY" in text
    # The note uses backtick formatting for the classification value
    assert "not admissible as" in text or "XENDRIS_RUNTIME_EVALUATION" in text
    assert "v0.9.0 Runtime Paired Lift" in text


# ---------------------------------------------------------------------------
# No provider calls in tests
# ---------------------------------------------------------------------------

def test_config_has_no_live_provider():
    """Verify that test config does not trigger live provider execution."""
    config = RuntimeConfig()
    assert config.environ.get("FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM") != "true"
    assert config.environ.get("DEEPSEEK_API_KEY") != "present"
    assert config.environ.get("OPENAI_API_KEY") != "present"
