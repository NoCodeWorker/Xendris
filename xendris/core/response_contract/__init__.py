"""Xendris Response Contract v0.2.0 core.

This package implements pure structures for representing response-contract
posture. It does not call models, validate factual truth, modify responses,
replace human review, run retrieval, or perform deep semantic reasoning.

It is a stable foundation for future evaluation layers, not a validator of
scientific or factual correctness.
"""

from .assessment import (
    ClaimAssessment,
    ResponseContractAssessment,
    assess_response_contract,
    classify_claim_text,
    detect_domain_validity,
    estimate_confidence,
    make_claim,
    normalize_text,
)
from .types import (
    ClaimType,
    ConfidenceLevel,
    DomainValidity,
    ResponseMode,
)

__all__ = [
    "ClaimType",
    "ConfidenceLevel",
    "ResponseMode",
    "DomainValidity",
    "ClaimAssessment",
    "ResponseContractAssessment",
    "make_claim",
    "normalize_text",
    "classify_claim_text",
    "estimate_confidence",
    "detect_domain_validity",
    "assess_response_contract",
]
