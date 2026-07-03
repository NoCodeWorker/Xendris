"""Schemas for v3.8 extract candidate review."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class RawExtractionCandidate(BaseModel):
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


class ReviewedExtractionCandidate(BaseModel):
    candidate_id: str
    source_id: str
    sha256: str
    page_number: int | None = None
    location_type: str
    location_value: str
    candidate_type: str
    extracted_text: str
    component_role: str
    review_status: str
    validation_ready: bool = False
    manual_review_required: bool = True
    limitations: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ValidationReadyExtract(BaseModel):
    extract_id: str
    source_id: str
    sha256: str
    source_filename: str | None = None
    page_number: int | None = None
    location_type: str
    location_value: str
    exact_text: str
    candidate_type: str
    component_role: str
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    review_status: str
    validation_ready: bool
    next_gate_required: str = "v3.9 validation-ready extract gate"


class ValidationReadyExtractPack(BaseModel):
    pack_id: str = "PHI-GRADIENT-VALIDATION-READY-EXTRACT-PACK-v3_8"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    source_manifest_ref: str = "data/real_sources/source_hashes_v3_6.json"
    extraction_manifest_ref: str = "data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json"
    extracts: list[ValidationReadyExtract] = Field(default_factory=list)
    rejected_count: int = 0
    manual_review_count: int = 0
    validation_ready_count: int = 0
    status: str = "PHI_GRADIENT_EXTRACT_REVIEW_NO_VALIDATION_READY_EXTRACTS"
    notes: list[str] = Field(default_factory=list)


class RejectedExtractionCandidate(BaseModel):
    candidate_id: str
    source_id: str
    reason: str
    original_candidate_type: str
    short_text_preview: str
    review_status: str


class ManualReviewQueueItem(BaseModel):
    candidate_id: str
    source_id: str
    page_number: int | None = None
    candidate_type: str
    text_preview: str
    reason: str
    priority: str
    suggested_action: str


class ReviewedCandidateMapEntry(BaseModel):
    candidate_id: str
    source_id: str
    review_decision: str
    component_role: str
    output_record_id: str | None = None
    notes: list[str] = Field(default_factory=list)


class PhiGradientExtractCandidateReviewGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    input_candidate_count: int = 0
    validation_ready_count: int = 0
    rejected_count: int = 0
    manual_review_count: int = 0
    component_role_counts: dict[str, int] = Field(default_factory=dict)
    pedernales_blocked: bool = False
    reviewed_candidates: list[ReviewedExtractionCandidate] = Field(default_factory=list)
    validation_ready_pack: ValidationReadyExtractPack
    rejected_candidates: list[RejectedExtractionCandidate] = Field(default_factory=list)
    manual_review_queue: list[ManualReviewQueueItem] = Field(default_factory=list)
    reviewed_candidate_map: list[ReviewedCandidateMapEntry] = Field(default_factory=list)
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientExtractCandidateReviewCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientExtractCandidateReviewGateResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
