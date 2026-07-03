"""Closed-loop feedback for LOG_BOUNDARY synthetic execution."""

from __future__ import annotations

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.synthetic_benchmark_design.schemas import (
    LogBoundaryExecutionResult,
    LogBoundaryLoopFeedbackResult,
)


def generate_log_boundary_loop_feedback(execution_result: LogBoundaryExecutionResult) -> LogBoundaryLoopFeedbackResult:
    best = execution_result.sweep_result.best_point
    loop_input = CandidateLoopInput(
        loop_id="LOG-BOUNDARY-v2_5",
        input_type="SYNTHETIC_BENCHMARK_RESULT",
        domain="physical_candidate",
        candidate_id=execution_result.candidate_id,
        candidate_family=execution_result.candidate_family,
        previous_status="SYNTHETIC_BENCHMARK_DESIGNED",
        result_status=execution_result.status,
        payload={
            "best_max_abs_delta": best.max_abs_delta if best else None,
            "failure_conditions": execution_result.failure_conditions,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposals = list(loop_result.update_proposals)
    if not proposals:
        proposals.append(_proposal_for_execution(execution_result))

    next_actions = list(execution_result.next_actions)
    for action in loop_result.next_actions:
        if action not in next_actions:
            next_actions.append(action)

    human_review = execution_result.status in {
        "LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS",
        "LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING",
        "LOG_BOUNDARY_EXECUTION_BLOCKED",
    }

    return LogBoundaryLoopFeedbackResult(
        loop_event_id=loop_result.audit_event_id,
        candidate_id=execution_result.candidate_id,
        result_status=execution_result.status,
        canonical_status=execution_result.canonical_status,
        candidate_loop_input=loop_input,
        candidate_loop_result=loop_result,
        update_proposals=proposals,
        blocked_updates=[
            "claim gate relaxation",
            "source requirement reduction",
            "benchmark requirement reduction",
            "experimental evidence requirement reduction",
            "canonical permission semantic changes",
        ],
        shadow_mode_required=False,
        human_review_required=human_review,
        next_actions=next_actions,
        rollbackable_config_changes=["candidate priority ordering", "source search priority", "benchmark pressure routing"],
        blocked_claims=execution_result.blocked_claims,
    )


def _proposal_for_execution(execution_result: LogBoundaryExecutionResult) -> CandidateUpdateProposal:
    if execution_result.status == "LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA":
        proposal_type = "SOURCE_AND_BENCHMARK_PRESSURE_UPDATE"
        description = "Increase source-search and benchmark-pressure priority while keeping physical claims blocked."
        proposed_change = {"source_search_priority": "increase", "benchmark_pressure": "increase"}
    elif execution_result.status == "LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA":
        proposal_type = "CANDIDATE_PRIORITY_DOWNRANK"
        description = "Record synthetic negative result and down-rank LOG_BOUNDARY until new justification appears."
        proposed_change = {"candidate_priority": "downrank", "result_record": "synthetic_negative"}
    else:
        proposal_type = "PARAMETER_JUSTIFICATION_REQUIRED"
        description = "Block promotion until parameter choices are pre-registered and source-backed."
        proposed_change = {"promotion": "blocked", "parameter_review": "required"}

    return CandidateUpdateProposal(
        proposal_id=f"LOG-BOUNDARY-v2_5-{proposal_type}",
        proposal_type=proposal_type,
        candidate_id=execution_result.candidate_id,
        candidate_family=execution_result.candidate_family,
        description=description,
        proposed_change=proposed_change,
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=False,
        forbidden_actions=["authorize physical claim", "validate Frontera C", "relax source requirement"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
