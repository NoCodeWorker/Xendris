"""
Phygn v1.8 — Copilot: Schemas

Defines Pydantic models for the Copilot, Truth Boundary UI, Socratic Question Engine,
Hypothesis Workspace, and Model Orchestration.
"""

from __future__ import annotations

from typing import Literal, Any
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Basic Types & Enums
# ---------------------------------------------------------------------------

QuestionType = Literal[
    "CLARIFY_TERM",
    "DEFINE_VARIABLE",
    "DEFINE_OBSERVABLE",
    "SELECT_PROXY",
    "DEFINE_TIME_HORIZON",
    "CHOOSE_BASELINE",
    "CHOOSE_BENCHMARK",
    "DEFINE_FAILURE_CONDITION",
    "REQUEST_SOURCE",
    "CHOOSE_METRIC",
    "ASSESS_RISK",
    "CONFIRM_SCOPE",
]

TruthBoundaryStatus = Literal[
    "INSIDE_DREAM_BOUNDARY",
    "INSIDE_EXPLORATION_BOUNDARY",
    "INSIDE_HYPOTHESIS_BOUNDARY",
    "INSIDE_TESTABILITY_BOUNDARY",
    "INSIDE_SYNTHETIC_SUPPORT_BOUNDARY",
    "INSIDE_SOURCE_BACKED_LIMITED_BOUNDARY",
    "INSIDE_BENCHMARK_SUPPORTED_BOUNDARY",
    "OUTSIDE_CLAIM_BOUNDARY",
    "OUTSIDE_ACTION_BOUNDARY",
    "OUTSIDE_EXECUTION_BOUNDARY",
    "CROSSED_OVERCLAIM_BOUNDARY",
    "CROSSED_FALSEHOOD_BOUNDARY",
]


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class CopilotInput(BaseModel):
    """Input query to the Copilot."""
    user_message: str
    workspace_id: str | None = None
    intended_use: str = "private_exploration"
    risk_level: str = "RISK_1_INTERNAL_NOTE"


class NextBestQuestion(BaseModel):
    """The socratic question calculated by Phygn to be asked next."""
    question_id: str
    question_type: QuestionType
    question_text: str
    why_needed: str
    answer_options: list[str] = Field(default_factory=list)
    free_text_allowed: bool = True
    updates_fields: list[str] = Field(default_factory=list)
    blocks_until_answered: list[str] = Field(default_factory=list)


class TruthBoundaryEvaluation(BaseModel):
    """Result of checking the truth boundary protocol constraints."""
    status: TruthBoundaryStatus
    is_valid: bool
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    evaluation_notes: list[str] = Field(default_factory=list)


class HypothesisCardState(BaseModel):
    """The state of a single hypothesis card in the workspace."""
    raw_idea: str
    clean_hypothesis: str | None = None
    domain: str | None = None
    suspected_relation: str | None = None
    variables: list[str] = Field(default_factory=list)
    observables: list[str] = Field(default_factory=list)
    proxies: list[str] = Field(default_factory=list)
    baseline_candidates: list[str] = Field(default_factory=list)
    benchmark_candidates: list[str] = Field(default_factory=list)
    evidence_needed: list[str] = Field(default_factory=list)
    failure_condition: str | None = None
    time_horizon: str | None = None
    risk_level: str = "RISK_1_INTERNAL_NOTE"
    current_ladder_level: str = "DREAM"
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    history: list[dict[str, Any]] = Field(default_factory=list)


class HypothesisWorkspaceState(BaseModel):
    """Main state of the user's workspace."""
    workspace_id: str
    idea_history: list[str] = Field(default_factory=list)
    current_hypothesis_card: HypothesisCardState | None = None
    answered_questions: list[dict[str, Any]] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    current_ladder_level: str = "DREAM"
    truth_boundary_status: TruthBoundaryStatus = "INSIDE_DREAM_BOUNDARY"
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    next_best_question: NextBestQuestion | None = None
    audit_trail: list[dict[str, Any]] = Field(default_factory=list)


class AllowedBlockedUses(BaseModel):
    """Helper container for usage guidelines."""
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)


class ModelOrchestrationResult(BaseModel):
    """Result of cheap/open-source model orchestration."""
    raw_response: str
    parsed_structured_output: dict[str, Any] = Field(default_factory=dict)
    validation_status: str  # "VALIDATED", "MODEL_OUTPUT_UNTRUSTED", "SOURCE_CLAIM_REJECTED"
    validation_notes: list[str] = Field(default_factory=list)


class CopilotResponseContract(BaseModel):
    """The strict boundary interface contract for any Copilot response."""
    user_facing_message: str
    epistemic_mode: str
    ladder_level: str
    risk_level: str
    friction_level: str
    truth_boundary_status: str
    allowed_uses: list[str]
    blocked_uses: list[str]
    next_best_question: NextBestQuestion | None = None
    hypothesis_card: dict[str, Any] | None = None
    audit_log_event: dict[str, Any]
