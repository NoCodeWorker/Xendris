"""Tests for v4.7 candidate public dataset screen."""

from __future__ import annotations

from phyng.candidate_screening.public_dataset_screen import screen_public_dataset


def test_public_dataset_availability() -> None:
    inputs = {}
    screen = screen_public_dataset(inputs)
    # Selection matrix record has PLAUSIBLE public dataset availability
    assert screen.dataset_availability == "PLAUSIBLE"
    assert screen.dataset_accessibility_score == 0.5
    assert "ZENODO" in screen.plausible_repository_types

    inputs_none = {"override_dataset_availability": "NONE"}
    screen_none = screen_public_dataset(inputs_none)
    assert screen_none.dataset_availability == "NONE"
    assert screen_none.dataset_accessibility_score == 0.0
