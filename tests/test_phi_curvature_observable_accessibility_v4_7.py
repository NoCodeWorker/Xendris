"""Tests for v4.7 candidate observable accessibility screen."""

from __future__ import annotations

from phyng.candidate_screening.observable_accessibility import screen_observable_accessibility


def test_observable_accessibility_clarity() -> None:
    inputs = {}
    screen = screen_observable_accessibility(inputs)
    assert screen.observable_clarity == "HIGH"
    assert screen.observable_accessibility_score == 0.8
    assert "CURVATURE_PROXY" in screen.observable_classes

    inputs_med = {"override_observable_clarity": "MEDIUM"}
    screen_med = screen_observable_accessibility(inputs_med)
    assert screen_med.observable_clarity == "MEDIUM"
    assert screen_med.observable_accessibility_score == 0.5
