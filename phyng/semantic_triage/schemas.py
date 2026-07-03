"""Schemas for v3.8.2 semantic triage."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.extract_candidate_review.schemas import RawExtractionCandidate


class SemanticTriageInputs(BaseModel):
    candidates: list[RawExtractionCandidate] = Field(default_factory=list)
    extraction_manifest: dict = Field(default_factory=dict)
    manual_review_queue: list[dict] = Field(default_factory=list)
    rejected_candidates: list[dict] = Field(default_factory=list)
    reviewed_candidate_map: list[dict] = Field(default_factory=list)
    validation_ready_pack: dict = Field(default_factory=dict)
    source_hashes: dict = Field(default_factory=dict)
    blocked_reason: str | None = None


class SemanticTriageRecord(BaseModel):
    candidate_id: str
    source_id: str
    sha256: str | None = None
    page_number: int | None = None
    candidate_type: str
    extracted_text: str
    normalized_text: str | None = None
    assigned_slot: str
    semantic_score: float
    source_priority_score: float
    slot_relevance_score: float
    cleanliness_score: float
    specificity_score: float
    risk_score: float
    triage_score: float
    priority: str
    include_in_priority_packet: bool
    review_question: str
    decision_needed: str
    notes: list[str] = Field(default_factory=list)


class PriorityReviewItem(BaseModel):
    review_item_id: str
    candidate_id: str
    source_id: str
    page_number: int | None = None
    assigned_slot: str
    priority: str
    exact_text_or_preview: str
    why_relevant: str
    review_question: str
    decision_needed: str
    possible_outcomes: list[str] = Field(default_factory=list)
    next_gate_impact: str


class SlotReviewQueue(BaseModel):
    slot_id: str
    items: list[PriorityReviewItem] = Field(default_factory=list)
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    source_coverage: dict[str, int] = Field(default_factory=dict)


class LowValueTriageExclusion(BaseModel):
    candidate_id: str
    source_id: str
    reason: str
    triage_score: float
    text_preview: str


class NextGateReadiness(BaseModel):
    status: str
    priority_packet_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    manual_review_required: bool = True
    ready_for_v3_9: bool = False
    reason: str
    recommended_next_action: str
    blocked_claims: list[str] = Field(default_factory=list)


class PhiGradientSemanticTriageGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    input_candidate_count: int = 0
    triaged_candidate_count: int = 0
    priority_packet_count: int = 0
    critical_count: int = 0
    high_count: int = 0
    validation_ready_count: int = 0
    pedernales_slot4_count: int = 0
    slot_coverage: dict[str, int] = Field(default_factory=dict)
    source_coverage: dict[str, int] = Field(default_factory=dict)
    triage_map: list[SemanticTriageRecord] = Field(default_factory=list)
    priority_packet: list[PriorityReviewItem] = Field(default_factory=list)
    slot_review_queues: list[SlotReviewQueue] = Field(default_factory=list)
    low_value_exclusions: list[LowValueTriageExclusion] = Field(default_factory=list)
    next_gate_readiness: NextGateReadiness
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientSemanticTriageCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientSemanticTriageGateResult
    report_paths: dict[str, str] = Field(default_factory=dict)
