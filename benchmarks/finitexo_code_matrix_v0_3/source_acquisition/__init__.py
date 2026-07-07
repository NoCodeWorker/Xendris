"""Source acquisition gate for Finitexo Code Matrix v0.3.2."""

from .acquisition_types import (
    ContaminationRisk,
    OriginCandidate,
    PromotionDecision,
    SourceType,
)
from .source_acquisition_record import SourceAcquisitionRecord
from .acquisition_validation import evaluate_promotion_eligibility

__all__ = [
    "ContaminationRisk",
    "OriginCandidate",
    "PromotionDecision",
    "SourceAcquisitionRecord",
    "SourceType",
    "evaluate_promotion_eligibility",
]

