"""Strict QC for v5.7.3 targeted y_true candidates."""

from __future__ import annotations

from phyng.targeted_ytrue.schemas import TargetedYTrueCandidate


def evaluate_candidate(candidate: TargetedYTrueCandidate) -> tuple[str, str | None, list[str], list[str]]:
    passed: list[str] = []
    failed: list[str] = []
    if candidate.source_identity.get("identity_complete"):
        passed.append("source_identity_complete")
    else:
        failed.append("source_identity_incomplete")
    if candidate.local_pdf_path and candidate.local_pdf_hash:
        passed.append("verified_source_object_and_hash")
    else:
        failed.append("local_source_or_hash_missing")
    if candidate.page_number and candidate.location_label:
        passed.append("page_location_present")
    else:
        failed.append("location_missing")
    if candidate.numeric_value is not None:
        passed.append("numeric_value_present")
    else:
        failed.append("numeric_value_missing")
    if candidate.normalized_unit:
        passed.append("unit_resolved")
    else:
        failed.append("unit_unresolved")
    if candidate.conditions:
        passed.append("condition_mapping_resolved")
    else:
        failed.append("condition_mapping_ambiguous")
    if _model_only(candidate):
        failed.append("model_only_context")
    if failed:
        reason = _reason(failed)
        return _status_for_reason(reason), reason, passed, failed
    return "PASS_WITH_LIMITATIONS", None, passed, failed


def _model_only(candidate: TargetedYTrueCandidate) -> bool:
    text = " ".join(candidate.limitations).lower()
    return "model-only" in text or "theory-only" in text


def _reason(failed: list[str]) -> str:
    if "source_identity_incomplete" in failed:
        return "SOURCE_IDENTITY_INCOMPLETE"
    if "local_source_or_hash_missing" in failed:
        return "LOCAL_HASH_MISSING"
    if "location_missing" in failed:
        return "LOCATION_MISSING"
    if "numeric_value_missing" in failed:
        return "NUMERIC_VALUE_MISSING"
    if "unit_unresolved" in failed:
        return "UNIT_UNRESOLVED"
    if "condition_mapping_ambiguous" in failed:
        return "CONDITION_MAPPING_AMBIGUOUS"
    if "model_only_context" in failed:
        return "MODEL_ONLY"
    return "PROVENANCE_FAILURE"


def _status_for_reason(reason: str) -> str:
    if reason == "UNIT_UNRESOLVED":
        return "REQUIRES_UNIT_RESOLUTION"
    if reason == "CONDITION_MAPPING_AMBIGUOUS":
        return "REQUIRES_CONDITION_MAPPING"
    return "REJECT"
