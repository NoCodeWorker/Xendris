"""Schemas for Phygn self-provisioning audit records."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SelfProvisioningAuditRecord(BaseModel):
    cycle_id: str
    phase: str
    gate_name: str
    gate_status_before: str
    blocker_id: str
    blocker_type: str
    missing_capability_type: str
    proposed_improvement: str
    why_minimal: str
    files_created: list[str] = Field(default_factory=list)
    files_modified: list[str] = Field(default_factory=list)
    tests_added: list[str] = Field(default_factory=list)
    tests_run: list[str] = Field(default_factory=list)
    tests_passed: bool
    gate_retried: bool
    gate_status_after: str
    blocker_removed: bool
    next_action: str
    forbidden_actions_avoided: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
