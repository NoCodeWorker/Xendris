from pydantic import BaseModel, Field
from pathlib import Path
from phyng.evidence.source_records_v0_9 import SourceRecordV09


class CitationAuditResult(BaseModel):
    source_id: str
    passed: bool
    audit_status: str
    missing_fields: list[str] = Field(default_factory=list)
    trust_issues: list[str] = Field(default_factory=list)
    extraction_issues: list[str] = Field(default_factory=list)
    allowed_support_types: list[str] = Field(default_factory=list)
    forbidden_support_types: list[str] = Field(default_factory=list)


def audit_citation_v0_9(record: SourceRecordV09) -> CitationAuditResult:
    missing = []
    trust_issues = []
    extract_issues = []
    
    # 1. Metadata check
    if not record.title or not record.title.strip():
        missing.append("title")
    if not record.authors:
        missing.append("authors")
    if not record.year or not record.year.strip():
        missing.append("year")
        
    # 2. Local content check
    has_local = False
    if record.local_path:
        local_file = Path(record.local_path)
        if local_file.exists() and local_file.is_file():
            has_local = True
            
    # 3. Contradiction check
    is_contradictory = False
    if record.notes and "contradicts" in record.notes.lower():
        is_contradictory = True
        
    # 4. Trust level check
    is_low_trust = record.trust_level in ["LOW", "BACKGROUND"]
    
    # Evaluate status
    if not has_local:
        status = "FAILED_NO_LOCAL_CONTENT"
        passed = False
        extract_issues.append("No local file found.")
    elif missing:
        status = "FAILED_MISSING_METADATA"
        passed = False
    elif is_contradictory:
        status = "FAILED_CONTRADICTORY"
        passed = False
        trust_issues.append("Source contradicts baseline physics.")
    elif is_low_trust:
        status = "FAILED_LOW_TRUST"
        passed = False
        trust_issues.append("Source trust level is too low.")
    elif record.ingestion_status == "INGESTED_METADATA_ONLY":
        status = "PASSED_METADATA_ONLY"
        passed = True
    else:
        status = "PASSED_LIMITED"
        passed = True
        
    # Allowed support types mapping
    if status == "PASSED_LIMITED":
        allowed = ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT", "PARAMETER_SUPPORT", "CONTEXT_SUPPORT"]
        forbidden = ["CONTRADICTION"]
    elif status == "PASSED_METADATA_ONLY":
        allowed = ["CONTEXT_SUPPORT"]
        forbidden = ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT", "PARAMETER_SUPPORT"]
    else:
        allowed = []
        forbidden = ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT", "PARAMETER_SUPPORT", "CONTEXT_SUPPORT"]
        
    return CitationAuditResult(
        source_id=record.source_id,
        passed=passed,
        audit_status=status,
        missing_fields=missing,
        trust_issues=trust_issues,
        extraction_issues=extract_issues,
        allowed_support_types=allowed,
        forbidden_support_types=forbidden
    )
