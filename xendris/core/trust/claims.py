"""Claim model for the Xendris Trust Kernel."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .types import ClaimStatus, ClaimType


def _validate_confidence(confidence: float) -> None:
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass(frozen=True)
class Claim:
    """An auditable claim extracted from, or declared for, an answer.

    The claim stores structural audit metadata. It is not a proof that the text
    is true.
    """

    text: str
    claim_type: ClaimType
    confidence: float
    status: ClaimStatus
    source_refs: tuple[str, ...] = ()
    notes: str | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("claim text must not be empty")
        _validate_confidence(self.confidence)
        object.__setattr__(self, "source_refs", tuple(self.source_refs))

    def to_dict(self) -> dict[str, object]:
        """Return a simple JSON-compatible representation."""

        return {
            "text": self.text,
            "claim_type": self.claim_type.value,
            "confidence": self.confidence,
            "status": self.status.value,
            "source_refs": list(self.source_refs),
            "notes": self.notes,
        }


def make_claim(
    *,
    text: str,
    claim_type: ClaimType,
    confidence: float,
    status: ClaimStatus,
    source_refs: Iterable[str] = (),
    notes: str | None = None,
) -> Claim:
    """Create a claim with validation and immutable source references."""

    return Claim(
        text=text,
        claim_type=claim_type,
        confidence=confidence,
        status=status,
        source_refs=tuple(source_refs),
        notes=notes,
    )
