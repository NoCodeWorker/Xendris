from phyng.evidence.schemas import EvidenceAuditResult, EvidenceRecord


HARD_CLAIM_LEVEL = 5


def audit_evidence_for_claim(
    claim_id: str,
    evidence_records: list[EvidenceRecord],
    required_requirement_ids: list[str] | None = None,
) -> EvidenceAuditResult:
    records = [record for record in evidence_records if record.claim_id == claim_id]
    required = set(required_requirement_ids or [])
    covered = {record.requirement_id for record in records if record.source_id is not None}
    missing = sorted(required - covered)

    if any(record.support_level == "CONTRADICTS" for record in records):
        return EvidenceAuditResult(
            claim_id=claim_id,
            support_status="CONTRADICTED",
            allowed_claim_level=0,
            can_unlock_hard_claim=False,
            reason="At least one evidence record contradicts the claim.",
            missing_requirements=missing,
            blocked_claims=[claim_id],
        )

    direct_high = [
        record
        for record in records
        if record.source_id is not None
        and record.support_level == "DIRECT_SUPPORT"
        and record.trust_level in {"PRIMARY", "HIGH"}
    ]
    if direct_high and not missing:
        return EvidenceAuditResult(
            claim_id=claim_id,
            support_status="DIRECTLY_SUPPORTED",
            allowed_claim_level=HARD_CLAIM_LEVEL,
            can_unlock_hard_claim=True,
            reason="Claim has direct high-trust support for required evidence.",
        )

    background = [record for record in records if record.support_level == "BACKGROUND"]
    if background:
        return EvidenceAuditResult(
            claim_id=claim_id,
            support_status="BACKGROUND_SUPPORTED",
            allowed_claim_level=3,
            can_unlock_hard_claim=False,
            reason="Background support is not sufficient for hard physical claims.",
            missing_requirements=missing,
            blocked_claims=[claim_id],
        )

    return EvidenceAuditResult(
        claim_id=claim_id,
        support_status="REQUIRES_SOURCE",
        allowed_claim_level=3,
        can_unlock_hard_claim=False,
        reason="No sufficient source-backed evidence exists.",
        missing_requirements=missing,
        blocked_claims=[claim_id],
    )
