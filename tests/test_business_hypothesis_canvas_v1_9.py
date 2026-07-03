"""
Tests v1.9 — Business Hypothesis Canvas & Claim Decomposition
"""

import pytest
from phyng.business_validation.schemas import BusinessIdeaInput
from phyng.business_validation.decomposition import decompose_business_idea


def test_business_idea_decomposes_into_hypotheses():
    idea = BusinessIdeaInput(
        idea_id="TEST-BI-001",
        raw_idea="Signphy AI Deeptech claim auditing.",
        target_customer="VCs",
        problem="Diligence on deeptech is hard.",
        urgency="high",
        wtp_assumption="Paid pilot",
        channel="LinkedIn"
    )
    canvas = decompose_business_idea(idea)
    assert canvas.idea_id == idea.idea_id
    assert len(canvas.hypotheses) == 4
    assert any(h.hypothesis_type == "CUSTOMER" for h in canvas.hypotheses)
    assert any(h.hypothesis_type == "PROBLEM" for h in canvas.hypotheses)
    assert any(h.hypothesis_type == "WILLINGNESS_TO_PAY" for h in canvas.hypotheses)
    assert any(h.hypothesis_type == "CHANNEL" for h in canvas.hypotheses)
    assert canvas.validation_status == "BUSINESS_HYPOTHESIS_SEED"


def test_unknown_customer_blocks_validation():
    # If target_customer is missing, status should be BUSINESS_BLOCKED_NO_CUSTOMER
    idea = BusinessIdeaInput(
        idea_id="TEST-BI-002",
        raw_idea="AI service.",
        target_customer=None, # Missing customer Segment
        problem="Diligence is hard."
    )
    canvas = decompose_business_idea(idea)
    assert canvas.validation_status == "BUSINESS_BLOCKED_NO_CUSTOMER"
