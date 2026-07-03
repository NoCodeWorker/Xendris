"""Schemas for v3.5 priority exact extract fill."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord
from phyng.source_pack_population.schemas import SeedSourceExtractPack, SeedSourceManifest


class PrioritySourceAvailabilityRecord(BaseModel):
    priority_source_id: str
    matched_source_id: str | None = None
    source_title: str | None = None
    local_path: str | None = None
    traceable_identifier: str | None = None
    source_text_status: str
    notes: list[str] = Field(default_factory=list)


class PriorityExactFillRecord(BaseModel):
    priority_source_id: str
    source_id: str
    slot_id: str
    source_title: str | None = None
    source_text_status: str = "SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD"
    location_type: str = "UNKNOWN_LOCATION_REQUIRES_REVIEW"
    location_value: str = ""
    exact_quote: str | None = None
    equation_text: str | None = None
    observable_text: str | None = None
    parameter_range_text: str | None = None
    benchmark_range_text: str | None = None
    negative_constraint_text: str | None = None
    supported_components: list[str] = Field(default_factory=list)
    contradicted_components: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    review_status: str = "EXACT_FILL_REQUIRES_SOURCE_TEXT"
    validation_ready: bool = False
    reviewer_notes: list[str] = Field(default_factory=list)


class PriorityExactFillLocationRecord(BaseModel):
    priority_source_id: str
    source_id: str
    status: str
    validation_ready: bool = False
    missing_requirements: list[str] = Field(default_factory=list)


class PriorityEquationObservableMapEntry(BaseModel):
    priority_source_id: str
    source_id: str
    equation_text: str | None = None
    observable_text: str | None = None
    slot_id: str
    candidate_relevance: str
    limitations: list[str] = Field(default_factory=list)


class PriorityEquationObservableMap(BaseModel):
    entries: list[PriorityEquationObservableMapEntry] = Field(default_factory=list)


class PriorityParameterRangeMapEntry(BaseModel):
    priority_source_id: str
    source_id: str
    parameter_range_text: str | None = None
    benchmark_range_text: str | None = None
    negative_constraint_text: str | None = None
    comparability_status: str
    missing_requirements: list[str] = Field(default_factory=list)


class PriorityParameterRangeMap(BaseModel):
    entries: list[PriorityParameterRangeMapEntry] = Field(default_factory=list)


class PhiGradientPriorityExactFillGateResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    manifest: SeedSourceManifest | None = None
    seed_extract_pack: SeedSourceExtractPack | None = None
    source_availability: list[PrioritySourceAvailabilityRecord] = Field(default_factory=list)
    priority_records: list[PriorityExactFillRecord] = Field(default_factory=list)
    location_records: list[PriorityExactFillLocationRecord] = Field(default_factory=list)
    equation_observable_map: PriorityEquationObservableMap
    parameter_range_map: PriorityParameterRangeMap
    priority_source_count: int = 0
    validation_ready_count: int = 0
    unresolved_count: int = 0
    source_text_required_count: int = 0
    negative_candidate_count: int = 0
    blocked_reason: str | None = None
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientPriorityExactFillCampaignResult(BaseModel):
    campaign_id: str
    status: str
    gate_result: PhiGradientPriorityExactFillGateResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
