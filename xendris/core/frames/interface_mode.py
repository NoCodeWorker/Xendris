"""Interface Mode and Action Intent models for Xendris Epistemic Frame Layer.

InterfaceMode describes the delivery channel of a model output.
ActionIntent describes the intended effect on the user.

Each combination of InterfaceMode × ActionIntent has a risk profile
that determines which epistemic frames are compatible.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class InterfaceMode(Enum):
    """Delivery channel for model output."""
    CHAT = "CHAT"
    DASHBOARD = "DASHBOARD"
    API = "API"
    REPORT = "REPORT"
    CANVAS = "CANVAS"

    @property
    def label(self) -> str:
        labels = {
            "CHAT": "Conversational Chat",
            "DASHBOARD": "Dashboard / Visual",
            "API": "Programmatic API",
            "REPORT": "Structured Report",
            "CANVAS": "Canvas / Editor",
        }
        return labels.get(self.value, self.value)

    @property
    def persistence(self) -> str:
        """How persistent the output is."""
        persistence_map = {
            "CHAT": "ephemeral",
            "DASHBOARD": "persistent",
            "API": "persistent",
            "REPORT": "persistent",
            "CANVAS": "persistent",
        }
        return persistence_map.get(self.value, "ephemeral")


class ActionIntent(Enum):
    """Intended effect of the output on the user."""
    EXPLAIN = "EXPLAIN"
    PERSUADE = "PERSUADE"
    INSTRUCT = "INSTRUCT"
    DECIDE = "DECIDE"
    CREATE = "CREATE"

    @property
    def label(self) -> str:
        labels = {
            "EXPLAIN": "Explain / Inform",
            "PERSUADE": "Persuade / Convince",
            "INSTRUCT": "Instruct / Guide",
            "DECIDE": "Decide / Recommend",
            "CREATE": "Create / Generate",
        }
        return labels.get(self.value, self.value)

    @property
    def risk_baseline(self) -> str:
        """Baseline epistemic risk for this intent."""
        risk_map = {
            "EXPLAIN": "LOW",
            "PERSUADE": "HIGH",
            "INSTRUCT": "MEDIUM",
            "DECIDE": "HIGH",
            "CREATE": "LOW",
        }
        return risk_map.get(self.value, "MEDIUM")


@dataclass(frozen=True)
class InterfaceRiskProfile:
    """Risk profile for a specific InterfaceMode × ActionIntent combination."""

    mode: InterfaceMode
    intent: ActionIntent
    risk_level: str
    recommended_frames: tuple[str, ...] = field(default_factory=tuple)
    warning: str = ""


_RISK_MATRIX: dict[tuple[str, str], InterfaceRiskProfile] = {}


def _register(mode: str, intent: str, risk: str, frames: tuple[str, ...], warning: str = "") -> None:
    _RISK_MATRIX[(mode, intent)] = InterfaceRiskProfile(
        mode=InterfaceMode(mode),
        intent=ActionIntent(intent),
        risk_level=risk,
        recommended_frames=frames,
        warning=warning,
    )


_register("CHAT", "EXPLAIN", "LOW", ("EDUCATIONAL", "INTERNAL_REVIEW"))
_register("CHAT", "PERSUADE", "HIGH", ("MARKETING",), "Chat persuasion carries high epistemic risk. Use MARKETING frame.")
_register("CHAT", "INSTRUCT", "MEDIUM", ("EDUCATIONAL", "INTERNAL_REVIEW"))
_register("CHAT", "DECIDE", "HIGH", ("INTERNAL_REVIEW", "REPORT"), "Chat-based decisions require internal review frame.")
_register("CHAT", "CREATE", "LOW", ("DEBUG", "HYPOTHESIS"))

_register("DASHBOARD", "EXPLAIN", "LOW", ("REPORT", "EDUCATIONAL"))
_register("DASHBOARD", "PERSUADE", "HIGH", ("MARKETING",), "Dashboard persuasion requires MARKETING frame.")
_register("DASHBOARD", "DECIDE", "CRITICAL", ("PRODUCTION", "SAFETY_AUDIT"), "Dashboard decisions require PRODUCTION or SAFETY_AUDIT frame.")

_register("API", "EXPLAIN", "LOW", ("BENCHMARK", "REPORT"))
_register("API", "INSTRUCT", "MEDIUM", ("PRODUCTION", "DEPLOYMENT"))
_register("API", "DECIDE", "CRITICAL", ("PRODUCTION", "SAFETY_AUDIT"), "API decisions require production evidence and safety audit.")

_register("REPORT", "EXPLAIN", "LOW", ("BENCHMARK", "REPORT"))
_register("REPORT", "PERSUADE", "HIGH", ("MARKETING",), "Report persuasion requires MARKETING frame.")
_register("REPORT", "DECIDE", "CRITICAL", ("PRODUCTION", "SAFETY_AUDIT"), "Report-based decisions require production evidence.")

_register("CANVAS", "EXPLAIN", "LOW", ("EDUCATIONAL", "HYPOTHESIS"))
_register("CANVAS", "CREATE", "LOW", ("DEBUG", "HYPOTHESIS"))
_register("CANVAS", "INSTRUCT", "MEDIUM", ("EDUCATIONAL", "INTERNAL_REVIEW"))


def get_risk_profile(mode: InterfaceMode, intent: ActionIntent) -> InterfaceRiskProfile:
    """Get the risk profile for a mode/intent combination."""
    key = (mode.value, intent.value)
    profile = _RISK_MATRIX.get(key)
    if profile:
        return profile
    return InterfaceRiskProfile(
        mode=mode,
        intent=intent,
        risk_level="MEDIUM",
        recommended_frames=("INTERNAL_REVIEW",),
        warning=f"No explicit risk profile for {mode.value}/{intent.value}. Defaulting to MEDIUM.",
    )
