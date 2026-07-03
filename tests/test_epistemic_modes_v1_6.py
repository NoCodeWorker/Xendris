"""
Tests v1.6 — Epistemic Modes Schemas and Mode Definitions

Tests:
    test_all_modes_have_risk_mapping
    test_dream_mode_is_low_risk
    test_automated_execution_is_high_risk
    test_mode_descriptions_non_empty
"""

import pytest
from typing import cast
from phyng.epistemic_modes.schemas import EpistemicMode
from phyng.epistemic_modes.modes import (
    MODE_DEFAULT_RISK,
    get_mode_risk,
    get_mode_description,
    is_high_risk_mode,
    is_low_risk_mode,
)
from phyng.epistemic_modes.schemas import HypothesisSeed, ModeGateResult


ALL_MODES = [
    "DREAM_MODE", "EXPLORATION_MODE", "HYPOTHESIS_MODE", "TEST_DESIGN_MODE",
    "CLAIM_MODE", "PUBLICATION_MODE", "FINANCIAL_ACTION_MODE", "AUTOMATED_EXECUTION_MODE",
]


def test_all_modes_have_risk_mapping():
    for mode in ALL_MODES:
        assert mode in MODE_DEFAULT_RISK


def test_dream_mode_is_low_risk():
    assert is_low_risk_mode("DREAM_MODE")
    assert not is_high_risk_mode("DREAM_MODE")


def test_automated_execution_is_high_risk():
    assert is_high_risk_mode("AUTOMATED_EXECUTION_MODE")
    assert not is_low_risk_mode("AUTOMATED_EXECUTION_MODE")


def test_financial_action_is_high_risk():
    assert is_high_risk_mode("FINANCIAL_ACTION_MODE")


def test_mode_descriptions_non_empty():
    for mode in ALL_MODES:
        desc = get_mode_description(cast(EpistemicMode, mode))
        assert isinstance(desc, str) and len(desc) > 0


def test_get_mode_risk_dream():
    assert get_mode_risk("DREAM_MODE") == "RISK_0_PRIVATE_THOUGHT"


def test_get_mode_risk_execution():
    assert get_mode_risk("AUTOMATED_EXECUTION_MODE") == "RISK_7_AUTOMATED_EXECUTION"


def test_hypothesis_seed_schema_defaults():
    seed = HypothesisSeed(
        seed_id="TEST-001",
        title="Test hypothesis",
        intuition="Maybe X causes Y.",
        domain="physics",
    )
    assert seed.current_level == "DREAM"
    assert seed.risk_level == "RISK_1_INTERNAL_NOTE"
    assert seed.known_unknowns == []
    assert seed.forbidden_claims == []
