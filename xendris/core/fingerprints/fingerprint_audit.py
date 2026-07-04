"""Deterministic FingerprintAudit definition for tracking fingerprint creations."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any
from xendris.core.fingerprints.model_fingerprint import ModelIdentity, ModelEpistemicFingerprint
from xendris.core.fingerprints.profile import FingerprintProfile


@dataclass(frozen=True)
class FingerprintAudit:
    """A deterministic audit record documenting the creation of a model fingerprint."""

    fingerprint_id: str
    model_identity: ModelIdentity
    source_audit_count: int
    metrics_hash: str
    generated_profile: FingerprintProfile
    limitations: tuple[str, ...]

    @classmethod
    def create(
        cls,
        fingerprint_id: str,
        fingerprint: ModelEpistemicFingerprint,
    ) -> FingerprintAudit:
        """Create a deterministic FingerprintAudit record from a fingerprint."""
        profile = FingerprintProfile.from_fingerprint(fingerprint)
        
        # Calculate a deterministic metrics hash
        serialized_metrics = json.dumps(profile.metrics, sort_keys=True)
        metrics_hash = hashlib.sha256(serialized_metrics.encode("utf-8")).hexdigest()

        return cls(
            fingerprint_id=fingerprint_id,
            model_identity=fingerprint.model_identity,
            source_audit_count=fingerprint.sample_count,
            metrics_hash=metrics_hash,
            generated_profile=profile,
            limitations=fingerprint.limitations,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert audit to a standard Python dictionary for serialization."""
        return {
            "fingerprint_id": self.fingerprint_id,
            "model_id": self.model_identity.model_id,
            "source_audit_count": self.source_audit_count,
            "metrics_hash": self.metrics_hash,
            "generated_profile": self.generated_profile.to_dict(),
            "limitations": list(self.limitations),
        }
