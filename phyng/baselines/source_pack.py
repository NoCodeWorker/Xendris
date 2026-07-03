from pydantic import BaseModel, Field
from phyng.evidence.source_candidates import SourceCandidate
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult
from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09


class BaselineSourcePack(BaseModel):
    pack_id: str
    campaign_id: str
    source_candidates: list[SourceCandidate] = Field(default_factory=list)
    minimum_requirements: list[str] = Field(default_factory=list)
    # EMPTY | PARTIAL | MINIMUM_COVERAGE | FULL_COVERAGE | CONTRADICTED
    coverage_status: str = "EMPTY"
    missing_requirements: list[str] = Field(default_factory=list)
    ready_for_upgrade_attempt: bool = False


def evaluate_source_pack(
    pack_id: str,
    campaign_id: str,
    candidates: list[SourceCandidate],
    audits: list[CitationAuditResult],
    links: list[ClaimSourceLinkV09]
) -> BaselineSourcePack:
    if not candidates:
        return BaselineSourcePack(
            pack_id=pack_id,
            campaign_id=campaign_id,
            source_candidates=[],
            minimum_requirements=["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
            coverage_status="EMPTY",
            missing_requirements=["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
            ready_for_upgrade_attempt=False
        )
        
    # Check for contradictions first
    has_contradiction = any(link.support_type == "CONTRADICTION" for link in links)
    if has_contradiction:
        return BaselineSourcePack(
            pack_id=pack_id,
            campaign_id=campaign_id,
            source_candidates=candidates,
            minimum_requirements=["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
            coverage_status="CONTRADICTED",
            missing_requirements=["Contradictory source linked."],
            ready_for_upgrade_attempt=False
        )
        
    # Audit lookup dictionary
    audit_dict = {a.source_id: a for a in audits}
    
    # Check formula and observable support
    has_formula = False
    has_observable = False
    has_parameter = False
    has_context = False
    
    for link in links:
        audit = audit_dict.get(link.source_id)
        if not audit or not audit.passed:
            continue
            
        if link.support_type == "FORMULA_SUPPORT":
            has_formula = True
        elif link.support_type == "OBSERVABLE_SUPPORT":
            has_observable = True
        elif link.support_type == "PARAMETER_SUPPORT":
            has_parameter = True
        elif link.support_type == "CONTEXT_SUPPORT":
            has_context = True
            
    missing = []
    if not has_formula:
        missing.append("FORMULA_SUPPORT")
    if not has_observable:
        missing.append("OBSERVABLE_SUPPORT")
        
    ready = len(missing) == 0
    
    if ready:
        if has_parameter and has_context:
            coverage = "FULL_COVERAGE"
        else:
            coverage = "MINIMUM_COVERAGE"
    else:
        coverage = "PARTIAL"
        
    return BaselineSourcePack(
        pack_id=pack_id,
        campaign_id=campaign_id,
        source_candidates=candidates,
        minimum_requirements=["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
        coverage_status=coverage,
        missing_requirements=missing,
        ready_for_upgrade_attempt=ready
    )
