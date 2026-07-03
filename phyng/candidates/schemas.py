"""
Phygn v1.4 — Candidate Model Schemas
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

ParameterStatus = Literal[
    "FIXED_BY_DEFINITION",
    "SOURCE_BACKED",
    "PRE_REGISTERED",
    "FITTED_WITH_PENALTY",
    "FREE_UNCONSTRAINED",
    "AD_HOC"
]

AdmissibilityStatus = Literal[
    "ADMISSIBLE_TOY_CANDIDATE",
    "ADMISSIBLE_NEGATIVE_CONTROL",
    "UNDERIDENTIFIED_CANDIDATE",
    "BLOCKED_AS_AD_HOC_CANDIDATE",
    "BLOCKED_DIMENSIONAL_INCOMPLETE",
    "REQUIRES_PARAMETER_PRIOR",
    "REQUIRES_SOURCE_BACKING"
]

class CandidatePredictionSpec(BaseModel):
    candidate_id: str = ""
    observable: str | None = None
    baseline_model: str | None = None
    candidate_model: str | None = None
    candidate_term: str | None = None
    parameters: dict[str, float | str] | list[str] = Field(default_factory=dict)
    parameter_status: ParameterStatus | None = None
    data_target: str | None = None
    error_metric: str | None = None
    expected_pattern: str | None = None
    detectability_threshold: float | None = None
    failure_condition: list[str] | str = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    benchmark_ids: list[str] = Field(default_factory=list)
    claim_level_requested: int = 0
    
    # Unit metadata fields for dimensional analysis
    term_units: str | None = None
    alpha_units: str | None = None
    dimensionless_core: str | None = None
    
    # Evidence / implementation flags (for positive prediction gate)
    has_source_support: bool = False
    has_benchmark: bool = False


class CandidateFamilyRecord(BaseModel):
    candidate_family_id: str
    display_name: str
    status_before_v5_9: str
    candidate_type: str
    allowed_role: str
    blocked_roles: list[str] = Field(default_factory=list)
    theoretical_basis: str
    target_observable_classes: list[str] = Field(default_factory=list)
    required_features: list[str] = Field(default_factory=list)
    optional_features: list[str] = Field(default_factory=list)
    prediction_rule_summary: str | None = None
    can_predict_without_ytrue: bool
    can_run_out_of_source: bool
    can_compare_to_baseline: bool
    can_run_negative_controls: bool
    can_run_c_structure_ablation: bool
    scientific_debt_blockers: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class CandidateFeatureSchema(BaseModel):
    dataset_id: str
    target_variable: str
    forbidden_feature_columns: list[str] = Field(default_factory=list)
    allowed_feature_columns: list[str] = Field(default_factory=list)
    missing_required_features_by_candidate: dict[str, list[str]] = Field(default_factory=dict)
    derived_feature_rules: list[dict] = Field(default_factory=list)
    leakage_notes: list[str] = Field(default_factory=list)


class CandidatePredictionRule(BaseModel):
    candidate_family_id: str
    rule_id: str
    rule_status: str
    input_features: list[str] = Field(default_factory=list)
    target_variable: str
    formula_or_algorithm: str
    parameter_policy: str
    training_policy: str
    prediction_domain: str
    constraints: list[str] = Field(default_factory=list)
    leakage_risk: str
    ablation_plan_available: bool
    notes: list[str] = Field(default_factory=list)


class CandidateRealityContactRecord(BaseModel):
    candidate_family_id: str
    has_target_alignment: bool
    has_required_features: bool
    has_prediction_rule: bool
    has_no_leakage: bool
    has_baseline_comparator: bool
    has_control_plan: bool
    has_ablation_plan: bool
    has_no_blocking_debt: bool
    reality_contact_passed: bool
    failure_reasons: list[str] = Field(default_factory=list)


class CandidateLeakageRecord(BaseModel):
    candidate_family_id: str
    target_column_not_used: bool
    original_value_text_not_used: bool
    source_lookup_not_used: bool
    page_figure_lookup_not_used: bool
    condition_value_not_derived_from_target: bool
    duplicate_target_not_used: bool
    posthoc_fit_flagged: bool
    ad_hoc_scale_flagged: bool
    leakage_status: str
    notes: list[str] = Field(default_factory=list)


class CandidateSelectionDecision(BaseModel):
    final_status: str
    selected_candidate_family: str | None = None
    selected_rule_id: str | None = None
    candidate_count: int
    passed_candidate_count: int
    rejected_candidate_count: int
    blocked_by_leakage_count: int
    blocked_by_missing_features_count: int
    blocked_by_scientific_debt_count: int
    rationale: str
    allowed_next_phase: str | None = None
    blocked_next_phases: list[str] = Field(default_factory=list)
