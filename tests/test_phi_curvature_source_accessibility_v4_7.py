"""Tests for v4.7 candidate source accessibility screen."""

from __future__ import annotations

from phyng.candidate_screening.source_accessibility import screen_source_accessibility


def test_source_accessibility_interpretation() -> None:
    # Test default/Medium quality
    inputs = {}
    screen = screen_source_accessibility(inputs)
    assert screen.source_location_quality == "MEDIUM"
    assert screen.source_accessibility_score == 0.6
    assert not screen.blockers

    # Test High quality override
    inputs_high = {"override_source_location_quality": "HIGH"}
    screen_high = screen_source_accessibility(inputs_high)
    assert screen_high.source_location_quality == "HIGH"
    assert screen_high.source_accessibility_score == 0.9

    # Test Low quality override
    inputs_low = {"override_source_location_quality": "LOW"}
    screen_low = screen_source_accessibility(inputs_low)
    assert screen_low.source_location_quality == "LOW"
    assert screen_low.source_accessibility_score == 0.2
    assert "No local or known indexed literature found" in screen_low.blockers
