"""Next gate decision for PHI_CURVATURE v4.8."""

from __future__ import annotations

from collections import Counter

from phyng.phi_curvature_minimal_campaign.schemas import (
    PhiCurvatureMinimalYTrueDataset,
    PhiCurvatureNextGateDecision,
    SourceAvailabilityRecord,
    SourceResolutionRecord,
)


BLOCKED_CLAIMS = [
    "PHI_CURVATURE is validated.",
    "PHI_CURVATURE has PredictiveGain.",
    "PHI_CURVATURE is empirically supported beyond accepted y_true records.",
    "PHI_CURVATURE validates Frontera C.",
    "PHI_CURVATURE confirms the invariant.",
]

ALLOWED_CLAIMS = [
    "PHI_CURVATURE minimal source/y_true campaign was performed.",
    "Accepted y_true records were added only if QC passed.",
    "PHI_CURVATURE may proceed only according to next gate.",
]


def decide_next_gate(
    dataset: PhiCurvatureMinimalYTrueDataset,
    resolutions: list[SourceResolutionRecord],
    availability: list[SourceAvailabilityRecord],
) -> PhiCurvatureNextGateDecision:
    final_status = final_status_for_dataset(dataset, resolutions, availability)
    allowed_next = _allowed_next_phase(final_status)
    return PhiCurvatureNextGateDecision(
        final_status=final_status,
        accepted_ytrue_count=dataset.accepted_ytrue_count,
        threshold_reached=dataset.threshold_reached,
        source_resolution_summary=dict(Counter(record.resolution_status for record in resolutions)),
        source_availability_summary=dict(Counter(record.availability_status for record in availability)),
        blocked_claims=BLOCKED_CLAIMS,
        allowed_claims=ALLOWED_CLAIMS,
        allowed_next_phase=allowed_next,
        blocked_next_phases=["PredictiveGain evaluation", "Physical validation", "Full benchmark construction before accepted y_true threshold"],
        required_before_predictive_gain=["At least three accepted y_true records", "Matched prediction records", "Benchmark alignment gate", "Source-pressure review"],
        notes=["Accessibility was converted into source lookup and QC artifacts; no PredictiveGain was computed."],
    )


def final_status_for_dataset(
    dataset: PhiCurvatureMinimalYTrueDataset,
    resolutions: list[SourceResolutionRecord] | None = None,
    availability: list[SourceAvailabilityRecord] | None = None,
) -> str:
    if dataset.threshold_reached:
        return "PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED"
    if dataset.accepted_ytrue_count > 0:
        return "PHI_CURVATURE_MINIMAL_YTRUE_FOUND"
    resolutions = resolutions or []
    availability = availability or []
    if resolutions and all(record.resolution_status not in {"RESOLVED_EXACT", "RESOLVED_PROBABLE"} for record in resolutions):
        return "PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES"
    if availability and any(record.availability_status in {"SOURCE_REQUIRES_DOWNLOAD", "SOURCE_REQUIRES_HUMAN_LOOKUP"} for record in availability):
        return "PHI_CURVATURE_REQUIRES_TARGETED_SOURCE_DOWNLOAD"
    return "PHI_CURVATURE_NO_ACCEPTED_YTRUE_IN_MINIMAL_CAMPAIGN"


def _allowed_next_phase(final_status: str) -> str:
    if final_status == "PHI_CURVATURE_MINIMAL_YTRUE_THRESHOLD_REACHED":
        return "v4.9 — PHI_CURVATURE Minimal Benchmark Construction & Prediction Alignment"
    if final_status == "PHI_CURVATURE_MINIMAL_YTRUE_FOUND":
        return "v4.9 — PHI_CURVATURE Targeted y_true Expansion"
    if final_status in {"PHI_CURVATURE_REQUIRES_TARGETED_SOURCE_DOWNLOAD", "PHI_CURVATURE_REJECTED_NO_RESOLVABLE_SOURCES"}:
        return "v4.9 — PHI_CURVATURE Source Acquisition Sprint"
    return "v4.9 — PHI_CURVATURE Human Table/Supplement Review"
