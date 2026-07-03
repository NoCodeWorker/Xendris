"""Update v4.4 y_true dataset and predictive-gain readiness."""

from __future__ import annotations

from phyng.manual_data_extraction.schemas import AcceptedManualYTrueRecord, ManualExtractionQualityReport, NextPredictiveGainInputsV44, UpdatedYTrueDataset


MINIMUM_YTRUE = 3


def build_updated_dataset(inputs, accepted: list[AcceptedManualYTrueRecord]) -> UpdatedYTrueDataset:
    previous_records = inputs.previous_dataset.get("records", [])
    all_records = list(previous_records) + [record.model_dump(mode="json") for record in accepted]
    matched_prediction_count = len({prediction_id for record in accepted for prediction_id in record.matched_prediction_ids})
    ready = len(accepted) >= MINIMUM_YTRUE and matched_prediction_count >= MINIMUM_YTRUE
    status = "READY_FOR_SMOKE_TEST" if ready else "UNDEFINED_INSUFFICIENT_YTRUE"
    return UpdatedYTrueDataset(
        target_count=inputs.normalized_targets.get("target_count", len(inputs.normalized_targets.get("normalized_targets", []))),
        previous_y_true_count=len(previous_records),
        new_y_true_count=len(accepted),
        total_y_true_count=len(all_records),
        records=all_records,
        ready_for_predictive_gain=ready,
        predictive_gain_status=status,
        minimum_viable_y_true_count=MINIMUM_YTRUE,
        matched_prediction_count=matched_prediction_count,
        slot4_debt_status=inputs.slot4_debt.get("status", "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"),
        physical_claim_permission="BLOCKED",
        notes=[
            "PredictiveGain remains undefined unless accepted y_true and matched predictions meet the threshold.",
            "SLOT_4 debt remains open blocking gradient mechanism claims.",
        ],
    )


def build_quality_report(inputs, reviews, accepted, rejected) -> ManualExtractionQualityReport:
    rerouted = [review for review in reviews if review.reviewer_decision.startswith("SEND_TO_")]
    return ManualExtractionQualityReport(
        manual_queue_count=len(inputs.manual_queue),
        reviewed_count=len(reviews),
        accepted_count=len(accepted),
        rejected_count=len(rejected),
        rerouted_count=len(rerouted),
        qc_pass_count=sum(1 for review in reviews if review.qc_status in {"PASS", "PASS_WITH_LIMITATIONS"}),
        qc_fail_count=sum(1 for review in reviews if review.qc_status.startswith("FAIL")),
        unit_issues=sum(1 for review in reviews if "MISSING_UNIT" in review.blockers),
        location_issues=sum(1 for review in reviews if "MISSING_SOURCE_LOCATION" in review.blockers),
        hash_issues=sum(1 for review in reviews if "MISSING_SOURCE_HASH" in review.blockers),
        prediction_match_issues=0 if len(accepted) == 0 else sum(1 for record in accepted if not record.matched_prediction_ids),
        ready_for_predictive_gain=len(accepted) >= MINIMUM_YTRUE,
        recommendations=[
            "Recover exact page/table/figure locations for visibility and decoherence-rate targets.",
            "Do not use parameter constraints or limitation flags as observed y_true.",
            "Keep SLOT_4 debt open until separate source-pressure review resolves it.",
        ],
    )


def build_next_inputs(dataset: UpdatedYTrueDataset, allowed_claims: list[str], blocked_claims: list[str]) -> NextPredictiveGainInputsV44:
    if dataset.ready_for_predictive_gain:
        next_phase = "v4.5 - PredictiveGain Smoke Test & Error Comparison"
    else:
        next_phase = "v4.5 - Continued Manual/Public Data Acquisition"
    return NextPredictiveGainInputsV44(
        ready_for_predictive_gain=dataset.ready_for_predictive_gain,
        y_true_dataset_path="data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json",
        model_predictions_path="data/model_comparison/phi_gradient_model_predictions_v4_1.json",
        accepted_y_true_count=dataset.new_y_true_count,
        matched_prediction_count=dataset.matched_prediction_count,
        minimum_viable_y_true_count=MINIMUM_YTRUE,
        predictive_gain_status=dataset.predictive_gain_status,
        recommended_next_phase=next_phase,
        blocked_claims=blocked_claims,
        allowed_claims=allowed_claims,
        notes=["No PredictiveGain is computed in v4.4."],
    )
