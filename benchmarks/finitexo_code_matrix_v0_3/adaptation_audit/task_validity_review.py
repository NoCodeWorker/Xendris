"""Deterministic task validity review for adapted candidates."""

from __future__ import annotations

from typing import Any, Mapping

from .adaptation_types import BenchmarkFitStatus, TaskValidityStatus


def review_task_validity(metadata: Mapping[str, Any]) -> dict[str, object]:
    reasons: list[str] = []
    warnings: list[str] = []
    if not metadata.get("expected_behavior"):
        reasons.append("missing_expected_behavior")
    if metadata.get("depends_on_live_network"):
        reasons.append("depends_on_live_network_state")
    if metadata.get("requires_secrets"):
        reasons.append("requires_secrets_or_private_keys")
    if metadata.get("requires_provider_execution"):
        reasons.append("requires_provider_execution")
    if not metadata.get("visible_tests"):
        reasons.append("missing_visible_tests_or_validation_oracle")
    if metadata.get("too_ambiguous"):
        reasons.append("too_ambiguous")
    if metadata.get("copied_internal_fixture"):
        reasons.append("copied_internal_fixture")
    if metadata.get("modifies_forbidden_files"):
        reasons.append("requires_modifying_forbidden_files")
    if not metadata.get("reproducible_setup"):
        warnings.append("missing_reproducible_setup_metadata")

    if any(reason in reasons for reason in ("depends_on_live_network_state", "requires_secrets_or_private_keys")):
        status = TaskValidityStatus.BLOCKED
        fit = BenchmarkFitStatus.TOO_DEPENDENT_ON_EXTERNAL_STATE
    elif reasons:
        status = TaskValidityStatus.INVALID
        fit = BenchmarkFitStatus.BLOCKED
    elif warnings:
        status = TaskValidityStatus.VALID_WITH_WARNINGS
        fit = BenchmarkFitStatus.FIT_WITH_LIMITATIONS
    else:
        status = TaskValidityStatus.VALID
        fit = BenchmarkFitStatus.FIT_FOR_AGENTIC_PROGRAMMING

    return {
        "task_validity_status": status,
        "benchmark_fit_status": fit,
        "rejection_reasons": reasons,
        "warnings": warnings,
    }

