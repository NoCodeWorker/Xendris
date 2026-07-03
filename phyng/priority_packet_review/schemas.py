"""Schemas for v3.8.3 priority packet review."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.semantic_triage.schemas import PriorityReviewItem, SemanticTriageRecord


class PriorityPacketReviewInputs(BaseModel):
    triage_records: list[SemanticTriageRecord] = Field(default_factory=list)
    priority_packet: list[PriorityReviewItem] = Field(default_factory=list)
    slot_review_queues: dict = Field(default_factory=dict)
    next_gate_readiness: dict = Field(default_factory=dict)
    pdf_text_extraction: dict = Field(default_factory=dict)
    extraction_manifest: dict = Field(default_factory=dict)
    source_hashes: dict = Field(default_factory=dict)
    blocked_reason: str | None = None


class ReviewTarget(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    page_number: int | None = None
    assigned_slot: str
    priority: str
    exact_text_or_preview: str
    review_question: str
    decision_needed: str
    triage_record: SemanticTriageRecord | None = None


class ValidationReadyExtractV383(BaseModel):
    extract_id: str
    source_id: str
    sha256: str
    source_filename: str | None = None
    page_number: int | None = None
    location_type: str
    location_value: str
    exact_text: str
    source_candidate_id: str
    assigned_slot: str
    component_role: str
    promotion_decision: str
    why_promoted: str
    limitations: list[str] = Field(default_factory=list)
    possible_pressure_direction: str
    validation_questions: list[str] = Field(default_factory=list)
    next_gate_required: str = "v3.9 source-pressure decision gate"


class ValidationReadyExtractPackV383(BaseModel):
    pack_id: str = "PHI-GRADIENT-VALIDATION-READY-EXTRACT-PACK-v3_8_3"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    created_at: str = "2026-07-01"
    source_manifest_ref: str = "data/real_sources/source_hashes_v3_6.json"
    triage_packet_ref: str = "data/real_sources/extracts/phi_gradient_priority_review_packet_v3_8_2.json"
    extracts: list[ValidationReadyExtractV383] = Field(default_factory=list)
    validation_ready_count: int = 0
    source_coverage: dict[str, int] = Field(default_factory=dict)
    slot_coverage: dict[str, int] = Field(default_factory=dict)
    manual_review_count: int = 0
    rejected_count: int = 0
    analogy_only_count: int = 0
    status: str
    ready_for_v3_9: bool = False
    blocked_claims: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class PriorityPacketReviewDecision(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    assigned_slot: str
    priority: str
    decision: str
    reason: str
    output_extract_id: str | None = None
    notes: list[str] = Field(default_factory=list)


class RejectedPriorityItem(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    reason: str
    text_preview: str
    decision: str


class AnalogyOnlyItem(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    assigned_slot: str
    why_analogy_only: str
    text_preview: str


class ManualReviewItemV383(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    page_number: int | None = None
    assigned_slot: str
    priority: str
    reason: str
    suggested_action: str
    text_preview: str


class PhiGradientPriorityPacketReviewGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    input_priority_packet_count: int = 0
    expanded_pedernales_slot4_count: int = 0
    review_target_count: int = 0
    validation_ready_count: int = 0
    rejected_count: int = 0
    manual_review_count: int = 0
    analogy_only_count: int = 0
    ready_for_v3_9: bool = False
    source_coverage: dict[str, int] = Field(default_factory=dict)
    slot_coverage: dict[str, int] = Field(default_factory=dict)
    validation_ready_pack: ValidationReadyExtractPackV383
    decisions: list[PriorityPacketReviewDecision] = Field(default_factory=list)
    rejected_items: list[RejectedPriorityItem] = Field(default_factory=list)
    analogy_only_items: list[AnalogyOnlyItem] = Field(default_factory=list)
    manual_review_queue: list[ManualReviewItemV383] = Field(default_factory=list)
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientPriorityPacketReviewCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientPriorityPacketReviewGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)
