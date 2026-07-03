from phyng.campaigns.non_inflation import evaluate_claim_level


def test_claim_level_overreach_blocked():
    decision = evaluate_claim_level(evidence_level=3, requested_claim_level=6)

    assert decision.decision == "BLOCKED_OVERCLAIM"
    assert decision.safe_rewrite is not None
    assert "No physical decoherence prediction is claimed" in decision.safe_rewrite


def test_claim_level_within_evidence_allowed():
    decision = evaluate_claim_level(evidence_level=3, requested_claim_level=3)

    assert decision.decision == "ALLOWED_WITHIN_EVIDENCE_LEVEL"
