"""Xendris response contract.

Minimal pure API for representing response posture, confidence, domain
validity, and conservative claim classification.

This package does not call models, rewrite responses, perform retrieval,
replace human review, validate factual truth, validate scientific claims, or
perform deep semantic reasoning. Its helpers expose deterministic surface
signals only.
"""

from .assessment import (
    assess_response_contract,
    classify_claim_text,
    detect_domain_validity,
    estimate_confidence,
    normalize_text,
)
from .types import (
    ClaimType,
    ConfidenceLevel,
    DomainValidity,
    ResponseContractAssessment,
    ResponseMode,
)

__all__ = [
    "ClaimType",
    "ConfidenceLevel",
    "ResponseMode",
    "DomainValidity",
    "ResponseContractAssessment",
    "normalize_text",
    "classify_claim_text",
    "estimate_confidence",
    "detect_domain_validity",
    "assess_response_contract",
]
