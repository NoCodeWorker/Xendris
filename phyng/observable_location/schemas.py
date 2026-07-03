"""Schemas for v5.7.2 observable-location review."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TargetedObservableLocationCandidate(BaseModel):
    location_id: str
    source_candidate_id: str
    source_id: str | None = None
    local_pdf_path: str
    local_pdf_hash: str
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
    reviewer_decision: str
    extraction_blockers: list[str] = Field(default_factory=list)
    recommended_next_action: str


class ObservableLocationCampaignResult(BaseModel):
    status: str
    location_candidates: list[TargetedObservableLocationCandidate] = Field(default_factory=list)
    observed_measurement_candidates: list[TargetedObservableLocationCandidate] = Field(default_factory=list)
    rejected_location_records: list[TargetedObservableLocationCandidate] = Field(default_factory=list)
    next_gate_decision: dict = Field(default_factory=dict)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
