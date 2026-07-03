"""Schemas for v5.7 visibility/decoherence dataset expansion."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourcePoolRecord(BaseModel):
    source_id: str
    title: str
    year: int | None = None
    authority: str | None = None
    external_identity: str | None = None
    local_pdf_path: str | None = None
    local_pdf_hash: str | None = None
    source_status: str
    candidate_relevance: list[str] = Field(default_factory=list)
    observable_targets: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class ObservableLocationCandidate(BaseModel):
    location_id: str
    source_id: str
    local_pdf_path: str | None = None
    local_pdf_hash: str | None = None
    page_number: int | None = None
    section_id: str | None = None
    figure_id: str | None = None
    table_id: str | None = None
    equation_id: str | None = None
    observable_class: str
    variable_name: str | None = None
    numeric_value_text: str | None = None
    unit_text: str | None = None
    condition_text: str | None = None
    snippet: str
    classification: str
    extraction_blockers: list[str] = Field(default_factory=list)
    recommended_next_action: str


class YTrueCandidate(BaseModel):
    ytrue_candidate_id: str
    source_id: str
    source_title: str
    source_year: int | None = None
    external_identity: str | None = None
    local_pdf_path: str | None = None
    local_pdf_hash: str | None = None
    page_number: int | None = None
    location_label: str
    observable_class: str
    variable_name: str
    value_numeric: float | None = None
    original_value_text: str
    unit: str | None = None
    conditions: dict = Field(default_factory=dict)
    extraction_method: str
    provenance_status: str
    qc_status: str
    limitations: list[str] = Field(default_factory=list)
    claim_impact: str = "NO_PHYSICAL_CLAIM_CREATED"


class VisibilityDecoherenceDataset(BaseModel):
    dataset_id: str
    version: str
    records: list[dict]
    source_count: int
    accepted_ytrue_count: int
    observable_class_distribution: dict
    condition_key_distribution: dict
    limitation_flags: list[str]
    notes: list[str] = Field(default_factory=list)


class DatasetExpansionCampaignResult(BaseModel):
    campaign_id: str = "FRONTERA-C-VISIBILITY-DECOHERENCE-DATASET-EXPANSION-v5_7"
    status: str
    inputs_loaded: bool
    source_pool: list[SourcePoolRecord] = Field(default_factory=list)
    location_candidates: list[ObservableLocationCandidate] = Field(default_factory=list)
    ytrue_candidates: list[YTrueCandidate] = Field(default_factory=list)
    accepted_ytrue: list[YTrueCandidate] = Field(default_factory=list)
    rejected_ytrue: list[YTrueCandidate] = Field(default_factory=list)
    dataset: VisibilityDecoherenceDataset | None = None
    dataset_quality: dict = Field(default_factory=dict)
    benchmark_readiness: dict = Field(default_factory=dict)
    next_gate_decision: dict = Field(default_factory=dict)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
    missing_inputs: list[str] = Field(default_factory=list)
