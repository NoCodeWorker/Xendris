"""Types for the v0.3.2 external source acquisition gate."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SourceType(str, Enum):
    PUBLIC_GITHUB_ISSUE = "PUBLIC_GITHUB_ISSUE"
    PUBLIC_GITHUB_PR = "PUBLIC_GITHUB_PR"
    OPEN_SOURCE_TEST_CASE = "OPEN_SOURCE_TEST_CASE"
    PUBLIC_BUG_REPORT = "PUBLIC_BUG_REPORT"
    PUBLIC_DOC_EXAMPLE = "PUBLIC_DOC_EXAMPLE"
    ACADEMIC_EXERCISE = "ACADEMIC_EXERCISE"
    INTERNAL_FIXTURE = "INTERNAL_FIXTURE"
    SYNTHETIC_LOCAL = "SYNTHETIC_LOCAL"
    UNKNOWN = "UNKNOWN"


class ContaminationRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


class OriginCandidate(str, Enum):
    EXTERNAL_VERIFIED = "EXTERNAL_VERIFIED"
    EXTERNAL_ADAPTED = "EXTERNAL_ADAPTED"
    MUTATED_FIXTURE = "MUTATED_FIXTURE"
    SEMI_EXTERNAL_SYNTHETIC = "SEMI_EXTERNAL_SYNTHETIC"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class PromotionDecision:
    promotion_allowed: bool
    decision: str
    blockers: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "promotion_allowed": self.promotion_allowed,
            "decision": self.decision,
            "blockers": list(self.blockers),
            "warnings": list(self.warnings),
        }

