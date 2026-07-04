"""Deterministic ModelCapabilityProfile and ModelRegistry definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from xendris.core.trust.types import RiskLevel


@dataclass(frozen=True)
class ModelCapabilityProfile:
    """Static capability profile representing a model's operational specifications."""

    model_id: str
    provider: str
    supported_contexts: tuple[str, ...]
    supported_sectors: tuple[str, ...]
    max_risk_level: RiskLevel
    cost_per_1k_input_tokens: float
    cost_per_1k_output_tokens: float
    expected_latency_ms: int
    supports_tools: bool
    supports_code: bool
    supports_json: bool
    supports_long_context: bool
    required_gates: tuple[str, ...]
    fingerprint_ref: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


class ModelRegistry:
    """Deterministic in-memory registry of available ModelCapabilityProfiles."""

    def __init__(self) -> None:
        self._models: dict[str, ModelCapabilityProfile] = {}

    def register_model(self, profile: ModelCapabilityProfile) -> None:
        """Register a model capability profile."""
        self._models[profile.model_id] = profile

    def get_model(self, model_id: str) -> ModelCapabilityProfile:
        """Retrieve a specific model profile by ID."""
        if model_id not in self._models:
            raise KeyError(f"Model {model_id} not registered.")
        return self._models[model_id]

    def list_models(self) -> list[ModelCapabilityProfile]:
        """List all registered model capability profiles."""
        return list(self._models.values())

    def filter_by_context(self, context: str) -> list[ModelCapabilityProfile]:
        """Filter models that explicitly support the given local context."""
        context_str = context.name if hasattr(context, "name") else context
        context_str = context_str.upper()
        return [
            m for m in self._models.values()
            if any(ctx.upper() == context_str for ctx in m.supported_contexts)
        ]

    def filter_by_sector(self, sector: str) -> list[ModelCapabilityProfile]:
        """Filter models that explicitly support the given epistemic sector."""
        sector_str = sector.name if hasattr(sector, "name") else sector
        sector_str = sector_str.upper()
        return [
            m for m in self._models.values()
            if any(sec.upper() == sector_str for sec in m.supported_sectors)
        ]

    def filter_by_risk(self, risk_level: RiskLevel) -> list[ModelCapabilityProfile]:
        """Filter models whose maximum risk level is greater than or equal to the requested risk."""
        risk_values = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }
        req_val = risk_values.get(risk_level, 1)
        return [
            m for m in self._models.values()
            if risk_values.get(m.max_risk_level, 1) >= req_val
        ]

    def filter_by_required_capability(self, capability: str) -> list[ModelCapabilityProfile]:
        """Filter models that support a specific capability (tools, code, json, long_context)."""
        cap = capability.lower()
        if cap == "tools":
            return [m for m in self._models.values() if m.supports_tools]
        elif cap == "code":
            return [m for m in self._models.values() if m.supports_code]
        elif cap == "json":
            return [m for m in self._models.values() if m.supports_json]
        elif cap == "long_context":
            return [m for m in self._models.values() if m.supports_long_context]
        return []
