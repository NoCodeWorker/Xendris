"""Conservative adaptation audit decision function."""

from __future__ import annotations

from benchmarks.finitexo_code_matrix_v0_3.source_acquisition import ContaminationRisk, OriginCandidate

from .adaptation_record import AdaptationRecord
from .adaptation_types import (
    AdaptationAuditDecision,
    AdaptationType,
    BenchmarkFitStatus,
    LeakageRisk,
    PromotionRecommendation,
    TaskValidityStatus,
)
from .contamination_audit import audit_contamination

SAFE_VALIDITY = {TaskValidityStatus.VALID, TaskValidityStatus.VALID_WITH_WARNINGS}
SAFE_FIT = {
    BenchmarkFitStatus.FIT_FOR_AGENTIC_PROGRAMMING,
    BenchmarkFitStatus.FIT_WITH_LIMITATIONS,
}


def evaluate_adaptation_candidate(record: AdaptationRecord) -> AdaptationAuditDecision:
    """Evaluate a candidate for future freeze recommendation only.

    This function does not modify any dataset and does not promote anything.
    """

    audit = audit_contamination(record)
    flags = list(audit["flags"])
    rejection_reasons = list(audit["rejection_reasons"])
    warnings = list(audit["warnings"])

    if record.source_origin_candidate not in {OriginCandidate.EXTERNAL_VERIFIED, OriginCandidate.EXTERNAL_ADAPTED}:
        rejection_reasons.append("source_origin_not_external_or_adapted")
    if record.adaptation_type in {AdaptationType.SYNTHETIC_EXPANSION, AdaptationType.MUTATED_INTERNAL_FIXTURE}:
        rejection_reasons.append("blocked_adaptation_type")
    if audit["contamination_risk"] in {ContaminationRisk.HIGH, ContaminationRisk.BLOCKED}:
        rejection_reasons.append("contamination_risk_blocks_recommendation")
    if record.leakage_risk == LeakageRisk.BLOCKED:
        rejection_reasons.append("leakage_risk_blocks_recommendation")
    elif record.leakage_risk == LeakageRisk.HIGH:
        warnings.append("high_leakage_risk")
    if record.task_validity_status not in SAFE_VALIDITY:
        rejection_reasons.append(f"task_validity_{record.task_validity_status.value.lower()}")
    if record.benchmark_fit_status not in SAFE_FIT:
        rejection_reasons.append(f"benchmark_fit_{record.benchmark_fit_status.value.lower()}")
    if record.semantic_preservation_score < 0.70:
        rejection_reasons.append("semantic_preservation_below_threshold")
    if record.structural_change_score > 0.65:
        rejection_reasons.append("structural_change_above_threshold")
    if record.difficulty_shift_score > 0.50:
        rejection_reasons.append("difficulty_shift_above_threshold")
    if not record.adapted_candidate_hash:
        rejection_reasons.append("missing_adapted_candidate_hash")
    if not record.raw_source_hash:
        rejection_reasons.append("missing_raw_source_hash")
    if not record.adaptation_summary:
        rejection_reasons.append("missing_adaptation_summary")

    unique_rejections = tuple(dict.fromkeys(rejection_reasons))
    unique_warnings = tuple(dict.fromkeys(warnings))
    if record.leakage_risk == LeakageRisk.BLOCKED or audit["contamination_risk"] == ContaminationRisk.BLOCKED:
        recommendation = PromotionRecommendation.BLOCKED
    elif unique_rejections:
        recommendation = PromotionRecommendation.DO_NOT_PROMOTE
    elif record.requires_human_review or record.task_validity_status == TaskValidityStatus.VALID_WITH_WARNINGS or unique_warnings:
        recommendation = PromotionRecommendation.RECOMMEND_WITH_HUMAN_REVIEW
    else:
        recommendation = PromotionRecommendation.RECOMMEND_FOR_FUTURE_FREEZE

    return AdaptationAuditDecision(
        recommendation=recommendation,
        flags=tuple(dict.fromkeys(flags)),
        rejection_reasons=unique_rejections,
        warnings=unique_warnings,
    )

