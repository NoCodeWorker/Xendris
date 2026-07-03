"""Pure assessment structures for the Xendris Response Contract v0.2.0.

This module represents conservative response-contract posture. It does not
validate factual truth, replace human review, call models, retrieve sources,
rewrite responses, or perform deep semantic reasoning.

The optional helpers are surface-level conservative heuristics. They only
inspect explicit wording signals such as uncertainty markers, absolute
language, and domain-validity hints.
"""

from __future__ import annotations

from dataclasses import dataclass

from .types import ClaimType, ConfidenceLevel, DomainValidity, ResponseMode


_ABSOLUTE_TERMS = (
    "always",
    "never",
    "exactly",
    "proven",
    "universal",
    "guaranteed",
    "siempre",
    "nunca",
    "exactamente",
    "probado",
    "universal",
    "garantizado",
)

_UNCERTAINTY_TERMS = (
    "may",
    "might",
    "suggests",
    "under these assumptions",
    "with current evidence",
    "uncertain",
    "puede",
    "podria",
    "podría",
    "sugiere",
    "bajo estas condiciones",
    "con la evidencia actual",
    "incierto",
)

_DOMAIN_LIMIT_TERMS = (
    "limit",
    "exception",
    "assumption",
    "domain",
    "scope",
    "unless",
    "locally",
    "context",
    "limite",
    "límite",
    "excepcion",
    "excepción",
    "supuesto",
    "dominio",
    "alcance",
    "salvo",
    "localmente",
    "contexto",
)

_EXPERIMENTAL_TERMS = (
    "experimental",
    "experiment",
    "trial",
    "pilot",
    "experimento",
    "experimental",
    "piloto",
)


