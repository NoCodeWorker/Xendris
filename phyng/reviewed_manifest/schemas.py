"""Schemas for v3.1 reviewed local manifest and extract pack."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.real_source_ingestion.schemas import RealSourceExtractValidationResult


class ReviewedSourceManifestEntry(BaseModel):
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
    review_status: str = "REVIEWED_SOURCE_REQUIRES_MANUAL_REVIEW"
    reviewer_notes: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    is_fixture: bool = False
    is_test_double: bool = False


class ReviewedSourceManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-REVIEWED-MANIFEST-v3_1"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    created_at: str = "2026-06-30"
    reviewer: str | None = None
    entries: list[ReviewedSourceManifestEntry] = Field(default_factory=list)
    fixture_entries: list[str] = Field(default_factory=list)
    test_double_entries: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ReviewedSourceManifestValidationResult(BaseModel):
    status: str
    manifest_id: str
    entry_count: int = 0
    traceable_entry_count: int = 0
    accepted_entry_ids: list[str] = Field(default_factory=list)
    rejected_entry_ids: list[str] = Field(default_factory=list)
    fixture_entry_ids: list[str] = Field(default_factory=list)
    test_double_entry_ids: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


class ReviewedSourceExtract(BaseModel):
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
    manual_review_required: bool = False
    extraction_notes: list[str] = Field(default_factory=list)
    is_fixture: bool = False
    is_test_double: bool = False


class ReviewedSourceExtractPack(BaseModel):
    extract_pack_id: str = "PHI-GRADIENT-EXTRACT-PACK-v3_1"
    manifest_id: str = "PHI-GRADIENT-REVIEWED-MANIFEST-v3_1"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    extracts: list[ReviewedSourceExtract] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ReviewedSourceExtractValidationResult(BaseModel):
    extract_id: str
    source_id: str
    slot_id: str
    status: str
    counts_as_real_support: bool = False
    bridge_validation: RealSourceExtractValidationResult | None = None
    reasons: list[str] = Field(default_factory=list)


class ReviewedSlotCoverageRecord(BaseModel):
    slot_id: str
    coverage_status: str
    candidate_sources: list[str] = Field(default_factory=list)
    validated_extracts: list[str] = Field(default_factory=list)
    accepted_support_count: int = 0
    missing_requirements: list[str] = Field(default_factory=list)


class ReviewedSlotCoverageMatrix(BaseModel):
    records: list[ReviewedSlotCoverageRecord] = Field(default_factory=list)
    missing_slots: list[str] = Field(default_factory=list)


class ReviewedBenchmarkComparabilityResult(BaseModel):
    status: str
    comparable_records: int = 0
    missing_requirements: list[str] = Field(default_factory=list)


class PhiGradientReviewedManifestGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: ReviewedSourceManifest
    manifest_validation: ReviewedSourceManifestValidationResult
    extract_pack: ReviewedSourceExtractPack
    extract_validations: list[ReviewedSourceExtractValidationResult] = Field(default_factory=list)
    slot_coverage: ReviewedSlotCoverageMatrix
    negative_source_ids: list[str] = Field(default_factory=list)
    benchmark_comparability: ReviewedBenchmarkComparabilityResult
    manifest_created: bool = False
    extract_pack_created: bool = False
    validated_extract_count: int = 0
    rejected_analogy_count: int = 0
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientReviewedManifestCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientReviewedManifestGateResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
