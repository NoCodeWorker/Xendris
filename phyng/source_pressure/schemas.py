"""Schemas for PHI_GRADIENT source and benchmark pressure."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class SourceEvidenceSlot(BaseModel):
    slot_id: str
    slot_name: str
    required_component: str
    acceptable_support_types: list[str] = Field(default_factory=list)
    unacceptable_support_types: list[str] = Field(default_factory=list)
    minimum_extract_fields: list[str] = Field(default_factory=list)
    status: str = "UNFILLED"


class SourceCandidate(BaseModel):
    source_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    source_type: str
    url_or_path: str | None = None
    slot_ids: list[str] = Field(default_factory=list)
    extracted_claims: list[str] = Field(default_factory=list)
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    equations_found: list[str] = Field(default_factory=list)
    observables_found: list[str] = Field(default_factory=list)
    parameter_constraints_found: list[str] = Field(default_factory=list)
    benchmark_data_found: bool = False
    citation_quality: str = "fixture"


class SourceSupportAssessment(BaseModel):
    source_id: str
    status: str
    counts_as_support: bool
    supported_slots: list[str] = Field(default_factory=list)
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    canonical_status: CanonicalStatusRecord


class BenchmarkPressureRecord(BaseModel):
    benchmark_id: str
    source_id: str | None = None
    observable: str
    parameter_ranges: dict[str, tuple[float, float]] = Field(default_factory=dict)
    data_type: str
    supports_baseline: bool = False
    supports_candidate_component: bool = False
    constrains_alpha: bool = False
    comparable_to_phi_gradient: bool = False
    has_visibility_or_decoherence_measure: bool = False
    has_environmental_baseline: bool = False
    citation_or_path: str | None = None
    limitations: list[str] = Field(default_factory=list)
    status: str = "UNASSESSED"


class PhiGradientBenchmarkPressureResult(BaseModel):
    benchmark_id: str
    status: str
    counts_as_benchmark_support: bool
    canonical_status: CanonicalStatusRecord
    reasons: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class PhiGradientSourcePressureResult(BaseModel):
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    status: str
    canonical_status: CanonicalStatusRecord
    slots: list[SourceEvidenceSlot] = Field(default_factory=list)
    sources: list[SourceCandidate] = Field(default_factory=list)
    assessments: list[SourceSupportAssessment] = Field(default_factory=list)
    negative_sources: list[SourceSupportAssessment] = Field(default_factory=list)
    missing_requirements: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    fixture_based: bool = True


class PhiGradientSourceBenchmarkCampaignResult(BaseModel):
    campaign_id: str
    status: str
    source_result: PhiGradientSourcePressureResult
    benchmark_results: list[PhiGradientBenchmarkPressureResult] = Field(default_factory=list)
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
