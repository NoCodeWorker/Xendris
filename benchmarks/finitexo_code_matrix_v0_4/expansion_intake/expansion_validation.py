"""Deterministic candidate validation for expansion intake."""

from __future__ import annotations

from dataclasses import replace

from .expansion_candidate import ExpansionCandidate
from .expansion_types import ExpansionReadiness, ExpansionSourceClass, FreezeRecommendation


VALID_ORIGINS = {ExpansionSourceClass.EXTERNAL_VERIFIED, ExpansionSourceClass.EXTERNAL_ADAPTED}
VALID_TASK_STATUS = {"VALID", "VALID_WITH_WARNINGS"}
VALID_FIT_STATUS = {"FIT_FOR_AGENTIC_PROGRAMMING", "FIT_WITH_LIMITATIONS"}


def validate_expansion_candidate(candidate: ExpansionCandidate) -> ExpansionCandidate:
    reasons: list[str] = list(candidate.rejection_reasons)
    warnings: list[str] = list(candidate.warnings)

    if candidate.contamination_risk == "BLOCKED":
        reasons.append("blocked_contamination_risk")
    if candidate.leakage_risk == "BLOCKED" or candidate.leakage_risk == "HIGH":
        reasons.append("blocked_or_high_leakage_risk")
    if candidate.provider_execution_required:
        reasons.append("provider_execution_required")
    if candidate.network_required:
        reasons.append("network_required")
    if candidate.secrets_required:
        reasons.append("secrets_required")
    if candidate.external_superiority_claim_authorized:
        reasons.append("external_superiority_claim_authorized")
    if not candidate.proposed_task_hash:
        reasons.append("missing_proposed_task_hash")
    if not candidate.provenance_ref:
        reasons.append("missing_provenance")
    if candidate.source_origin == ExpansionSourceClass.MUTATED_FIXTURE:
        reasons.append("mutated_fixture_cannot_be_presented_as_external")
    if candidate.source_origin == ExpansionSourceClass.SYNTHETIC_LOCAL:
        reasons.append("synthetic_local_cannot_be_presented_as_external")

    text = " ".join((candidate.proposed_task_ref or "", *candidate.warnings, *candidate.rejection_reasons)).lower()
    if "hidden test" in text or "scoring formula" in text or "xendris-specific" in text:
        reasons.append("leakage_or_self_favoring_instruction")

    missing_provenance = not all(
        [
            candidate.source_url,
            candidate.source_license and candidate.source_license != "UNKNOWN",
            candidate.acquisition_record_ref,
            candidate.adaptation_record_ref,
            candidate.proposed_task_ref,
            candidate.proposed_task_hash,
            candidate.provenance_ref,
        ]
    )
    if missing_provenance:
        warnings.append("incomplete_provenance")

    structurally_strong = (
        candidate.source_origin in VALID_ORIGINS
        and not missing_provenance
        and candidate.contamination_risk == "LOW"
        and candidate.leakage_risk in {"LOW", "MEDIUM"}
        and candidate.task_validity_status in VALID_TASK_STATUS
        and candidate.benchmark_fit_status in VALID_FIT_STATUS
        and candidate.semantic_preservation_score >= 0.70
        and candidate.structural_change_score <= 0.65
        and candidate.difficulty_shift_score <= 0.50
    )

    if reasons:
        blocked = any(reason in reasons for reason in ("blocked_contamination_risk", "blocked_or_high_leakage_risk", "provider_execution_required", "network_required", "secrets_required"))
        return replace(
            candidate,
            expansion_readiness=ExpansionReadiness.BLOCKED if blocked else ExpansionReadiness.DO_NOT_FREEZE,
            freeze_recommendation=FreezeRecommendation.BLOCKED if blocked else FreezeRecommendation.DO_NOT_RECOMMEND,
            rejection_reasons=tuple(dict.fromkeys(reasons)),
            warnings=tuple(dict.fromkeys(warnings)),
        )

    if structurally_strong and candidate.human_review_required:
        return replace(
            candidate,
            expansion_readiness=ExpansionReadiness.READY_WITH_HUMAN_REVIEW,
            freeze_recommendation=FreezeRecommendation.RECOMMEND_WITH_HUMAN_REVIEW,
            warnings=tuple(dict.fromkeys(warnings)),
        )

    if structurally_strong:
        return replace(
            candidate,
            expansion_readiness=ExpansionReadiness.READY_FOR_FUTURE_FREEZE,
            freeze_recommendation=FreezeRecommendation.RECOMMEND_FOR_V0_4_X_FREEZE,
            warnings=tuple(dict.fromkeys(warnings)),
        )

    readiness = ExpansionReadiness.NEEDS_MORE_PROVENANCE if missing_provenance else ExpansionReadiness.NEEDS_MORE_VALIDATION
    return replace(
        candidate,
        expansion_readiness=readiness,
        freeze_recommendation=FreezeRecommendation.DO_NOT_RECOMMEND,
        warnings=tuple(dict.fromkeys(warnings)),
    )
