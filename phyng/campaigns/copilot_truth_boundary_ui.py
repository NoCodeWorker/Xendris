"""
Phygn v1.8 — Copilot Truth-Boundary UI Campaign Orchestrator
"""

from __future__ import annotations

import json
from pathlib import Path
from phyng.copilot.schemas import (
    CopilotInput,
    HypothesisCardState,
    HypothesisWorkspaceState,
)
from phyng.copilot.workspace import create_or_update_workspace
from phyng.copilot.question_engine import generate_next_best_question
from phyng.copilot.truth_boundary import evaluate_truth_boundary
from phyng.copilot.response_contract import create_copilot_response
from phyng.copilot.orchestration import orchestrate_model_assisted_response
from phyng.copilot.report import write_copilot_reports


def run_copilot_truth_boundary_campaign(
    reports_dir: str | Path = "reports",
) -> dict:
    """
    Run the full v1.8 campaign demo.
    """
    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)

    # 1. Initialize workspace with raw idea
    raw_idea = "BTC price will rise if social sentiment spikes."
    workspace_id = "WORK-COPILOT-001"
    workspace = create_or_update_workspace(
        workspace_id=workspace_id,
        new_user_message=raw_idea,
    )

    # 2. Simulate answer to DEFINE_VARIABLE (or similar) to show workspace transition
    workspace = create_or_update_workspace(
        workspace_id=workspace_id,
        current_state=workspace,
        answer="independent: social mentions count, dependent: BTC-USD 1-day return",
        answered_question_type="DEFINE_VARIABLE"
    )

    card = workspace.current_hypothesis_card
    assert card is not None

    # 3. Socratic Question Engine next question
    next_q = generate_next_best_question(
        input_text=raw_idea,
        hypothesis_card=card,
        mode="HYPOTHESIS_MODE",
        risk_level=card.risk_level,
    )

    # 4. Truth Boundary Evaluation
    tb_eval = evaluate_truth_boundary(
        ladder_level=card.current_ladder_level,
        mode="HYPOTHESIS_MODE",
        risk_level=card.risk_level,
        has_sources=False,
        has_benchmark=False,
    )

    # 5. Model Orchestration
    # Simulate a structured output from a cheap model that includes a proposal
    model_proposal = {
        "clean_hypothesis": "If social mentions of 'BTC' spike by 20%, BTC-USD return over the next 24 hours is positive.",
        "claims_source_support": False,
        "current_ladder_level": "HYPOTHESIS_SEED"
    }
    orch_result = orchestrate_model_assisted_response(
        user_message=raw_idea,
        hypothesis_card=card,
        mode="HYPOTHESIS_MODE",
        risk_level=card.risk_level,
        model_raw_response=json.dumps(model_proposal),
        has_sources=False
    )

    # 6. Response Contract
    response = create_copilot_response(
        user_facing_message="We have captured your variables. Now, let's define the observable.",
        epistemic_mode="HYPOTHESIS_MODE",
        ladder_level=card.current_ladder_level,
        risk_level=card.risk_level,
        friction_level="FRICTION_2_STRUCTURE",
        truth_boundary_status=tb_eval.status,
        allowed_uses=tb_eval.allowed_uses,
        blocked_uses=tb_eval.blocked_uses,
        next_best_question=next_q,
        hypothesis_card=card,
        additional_audit_notes=["Successfully processed DEFINE_VARIABLE answer."]
    )

    # 7. Write reports
    report_paths = write_copilot_reports(
        reports_dir=reports_path,
        response_contract=response,
        workspace_state=workspace,
        next_question=next_q,
        orchestration_result=orch_result,
    )

    return {
        "workspace": workspace,
        "next_question": next_q,
        "tb_eval": tb_eval,
        "orch_result": orch_result,
        "response_contract": response,
        "report_paths": report_paths,
    }
