"""ActionabilityGate for Xendris Epistemic Frame Layer.

Classifies outputs by actionability level and enforces evidence requirements
based on the level. More actionable outputs require stronger evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


ActionClass = Literal["explanatory", "actionable", "critical"]


class ActionabilityDecision(Enum):
    ALLOW = "ALLOW"
    REQUIRE_MORE_EVIDENCE = "REQUIRE_MORE_EVIDENCE"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class ActionabilityVerdict:
    decision: ActionabilityDecision
    action_class: ActionClass
    reason: str
    requires_human_review: bool = False


def _detect_action_class(
    output_text: str,
    has_production_keywords: bool = False,
    has_deployment_references: bool = False,
    has_recommendation_language: bool = False,
    has_safety_critical_terms: bool = False,
) -> ActionClass:
    """Classify an output into explanatory / actionable / critical.

    Uses a combination of keyword signals and explicit flags. In production,
    this should be informed by the frame context rather than text heuristics.
    """
    if has_safety_critical_terms or (has_production_keywords and has_deployment_references):
        return "critical"
    if has_recommendation_language or has_production_keywords:
        return "actionable"
    return "explanatory"


def _min_evidence_for_action(action_class: ActionClass) -> str:
    """Minimum evidence bar for each action class."""
    return {
        "explanatory": "Claims must not contradict available evidence.",
        "actionable": "Claims must be supported by evidence and include limitations.",
        "critical": "Claims must be supported by verifiable evidence, include limitations, and undergo human review if uncertain.",
    }.get(action_class, "Claims should be supported by available evidence.")


def evaluate_actionability(
    output_text: str,
    frame_actionability: ActionClass | None = None,
    has_production_keywords: bool = False,
    has_deployment_references: bool = False,
    has_recommendation_language: bool = False,
    has_safety_critical_terms: bool = False,
    evidence_score: float = 0.0,
) -> ActionabilityVerdict:
    """Evaluate whether an output meets the evidence bar for its actionability class.

    Args:
        output_text: The model output to evaluate.
        frame_actionability: Override actionability from the epistemic frame.
        evidence_score: 0.0 (no evidence) to 1.0 (fully supported).

    Returns an ActionabilityVerdict with the decision.
    """
    action_class = frame_actionability or _detect_action_class(
        output_text,
        has_production_keywords=has_production_keywords,
        has_deployment_references=has_deployment_references,
        has_recommendation_language=has_recommendation_language,
        has_safety_critical_terms=has_safety_critical_terms,
    )

    min_evidence = _min_evidence_for_action(action_class)

    if action_class == "explanatory":
        return ActionabilityVerdict(
            decision=ActionabilityDecision.ALLOW,
            action_class=action_class,
            reason=f"Explanatory output. {min_evidence}",
        )

    if action_class == "actionable":
        if evidence_score >= 0.5:
            return ActionabilityVerdict(
                decision=ActionabilityDecision.ALLOW,
                action_class=action_class,
                reason=f"Actionable output with sufficient evidence (score={evidence_score:.2f}). {min_evidence}",
            )
        return ActionabilityVerdict(
            decision=ActionabilityDecision.REQUIRE_MORE_EVIDENCE,
            action_class=action_class,
            reason=f"Actionable output needs more evidence (score={evidence_score:.2f}). {min_evidence}",
        )

    if action_class == "critical":
        if evidence_score >= 0.8:
            return ActionabilityVerdict(
                decision=ActionabilityDecision.ESCALATE_TO_HUMAN,
                action_class=action_class,
                requires_human_review=True,
                reason=f"Critical output with strong evidence (score={evidence_score:.2f}). Escalating to human review.",
            )
        if evidence_score >= 0.5:
            return ActionabilityVerdict(
                decision=ActionabilityDecision.ESCALATE_TO_HUMAN,
                action_class=action_class,
                requires_human_review=True,
                reason=f"Critical output with partial evidence (score={evidence_score:.2f}). Escalating to human review.",
            )
        return ActionabilityVerdict(
            decision=ActionabilityDecision.BLOCK,
            action_class=action_class,
            reason=f"Critical output with insufficient evidence (score={evidence_score:.2f}). Blocked.",
        )

    return ActionabilityVerdict(
        decision=ActionabilityDecision.ALLOW,
        action_class="explanatory",
        reason="Default allow for unclassified output.",
    )
