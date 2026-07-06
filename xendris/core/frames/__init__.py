"""xendris.core.frames — Epistemic frame layer for Xendris.

Defines epistemic frames that govern what evidence is required for
claims made within each frame, and guards that detect frame shifts,
actionability mismatches, and presentation/truth gaps.
"""

from xendris.core.frames.actionability_gate import (
    ActionClass,
    ActionabilityDecision,
    ActionabilityVerdict,
    evaluate_actionability,
)
from xendris.core.frames.epistemic_frame import (
    ActionabilityLevel,
    EpistemicFrame,
    EvidenceRequirements,
    FrameProfile,
)
from xendris.core.frames.evidence_requirements import (
    EvidenceRequirementVerdict,
    EvidenceRequirementsResult,
    RequirementCheck,
    check_evidence_requirements,
)
from xendris.core.frames.frame_shift_guard import (
    FrameShiftDecision,
    FrameShiftVerdict,
    evaluate_frame_shift,
)
from xendris.core.frames.interface_mode import (
    ActionIntent,
    InterfaceMode,
    InterfaceRiskProfile,
    get_risk_profile,
)
from xendris.core.frames.interface_truth_gap import (
    TruthGapAssessment,
    TruthGapSeverity,
    assess_interface_truth_gap,
)
from xendris.core.frames.presentation_boundary import (
    PresentationBoundaryDecision,
    PresentationBoundaryVerdict,
    evaluate_presentation_boundary,
)

__all__ = [
    "ActionClass",
    "ActionabilityDecision",
    "ActionabilityLevel",
    "ActionabilityVerdict",
    "ActionIntent",
    "EpistemicFrame",
    "EvidenceRequirements",
    "EvidenceRequirementVerdict",
    "EvidenceRequirementsResult",
    "FrameProfile",
    "FrameShiftDecision",
    "FrameShiftVerdict",
    "InterfaceMode",
    "InterfaceRiskProfile",
    "PresentationBoundaryDecision",
    "PresentationBoundaryVerdict",
    "RequirementCheck",
    "TruthGapAssessment",
    "TruthGapSeverity",
    "assess_interface_truth_gap",
    "get_risk_profile",
    "check_evidence_requirements",
    "evaluate_actionability",
    "evaluate_frame_shift",
    "evaluate_presentation_boundary",
]
