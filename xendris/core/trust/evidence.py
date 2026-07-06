"""Deterministic evidence bindings for the Xendris Trust Kernel.

The evidence layer does not crawl files, call networks, retrieve sources, or
validate factual truth. It only represents evidence objects supplied by the
caller and computes conservative support scores from their declared confidence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Iterable, Mapping

from .claims import Claim


class EvidenceType(str, Enum):
    """Structural type for an evidence object."""

    DOCUMENT = "DOCUMENT"
    TEST_RESULT = "TEST_RESULT"
    CODE_SYMBOL = "CODE_SYMBOL"
    RUNTIME_OUTPUT = "RUNTIME_OUTPUT"
    USER_MESSAGE = "USER_MESSAGE"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"
    DERIVED_PROOF = "DERIVED_PROOF"


def _validate_confidence(confidence: float) -> None:
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("evidence confidence must be between 0.0 and 1.0")


def _clamp_score(score: float) -> float:
    return min(max(score, 0.0), 1.0)


@dataclass(frozen=True)
class Evidence:
    """Immutable deterministic evidence record supplied to the trust kernel."""

    evidence_id: str
    evidence_type: EvidenceType
    source: str
    content_hash: str
    excerpt: str | None
    confidence: float
    metadata: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.evidence_id.strip():
            raise ValueError("evidence_id must not be empty")
        if not isinstance(self.evidence_type, EvidenceType):
            raise ValueError("evidence_type must be a valid EvidenceType")
        if not self.source.strip():
            raise ValueError("source must not be empty")
        if not self.content_hash.strip():
            raise ValueError("content_hash must not be empty")
        _validate_confidence(self.confidence)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    def to_dict(self) -> dict[str, object]:
        """Return a simple JSON-compatible representation."""

        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "source": self.source,
            "content_hash": self.content_hash,
            "excerpt": self.excerpt,
            "confidence": self.confidence,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class EvidenceBinding:
    """A claim plus the evidence items used to support it."""

    claim: Claim
    evidence_items: tuple[Evidence, ...]
    support_score: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_items", tuple(self.evidence_items))
        object.__setattr__(self, "support_score", _clamp_score(self.support_score))

    def to_dict(self) -> dict[str, object]:
        """Return a simple JSON-compatible representation."""

        return {
            "claim": self.claim.to_dict(),
            "evidence_items": [item.to_dict() for item in self.evidence_items],
            "support_score": self.support_score,
        }


def compute_support_score(claim: Claim, evidence_items: Iterable[Evidence]) -> float:
    """Compute deterministic support score for a claim from supplied evidence.

    The current v0.3.1 rule is intentionally simple: no evidence returns 0.0;
    otherwise the support score is the average evidence confidence clamped to
    ``[0.0, 1.0]``. The claim argument is retained for future source weighting.
    """

    del claim
    items = tuple(evidence_items)
    if not items:
        return 0.0
    return _clamp_score(sum(item.confidence for item in items) / len(items))


def bind_evidence_to_claim(
    claim: Claim,
    evidence_items: Iterable[Evidence],
) -> EvidenceBinding:
    """Bind supplied evidence to an immutable claim without mutating it."""

    items = tuple(evidence_items)
    return EvidenceBinding(
        claim=claim,
        evidence_items=items,
        support_score=compute_support_score(claim, items),
    )
