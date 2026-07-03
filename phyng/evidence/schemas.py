from pydantic import BaseModel, Field


class SourceRequirement(BaseModel):
    requirement_id: str
    topic: str
    reason: str
    linked_claim_ids: list[str] = Field(default_factory=list)
    linked_campaign_ids: list[str] = Field(default_factory=list)
    required_trust_level: str
    required_source_types: list[str] = Field(default_factory=list)
    suggested_queries: list[str] = Field(default_factory=list)
    status: str = "REQUIRED"


class SourceIngestionResult(BaseModel):
    requirement_id: str
    source_id: str | None = None
    status: str
    action: str
    reason: str
    created_claim_links: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


class EvidenceRecord(BaseModel):
    evidence_id: str
    requirement_id: str
    source_id: str | None = None
    claim_id: str
    support_level: str
    trust_level: str | None = None
    evidence_type: str
    note: str | None = None
    status: str = "UNVERIFIED"


class EvidenceAuditResult(BaseModel):
    claim_id: str
    support_status: str
    allowed_claim_level: int
    can_unlock_hard_claim: bool
    reason: str
    missing_requirements: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
