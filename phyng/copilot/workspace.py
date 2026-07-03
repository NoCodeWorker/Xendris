"""
Phygn v1.8 — Hypothesis Workspace State

Manages the workspace life cycle, including create_or_update_workspace.
Ensures state transitions are correctly audited and fields are updated after questions are answered.
"""

from __future__ import annotations

import datetime
from typing import Any
from phyng.copilot.schemas import (
    HypothesisWorkspaceState,
    HypothesisCardState,
    NextBestQuestion,
)
from phyng.copilot.question_engine import generate_next_best_question
from phyng.copilot.truth_boundary import evaluate_truth_boundary
from phyng.epistemic_modes.ladder import classify_ladder_level


def create_or_update_workspace(
    workspace_id: str,
    new_user_message: str | None = None,
    current_state: HypothesisWorkspaceState | None = None,
    answer: str | None = None,
    answered_question_type: str | None = None,
) -> HypothesisWorkspaceState:
    """
    Initialize or transition the state of a HypothesisWorkspaceState.
    """
    # 1. Initialize state if None
    if current_state is None:
        raw = new_user_message or "Empty workspace initialized."
        card = HypothesisCardState(
            raw_idea=raw,
            clean_hypothesis=f"Initial seed: {raw}",
            current_ladder_level="DREAM",
        )
        current_state = HypothesisWorkspaceState(
            workspace_id=workspace_id,
            idea_history=[raw],
            current_hypothesis_card=card,
            answered_questions=[],
            missing_fields=["variables", "observables", "failure_condition", "time_horizon", "baseline_candidates"],
            current_ladder_level="DREAM",
            truth_boundary_status="INSIDE_DREAM_BOUNDARY",
            allowed_uses=["Private exploration"],
            blocked_uses=["Public claims", "Automated execution"],
            next_best_question=None,
            audit_trail=[{"event": "workspace_created", "timestamp": str(datetime.datetime.now(datetime.timezone.utc))}]
        )

    card = current_state.current_hypothesis_card
    assert card is not None

    # 2. Process user answer if provided
    if answer is not None and answered_question_type is not None:
        current_state.answered_questions.append({
            "question_type": answered_question_type,
            "answer": answer,
            "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
        })

        # Map answer to card fields
        if answered_question_type == "CLARIFY_TERM":
            card.suspected_relation = answer
            if "suspected_relation" in current_state.missing_fields:
                current_state.missing_fields.remove("suspected_relation")
        elif answered_question_type == "DEFINE_VARIABLE":
            card.variables = [v.strip() for v in answer.split(",") if v.strip()]
            if "variables" in current_state.missing_fields:
                current_state.missing_fields.remove("variables")
        elif answered_question_type == "DEFINE_OBSERVABLE":
            card.observables = [o.strip() for o in answer.split(",") if o.strip()]
            if "observables" in current_state.missing_fields:
                current_state.missing_fields.remove("observables")
        elif answered_question_type == "DEFINE_FAILURE_CONDITION":
            card.failure_condition = answer
            if "failure_condition" in current_state.missing_fields:
                current_state.missing_fields.remove("failure_condition")
        elif answered_question_type == "DEFINE_TIME_HORIZON":
            card.time_horizon = answer
            if "time_horizon" in current_state.missing_fields:
                current_state.missing_fields.remove("time_horizon")
        elif answered_question_type == "CHOOSE_BASELINE":
            card.baseline_candidates = [b.strip() for b in answer.split(",") if b.strip()]
            if "baseline_candidates" in current_state.missing_fields:
                current_state.missing_fields.remove("baseline_candidates")

        card.history.append({
            "action": f"answered_{answered_question_type}",
            "value": answer,
            "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
        })
        current_state.audit_trail.append({
            "event": "field_updated",
            "field": answered_question_type,
            "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
        })

    # 3. Handle new message if provided (without direct answer)
    if new_user_message is not None and answer is None:
        current_state.idea_history.append(new_user_message)
        card.raw_idea = new_user_message
        current_state.audit_trail.append({
            "event": "new_idea_message_received",
            "timestamp": str(datetime.datetime.now(datetime.timezone.utc))
        })

    # 4. Calculate ladder level & truth boundary status
    evidence = []
    if card.suspected_relation:
        evidence.extend(["candidate_phenomenon", "domain", "uncertainty_acknowledged"])
    if card.variables:
        evidence.extend(["variables", "scope_boundary"])
    if card.observables:
        evidence.extend(["possible_observable", "rough_mechanism"])
    if card.failure_condition and card.baseline_candidates and card.time_horizon:
        evidence.extend(["observable", "baseline", "candidate_model", "failure_condition", "metric", "detectability_threshold"])

    ladder_class = classify_ladder_level(card.raw_idea, "explore", evidence)

    current_state.current_ladder_level = ladder_class.ladder_level
    card.current_ladder_level = ladder_class.ladder_level

    # Check truth boundary status
    tb_eval = evaluate_truth_boundary(
        ladder_level=ladder_class.ladder_level,
        mode="HYPOTHESIS_MODE",
        risk_level=card.risk_level,
        has_sources=len(card.benchmark_candidates) > 0,
        has_benchmark=len(card.benchmark_candidates) > 0,
    )

    current_state.truth_boundary_status = tb_eval.status
    current_state.allowed_uses = tb_eval.allowed_uses
    current_state.blocked_uses = tb_eval.blocked_uses
    card.allowed_uses = tb_eval.allowed_uses
    card.blocked_uses = tb_eval.blocked_uses

    # 5. Generate next best question
    current_state.next_best_question = generate_next_best_question(
        input_text=card.raw_idea,
        hypothesis_card=card,
        mode="HYPOTHESIS_MODE",
        risk_level=card.risk_level,
    )

    return current_state
