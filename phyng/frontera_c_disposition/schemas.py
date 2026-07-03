"""Schemas for v5.6 LOG_BOUNDARY control failure disposition."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ControlFailureInputs(BaseModel):
    root: str
    missing_files: list[str] = Field(default_factory=list)
    control_decision: dict = Field(default_factory=dict)
    next_gate_decision: dict = Field(default_factory=dict)
    predictive_gain_smoke_test: dict = Field(default_factory=dict)
    ytrue_dataset: dict = Field(default_factory=dict)
    accepted_ytrue: dict = Field(default_factory=dict)
    error_metrics: dict = Field(default_factory=dict)
    leakage_tests: dict = Field(default_factory=dict)
    loo_results: dict = Field(default_factory=dict)


class ControlFailureReview(BaseModel):
    candidate_family: str
    previous_status: str
    positive_smoke_test_ref: str
    negative_control_ref: str
    failure_summary: str
    primary_failure_reason: str
    supporting_control_results: list[dict] = Field(default_factory=list)
    can_proceed_to_c_structure_ablation: bool
    can_support_frontera_c_validation: bool
    notes: list[str] = Field(default_factory=list)


class CandidateDisposition(BaseModel):
    candidate_family: str
    primary_disposition: str
    secondary_roles: list[str] = Field(default_factory=list)
    archived_as_validation_candidate: bool
    retained_as_fixture: bool
    reason: str
    required_to_reopen_as_candidate: list[str] = Field(default_factory=list)
    prohibited_actions: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class AllowedFutureRoles(BaseModel):
    candidate_family: str
    allowed_roles: list[str] = Field(default_factory=list)
    blocked_roles: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class BlockedClaims(BaseModel):
    candidate_family: str
    blocked_claims: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    claim_permission: str
    physical_claim_created: bool = False
    frontera_c_validated: bool = False
    invariant_confirmed: bool = False


class FronteraCRoadmapUpdate(BaseModel):
    previous_active_candidate: str
    previous_blocker: str
    new_blocker: str
    candidates_archived: list[str] = Field(default_factory=list)
    candidates_retained_as_fixtures: list[str] = Field(default_factory=list)
    current_validation_status: str
    next_viable_paths: list[str] = Field(default_factory=list)
    recommended_path: str
    rationale: str
    forbidden_paths: list[str] = Field(default_factory=list)


class NextResearchDirection(BaseModel):
    final_status: str
    selected_next_direction: str
    allowed_next_phase: str | None = None
    blocked_next_phases: list[str] = Field(default_factory=list)
    required_inputs: list[str] = Field(default_factory=list)
    rationale: str
    blocked_claims: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class LogBoundaryControlFailureCampaignResult(BaseModel):
    campaign_id: str = "FRONTERA-C-LOG-BOUNDARY-CONTROL-FAILURE-REVIEW-v5_6"
    status: str
    inputs_loaded: bool
    review: ControlFailureReview | None = None
    disposition: CandidateDisposition | None = None
    future_roles: AllowedFutureRoles | None = None
    blocked_claims: BlockedClaims | None = None
    roadmap_update: FronteraCRoadmapUpdate | None = None
    next_direction: NextResearchDirection | None = None
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
    missing_files: list[str] = Field(default_factory=list)
