"""
Tests v1.8 — Hypothesis Workspace
"""

import pytest
from phyng.copilot.workspace import create_or_update_workspace


def test_workspace_updates_after_answer():
    workspace_id = "WORK-TEST-001"

    # 1. Initialize
    state = create_or_update_workspace(
        workspace_id=workspace_id,
        new_user_message="Initial raw intuition text."
    )
    assert state.workspace_id == workspace_id
    assert state.current_ladder_level == "DREAM"
    assert "variables" in state.missing_fields

    # 2. Answer a question
    state_after = create_or_update_workspace(
        workspace_id=workspace_id,
        current_state=state,
        answer="independent: alpha, dependent: visibility_loss",
        answered_question_type="DEFINE_VARIABLE"
    )

    # Variables should be updated
    assert state_after.current_hypothesis_card is not None
    assert "independent: alpha" in state_after.current_hypothesis_card.variables[0]
    assert len(state_after.answered_questions) == 1
    assert state_after.answered_questions[0]["question_type"] == "DEFINE_VARIABLE"
    assert len(state_after.audit_trail) > 1
