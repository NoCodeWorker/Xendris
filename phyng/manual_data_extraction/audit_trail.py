"""Audit trail and serialization for v4.4 manual extraction."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.manual_data_extraction.schemas import (
    AcceptedManualYTrueRecord,
    ManualExtractionAuditEvent,
    ManualExtractionReviewRecord,
    RejectedManualExtractionRecord,
    UpdatedYTrueDataset,
    ManualExtractionQualityReport,
    NextPredictiveGainInputsV44,
)


OUTPUT_PATHS = {
    "review_records": Path("data/y_true/manual_extraction/phi_gradient_manual_extraction_review_records_v4_4.json"),
    "accepted_y_true": Path("data/y_true/manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.json"),
    "rejected": Path("data/y_true/manual_extraction/phi_gradient_manual_extraction_rejected_v4_4.json"),
    "audit_trail": Path("data/y_true/manual_extraction/phi_gradient_manual_extraction_audit_trail_v4_4.json"),
    "assembled_dataset": Path("data/y_true/phi_gradient_assembled_y_true_dataset_v4_4.json"),
    "quality_report": Path("data/y_true/phi_gradient_dataset_quality_report_v4_4.json"),
    "next_predictive_gain_inputs": Path("data/y_true/phi_gradient_v4_4_next_predictive_gain_inputs.json"),
}


def build_audit_trail(reviews: list[ManualExtractionReviewRecord], accepted: list[AcceptedManualYTrueRecord], rejected: list[RejectedManualExtractionRecord]) -> list[ManualExtractionAuditEvent]:
    accepted_by_review = {record.source_review_id: record for record in accepted}
    rejected_by_review = {record.review_id: record for record in rejected}
    events: list[ManualExtractionAuditEvent] = []
    for index, review in enumerate(reviews, start=1):
        if review.review_id in accepted_by_review:
            decision = "ACCEPT_AS_YTRUE"
            output = str(OUTPUT_PATHS["accepted_y_true"])
            reason = "QC passed with numeric value, unit, source hash, location and prediction match."
            impact = "Accepted for future PredictiveGain readiness only; no physical claim granted."
        else:
            rejected_record = rejected_by_review.get(review.review_id)
            decision = rejected_record.rejection_reason if rejected_record else review.reviewer_decision
            output = str(OUTPUT_PATHS["rejected"])
            reason = decision
            impact = "Rejected or rerouted; no y_true and no PredictiveGain impact."
        events.append(
            ManualExtractionAuditEvent(
                audit_id=f"MANUAL-AUDIT-v4_4-{index:03d}",
                queue_item_id=review.queue_item_id,
                target_id=review.target_id,
                decision=decision,
                reason=reason,
                output_path=output,
                claim_impact=impact,
            )
        )
    return events


def write_v4_4_outputs(
    root: str | Path,
    reviews: list[ManualExtractionReviewRecord],
    accepted: list[AcceptedManualYTrueRecord],
    rejected: list[RejectedManualExtractionRecord],
    audit: list[ManualExtractionAuditEvent],
    dataset: UpdatedYTrueDataset,
    quality: ManualExtractionQualityReport,
    next_inputs: NextPredictiveGainInputsV44,
) -> dict[str, str]:
    repo_root = Path(root)
    paths = {key: repo_root / path for key, path in OUTPUT_PATHS.items()}
    paths["review_records"].parent.mkdir(parents=True, exist_ok=True)
    _write_json(paths["review_records"], {"review_records": [item.model_dump(mode="json") for item in reviews], "reviewed_count": len(reviews)})
    _write_json(paths["accepted_y_true"], {"accepted_y_true": [item.model_dump(mode="json") for item in accepted], "accepted_count": len(accepted)})
    _write_json(paths["rejected"], {"rejected_records": [item.model_dump(mode="json") for item in rejected], "rejected_count": len(rejected)})
    _write_json(paths["audit_trail"], {"audit_trail": [item.model_dump(mode="json") for item in audit], "audit_event_count": len(audit)})
    _write_json(paths["assembled_dataset"], dataset.model_dump(mode="json"))
    _write_json(paths["quality_report"], quality.model_dump(mode="json"))
    _write_json(paths["next_predictive_gain_inputs"], next_inputs.model_dump(mode="json"))
    return {key: str(path.relative_to(repo_root)) for key, path in paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
