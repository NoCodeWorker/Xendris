"""Candidate intake validation for Finitexo Code Matrix v0.3.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .source_registry import get_source_by_id

ORIGINS = {
    "EXTERNAL_VERIFIED",
    "EXTERNAL_ADAPTED",
    "SEMI_EXTERNAL_SYNTHETIC",
    "MUTATED_FIXTURE",
    "REJECTED_INSUFFICIENT_ORIGIN",
}

REQUIRED_FIELDS = {
    "task_id",
    "origin",
    "source_id",
    "source_reference",
    "title",
    "category",
    "difficulty",
    "prompt",
    "repository_fixture",
    "hidden_tests_description",
    "forbidden_files",
    "public_api_contract",
    "success_criteria",
    "anti_xendris_bias_notes",
    "h0_risk_notes",
    "origin_confidence",
    "externality_score",
    "admissible_for_v0_3",
    "hash_material",
}

ORIGIN_BANDS = {
    "EXTERNAL_VERIFIED": (0.85, 1.0),
    "EXTERNAL_ADAPTED": (0.65, 0.85),
    "MUTATED_FIXTURE": (0.45, 0.70),
    "SEMI_EXTERNAL_SYNTHETIC": (0.25, 0.55),
    "REJECTED_INSUFFICIENT_ORIGIN": (0.0, 0.25),
}

FORBIDDEN_VALUE_TERMS = (
    "xendris",
    "benchmark gate",
    "trust gate",
    "internal gate",
    "response contract",
)


def _candidate_value_text(value: Any) -> str:
    if isinstance(value, Mapping):
        return "\n".join(_candidate_value_text(item) for item in value.values())
    if isinstance(value, list):
        return "\n".join(_candidate_value_text(item) for item in value)
    return str(value).lower()


def _candidate_duplicates_existing_hash_material(candidate: Mapping[str, Any]) -> bool:
    root = Path("benchmarks")
    material = str(candidate.get("hash_material", ""))
    if not material:
        return False
    for path in root.glob("finitexo_code_matrix_v0_[123]*/**/*"):
        if not path.is_file() or "tasks_external_candidates" in str(path):
            continue
        try:
            if material in path.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def validate_candidate(candidate: Mapping[str, Any], registry: Mapping[str, Any]) -> dict[str, Any]:
    warnings: list[str] = []
    blocking_issues: list[str] = []

    missing = sorted(REQUIRED_FIELDS - set(candidate))
    blocking_issues.extend(f"missing_field:{field}" for field in missing)

    source_id = str(candidate.get("source_id", ""))
    source = get_source_by_id(registry, source_id)
    if source is None:
        blocking_issues.append("source_id_not_found")
    else:
        if not source.get("accepted"):
            blocking_issues.append("source_not_accepted")
        if candidate.get("origin") != source.get("source_type"):
            warnings.append("origin_differs_from_source_type")
        if candidate.get("origin") == "EXTERNAL_ADAPTED":
            if not source.get("adaptation_notes"):
                blocking_issues.append("external_adapted_missing_adaptation_notes")
            if not source.get("reference"):
                blocking_issues.append("external_adapted_missing_source_reference")
            if source.get("traceability_confidence") not in {"MEDIUM", "HIGH"}:
                blocking_issues.append("external_adapted_insufficient_traceability")

    origin = str(candidate.get("origin", ""))
    if origin not in ORIGINS:
        blocking_issues.append("invalid_origin")

    score = candidate.get("externality_score")
    if not isinstance(score, (int, float)) or not 0 <= float(score) <= 1:
        blocking_issues.append("externality_score_out_of_range")
        numeric_score = 0.0
    else:
        numeric_score = float(score)
        low, high = ORIGIN_BANDS.get(origin, (0.0, 1.0))
        if not low <= numeric_score <= high:
            warnings.append("externality_score_outside_origin_band")

    text = _candidate_value_text(candidate)
    for term in FORBIDDEN_VALUE_TERMS:
        if term in text:
            blocking_issues.append(f"forbidden_term:{term}")

    if not candidate.get("public_api_contract"):
        blocking_issues.append("missing_public_api_contract")
    if not candidate.get("hidden_tests_description"):
        blocking_issues.append("missing_hidden_tests_description")
    if not candidate.get("anti_xendris_bias_notes"):
        blocking_issues.append("missing_anti_bias_notes")
    if not candidate.get("h0_risk_notes"):
        blocking_issues.append("missing_h0_risk_notes")
    if not isinstance(candidate.get("admissible_for_v0_3"), bool):
        blocking_issues.append("admissible_for_v0_3_not_boolean")
    if candidate.get("admissible_for_v0_3") is False and not candidate.get("rejection_reason"):
        blocking_issues.append("rejected_candidate_missing_reason")
    if _candidate_duplicates_existing_hash_material(candidate):
        blocking_issues.append("duplicates_existing_task_hash_material")

    if blocking_issues:
        decision = "REJECTED"
    elif warnings:
        decision = "WARNINGS_PRESENT"
    else:
        decision = "ACCEPTED"

    return {
        "task_id": candidate.get("task_id"),
        "intake_decision": decision,
        "externality_score": numeric_score,
        "origin": origin,
        "warnings": warnings,
        "blocking_issues": blocking_issues,
    }


def apply_candidate_pool_checks(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Apply cross-candidate checks that need the whole candidate pool."""

    counts: dict[str, int] = {}
    for decision in decisions:
        task_id = str(decision.get("task_id", ""))
        counts[task_id] = counts.get(task_id, 0) + 1
    checked: list[dict[str, Any]] = []
    for decision in decisions:
        updated = dict(decision)
        if counts.get(str(updated.get("task_id", "")), 0) > 1:
            updated["blocking_issues"] = list(updated["blocking_issues"]) + ["duplicate_candidate_task_id"]
            updated["intake_decision"] = "REJECTED"
        checked.append(updated)
    return checked
