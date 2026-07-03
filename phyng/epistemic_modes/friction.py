"""
Phygn v1.6 — Friction Gradient Evaluator

Maps (RiskLevel × EpistemicMode) → FrictionDecision.

Rule: friction scales with harm, not with imagination.
Low risk → allow/label/structure.
High risk → require evidence/risk/human approval/block.
"""

from __future__ import annotations

from phyng.epistemic_modes.schemas import (
    EpistemicMode,
    RiskLevel,
    FrictionLevel,
    FrictionDecision,
)

# ---------------------------------------------------------------------------
# Risk-level index (higher = more friction)
# ---------------------------------------------------------------------------

RISK_INDEX: dict[RiskLevel, int] = {
    "RISK_0_PRIVATE_THOUGHT":       0,
    "RISK_1_INTERNAL_NOTE":         1,
    "RISK_2_INTERNAL_RESEARCH":     2,
    "RISK_3_PUBLIC_CONTENT":        3,
    "RISK_4_CLIENT_DELIVERABLE":    4,
    "RISK_5_FINANCIAL_RECOMMENDATION": 5,
    "RISK_6_REAL_WORLD_ACTION":     6,
    "RISK_7_AUTOMATED_EXECUTION":   7,
}

# Default friction for each risk level (per protocol doc §4)
RISK_TO_DEFAULT_FRICTION: dict[RiskLevel, FrictionLevel] = {
    "RISK_0_PRIVATE_THOUGHT":          "FRICTION_0_FREE",
    "RISK_1_INTERNAL_NOTE":            "FRICTION_1_LABEL",
    "RISK_2_INTERNAL_RESEARCH":        "FRICTION_3_REQUIRE_OBSERVABLE",
    "RISK_3_PUBLIC_CONTENT":           "FRICTION_4_REQUIRE_SOURCE",
    "RISK_4_CLIENT_DELIVERABLE":       "FRICTION_5_REQUIRE_BENCHMARK",
    "RISK_5_FINANCIAL_RECOMMENDATION": "FRICTION_6_REQUIRE_RISK_ENGINE",
    "RISK_6_REAL_WORLD_ACTION":        "FRICTION_7_REQUIRE_HUMAN_APPROVAL",
    "RISK_7_AUTOMATED_EXECUTION":      "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED",
}

FRICTION_INDEX: dict[FrictionLevel, int] = {
    "FRICTION_0_FREE":                       0,
    "FRICTION_1_LABEL":                      1,
    "FRICTION_2_STRUCTURE":                  2,
    "FRICTION_3_REQUIRE_OBSERVABLE":         3,
    "FRICTION_4_REQUIRE_SOURCE":             4,
    "FRICTION_5_REQUIRE_BENCHMARK":          5,
    "FRICTION_6_REQUIRE_RISK_ENGINE":        6,
    "FRICTION_7_REQUIRE_HUMAN_APPROVAL":     7,
    "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED": 8,
}

FRICTION_LEVELS_LIST: list[FrictionLevel] = [
    "FRICTION_0_FREE",
    "FRICTION_1_LABEL",
    "FRICTION_2_STRUCTURE",
    "FRICTION_3_REQUIRE_OBSERVABLE",
    "FRICTION_4_REQUIRE_SOURCE",
    "FRICTION_5_REQUIRE_BENCHMARK",
    "FRICTION_6_REQUIRE_RISK_ENGINE",
    "FRICTION_7_REQUIRE_HUMAN_APPROVAL",
    "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED",
]

# Mode-based friction floor (modes that force a minimum friction regardless of risk)
MODE_FRICTION_FLOOR: dict[EpistemicMode, int] = {
    "DREAM_MODE":               0,
    "EXPLORATION_MODE":         1,
    "HYPOTHESIS_MODE":          2,
    "TEST_DESIGN_MODE":         3,
    "CLAIM_MODE":               4,
    "PUBLICATION_MODE":         5,
    "FINANCIAL_ACTION_MODE":    6,
    "AUTOMATED_EXECUTION_MODE": 8,
}


def evaluate_friction(
    risk_level: RiskLevel,
    mode: EpistemicMode,
) -> FrictionDecision:
    """
    Compute the friction decision for a given (risk_level, mode) pair.

    The actual friction is max(risk-default-friction, mode-floor).
    """
    risk_friction_idx = FRICTION_INDEX[RISK_TO_DEFAULT_FRICTION[risk_level]]
    mode_floor_idx = MODE_FRICTION_FLOOR[mode]

    # Effective friction = whichever is higher
    effective_idx = max(risk_friction_idx, mode_floor_idx)
    effective_friction: FrictionLevel = FRICTION_LEVELS_LIST[effective_idx]

    is_blocked = effective_idx >= 8
    requires_human = effective_idx >= 7

    # Build gate notes
    notes: list[str] = []
    if effective_idx == 0:
        notes.append("Free: no friction required.")
    elif effective_idx == 1:
        notes.append("Label required: mark as intuition/internal.")
    elif effective_idx == 2:
        notes.append("Structure required: define domain and format.")
    elif effective_idx == 3:
        notes.append("Observable required before proceeding.")
    elif effective_idx == 4:
        notes.append("Source backing required.")
    elif effective_idx == 5:
        notes.append("Benchmark / backtest required.")
    elif effective_idx == 6:
        notes.append("Risk engine evaluation required.")
    elif effective_idx == 7:
        notes.append("Human approval required before any action.")
    elif effective_idx == 8:
        notes.append("BLOCKED unless fully authorized.")

    return FrictionDecision(
        risk_level=risk_level,
        mode=mode,
        friction_level=effective_friction,
        is_blocked=is_blocked,
        requires_human_approval=requires_human,
        gate_notes=notes,
    )


def get_friction_for_risk(risk_level: RiskLevel) -> FrictionLevel:
    """Convenience: return default friction for a risk level."""
    return RISK_TO_DEFAULT_FRICTION[risk_level]
