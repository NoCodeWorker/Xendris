"""Manifest validation for Finitexo Code Matrix v0.4."""

from __future__ import annotations

from typing import Any, Mapping

from .freeze_types import FreezeIssue, FreezeIssueSeverity


def validate_manifest(manifest: Mapping[str, Any]) -> list[FreezeIssue]:
    issues: list[FreezeIssue] = []
    expected = {
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.4",
        "dataset_version": "0.4",
        "dataset_status": "FROZEN",
        "dataset_type": "EXTERNAL_ADAPTED",
        "created_from_trust_infrastructure": "v0.3.x",
        "provider_execution_allowed": False,
        "model_comparison_allowed": False,
        "external_superiority_claim_authorized": False,
        "statistical_claim_authorized": False,
        "frozen_dataset_modified_without_version_bump_allowed": False,
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            issues.append(
                FreezeIssue(
                    code=f"manifest_invalid_{key}",
                    severity=FreezeIssueSeverity.BLOCKER,
                    message=f"Manifest field {key!r} must be {value!r}.",
                )
            )
    if not manifest.get("frozen_task_ids"):
        issues.append(
            FreezeIssue(
                code="manifest_missing_frozen_task_ids",
                severity=FreezeIssueSeverity.BLOCKER,
                message="Manifest must list frozen task ids.",
            )
        )
    return issues
