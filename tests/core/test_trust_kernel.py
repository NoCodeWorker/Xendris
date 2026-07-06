import pytest

from xendris.core.trust import (
    AuditDecision,
    Claim,
    ClaimStatus,
    ClaimType,
    Evidence,
    EvidenceType,
    ReasoningAudit,
    RiskLevel,
    TrustKernelEvaluator,
    bind_evidence_to_claim,
    make_claim,
    validate_reasoning_audit,
)


def test_valid_claim_constructs_correctly():
    claim = make_claim(
        text="Suite completa: 1080 passed, 4 warnings.",
        claim_type=ClaimType.CODE_STATE,
        confidence=0.98,
        status=ClaimStatus.VERIFIED,
        source_refs=("pytest",),
    )

    assert claim.text == "Suite completa: 1080 passed, 4 warnings."
    assert claim.claim_type == ClaimType.CODE_STATE
    assert claim.confidence == 0.98
    assert claim.status == ClaimStatus.VERIFIED
    assert claim.source_refs == ("pytest",)
    assert claim.to_dict()["source_refs"] == ["pytest"]


def test_invalid_claim_rejects_empty_text_and_bad_confidence():
    with pytest.raises(ValueError):
        make_claim(
            text="",
            claim_type=ClaimType.FACTUAL,
            confidence=0.5,
            status=ClaimStatus.VERIFIED,
        )

    with pytest.raises(ValueError):
        make_claim(
            text="invalid",
            claim_type=ClaimType.FACTUAL,
            confidence=-0.01,
            status=ClaimStatus.VERIFIED,
        )

    with pytest.raises(ValueError):
        make_claim(
            text="invalid",
            claim_type=ClaimType.FACTUAL,
            confidence=1.01,
            status=ClaimStatus.VERIFIED,
        )


def test_verified_claims_produce_approved_low_risk_audit():
    claims = (
        make_claim(
            text="Suite completa: 1080 passed, 4 warnings.",
            claim_type=ClaimType.CODE_STATE,
            confidence=0.98,
            status=ClaimStatus.VERIFIED,
        ),
    )
    evidence = Evidence(
        evidence_id="EV-PYTEST-1080",
        evidence_type=EvidenceType.TEST_RESULT,
        source="pytest",
        content_hash="pytest-1080-4-warnings",
        excerpt="1080 passed, 4 warnings",
        confidence=0.98,
    )

    audit = TrustKernelEvaluator().evaluate(
        answer="The current Python suite passes with 1080 tests and 4 warnings.",
        claims=claims,
        evidence_bindings=(bind_evidence_to_claim(claims[0], (evidence,)),),
    )

    assert audit.risk_level == RiskLevel.LOW
    assert audit.decision == AuditDecision.APPROVED
    assert audit.global_confidence >= 0.9
    assert audit.unsupported_claims == ()
    assert validate_reasoning_audit(audit) is True


def test_unsupported_low_confidence_claim_is_approved_with_limitations():
    unsupported_claim = make_claim(
        text="Xendris is objectively superior to DeepSeek in general reasoning.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.45,
        status=ClaimStatus.UNSUPPORTED,
    )

    audit = TrustKernelEvaluator().evaluate(
        answer="This unsupported comparison should be treated with limitations.",
        claims=(unsupported_claim,),
    )

    assert audit.risk_level == RiskLevel.MEDIUM
    assert audit.decision == AuditDecision.APPROVED_WITH_LIMITATIONS
    assert audit.unsupported_claims == (unsupported_claim,)
    assert validate_reasoning_audit(audit) is True


def test_unsupported_high_confidence_claim_requires_human_review():
    unsupported_claim = make_claim(
        text="Xendris is objectively superior to DeepSeek in general reasoning.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.88,
        status=ClaimStatus.UNSUPPORTED,
    )

    audit = TrustKernelEvaluator().evaluate(
        answer="This high-confidence unsupported comparison needs review.",
        claims=(unsupported_claim,),
    )

    assert audit.risk_level == RiskLevel.HIGH
    assert audit.decision == AuditDecision.HUMAN_REVIEW_REQUIRED
    assert audit.unsupported_claims == (unsupported_claim,)
    assert validate_reasoning_audit(audit) is True


def test_contradicted_documentation_claim_blocks_audit():
    readme_claim = make_claim(
        text="README says 1070 passed.",
        claim_type=ClaimType.CODE_STATE,
        confidence=0.9,
        status=ClaimStatus.CONTRADICTED,
        source_refs=("README.md",),
    )
    release_gate_claim = make_claim(
        text="Release Gate says 1080 passed.",
        claim_type=ClaimType.CODE_STATE,
        confidence=0.98,
        status=ClaimStatus.VERIFIED,
        source_refs=("docs/status/RELEASE_GATE_V0_2_0.md",),
    )

    audit = TrustKernelEvaluator().evaluate(
        answer="La documentación está desalineada.",
        claims=(readme_claim, release_gate_claim),
    )

    assert audit.risk_level == RiskLevel.HIGH
    assert audit.decision == AuditDecision.BLOCKED
    assert validate_reasoning_audit(audit) is True


def test_no_claims_requires_human_review():
    audit = TrustKernelEvaluator().evaluate(
        answer="No claims were declared for this answer.",
        claims=(),
    )

    assert audit.risk_level == RiskLevel.MEDIUM
    assert audit.decision == AuditDecision.HUMAN_REVIEW_REQUIRED
    assert audit.global_confidence <= 0.5
    assert validate_reasoning_audit(audit) is True


def test_validate_reasoning_audit_rejects_impossible_approval():
    claim = make_claim(
        text="Critical risk cannot be silently approved.",
        claim_type=ClaimType.POLICY,
        confidence=0.8,
        status=ClaimStatus.PARTIALLY_SUPPORTED,
    )
    audit = ReasoningAudit(
        answer="This audit is structurally impossible.",
        claims=(claim,),
        global_confidence=0.8,
        risk_level=RiskLevel.CRITICAL,
        decision=AuditDecision.APPROVED,
        notes=None,
    )

    assert validate_reasoning_audit(audit) is False


def test_validate_reasoning_audit_rejects_missing_unsupported_claim_list():
    unsupported_claim = make_claim(
        text="Unsupported claim must be listed.",
        claim_type=ClaimType.UNSUPPORTED,
        confidence=0.6,
        status=ClaimStatus.UNSUPPORTED,
    )
    audit = ReasoningAudit(
        answer="Unsupported claim is omitted from unsupported_claims.",
        claims=(unsupported_claim,),
        global_confidence=0.6,
        risk_level=RiskLevel.MEDIUM,
        decision=AuditDecision.APPROVED_WITH_LIMITATIONS,
        unsupported_claims=(),
    )

    assert validate_reasoning_audit(audit) is False
