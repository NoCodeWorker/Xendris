"""Provenance validation for v0.4.3 expanded freeze."""

from __future__ import annotations

from typing import Any, Mapping


REQUIRED_PROVENANCE_FIELDS = (
    "task_id",
    "source_id",
    "source_origin",
    "source_url",
    "source_license",
    "raw_source_hash",
    "adapted_candidate_hash",
    "frozen_task_hash",
    "acquisition_record_ref",
    "adaptation_record_ref",
    "promotion_gate_result",
    "known_limitations",
    "non_claims",
)


def validate_provenance(provenance: Mapping[str, Any], expected_task_hash: str) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_PROVENANCE_FIELDS:
        if field not in provenance:
            errors.append(f"provenance_missing_{field}")
    if provenance.get("frozen_task_hash") != expected_task_hash:
        errors.append("provenance_task_hash_mismatch")
    return errors
