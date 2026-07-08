from __future__ import annotations

from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_config import (
    REQUIRED_ARTIFACTS,
    RuntimeEvidenceGateConfig,
)


def check_evidence_integrity(
    config: RuntimeEvidenceGateConfig,
    artifacts: dict[str, Any],
) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    failures: list[str] = []

    checks["source_run_dir_exists"] = config.source_run_dir.is_dir()
    if not checks["source_run_dir_exists"]:
        failures.append("source_run_dir_not_found")

    missing_artifacts = []
    for name in REQUIRED_ARTIFACTS:
        path = config.source_run_dir / name
        if not path.exists():
            missing_artifacts.append(name)
    checks["all_required_artifacts_exist"] = len(missing_artifacts) == 0
    if not checks["all_required_artifacts_exist"]:
        failures.append(f"missing_artifacts:{','.join(missing_artifacts)}")

    summary = artifacts.get("summary", {})

    checks["final_decision_matches"] = (
        summary.get("final_decision") == "RUNTIME_LIFT_COMPLETED_DIAGNOSTIC_ONLY"
    )
    if not checks["final_decision_matches"]:
        failures.append("final_decision_not_completed_diagnostic_only")

    checks["provider_mode_is_real"] = summary.get("provider_mode") == "real"
    if not checks["provider_mode_is_real"]:
        failures.append("provider_mode_not_real")

    checks["dataset_hash_matches"] = (
        summary.get("dataset_hash") == config.expected_dataset_hash
    )
    if not checks["dataset_hash_matches"]:
        failures.append("dataset_hash_mismatch")

    checks["manifest_hash_matches"] = (
        summary.get("manifest_hash") == config.expected_manifest_hash
    )
    if not checks["manifest_hash_matches"]:
        failures.append("manifest_hash_mismatch")

    checks["total_expected"] = summary.get("total_expected", -1)
    if checks["total_expected"] != config.expected_total_attempts:
        failures.append(f"total_expected_{checks['total_expected']}_expected_{config.expected_total_attempts}")

    checks["total_attempted"] = summary.get("total_attempted", -1)
    if checks["total_attempted"] != config.expected_total_attempts:
        failures.append(f"total_attempted_{checks['total_attempted']}_expected_{config.expected_total_attempts}")

    checks["total_completed"] = summary.get("total_completed", -1)
    if checks["total_completed"] != config.expected_total_completed:
        failures.append(f"total_completed_{checks['total_completed']}_expected_{config.expected_total_completed}")

    checks["total_failed"] = summary.get("total_failed", -1)
    if checks["total_failed"] != config.expected_total_failed:
        failures.append(f"total_failed_{checks['total_failed']}_expected_{config.expected_total_failed}")

    checks["responses_count"] = len(artifacts.get("responses", []))
    if checks["responses_count"] != config.expected_responses:
        failures.append(f"responses_count_{checks['responses_count']}_expected_{config.expected_responses}")

    checks["scores_count"] = len(artifacts.get("scores", []))
    if checks["scores_count"] != config.expected_scores:
        failures.append(f"scores_count_{checks['scores_count']}_expected_{config.expected_scores}")

    checks["metadata_count"] = len(artifacts.get("metadata", []))
    if checks["metadata_count"] != config.expected_metadata:
        failures.append(f"metadata_count_{checks['metadata_count']}_expected_{config.expected_metadata}")

    checks["runtime_traces_count"] = len(artifacts.get("runtime_traces", []))
    if checks["runtime_traces_count"] != config.expected_runtime_traces:
        failures.append(f"runtime_traces_{checks['runtime_traces_count']}_expected_{config.expected_runtime_traces}")

    checks["audit_decisions_count"] = len(artifacts.get("audit_decisions", []))
    if checks["audit_decisions_count"] != config.expected_runtime_traces:
        failures.append(f"audit_decisions_count_{checks['audit_decisions_count']}_expected_{config.expected_runtime_traces}")

    checks["repair_attempts_count"] = len(artifacts.get("repair_attempts", []))
    if checks["repair_attempts_count"] < 0 or checks["repair_attempts_count"] > config.expected_runtime_traces:
        failures.append(f"repair_attempts_count_{checks['repair_attempts_count']}_expected_0_to_{config.expected_runtime_traces}")

    checks["calibration_traces_count"] = len(artifacts.get("calibration_traces", []))
    if checks["calibration_traces_count"] != config.expected_calibration_traces:
        failures.append(f"calibration_traces_count_{checks['calibration_traces_count']}_expected_{config.expected_calibration_traces}")

    claims = artifacts.get("claim_status", [])
    checks["claim_status_count"] = len(claims)
    if checks["claim_status_count"] != config.expected_calibration_traces:
        failures.append(f"claim_status_count_{checks['claim_status_count']}_expected_{config.expected_calibration_traces}")

    checks["confidence_bands_count"] = len(artifacts.get("confidence_bands", []))
    if checks["confidence_bands_count"] != config.expected_calibration_traces:
        failures.append(f"confidence_bands_count_{checks['confidence_bands_count']}_expected_{config.expected_calibration_traces}")

    checks["allowed_blocked_language_count"] = len(artifacts.get("allowed_blocked_language", []))
    if checks["allowed_blocked_language_count"] != config.expected_calibration_traces:
        failures.append(f"allowed_blocked_language_count_{checks['allowed_blocked_language_count']}_expected_{config.expected_calibration_traces}")

    checks["calibrated_final_responses_count"] = len(artifacts.get("calibrated_final_responses", []))
    if checks["calibrated_final_responses_count"] != config.expected_calibration_traces:
        failures.append(f"calibrated_final_responses_count_{checks['calibrated_final_responses_count']}_expected_{config.expected_calibration_traces}")

    checks["errors_count"] = len(artifacts.get("errors", []))
    if checks["errors_count"] != config.expected_errors:
        failures.append(f"errors_count_{checks['errors_count']}_expected_{config.expected_errors}")

    ei = artifacts.get("evidence_integrity", {})
    checks["evidence_integrity_ready"] = ei.get("evidence_integrity_ready") is True
    if not checks["evidence_integrity_ready"]:
        failures.append("evidence_integrity_not_ready")

    scores = artifacts.get("scores", [])
    variant_names_in_scores = set(s.get("variant_name") for s in scores)
    expected_set = set(config.expected_variants)
    checks["all_expected_variants_exist"] = expected_set.issubset(variant_names_in_scores)
    if not checks["all_expected_variants_exist"]:
        missing = expected_set - variant_names_in_scores
        failures.append(f"missing_variants:{','.join(sorted(missing))}")

    variant_counts: dict[str, int] = {}
    for s in scores:
        vn = s.get("variant_name", "")
        variant_counts[vn] = variant_counts.get(vn, 0) + 1

    checks["variant_counts"] = variant_counts
    checks["all_variants_have_30"] = all(
        count == 30 for vn, count in variant_counts.items() if vn in expected_set
    )
    if not checks["all_variants_have_30"]:
        bad = {vn: c for vn, c in variant_counts.items() if c != 30 and vn in expected_set}
        failures.append(f"variant_count_not_30:{bad}")

    checks["all_scores_in_0_1"] = all(
        0.0 <= s.get("score_total", -1) <= 1.0 for s in scores
    )
    if not checks["all_scores_in_0_1"]:
        failures.append("score_outside_range")

    task_ids_by_variant: dict[str, set[str]] = {}
    for s in scores:
        vn = s.get("variant_name", "")
        tid = s.get("task_id", "")
        if vn in expected_set:
            task_ids_by_variant.setdefault(vn, set()).add(tid)
    variant_task_ids = {
        vn: tids for vn, tids in task_ids_by_variant.items() if vn in expected_set
    }
    if variant_task_ids:
        first_variant = next(iter(variant_task_ids))
        reference_ids = variant_task_ids[first_variant]
        checks["task_ids_match_across_variants"] = all(
            tids == reference_ids for tids in variant_task_ids.values()
        )
        if not checks["task_ids_match_across_variants"]:
            failures.append("task_id_mismatch_across_variants")
        checks["task_id_set_identical"] = checks["task_ids_match_across_variants"]
    else:
        checks["task_ids_match_across_variants"] = False
        checks["task_id_set_identical"] = False

    families_in_scores = set(s.get("task_family") for s in scores if s.get("task_family"))
    checks["all_expected_families_present"] = all(
        f in families_in_scores for f in config.expected_families
    )
    if not checks["all_expected_families_present"]:
        missing_f = [f for f in config.expected_families if f not in families_in_scores]
        failures.append(f"missing_families:{','.join(missing_f)}")

    passed = len(failures) == 0
    checks["integrity_passed"] = passed
    checks["failure_count"] = len(failures)
    checks["failures"] = failures
    checks["integrity_decision"] = (
        "EVIDENCE_INTEGRITY_PASS" if passed else "EVIDENCE_INTEGRITY_FAIL"
    )

    return checks
