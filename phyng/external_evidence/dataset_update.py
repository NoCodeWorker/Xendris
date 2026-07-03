"""Dataset update logic for v4.5 assembled y_true dataset."""

from __future__ import annotations

import datetime
from phyng.external_evidence.schemas import (
    AssembledYTrueDatasetv45,
    AcceptedExternalYTrueRecord,
    NextPredictiveGainInputsv45,
)


def update_assembled_dataset(
    inputs: dict,
    accepted_records: list[AcceptedExternalYTrueRecord],
) -> tuple[AssembledYTrueDatasetv45, NextPredictiveGainInputsv45]:
    prev_dataset = inputs.get("assembled_dataset_v4_4", {})
    prev_records = prev_dataset.get("records", [])

    # Merge records
    merged_records = list(prev_records)
    for r in accepted_records:
        merged_records.append(r.model_dump())

    total_count = len(merged_records)
    prev_count = len(prev_records)
    new_count = len(accepted_records)

    # Compute prediction match count
    # Each record has a list of matched_prediction_ids
    matched_preds = set()
    for r in merged_records:
        for p_id in r.get("matched_prediction_ids", []):
            matched_preds.add(p_id)
    matched_prediction_count = len(matched_preds)

    # Threshold rules
    ready = total_count >= 3 and matched_prediction_count >= 3
    status = "READY_FOR_SMOKE_TEST" if ready else "UNDEFINED_INSUFFICIENT_YTRUE"
    next_phase = "v4.6 — PredictiveGain Smoke Test & Error Comparison" if ready else "candidate freeze or new experiment design"

    assembled = AssembledYTrueDatasetv45(
        dataset_id="YTRUE-DATASET-v4_5",
        created_at=datetime.date.today().isoformat(),
        previous_dataset_ref="data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json",
        external_evidence_ref="data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json",
        previous_y_true_count=prev_count,
        new_y_true_count=new_count,
        total_y_true_count=total_count,
        records=merged_records,
        ready_for_predictive_gain=ready,
        predictive_gain_status=status,
        minimum_viable_y_true_count=3,
        matched_prediction_count=matched_prediction_count,
        slot4_debt_status="OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        physical_claim_permission="BLOCKED",
        notes=[
            "PredictiveGain remains undefined unless accepted y_true and matched predictions meet the threshold.",
            "SLOT_4 debt remains open blocking gradient mechanism claims.",
        ],
    )

    allowed_claims = [
        "External evidence acquisition was attempted.",
        "Accepted external y_true records were added if QC passed.",
        "Candidate was frozen if the y_true threshold was not reached.",
    ]
    blocked_claims = [
        "PHI_GRADIENT is validated.",
        "PHI_GRADIENT has PredictiveGain before v4.6.",
        "Gradient mechanism is supported.",
        "SLOT_4 debt is resolved.",
        "Frontera C is validated.",
        "Invariant is empirically confirmed.",
    ]

    next_inputs = NextPredictiveGainInputsv45(
        ready_for_predictive_gain=ready,
        predictive_gain_status=status,
        minimum_viable_y_true_count=3,
        recommended_next_phase=next_phase,
        y_true_dataset_path="data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json",
        model_predictions_path="data/model_comparison/phi_gradient_model_predictions_v4_1.json",
        accepted_y_true_count=total_count,
        matched_prediction_count=matched_prediction_count,
        allowed_claims=allowed_claims,
        blocked_claims=blocked_claims,
        notes=["PredictiveGain remains undefined until a later gate computes it."],
    )

    return assembled, next_inputs
