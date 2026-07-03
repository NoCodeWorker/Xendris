"""Schemas for the v2.2 heuristic discovery layer."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


HeuristicStatus = Literal[
    "HEURISTIC_SEED",
    "HEURISTIC_PRIORITIZED",
    "HEURISTIC_TEST_DESIGN_READY",
    "HEURISTIC_REVIEW_REQUIRED",
    "HEURISTIC_REJECTED_DIMENSIONAL_INCONSISTENCY",
    "HEURISTIC_REJECTED_AD_HOC",
    "HEURISTIC_REJECTED_NO_OBSERVABLE",
]


class HeuristicCandidate(BaseModel):
    candidate_id: str
    domain: str
    raw_idea: str
    proposed_hypothesis: str
    candidate_family: str | None = None
    suggested_observables: list[str] = Field(default_factory=list)
    suggested_proxies: list[str] = Field(default_factory=list)
    required_sources: list[str] = Field(default_factory=list)
    required_benchmarks: list[str] = Field(default_factory=list)
    failure_conditions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    heuristic_scores: dict[str, float] = Field(default_factory=dict)
    canonical_status: CanonicalStatusRecord


class HeuristicScorecard(BaseModel):
    candidate_id: str
    detectability_potential: float = 0.0
    non_ad_hoc_score: float = 0.0
    dimensional_consistency: float = 0.0
    falsifiability: float = 0.0
    benchmarkability: float = 0.0
    source_searchability: float = 0.0
    simplicity: float = 0.0
    novelty: float = 0.0
    cost_to_test_inverse: float = 0.0
    risk_penalty: float = 0.0
    priority_score: float = 0.0
    evidence_note: str = "Priority score is not evidence."


class HeuristicRankingResult(BaseModel):
    candidates: list[HeuristicCandidate]
    ranking_method: str
    weights: dict[str, float]
    top_candidate_id: str | None = None
    warnings: list[str] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord


class HeuristicPermissionGateResult(BaseModel):
    candidate_id: str
    domain_status: HeuristicStatus
    is_claim_authorized: bool = False
    is_test_design_allowed: bool = False
    missing_fields: list[str] = Field(default_factory=list)
    blocked_reasons: list[str] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord
    notes: list[str] = Field(default_factory=list)


class HeuristicPipelineResult(BaseModel):
    raw_problem: str
    domain: str
    candidates: list[HeuristicCandidate]
    ranking: HeuristicRankingResult
    permission_results: list[HeuristicPermissionGateResult]
    top_candidate: HeuristicCandidate | None = None
    missing_fields: list[str] = Field(default_factory=list)
    next_best_question: str
    canonical_status: CanonicalStatusRecord


class HeuristicDiscoveryCampaignResult(BaseModel):
    campaign_id: str
    status: str
    pipeline_result: HeuristicPipelineResult
    report_paths: dict[str, str] = Field(default_factory=dict)
