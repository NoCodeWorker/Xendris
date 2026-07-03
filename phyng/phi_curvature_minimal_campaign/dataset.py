"""Minimal y_true dataset assembly for PHI_CURVATURE."""

from __future__ import annotations

from phyng.phi_curvature_minimal_campaign.schemas import PhiCurvatureAcceptedYTrue, PhiCurvatureMinimalYTrueDataset


def build_minimal_dataset(accepted: list[PhiCurvatureAcceptedYTrue]) -> PhiCurvatureMinimalYTrueDataset:
    return PhiCurvatureMinimalYTrueDataset(
        accepted_ytrue_count=len(accepted),
        threshold_reached=len(accepted) >= 3,
        records=[record.model_dump() for record in accepted],
        notes=[
            "matched_prediction_placeholder may be true in v4.8.",
            "PredictiveGain is not computed in the minimal campaign.",
            "Physical claim permission remains BLOCKED.",
        ],
    )
