"""Schemas for v3.2 source-pack seed population."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class SeedSourceManifestEntry(BaseModel):
    source_id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    url: str | None = None
    local_path: str | None = None
    source_type: str = "paper"
    target_slots: list[str] = Field(default_factory=list)
    expected_components: list[str] = Field(default_factory=list)
    review_status: str = "REVIEWED_SOURCE_CANDIDATE"
    reviewer_notes: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    evidence_status: str = "CANDIDATE_NOT_VALIDATED"


class SeedSourceManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-REVIEWED-SOURCE-PACK-v3_2"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    created_at: str = "2026-06-30"
    entries: list[SeedSourceManifestEntry] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class SeedSourceExtract(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    extract_text_or_paraphrase: str
    exact_quote_available: bool = False
    quote_location: str | None = None
    equation_text: str | None = None
    observable_text: str | None = None
    parameter_constraint_text: str | None = None
    benchmark_data_text: str | None = None
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    manual_review_required: bool = True
    extraction_notes: list[str] = Field(default_factory=list)
    initial_validation_status: str = "EXTRACT_CANDIDATE_REQUIRES_REVIEW"


class SeedSourceExtractPack(BaseModel):
    extract_pack_id: str = "PHI-GRADIENT-EXTRACT-PACK-v3_2"
    manifest_id: str = "PHI-GRADIENT-REVIEWED-SOURCE-PACK-v3_2"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    extracts: list[SeedSourceExtract] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class SourcePackPopulationValidationResult(BaseModel):
    status: str
    manifest_entry_count: int = 0
    extract_count: int = 0
    traceable_entry_count: int = 0
    valid_slot_entry_count: int = 0
    benchmark_candidate_count: int = 0
    negative_candidate_count: int = 0
    manual_review_extract_count: int = 0
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class PhiGradientSourcePackPopulationResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: SeedSourceManifest
    extract_pack: SeedSourceExtractPack
    validation: SourcePackPopulationValidationResult
    manifest_path: str
    extract_pack_path: str
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientSourcePackPopulationCampaignResult(BaseModel):
    campaign_id: str
    status: str
    population_result: PhiGradientSourcePackPopulationResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
