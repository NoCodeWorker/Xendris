"""RouteRequest and RouteDecision data structures for the Multi-Model Selector."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel


@dataclass(frozen=True)
class RouteRequest:
    """Immutable request specification detailing constraints for the routing decision."""

    request_id: str
    user_intent: str
    local_context: LocalContext
    epistemic_sector: EpistemicSector
    claim_type: ClaimType
    risk_level: RiskLevel
    estimated_input_tokens: int
    estimated_output_tokens: int
    requires_tools: bool = False
    requires_code: bool = False
    requires_json: bool = False
    requires_long_context: bool = False
    prefer_low_cost: bool = False
    prefer_low_latency: bool = False
    require_strict_gate: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RouteDecision:
    """Immutable routing decision output detailing model selection and gating rules."""

    decision: str  # SELECT, SELECT_WITH_LIMITATIONS, REQUIRE_STRONGER_MODEL, REQUIRE_HUMAN_REVIEW, NO_SAFE_MODEL_AVAILABLE, BLOCK
    selected_model_id: str | None
    selected_provider: str | None
    reason: str
    required_gates: tuple[str, ...]
    rejected_models: tuple[str, ...]
    estimated_cost: float
    estimated_latency_ms: int
    limitations: tuple[str, ...]
    fallback_model_id: str | None = None
    human_review_required: bool = False
    audit_tags: tuple[str, ...] = ()
