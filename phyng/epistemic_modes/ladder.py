"""
Phygn v1.6 — Dream-to-Claim Ladder

Classifies an input (text, evidence fields) into a ladder level from
DREAM (level 0) to AUTOMATED_EXECUTION_ALLOWED (level 8).

The ladder prevents two opposite errors:
  - killing ideas too early
  - letting ideas masquerade as truth too early
"""

from __future__ import annotations

from phyng.epistemic_modes.schemas import (
    LadderLevel,
    LadderClassification,
    GateStatus,
)

# ---------------------------------------------------------------------------
# Ladder index mapping
# ---------------------------------------------------------------------------

LADDER_ORDER: list[LadderLevel] = [
    "DREAM",
    "HYPOTHESIS_SEED",
    "FORMALIZING_HYPOTHESIS",
    "TESTABLE_HYPOTHESIS",
    "SYNTHETIC_SUPPORT",
    "SOURCE_BACKED_LIMITED",
    "BENCHMARK_SUPPORTED",
    "OPERATIONALLY_ACTIONABLE",
    "AUTOMATED_EXECUTION_ALLOWED",
]

LADDER_INDEX: dict[LadderLevel, int] = {lv: i for i, lv in enumerate(LADDER_ORDER)}

# What each level requires to be valid
LADDER_REQUIREMENTS: dict[LadderLevel, list[str]] = {
    "DREAM":                    [],
    "HYPOTHESIS_SEED":          ["candidate_phenomenon", "domain", "uncertainty_acknowledged"],
    "FORMALIZING_HYPOTHESIS":   ["variables", "possible_observable", "rough_mechanism", "scope_boundary"],
    "TESTABLE_HYPOTHESIS":      ["observable", "baseline", "candidate_model", "failure_condition", "metric", "detectability_threshold"],
    "SYNTHETIC_SUPPORT":        ["synthetic_benchmark", "delta_computation", "toy_failure_conditions"],
    "SOURCE_BACKED_LIMITED":    ["source_audit", "claim_source_links", "source_support"],
    "BENCHMARK_SUPPORTED":      ["y_true", "baseline_comparison", "metric", "uncertainty"],
    "OPERATIONALLY_ACTIONABLE": ["risk_assessment", "scope_limits", "failure_protocol", "monitoring"],
    "AUTOMATED_EXECUTION_ALLOWED": ["strong_evidence", "risk_engine", "logging", "rollback", "kill_switch", "compliance_review"],
}

# What is allowed at each level
LADDER_IDEA_ALLOWED: set[LadderLevel] = set(LADDER_ORDER)  # ideas always allowed
LADDER_CLAIM_ALLOWED: set[LadderLevel] = {
    "SOURCE_BACKED_LIMITED",
    "BENCHMARK_SUPPORTED",
    "OPERATIONALLY_ACTIONABLE",
    "AUTOMATED_EXECUTION_ALLOWED",
}
LADDER_ACTION_ALLOWED: set[LadderLevel] = {
    "OPERATIONALLY_ACTIONABLE",
    "AUTOMATED_EXECUTION_ALLOWED",
}
LADDER_EXECUTION_ALLOWED: set[LadderLevel] = {
    "AUTOMATED_EXECUTION_ALLOWED",
}

# Status per level
LADDER_STATUS: dict[LadderLevel, GateStatus] = {
    "DREAM":                        "IDEA_ALLOWED",
    "HYPOTHESIS_SEED":              "HYPOTHESIS_SEED",
    "FORMALIZING_HYPOTHESIS":       "HYPOTHESIS_INCUBATING",
    "TESTABLE_HYPOTHESIS":          "HYPOTHESIS_TESTABLE",
    "SYNTHETIC_SUPPORT":            "CLAIM_REQUIRES_EVIDENCE",
    "SOURCE_BACKED_LIMITED":        "CLAIM_ALLOWED_LIMITED",
    "BENCHMARK_SUPPORTED":          "CLAIM_ALLOWED_LIMITED",
    "OPERATIONALLY_ACTIONABLE":     "ACTION_REQUIRES_RISK_GATE",
    "AUTOMATED_EXECUTION_ALLOWED":  "EXECUTION_ALLOWED_LIMITED",
}


def classify_ladder_level(
    input_text: str,
    requested_use: str,
    available_evidence: list[str],
) -> LadderClassification:
    """
    Classify the ladder level of an input based on available evidence.

    Args:
        input_text: Raw text of the idea or claim.
        requested_use: What the user wants to do with it (e.g. "publish", "dream", "trade").
        available_evidence: List of evidence keys present (e.g. ["observable", "baseline"]).

    Returns:
        LadderClassification with the appropriate ladder level and gate permissions.
    """
    # Walk the ladder from top to bottom; pick the highest level satisfied
    reached_level: LadderLevel = "DREAM"
    for level in LADDER_ORDER:
        required = LADDER_REQUIREMENTS[level]
        if all(req in available_evidence for req in required):
            reached_level = level
        else:
            break  # can't skip rungs

    idx = LADDER_INDEX[reached_level]
    missing = [
        req
        for req in LADDER_REQUIREMENTS.get(LADDER_ORDER[min(idx + 1, 8)], [])
        if req not in available_evidence
    ]

    return LadderClassification(
        ladder_level=reached_level,
        level_index=idx,
        idea_allowed=reached_level in LADDER_IDEA_ALLOWED,
        claim_allowed=reached_level in LADDER_CLAIM_ALLOWED,
        action_allowed=reached_level in LADDER_ACTION_ALLOWED,
        execution_allowed=reached_level in LADDER_EXECUTION_ALLOWED,
        status=LADDER_STATUS[reached_level],
        missing_for_next_level=missing,
    )


def get_ladder_level_name(index: int) -> LadderLevel:
    """Return the ladder level for a given index (0–8)."""
    return LADDER_ORDER[max(0, min(index, 8))]
