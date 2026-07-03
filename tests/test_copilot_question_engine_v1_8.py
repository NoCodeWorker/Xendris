"""
Tests v1.8 — Socratic Question Engine
"""

import pytest
from phyng.copilot.question_engine import generate_next_best_question
from phyng.copilot.schemas import HypothesisCardState


def test_next_best_question_for_raw_business_idea():
    text = "I think companies will pay for claim audits before raising investment."
    q = generate_next_best_question(text, None, "DREAM_MODE", "RISK_1_INTERNAL_NOTE")
    assert q.question_type == "CLARIFY_TERM"
    assert "pay first" in q.question_text
    assert len(q.answer_options) > 0


def test_next_best_question_for_scientific_hypothesis():
    text = "Frontera C may modulate visibility loss at boundary scale."
    # Initialize card with variables already set so it moves to observable
    card = HypothesisCardState(
        raw_idea=text,
        suspected_relation="Frontera C modulates visibility loss",
        variables=["mass", "B"],
    )
    q = generate_next_best_question(text, card, "HYPOTHESIS_MODE", "RISK_2_INTERNAL_RESEARCH")
    assert q.question_type == "DEFINE_OBSERVABLE"
    assert "observable" in q.question_text.lower() or "change" in q.question_text.lower()
    assert "visibility decay curve" in q.answer_options


def test_question_engine_asks_only_one_question():
    text = "General intuition"
    q = generate_next_best_question(text, None, "DREAM_MODE", "RISK_1_INTERNAL_NOTE")
    # Must be a single NextBestQuestion instance (not a list of questions)
    assert q is not None
    assert isinstance(q.question_text, str)


def test_question_engine_offers_options():
    text = "BTC price will rise."
    card = HypothesisCardState(
        raw_idea=text,
        suspected_relation="correlation between sentiment and price",
        variables=["sentiment", "price"],
        observables=["price return"],
    )
    q = generate_next_best_question(text, card, "FINANCIAL_ACTION_MODE", "RISK_5_FINANCIAL_RECOMMENDATION")
    assert q.question_type == "DEFINE_FAILURE_CONDITION"
    assert len(q.answer_options) > 0
    assert any("price closes below" in opt for opt in q.answer_options)
