"""Tests for v4.7 candidate claim risk screen."""

from __future__ import annotations

from phyng.candidate_screening.claim_risk import screen_claim_risk


def test_claim_risk_evaluation() -> None:
    inputs = {}
    screen = screen_claim_risk(inputs)
    # Selection matrix record has LOW claim risk and INDEPENDENT slot4
    assert screen.physical_claim_risk == "LOW"
    assert screen.slot4_dependency_risk == "LOW"
    assert screen.claim_risk_score == 0.2

    inputs_high = {"override_physical_claim_risk": "HIGH"}
    screen_high = screen_claim_risk(inputs_high)
    assert screen_high.physical_claim_risk == "HIGH"
    assert screen_high.claim_risk_score == 0.8

    inputs_dep = {"override_slot4_independence": "DEPENDENT_BLOCKING"}
    screen_dep = screen_claim_risk(inputs_dep)
    assert screen_dep.slot4_dependency_risk == "HIGH"
    assert screen_dep.claim_risk_score == 0.8
