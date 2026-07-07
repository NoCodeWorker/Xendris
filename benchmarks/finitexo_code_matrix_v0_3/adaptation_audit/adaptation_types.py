"""Types for v0.3.3 adaptation and contamination audit."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class AdaptationType(str, Enum):
    DIRECT_PORT = "DIRECT_PORT"
    API_NORMALIZATION = "API_NORMALIZATION"
    BUG_REPRODUCTION_TO_FIXTURE = "BUG_REPRODUCTION_TO_FIXTURE"
    REQUIREMENT_EXTRACTION = "REQUIREMENT_EXTRACTION"
    TESTCASE_EXTRACTION = "TESTCASE_EXTRACTION"
    LANGUAGE_PORT = "LANGUAGE_PORT"
    SYNTHETIC_EXPANSION = "SYNTHETIC_EXPANSION"
    MUTATED_INTERNAL_FIXTURE = "MUTATED_INTERNAL_FIXTURE"
    UNKNOWN = "UNKNOWN"


class TaskValidityStatus(str, Enum):
    VALID = "VALID"
    VALID_WITH_WARNINGS = "VALID_WITH_WARNINGS"
    NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"
    INVALID = "INVALID"
    BLOCKED = "BLOCKED"


class BenchmarkFitStatus(str, Enum):
    FIT_FOR_AGENTIC_PROGRAMMING = "FIT_FOR_AGENTIC_PROGRAMMING"
    FIT_WITH_LIMITATIONS = "FIT_WITH_LIMITATIONS"
    TOO_TRIVIAL = "TOO_TRIVIAL"
    TOO_AMBIGUOUS = "TOO_AMBIGUOUS"
    TOO_DOMAIN_SPECIFIC = "TOO_DOMAIN_SPECIFIC"
    TOO_DEPENDENT_ON_EXTERNAL_STATE = "TOO_DEPENDENT_ON_EXTERNAL_STATE"
    BLOCKED = "BLOCKED"


class LeakageRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


class DifficultyLevel(str, Enum):
    TRIVIAL = "TRIVIAL"
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXTREME = "EXTREME"
    UNKNOWN = "UNKNOWN"


class PromotionRecommendation(str, Enum):
    RECOMMEND_FOR_FUTURE_FREEZE = "RECOMMEND_FOR_FUTURE_FREEZE"
    RECOMMEND_WITH_HUMAN_REVIEW = "RECOMMEND_WITH_HUMAN_REVIEW"
    DO_NOT_PROMOTE = "DO_NOT_PROMOTE"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class AdaptationAuditDecision:
    recommendation: PromotionRecommendation
    flags: tuple[str, ...] = ()
    rejection_reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "recommendation": self.recommendation.value,
            "flags": list(self.flags),
            "rejection_reasons": list(self.rejection_reasons),
            "warnings": list(self.warnings),
        }

