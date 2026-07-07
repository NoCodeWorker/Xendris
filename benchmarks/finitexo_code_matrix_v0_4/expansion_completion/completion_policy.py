"""Deterministic completion policy for v0.4.2."""

from __future__ import annotations

from typing import Any

from .completion_types import CompletionCondition, CompletionDecision


def evaluate_pool_completion(
    *,
    current_frozen_task_count: int,
    target_frozen_task_count: int,
    additional_ready_candidates_required: int,
    ready_for_future_freeze: int,
    ready_with_human_review: int,
    frozen_hashes_unchanged: bool,
    providers_executed: bool,
) -> dict[str, Any]:
    strict_ready = ready_for_future_freeze >= additional_ready_candidates_required
    mixed_conservative = ready_for_future_freeze >= 6 and ready_with_human_review >= 2
    boundary_ok = (
        current_frozen_task_count == 2
        and target_frozen_task_count >= 10
        and additional_ready_candidates_required == 8
        and frozen_hashes_unchanged
        and not providers_executed
    )
    ready = boundary_ok and (strict_ready or mixed_conservative)
    if strict_ready and boundary_ok:
        condition = CompletionCondition.STRICT_READY
    elif mixed_conservative and boundary_ok:
        condition = CompletionCondition.MIXED_CONSERVATIVE
    else:
        condition = CompletionCondition.INSUFFICIENT
    return {
        "strict_ready_condition_passed": strict_ready and boundary_ok,
        "mixed_conservative_condition_passed": mixed_conservative and boundary_ok,
        "completion_condition": condition.value,
        "future_explicit_freeze_recommended": ready,
        "final_decision": (
            CompletionDecision.EXPANSION_POOL_COMPLETED_READY_FOR_EXPLICIT_FREEZE.value
            if ready
            else CompletionDecision.EXPANSION_POOL_STILL_INSUFFICIENT_NO_FREEZE.value
        ),
    }
