"""Tests for v4.7 candidate screening decision gate."""

from __future__ import annotations

from phyng.candidate_screening.source_accessibility import screen_source_accessibility
from phyng.candidate_screening.observable_accessibility import screen_observable_accessibility
from phyng.candidate_screening.ytrue_accessibility import screen_ytrue_accessibility
from phyng.candidate_screening.public_dataset_screen import screen_public_dataset
from phyng.candidate_screening.experimental_feasibility import screen_experimental_feasibility
from phyng.candidate_screening.claim_risk import screen_claim_risk
from phyng.candidate_screening.decision import evaluate_screening_decision


def test_pass_requires_at_least_two_accessibility_criteria() -> None:
    inputs = {}
    source = screen_source_accessibility(inputs)
    observable = screen_observable_accessibility(inputs)
    ytrue = screen_ytrue_accessibility(inputs)
    public_dataset = screen_public_dataset(inputs)
    experiment = screen_experimental_feasibility(inputs)
    claim = screen_claim_risk(inputs)

    # Standard inputs have:
    # source: 0.6 (medium) -> met
    # observable: 0.8 (high) -> met
    # ytrue: 0.4 (medium) -> met
    # public_dataset: 0.5 (plausible) -> met
    # experiment: 0.8 (high) -> met
    # claim/slot4: low -> met
    # Total 6 met -> Passed the count >= 2 criteria
    decision = evaluate_screening_decision(inputs, source, observable, ytrue, public_dataset, experiment, claim)
    assert decision.final_status == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PASSED"
    assert "source_accessibility >= MEDIUM" in decision.pass_criteria_met


def test_less_than_two_criteria_fails_screen() -> None:
    # Override all to low/none
    inputs = {
        "override_source_location_quality": "LOW",
        "override_observable_clarity": "LOW",
        "override_ytrue_accessibility": "LOW",
        "override_dataset_availability": "LOW",
        "override_feasibility_level": "LOW",
        "override_slot4_independence": "INDEPENDENT",
    }
    source = screen_source_accessibility(inputs)
    observable = screen_observable_accessibility(inputs)
    ytrue = screen_ytrue_accessibility(inputs)
    public_dataset = screen_public_dataset(inputs)
    experiment = screen_experimental_feasibility(inputs)
    claim = screen_claim_risk(inputs)

    decision = evaluate_screening_decision(inputs, source, observable, ytrue, public_dataset, experiment, claim)
    assert decision.final_status == "PHI_CURVATURE_REJECTED_NO_REALITY_CONTACT"
    assert "Less than two accessibility criteria met" in decision.fail_criteria_met


def test_high_claim_risk_blocks_pass() -> None:
    inputs = {"override_physical_claim_risk": "HIGH"}
    source = screen_source_accessibility(inputs)
    observable = screen_observable_accessibility(inputs)
    ytrue = screen_ytrue_accessibility(inputs)
    public_dataset = screen_public_dataset(inputs)
    experiment = screen_experimental_feasibility(inputs)
    claim = screen_claim_risk(inputs)

    decision = evaluate_screening_decision(inputs, source, observable, ytrue, public_dataset, experiment, claim)
    # High risk blocks full pass, demotes to partial
    assert decision.final_status == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_PARTIAL"
    assert "claim risk HIGH with no mitigation" in decision.fail_criteria_met


def test_slot4_dependency_blocks_physical_candidate() -> None:
    inputs = {"override_slot4_independence": "DEPENDENT_BLOCKING"}
    source = screen_source_accessibility(inputs)
    observable = screen_observable_accessibility(inputs)
    ytrue = screen_ytrue_accessibility(inputs)
    public_dataset = screen_public_dataset(inputs)
    experiment = screen_experimental_feasibility(inputs)
    claim = screen_claim_risk(inputs)

    decision = evaluate_screening_decision(inputs, source, observable, ytrue, public_dataset, experiment, claim)
    assert decision.final_status == "PHI_CURVATURE_ACCESSIBILITY_SCREEN_FAILED"
    assert "SLOT_4 dependency remains unresolved" in decision.fail_criteria_met
