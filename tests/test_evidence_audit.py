from phyng.evidence import EvidenceRecord, audit_evidence_for_claim


def test_background_support_does_not_unlock_hard_claim():
    result = audit_evidence_for_claim(
        "CLAIM-DECOH-BASELINE-001",
        [
            EvidenceRecord(
                evidence_id="EV-001",
                requirement_id="REQ-SRC-006",
                source_id="SRC-001",
                claim_id="CLAIM-DECOH-BASELINE-001",
                support_level="BACKGROUND",
                trust_level="HIGH",
                evidence_type="SOURCE_LINK",
            )
        ],
        required_requirement_ids=["REQ-SRC-006"],
    )

    assert result.support_status == "BACKGROUND_SUPPORTED"
    assert result.can_unlock_hard_claim is False
    assert result.allowed_claim_level == 3


def test_high_trust_direct_support_allows_limited_claim():
    result = audit_evidence_for_claim(
        "CLAIM-DECOH-BASELINE-001",
        [
            EvidenceRecord(
                evidence_id="EV-002",
                requirement_id="REQ-SRC-006",
                source_id="SRC-002",
                claim_id="CLAIM-DECOH-BASELINE-001",
                support_level="DIRECT_SUPPORT",
                trust_level="HIGH",
                evidence_type="SOURCE_LINK",
            )
        ],
        required_requirement_ids=["REQ-SRC-006"],
    )

    assert result.support_status == "DIRECTLY_SUPPORTED"
    assert result.can_unlock_hard_claim is True
    assert result.allowed_claim_level == 5
