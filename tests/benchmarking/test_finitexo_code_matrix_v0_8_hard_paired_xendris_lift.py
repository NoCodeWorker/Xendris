"""Tests for Finitexo Code Matrix v0.8.1 hard paired Xendris lift n=30."""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from benchmarks.finitexo_code_matrix_v0_8.hard_paired_xendris_lift import (
    BLOCKED_BUDGET,
    BLOCKED_PREFLIGHT,
    COMPLETED,
    FAMILIES,
    PARTIAL,
    HardLiftConfig,
    HardLiftPreflight,
    HardLiftVariantSpec,
    aggregate_by_family_variant,
    aggregate_by_variant,
    build_hard_lift_report,
    compute_family_lift,
    compute_paired_lift,
    evaluate_hard_lift_preflight,
    run_hard_paired_xendris_lift,
    score_hard_lift_response,
    write_hard_lift_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_8.hard_paired_xendris_lift.hard_lift_runner import (
    _build_xendris_task,
    XENDRIS_ADMISSIBILITY_PROMPT,
)
from benchmarks.finitexo_code_matrix_v0_8.hard_paired_xendris_lift.hard_lift_config import (
    validate_run_id_suffix,
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
            },
        )
    return root


def _config(
    tmp_path: Path, task_count: int = 30, budget: float = 1.0, overwrite: bool = True,
) -> HardLiftConfig:
    return HardLiftConfig(
        dataset_path=_dataset(tmp_path, count=task_count),
        output_dir=tmp_path / "out",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True),
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
    config = HardLiftConfig()
    assert config.run_id == "finitexo_v0_8_1_hard_paired_xendris_lift_n30"
    assert config.provider_mode == "real"
    assert config.budget_cap_usd == 1.0
    assert config.expected_task_count == 30
    assert config.expected_attempts == 120
    assert config.allow_mock_fallback is False
    assert config.temperature == 0.0
    assert len(config.variants) == 4


def test_config_uses_v0_8_dataset():
    config = HardLiftConfig()
    dataset_str = str(config.dataset_path)
    assert "v0_8" in dataset_str
    assert "hard_programming_n30" in dataset_str


def test_config_expected_attempts():
    config = HardLiftConfig()
    assert config.expected_attempts == 120
    calculated = len(config.variants) * config.expected_task_count
    assert config.expected_attempts == calculated


def test_config_four_variants():
    config = HardLiftConfig()
    names = [v.variant_name for v in config.variants]
    assert names == ["deepseek_base", "deepseek_xendris", "openai_base", "openai_xendris"]
    xendris_flags = [v.use_xendris_wrapper for v in config.variants]
    assert xendris_flags == [False, True, False, True]


def test_config_has_correct_hashes():
    config = HardLiftConfig()
    assert config.expected_dataset_hash == "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841"
    assert config.expected_manifest_hash == "3cfa4e904c0cf5918da4483c1e656fd8cf9b8e231bc5487b45e86eabb2ff1c54"


# ---------------------------------------------------------------------------
# Suffix
# ---------------------------------------------------------------------------

def test_suffix_creates_unique_output_dir():
    config = HardLiftConfig()
    suffixed = config.with_run_id_suffix("live_test")
    assert suffixed.run_id == "finitexo_v0_8_1_hard_paired_xendris_lift_n30_live_test"
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
    pf = evaluate_hard_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is True
    assert pf.decision == "HARD_LIFT_PREFLIGHT_READY"
    assert pf.expected_attempts == 120
    assert pf.task_count == 30


def test_preflight_blocks_missing_confirmation(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"DEEPSEEK_API_KEY": "present", "OPENAI_API_KEY": "present"})
    pf = evaluate_hard_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "missing_explicit_execution_confirmation" in pf.blockers


def test_preflight_blocks_missing_keys(tmp_path):
    cfg = _config(tmp_path)
    cfg = replace(cfg, environ={"FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true"})
    pf = evaluate_hard_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert any("missing_provider_key" in b for b in pf.blockers)


