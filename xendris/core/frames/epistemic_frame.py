"""Epistemic Frame definitions for Xendris Trust Kernel.

An EpistemicFrame classifies the communicative context of a model output.
Each frame defines what kind of evidence is required, how actionable the
output is, and which trust gates should apply by default.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


ActionabilityLevel = Literal["explanatory", "actionable", "critical"]
"""How actionable an output in this frame is considered."""


@dataclass(frozen=True)
class EvidenceRequirements:
    """What evidence is required for claims in this frame."""

    requires_deployment_evidence: bool = False
    requires_dataset_scope: bool = False
    requires_provider_disclosure: bool = False
    requires_cost_disclosure: bool = False
    requires_latency_disclosure: bool = False
    bans_universal_language: bool = False
    bans_absolute_guarantees: bool = False
    requires_external_citation: bool = False
    requires_limitation_statement: bool = False
    requires_human_review_for_critical: bool = False
    allows_hypothesis_without_proof: bool = False


@dataclass(frozen=True)
class FrameProfile:
    """Complete profile for a single EpistemicFrame."""

    name: str
    label: str
    actionability: ActionabilityLevel
    evidence_requirements: EvidenceRequirements
    default_gates: tuple[str, ...] = field(default_factory=tuple)
    description: str = ""


class EpistemicFrame(Enum):
    """Epistemic frames for classifying model output context.

    Each frame represents a distinct communicative context with specific
    evidence requirements, actionability levels, and default trust gates.
    """

    # === Production / Deployment ===
    PRODUCTION = FrameProfile(
        name="PRODUCTION",
        label="Production Deployment",
        actionability="critical",
        evidence_requirements=EvidenceRequirements(
            requires_deployment_evidence=True,
            requires_limitation_statement=True,
            requires_human_review_for_critical=True,
            bans_absolute_guarantees=True,
        ),
        default_gates=("actionability", "presentation_boundary", "human_review"),
        description="Output intended for production use. Requires deployment evidence and human review for critical decisions.",
    )
    DEPLOYMENT = FrameProfile(
        name="DEPLOYMENT",
        label="Deployment Decision",
        actionability="critical",
        evidence_requirements=EvidenceRequirements(
            requires_deployment_evidence=True,
            requires_limitation_statement=True,
            requires_human_review_for_critical=True,
        ),
        default_gates=("actionability", "presentation_boundary"),
        description="Output supporting a deployment decision. Requires operational evidence.",
    )

    # === Benchmark / Evaluation ===
    BENCHMARK = FrameProfile(
        name="BENCHMARK",
        label="Benchmark Evaluation",
        actionability="actionable",
        evidence_requirements=EvidenceRequirements(
            requires_dataset_scope=True,
            requires_provider_disclosure=True,
            requires_cost_disclosure=True,
            requires_latency_disclosure=True,
            bans_universal_language=True,
        ),
        default_gates=("frame_shift", "evidence_requirements"),
        description="Benchmark evaluation results. Must disclose dataset scope, provider, cost, and latency.",
    )
    ABLATION = FrameProfile(
        name="ABLATION",
        label="Ablation Study",
        actionability="actionable",
        evidence_requirements=EvidenceRequirements(
            requires_dataset_scope=True,
            requires_provider_disclosure=True,
            requires_limitation_statement=True,
            bans_universal_language=True,
        ),
        default_gates=("frame_shift", "evidence_requirements"),
        description="Ablation study comparing system variants. Must disclose dataset and limitations.",
    )

    # === Research / Hypothesis ===
    HYPOTHESIS = FrameProfile(
        name="HYPOTHESIS",
        label="Research Hypothesis",
        actionability="explanatory",
        evidence_requirements=EvidenceRequirements(
            allows_hypothesis_without_proof=True,
            requires_limitation_statement=True,
        ),
        default_gates=("presentation_boundary",),
        description="Exploratory hypothesis or research direction. Evidence not required but must be labeled as hypothesis.",
    )
    THEORETICAL = FrameProfile(
        name="THEORETICAL",
        label="Theoretical Analysis",
        actionability="explanatory",
        evidence_requirements=EvidenceRequirements(
            allows_hypothesis_without_proof=True,
            requires_limitation_statement=True,
        ),
        default_gates=("presentation_boundary",),
        description="Theoretical analysis without empirical validation. Must note absence of empirical evidence.",
    )

    # === Marketing / Communication ===
    MARKETING = FrameProfile(
        name="MARKETING",
        label="Marketing / Communication",
        actionability="actionable",
        evidence_requirements=EvidenceRequirements(
            bans_universal_language=True,
            bans_absolute_guarantees=True,
            requires_limitation_statement=True,
        ),
        default_gates=("presentation_boundary", "frame_shift"),
        description="Marketing or public communication. Universal superiority claims and absolute guarantees are banned.",
    )
    EDUCATIONAL = FrameProfile(
        name="EDUCATIONAL",
        label="Educational / Tutorial",
        actionability="explanatory",
        evidence_requirements=EvidenceRequirements(
            requires_limitation_statement=True,
        ),
        default_gates=("presentation_boundary",),
        description="Educational or tutorial content. Limitations should be noted.",
    )

    # === Internal / Development ===
    INTERNAL_REVIEW = FrameProfile(
        name="INTERNAL_REVIEW",
        label="Internal Review",
        actionability="actionable",
        evidence_requirements=EvidenceRequirements(
            requires_limitation_statement=True,
        ),
        default_gates=("actionability",),
        description="Internal team review. Actionable but not externally validated.",
    )
    DEBUG = FrameProfile(
        name="DEBUG",
        label="Debug / Diagnostic",
        actionability="explanatory",
        evidence_requirements=EvidenceRequirements(
            allows_hypothesis_without_proof=True,
        ),
        default_gates=(),
        description="Debug or diagnostic output. Lowest evidence bar.",
    )

    # === Safety / Security ===
    SAFETY_AUDIT = FrameProfile(
        name="SAFETY_AUDIT",
        label="Safety Audit",
        actionability="critical",
        evidence_requirements=EvidenceRequirements(
            requires_external_citation=True,
            requires_human_review_for_critical=True,
            bans_absolute_guarantees=True,
        ),
        default_gates=("actionability", "frame_shift", "human_review"),
        description="Safety or security audit. Requires external citations and human review.",
    )

    # === Reporting ===
    REPORT = FrameProfile(
        name="REPORT",
        label="Structured Report",
        actionability="actionable",
        evidence_requirements=EvidenceRequirements(
            requires_limitation_statement=True,
            requires_provider_disclosure=True,
        ),
        default_gates=("presentation_boundary", "evidence_requirements"),
        description="Structured report. Must include limitations and provider disclosure.",
    )

    @property
    def profile(self) -> FrameProfile:
        return self.value

    @property
    def actionability(self) -> ActionabilityLevel:
        return self.profile.actionability

    @property
    def evidence_requirements(self) -> EvidenceRequirements:
        return self.profile.evidence_requirements

    @property
    def default_gates(self) -> tuple[str, ...]:
        return self.profile.default_gates

    @classmethod
    def from_name(cls, name: str) -> EpistemicFrame | None:
        for frame in cls:
            if frame.profile.name == name:
                return frame
        return None

    def can_shift_to(self, target: EpistemicFrame, has_evidence_bridge: bool = False) -> bool:
        """Whether a shift from this frame to target is allowed.

        A shift requires an evidence bridge unless both frames share the same
        actionability level or the target has lower actionability.
        """
        if self == target:
            return True
        levels = {"critical": 3, "actionable": 2, "explanatory": 1}
        current_level = levels.get(self.actionability, 0)
        target_level = levels.get(target.actionability, 0)
        if target_level <= current_level:
            return True
        return has_evidence_bridge
