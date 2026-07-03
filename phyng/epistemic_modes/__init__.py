"""
Phygn v1.6 — Epistemic Modes Package

Public API for the epistemic_modes subsystem.
"""

from phyng.epistemic_modes.schemas import (
    EpistemicMode,
    RiskLevel,
    FrictionLevel,
    LadderLevel,
    GateStatus,
    IncubationStatus,
    ModeGateResult,
    HypothesisSeed,
    IncubationResult,
    LadderClassification,
    FrictionDecision,
    FinancialActionGateResult,
)
from phyng.epistemic_modes.modes import (
    get_mode_risk,
    get_mode_description,
    is_high_risk_mode,
    is_low_risk_mode,
    MODE_DEFAULT_RISK,
)
from phyng.epistemic_modes.ladder import classify_ladder_level
from phyng.epistemic_modes.friction import evaluate_friction, get_friction_for_risk
from phyng.epistemic_modes.incubation import incubate_hypothesis
from phyng.epistemic_modes.gatekeeper import evaluate_mode_gate, evaluate_financial_action_gate
from phyng.epistemic_modes.report import write_epistemic_modes_reports

__all__ = [
    # Schemas
    "EpistemicMode",
    "RiskLevel",
    "FrictionLevel",
    "LadderLevel",
    "GateStatus",
    "IncubationStatus",
    "ModeGateResult",
    "HypothesisSeed",
    "IncubationResult",
    "LadderClassification",
    "FrictionDecision",
    "FinancialActionGateResult",
    # Modes
    "get_mode_risk",
    "get_mode_description",
    "is_high_risk_mode",
    "is_low_risk_mode",
    "MODE_DEFAULT_RISK",
    # Core functions
    "classify_ladder_level",
    "evaluate_friction",
    "get_friction_for_risk",
    "incubate_hypothesis",
    "evaluate_mode_gate",
    "evaluate_financial_action_gate",
    "write_epistemic_modes_reports",
]