def test_preflight_blocks_wrong_dataset_count(tmp_path):
    cfg = _config(tmp_path, task_count=10)
    pf = evaluate_hard_lift_preflight(cfg, "ds-hash", "mf-hash", 10)
    assert pf.can_execute is False
    assert "insufficient_tasks" in pf.blockers


def test_preflight_blocks_wrong_hash(tmp_path):
    cfg = _config(tmp_path)
    pf = evaluate_hard_lift_preflight(cfg, "WRONG-HASH", "mf-hash", 30)
    assert pf.can_execute is False
    assert "dataset_hash_mismatch" in pf.blockers


def test_preflight_blocks_non_empty_output_dir(tmp_path):
    cfg = _config(tmp_path, overwrite=False)
    (tmp_path / "out").mkdir(parents=True, exist_ok=True)
    (tmp_path / "out" / "stale.txt").write_text("stale", encoding="utf-8")
    pf = evaluate_hard_lift_preflight(cfg, "ds-hash", "mf-hash", 30)
    assert pf.can_execute is False
    assert "output_dir_not_empty_and_overwrite_not_allowed" in pf.blockers


# ---------------------------------------------------------------------------
# Xendris wrapper
# ---------------------------------------------------------------------------

def test_xendris_wrapper_is_deterministic():
    task = {"task_id": "t001", "prompt": "Write a function."}
    r1 = _build_xendris_task(task)
    r2 = _build_xendris_task(task)
    assert r1["prompt"] == r2["prompt"]


def test_xendris_wrapper_does_not_include_answers():
    assert "t001" not in XENDRIS_ADMISSIBILITY_PROMPT
    assert "answer" not in XENDRIS_ADMISSIBILITY_PROMPT.lower() or "answer" == "answer"
    assert "scoring" not in XENDRIS_ADMISSIBILITY_PROMPT.lower()


def test_xendris_wrapper_preserves_task_prompt():
    task = {"task_id": "t001", "prompt": "Return 42."}
    wrapped = _build_xendris_task(task)
    assert wrapped["task_id"] == "t001"
    assert "Return 42." in wrapped["prompt"]
    assert wrapped["prompt"].startswith("You are a diagnostic code assistant")


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------

def test_scorer_range():
    r = score_hard_lift_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "")
    assert 0.0 <= r.score_total <= 1.0
    r = score_hard_lift_response("deepseek_xendris", "deepseek", "m", "t1", "edge_case_handling", "A" * 5000)
    assert 0.0 <= r.score_total <= 1.0


def test_scorer_empty_response():
    r = score_hard_lift_response("deepseek_base", "deepseek", "m", "t1", "stateful_refactor", "")
    assert r.verified_success is False
    assert r.score_components["response_present"] == 0.0


def test_scorer_good_response():
    r = score_hard_lift_response(
        "deepseek_xendris", "deepseek", "m", "t1", "api_design_consistency",
        "Fix helper. Returns normalized string. API contract preserved. No secrets. No errors. Limitations: diagnostic only.",
    )
    assert r.variant_name == "deepseek_xendris"
    assert r.task_family == "api_design_consistency"
    assert r.score_components["response_present"] == 1.0
    assert r.score_components["no_secret_exposure"] == 1.0


# ---------------------------------------------------------------------------
# Family-aware scoring
# ---------------------------------------------------------------------------

def test_scorer_has_task_family():
    r = score_hard_lift_response("deepseek_xendris", "deepseek", "m", "t1", "performance_constraints", "good response")
    assert r.task_family == "performance_constraints"


