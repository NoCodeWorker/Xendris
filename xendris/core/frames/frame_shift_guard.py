"""FrameShiftGuard for Xendris Epistemic Frame Layer.

Detects attempts to shift between epistemic frames without providing
evidence bridges. A shift from a low-evidence frame (e.g., HYPOTHESIS)
to a high-evidence frame (e.g., PRODUCTION) requires explicit bridging
evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .epistemic_frame import EpistemicFrame


class FrameShiftDecision(Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_WARNING = "ALLOW_WITH_WARNING"
    REQUIRE_EVIDENCE_BRIDGE = "REQUIRE_EVIDENCE_BRIDGE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class FrameShiftVerdict:
    decision: FrameShiftDecision
    source_frame: str
    target_frame: str
    reason: str
    bridge_requirements: tuple[str, ...] = ()


_EVIDENCE_BRIDGE_TYPES = {
    "empirical_study": "An empirical study validating the claim in the target context.",
    "external_audit": "An independent audit of the system's behavior.",
    "deployment_logs": "Production deployment logs showing real-world performance.",
    "benchmark_results": "Benchmark results under the target evaluation protocol.",
    "expert_review": "Expert review attesting to the validity of the shift.",
    "formal_proof": "A formal mathematical or logical proof.",
    "user_study": "A user study demonstrating real-world utility.",
    "ablation_analysis": "An ablation study isolating the claimed effect.",
}


def _actionability_distance(source: EpistemicFrame, target: EpistemicFrame) -> int:
    levels = {"critical": 3, "actionable": 2, "explanatory": 1}
    s = levels.get(source.actionability, 0)
    t = levels.get(target.actionability, 0)
    return t - s


def evaluate_frame_shift(
    source: EpistemicFrame | None,
    target: EpistemicFrame,
    has_evidence_bridge: bool = False,
    bridge_type: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> FrameShiftVerdict:
    """Evaluate whether a frame shift is allowed.

    Args:
        source: The current epistemic frame, or None if no prior frame.
        target: The target epistemic frame.
        has_evidence_bridge: Whether bridging evidence has been provided.
        bridge_type: Type of evidence bridge provided.

    Returns a FrameShiftVerdict.
    """
    if source is None:
        return FrameShiftVerdict(
            decision=FrameShiftDecision.ALLOW,
            source_frame="NONE",
            target_frame=target.profile.name,
            reason="No prior frame; shifting to initial frame is always allowed.",
        )

    if source == target:
        return FrameShiftVerdict(
            decision=FrameShiftDecision.ALLOW,
            source_frame=source.profile.name,
            target_frame=target.profile.name,
            reason="Same frame; no shift required.",
        )

    distance = _actionability_distance(source, target)

    if distance <= 0:
        return FrameShiftVerdict(
            decision=FrameShiftDecision.ALLOW,
            source_frame=source.profile.name,
            target_frame=target.profile.name,
            reason=f"Shift from {source.profile.name} (actionability={source.actionability}) "
                   f"to {target.profile.name} (actionability={target.actionability}) "
                   f"reduces or maintains actionability. Allowed.",
        )

    bridge_requirements: list[str] = []

    if distance == 1:
        if has_evidence_bridge:
            return FrameShiftVerdict(
                decision=FrameShiftDecision.ALLOW_WITH_WARNING,
                source_frame=source.profile.name,
                target_frame=target.profile.name,
                reason=f"Shift from {source.profile.name} to {target.profile.name} "
                       f"with evidence bridge ({bridge_type or 'unknown'}). Allowed with warning.",
            )
        bridge_requirements.extend(_EVIDENCE_BRIDGE_TYPES.get(t, t) for t in ["benchmark_results", "empirical_study"])
        return FrameShiftVerdict(
            decision=FrameShiftDecision.REQUIRE_EVIDENCE_BRIDGE,
            source_frame=source.profile.name,
            target_frame=target.profile.name,
            reason=f"Cannot shift from {source.profile.name} (explanatory/actionable) "
                   f"to {target.profile.name} (actionable/critical) without evidence bridge.",
            bridge_requirements=tuple(bridge_requirements),
        )

    if distance >= 2:
        if has_evidence_bridge and bridge_type in ("external_audit", "deployment_logs", "formal_proof"):
            return FrameShiftVerdict(
                decision=FrameShiftDecision.ALLOW_WITH_WARNING,
                source_frame=source.profile.name,
                target_frame=target.profile.name,
                reason=f"Shift from {source.profile.name} to {target.profile.name} "
                       f"with strong evidence bridge ({bridge_type}). Allowed with warning.",
            )
        bridge_requirements.extend(
            _EVIDENCE_BRIDGE_TYPES.get(t, t) for t in ["external_audit", "deployment_logs", "formal_proof"]
        )
        return FrameShiftVerdict(
            decision=FrameShiftDecision.BLOCK if not has_evidence_bridge else FrameShiftDecision.REQUIRE_EVIDENCE_BRIDGE,
            source_frame=source.profile.name,
            target_frame=target.profile.name,
            reason=f"Cannot shift from {source.profile.name} to {target.profile.name}: "
                   f"actionability distance is {distance}. Strong evidence bridge required.",
            bridge_requirements=tuple(bridge_requirements),
        )

    return FrameShiftVerdict(
        decision=FrameShiftDecision.ALLOW,
        source_frame=source.profile.name,
        target_frame=target.profile.name,
        reason=f"Shift from {source.profile.name} to {target.profile.name} allowed.",
    )
