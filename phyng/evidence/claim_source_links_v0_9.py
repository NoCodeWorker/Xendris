from pydantic import BaseModel


class ClaimSourceLinkV09(BaseModel):
    link_id: str
    claim_id: str
    source_id: str
    # FORMULA_SUPPORT | OBSERVABLE_SUPPORT | PARAMETER_SUPPORT | CONTEXT_SUPPORT | BACKGROUND_ONLY | CONTRADICTION
    support_type: str
    # HIGH | MEDIUM | LOW
    support_strength: str
    quote_or_excerpt: str | None = None
    local_reference: str | None = None
    # PASSED_LIMITED | PASSED_METADATA_ONLY | FAILED_MISSING_METADATA | FAILED_NO_LOCAL_CONTENT | FAILED_LOW_TRUST | FAILED_CONTRADICTORY
    audit_status: str
