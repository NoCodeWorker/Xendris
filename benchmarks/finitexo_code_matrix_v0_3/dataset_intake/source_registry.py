"""Source registry validation for Finitexo Code Matrix v0.3.1."""

from __future__ import annotations

from typing import Any, Mapping

SOURCE_TYPES = {
    "EXTERNAL_VERIFIED",
    "EXTERNAL_ADAPTED",
    "SEMI_EXTERNAL_SYNTHETIC",
    "MUTATED_FIXTURE",
    "REJECTED_INSUFFICIENT_ORIGIN",
}

RISK_LEVELS = {"LOW", "MEDIUM", "HIGH"}
CONFIDENCE_LEVELS = {"LOW", "MEDIUM", "HIGH"}


def get_source_by_id(registry: Mapping[str, Any], source_id: str) -> dict[str, Any] | None:
    for source in registry.get("sources", []):
        if source.get("source_id") == source_id:
            return dict(source)
    return None


def source_acceptance_is_coherent(source: Mapping[str, Any]) -> bool:
    source_type = source.get("source_type")
    accepted = source.get("accepted")
    rejection_reason = source.get("rejection_reason")
    if source_type == "REJECTED_INSUFFICIENT_ORIGIN":
        return accepted is False and bool(rejection_reason)
    if accepted is False:
        return bool(rejection_reason)
    return accepted is True and rejection_reason is None


def validate_source_registry(registry: Mapping[str, Any]) -> list[str]:
    issues: list[str] = []
    seen: set[str] = set()
    if registry.get("registry_version") != "0.1":
        issues.append("invalid_registry_version")
    for source in registry.get("sources", []):
        source_id = source.get("source_id")
        if not source_id:
            issues.append("missing_source_id")
            continue
        if source_id in seen:
            issues.append(f"duplicate_source_id:{source_id}")
        seen.add(source_id)
        if source.get("source_type") not in SOURCE_TYPES:
            issues.append(f"invalid_source_type:{source_id}")
        if source.get("xendris_contamination_risk") not in RISK_LEVELS:
            issues.append(f"invalid_contamination_risk:{source_id}")
        if source.get("traceability_confidence") not in CONFIDENCE_LEVELS:
            issues.append(f"invalid_traceability_confidence:{source_id}")
        if not source_acceptance_is_coherent(source):
            issues.append(f"incoherent_acceptance:{source_id}")
    return issues

