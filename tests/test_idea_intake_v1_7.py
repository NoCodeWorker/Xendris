"""
Tests v1.7 — UX: Idea Intake & Seed Card
"""

import pytest
from phyng.ux.idea_intake import IdeaIntake
from phyng.ux.hypothesis_builder import process_idea_intake


def test_idea_intake_creates_seed_card():
    intake = IdeaIntake(
        raw_intuition="Maybe gravitational effects trigger decoherence at the Planck boundary.",
        domain="quantum_decoherence",
        possible_cause="Planck length ratio",
        possible_effect="faster decay",
    )
    card = process_idea_intake(intake)
    assert card.idea_id == intake.idea_id
    assert "faster decay" in card.cleaned_hypothesis
    assert card.proposal_label == "SUGGESTED_NOT_VALIDATED"
    assert len(card.candidate_variables) > 0
    assert len(card.missing_information) > 0


def test_seed_card_allows_exploration_blocks_claim():
    intake = IdeaIntake(
        raw_intuition="Metaphors are nice",
        domain="general",
    )
    card = process_idea_intake(intake)
    # Check that private/exploration is allowed
    assert any("explore" in u.lower() or "private" in u.lower() for u in card.allowed_uses)
    # Check that publication/automated execution is blocked
    assert any("publish" in b.lower() for b in card.blocked_uses)
    assert any("execution" in b.lower() for b in card.blocked_uses)
