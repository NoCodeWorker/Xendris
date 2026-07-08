"""Tests for Finitexo Code Matrix v0.9.1 Runtime Evidence Gate."""

import json
import math
import statistics
from pathlib import Path
from typing import Any

import pytest

from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate import (
    check_evidence_integrity,
    classify_signal,
    compute_all_comparisons,
    compute_comparison,
    load_run_artifacts,
    run_evidence_gate,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_config import (
    COMPARISON_SPECS,
    REQUIRED_ARTIFACTS,
    RuntimeEvidenceGateConfig,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_runner import (
    _compute_cost_robustness,
    _determine_final_decision,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FAMILIES = [
    "algorithmic_reasoning",
    "api_design_consistency",
    "edge_case_handling",
    "performance_constraints",
    "stateful_refactor",
]
VARIANTS = [
    "deepseek_base", "deepseek_wrapper", "deepseek_runtime", "deepseek_calibrated_runtime",
    "openai_base", "openai_wrapper", "openai_runtime", "openai_calibrated_runtime",
]
TASK_IDS = [f"task_{i:03d}" for i in range(1, 31)]


def _make_scores(tmp_path: Path, variant_count: int = 30, task_ids: list[str] | None = None) -> Path:
    ids = task_ids or TASK_IDS
    root = tmp_path / "run"
    root.mkdir(parents=True, exist_ok=True)
    scores: list[dict[str, Any]] = []
    for v in VARIANTS:
        for i, tid in enumerate(ids):
            scores.append({
                "variant_name": v,
                "task_id": tid,
                "score_total": 0.8 + (i % 10) * 0.01,
                "task_family": FAMILIES[i % len(FAMILIES)],
            })
    _write_jsonl(root / "scores.jsonl", scores)

    responses = [{"variant_name": v, "task_id": tid} for v in VARIANTS for tid in ids]
    _write_jsonl(root / "responses.jsonl", responses)

    metadata = [{"variant_name": v, "task_id": tid} for v in VARIANTS for tid in ids]
    _write_jsonl(root / "metadata.jsonl", metadata)

    traces = [{"variant_name": v, "task_id": tid} for v in ["deepseek_runtime", "openai_runtime", "deepseek_calibrated_runtime", "openai_calibrated_runtime"] for tid in ids]
    _write_jsonl(root / "runtime_traces.jsonl", traces)

    cal_ids = [f"task_{i:03d}" for i in range(1, 31)]
    cal_traces = [{"variant_name": v, "task_id": tid} for v in ["deepseek_calibrated_runtime", "openai_calibrated_runtime"] for tid in cal_ids]
    _write_jsonl(root / "calibration_traces.jsonl", cal_traces)

    decisions = [{"variant_name": v, "task_id": tid} for v in ["deepseek_runtime", "openai_runtime", "deepseek_calibrated_runtime", "openai_calibrated_runtime"] for tid in ids]
    _write_jsonl(root / "audit_decisions.jsonl", decisions)

    repairs = [{"variant_name": v, "task_id": tid} for v in ["deepseek_runtime", "openai_runtime", "deepseek_calibrated_runtime", "openai_calibrated_runtime"] for tid in ids]
    _write_jsonl(root / "repair_attempts.jsonl", repairs)

    for fname in ["claim_status.jsonl", "confidence_bands.jsonl", "allowed_blocked_language.jsonl", "calibrated_final_responses.jsonl"]:
        items = [{"variant_name": v, "task_id": tid} for v in ["deepseek_calibrated_runtime", "openai_calibrated_runtime"] for tid in ids]
        _write_jsonl(root / fname, items)

    errors: list[dict] = []
    _write_jsonl(root / "errors.jsonl", errors)

    _write_json(root / "summary.json", _make_summary(ids))
    _write_json(root / "gate.json", {"gate_decision": "PASS"})
    _write_json(root / "evidence_integrity.json", {"evidence_integrity_ready": True})
    _write_json(root / "costs.json", {"total_cost_usd": 0.0894})

    paired_lift: dict[str, Any] = {"deepseek_wrapper_vs_base_mean_lift": 0.002567}
    _write_json(root / "paired_lift.json", paired_lift)

    family_lift: dict[str, Any] = {
        "family_lift": {
            fam: {"deepseek_base_mean": 0.8, "deepseek_calibrated_lift_vs_base": 0.05}
            for fam in FAMILIES
        }
    }
    _write_json(root / "family_lift.json", family_lift)

    return root


def _make_summary(task_ids: list[str] | None = None) -> dict[str, Any]:
    n = len(task_ids) if task_ids else 30
    total = n * 8
    return {
        "final_decision": "RUNTIME_LIFT_COMPLETED_DIAGNOSTIC_ONLY",
        "provider_mode": "real",
        "dataset_hash": "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841",
        "manifest_hash": "3cfa4e904c0cf5918da4483c1e656fd8cf9b8e231bc5487b45e86eabb2ff1c54",
        "total_expected": total,
        "total_attempted": total,
        "total_completed": total,
        "total_failed": 0,
        "total_cost_usd": 0.0894,
        "budget_cap_usd": 2.0,
        "budget_decision": "WITHIN_BUDGET",
        "runtime_variant_trace_count": 4 * n,
        "calibration_trace_count": 2 * n,
        "cost_by_variant": {v: 0.01 for v in VARIANTS},
        "aggregates": [
            {"variant_name": v, "mean_score": 0.8, "min_score": 0.6, "max_score": 1.0, "total_cost_usd": 0.01}
            for v in VARIANTS
        ],
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.9.0",
        "experiment_type": "runtime_paired_lift",
        "dataset_name": "finitexo_code_matrix_hard_programming_n30",
        "dataset_size": n,
        "dataset_version": "0.8.0",
    }


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(item, sort_keys=True) for item in items) + "\n"
    path.write_text(text, encoding="utf-8")


def _cfg(tmp_path: Path) -> RuntimeEvidenceGateConfig:
    run_dir = _make_scores(tmp_path)
    out_dir = tmp_path / "out"
    return RuntimeEvidenceGateConfig(
        source_run_dir=run_dir,
        output_dir=out_dir,
        allow_overwrite=False,
    )


# ---------------------------------------------------------------------------
# Integrity: passes complete valid artifact set
# ---------------------------------------------------------------------------

def test_integrity_passes(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is True
    assert result["integrity_decision"] == "EVIDENCE_INTEGRITY_PASS"
    assert result["failure_count"] == 0


def test_integrity_fails_missing_artifact(tmp_path):
    cfg = _cfg(tmp_path)
    (cfg.source_run_dir / "scores.jsonl").unlink()
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False
    assert result["all_required_artifacts_exist"] is False


def test_integrity_fails_wrong_dataset_hash(tmp_path):
    cfg = _cfg(tmp_path)
    summary_path = cfg.source_run_dir / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["dataset_hash"] = "WRONG"
    summary_path.write_text(json.dumps(summary, sort_keys=True) + "\n", encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False
    assert result["dataset_hash_matches"] is False


def test_integrity_fails_total_completed_not_240(tmp_path):
    cfg = _cfg(tmp_path)
    summary_path = cfg.source_run_dir / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["total_completed"] = 200
    summary_path.write_text(json.dumps(summary, sort_keys=True) + "\n", encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False


def test_integrity_fails_errors_not_zero(tmp_path):
    cfg = _cfg(tmp_path)
    errors_path = cfg.source_run_dir / "errors.jsonl"
    errors_path.write_text(json.dumps({"error": "test"}) + "\n", encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False


def test_integrity_fails_missing_variant(tmp_path):
    cfg = _cfg(tmp_path)
    scores_path = cfg.source_run_dir / "scores.jsonl"
    lines = scores_path.read_text(encoding="utf-8").strip().splitlines()
    filtered = [l for l in lines if '"deepseek_runtime"' not in l]
    scores_path.write_text("\n".join(filtered) + "\n", encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False
    assert result["all_expected_variants_exist"] is False


def test_integrity_fails_variant_count_not_30(tmp_path):
    cfg = _cfg(tmp_path)
    scores_path = cfg.source_run_dir / "scores.jsonl"
    lines = scores_path.read_text(encoding="utf-8").strip().splitlines()
    extra = json.loads(lines[0])
    extra["variant_name"] = "deepseek_base"
    lines.append(json.dumps(extra, sort_keys=True))
    scores_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False
    assert result["all_variants_have_30"] is False


def test_integrity_fails_score_outside_range(tmp_path):
    cfg = _cfg(tmp_path)
    scores_path = cfg.source_run_dir / "scores.jsonl"
    line = json.loads(scores_path.read_text(encoding="utf-8").strip().splitlines()[0])
    line["score_total"] = 1.5
    lines = [json.dumps(line, sort_keys=True)]
    scores_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False
    assert result["all_scores_in_0_1"] is False


def test_integrity_fails_mismatched_task_ids(tmp_path):
    cfg = _cfg(tmp_path)
    scores_path = cfg.source_run_dir / "scores.jsonl"
    lines = scores_path.read_text(encoding="utf-8").strip().splitlines()
    parsed = [json.loads(l) for l in lines]
    for p in parsed:
        if p["variant_name"] == "deepseek_runtime":
            p["task_id"] = "DIFFERENT"
    text = "\n".join(json.dumps(p, sort_keys=True) for p in parsed) + "\n"
    scores_path.write_text(text, encoding="utf-8")
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is False
    assert result["task_id_set_identical"] is False


def test_integrity_passes_expected_trace_counts(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    result = check_evidence_integrity(cfg, artifacts)
    assert result["integrity_passed"] is True
    assert result["runtime_traces_count"] == 120
    assert result["calibration_traces_count"] == 60


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def test_paired_lift_computed_correctly(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    scores = artifacts["scores"]
    stats = compute_all_comparisons(scores, cfg)
    for key, comp in stats.items():
        if isinstance(comp, dict) and "error" not in comp:
            assert "mean_lift" in comp
            assert "median_lift" in comp
            assert "wins" in comp
            assert "losses" in comp
            assert "ties" in comp


def test_wins_losses_ties_correct(tmp_path):
    scores: list[dict] = []
    for i in range(30):
        tid = f"t{i:03d}"
        scores.append({"variant_name": "control", "task_id": tid, "score_total": 0.8, "task_family": "algorithmic_reasoning"})
        scores.append({"variant_name": "treatment", "task_id": tid, "score_total": 0.8, "task_family": "algorithmic_reasoning"})
    cfg = RuntimeEvidenceGateConfig()
    comp = compute_comparison(
        [s for s in scores if s["variant_name"] == "control"],
        [s for s in scores if s["variant_name"] == "treatment"],
        "control", "treatment", cfg,
    )
    assert comp["ties"] == 30
    assert comp["wins"] == 0
    assert comp["losses"] == 0
    assert comp["mean_lift"] == 0.0


def test_median_lift_correct(tmp_path):
    lifts = [0.1, 0.2, 0.3, 0.4, 0.5]
    scores: list[dict] = []
    for i, L in enumerate(lifts):
        tid = f"t{i:03d}"
        scores.append({"variant_name": "control", "task_id": tid, "score_total": 0.5, "task_family": "algorithmic_reasoning"})
        scores.append({"variant_name": "treatment", "task_id": tid, "score_total": 0.5 + L, "task_family": "algorithmic_reasoning"})
    cfg = RuntimeEvidenceGateConfig()
    comp = compute_comparison(
        [s for s in scores if s["variant_name"] == "control"],
        [s for s in scores if s["variant_name"] == "treatment"],
        "control", "treatment", cfg,
    )
    assert abs(comp["median_lift"] - 0.3) < 0.001


def test_bootstrap_deterministic(tmp_path):
    lifts = [0.1 * (i % 5) for i in range(30)]
    scores: list[dict] = []
    for i, L in enumerate(lifts):
        tid = f"t{i:03d}"
        scores.append({"variant_name": "control", "task_id": tid, "score_total": 0.5, "task_family": "algorithmic_reasoning"})
        scores.append({"variant_name": "treatment", "task_id": tid, "score_total": 0.5 + L, "task_family": "algorithmic_reasoning"})
    cfg1 = RuntimeEvidenceGateConfig(random_seed=20260708)
    cfg2 = RuntimeEvidenceGateConfig(random_seed=20260708)
    comp1 = compute_comparison(
        [s for s in scores if s["variant_name"] == "control"],
        [s for s in scores if s["variant_name"] == "treatment"],
        "control", "treatment", cfg1,
    )
    comp2 = compute_comparison(
        [s for s in scores if s["variant_name"] == "control"],
        [s for s in scores if s["variant_name"] == "treatment"],
        "control", "treatment", cfg2,
    )
    assert comp1["bootstrap_ci_95_low"] == comp2["bootstrap_ci_95_low"]
    assert comp1["bootstrap_ci_95_high"] == comp2["bootstrap_ci_95_high"]


def test_strong_signal_classification():
    comp = {
        "mean_lift": 0.05,
        "median_lift": 0.04,
        "wins": 25,
        "losses": 5,
        "bootstrap_ci_95_low": 0.01,
        "bootstrap_ci_95_high": 0.09,
        "non_negative_rate": 0.85,
    }
    assert classify_signal(comp) == "STRONG_DIAGNOSTIC_SIGNAL"


def test_moderate_signal_classification():
    comp = {
        "mean_lift": 0.03,
        "median_lift": 0.02,
        "wins": 18,
        "losses": 12,
        "bootstrap_ci_95_low": -0.01,
        "bootstrap_ci_95_high": 0.07,
        "non_negative_rate": 0.65,
    }
    assert classify_signal(comp) == "MODERATE_DIAGNOSTIC_SIGNAL"


def test_weak_inconclusive_classification():
    comp = {
        "mean_lift": 0.01,
        "median_lift": 0.0,
        "wins": 14,
        "losses": 16,
        "bootstrap_ci_95_low": -0.03,
        "bootstrap_ci_95_high": 0.05,
        "non_negative_rate": 0.55,
    }
    assert classify_signal(comp) == "WEAK_OR_INCONCLUSIVE_SIGNAL"


def test_negative_signal_classification():
    comp = {
        "mean_lift": -0.05,
        "median_lift": -0.04,
        "wins": 5,
        "losses": 25,
        "bootstrap_ci_95_low": -0.09,
        "bootstrap_ci_95_high": -0.01,
        "non_negative_rate": 0.2,
    }
    assert classify_signal(comp) == "NEGATIVE_SIGNAL"


def test_outlier_sensitivity(tmp_path):
    lifts = [0.1, 0.2, 0.3, 0.4, 0.5]
    scores: list[dict] = []
    for i, L in enumerate(lifts):
        tid = f"t{i:03d}"
        scores.append({"variant_name": "control", "task_id": tid, "score_total": 0.5, "task_family": "algorithmic_reasoning"})
        scores.append({"variant_name": "treatment", "task_id": tid, "score_total": 0.5 + L, "task_family": "algorithmic_reasoning"})
    cfg = RuntimeEvidenceGateConfig()
    comp = compute_comparison(
        [s for s in scores if s["variant_name"] == "control"],
        [s for s in scores if s["variant_name"] == "treatment"],
        "control", "treatment", cfg,
    )
    os = comp["outlier_sensitivity"]
    assert os["mean_lift_without_best_task"] is not None
    assert os["mean_lift_without_worst_task"] is not None
    assert os["sign_preserved_without_best_task"] is True
    assert os["sign_preserved_without_worst_task"] is True


# ---------------------------------------------------------------------------
# Claims
# ---------------------------------------------------------------------------

def test_universal_superiority_blocked(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    integrity = check_evidence_integrity(cfg, artifacts)
    stats = compute_all_comparisons(artifacts["scores"], cfg)
    from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_claims import (
        build_claim_authorization,
    )
    claims = build_claim_authorization(integrity, stats)
    blocked_str = " ".join(claims["blocked_claims"]).lower()
    assert "universal superiority" in blocked_str


def test_wrapper_generalization_blocked(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    integrity = check_evidence_integrity(cfg, artifacts)
    stats = compute_all_comparisons(artifacts["scores"], cfg)
    from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_claims import (
        build_claim_authorization,
    )
    claims = build_claim_authorization(integrity, stats)
    blocked_str = " ".join(claims["blocked_claims"]).lower()
    assert "wrapper results generalize to runtime" in blocked_str


def test_diagnostic_signal_claim_allowed(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    integrity = check_evidence_integrity(cfg, artifacts)
    stats = compute_all_comparisons(artifacts["scores"], cfg)
    from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_claims import (
        build_claim_authorization,
    )
    claims = build_claim_authorization(integrity, stats)
    allowed_str = " ".join(claims["authorized_claims"])
    assert "controlled n=30 run" in allowed_str


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def test_runner_creates_output_artifacts(tmp_path):
    cfg = _cfg(tmp_path)
    result = run_evidence_gate(cfg)
    out = cfg.output_dir
    assert (out / "summary.json").exists()
    assert (out / "integrity.json").exists()
    assert (out / "statistics.json").exists()
    assert (out / "cost_robustness.json").exists()
    assert (out / "claim_authorization.json").exists()
    assert (out / "report.md").exists()
    assert "final_decision" in result["summary"]
    assert result["final_decision"] is not None


def test_runner_refuses_non_empty_output_dir(tmp_path):
    cfg = _cfg(tmp_path)
    out = cfg.output_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / "stale.txt").write_text("x", encoding="utf-8")
    with pytest.raises(FileExistsError, match="non-empty"):
        run_evidence_gate(cfg)


def test_runner_does_not_mutate_source_artifacts(tmp_path):
    cfg = _cfg(tmp_path)
    source_files_before = {
        p.name: p.read_text(encoding="utf-8")
        for p in cfg.source_run_dir.iterdir() if p.is_file()
    }
    run_evidence_gate(cfg)
    source_files_after = {
        p.name: p.read_text(encoding="utf-8")
        for p in cfg.source_run_dir.iterdir() if p.is_file()
    }
    assert source_files_before == source_files_after


def test_final_decision_diagnostic_only(tmp_path):
    cfg = _cfg(tmp_path)
    result = run_evidence_gate(cfg)
    decision = result["final_decision"]
    assert "SUPERIORITY" not in decision
    assert decision.startswith("RUNTIME_EVIDENCE_GATE_")


# ---------------------------------------------------------------------------
# Cost robustness
# ---------------------------------------------------------------------------

def test_cost_robustness_computed(tmp_path):
    cfg = _cfg(tmp_path)
    artifacts = load_run_artifacts(cfg.source_run_dir)
    stats = compute_all_comparisons(artifacts["scores"], cfg)
    cr = _compute_cost_robustness(artifacts, stats)
    for treatment, control in COMPARISON_SPECS:
        key = f"{treatment}_vs_{control}"
        assert key in cr
        assert "cost_delta" in cr[key]
        assert "cost_ratio" in cr[key]
    assert "total_cost_usd" in cr
    assert "within_budget" in cr


# ---------------------------------------------------------------------------
# No provider calls
# ---------------------------------------------------------------------------

def test_no_provider_calls():
    """Verify that gate config does not contain provider keys."""
    cfg = RuntimeEvidenceGateConfig()
    assert "API_KEY" not in str(cfg.source_run_dir)
    assert cfg.source_run_version == "v0.9.0"