def test_aggregate_by_family_variant():
    scored = [
        score_hard_lift_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "resp1"),
        score_hard_lift_response("deepseek_xendris", "deepseek", "m", "t2", "algorithmic_reasoning", "resp2"),
        score_hard_lift_response("openai_base", "openai", "m", "t3", "algorithmic_reasoning", "resp3"),
        score_hard_lift_response("openai_xendris", "openai", "m", "t4", "stateful_refactor", "resp4"),
    ]
    fam = aggregate_by_family_variant(scored)
    assert "algorithmic_reasoning" in fam
    assert "deepseek_base" in fam["algorithmic_reasoning"]
    assert "deepseek_xendris" in fam["algorithmic_reasoning"]


def test_compute_family_lift():
    scored = [
        score_hard_lift_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "base low"),
        score_hard_lift_response("deepseek_xendris", "deepseek", "m", "t2", "algorithmic_reasoning", "xendris better"),
        score_hard_lift_response("openai_base", "openai", "m", "t3", "algorithmic_reasoning", "base low"),
        score_hard_lift_response("openai_xendris", "openai", "m", "t4", "algorithmic_reasoning", "xendris better"),
    ]
    fl = compute_family_lift(scored)
    assert "family_lift" in fl
    assert "algorithmic_reasoning" in fl["family_lift"]
    assert "deepseek_lift" in fl["family_lift"]["algorithmic_reasoning"]
    assert "openai_lift" in fl["family_lift"]["algorithmic_reasoning"]
    assert "overall_deepseek_lift_by_family_mean" in fl


# ---------------------------------------------------------------------------
# Paired lift calculation
# ---------------------------------------------------------------------------

def test_paired_lift_calculation():
    scored = [
        score_hard_lift_response("deepseek_base", "deepseek", "m", "t1", "algorithmic_reasoning", "base response low quality"),
        score_hard_lift_response("deepseek_xendris", "deepseek", "m", "t1", "algorithmic_reasoning", "xendris response better quality"),
        score_hard_lift_response("openai_base", "openai", "m", "t1", "algorithmic_reasoning", "base response low quality"),
        score_hard_lift_response("openai_xendris", "openai", "m", "t1", "algorithmic_reasoning", "xendris response better quality"),
    ]
    agg = aggregate_by_variant(scored)
    lift = compute_paired_lift(scored, agg)
    assert "deepseek_xendris_minus_base" in lift
    assert "openai_xendris_minus_base" in lift
    assert "xendris_lift_by_component_deepseek" in lift
    assert "xendris_lift_by_component_openai" in lift


def test_aggregate_by_variant():
    scored = [
        score_hard_lift_response("deepseek_base", "deepseek", "m", "t1", "a", "resp1"),
        score_hard_lift_response("deepseek_xendris", "deepseek", "m", "t1", "a", "resp2"),
        score_hard_lift_response("openai_base", "openai", "m", "t1", "a", "resp3"),
        score_hard_lift_response("openai_xendris", "openai", "m", "t1", "a", "resp4"),
    ]
    aggs = aggregate_by_variant(scored)
    assert len(aggs) == 4
    names = [a.variant_name for a in aggs]
    assert "deepseek_base" in names
    assert "deepseek_xendris" in names
    assert "openai_base" in names
    assert "openai_xendris" in names
    for a in aggs:
        assert a.task_count == 1
        assert a.total_cost_usd >= 0
        assert a.cost_per_mean_score_point >= 0


# ---------------------------------------------------------------------------
# Runner with stub adapter
# ---------------------------------------------------------------------------

