"""
Phygn v1.8 — Copilot Subsystem

DEPRECATED (REFACTOR_PLAN.md — Fase 4):
    phyng.copilot is a DELETE_CANDIDATE.
    Console-based prototytpes are superseded by the unified Xendris UI (/x).
    This module will be removed in a future cleanup pass.
"""
import warnings
warnings.warn(
    "phyng.copilot is deprecated and scheduled for removal. "
    "Use the main Xendris web interface.",
    DeprecationWarning,
    stacklevel=2,
)

from phyng.copilot.schemas import (
    CopilotInput,
    NextBestQuestion,
    TruthBoundaryEvaluation,
    CopilotResponseContract,
    HypothesisWorkspaceState,
    HypothesisCardState,
    AllowedBlockedUses,
    ModelOrchestrationResult,
)
from phyng.copilot.question_engine import generate_next_best_question
from phyng.copilot.truth_boundary import evaluate_truth_boundary
from phyng.copilot.workspace import create_or_update_workspace
from phyng.copilot.response_contract import create_copilot_response
from phyng.copilot.orchestration import (
    compose_copilot_prompt_for_model,
    validate_model_structured_output,
    fallback_to_rule_based_question,
    orchestrate_model_assisted_response,
)
from phyng.copilot.report import write_copilot_reports

__all__ = [
    "CopilotInput",
    "NextBestQuestion",
    "TruthBoundaryEvaluation",
    "CopilotResponseContract",
    "HypothesisWorkspaceState",
    "HypothesisCardState",
    "AllowedBlockedUses",
    "ModelOrchestrationResult",
    "generate_next_best_question",
    "evaluate_truth_boundary",
    "create_or_update_workspace",
    "create_copilot_response",
    "compose_copilot_prompt_for_model",
    "validate_model_structured_output",
    "fallback_to_rule_based_question",
    "orchestrate_model_assisted_response",
    "write_copilot_reports",
]
