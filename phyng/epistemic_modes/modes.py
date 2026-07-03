"""
Phygn v1.6 — Epistemic Modes: Mode Definitions

Maps each EpistemicMode to its inherent risk level and default permissions.
"""

from __future__ import annotations

from phyng.epistemic_modes.schemas import (
    EpistemicMode,
    RiskLevel,
    FrictionLevel,
)

# ---------------------------------------------------------------------------
# Mode → default risk level mapping
# ---------------------------------------------------------------------------

MODE_DEFAULT_RISK: dict[EpistemicMode, RiskLevel] = {
    "DREAM_MODE":               "RISK_0_PRIVATE_THOUGHT",
    "EXPLORATION_MODE":         "RISK_1_INTERNAL_NOTE",
    "HYPOTHESIS_MODE":          "RISK_2_INTERNAL_RESEARCH",
    "TEST_DESIGN_MODE":         "RISK_2_INTERNAL_RESEARCH",
    "CLAIM_MODE":               "RISK_3_PUBLIC_CONTENT",
    "PUBLICATION_MODE":         "RISK_4_CLIENT_DELIVERABLE",
    "FINANCIAL_ACTION_MODE":    "RISK_5_FINANCIAL_RECOMMENDATION",
    "AUTOMATED_EXECUTION_MODE": "RISK_7_AUTOMATED_EXECUTION",
}

# ---------------------------------------------------------------------------
# Mode-level descriptions
# ---------------------------------------------------------------------------

MODE_DESCRIPTIONS: dict[EpistemicMode, str] = {
    "DREAM_MODE":               "Free intuition, metaphor, speculative association, aesthetic idea.",
    "EXPLORATION_MODE":         "Structured but informal exploration of an idea or domain.",
    "HYPOTHESIS_MODE":          "An idea stated as a possible relation, with rough observable.",
    "TEST_DESIGN_MODE":         "Formal testable hypothesis with baseline, metric, and failure conditions.",
    "CLAIM_MODE":               "A factual claim about the world, intended for internal or external use.",
    "PUBLICATION_MODE":         "A public-facing claim or deliverable with external impact.",
    "FINANCIAL_ACTION_MODE":    "A recommendation or action with financial consequence.",
    "AUTOMATED_EXECUTION_MODE": "Automated system action with real-world irreversible effects.",
}


def get_mode_risk(mode: EpistemicMode) -> RiskLevel:
    """Return the default risk level for a given epistemic mode."""
    return MODE_DEFAULT_RISK[mode]


def get_mode_description(mode: EpistemicMode) -> str:
    """Return a human-readable description of the mode."""
    return MODE_DESCRIPTIONS[mode]


def is_high_risk_mode(mode: EpistemicMode) -> bool:
    """True for modes that carry RISK_4 or higher."""
    high_risk = {
        "CLAIM_MODE",
        "PUBLICATION_MODE",
        "FINANCIAL_ACTION_MODE",
        "AUTOMATED_EXECUTION_MODE",
    }
    return mode in high_risk


def is_low_risk_mode(mode: EpistemicMode) -> bool:
    """True for modes that carry RISK_2 or lower."""
    low_risk = {
        "DREAM_MODE",
        "EXPLORATION_MODE",
        "HYPOTHESIS_MODE",
        "TEST_DESIGN_MODE",
    }
    return mode in low_risk
