from pydantic import BaseModel, Field
from phyng.baselines.source_pack import BaselineSourcePack
from phyng.evidence.citation_audit_v0_9 import CitationAuditResult
from phyng.evidence.claim_source_links_v0_9 import ClaimSourceLinkV09

_CANDIDATE_BLOCKED = [
    "Phygn predicts gravitational decoherence.",
    "The candidate is validated.",
    "SyntheticGain is physical PredictiveGain.",
    "Frontera C is proven."
]


class BaselineUpgradeAttemptResult(BaseModel):
    attempt_id: str
    campaign_id: str
    baseline_before: str
    baseline_after: str
    success: bool
    reason: str
    source_pack_status: str
    direct_support_types: list[str] = Field(default_factory=list)
    missing_support_types: list[str] = Field(default_factory=list)
    contradiction_ids: list[str] = Field(default_factory=list)
    max_claim_level: int = 3
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)
    next_research_tasks: list[str] = Field(default_factory=list)


def run_baseline_upgrade_attempt_v0_9(
    attempt_id: str,
    campaign_id: str,
    baseline_before: str,
    pack: BaselineSourcePack,
    audits: list[CitationAuditResult],
    links: list[ClaimSourceLinkV09],
    has_parameter: bool = False,
    has_assumptions: bool = False
) -> BaselineUpgradeAttemptResult:
    # Extract contradictions
    contradiction_ids = [l.source_id for l in links if l.support_type == "CONTRADICTION"]
    
    if pack.coverage_status == "EMPTY":
        return BaselineUpgradeAttemptResult(
            attempt_id=attempt_id,
            campaign_id=campaign_id,
            baseline_before=baseline_before,
            baseline_after="BASELINE_REQUIRES_SOURCE",
            success=False,
            reason="No audited sources available. Upgrade blocked.",
            source_pack_status=pack.coverage_status,
            direct_support_types=[],
            missing_support_types=["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
            contradiction_ids=[],
            max_claim_level=3,
            allowed_claims=["Baseline remains TOY_INTERNAL pending source ingestion."],
            blocked_claims=_CANDIDATE_BLOCKED,
            next_research_tasks=["RT-BASELINE-SRC-001", "RT-BASELINE-SRC-002"]
        )
        
    if pack.coverage_status == "CONTRADICTED" or len(contradiction_ids) > 0:
        return BaselineUpgradeAttemptResult(
            attempt_id=attempt_id,
            campaign_id=campaign_id,
            baseline_before=baseline_before,
            baseline_after="BASELINE_CONTRADICTED",
            success=False,
            reason="Contradictory source linked. Baseline is blocked.",
            source_pack_status="CONTRADICTED",
            direct_support_types=[],
            missing_support_types=[],
            contradiction_ids=contradiction_ids,
            max_claim_level=0,
            allowed_claims=[],
            blocked_claims=_CANDIDATE_BLOCKED + ["Baseline is contradicted by source evidence."],
            next_research_tasks=[]
        )
        
    # Check passed audits
    passed_audits = {a.source_id for a in audits if a.passed}
    metadata_only = len(passed_audits) > 0 and all(
        a.audit_status == "PASSED_METADATA_ONLY" for a in audits if a.source_id in passed_audits
    )
    
    if metadata_only:
        return BaselineUpgradeAttemptResult(
            attempt_id=attempt_id,
            campaign_id=campaign_id,
            baseline_before=baseline_before,
            baseline_after="BASELINE_REQUIRES_DIRECT_SUPPORT",
            success=False,
            reason="Sources only support metadata, not physical equations.",
            source_pack_status=pack.coverage_status,
            direct_support_types=["CONTEXT_SUPPORT"],
            missing_support_types=["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
            contradiction_ids=[],
            max_claim_level=3,
            allowed_claims=["Metadata-only support found. Baseline upgrade failed."],
            blocked_claims=_CANDIDATE_BLOCKED,
            next_research_tasks=["RT-BASELINE-SRC-001"]
        )
        
    # Calculate support types
    direct_types = []
    for link in links:
        if link.source_id in passed_audits:
            direct_types.append(link.support_type)
            
    has_formula = "FORMULA_SUPPORT" in direct_types
    has_observable = "OBSERVABLE_SUPPORT" in direct_types
    
    missing = []
    if not has_formula:
        missing.append("FORMULA_SUPPORT")
    if not has_observable:
        missing.append("OBSERVABLE_SUPPORT")
        
    if has_formula and has_observable:
        if has_parameter and has_assumptions:
            baseline_after = "BASELINE_SOURCE_BACKED_READY"
            success = True
            level = 5
            allowed = [
                "The baseline is ready for limited source-backed comparison.",
                "CAMPAIGN-002 uses a source-backed ready baseline."
            ]
        else:
            baseline_after = "BASELINE_SOURCE_BACKED_LIMITED"
            success = True
            level = 4
            allowed = [
                "CAMPAIGN-002 now has a source-backed limited baseline.",
                "CAMPAIGN-002 now uses a source-backed limited baseline for visibility decay."
            ]
            if not has_parameter:
                missing.append("PARAMETER_SUPPORT")
            if not has_assumptions:
                missing.append("assumptions")
        reason = f"Baseline successfully upgraded to {baseline_after.replace('BASELINE_', '')}."
    elif has_formula:
        baseline_after = "BASELINE_BACKGROUND_SUPPORTED"
        success = False
        level = 3
        allowed = ["Formula supported but observable context is missing."]
        reason = "Formula only support found."
    else:
        baseline_after = "BASELINE_REQUIRES_DIRECT_SUPPORT"
        success = False
        level = 3
        allowed = ["Direct support is missing."]
        reason = "Direct formula or observable support is missing."
        
    return BaselineUpgradeAttemptResult(
        attempt_id=attempt_id,
        campaign_id=campaign_id,
        baseline_before=baseline_before,
        baseline_after=baseline_after,
        success=success,
        reason=reason,
        source_pack_status=pack.coverage_status,
        direct_support_types=list(set(direct_types)),
        missing_support_types=missing,
        contradiction_ids=[],
        max_claim_level=level,
        allowed_claims=allowed,
        blocked_claims=_CANDIDATE_BLOCKED,
        next_research_tasks=[]
    )
