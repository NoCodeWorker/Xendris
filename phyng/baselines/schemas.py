"""
Phygn v0.8 — Baseline Schemas

Defines data models for the Source-Backed Baseline subsystem.
These schemas track how well-supported a baseline model is by evidence.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class BaselineSourceRequirement(BaseModel):
    """A requirement for a source to support the baseline model."""

    requirement_id: str
    topic: str
    baseline_role: str
    reason: str
    required_for: list[str] = Field(default_factory=list)
    linked_model_ids: list[str] = Field(default_factory=list)
    linked_claim_ids: list[str] = Field(default_factory=list)
    required_trust_level: str = "HIGH"
    suggested_queries: list[str] = Field(default_factory=list)
    # AWAITING_SOURCE_INGESTION | SOURCED | UNAVAILABLE
    status: str = "AWAITING_SOURCE_INGESTION"


class VisibilityDecayBaselineSpec(BaseModel):
    """
    Specification for the exponential visibility-decay baseline model:

        V_base(t) = exp(-Gamma_env * t)

    Classified by evidence level.
    """

    model_id: str
    formula: str = "V_base(t) = exp(-Gamma_env * t)"
    observable: str = "visibility_loss"
    gamma_parameter_name: str = "Gamma_env"
    # None means parameter is not sourced yet (PARAMETER_TOY)
    gamma_value: float | None = None
    gamma_units: str = "s^{-1}"
    assumptions: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)

    # TOY_INTERNAL | BACKGROUND_SUPPORTED | SOURCE_BACKED_LIMITED |
    # SOURCE_BACKED_READY | CONTRADICTED
    support_status: str = "TOY_INTERNAL"

    allowed_uses: list[str] = Field(
        default_factory=lambda: [
            "baseline comparison",
            "toy-to-source-backed transition",
            "visibility/coherence decay reference",
            "limited model comparison",
        ]
    )
    forbidden_uses: list[str] = Field(
        default_factory=lambda: [
            "universal decoherence model",
            "proof of physical mechanism",
            "validation of boundary candidate",
            "experimental prediction without data",
        ]
    )

    # PARAMETER_TOY | PARAMETER_SOURCE_BACKED | PARAMETER_FITTED | PARAMETER_EXPERIMENTAL
    parameter_status: str = "PARAMETER_TOY"


class BaselineReadinessResult(BaseModel):
    """Result of classifying baseline readiness for a visibility-decay model."""

    model_id: str
    support_status: str
    parameter_status: str
    can_be_used_as_baseline: bool
    # 3=TOY, 4=SOURCE_BACKED_LIMITED, 5=SOURCE_BACKED_READY
    max_claim_level: int
    missing_requirements: list[str] = Field(default_factory=list)
    allowed_claims: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


class BaselineSourceSupport(BaseModel):
    """Tracks how a source supports (or contradicts) the baseline."""

    source_id: str
    support_level: str  # FORMULA_SUPPORT | PARAMETER_SUPPORT | OBSERVABLE_SUPPORT | CONTEXT_SUPPORT | CONTRADICTS
    trust_level: str  # PRIMARY | HIGH | MEDIUM | LOW | BACKGROUND
    note: str = ""


class Campaign002BaselineUpgradeResult(BaseModel):
    """Result of upgrading the CAMPAIGN-002 baseline from TOY_INTERNAL."""

    campaign_id: str = "CAMPAIGN-002"
    baseline_before: str = "TOY_INTERNAL"
    baseline_after: str
    baseline_readiness: dict = Field(default_factory=dict)
    source_requirements: list[str] = Field(default_factory=list)
    source_support_matrix_path: str | None = None
    updated_max_claim_level: int = 3
    allowed_new_claims: list[str] = Field(default_factory=list)
    still_blocked_claims: list[str] = Field(
        default_factory=lambda: [
            "Phygn predicts gravitational decoherence.",
            "Boundary C causes decoherence.",
            "SyntheticGain proves physical gain.",
            "The source-backed baseline validates the boundary-aware candidate.",
        ]
    )
    next_required_steps: list[str] = Field(default_factory=list)
