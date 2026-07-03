"""
Phygn v1.6 — Epistemic Modes & Friction Gradient: Schemas

Defines all Pydantic models, enums, and type aliases used by the
epistemic modes subsystem.
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Epistemic Mode
# ---------------------------------------------------------------------------

EpistemicMode = Literal[
    "DREAM_MODE",
    "EXPLORATION_MODE",
    "HYPOTHESIS_MODE",
    "TEST_DESIGN_MODE",
    "CLAIM_MODE",
    "PUBLICATION_MODE",
    "FINANCIAL_ACTION_MODE",
    "AUTOMATED_EXECUTION_MODE",
]

# ---------------------------------------------------------------------------
# Risk Level
# ---------------------------------------------------------------------------

RiskLevel = Literal[
    "RISK_0_PRIVATE_THOUGHT",
    "RISK_1_INTERNAL_NOTE",
    "RISK_2_INTERNAL_RESEARCH",
    "RISK_3_PUBLIC_CONTENT",
    "RISK_4_CLIENT_DELIVERABLE",
    "RISK_5_FINANCIAL_RECOMMENDATION",
    "RISK_6_REAL_WORLD_ACTION",
    "RISK_7_AUTOMATED_EXECUTION",
]

# ---------------------------------------------------------------------------
# Friction Level
# ---------------------------------------------------------------------------

FrictionLevel = Literal[
    "FRICTION_0_FREE",
    "FRICTION_1_LABEL",
    "FRICTION_2_STRUCTURE",
    "FRICTION_3_REQUIRE_OBSERVABLE",
    "FRICTION_4_REQUIRE_SOURCE",
    "FRICTION_5_REQUIRE_BENCHMARK",
    "FRICTION_6_REQUIRE_RISK_ENGINE",
    "FRICTION_7_REQUIRE_HUMAN_APPROVAL",
    "FRICTION_8_BLOCK_UNLESS_FULLY_AUTHORIZED",
]

# ---------------------------------------------------------------------------
# Ladder Level
# ---------------------------------------------------------------------------

LadderLevel = Literal[
    "DREAM",
    "HYPOTHESIS_SEED",
    "FORMALIZING_HYPOTHESIS",
    "TESTABLE_HYPOTHESIS",
    "SYNTHETIC_SUPPORT",
    "SOURCE_BACKED_LIMITED",
    "BENCHMARK_SUPPORTED",
    "OPERATIONALLY_ACTIONABLE",
    "AUTOMATED_EXECUTION_ALLOWED",
]

# ---------------------------------------------------------------------------
# Gate result statuses
# ---------------------------------------------------------------------------

GateStatus = Literal[
    "IDEA_ALLOWED",
    "INTUITION_LOGGED",
    "HYPOTHESIS_SEED",
    "HYPOTHESIS_INCUBATING",
    "HYPOTHESIS_TESTABLE",
    "CLAIM_REQUIRES_EVIDENCE",
    "CLAIM_ALLOWED_LIMITED",
    "CLAIM_BLOCKED",
    "ACTION_REQUIRES_RISK_GATE",
    "ACTION_BLOCKED",
    "EXECUTION_BLOCKED",
    "EXECUTION_ALLOWED_LIMITED",
]

# Incubation statuses
IncubationStatus = Literal[
    "INCUBATING_AS_INTUITION",
    "NEEDS_OBSERVABLE",
    "NEEDS_VARIABLES",
    "NEEDS_BASELINE",
    "NEEDS_FAILURE_CONDITION",
    "READY_FOR_TESTABLE_HYPOTHESIS",
    "ARCHIVED_AS_POETIC_OR_ANALOGICAL",
]

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class ModeGateResult(BaseModel):
    """Result of evaluating idea/claim/action permission for a given mode."""
    mode: EpistemicMode
    risk_level: RiskLevel
    friction_level: FrictionLevel
    idea_permission: GateStatus
    hypothesis_permission: GateStatus
    claim_permission: GateStatus
    action_permission: GateStatus
    execution_permission: GateStatus
    allowed_uses: list[str] = Field(default_factory=list)
    blocked_uses: list[str] = Field(default_factory=list)
    required_next_steps: list[str] = Field(default_factory=list)


class HypothesisSeed(BaseModel):
    """A raw hypothesis seed, potentially very incomplete."""
    seed_id: str
    title: str
    intuition: str
    domain: str
    possible_observable: str | None = None
    analogy: str | None = None
    current_level: LadderLevel = "DREAM"
    risk_level: RiskLevel = "RISK_1_INTERNAL_NOTE"
    known_unknowns: list[str] = Field(default_factory=list)
    next_formalization_steps: list[str] = Field(default_factory=list)
    forbidden_claims: list[str] = Field(default_factory=list)


class IncubationResult(BaseModel):
    """Result of processing a HypothesisSeed through incubation."""
    seed_id: str
    current_level: LadderLevel
    incubation_status: IncubationStatus
    allowed_use: list[str] = Field(default_factory=list)
    blocked_use: list[str] = Field(default_factory=list)
    next_formalization_steps: list[str] = Field(default_factory=list)
    required_evidence_for_next_level: list[str] = Field(default_factory=list)
    friction_level: FrictionLevel = "FRICTION_1_LABEL"


class LadderClassification(BaseModel):
    """Output of classify_ladder_level()."""
    ladder_level: LadderLevel
    level_index: int  # 0..8
    idea_allowed: bool
    claim_allowed: bool
    action_allowed: bool
    execution_allowed: bool
    status: GateStatus
    missing_for_next_level: list[str] = Field(default_factory=list)


class FrictionDecision(BaseModel):
    """Output of evaluate_friction()."""
    risk_level: RiskLevel
    mode: EpistemicMode
    friction_level: FrictionLevel
    is_blocked: bool
    requires_human_approval: bool
    gate_notes: list[str] = Field(default_factory=list)


class FinancialActionGateResult(BaseModel):
    """Result of the financial action gate."""
    asset: str | None = None
    action_status: GateStatus
    intuition_status: GateStatus
    missing_fields: list[str] = Field(default_factory=list)
    gate_notes: list[str] = Field(default_factory=list)
