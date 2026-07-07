"""Small typed constants for the v0.4 frozen dataset validator."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FreezeDecision(str, Enum):
    READY = "READY"
    BLOCKED = "BLOCKED"


class FreezeIssueSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    WARNING = "WARNING"
    NOTE = "NOTE"


@dataclass(frozen=True)
class FreezeIssue:
    code: str
    severity: FreezeIssueSeverity
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "severity": self.severity.value,
            "message": self.message,
        }
