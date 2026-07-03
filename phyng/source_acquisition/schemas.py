"""Schemas for v5.7.1 targeted source acquisition."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourceAcquisitionQueueItem(BaseModel):
    acquisition_id: str
    priority: str
    source_title_candidate: str | None = None
    authors_candidate: list[str] = Field(default_factory=list)
    year_candidate: int | None = None
    publication_candidate: str | None = None
    doi_candidate: str | None = None
    arxiv_candidate: str | None = None
    url_candidate: str | None = None
    search_queries: list[str] = Field(default_factory=list)
    reason_for_relevance: str
    target_observable_classes: list[str] = Field(default_factory=list)
    expected_conditions: list[str] = Field(default_factory=list)
    source_identity_status: str
    availability_status: str
    likely_observable_location: str | None = None
    manual_action_required: str
    notes: list[str] = Field(default_factory=list)


class CandidateSourceIdentityRecord(BaseModel):
    source_candidate_id: str
    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    publication: str | None = None
    doi: str | None = None
    arxiv: str | None = None
    url: str | None = None
    identity_completeness_score: float
    identity_complete: bool
    missing_identity_fields: list[str] = Field(default_factory=list)


class ObservableTargetRecord(BaseModel):
    source_candidate_id: str
    target_observable_class: str
    target_variable: str
    expected_condition_axis: str
    expected_location_type: str
    expected_numeric_form: str
    why_ytrue_possible: str
    risk_of_not_ytrue: str
    priority: str


class DownloadQueueItem(BaseModel):
    source_candidate_id: str
    download_priority: str
    preferred_url: str | None = None
    expected_filename: str
    target_local_path: str
    requires_manual_download: bool
    requires_paywall_access: bool
    requires_supplementary_download: bool
    notes: list[str] = Field(default_factory=list)


class SourceRejectionRecord(BaseModel):
    source_candidate_id: str
    source_title_candidate: str | None
    rejection_reason: str
    notes: list[str] = Field(default_factory=list)


class SourceAcquisitionCampaignResult(BaseModel):
    campaign_id: str = "FRONTERA-C-TARGETED-VISIBILITY-DECOHERENCE-LITERATURE-ACQUISITION-v5_7_1"
    status: str
    inputs_loaded: bool
    acquisition_queue: list[SourceAcquisitionQueueItem] = Field(default_factory=list)
    identity_matrix: list[CandidateSourceIdentityRecord] = Field(default_factory=list)
    observable_matrix: list[ObservableTargetRecord] = Field(default_factory=list)
    download_queue: list[DownloadQueueItem] = Field(default_factory=list)
    rejection_log: list[SourceRejectionRecord] = Field(default_factory=list)
    next_gate_decision: dict = Field(default_factory=dict)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
    missing_inputs: list[str] = Field(default_factory=list)
