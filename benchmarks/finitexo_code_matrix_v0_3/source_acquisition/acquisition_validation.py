"""Conservative promotion gate for acquired source records."""

from __future__ import annotations

from .acquisition_types import ContaminationRisk, OriginCandidate, PromotionDecision, SourceType
from .source_acquisition_record import SourceAcquisitionRecord

EXTERNAL_ORIGINS = {
    OriginCandidate.EXTERNAL_VERIFIED,
    OriginCandidate.EXTERNAL_ADAPTED,
}


def evaluate_promotion_eligibility(record: SourceAcquisitionRecord) -> PromotionDecision:
    """Evaluate whether a record can be eligible for future promotion.

    Eligibility is not dataset promotion. It only means the record passed the
    acquisition gate and may be considered in a later explicit dataset phase.
    """

    blockers: list[str] = []
    warnings: list[str] = []

    if record.origin_candidate not in EXTERNAL_ORIGINS:
        blockers.append("origin_not_external_candidate")
    if record.source_type in {SourceType.INTERNAL_FIXTURE, SourceType.SYNTHETIC_LOCAL, SourceType.UNKNOWN}:
        if record.origin_candidate == OriginCandidate.EXTERNAL_VERIFIED:
            blockers.append("internal_or_unknown_source_cannot_be_external_verified")
        elif record.origin_candidate == OriginCandidate.EXTERNAL_ADAPTED:
            blockers.append("internal_or_unknown_source_cannot_be_external_adapted")
    if not record.source_url:
        blockers.append("missing_source_url")
    if not record.source_hash:
        blockers.append("missing_source_hash")
    if not record.license or record.license.upper() == "UNKNOWN":
        blockers.append("missing_or_unknown_license")
    if record.contamination_risk not in {ContaminationRisk.LOW, ContaminationRisk.MEDIUM}:
        blockers.append("contamination_risk_blocks_promotion")
    if not record.raw_snapshot_path:
        blockers.append("missing_raw_snapshot_path")
    if record.adaptation_required and not record.adaptation_notes:
        blockers.append("missing_adaptation_notes")
    blockers.extend(record.rejection_reasons)

    if not record.normalized_snapshot_path:
        warnings.append("missing_normalized_snapshot_path")
    if record.origin_candidate == OriginCandidate.EXTERNAL_ADAPTED and not record.adapted_task_path:
        warnings.append("missing_adapted_task_path")

    if blockers:
        return PromotionDecision(
            promotion_allowed=False,
            decision="BLOCKED_FOR_FUTURE_PROMOTION",
            blockers=tuple(blockers),
            warnings=tuple(warnings),
        )
    return PromotionDecision(
        promotion_allowed=True,
        decision="ELIGIBLE_FOR_FUTURE_PROMOTION",
        blockers=(),
        warnings=tuple(warnings),
    )

