"""Provenance validation for Finitexo Code Matrix v0.4 frozen tasks."""

from __future__ import annotations

from typing import Any, Mapping

from .freeze_types import FreezeIssue, FreezeIssueSeverity


REQUIRED_PROVENANCE_FIELDS = (
    "task_id",
    "source_id",
    "source_url",
    "source_license",
    "raw_source_hash",
    "normalized_source_hash",
    "adapted_candidate_hash",
    "frozen_task_hash",
    "acquisition_record_path",
    "adaptation_record_path",
    "promotion_gate_result",
    "human_review_required",
    "human_review_status",
    "known_limitations",
    "non_claims",
)


def validate_provenance(provenance: Mapping[str, Any], expected_task_hash: str) -> list[FreezeIssue]:
    issues: list[FreezeIssue] = []
    for field in REQUIRED_PROVENANCE_FIELDS:
        if field not in provenance:
            issues.append(
                FreezeIssue(
                    code=f"provenance_missing_{field}",
                    severity=FreezeIssueSeverity.BLOCKER,
                    message=f"Provenance record is missing {field!r}.",
                )
            )
    if provenance.get("frozen_task_hash") != expected_task_hash:
        issues.append(
            FreezeIssue(
                code="provenance_task_hash_mismatch",
                severity=FreezeIssueSeverity.BLOCKER,
                message="Provenance frozen task hash must match the current frozen task.",
            )
        )
    return issues
