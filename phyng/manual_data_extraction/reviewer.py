"""Reviewer orchestration for v4.4 manual extraction."""

from __future__ import annotations

from phyng.manual_data_extraction.schemas import AcceptedManualYTrueRecord, ManualExtractionReviewRecord, RejectedManualExtractionRecord
from phyng.manual_data_extraction.table_review import can_accept, location_value, review_queue_item


def review_manual_queue(inputs) -> tuple[list[ManualExtractionReviewRecord], list[AcceptedManualYTrueRecord], list[RejectedManualExtractionRecord]]:
    target_by_id = {target["target_id"]: target for target in inputs.normalized_targets.get("normalized_targets", [])}
    hash_by_source = {item["source_id"]: item for item in inputs.source_hashes.get("hashes", [])}
    predictions_by_benchmark = _predictions_by_benchmark(inputs.model_predictions.get("predictions", []))
    reviews: list[ManualExtractionReviewRecord] = []
    accepted: list[AcceptedManualYTrueRecord] = []
    rejected: list[RejectedManualExtractionRecord] = []
    for index, item in enumerate(inputs.manual_queue, start=1):
        review = review_queue_item(item, index, target_by_id, hash_by_source)
        reviews.append(review)
        matched_predictions = predictions_by_benchmark.get(review.benchmark_id, [])
        if can_accept(review) and matched_predictions:
            target = target_by_id.get(review.target_id, {})
            accepted.append(
                AcceptedManualYTrueRecord(
                    y_true_id=f"YTRUE-MANUAL-v4_4-{len(accepted) + 1:03d}",
                    source_review_id=review.review_id,
                    target_id=review.target_id,
                    benchmark_id=review.benchmark_id,
                    source_id=review.source_id,
                    source_hash=review.source_hash or "",
                    observable_class=review.observable_class,
                    normalized_variable_name=target.get("normalized_variable_name", review.observable_class.lower()),
                    value=review.numeric_value or 0.0,
                    unit=review.unit or "dimensionless",
                    uncertainty=review.uncertainty,
                    source_location_type="PAGE_TABLE_FIGURE",
                    source_location_value=location_value(review),
                    extraction_method=review.extraction_method,
                    approximate=False,
                    qc_status=review.qc_status,
                    matched_prediction_ids=matched_predictions,
                    limitations=["Accepted as y_true only for future predictive-gain evaluation; no physical validation is granted."],
                )
            )
        else:
            reason = review.reviewer_decision
            if can_accept(review) and not matched_predictions:
                reason = "REJECT_NO_MATCHED_PREDICTION"
            rejected.append(
                RejectedManualExtractionRecord(
                    review_id=review.review_id,
                    queue_item_id=review.queue_item_id,
                    target_id=review.target_id,
                    source_id=review.source_id,
                    observable_class=review.observable_class,
                    rejection_reason=reason,
                    required_next_action=_next_action(reason),
                    claim_impact="No PredictiveGain and no physical claim may use this item.",
                )
            )
    return reviews, accepted, rejected


def _predictions_by_benchmark(predictions: list[dict]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = {}
    for prediction in predictions:
        if not prediction.get("comparison_allowed", False):
            continue
        benchmark_id = prediction.get("benchmark_id")
        if not benchmark_id:
            continue
        grouped.setdefault(benchmark_id, []).append(prediction.get("prediction_id", ""))
    return grouped


def _next_action(reason: str) -> str:
    if reason == "REJECT_MISSING_LOCATION":
        return "Locate exact page/table/figure before accepting y_true."
    if reason == "REJECT_MISSING_UNIT":
        return "Recover unit from table caption or source text."
    if reason in {"REJECT_CONSTRAINT_NOT_YTRUE", "REJECT_LIMITATION_NOT_YTRUE"}:
        return "Keep as context/constraint, not observed y_true."
    if reason == "REJECT_NO_MATCHED_PREDICTION":
        return "Add or map model prediction for this benchmark before PredictiveGain."
    return "Perform stricter manual source review."
