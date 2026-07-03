"""Schemas for v4.1 model comparison and legacy model comparison."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


# --- Legacy comparison schemas ---

class BoundaryCouplingSpec(BaseModel):
    coupling_id: str
    formula: str
    reason: str
    status: str
    forbidden_interpretations: list[str] = Field(default_factory=list)


class ModelComparisonSpec(BaseModel):
    comparison_id: str
    campaign_id: str
    system_id: str
    observable: str
    t: list[float]
    parameters: dict[str, float]
    model_base_name: str
    model_candidate_name: str
    model_base_description: str
    model_candidate_description: str
    error_metric: str
    epsilon_exp: float | None = None
    y_true: list[float] | None = None
    source_ids: list[str] = Field(default_factory=list)
    benchmark_ids: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(default_factory=list)
    status: str
    boundary_coupling: BoundaryCouplingSpec | None = None


class ModelComparisonResult(BaseModel):
    comparison_id: str
    campaign_id: str
    system_id: str
    observable: str
    y_true: list[float] | None = None
    y_base: list[float]
    y_candidate: list[float]
    error_base: float | None = None
    error_candidate: float | None = None
    gain_c: float | None = None
    delta_series: list[float]
    max_abs_delta: float
    detectability_status: str
    predictive_status: str
    evidence_level: int
    maximum_allowed_claim_level: int
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    required_sources: list[str] = Field(default_factory=list)
    required_tests: list[str] = Field(default_factory=list)
    required_next_steps: list[str] = Field(default_factory=list)


# --- v4.1 model comparison schemas ---

class ModelRegistryRecord(BaseModel):
    model_id: str
    model_name: str
    model_family: str
    allowed_claim_scope: str
    uses_slot4_gradient_mechanism: bool
    slot4_debt_compliant: bool
    input_features: list[str] = Field(default_factory=list)
    output_observables: list[str] = Field(default_factory=list)
    parameter_constraints_used: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class ModelPredictionRecord(BaseModel):
    prediction_id: str
    model_id: str
    benchmark_id: str
    source_id: str
    observable_type: str
    predicted_behavior: str
    prediction_basis: str
    uses_real_y_true: bool
    y_true_available: bool
    comparison_allowed: bool
    limitations: list[str] = Field(default_factory=list)


class BenchmarkComparisonScore(BaseModel):
    score_id: str
    model_id: str
    benchmark_row_count: int
    observable_alignment_score: float
    benchmark_coverage_score: float
    parameter_constraint_score: float
    negative_control_score: float
    debt_compliance_score: float
    aggregate_score: float
    predictive_gain: float | None = None
    predictive_gain_status: str
    verdict: str
    limitations: list[str] = Field(default_factory=list)


class NegativeControlResult(BaseModel):
    control_id: str
    control_type: str
    tested_models: list[str] = Field(default_factory=list)
    expected_result_if_candidate_is_only_analogy: str
    expected_result_if_candidate_has_signal: str
    observed_result: str
    survival_status: str
    failure_reason: str | None = None
    claim_impact: str


class ClaimPermissionUpdate(BaseModel):
    update_id: str = "PHI-GRADIENT-CLAIM-PERMISSION-v4_1"
    source_pressure_ref: str
    benchmark_ref: str
    debt_ref: str
    model_comparison_ref: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    conditional_claims: list[str] = Field(default_factory=list)
    physical_claim_permission: str
    gradient_mechanism_claim_permission: str
    benchmark_claim_permission: str
    next_required_gate: str


class ModelComparisonGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    models: list[ModelRegistryRecord] = Field(default_factory=list)
    predictions: list[ModelPredictionRecord] = Field(default_factory=list)
    comparison_scores: list[BenchmarkComparisonScore] = Field(default_factory=list)
    negative_control_results: list[NegativeControlResult] = Field(default_factory=list)
    claim_permission_update: ClaimPermissionUpdate
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class ModelComparisonCampaignResult(BaseModel):
    campaign_id: str = "PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1"
    status: str
    gate_result: ModelComparisonGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class ModelComparisonInputs(BaseModel):
    benchmark_manifest: dict = Field(default_factory=dict)
    observable_alignment: dict = Field(default_factory=dict)
    benchmark_rows: dict = Field(default_factory=dict)
    negative_control_plan: dict = Field(default_factory=dict)
    debt_object: dict = Field(default_factory=dict)
    slot4_resolution_plan: dict = Field(default_factory=dict)
    next_gate_inputs: dict = Field(default_factory=dict)
    blocked_reason: str | None = None
