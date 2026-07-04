"""ClaimRepresentation definition for Xendris."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ClaimRepresentation:
    """An immutable, serialized representation of a claim from a specific source."""

    representation_id: str
    claim_id: str
    content: str
    source_model: str
    source_provider: str
    source_context: str
    epistemic_sector: str
    claim_type: str
    confidence: float
    evidence_refs: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.representation_id.strip():
            raise ValueError("representation_id must not be empty")
        if not self.claim_id.strip():
            raise ValueError("claim_id must not be empty")
        # Ensure collections are tuples
        object.__setattr__(self, "evidence_refs", tuple(self.evidence_refs))
        object.__setattr__(self, "limitations", tuple(self.limitations))