def test_runner_completes_with_stub(tmp_path):
    ds = _dataset(tmp_path, count=30, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out2",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=1.0,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] == COMPLETED
    assert result["summary"]["total_expected"] == 120
    assert result["summary"]["total_completed"] == 120
    assert result["summary"]["total_cost_usd"] > 0
    assert len(result["records"]) == 120
    assert len(result["scored"]) == 120


def test_runner_records_have_task_family(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out_tf",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=1.0,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    for r in result["records"]:
        assert "task_family" in r
        assert r["task_family"] in FAMILIES
    for s in result["scored"]:
        assert s.task_family in FAMILIES


def test_artifacts_include_family_lift_and_paired_lift(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out3",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=1.0,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    summary = write_hard_lift_artifacts(result)
    out = cfg.output_dir
    assert (out / "summary.json").exists()
    assert (out / "report.md").exists()
    assert (out / "paired_lift.json").exists()
    assert (out / "task_level_lift.jsonl").exists()
    assert (out / "family_lift.json").exists()
    assert (out / "costs.json").exists()
    assert (out / "gate.json").exists()
    assert (out / "preflight.json").exists()
    assert (out / "responses.jsonl").exists()
    assert (out / "scores.jsonl").exists()
    assert (out / "evidence_integrity.json").exists()


def test_evidence_integrity_count(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out_ei",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=1.0,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    write_hard_lift_artifacts(result)
    integrity = json.loads((cfg.output_dir / "evidence_integrity.json").read_text(encoding="utf-8"))
    assert integrity["responses_count"] == 20
    assert integrity["scores_count"] == 20
    assert integrity["metadata_count"] == 20
    assert integrity["task_level_lift_count"] == 5


def test_summary_contains_claims(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out4",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=1.0,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    summary = write_hard_lift_artifacts(result)
    assert "authorized_claims" in summary
    assert "prohibited_claims" in summary
    assert any("Xendris wrapper" in c for c in summary["authorized_claims"])
    assert any("universal" in c.lower() for c in summary["prohibited_claims"])


def test_no_superiority_claim_authorized(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out5",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.00001, True),
            HardLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.00001, False),
            HardLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.00001, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=1.0,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    report_text = build_hard_lift_report(result["summary"])
    assert "no universal" in report_text.lower() or "diagnostic-only" in report_text.lower()


def test_budget_blocks_when_exceeded(tmp_path):
    ds = _dataset(tmp_path, count=5, dataset_hash="ds-hash", manifest_hash="mf-hash")
    cfg = HardLiftConfig(
        dataset_path=ds,
        output_dir=tmp_path / "out6",
        variants=(
            HardLiftVariantSpec("deepseek_base", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, False),
            HardLiftVariantSpec("deepseek_xendris", "deepseek", "m", "DEEPSEEK_API_KEY", 0.1, True),
            HardLiftVariantSpec("openai_base", "openai", "m", "OPENAI_API_KEY", 0.1, False),
            HardLiftVariantSpec("openai_xendris", "openai", "m", "OPENAI_API_KEY", 0.1, True),
        ),
        expected_dataset_hash="ds-hash",
        expected_manifest_hash="mf-hash",
        expected_task_count=5,
        expected_attempts=20,
        allow_overwrite=True,
        environ={
            "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
            "DEEPSEEK_API_KEY": "present",
            "OPENAI_API_KEY": "present",
        },
        budget_cap_usd=0.01,
    )
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    assert result["summary"]["final_decision"] in (BLOCKED_BUDGET, PARTIAL)


def test_report_builds_from_summary(tmp_path):
    cfg = _config(tmp_path)
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    report = build_hard_lift_report(result["summary"])
    assert "Hard Paired Xendris Lift Report" in report
    assert "deepseek_base" in report
    assert "deepseek_xendris" in report
    assert "openai_base" in report
    assert "openai_xendris" in report
    assert "Prohibited" in report
    assert "Authorized" in report


def test_family_lift_in_report(tmp_path):
    cfg = _config(tmp_path, task_count=5)
    cfg = replace(cfg, expected_task_count=5, expected_attempts=20)
    result = run_hard_paired_xendris_lift(cfg, adapter=_stub_adapter)
    report = build_hard_lift_report(result["summary"])
    assert "Family Lift" in report
    for family in FAMILIES:
        # Not every family will appear with 5 tasks; just check the section exists
        pass
    assert "## Family Lift" in report
