"""Schemas for v4.4 manual data extraction."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class ManualExtractionInputs(BaseModel):
    manual_queue: list[dict] = Field(default_factory=list)
    source_coverage_audit: dict = Field(default_factory=dict)
    ytrue_candidates: dict = Field(default_factory=dict)
    previous_dataset: dict = Field(default_factory=dict)
    blocked_targets: dict = Field(default_factory=dict)
    previous_quality_report: dict = Field(default_factory=dict)
    previous_next_inputs: dict = Field(default_factory=dict)
    normalized_targets: dict = Field(default_factory=dict)
    qc_rules: dict = Field(default_factory=dict)
    model_predictions: dict = Field(default_factory=dict)
    source_hashes: dict = Field(default_factory=dict)
    slot4_debt: dict = Field(default_factory=dict)
    blocked_reason: str | None = None


class ManualExtractionReviewRecord(BaseModel):
    review_id: str
    queue_item_id: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str | None = None
    observable_class: str
    expected_measurement: str
    local_pdf_path: str | None = None
    page_number: int | None = None
    table_number: str | None = None
    figure_number: str | None = None
    extracted_value_text: str | None = None
    numeric_value: float | None = None
    unit: str | None = None
    uncertainty: float | None = None
    extraction_method: str
    reviewer_decision: str
    qc_status: str
    blockers: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class AcceptedManualYTrueRecord(BaseModel):
    y_true_id: str
    source_review_id: str
    target_id: str
    benchmark_id: str
    source_id: str
    source_hash: str
    observable_class: str
    normalized_variable_name: str
    value: float
    unit: str
    uncertainty: float | None = None
    source_location_type: str
    source_location_value: str
    extraction_method: str
    approximate: bool
    qc_status: str
    matched_prediction_ids: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class RejectedManualExtractionRecord(BaseModel):
    review_id: str
    queue_item_id: str
    target_id: str
    source_id: str
    observable_class: str
    rejection_reason: str
    required_next_action: str
    claim_impact: str


class ManualExtractionAuditEvent(BaseModel):
    audit_id: str
    queue_item_id: str
    target_id: str
    decision: str
    reason: str
    output_path: str
    timestamp: str = "2026-07-01"
    claim_impact: str


class ManualExtractionQualityReport(BaseModel):
    manual_queue_count: int = 0
    reviewed_count: int = 0
    accepted_count: int = 0
    rejected_count: int = 0
    rerouted_count: int = 0
    qc_pass_count: int = 0
    qc_fail_count: int = 0
    unit_issues: int = 0
    location_issues: int = 0
    hash_issues: int = 0
    prediction_match_issues: int = 0
    ready_for_predictive_gain: bool = False
    recommendations: list[str] = Field(default_factory=list)


class UpdatedYTrueDataset(BaseModel):
    dataset_id: str = "YTRUE-DATASET-v4_4"
    created_at: str = "2026-07-01"
    previous_dataset_ref: str = "data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json"
    manual_extraction_ref: str = "data/y_true/manual_extraction/phi_gradient_manual_extraction_accepted_y_true_v4_4.json"
    target_count: int = 0
    previous_y_true_count: int = 0
    new_y_true_count: int = 0
    total_y_true_count: int = 0
    records: list[dict] = Field(default_factory=list)
    ready_for_predictive_gain: bool = False
    predictive_gain_status: str = "UNDEFINED_INSUFFICIENT_YTRUE"
    minimum_viable_y_true_count: int = 3
    matched_prediction_count: int = 0
    slot4_debt_status: str = "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
    physical_claim_permission: str = "BLOCKED"
    notes: list[str] = Field(default_factory=list)


class NextPredictiveGainInputsV44(BaseModel):
    ready_for_predictive_gain: bool
    y_true_dataset_path: str
    model_predictions_path: str
    accepted_y_true_count: int
    matched_prediction_count: int
    minimum_viable_y_true_count: int = 3
    predictive_gain_status: str
    recommended_next_phase: str
    blocked_claims: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ManualDataExtractionGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manual_queue_count: int = 0
    reviewed_count: int = 0
    accepted_y_true_count: int = 0
    rejected_count: int = 0
    rerouted_count: int = 0
    matched_prediction_count: int = 0
    ready_for_predictive_gain: bool = False
    predictive_gain_status: str = "UNDEFINED_INSUFFICIENT_YTRUE"
    slot4_debt_status: str = "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
    physical_claim_permission: str = "BLOCKED"
    review_records: list[ManualExtractionReviewRecord] = Field(default_factory=list)
    accepted_y_true_records: list[AcceptedManualYTrueRecord] = Field(default_factory=list)
    rejected_records: list[RejectedManualExtractionRecord] = Field(default_factory=list)
    audit_trail: list[ManualExtractionAuditEvent] = Field(default_factory=list)
    assembled_dataset: UpdatedYTrueDataset
    quality_report: ManualExtractionQualityReport
    next_predictive_gain_inputs: NextPredictiveGainInputsV44
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class ManualDataExtractionCampaignResult(BaseModel):
    campaign_id: str = "PHI-GRADIENT-MANUAL-DATA-EXTRACTION-v4_4"
    status: str
    gate_result: ManualDataExtractionGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)
