"""Tests for v4.7 candidate experimental feasibility screen."""

from __future__ import annotations

from phyng.candidate_screening.experimental_feasibility import screen_experimental_feasibility


def test_experimental_feasibility_level() -> None:
    inputs = {}
    screen = screen_experimental_feasibility(inputs)
    # Selection matrix record has HIGH experimental feasibility
    assert screen.feasibility_level == "HIGH"
    assert screen.experiment_accessibility_score == 0.8
    assert screen.cost_risk == "MEDIUM"

    inputs_low = {"override_feasibility_level": "LOW"}
    screen_low = screen_experimental_feasibility(inputs_low)
    assert screen_low.feasibility_level == "LOW"
    assert screen_low.experiment_accessibility_score == 0.2
    assert screen_low.cost_risk == "HIGH"
