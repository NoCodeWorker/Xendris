"""Tests for v4.7 candidate y_true accessibility screen."""

from __future__ import annotations

from phyng.candidate_screening.ytrue_accessibility import screen_ytrue_accessibility


def test_ytrue_accessibility_evaluation() -> None:
    inputs = {}
    screen = screen_ytrue_accessibility(inputs)
    assert screen.minimum_ytrue_feasibility == "MEDIUM"
    assert screen.ytrue_accessibility_score == 0.4
    assert screen.experiment_required is False

    inputs_low = {"override_ytrue_accessibility": "LOW"}
    screen_low = screen_ytrue_accessibility(inputs_low)
    assert screen_low.minimum_ytrue_feasibility == "LOW"
    assert screen_low.ytrue_accessibility_score == 0.2
    assert screen_low.experiment_required is True

    inputs_none = {"override_ytrue_accessibility": "NONE"}
    screen_none = screen_ytrue_accessibility(inputs_none)
    assert screen_none.ytrue_accessibility_score == 0.0
    assert "No plausible y_true path available" in screen_none.blockers
