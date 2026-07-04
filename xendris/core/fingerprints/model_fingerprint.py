"""Immutable ModelIdentity and ModelEpistemicFingerprint dataclass definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping
from xendris.core.fingerprints.metrics import FingerprintMetric


@dataclass(frozen=True)
class ModelIdentity:
    """Immutable representation of a model's operational deployment configuration."""

    model_id: str
    provider: str
    version: str
    configuration: Mapping[str, Any] = field(default_factory=dict)
    temperature: float = 0.0
    max_tokens: int = 2048
    run_context: str = "DEFAULT"
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModelEpistemicFingerprint:
    """Immutable profile aggregating logical verification outcomes at the model level."""

    model_identity: ModelIdentity
    sample_count: int
    run_id: str
    dataset_id: str
    metrics: Mapping[FingerprintMetric, float]
    observed_strengths: tuple[str, ...]
    observed_risks: tuple[str, ...]
    recommended_use: tuple[str, ...]
    required_gates: tuple[str, ...]
    limitations: tuple[str, ...]
    created_from_audits: tuple[str, ...]
