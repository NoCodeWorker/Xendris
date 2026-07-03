"""Schemas for synthetic benchmark design and execution."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class LogBoundaryCandidateSpec(BaseModel):
    candidate_id: str = "HEUR-PHY-003"
    candidate_family: Literal["LOG_BOUNDARY"] = "LOG_BOUNDARY"
    observable: str
    baseline_equation: str
    candidate_equation: str
    delta_gamma_equation: str
    phi_function: str
    dimensionless_variables: list[str] = Field(default_factory=list)
    parameters: dict[str, float] = Field(default_factory=dict)
    parameter_ranges: dict[str, tuple[float, float]] = Field(default_factory=dict)
    t_grid: list[float] = Field(default_factory=list)
    epsilon_exp: float
    scale_L_declared: bool = True
    scale_L_post_hoc: bool = False
    failure_conditions: list[str] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord


class SyntheticBenchmarkDesign(BaseModel):
    candidate_id: str
    baseline_model: str
    candidate_model: str
    delta_metric: str
    t_grid: list[float]
    parameter_sweep_plan: dict[str, list[float]]
    epsilon_exp: float
    failure_conditions: list[str]


class EquationAdmissibilityResult(BaseModel):
    candidate_id: str
    is_admissible: bool
    blocked_reasons: list[str] = Field(default_factory=list)
    checks_passed: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord


class DetectabilityProtocolSpec(BaseModel):
    candidate_id: str
    baseline_equation: str
    candidate_equation: str
    delta_equation: str
    detectability_metric: str
    epsilon_exp: float
    alpha_sweep: list[float]
    k_sweep: list[float]
    u0_sweep: list[float]
    w0_sweep: list[float]
    detectability_classification_rule: str
    failure_classification_rules: list[str]
    canonical_status: CanonicalStatusRecord


class SyntheticBenchmarkDesignResult(BaseModel):
    candidate_id: str
    status: str
    admissibility: EquationAdmissibilityResult
    benchmark_design: SyntheticBenchmarkDesign | None = None
    detectability_protocol: DetectabilityProtocolSpec | None = None
    canonical_status: CanonicalStatusRecord
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class HeuristicToBenchmarkCampaignResult(BaseModel):
    campaign_id: str
    status: str
    candidate_spec: LogBoundaryCandidateSpec
    design_result: SyntheticBenchmarkDesignResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class BoundaryCoordinates(BaseModel):
    m_kg: float
    L_m: float
    lambda_C_m: float
    r_g_m: float
    Q: float
    B: float
    q: float
    b: float
    u: float
    w: float


class VisibilityCurveResult(BaseModel):
    t_grid: list[float]
    V_base: list[float]
    V_log: list[float]
    delta: list[float]
    Gamma_env: float
    DeltaGamma_log: float
    phi_log: float


class ParameterReasonablenessResult(BaseModel):
    classification: str
    is_declared_toy_range: bool = False
    is_extreme_toy_range: bool = False
    is_post_hoc: bool = False
    is_unjustified_or_unphysical: bool = False
    notes: list[str] = Field(default_factory=list)


class LogBoundarySweepPoint(BaseModel):
    alpha: float
    k: float
    k2: float
    u0: float
    w0: float
    Gamma_env: float
    m_kg: float
    L_m: float
    q: float
    b: float
    u: float
    w: float
    phi_log: float
    DeltaGamma_log: float
    max_abs_delta: float
    detectability_status: str
    parameter_reasonableness: ParameterReasonablenessResult


class LogBoundarySweepResult(BaseModel):
    candidate_id: str
    candidate_family: Literal["LOG_BOUNDARY"] = "LOG_BOUNDARY"
    sweep_count: int
    epsilon_exp: float
    best_point: LogBoundarySweepPoint | None = None
    points: list[LogBoundarySweepPoint] = Field(default_factory=list)
    failure_conditions: list[str] = Field(default_factory=list)


class LogBoundaryExecutionResult(BaseModel):
    candidate_id: str
    candidate_family: Literal["LOG_BOUNDARY"] = "LOG_BOUNDARY"
    status: str
    sweep_result: LogBoundarySweepResult
    canonical_status: CanonicalStatusRecord
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    failure_conditions: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class LogBoundaryLoopFeedbackResult(BaseModel):
    loop_event_id: str
    candidate_id: str
    result_status: str
    canonical_status: CanonicalStatusRecord
    candidate_loop_input: CandidateLoopInput
    candidate_loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    blocked_updates: list[str] = Field(default_factory=list)
    shadow_mode_required: bool = False
    human_review_required: bool = False
    next_actions: list[str] = Field(default_factory=list)
    rollbackable_config_changes: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class LogBoundarySyntheticExecutionCampaignResult(BaseModel):
    campaign_id: str
    status: str
    candidate_spec: LogBoundaryCandidateSpec
    execution_result: LogBoundaryExecutionResult
    loop_feedback: LogBoundaryLoopFeedbackResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class LogBoundaryAblationControl(BaseModel):
    control_id: str
    description: str
    max_abs_delta: float
    phi_value: float | None = None
    detectability_status: str
    notes: list[str] = Field(default_factory=list)


class LogBoundarySensitivityMetrics(BaseModel):
    candidate_delta: float
    constant_phi_delta: float
    mean_phi_delta: float
    remove_u_delta: float
    remove_w_delta: float
    no_log_coordinates_delta: float
    alpha_1_delta: float
    saturation_ratio: float
    control_gain: float
    coordinate_contribution_score: float
    threshold_sensitivity_score: float
    warnings: list[str] = Field(default_factory=list)


class LogBoundaryAblationClassification(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    reason: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LogBoundaryAblationResult(BaseModel):
    candidate_id: str
    candidate_family: Literal["LOG_BOUNDARY"] = "LOG_BOUNDARY"
    execution_result: LogBoundaryExecutionResult
    controls: list[LogBoundaryAblationControl] = Field(default_factory=list)
    metrics: LogBoundarySensitivityMetrics
    classification: LogBoundaryAblationClassification
    failure_conditions: list[str] = Field(default_factory=list)


class LogBoundaryAblationLoopFeedbackResult(BaseModel):
    loop_event_id: str
    candidate_id: str
    ablation_status: str
    canonical_status: CanonicalStatusRecord
    candidate_loop_input: CandidateLoopInput
    candidate_loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    allowed_updates: list[str] = Field(default_factory=list)
    blocked_updates: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class LogBoundarySensitivityAblationCampaignResult(BaseModel):
    campaign_id: str
    status: str
    candidate_spec: LogBoundaryCandidateSpec
    execution_result: LogBoundaryExecutionResult
    ablation_result: LogBoundaryAblationResult
    loop_feedback: LogBoundaryAblationLoopFeedbackResult
    report_paths: dict[str, str] = Field(default_factory=dict)


class PhiCandidateSpec(BaseModel):
    candidate_id: str
    family: str
    formula: str
    parameters: dict[str, float] = Field(default_factory=dict)
    boundedness_claim: str
    dimensionless_inputs: list[str] = Field(default_factory=list)
    known_risks: list[str] = Field(default_factory=list)
    control_expectations: list[str] = Field(default_factory=list)


class PhiControlResistanceMetrics(BaseModel):
    candidate_delta: float
    constant_phi_delta: float
    mean_phi_delta: float
    remove_u_delta: float
    remove_w_delta: float
    no_log_delta: float
    alpha_1_delta: float
    saturation_ratio: float
    control_gain: float
    coordinate_contribution_score: float
    threshold_robustness_score: float
    alpha_sensitivity_score: float
    non_saturation_score: float
    numerical_stability_score: float
    control_resistance_score: float
    warnings: list[str] = Field(default_factory=list)


class PhiCandidateEvaluationResult(BaseModel):
    candidate: PhiCandidateSpec
    classification: str
    canonical_status: CanonicalStatusRecord
    metrics: PhiControlResistanceMetrics
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiCandidateRankingResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    ranked_candidates: list[PhiCandidateEvaluationResult] = Field(default_factory=list)
    survivor_count: int = 0
    best_candidate_family: str | None = None
    ranking_note: str = "Ranking is synthetic-only and is not evidence of physical truth."


class PhiSearchLoopFeedbackResult(BaseModel):
    loop_event_id: str
    result_status: str
    canonical_status: CanonicalStatusRecord
    candidate_loop_input: CandidateLoopInput
    candidate_loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    allowed_updates: list[str] = Field(default_factory=list)
    blocked_updates: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class PhiSearchCampaignResult(BaseModel):
    campaign_id: str
    status: str
    candidate_spec: LogBoundaryCandidateSpec
    evaluations: list[PhiCandidateEvaluationResult] = Field(default_factory=list)
    ranking: PhiCandidateRankingResult
    loop_feedback: PhiSearchLoopFeedbackResult
    report_paths: dict[str, str] = Field(default_factory=dict)
