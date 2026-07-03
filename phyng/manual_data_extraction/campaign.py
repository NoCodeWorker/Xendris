"""Campaign orchestration for PHI_GRADIENT manual data extraction v4.4."""

from __future__ import annotations

from pathlib import Path

from phyng.core.compatibility import normalize_status
from phyng.manual_data_extraction.audit_trail import build_audit_trail, write_v4_4_outputs
from phyng.manual_data_extraction.dataset_update import build_next_inputs, build_quality_report, build_updated_dataset
from phyng.manual_data_extraction.loader import load_manual_extraction_inputs
from phyng.manual_data_extraction.reports import write_manual_data_extraction_reports
from phyng.manual_data_extraction.reviewer import review_manual_queue
from phyng.manual_data_extraction.schemas import (
    ManualDataExtractionCampaignResult,
    ManualDataExtractionGateResult,
    ManualExtractionQualityReport,
    NextPredictiveGainInputsV44,
    UpdatedYTrueDataset,
)


def run_phi_gradient_manual_data_extraction_campaign(root: str | Path = ".") -> ManualDataExtractionCampaignResult:
    repo_root = Path(root)
    inputs = load_manual_extraction_inputs(repo_root)
    allowed_claims = _allowed_claims()
    blocked_claims = _blocked_claims()
    if inputs.blocked_reason:
        dataset = UpdatedYTrueDataset()
        quality = ManualExtractionQualityReport()
        next_inputs = build_next_inputs(dataset, allowed_claims, blocked_claims)
        gate = ManualDataExtractionGateResult(
            status=inputs.blocked_reason,
            canonical_status=normalize_status(inputs.blocked_reason, domain="manual_data_extraction"),
            assembled_dataset=dataset,
            quality_report=quality,
            next_predictive_gain_inputs=next_inputs,
            allowed_claims=allowed_claims,
            blocked_claims=blocked_claims,
            next_actions=["Restore v4.3 manual extraction queue before v4.4."],
        )
        result = ManualDataExtractionCampaignResult(status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_manual_data_extraction_reports(result, repo_root / "reports")
        return result

    reviews, accepted, rejected = review_manual_queue(inputs)
    audit = build_audit_trail(reviews, accepted, rejected)
    dataset = build_updated_dataset(inputs, accepted)
    quality = build_quality_report(inputs, reviews, accepted, rejected)
    next_inputs = build_next_inputs(dataset, allowed_claims, blocked_claims)
    status = _status(accepted, dataset.ready_for_predictive_gain, reviews)
    output_paths = write_v4_4_outputs(repo_root, reviews, accepted, rejected, audit, dataset, quality, next_inputs)
    gate = ManualDataExtractionGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="manual_data_extraction"),
        manual_queue_count=len(inputs.manual_queue),
        reviewed_count=len(reviews),
        accepted_y_true_count=len(accepted),
        rejected_count=len(rejected),
        rerouted_count=sum(1 for review in reviews if review.reviewer_decision.startswith("SEND_TO_")),
        matched_prediction_count=dataset.matched_prediction_count,
        ready_for_predictive_gain=dataset.ready_for_predictive_gain,
        predictive_gain_status=dataset.predictive_gain_status,
        slot4_debt_status=dataset.slot4_debt_status,
        physical_claim_permission=dataset.physical_claim_permission,
        review_records=reviews,
        accepted_y_true_records=accepted,
        rejected_records=rejected,
        audit_trail=audit,
        assembled_dataset=dataset,
        quality_report=quality,
        next_predictive_gain_inputs=next_inputs,
        output_paths=output_paths,
        allowed_claims=allowed_claims,
        blocked_claims=blocked_claims,
        next_actions=_next_actions(dataset.ready_for_predictive_gain),
    )
    result = ManualDataExtractionCampaignResult(status=status, gate_result=gate)
    result.report_paths = write_manual_data_extraction_reports(result, repo_root / "reports")
    return result


def _status(accepted: list, ready_for_predictive_gain: bool, reviews: list) -> str:
    if ready_for_predictive_gain:
        return "PHI_GRADIENT_MANUAL_EXTRACTION_READY_FOR_PREDICTIVE_GAIN"
    if accepted:
        return "PHI_GRADIENT_MANUAL_EXTRACTION_PARTIAL"
    if reviews:
        return "PHI_GRADIENT_MANUAL_EXTRACTION_NO_YTRUE_ACCEPTED"
    return "PHI_GRADIENT_MANUAL_EXTRACTION_COMPLETED"


def _allowed_claims() -> list[str]:
    return [
        "Manual data extraction was performed.",
        "Accepted y_true records were added if QC passed.",
        "PredictiveGain readiness was evaluated.",
        "SLOT_4 debt remained blocking.",
    ]


def _blocked_claims() -> list[str]:
    return [
        "PHI_GRADIENT is predictively validated.",
        "PHI_GRADIENT has PredictiveGain unless v4.5 computes it.",
        "Gradient mechanism is supported.",
        "SLOT_4 debt is resolved.",
        "Frontera C is validated.",
        "Invariant is empirically confirmed.",
    ]


def _next_actions(ready_for_predictive_gain: bool) -> list[str]:
    if ready_for_predictive_gain:
        return ["Run v4.5 PredictiveGain smoke test without claiming validation."]
    return [
        "Recover exact table/page values for manual extraction targets.",
        "Continue public/supplementary dataset acquisition.",
        "Keep v4.1-SLOT4 debt work separate and open.",
    ]