@dataclass(frozen=True)
class ClaimAssessment:
    """Conservative representation of a single claim-like statement.

    This is not a truth label. It records how a claim is being represented for
    response-contract checks.
    """

    text: str
    claim_type: ClaimType
    confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN
    domain_validity: DomainValidity = DomainValidity.UNKNOWN
    notes: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        """Return a JSON-friendly representation."""

        return {
            "text": self.text,
            "claim_type": self.claim_type.value,
            "confidence": self.confidence.value,
            "domain_validity": self.domain_validity.value,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class ResponseContractAssessment:
    """Conservative response-contract posture for one response.

    This assessment does not validate whether a response is correct. It only
    records whether its represented claims and formal caution signals satisfy
    minimal conservative posture rules.
    """

    mode: ResponseMode
    claims: tuple[ClaimAssessment, ...] = ()
    has_domain_limits: bool = False
    has_uncertainty_marker: bool = False
    has_overclaim_risk: bool = False
    notes: str | None = None

    def is_conservative(self) -> bool:
        """Return whether the assessment satisfies conservative posture rules."""

        if self.has_overclaim_risk:
            return False
        for claim in self.claims:
            if claim.confidence == ConfidenceLevel.HIGH and claim.claim_type in {
                ClaimType.SPECULATION,
                ClaimType.UNVERIFIED,
            }:
                return False
        return True

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-friendly representation."""

        return {
            "mode": self.mode.value,
            "claims": [claim.to_dict() for claim in self.claims],
            "has_domain_limits": self.has_domain_limits,
            "has_uncertainty_marker": self.has_uncertainty_marker,
            "has_overclaim_risk": self.has_overclaim_risk,
            "is_conservative": self.is_conservative(),
            "notes": self.notes,
        }


def make_claim(
    *,
    text: str,
    claim_type: ClaimType,
    confidence: ConfidenceLevel = ConfidenceLevel.UNKNOWN,
    domain_validity: DomainValidity = DomainValidity.UNKNOWN,
    notes: str | None = None,
) -> ClaimAssessment:
    """Create a claim assessment without inferring factual truth."""

    return ClaimAssessment(
        text=text,
        claim_type=claim_type,
        confidence=confidence,
        domain_validity=domain_validity,
        notes=notes,
    )


def normalize_text(text: str) -> str:
    """Normalize text for deterministic surface-level checks."""

    return " ".join(text.strip().lower().split())


def classify_claim_text(text: str) -> ClaimType:
    """Classify explicit wording cues using superficial conservative heuristics.

    This helper does not know whether the claim is true. It only maps visible
    wording into a coarse claim posture.
    """

    normalized = normalize_text(text)
    if not normalized:
        return ClaimType.UNVERIFIED
    if any(term in normalized for term in ("observed", "measured", "medido", "observado")):
        return ClaimType.OBSERVED
    if any(term in normalized for term in ("therefore", "derived", "derives", "por tanto", "deriva")):
        return ClaimType.DERIVED
    if any(term in normalized for term in ("standard", "known", "established", "estándar", "estandar", "conocido")):
        return ClaimType.STANDARD_KNOWLEDGE
    if any(term in normalized for term in ("suggests", "implies", "inference", "sugiere", "implica", "inferencia")):
        return ClaimType.INFERENCE
    if any(term in normalized for term in ("speculative", "hypothesis", "could be", "especulativo", "hipótesis", "hipotesis")):
        return ClaimType.SPECULATION
    return ClaimType.UNVERIFIED


def estimate_confidence(text: str) -> ConfidenceLevel:
    """Estimate coarse confidence posture from wording only.

    This v0.2.0 helper intentionally never returns ``HIGH``. High confidence
    requires evidence this surface-level layer cannot inspect.
    """

    normalized = normalize_text(text)
    if not normalized:
        return ConfidenceLevel.UNKNOWN
    if any(term in normalized for term in _ABSOLUTE_TERMS):
        return ConfidenceLevel.LOW
    if any(term in normalized for term in _UNCERTAINTY_TERMS):
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.UNKNOWN


def detect_domain_validity(text: str, domain: str | None = None) -> DomainValidity:
    """Detect domain-validity posture from explicit wording only."""

    combined = normalize_text(" ".join(part for part in (domain or "", text) if part))
    if not combined:
        return DomainValidity.UNKNOWN
    if any(term in combined for term in _EXPERIMENTAL_TERMS):
        return DomainValidity.EXPERIMENTAL
    if any(term in combined for term in _DOMAIN_LIMIT_TERMS):
        return DomainValidity.CONTEXT_DEPENDENT
    if any(term in combined for term in ("local", "locally", "localmente")):
        return DomainValidity.LOCAL
    if domain:
        return DomainValidity.CONTEXT_DEPENDENT
    return DomainValidity.GENERAL


def assess_response_contract(
    text: str,
    *,
    domain: str | None = None,
    mode: ResponseMode = ResponseMode.STANDARD,
) -> ResponseContractAssessment:
    """Create a surface-level conservative response-contract assessment.

    This helper checks explicit wording signals only. It does not validate
    factual correctness, scientific support, semantic quality, or usefulness.
    """

    normalized = normalize_text(text)
    has_overclaim_risk = any(term in normalized for term in _ABSOLUTE_TERMS)
    has_uncertainty_marker = any(term in normalized for term in _UNCERTAINTY_TERMS)
    has_domain_limits = any(term in normalized for term in _DOMAIN_LIMIT_TERMS)
    claim = make_claim(
        text=text,
        claim_type=classify_claim_text(text),
        confidence=estimate_confidence(text),
        domain_validity=detect_domain_validity(text, domain),
    )
    notes: list[str] = []

    if has_overclaim_risk:
        notes.append("surface_overclaim_signal")
    if not has_uncertainty_marker:
        notes.append("uncertainty_marker_not_detected")
    if not has_domain_limits:
        notes.append("domain_limits_not_detected")

    return ResponseContractAssessment(
        mode=mode,
        claims=(claim,),
        has_domain_limits=has_domain_limits,
        has_uncertainty_marker=has_uncertainty_marker,
        has_overclaim_risk=has_overclaim_risk,
        notes=", ".join(notes) or None,
    )
