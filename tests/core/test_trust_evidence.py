import pytest

import xendris.core.trust as trust


def make_test_evidence(confidence: float = 0.9) -> trust.Evidence:
    return trust.Evidence(
        evidence_id=f"EV-{confidence}",
        evidence_type=trust.EvidenceType.TEST_RESULT,
        source="pytest",
        content_hash=f"hash-{confidence}",
        excerpt="1089 passed, 4 warnings",
        confidence=confidence,
        metadata={"command": "pytest"},
    )


def test_evidence_creation_is_immutable_and_serializable():
    evidence = make_test_evidence(0.95)

    assert evidence.evidence_type == trust.EvidenceType.TEST_RESULT
    assert evidence.confidence == 0.95
    assert evidence.metadata["command"] == "pytest"
    assert evidence.to_dict()["metadata"] == {"command": "pytest"}

    with pytest.raises(TypeError):
        evidence.metadata["command"] = "changed"


def test_invalid_evidence_confidence_is_rejected():
    with pytest.raises(ValueError):
        make_test_evidence(-0.01)

    with pytest.raises(ValueError):
        make_test_evidence(1.01)


def test_empty_evidence_required_fields_are_rejected():
    with pytest.raises(ValueError):
        trust.Evidence(
            evidence_id="",
            evidence_type=trust.EvidenceType.DOCUMENT,
            source="README.md",
            content_hash="hash",
            excerpt=None,
            confidence=0.8,
        )

    with pytest.raises(ValueError):
        trust.Evidence(
            evidence_id="EV-DOC",
            evidence_type=trust.EvidenceType.DOCUMENT,
            source="",
            content_hash="hash",
            excerpt=None,
            confidence=0.8,
        )

    with pytest.raises(ValueError):
        trust.Evidence(
            evidence_id="EV-DOC",
            evidence_type=trust.EvidenceType.DOCUMENT,
            source="README.md",
            content_hash="",
            excerpt=None,
            confidence=0.8,
        )


def test_no_evidence_gives_zero_support_score():
    claim = trust.make_claim(
        text="The test suite passed.",
        claim_type=trust.ClaimType.CODE_STATE,
        confidence=0.9,
        status=trust.ClaimStatus.VERIFIED,
    )

    assert trust.compute_support_score(claim, ()) == 0.0


def test_multiple_evidence_items_compute_stable_average_support_score():
    claim = trust.make_claim(
        text="The test suite passed.",
        claim_type=trust.ClaimType.CODE_STATE,
        confidence=0.9,
        status=trust.ClaimStatus.VERIFIED,
    )
    evidence_items = (make_test_evidence(0.8), make_test_evidence(1.0))

    assert trust.compute_support_score(claim, evidence_items) == 0.9
    binding = trust.bind_evidence_to_claim(claim, evidence_items)
    assert binding.support_score == 0.9
    assert binding.claim == claim
    assert binding.evidence_items == evidence_items


def test_factual_claim_without_evidence_cannot_be_verified_by_evaluator():
    claim = trust.make_claim(
        text="The release is ready.",
        claim_type=trust.ClaimType.FACTUAL,
        confidence=0.9,
        status=trust.ClaimStatus.VERIFIED,
    )

    audit = trust.evaluate_claims("The release is ready.", (claim,))

    assert audit.risk_level == trust.RiskLevel.HIGH
    assert audit.decision == trust.AuditDecision.HUMAN_REVIEW_REQUIRED
    assert audit.unsupported_claims == (claim,)
    assert trust.validate_reasoning_audit(audit) is True


def test_factual_claim_with_strong_evidence_can_be_approved():
    claim = trust.make_claim(
        text="The release gate suite passed.",
        claim_type=trust.ClaimType.FACTUAL,
        confidence=0.9,
        status=trust.ClaimStatus.VERIFIED,
    )
    evidence = trust.Evidence(
        evidence_id="EV-RELEASE-GATE",
        evidence_type=trust.EvidenceType.DOCUMENT,
        source="docs/status/RELEASE_GATE_V0_2_0.md",
        content_hash="release-gate-hash",
        excerpt="1080 passed, 4 warnings",
        confidence=0.95,
    )

    audit = trust.evaluate_claims(
        "The release gate suite passed.",
        (claim,),
        evidence_bindings=(trust.bind_evidence_to_claim(claim, (evidence,)),),
    )

    assert audit.risk_level == trust.RiskLevel.LOW
    assert audit.decision == trust.AuditDecision.APPROVED
    assert audit.unsupported_claims == ()
    assert trust.validate_reasoning_audit(audit) is True


def test_user_provided_claim_can_pass_with_limitations_without_external_evidence():
    claim = trust.make_claim(
        text="The user says this is their intended release goal.",
        claim_type=trust.ClaimType.USER_PROVIDED,
        confidence=0.7,
        status=trust.ClaimStatus.VERIFIED,
    )

    audit = trust.evaluate_claims("User-provided context accepted with limitations.", (claim,))

    assert audit.risk_level == trust.RiskLevel.MEDIUM
    assert audit.decision == trust.AuditDecision.APPROVED_WITH_LIMITATIONS
    assert trust.validate_reasoning_audit(audit) is True


def test_public_imports_are_available_from_trust_namespace():
    assert trust.EvidenceType.DOCUMENT.value == "DOCUMENT"
    assert trust.Evidence is not None
    assert trust.EvidenceBinding is not None
    assert trust.compute_support_score is not None
    assert trust.bind_evidence_to_claim is not None
