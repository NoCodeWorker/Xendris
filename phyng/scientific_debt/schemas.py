"""Schemas for v4.0 scientific debt and resolution plan."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScientificDebtObject(BaseModel):
    debt_id: str
    title: str
    status: str
    severity: str
    opened_by: str
    source_pressure_ref: str
    blocks: list[str] = Field(default_factory=list)
    does_not_block: list[str] = Field(default_factory=list)
    evidence_gap: str
    current_findings: list[str] = Field(default_factory=list)
    resolution_conditions: list[str] = Field(default_factory=list)
    prohibited_claims: list[str] = Field(default_factory=list)
    allowed_work: list[str] = Field(default_factory=list)
    review_frequency: str
    notes: list[str] = Field(default_factory=list)


class Slot4ResolutionTask(BaseModel):
    task_id: str
    name: str
    description: str
    status: str
    owner: str


class Slot4ResolutionPlan(BaseModel):
    plan_id: str = "PHI-GRADIENT-SLOT4-RESOLUTION-PLAN-v4_0"
    debt_id: str = "DEBT-SLOT4-GRADIENT-COMPONENT-GAP"
    status: str = "SLOT4_DEBT_OPEN"
    tasks: list[Slot4ResolutionTask] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
