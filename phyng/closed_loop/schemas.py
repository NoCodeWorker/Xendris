"""Schemas for v2.4 closed-loop learning and meta-improvement."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class CandidateLoopInput(BaseModel):
    loop_id: str
    input_type: str
    domain: str
    candidate_id: str | None = None
    candidate_family: str | None = None
    previous_status: str | None = None
    result_status: str
    payload: dict = Field(default_factory=dict)


class CandidateUpdateProposal(BaseModel):
    proposal_id: str
    proposal_type: str
    candidate_id: str | None = None
    candidate_family: str | None = None
    description: str
    proposed_change: dict = Field(default_factory=dict)
    risk_level: str = "LOW"
    requires_shadow_mode: bool = False
    requires_human_review: bool = False
    forbidden_actions: list[str] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord


class CandidateLoopResult(BaseModel):
    loop_id: str
    input_type: str
    domain: str
    candidate_id: str | None = None
    candidate_family: str | None = None
    previous_status: str | None = None
    new_status: str
    canonical_status: CanonicalStatusRecord
    ledger_event_id: str | None = None
    post_mortem_id: str | None = None
    post_mortem_skip_reason: str | None = None
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    blocked_reasons: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    audit_event_id: str


class MetaObservation(BaseModel):
    observation_id: str
    source: str
    observation_type: str
    summary: str
    evidence: dict = Field(default_factory=dict)


class MetaChangeProposal(BaseModel):
    proposal_id: str
    change_type: str
    description: str
    affected_modules: list[str] = Field(default_factory=list)
    current_behavior: str
    proposed_behavior: str
    risk_level: str = "UNCLASSIFIED"
    requires_shadow_mode: bool = True
    requires_human_review: bool = True
    expected_behavior_change: bool = False
    canonical_status: CanonicalStatusRecord


class ShadowModeResult(BaseModel):
    proposal_id: str
    current_outputs: list[dict] = Field(default_factory=list)
    shadow_outputs: list[dict] = Field(default_factory=list)
    differences: list[dict] = Field(default_factory=list)
    permission_differences: list[dict] = Field(default_factory=list)
    blocked_reason_differences: list[dict] = Field(default_factory=list)
    regression_warnings: list[str] = Field(default_factory=list)
    recommendation: str
    canonical_status: CanonicalStatusRecord


class LoopGuardResult(BaseModel):
    guard_name: str
    passed: bool
    severity: str = "INFO"
    message: str


class MetaImprovementResult(BaseModel):
    observation: MetaObservation
    proposal: MetaChangeProposal
    shadow_result: ShadowModeResult | None = None
    guard_results: list[LoopGuardResult] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord


class VersionedUpdateRecord(BaseModel):
    version_id: str
    proposal_id: str
    previous_config: dict
    new_config: dict
    reason: str
    tests_required: list[str]
    rollback_path: str
    impact_summary: str
    canonical_status: CanonicalStatusRecord


class ClosedLoopCampaignResult(BaseModel):
    campaign_id: str
    status: str
    candidate_loop_result: CandidateLoopResult
    meta_improvement_result: MetaImprovementResult
    shadow_mode_result: ShadowModeResult
    guard_results: list[LoopGuardResult]
    versioned_record: VersionedUpdateRecord
    report_paths: dict[str, str] = Field(default_factory=dict)
