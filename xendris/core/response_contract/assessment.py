"""Conservative helpers for the Xendris response contract.

The helpers in this module are deterministic surface-signal checks. They do
not validate factual truth, replace human review, call models, retrieve
sources, rewrite answers, or perform deep semantic reasoning. They only expose
minimal contract posture signals such as absolute wording, uncertainty wording,
and domain-validity hints.
"""

from __future__ import annotations

from .types import (
    ClaimType,
    ConfidenceLevel,
    DomainValidity,
    ResponseContractAssessment,
    ResponseMode,
)


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

_LIMIT_TERMS = (
    "limit",
    "exception",
    "assumption",
    "domain",
    "scope",
    "unless",
    "limite",
    "límite",
    "excepcion",
    "excepción",
    "supuesto",
    "dominio",
    "alcance",
    "salvo",
)

_SENSITIVE_DOMAINS = (
    "medical",
    "medicine",
    "legal",
    "finance",
    "financial",
    "salud",
    "medicina",
    "juridico",
    "jurídico",
    "legal",
    "finanzas",
    "financiero",
)


def normalize_text(text: str) -> str:
    """Normalize text for deterministic surface-signal helpers."""

    return " ".join(text.strip().lower().split())


def classify_claim_text(text: str) -> ClaimType:
    """Classify visible claim wording with superficial conservative heuristics.

    This helper does not know whether the claim is true. It only maps explicit
    wording cues into a coarse posture bucket.
    """

    normalized = normalize_text(text)
    if not normalized:
        return ClaimType.UNVERIFIED
    if any(term in normalized for term in ("observed", "measured", "medido", "observado")):
        return ClaimType.OBSERVED
    if any(term in normalized for term in ("therefore", "derives", "derived", "por tanto", "deriva")):
        return ClaimType.DERIVED
    if any(term in normalized for term in ("standard", "known", "established", "estandar", "estándar", "conocido")):
        return ClaimType.STANDARD_KNOWLEDGE
    if any(term in normalized for term in ("suggests", "implies", "inference", "sugiere", "implica", "inferencia")):
        return ClaimType.INFERENCE
    if any(term in normalized for term in ("speculative", "hypothesis", "could be", "especulativo", "hipotesis", "hipótesis")):
        return ClaimType.SPECULATION
    return ClaimType.UNVERIFIED


def estimate_confidence(text: str) -> ConfidenceLevel:
    """Estimate a coarse confidence posture from response wording.

    This helper intentionally avoids returning ``HIGH``. High confidence should
    require stronger evidence than this v0.2.0 surface-signal layer can provide.
    """

    normalized = normalize_text(text)
    if not normalized:
        return ConfidenceLevel.UNKNOWN
    if any(term in normalized for term in _UNCERTAINTY_TERMS):
        return ConfidenceLevel.MEDIUM
    if any(term in normalized for term in _ABSOLUTE_TERMS):
        return ConfidenceLevel.LOW
    if len(normalized.split()) >= 24:
        return ConfidenceLevel.MEDIUM
    return ConfidenceLevel.UNKNOWN


def detect_domain_validity(text: str, domain: str | None = None) -> DomainValidity:
    """Classify domain-of-validity posture from explicit wording only."""

    combined = normalize_text(" ".join(part for part in (domain or "", text) if part))
    if not combined:
        return DomainValidity.UNKNOWN
    if any(term in combined for term in _SENSITIVE_DOMAINS):
        return DomainValidity.SENSITIVE_DOMAIN
    if any(term in combined for term in ("assumption", "under", "if ", "supuesto", "bajo", "si ")):
        return DomainValidity.ASSUMPTION_BOUND
    if domain:
        return DomainValidity.DOMAIN_SPECIFIC
    return DomainValidity.GENERAL


def assess_response_contract(
    text: str,
    *,
    domain: str | None = None,
    response_mode: ResponseMode = ResponseMode.PRACTICAL,
) -> ResponseContractAssessment:
    """Create a minimal pure response-contract assessment.

    The assessment represents formal contract signals. It does not validate
    factual correctness or scientific support.
    """

    normalized = normalize_text(text)
    absolute_terms_present = any(term in normalized for term in _ABSOLUTE_TERMS)
    uncertainty_marked = any(term in normalized for term in _UNCERTAINTY_TERMS)
    limits_stated = any(term in normalized for term in _LIMIT_TERMS)
    notes: list[str] = []

    if absolute_terms_present:
        notes.append("absolute_language_detected")
    if not limits_stated:
        notes.append("limits_not_explicit")
    if not uncertainty_marked:
        notes.append("uncertainty_not_explicit")

    return ResponseContractAssessment(
        claim_type=classify_claim_text(text),
        confidence_level=estimate_confidence(text),
        response_mode=response_mode,
        domain_validity=detect_domain_validity(text, domain),
        non_overclaiming=not absolute_terms_present,
        limits_stated=limits_stated,
        uncertainty_marked=uncertainty_marked,
        has_overclaim_risk=absolute_terms_present,
        notes=tuple(notes),
    )
