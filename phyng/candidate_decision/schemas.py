from __future__ import annotations
from pydantic import BaseModel, Field

class CandidateFreezeReview(BaseModel):
    candidate_id: str
    freeze_decision_ref: str
    freeze_status: str
    accepted_y_true_count: int
    predictive_gain_status: str
    slot4_debt_status: str
    review_status: str
    notes: list[str] = Field(default_factory=list)

class FinalClaimPermissions(BaseModel):
    candidate_id: str
    decision_ref: str
    predictive_gain_permission: str
    physical_claim_permission: str
    gradient_mechanism_claim_permission: str
    benchmark_method_permission: str
    method_only_permission: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    archived_claims: list[str] = Field(default_factory=list)
    required_to_unblock: list[str] = Field(default_factory=list)

class MethodOnlyRedefinition(BaseModel):
    candidate_id: str
    redefinition_status: str
    allowed_method_roles: list[str] = Field(default_factory=list)
    prohibited_scientific_roles: list[str] = Field(default_factory=list)
    allowed_future_use: list[str] = Field(default_factory=list)
    required_label: str
    notes: list[str] = Field(default_factory=list)

class ExperimentRequirement(BaseModel):
    candidate_id: str
    requirement_status: str
    required_observables: list[str] = Field(default_factory=list)
    minimum_measurements: int
    required_sensitivity: str | None = None
    required_apparatus: list[str] = Field(default_factory=list)
    feasibility_risk: str
    cost_risk: str
    timeline_risk: str
    reason: str
    recommended_action: str

class CandidateFamilySelectionRecord(BaseModel):
    family_id: str
    previous_status: str
    synthetic_survivability_score: float | None = None
    negative_control_resistance_score: float | None = None
    source_support_availability: str
    y_true_accessibility: str
    public_dataset_availability: str
    observable_clarity: str
    slot4_independence: str
    experimental_feasibility: str
    claim_risk_level: str
    selection_score: float
    recommended_action: str
    notes: list[str] = Field(default_factory=list)

class PivotDecision(BaseModel):
    candidate_id: str
    decision_ref: str
    freeze_review_status: str
    pivot_recommended: bool
    next_candidate_family: str | None = None
    recommended_next_phase: str
    notes: list[str] = Field(default_factory=list)

class CampaignResultv46(BaseModel):
    status: str
    freeze_review: CandidateFreezeReview
    permissions: FinalClaimPermissions
    redefinition: MethodOnlyRedefinition
    experiment: ExperimentRequirement
    matrix: list[CandidateFamilySelectionRecord] = Field(default_factory=list)
    pivot: PivotDecision
