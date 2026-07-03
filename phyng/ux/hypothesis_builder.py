"""
Phygn v1.7 — UX: Hypothesis Builder

process_idea_intake: converts IdeaIntake → HypothesisSeedCard.

All output is labeled SUGGESTED_NOT_VALIDATED and is allowed only
for private exploration and hypothesis seed purposes. Claims and
actions remain blocked until evidence is obtained.
"""

from __future__ import annotations

from phyng.ux.idea_intake import IdeaIntake, HypothesisSeedCard

# Always-allowed uses at seed level
_ALLOWED_USES = [
    "Explore privately as a hypothesis seed.",
    "Record intuition for research backlog.",
    "Share as a draft (not a claim) with collaborators.",
    "Use as starting point for formal hypothesis design.",
]

# Always-blocked uses at seed level
_BLOCKED_USES = [
    "Publish as a scientific fact.",
    "Use for client deliverable or recommendation.",
    "Financial action or trade execution.",
    "Automated execution of any kind.",
    "Clinical or legal claim.",
]

# Guided questions to advance formalization
_GUIDED_QUESTIONS = [
    "What do you think influences what? (cause → effect)",
    "What would you expect to observe if the idea is correct?",
    "When would you expect to see the effect? (time horizon)",
    "What would prove you wrong? (failure condition)",
    "What data could represent this idea? (proxy / observable)",
    "What is the baseline? (no-effect expectation)",
    "What is the cost of being wrong? (risk level)",
    "Is this private exploration, public claim, or action?",
]

_MINIMUM_TEST_PLAN = [
    "Define at least one observable quantity.",
    "Define a baseline model (no-effect expectation).",
    "Define a candidate model (with-effect expectation).",
    "Define a detectability threshold.",
    "Define a failure condition (when the hypothesis is falsified).",
    "Run synthetic benchmark to compute delta.",
]


def _build_title(intake: IdeaIntake) -> str:
    """Create a cleaned-up title from the intake."""
    intuition = intake.raw_intuition.strip()
    domain = f"[{intake.domain}] " if intake.domain else ""
    return f"{domain}{intuition[:80]}{'...' if len(intuition) > 80 else ''}"


def _build_cleaned_hypothesis(intake: IdeaIntake) -> str:
    """
    Produce a lightly structured hypothesis statement.
    Does NOT require the user to provide variables or equations.
    """
    cause = intake.possible_cause or "an unknown cause"
    effect = intake.possible_effect or "an observable effect"
    relation = intake.suspected_relation or f"{cause} may influence {effect}"
    domain = f"in the domain of {intake.domain}" if intake.domain else ""
    return f"It is hypothesized that {relation} {domain}. (SUGGESTED_NOT_VALIDATED)".strip()


def _infer_candidate_variables(intake: IdeaIntake) -> list[str]:
    """Extract candidate variables from free-text fields."""
    candidates: list[str] = []
    if intake.possible_cause:
        candidates.append(f"X (cause): {intake.possible_cause}")
    if intake.possible_effect:
        candidates.append(f"Y (effect): {intake.possible_effect}")
    if intake.suspected_relation:
        candidates.append(f"Relation: {intake.suspected_relation}")
    if not candidates:
        candidates.append("X (cause): to be defined")
        candidates.append("Y (effect): to be defined")
    return candidates


def _infer_missing_information(intake: IdeaIntake) -> list[str]:
    """List what information is still missing."""
    missing: list[str] = []
    if not intake.possible_cause:
        missing.append("Causal variable (X) not specified.")
    if not intake.possible_effect:
        missing.append("Effect variable (Y) not specified.")
    if not intake.suspected_relation:
        missing.append("Suspected relation (X → Y) not stated.")
    if not intake.domain:
        missing.append("Domain not specified.")
    missing.append("Observable quantity not yet defined.")
    missing.append("Baseline model not yet defined.")
    missing.append("Failure condition not yet defined.")
    return missing


def process_idea_intake(intake: IdeaIntake) -> HypothesisSeedCard:
    """
    Convert a raw IdeaIntake into a HypothesisSeedCard.

    No LLM call. All outputs are SUGGESTED_NOT_VALIDATED.
    The user does not need a mathematical model to use this function.
    """
    title = _build_title(intake)
    cleaned = _build_cleaned_hypothesis(intake)
    variables = _infer_candidate_variables(intake)
    missing = _infer_missing_information(intake)

    # Infer observables and proxies from available free text
    observables: list[str] = []
    proxies: list[str] = []
    if intake.possible_effect:
        observables.append(f"Possible observable: {intake.possible_effect} (to be operationalized)")
        proxies.append(f"Proxy candidate: any measurable proxy for '{intake.possible_effect}'")
    else:
        observables.append("Observable: to be defined — what changes when the hypothesis is true?")
        proxies.append("Proxy: to be defined — what data could stand in for the observable?")

    return HypothesisSeedCard(
        idea_id=intake.idea_id,
        title=title,
        raw_intuition=intake.raw_intuition,
        cleaned_hypothesis=cleaned,
        current_ladder_level="HYPOTHESIS_SEED",
        ux_status="HYPOTHESIS_SEED_CREATED",
        allowed_uses=_ALLOWED_USES,
        blocked_uses=_BLOCKED_USES,
        candidate_variables=variables,
        candidate_observables=observables,
        candidate_proxies=proxies,
        missing_information=missing,
        next_best_questions=_GUIDED_QUESTIONS,
        minimum_test_plan=_MINIMUM_TEST_PLAN,
        proposal_label="SUGGESTED_NOT_VALIDATED",
    )
