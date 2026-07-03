from pydantic import BaseModel, Field


class SourceRecordV09(BaseModel):
    source_id: str
    title: str | None = None
    authors: list[str] = Field(default_factory=list)
    year: str | None = None
    source_type: str = "PAPER"
    trust_level: str = "MEDIUM"
    local_path: str | None = None
    url: str | None = None
    # NOT_INGESTED | CANDIDATE_ONLY | INGESTED_METADATA_ONLY | INGESTED_LOCAL_TEXT | INGESTED_LOCAL_PDF_METADATA | INGESTED_WITH_EXTRACTS | REJECTED
    ingestion_status: str = "NOT_INGESTED"
    # COMPLETE | PARTIAL | UNKNOWN | CONFLICTING
    metadata_status: str = "UNKNOWN"
    # pending | passed | failed
    citation_audit_status: str = "pending"
    notes: str | None = None
