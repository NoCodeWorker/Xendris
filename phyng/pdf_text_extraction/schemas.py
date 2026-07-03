"""Schemas for v3.7 PDF/text extraction."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class RegisteredPDFSource(BaseModel):
    source_id: str
    local_path: str
    sha256: str
    size_bytes: int
    file_type: str = ".pdf"


class ExtractedPageText(BaseModel):
    source_id: str
    sha256: str
    local_path: str
    page_number: int
    text: str
    extraction_method: str
    extraction_status: str


class SourceExtractionSummary(BaseModel):
    source_id: str
    sha256: str | None = None
    local_path: str
    extraction_status: str
    reader_used: str | None = None
    pages_extracted: int = 0
    candidate_count: int = 0
    blocked_reason: str | None = None
    requires_manual_review: bool = False
    reader_availability: dict[str, bool] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)


class PDFExtractionCandidate(BaseModel):
    candidate_id: str
    source_id: str
    sha256: str
    page_number: int | None = None
    location_type: str
    location_value: str
    candidate_type: str
    extracted_text: str
    normalized_text: str | None = None
    confidence: str = "LOW"
    requires_manual_review: bool = True
    notes: list[str] = Field(default_factory=list)


class PDFExtractionCandidateSet(BaseModel):
    manifest_id: str
    candidates: list[PDFExtractionCandidate] = Field(default_factory=list)


class PDFExtractionManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-PDF-EXTRACTION-MANIFEST-v3_7"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    created_at: str = "2026-07-01"
    input_registry_id: str | None = None
    reader_availability: dict[str, bool] = Field(default_factory=dict)
    hashed_sources_seen: int = 0
    sources_extracted: int = 0
    sources_blocked: int = 0
    total_pages_extracted: int = 0
    total_candidates: int = 0
    quote_candidate_count: int = 0
    equation_candidate_count: int = 0
    table_range_candidate_count: int = 0
    negative_candidate_count: int = 0
    manual_review_count: int = 0
    status: str = "PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING"
    source_summaries: list[SourceExtractionSummary] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PhiGradientPDFTextExtractionResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    registered_sources: list[RegisteredPDFSource] = Field(default_factory=list)
    pages: list[ExtractedPageText] = Field(default_factory=list)
    quote_candidates: list[PDFExtractionCandidate] = Field(default_factory=list)
    equation_candidates: list[PDFExtractionCandidate] = Field(default_factory=list)
    table_range_candidates: list[PDFExtractionCandidate] = Field(default_factory=list)
    negative_candidates: list[PDFExtractionCandidate] = Field(default_factory=list)
    manifest: PDFExtractionManifest
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientPDFTextExtractionCampaignResult(BaseModel):
    campaign_id: str
    status: str
    extraction_result: PhiGradientPDFTextExtractionResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
