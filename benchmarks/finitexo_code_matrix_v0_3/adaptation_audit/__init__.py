"""External adaptation and contamination audit for Finitexo Code Matrix v0.3.3."""

from .adaptation_record import AdaptationRecord
from .adaptation_types import (
    AdaptationType,
    BenchmarkFitStatus,
    DifficultyLevel,
    LeakageRisk,
    PromotionRecommendation,
    TaskValidityStatus,
)
from .adaptation_validation import evaluate_adaptation_candidate

__all__ = [
    "AdaptationRecord",
    "AdaptationType",
    "BenchmarkFitStatus",
    "DifficultyLevel",
    "LeakageRisk",
    "PromotionRecommendation",
    "TaskValidityStatus",
    "evaluate_adaptation_candidate",
]

