"""
Phygn v1.6 — Hypothesis Incubation Mode

Allows early ideas to live without being prematurely upgraded to claims.
The antidote to Phygn becoming the Grinch of hypothesis generation.

Core message to user:
  "This idea is allowed as a seed.
   It is not yet allowed as a claim.
   Here is what would make it testable."
"""

from __future__ import annotations

from phyng.epistemic_modes.schemas import (
    HypothesisSeed,
    IncubationResult,
    IncubationStatus,
    LadderLevel,
    FrictionLevel,
)

# ---------------------------------------------------------------------------
# What each incubation status means the seed is missing
# ---------------------------------------------------------------------------

_INCUBATION_MISSING: dict[IncubationStatus, list[str]] = {
    "NEEDS_OBSERVABLE":         ["possible_observable"],
    "NEEDS_VARIABLES":          ["variables"],
    "NEEDS_BASELINE":           ["baseline"],
    "NEEDS_FAILURE_CONDITION":  ["failure_condition"],
    "READY_FOR_TESTABLE_HYPOTHESIS": [],
    "INCUBATING_AS_INTUITION":  ["possible_observable", "variables", "baseline", "failure_condition"],
    "ARCHIVED_AS_POETIC_OR_ANALOGICAL": [],
}

# What friction applies per seed level
_LEVEL_FRICTION: dict[LadderLevel, FrictionLevel] = {
    "DREAM":                        "FRICTION_1_LABEL",
    "HYPOTHESIS_SEED":              "FRICTION_2_STRUCTURE",
    "FORMALIZING_HYPOTHESIS":       "FRICTION_3_REQUIRE_OBSERVABLE",
    "TESTABLE_HYPOTHESIS":          "FRICTION_4_REQUIRE_SOURCE",
    "SYNTHETIC_SUPPORT":            "FRICTION_4_REQUIRE_SOURCE",
    "SOURCE_BACKED_LIMITED":        "FRICTION_5_REQUIRE_BENCHMARK",
    "BENCHMARK_SUPPORTED":          "FRICTION_5_REQUIRE_BENCHMARK",
    "OPERATIONALLY_ACTIONABLE":     "FRICTION_6_REQUIRE_RISK_ENGINE",
    "AUTOMATED_EXECUTION_ALLOWED":  "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED",
}

# Always-allowed uses for an incubating hypothesis
_ALLOWED_USES = [
    "Record intuition privately.",
    "Link possible analogies.",
    "Add to research backlog.",
    "Suggest formalization steps.",
    "Preserve creative momentum.",
]

# Always-blocked uses for an incubating hypothesis
_BLOCKED_USES = [
    "Publication claim.",
    "Financial action.",
    "Scientific validation.",
    "Automated execution.",
]


def _classify_incubation_status(seed: HypothesisSeed) -> IncubationStatus:
    """Determine incubation status from the seed's available fields."""
    level = seed.current_level

    if level in ("DREAM", "HYPOTHESIS_SEED"):
        if seed.possible_observable is None:
            return "NEEDS_OBSERVABLE"
        if not seed.next_formalization_steps:
            return "INCUBATING_AS_INTUITION"
        return "INCUBATING_AS_INTUITION"

    if level == "FORMALIZING_HYPOTHESIS":
        if seed.possible_observable is None:
            return "NEEDS_OBSERVABLE"
        if not seed.known_unknowns:
            return "NEEDS_VARIABLES"
        return "NEEDS_BASELINE"

    if level == "TESTABLE_HYPOTHESIS":
        return "READY_FOR_TESTABLE_HYPOTHESIS"

    # Higher levels don't need incubation
    return "READY_FOR_TESTABLE_HYPOTHESIS"


def _evidence_for_next_level(seed: HypothesisSeed) -> list[str]:
    """Return what is needed to advance to the next ladder level."""
    level = seed.current_level
    if level == "DREAM":
        return [
            "Define a candidate phenomenon (rough domain).",
            "Acknowledge uncertainty explicitly.",
        ]
    if level == "HYPOTHESIS_SEED":
        return [
            "Define at least one observable quantity.",
            "Identify a plausible mechanism.",
            "Set scope limits.",
        ]
    if level == "FORMALIZING_HYPOTHESIS":
        return [
            "Define baseline model.",
            "Define candidate model.",
            "Define failure condition.",
            "Define detectability metric and threshold.",
        ]
    if level == "TESTABLE_HYPOTHESIS":
        return [
            "Run synthetic benchmark.",
            "Compute delta and max_abs_delta.",
            "Evaluate toy failure conditions.",
        ]
    if level == "SYNTHETIC_SUPPORT":
        return [
            "Obtain source support (published papers / experimental references).",
            "Link sources to claims.",
        ]
    if level == "SOURCE_BACKED_LIMITED":
        return [
            "Obtain real or literature-extracted y_true data.",
            "Run baseline comparison.",
            "Compute uncertainty.",
        ]
    if level == "BENCHMARK_SUPPORTED":
        return [
            "Complete risk assessment.",
            "Define failure protocol and monitoring plan.",
            "Obtain human review if needed.",
        ]
    if level == "OPERATIONALLY_ACTIONABLE":
        return [
            "Deploy risk engine.",
            "Implement logging and rollback.",
            "Obtain compliance review.",
            "Implement kill switch.",
        ]
    return []


def incubate_hypothesis(seed: HypothesisSeed) -> IncubationResult:
    """
    Process a HypothesisSeed through incubation.

    Returns an IncubationResult with:
        - allowed_use (always: record, backlog, formalization)
        - blocked_use (always: publication, action, execution)
        - next_formalization_steps
        - required_evidence_for_next_level
        - incubation_status
        - friction_level
    """
    status = _classify_incubation_status(seed)
    next_evidence = _evidence_for_next_level(seed)
    friction = _LEVEL_FRICTION.get(seed.current_level, "FRICTION_2_STRUCTURE")

    # Combine seed-defined steps with generated steps
    all_next_steps = list(seed.next_formalization_steps) + [
        s for s in next_evidence if s not in seed.next_formalization_steps
    ]

    return IncubationResult(
        seed_id=seed.seed_id,
        current_level=seed.current_level,
        incubation_status=status,
        allowed_use=_ALLOWED_USES,
        blocked_use=_BLOCKED_USES + list(seed.forbidden_claims),
        next_formalization_steps=all_next_steps,
        required_evidence_for_next_level=next_evidence,
        friction_level=friction,
    )
