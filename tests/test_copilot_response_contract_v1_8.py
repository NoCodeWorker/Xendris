"""
Tests v1.8 — Copilot Response Contract
"""

import pytest
from phyng.copilot.response_contract import create_copilot_response
from phyng.copilot.schemas import NextBestQuestion, HypothesisCardState


def test_response_contract_contains_required_fields():
    q = NextBestQuestion(
        question_id="Q-TEST",
        question_type="CLARIFY_TERM",
        question_text="What do you mean?",
        why_needed="For clarification."
    )
    card = HypothesisCardState(
        raw_idea="Test idea",
    )

    resp = create_copilot_response(
        user_facing_message="Hello",
        epistemic_mode="DREAM_MODE",
        ladder_level="DREAM",
        risk_level="RISK_0_PRIVATE_THOUGHT",
        friction_level="FRICTION_0_FREE",
        truth_boundary_status="INSIDE_DREAM_BOUNDARY",
        allowed_uses=["Refinement"],
        blocked_uses=["Action"],
        next_best_question=q,
        hypothesis_card=card,
        additional_audit_notes=["Created test contract."]
    )

    # Verify schema fields
    assert resp.user_facing_message == "Hello"
    assert resp.epistemic_mode == "DREAM_MODE"
    assert resp.ladder_level == "DREAM"
    assert resp.risk_level == "RISK_0_PRIVATE_THOUGHT"
    assert resp.friction_level == "FRICTION_0_FREE"
    assert resp.truth_boundary_status == "INSIDE_DREAM_BOUNDARY"
    assert resp.allowed_uses == ["Refinement"]
    assert resp.blocked_uses == ["Action"]
    assert resp.next_best_question.question_id == "Q-TEST" if resp.next_best_question else False
    assert resp.hypothesis_card is not None
    assert resp.hypothesis_card["raw_idea"] == "Test idea"
    assert resp.audit_log_event["epistemic_mode"] == "DREAM_MODE"
