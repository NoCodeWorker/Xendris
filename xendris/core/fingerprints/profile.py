"""Serializable FingerprintProfile representing aggregated model behaviors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from xendris.core.fingerprints.model_fingerprint import ModelEpistemicFingerprint


@dataclass(frozen=True)
class FingerprintProfile:
    """A serializable snapshot profile of a model's epistemic fingerprint."""

    model_id: str
    provider: str
    dataset_id: str
    run_id: str
    summary: str
    metrics: dict[str, float]
    observed_strengths: list[str]
    observed_risks: list[str]
    recommended_use: list[str]
    required_gates: list[str]
    limitations: list[str]

    @classmethod
    def from_fingerprint(cls, fingerprint: ModelEpistemicFingerprint) -> FingerprintProfile:
        """Construct a serializable profile from a ModelEpistemicFingerprint."""
        identity = fingerprint.model_identity
        
        # Format metrics as simple string keys for serialization
        metrics_dict = {
            metric.name: val
            for metric, val in fingerprint.metrics.items()
        }
        
        summary = (
            f"Epistemic fingerprint for model {identity.model_id} (provider {identity.provider}) "
            f"over {fingerprint.sample_count} claims on dataset {fingerprint.dataset_id}."
        )

        return cls(
            model_id=identity.model_id,
            provider=identity.provider,
            dataset_id=fingerprint.dataset_id,
            run_id=fingerprint.run_id,
            summary=summary,
            metrics=metrics_dict,
            observed_strengths=list(fingerprint.observed_strengths),
            observed_risks=list(fingerprint.observed_risks),
            recommended_use=list(fingerprint.recommended_use),
            required_gates=list(fingerprint.required_gates),
            limitations=list(fingerprint.limitations),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert profile to a standard Python dictionary for serialization."""
        return {
            "model_id": self.model_id,
            "provider": self.provider,
            "dataset_id": self.dataset_id,
            "run_id": self.run_id,
            "summary": self.summary,
            "metrics": self.metrics,
            "observed_strengths": self.observed_strengths,
            "observed_risks": self.observed_risks,
            "recommended_use": self.recommended_use,
            "required_gates": self.required_gates,
            "limitations": self.limitations,
        }
