"""
Phygn v1.8 — Socratic Question Engine

Determines the next best question to ask the user, based on the missing fields
in the HypothesisCardState and priority ranking.
"""

from __future__ import annotations

import uuid
from phyng.copilot.schemas import NextBestQuestion, HypothesisCardState, QuestionType


# Priority ranking for general hypothesis development:
# 1. CLARIFY_TERM / CONFIRM_SCOPE (relation clarify)
# 2. DEFINE_VARIABLE (independent / dependent variables)
# 3. DEFINE_OBSERVABLE (what is measured)
# 4. DEFINE_FAILURE_CONDITION (falsification)
# 5. DEFINE_TIME_HORIZON (duration / grid)
# 6. CHOOSE_BASELINE (reference model)
# 7. SELECT_PROXY (measurement stand-in)
# 8. CHOOSE_BENCHMARK / REQUEST_SOURCE (source backed check)
# 9. CHOOSE_METRIC (comparison metrics)
# 10. ASSESS_RISK (risk alignment)

def generate_next_best_question(
    input_text: str,
    hypothesis_card: HypothesisCardState | None,
    mode: str,
    risk_level: str,
) -> NextBestQuestion:
    """
    Generate one next best question based on missing hypothesis card fields or input text context.

    Rank missing fields by epistemic leverage:
      - relation / term clarification
      - variables
      - observables
      - failure condition
      - time horizon
      - baseline / proxy
      - sources / benchmarks
      - metrics
    """
    # If no card exists, initialize a skeleton card or analyze input text directly
    card = hypothesis_card or HypothesisCardState(
        raw_idea=input_text,
        risk_level=risk_level,
    )

    # Heuristics for specific inputs if card lacks details
    is_finance = "btc" in input_text.lower() or "price" in input_text.lower() or "market" in input_text.lower() or "invest" in input_text.lower()
    is_scientific = "frontera" in input_text.lower() or "decoherence" in input_text.lower() or "quantum" in input_text.lower()
    is_business = "companies" in input_text.lower() or "pay" in input_text.lower() or "customer" in input_text.lower()

    # 1. Clarify Term / Relation
    if not card.suspected_relation:
        if is_business:
            return NextBestQuestion(
                question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
                question_type="CLARIFY_TERM",
                question_text="Who exactly would pay first for these audits?",
                why_needed="Without buyer definition, willingness-to-pay cannot be tested.",
                answer_options=["startup founder", "investor / fund", "consultant", "corporate innovation team", "other"],
                free_text_allowed=True,
                updates_fields=["suspected_relation"],
                blocks_until_answered=["suspected_relation"]
            )
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="CLARIFY_TERM",
            question_text="Could you clarify what suspected relation you are proposing between the variables?",
            why_needed="We need a clear cause-and-effect relationship to begin formalization.",
            answer_options=["X causes Y directly", "X modulates Y through a third factor", "X and Y are correlated", "other"],
            free_text_allowed=True,
            updates_fields=["suspected_relation"],
            blocks_until_answered=["suspected_relation"]
        )

    # 2. Variables
    if not card.variables:
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_VARIABLE",
            question_text="What is the primary independent variable (X) and dependent variable (Y) in this idea?",
            why_needed="To build a testable structure, we must identify the variables to vary and measure.",
            answer_options=[],
            free_text_allowed=True,
            updates_fields=["variables"],
            blocks_until_answered=["variables"]
        )

    # 3. Observables
    if not card.observables:
        if is_scientific:
            return NextBestQuestion(
                question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
                question_type="DEFINE_OBSERVABLE",
                question_text="What observable would change if Frontera C was active?",
                why_needed="A physical hypothesis needs an observable before it can become testable.",
                answer_options=["visibility decay curve", "coherence time", "interference contrast", "environmental decoherence rate", "other"],
                free_text_allowed=True,
                updates_fields=["observables"],
                blocks_until_answered=["observables"]
            )
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_OBSERVABLE",
            question_text="What primary quantity would you observe or measure to test this?",
            why_needed="A hypothesis must be grounded in an observable quantity.",
            answer_options=[],
            free_text_allowed=True,
            updates_fields=["observables"],
            blocks_until_answered=["observables"]
        )

    # 4. Failure Condition
    if not card.failure_condition:
        if is_finance:
            return NextBestQuestion(
                question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
                question_type="DEFINE_FAILURE_CONDITION",
                question_text="What would make you accept that this financial intuition was wrong?",
                why_needed="Financial intuition cannot move toward action without a clear invalidation/failure condition.",
                answer_options=["price closes below a defined level", "invalidating news/event", "underperformance versus benchmark", "failure to move within the time horizon", "other"],
                free_text_allowed=True,
                updates_fields=["failure_condition"],
                blocks_until_answered=["failure_condition"]
            )
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_FAILURE_CONDITION",
            question_text="What observation or numeric result would prove your hypothesis wrong?",
            why_needed="A scientific hypothesis must be falsifiable with a defined failure condition.",
            answer_options=[],
            free_text_allowed=True,
            updates_fields=["failure_condition"],
            blocks_until_answered=["failure_condition"]
        )

    # 5. Time Horizon
    if not card.time_horizon:
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="DEFINE_TIME_HORIZON",
            question_text="What is the expected time horizon or observation period for this effect?",
            why_needed="We need a time duration or grid to run simulations or evaluate data.",
            answer_options=["1 day", "1 week", "1 month", "1 year", "transient (microseconds)", "other"],
            free_text_allowed=True,
            updates_fields=["time_horizon"],
            blocks_until_answered=["time_horizon"]
        )

    # 6. Baseline Candidates
    if not card.baseline_candidates:
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="CHOOSE_BASELINE",
            question_text="What baseline model or reference state should we compare the candidate against?",
            why_needed="To demonstrate predictive lift, we must compare results to a standard baseline or null hypothesis.",
            answer_options=["environment-only decay (exp(-gamma_env * t))", "buy-and-hold index", "random walk", "other"],
            free_text_allowed=True,
            updates_fields=["baseline_candidates"],
            blocks_until_answered=["baseline_candidates"]
        )

    # 7. Proxies
    if not card.proxies:
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="SELECT_PROXY",
            why_needed="When direct measurement is difficult, we need proxy indicators.",
            question_text="What proxy metrics could stand in for your observable?",
            answer_options=[],
            free_text_allowed=True,
            updates_fields=["proxies"],
            blocks_until_answered=["proxies"]
        )

    # 8. Benchmark / Source Support
    if not card.benchmark_candidates:
        return NextBestQuestion(
            question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
            question_type="CHOOSE_BENCHMARK",
            why_needed="Source support is required before advancing to public claims.",
            question_text="Do you have any literature source or historical benchmark reference to support this?",
            answer_options=["Yes, published literature", "Yes, backtest database", "No, this is purely exploratory"],
            free_text_allowed=True,
            updates_fields=["benchmark_candidates", "evidence_needed"],
            blocks_until_answered=["evidence_needed"]
        )

    # 9. Metric / Confirm Scope (Default fallback when all core fields filled)
    return NextBestQuestion(
        question_id=f"Q-{uuid.uuid4().hex[:8].upper()}",
        question_type="CONFIRM_SCOPE",
        question_text="All core variables defined. Would you like to confirm the scope and run the test plan?",
        why_needed="Confirming scope permits transitioning the hypothesis workspace to execution.",
        answer_options=["Yes, run benchmark", "No, revise variables"],
        free_text_allowed=False,
        updates_fields=[],
        blocks_until_answered=[]
    )
