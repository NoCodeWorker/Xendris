"""Schemas for v4.3 y_true extraction and dataset assembly."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class SourceCoverageAuditRecord(BaseModel):
    audit_id: str
    target_id: str
    benchmark_id: str
    source_id: str
    extract_id: str
    source_hash_present: bool
    local_pdf_present: bool
    supplementary_present: bool
    public_dataset_reference_present: bool
    page_reference_present: bool
    table_reference_present: bool
    figure_reference_present: bool
    source_coverage_status: str
    blockers: list[str] = Field(default_factory=list)
    next_action: str


class YTrueExtractionCandidate(BaseModel):
    candidate_id: str
    target_id: str
    observable_class: str
    source_id: str
    extract_id: str
    candidate_value_text: str
    numeric_value: float | None = None
    unit: str | None = None
    uncertainty: float | None = None
    extraction_method: str
    source_location: str
    provenance_status: str
    qc_status: str
    can_enter_dataset: bool
    blockers: list[str] = Field(default_factory=list)


class YTrueRecord(BaseModel):
    y_true_id: str
    target_id: str
    benchmark_id: str
    observable_class: str
    normalized_variable_name: str
    value: float | str | bool
    unit: str | None = None
    uncertainty: float | None = None
    source_id: str
    extract_id: str
    source_hash: str
    source_location_type: str
    source_location_value: str
    extraction_method: str
    approximate: bool
    qc_status: str
    limitations: list[str] = Field(default_factory=list)
    matched_prediction_ids: list[str] = Field(default_factory=list)


class QueueItem(BaseModel):
    target_id: str
    source_id: str
    observable_class: str
    expected_measurement: str
    source_location_hint: str
    required_action: str
    priority: str
    blocking_reason: str


class BlockedTarget(BaseModel):
    target_id: str
    benchmark_id: str
    source_id: str
    observable_class: str
    blocked_reason: str
    required_action: str
    priority: str
    can_be_unblocked: bool


class DatasetQualityReport(BaseModel):
    target_count: int
    candidate_count: int
    accepted_y_true_count: int
    blocked_count: int
    manual_table_queue_count: int
    figure_digitization_queue_count: int
    public_dataset_lookup_count: int
    supplementary_lookup_count: int
    qc_pass_count: int
    qc_fail_count: int
    unit_normalization_issues: int
    source_coverage_issues: int
    prediction_matching_issues: int
    readiness_status: str
    recommendations: list[str] = Field(default_factory=list)


class AssembledDatasetPayload(BaseModel):
    dataset_id: str = "YTRUE-DATASET-v4_3"
    created_at: str
    source_plan_ref: str
    target_count: int
    y_true_record_count: int
    records: list[YTrueRecord] = Field(default_factory=list)
    ready_for_predictive_gain: bool
    predictive_gain_status: str | None = None
    slot4_debt_status: str
    physical_claim_permission: str
    notes: list[str] = Field(default_factory=list)


class NextPredictiveGainInputs(BaseModel):
    ready_for_predictive_gain: bool
    y_true_dataset_path: str
    prediction_dataset_path: str
    matched_prediction_count: int
    minimum_viable_y_true_count: int
    predictive_gain_status: str | None = None
    recommended_next_phase: str
    blocked_claims: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ExtractionGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    source_coverage_audit: list[SourceCoverageAuditRecord] = Field(default_factory=list)
    extraction_candidates: list[YTrueExtractionCandidate] = Field(default_factory=list)
    manual_table_extraction_queue: list[QueueItem] = Field(default_factory=list)
    figure_digitization_queue: list[QueueItem] = Field(default_factory=list)
    public_dataset_lookup_queue: list[QueueItem] = Field(default_factory=list)
    supplementary_lookup_queue: list[QueueItem] = Field(default_factory=list)
    assembled_y_true_dataset: AssembledDatasetPayload
    blocked_y_true_targets: list[BlockedTarget] = Field(default_factory=list)
    dataset_quality_report: DatasetQualityReport
    next_predictive_gain_inputs: NextPredictiveGainInputs
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class ExtractionCampaignResult(BaseModel):
    campaign_id: str = "PHI-GRADIENT-REAL-YTRUE-EXTRACTION-v4_3"
    status: str
    gate_result: ExtractionGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class ExtractionInputs(BaseModel):
    observable_schema: dict = Field(default_factory=dict)
    normalized_targets: dict = Field(default_factory=dict)
    y_true_acquisition_plan: dict = Field(default_factory=dict)
    dataset_source_registry: dict = Field(default_factory=dict)
    measurement_readiness_matrix: dict = Field(default_factory=dict)
    quality_control_rules: dict = Field(default_factory=dict)
    v4_2_next_gate_inputs: dict = Field(default_factory=dict)
    benchmark_rows: dict = Field(default_factory=dict)
    source_hashes: dict = Field(default_factory=dict)
    debt_object: dict = Field(default_factory=dict)
    model_predictions: dict = Field(default_factory=dict)
    blocked_reason: str | None = None
