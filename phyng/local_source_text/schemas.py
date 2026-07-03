"""Schemas for v3.6 local source text registry."""

from __future__ import annotations

from pydantic import BaseModel, Field

from phyng.closed_loop.schemas import CandidateLoopInput, CandidateLoopResult, CandidateUpdateProposal
from phyng.core.status_mapping import CanonicalStatusRecord


class PriorityLocalSourceSpec(BaseModel):
    source_id: str
    matched_seed_source_id: str | None = None
    title: str
    preferred_filename: str
    target_path: str
    known_identifiers: dict[str, str | None] = Field(default_factory=dict)
    priority: int


class LocalSourceFileRecord(BaseModel):
    source_id: str
    canonical_filename: str
    local_path: str
    exists: bool
    file_type: str
    size_bytes: int | None = None
    sha256: str | None = None
    text_extractable: bool | None = None
    registry_status: str
    notes: list[str] = Field(default_factory=list)


class LocalSourceTextRegistry(BaseModel):
    registry_id: str = "PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6"
    candidate_family: str = "LOG_BOUNDARY"
    phi_family: str = "PHI_GRADIENT"
    created_at: str = "2026-06-30"
    source_records: list[LocalSourceFileRecord] = Field(default_factory=list)
    available_count: int = 0
    missing_count: int = 0
    hash_count: int = 0
    unsupported_file_count: int = 0
    registry_status: str = "PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_CREATED"


class SourceFileManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-SOURCE-FILE-MANIFEST-v3_6"
    source_files: list[LocalSourceFileRecord] = Field(default_factory=list)


class SourceHashRecord(BaseModel):
    source_id: str
    local_path: str
    sha256: str
    size_bytes: int
    file_type: str


class SourceHashManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-SOURCE-HASHES-v3_6"
    hashes: list[SourceHashRecord] = Field(default_factory=list)


class SourceAvailabilityRecord(BaseModel):
    source_id: str
    local_path: str
    availability_status: str
    exists: bool
    hashed: bool
    notes: list[str] = Field(default_factory=list)


class SourceAvailabilityManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-SOURCE-AVAILABILITY-v3_6"
    availability: list[SourceAvailabilityRecord] = Field(default_factory=list)


class ManualSourceDownloadTask(BaseModel):
    task_id: str
    source_id: str
    title: str
    preferred_filename: str
    target_path: str
    known_identifiers: dict[str, str | None] = Field(default_factory=dict)
    priority: int
    reason: str
    status: str = "DOWNLOAD_TASK_CREATED"


class ManualSourceDownloadTaskManifest(BaseModel):
    manifest_id: str = "PHI-GRADIENT-MANUAL-DOWNLOAD-TASKS-v3_6"
    tasks: list[ManualSourceDownloadTask] = Field(default_factory=list)


class PhiGradientLocalSourceTextRegistryResult(BaseModel):
    status: str
    canonical_status: CanonicalStatusRecord
    priority_sources: list[PriorityLocalSourceSpec] = Field(default_factory=list)
    registry: LocalSourceTextRegistry
    file_manifest: SourceFileManifest
    hash_manifest: SourceHashManifest
    availability_manifest: SourceAvailabilityManifest
    download_tasks: ManualSourceDownloadTaskManifest
    available_file_count: int = 0
    missing_file_count: int = 0
    hash_count: int = 0
    unsupported_file_count: int = 0
    manual_download_task_count: int = 0
    blocked_reason: str | None = None
    output_paths: dict[str, str] = Field(default_factory=dict)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)


class PhiGradientLocalSourceTextRegistryCampaignResult(BaseModel):
    campaign_id: str
    status: str
    registry_result: PhiGradientLocalSourceTextRegistryResult
    loop_input: CandidateLoopInput
    loop_result: CandidateLoopResult
    update_proposals: list[CandidateUpdateProposal] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
