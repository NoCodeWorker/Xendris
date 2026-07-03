"""Schemas for v5.7.2 targeted source download and hashing."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SourceDownloadManifestRecord(BaseModel):
    source_candidate_id: str
    source_id: str | None = None
    title: str
    authors: list[str] = Field(default_factory=list)
    year: int | None = None
    external_identity: str | None = None
    preferred_url: str | None = None
    expected_filename: str | None = None
    local_pdf_path: str | None = None
    local_pdf_hash: str | None = None
    download_status: str
    file_verified: bool
    source_identity_complete: bool
    notes: list[str] = Field(default_factory=list)


class SourceHashRegistryUpdateRecord(BaseModel):
    source_id: str
    local_pdf_path: str | None = None
    sha256: str | None = None
    file_size_bytes: int | None = None
    modified_time_utc: str | None = None
    hash_status: str
    previous_hash_if_any: str | None = None


class SourceDownloadFailureRecord(BaseModel):
    source_candidate_id: str
    title: str
    preferred_url: str | None = None
    doi_or_arxiv: str | None = None
    expected_filename: str | None = None
    target_local_path: str | None = None
    reason: str
    priority: str
    required_next_action: str


class SourceDownloadCampaignResult(BaseModel):
    status: str
    manifest_records: list[SourceDownloadManifestRecord] = Field(default_factory=list)
    hash_records: list[SourceHashRegistryUpdateRecord] = Field(default_factory=list)
    failure_records: list[SourceDownloadFailureRecord] = Field(default_factory=list)
    output_paths: dict[str, str] = Field(default_factory=dict)
    report_paths: dict[str, str] = Field(default_factory=dict)
