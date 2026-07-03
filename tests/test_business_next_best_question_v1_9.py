"""
Tests v1.9 — Business Next Best Question
"""

import pytest
from phyng.business_validation.schemas import BusinessHypothesisCanvas
from phyng.business_validation.canvas import generate_next_best_business_question


def test_next_question_prioritizes_customer_first():
    # 1. No customer segment
    canvas = BusinessHypothesisCanvas(idea_id="I-001", business_idea="Idea text")
    q = generate_next_best_business_question(canvas)
    assert q.updates_fields == ["target_customer"]

    # 2. Has customer segment but no problem
    canvas.target_customer = "Startups"
    q_prob = generate_next_best_business_question(canvas)
    assert q_prob.updates_fields == ["problem"]

    # 3. Has customer segment and problem but no current alternative
    canvas.problem = "Diligence is slow"
    q_alt = generate_next_best_business_question(canvas)
    assert q_alt.updates_fields == ["current_alternative"]
