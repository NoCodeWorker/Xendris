"""
Phygn v1.9 — Business Model Validation Gate package
"""

from phyng.business_validation.schemas import (
    BusinessIdeaInput,
    BusinessHypothesis,
    BusinessHypothesisCanvas,
    WillingnessToPayTest,
    ChannelTest,
    UnitEconomicsProfile,
    BusinessRiskAssessment,
    KillCriteria,
    BusinessValidationGateResult,
    BusinessPostMortem,
    BusinessHypothesisType,
    BusinessValidationStatus,
    WillingnessToPayLevel,
    ChannelValidationLevel,
    UnitEconomicsStatus,
    BusinessRiskStatus,
    BusinessPermissionLevel,
)
from phyng.business_validation.decomposition import decompose_business_idea
from phyng.business_validation.canvas import generate_next_best_business_question
from phyng.business_validation.wtp import evaluate_willingness_to_pay, WTPGateResult
from phyng.business_validation.channel import evaluate_channel_test, ChannelGateResult
from phyng.business_validation.unit_economics import evaluate_unit_economics, UnitEconomicsGateResult
from phyng.business_validation.risk import evaluate_business_risk, BusinessRiskGateResult
from phyng.business_validation.kill_criteria import evaluate_kill_criteria, KillCriteriaGateResult
from phyng.business_validation.post_mortem import create_business_post_mortem
from phyng.business_validation.gatekeeper import evaluate_business_validation_gate
from phyng.business_validation.report import write_business_validation_reports

__all__ = [
    "BusinessIdeaInput",
    "BusinessHypothesis",
    "BusinessHypothesisCanvas",
    "WillingnessToPayTest",
    "ChannelTest",
    "UnitEconomicsProfile",
    "BusinessRiskAssessment",
    "KillCriteria",
    "BusinessValidationGateResult",
    "BusinessPostMortem",
    "BusinessHypothesisType",
    "BusinessValidationStatus",
    "WillingnessToPayLevel",
    "ChannelValidationLevel",
    "UnitEconomicsStatus",
    "BusinessRiskStatus",
    "BusinessPermissionLevel",
    "decompose_business_idea",
    "generate_next_best_business_question",
    "evaluate_willingness_to_pay",
    "WTPGateResult",
    "evaluate_channel_test",
    "ChannelGateResult",
    "evaluate_unit_economics",
    "UnitEconomicsGateResult",
    "evaluate_business_risk",
    "BusinessRiskGateResult",
    "evaluate_kill_criteria",
    "KillCriteriaGateResult",
    "create_business_post_mortem",
    "evaluate_business_validation_gate",
    "write_business_validation_reports",
]
