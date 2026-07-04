"""RuntimeRequest definition composing RouteRequest."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from xendris.core.local.context import LocalContext
from xendris.core.sectors.sector import EpistemicSector
from xendris.core.trust.types import ClaimType, RiskLevel
from xendris.core.router.route_request import RouteRequest


@dataclass(frozen=True)
class RuntimeRequest:
    """Immutable runtime request representing the user query and its safety constraints."""

    request_id: str
    user_input: str
    user_intent: str
    local_context: LocalContext
    epistemic_sector: EpistemicSector
    claim_type: ClaimType
    risk_level: RiskLevel
    estimated_input_tokens: int = 1000
    estimated_output_tokens: int = 1000
    requires_tools: bool = False
    requires_code: bool = False
    requires_json: bool = False
    requires_long_context: bool = False
    prefer_low_cost: bool = False
    prefer_low_latency: bool = False
    require_strict_gate: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_route_request(self) -> RouteRequest:
        """Convert the runtime request to a RouteRequest for the MultiModelSelector."""
        return RouteRequest(
            request_id=self.request_id,
            user_intent=self.user_intent,
            local_context=self.local_context,
            epistemic_sector=self.epistemic_sector,
            claim_type=self.claim_type,
            risk_level=self.risk_level,
            estimated_input_tokens=self.estimated_input_tokens,
            estimated_output_tokens=self.estimated_output_tokens,
            requires_tools=self.requires_tools,
            requires_code=self.requires_code,
            requires_json=self.requires_json,
            requires_long_context=self.requires_long_context,
            prefer_low_cost=self.prefer_low_cost,
            prefer_low_latency=self.prefer_low_latency,
            require_strict_gate=self.require_strict_gate,
            metadata=self.metadata,
        )
