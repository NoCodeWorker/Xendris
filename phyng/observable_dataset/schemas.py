"""Schemas for v4.2 observable dataset and y_true plan."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class ObservableSchemaRecord(BaseModel):
    observable_class: str
    canonical_name: str
    allowed_units: list[str] = Field(default_factory=list)
    expected_data_type: str
    valid_range_description: str
    source_slots: list[str] = Field(default_factory=list)
    measurement_requirement: str
    y_true_definition: str
    notes: list[str] = Field(default_factory=list)


class NormalizedObservableTarget(BaseModel):
    target_id: str
    benchmark_id: str
    source_id: str
    extract_id: str
    observable_class: str
    observable_name: str
    source_observable_text: str
    normalized_variable_name: str
    unit: str | None = None
    expected_dtype: str
    measurement_context: str
    regime_fields: dict[str, str | None] = Field(default_factory=dict)
    candidate_model_fields: list[str] = Field(default_factory=list)
    baseline_model_fields: list[str] = Field(default_factory=list)
    y_true_required: bool = True
    y_true_status: str
    slot4_debt_status: str
    predictive_gain_allowed: bool = False
    notes: list[str] = Field(default_factory=list)


class YTrueAcquisitionItem(BaseModel):
    acquisition_id: str
    target_id: str
    observable_class: str
    y_true_status: str
    required_measurement: str
    candidate_data_sources: list[str] = Field(default_factory=list)
    acquisition_method: str
    manual_extraction_required: bool
    experimental_required: bool
    expected_unit: str | None = None
    quality_requirements: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    priority: str


class DatasetSourceRegistryRecord(BaseModel):
    dataset_source_id: str
    related_source_id: str
    source_type: str
    access_status: str
    expected_observables: list[str] = Field(default_factory=list)
    acquisition_method: str
    requires_manual_review: bool
    notes: list[str] = Field(default_factory=list)


class MeasurementReadinessRecord(BaseModel):
    observable_class: str
    target_count: int
    y_true_available_count: int
    public_data_acquirable_count: int
    manual_extraction_count: int
    experiment_required_count: int
    blocked_count: int
    readiness_status: str
    next_action: str


class QualityControlRules(BaseModel):
    rules_id: str = "QC-RULES-v4_2"
    rules: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ObservableYTrueGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    schema_records: list[ObservableSchemaRecord] = Field(default_factory=list)
    normalized_targets: list[NormalizedObservableTarget] = Field(default_factory=list)
    y_true_acquisition_plan: list[YTrueAcquisitionItem] = Field(default_factory=list)
    source_registry: list[DatasetSourceRegistryRecord] = Field(default_factory=list)
    readiness_matrix: list[MeasurementReadinessRecord] = Field(default_factory=list)
    qc_rules: QualityControlRules
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class ObservableYTrueCampaignResult(BaseModel):
    campaign_id: str = "PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2"
    status: str
    gate_result: ObservableYTrueGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class ObservableYTrueInputs(BaseModel):
    model_registry: dict = Field(default_factory=dict)
    model_predictions: dict = Field(default_factory=dict)
    benchmark_scores: dict = Field(default_factory=dict)
    negative_control_results: dict = Field(default_factory=dict)
    claim_permission_update: dict = Field(default_factory=dict)
    next_gate_inputs: dict = Field(default_factory=dict)
    benchmark_rows: dict = Field(default_factory=dict)
    observable_alignment: dict = Field(default_factory=dict)
    debt_object: dict = Field(default_factory=dict)
    blocked_reason: str | None = None
