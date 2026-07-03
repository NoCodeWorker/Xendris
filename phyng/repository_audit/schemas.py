"""Schemas for the Phygn v2.0 repository orchestration audit."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


RecommendationRiskLevel = Literal[
    "NO_CHANGE",
    "DOCUMENT_ONLY",
    "LOW_RISK_EXTRACT_CONSTANTS",
    "LOW_RISK_EXTRACT_ENUM",
    "MEDIUM_RISK_SCHEMA_UNIFICATION",
    "MEDIUM_RISK_REPORT_CONTRACT_UNIFICATION",
    "HIGH_RISK_MODULE_MOVE",
    "HIGH_RISK_PUBLIC_API_CHANGE",
    "BLOCKED_NEEDS_HUMAN_REVIEW",
]


class RepositoryAuditResult(BaseModel):
    root: str
    packages: list[str] = Field(default_factory=list)
    modules: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    reports: list[str] = Field(default_factory=list)
    campaigns: list[str] = Field(default_factory=list)
    schemas: list[str] = Field(default_factory=list)
    enums: list[str] = Field(default_factory=list)
    status_strings: list[str] = Field(default_factory=list)
    imports: dict[str, list[str]] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class ModuleAuditRecord(BaseModel):
    module: str
    path: str
    responsibility_guess: str
    imports: list[str] = Field(default_factory=list)
    imported_by: list[str] = Field(default_factory=list)
    defined_schemas: list[str] = Field(default_factory=list)
    defined_enums: list[str] = Field(default_factory=list)
    reports_written: list[str] = Field(default_factory=list)
    tests_covering_module: list[str] = Field(default_factory=list)
    possible_duplicates: list[str] = Field(default_factory=list)
    boundary_warnings: list[str] = Field(default_factory=list)


class StateFamilyRecord(BaseModel):
    state_family: str
    definitions: list[str] = Field(default_factory=list)
    consumers: list[str] = Field(default_factory=list)
    producers: list[str] = Field(default_factory=list)
    serialized_in_reports: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    is_canonical: bool = False
    representation: str = "missing"
    likely_string_only_statuses: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class StatusMappingRecord(BaseModel):
    domain_status: str
    domain_module: str
    canonical_permission: str
    canonical_blocked_reason: str | None = None
    canonical_evidence_level: str | None = None
    canonical_risk_level: str | None = None
    notes: str = ""


class DependencyRecord(BaseModel):
    module: str
    imports: list[str] = Field(default_factory=list)
    imported_by: list[str] = Field(default_factory=list)
    cycle_warnings: list[str] = Field(default_factory=list)
    coupling_warnings: list[str] = Field(default_factory=list)
    boundary_warnings: list[str] = Field(default_factory=list)


class CampaignAuditRecord(BaseModel):
    campaign_id: str
    entrypoint: str
    reports: list[str] = Field(default_factory=list)
    gatekeepers: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ReportAuditRecord(BaseModel):
    path: str
    title: bool = False
    date: bool = False
    campaign_id: bool = False
    inputs: bool = False
    core_results: bool = False
    gate_results: bool = False
    allowed_claims: bool = False
    blocked_claims: bool = False
    failure_conditions: bool = False
    next_actions: bool = False
    tests: bool = False
    warnings: list[str] = Field(default_factory=list)


class TestAuditRecord(BaseModel):
    path: str
    test_count_estimate: int = 0
    modules_covered: list[str] = Field(default_factory=list)
    campaign_tests: bool = False
    negative_tests: bool = False
    contract_tests: bool = False
    report_tests: bool = False


class RefactorRecommendation(BaseModel):
    title: str
    description: str
    affected_modules: list[str] = Field(default_factory=list)
    risk_level: RecommendationRiskLevel
    expected_benefit: str
    behavior_change_expected: bool = False
    requires_human_review: bool = False
    suggested_order: int


class RepositoryAuditCampaignResult(BaseModel):
    campaign_id: str
    version: str
    status: str
    repository_audit: RepositoryAuditResult
    ontology_records: list[StateFamilyRecord] = Field(default_factory=list)
    module_records: list[ModuleAuditRecord] = Field(default_factory=list)
    dependency_records: list[DependencyRecord] = Field(default_factory=list)
    campaign_records: list[CampaignAuditRecord] = Field(default_factory=list)
    report_records: list[ReportAuditRecord] = Field(default_factory=list)
    test_records: list[TestAuditRecord] = Field(default_factory=list)
    recommendations: list[RefactorRecommendation] = Field(default_factory=list)
    report_paths: dict[str, str] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
