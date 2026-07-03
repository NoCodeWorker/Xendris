"""Schemas for v3.0 real source acquisition."""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.real_source_ingestion.schemas import RealSourceExtractValidationResult


class SlotQuery(BaseModel):
    query_id: str
    slot_id: str
    query_text: str
    expected_components: list[str] = Field(default_factory=list)
    priority: int
    source_types: list[str] = Field(default_factory=list)


class RealSourceQueryPlan(BaseModel):
    campaign_id: str
    target_candidate: str
    slot_queries: list[SlotQuery] = Field(default_factory=list)
    negative_queries: list[SlotQuery] = Field(default_factory=list)
    benchmark_queries: list[SlotQuery] = Field(default_factory=list)
    acquisition_limits: dict[str, int] = Field(default_factory=dict)
    inclusion_rules: list[str] = Field(default_factory=list)
    exclusion_rules: list[str] = Field(default_factory=list)


class RealSourceCandidate(BaseModel):
    source_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source_type: str
    url: str | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    local_path: str | None = None
    targeted_slots: list[str] = Field(default_factory=list)
    expected_components: list[str] = Field(default_factory=list)
    acquisition_status: str = "REAL_SOURCE_CANDIDATE_IDENTIFIED"
    reason_for_inclusion: str
    analogy_risk: str = "UNKNOWN"
    is_support: bool = False


class RealSourceCandidateManifest(BaseModel):
    candidates: list[RealSourceCandidate] = Field(default_factory=list)
    actual_real_sources_acquired: bool = False
    backend_status: str
    notes: list[str] = Field(default_factory=list)


class RealExtractIngestionResult(BaseModel):
    source_id: str
    attempted: bool
    status: str
    validation: RealSourceExtractValidationResult | None = None
    notes: list[str] = Field(default_factory=list)


class SlotCoverageRecord(BaseModel):
    slot_id: str
    required_component: str
    candidate_sources: list[str] = Field(default_factory=list)
    validated_extracts: list[str] = Field(default_factory=list)
    accepted_support_count: int = 0
    analogy_only_count: int = 0
    negative_count: int = 0
    coverage_status: str
    missing_requirements: list[str] = Field(default_factory=list)


class SlotCoverageMatrix(BaseModel):
    records: list[SlotCoverageRecord] = Field(default_factory=list)
    missing_slots: list[str] = Field(default_factory=list)


class NegativeSourceRecord(BaseModel):
    source_id: str
    slot_id: str
    contradicted_component: str
    severity: str = "REVIEW"
    blocks_upgrade: bool = True


class BenchmarkComparabilityResult(BaseModel):
    benchmark_id: str | None = None
    status: str
    comparable_records: int = 0
    missing_requirements: list[str] = Field(default_factory=list)


class PhiGradientRealSourceAcquisitionResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    query_plan: RealSourceQueryPlan
    candidate_manifest: RealSourceCandidateManifest
    ingestion_results: list[RealExtractIngestionResult] = Field(default_factory=list)
    slot_coverage: SlotCoverageMatrix
    negative_sources: list[NegativeSourceRecord] = Field(default_factory=list)
    benchmark_comparability: BenchmarkComparabilityResult
    actual_real_sources_acquired: bool = False
    actual_real_extracts_validated: bool = False
    backend_status: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientRealSourceAcquisitionCampaignResult(BaseModel):
    campaign_id: str
    status: str
    acquisition_result: PhiGradientRealSourceAcquisitionResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)


class SourceAcquisitionBackend(Protocol):
    backend_name: str

    def search(self, query: SlotQuery) -> list[RealSourceCandidate]:
        ...
