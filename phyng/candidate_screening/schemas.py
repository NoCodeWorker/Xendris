from __future__ import annotations
from pydantic import BaseModel, Field

class SourceAccessibilityScreen(BaseModel):
    candidate_family: str
    likely_source_domains: list[str] = Field(default_factory=list)
    known_source_refs: list[str] = Field(default_factory=list)
    local_source_refs: list[str] = Field(default_factory=list)
    source_location_quality: str
    source_accessibility_score: float
    blockers: list[str] = Field(default_factory=list)
    recommended_next_action: str

class ObservableAccessibilityScreen(BaseModel):
    candidate_family: str
    proposed_observables: list[str] = Field(default_factory=list)
    observable_classes: list[str] = Field(default_factory=list)
    directly_measurable: list[str] = Field(default_factory=list)
    proxy_observables: list[str] = Field(default_factory=list)
    blocked_observables: list[str] = Field(default_factory=list)
    observable_clarity: str
    observable_accessibility_score: float
    notes: list[str] = Field(default_factory=list)

class YTrueAccessibilityScreen(BaseModel):
    candidate_family: str
    target_observables: list[str] = Field(default_factory=list)
    plausible_ytrue_sources: list[str] = Field(default_factory=list)
    manual_extraction_likelihood: str
    public_dataset_likelihood: str
    experiment_required: bool
    minimum_ytrue_feasibility: str
    ytrue_accessibility_score: float
    blockers: list[str] = Field(default_factory=list)

class PublicDatasetScreen(BaseModel):
    candidate_family: str
    plausible_repository_types: list[str] = Field(default_factory=list)
    known_dataset_refs: list[str] = Field(default_factory=list)
    local_dataset_refs: list[str] = Field(default_factory=list)
    dataset_availability: str
    dataset_accessibility_score: float
    required_search_queries: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

class ExperimentalFeasibilityScreen(BaseModel):
    candidate_family: str
    required_observables: list[str] = Field(default_factory=list)
    possible_experiment_classes: list[str] = Field(default_factory=list)
    required_apparatus: list[str] = Field(default_factory=list)
    required_sensitivity: str | None = None
    feasibility_level: str
    cost_risk: str
    timeline_risk: str
    experiment_accessibility_score: float
    notes: list[str] = Field(default_factory=list)

class ClaimRiskScreen(BaseModel):
    candidate_family: str
    physical_claim_risk: str
    source_overclaim_risk: str
    benchmark_laundering_risk: str
    slot4_dependency_risk: str
    predictive_gain_misuse_risk: str
    mitigation_rules: list[str] = Field(default_factory=list)
    claim_risk_score: float

class CandidateScreeningDecision(BaseModel):
    candidate_family: str
    final_status: str
    source_score: float
    observable_score: float
    ytrue_score: float
    public_dataset_score: float
    experimental_feasibility_score: float
    claim_risk_score: float
    aggregate_accessibility_score: float
    pass_criteria_met: list[str] = Field(default_factory=list)
    fail_criteria_met: list[str] = Field(default_factory=list)
    allowed_next_phase: str | None = None
    blocked_next_phases: list[str] = Field(default_factory=list)
    required_guardrails: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

class CampaignResultv47(BaseModel):
    status: str
    source_screen: SourceAccessibilityScreen
    observable_screen: ObservableAccessibilityScreen
    ytrue_screen: YTrueAccessibilityScreen
    public_dataset: PublicDatasetScreen
    experiment: ExperimentalFeasibilityScreen
    claim_risk: ClaimRiskScreen
    decision: CandidateScreeningDecision
