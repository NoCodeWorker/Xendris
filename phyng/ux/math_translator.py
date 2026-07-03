"""
Phygn v1.7 — UX: Math Translator

Converts natural language intuition into candidate testable structures.
All outputs are labeled SUGGESTED_NOT_VALIDATED.

Rule: LLM proposes. Phygn verifies.
This module provides the deterministic/heuristic translation layer.
When an LLM is available, its proposals feed into this structure
but must be validated by the Phygn gate system before use.
"""

from __future__ import annotations

from phyng.ux.idea_intake import IdeaIntake, MathTranslatorOutput


# ---------------------------------------------------------------------------
# Domain-specific heuristic templates
# ---------------------------------------------------------------------------

_DOMAIN_TEMPLATES: dict[str, dict[str, list[str]]] = {
    "finance": {
        "x_variables": ["price", "volume", "sentiment score", "news count", "earnings surprise"],
        "y_observables": ["return (N-day)", "direction (up/down)", "volatility change"],
        "proxies": ["relative volume", "RSI", "VWAP deviation", "social mention count"],
        "baselines": ["buy-and-hold return", "market index return", "random walk null"],
        "failure_conditions": ["no significant return difference vs baseline over N periods"],
    },
    "quantum_decoherence": {
        "x_variables": ["mass", "length scale", "gravitational parameter B"],
        "y_observables": ["visibility loss", "decoherence rate", "coherence time"],
        "proxies": ["fringe contrast", "visibility V(t)", "decay rate Γ"],
        "baselines": ["exp(-Γ_env * t) — environment-only model"],
        "failure_conditions": ["|delta| < epsilon_exp over entire time grid"],
    },
    "biology": {
        "x_variables": ["gene expression", "protein concentration", "stimulus intensity"],
        "y_observables": ["cell viability", "proliferation rate", "apoptosis rate"],
        "proxies": ["fluorescence intensity", "OD600", "qPCR Ct value"],
        "baselines": ["untreated control group mean"],
        "failure_conditions": ["no statistically significant difference from control"],
    },
    "default": {
        "x_variables": ["independent variable X (to be defined by user)"],
        "y_observables": ["dependent variable Y (to be defined by user)"],
        "proxies": ["measurable proxy for Y (to be identified)"],
        "baselines": ["null hypothesis: X has no effect on Y"],
        "failure_conditions": ["effect not detectable above declared threshold"],
    },
}

_TEST_PLAN_TEMPLATE = [
    "Step 1: Define precise operationalization of X and Y.",
    "Step 2: Collect or simulate data for X and Y.",
    "Step 3: Define baseline model prediction.",
    "Step 4: Compute candidate model prediction.",
    "Step 5: Compute delta (candidate − baseline).",
    "Step 6: Compare delta against detectability threshold.",
    "Step 7: Evaluate failure conditions.",
    "Step 8: Report result with allowed/blocked claims.",
]


def translate_intuition_to_testable_structure(
    intuition: str,
    domain: str | None,
    intended_use: str,
    idea_id: str | None = None,
) -> MathTranslatorOutput:
    """
    Convert natural language intuition into candidate testable structures.

    All outputs are SUGGESTED_NOT_VALIDATED. The user or a validated LLM
    must review and confirm before the hypothesis advances to TESTABLE_HYPOTHESIS.

    Args:
        intuition: Free-text natural language intuition.
        domain: Optional domain string (e.g. "finance", "biology").
        intended_use: What the user intends to do with the output.
        idea_id: Optional idea identifier.

    Returns:
        MathTranslatorOutput with candidate variables, observables, proxies, etc.
    """
    _id = idea_id or "IDEA-UNKNOWN"
    template = _DOMAIN_TEMPLATES.get(domain or "default", _DOMAIN_TEMPLATES["default"])

    # Build a candidate hypothesis from the intuition
    candidate_hyp = (
        f"It is hypothesized that a change in [{template['x_variables'][0]}] "
        f"leads to an observable change in [{template['y_observables'][0]}]. "
        f"(SUGGESTED_NOT_VALIDATED from: '{intuition[:100]}')"
    )

    return MathTranslatorOutput(
        idea_id=_id,
        label="SUGGESTED_NOT_VALIDATED",
        possible_x_variables=template["x_variables"],
        possible_y_observables=template["y_observables"],
        proxy_candidates=template["proxies"],
        baseline_candidates=template["baselines"],
        failure_condition_candidates=template["failure_conditions"],
        test_plan_candidates=_TEST_PLAN_TEMPLATE,
        candidate_hypothesis_text=candidate_hyp,
    )


def translate_from_intake(intake: IdeaIntake) -> MathTranslatorOutput:
    """Convenience: translate directly from an IdeaIntake object."""
    return translate_intuition_to_testable_structure(
        intuition=intake.raw_intuition,
        domain=intake.domain,
        intended_use=intake.intended_use,
        idea_id=intake.idea_id,
    )
