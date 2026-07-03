"""Schemas for the v4.9 source identity preflight gate."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.core.status_mapping import CanonicalStatusRecord


class SourceIdentityPreflightInputs(BaseModel):
    v48_gate: dict = Field(default_factory=dict)
    v48_resolution: list[dict] = Field(default_factory=list)
    v48_availability: list[dict] = Field(default_factory=list)
    candidate_matrix: list[dict] = Field(default_factory=list)
    pivot_decision: dict = Field(default_factory=dict)
    phi_gradient_method_only: dict = Field(default_factory=dict)
    slot4_debt: dict = Field(default_factory=dict)
    missing_files: list[str] = Field(default_factory=list)


class CandidateFamilySourceInventory(BaseModel):
    family_id: str
    previous_status: str | None = None
    raw_source_refs: list[str] = Field(default_factory=list)
    known_resolved_sources: list[str] = Field(default_factory=list)
    local_pdf_refs: list[str] = Field(default_factory=list)
    supplementary_refs: list[str] = Field(default_factory=list)
    dataset_refs: list[str] = Field(default_factory=list)
    inventory_status: str
    notes: list[str] = Field(default_factory=list)


class SourceIdentityResolutionRecord(BaseModel):
    family_id: str
    source_ref_raw: str
    source_id: str | None = None
    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    publication: str | None = None
    year: int | None = None
    doi: str | None = None
    arxiv_id: str | None = None
    url: str | None = None
    local_hash: str | None = None
    resolution_status: str
    confidence: str
    identity_complete: bool = False
    blockers: list[str] = Field(default_factory=list)


class SourceAvailabilityMatrixRecord(BaseModel):
    family_id: str
    source_id: str | None = None
    identity_complete: bool = False
    local_pdf_available: bool = False
    local_pdf_path: str | None = None
    local_pdf_hash: str | None = None
    supplementary_available: bool = False
    dataset_available: bool = False
    availability_status: str
    required_next_action: str


class ObservableIdentityRecord(BaseModel):
    family_id: str
    source_id: str | None = None
    observable_class: str
    observable_name: str
    source_locatable: bool = False
    expected_location_type: str | None = None
    expected_unit: str | None = None
    numeric_value_expected: bool = False
    observable_status: str
    blockers: list[str] = Field(default_factory=list)


class YTruePathPlausibilityRecord(BaseModel):
    family_id: str
    source_id: str | None = None
    observable_class: str
    possible_ytrue_source: str
    plausibility_level: str
    requires_manual_review: bool = False
    requires_download: bool = False
    requires_new_experiment: bool = False
    blockers: list[str] = Field(default_factory=list)


class CandidatePreflightDecisionRecord(BaseModel):
    family_id: str
    resolvable_source_count: int = 0
    local_or_exact_source_count: int = 0
    source_locatable_observable_count: int = 0
    plausible_ytrue_path_count: int = 0
    slot4_dependency: str
    claim_risk: str
    preflight_status: str
    allowed_next_phase: str | None = None
    blocked_next_phases: list[str] = Field(default_factory=list)
    required_next_action: str
    notes: list[str] = Field(default_factory=list)


class SourceIdentityPreflightGate(BaseModel):
    gate_id: str = "PHYGN-SOURCE-IDENTITY-PREFLIGHT-GATE-v4_9"
    final_status: str
    candidate_count: int
    passed_candidate_count: int
    partial_candidate_count: int
    failed_candidate_count: int
    selected_candidate_family: str | None = None
    allowed_next_phase: str | None = None
    blocked_next_phases: list[str] = Field(default_factory=list)
    required_before_next_pipeline: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class SourceIdentityPreflightCampaignResult(BaseModel):
    campaign_id: str = "PHYGN-SOURCE-IDENTITY-PREFLIGHT-GATE-v4_9"
    status: str
    canonical_status: CanonicalStatusRecord
    inputs_loaded: bool
    inventory: list[CandidateFamilySourceInventory] = Field(default_factory=list)
    identity_matrix: list[SourceIdentityResolutionRecord] = Field(default_factory=list)
    availability_matrix: list[SourceAvailabilityMatrixRecord] = Field(default_factory=list)
    observable_matrix: list[ObservableIdentityRecord] = Field(default_factory=list)
    ytrue_path_matrix: list[YTruePathPlausibilityRecord] = Field(default_factory=list)
    decision_matrix: list[CandidatePreflightDecisionRecord] = Field(default_factory=list)
    gate: SourceIdentityPreflightGate
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
