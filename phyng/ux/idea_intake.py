"""
Phygn v1.7 — UX: Idea Intake & Hypothesis Builder Schemas + Core Logic

Process flow:
    intuition → IdeaIntake → HypothesisSeedCard (via process_idea_intake)

The Math Translator produces SUGGESTED_NOT_VALIDATED candidate structures
from natural language. No LLM call is made here — the translation is
deterministic/heuristic. LLMs may propose; Phygn verifies.
"""

from __future__ import annotations

import uuid
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# IdeaIntake — user entry point
# ---------------------------------------------------------------------------

class IdeaIntake(BaseModel):
    """Raw intuition as entered by the user. No mathematical model required."""
    idea_id: str = Field(default_factory=lambda: f"IDEA-{uuid.uuid4().hex[:8].upper()}")
    raw_intuition: str
    domain: str | None = None
    suspected_relation: str | None = None
    possible_cause: str | None = None
    possible_effect: str | None = None
    context: str | None = None
    user_confidence: float | None = None  # 0.0–1.0
    intended_use: str = "private_exploration"
    risk_level: str = "RISK_1_INTERNAL_NOTE"


# ---------------------------------------------------------------------------
# HypothesisSeedCard — output of intake processing
# ---------------------------------------------------------------------------

class HypothesisSeedCard(BaseModel):
    """Structured hypothesis seed generated from a raw IdeaIntake."""
    seed_id: str = Field(default_factory=lambda: f"SEED-{uuid.uuid4().hex[:8].upper()}")
    idea_id: str
    title: str
    raw_intuition: str
    cleaned_hypothesis: str
    current_ladder_level: str = "HYPOTHESIS_SEED"
    ux_status: str = "HYPOTHESIS_SEED_CREATED"
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    candidate_variables: list[str] = Field(default_factory=list)
    candidate_observables: list[str] = Field(default_factory=list)
    candidate_proxies: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    next_best_questions: list[str] = Field(default_factory=list)
    minimum_test_plan: list[str] = Field(default_factory=list)
    proposal_label: str = "SUGGESTED_NOT_VALIDATED"


# ---------------------------------------------------------------------------
# MathTranslatorOutput — structured proposal from translate_intuition_to_testable_structure
# ---------------------------------------------------------------------------

class MathTranslatorOutput(BaseModel):
    """
    Candidate testable structure derived from natural language.
    All fields are SUGGESTED_NOT_VALIDATED — they must be reviewed by the user.
    """
    idea_id: str
    label: str = "SUGGESTED_NOT_VALIDATED"
    possible_x_variables: list[str] = Field(default_factory=list)
    possible_y_observables: list[str] = Field(default_factory=list)
    proxy_candidates: list[str] = Field(default_factory=list)
    baseline_candidates: list[str] = Field(default_factory=list)
    failure_condition_candidates: list[str] = Field(default_factory=list)
    test_plan_candidates: list[str] = Field(default_factory=list)
    candidate_hypothesis_text: str = ""
