"""RuntimePolicy logic for determining final query decisions."""

from __future__ import annotations

from typing import Any
from xendris.core.sectors.sector import EpistemicSector


class RuntimePolicy:
    """Evaluates router and guard outcomes to make a final logical decision."""

    @staticmethod
    def evaluate_decision(
        route_decision: Any,
        boundary_decisions: list[Any],
        transition_decisions: list[Any],
        consistency_decisions: list[Any],
    ) -> tuple[str, str, list[str]]:
        """Evaluate outcomes and return (final_decision, reason, accumulated_limitations)."""
        limitations: list[str] = []

        # 1. Router overrides
        route_status = getattr(route_decision, "decision", "BLOCK")
        if route_status == "NO_SAFE_MODEL_AVAILABLE":
            return "NO_SAFE_MODEL_AVAILABLE", "No safe model could be routed for constraints.", []
        if route_status == "REQUIRE_HUMAN_REVIEW":
            return "HUMAN_REVIEW_REQUIRED", "High-risk routing requires human review.", ["Manual Review Routing Gate"]

        # Collect routing limitations
        route_limits = getattr(route_decision, "limitations", ())
        limitations.extend(route_limits)

        # 2. Block/Human Review overrides in guards
        for b in boundary_decisions:
            dec = getattr(b, "decision", "BLOCK")
            if dec == "BLOCKED" or dec == "BLOCK":
                reason = getattr(b, "reason", "Claim boundary blocked.")
                return "BLOCKED", f"Contamination guard blocked: {reason}", []
            if dec == "HUMAN_REVIEW_REQUIRED" or dec == "NEEDS_HUMAN_REVIEW":
                return "HUMAN_REVIEW_REQUIRED", "Claim boundary requires human review.", ["Boundary review required"]

        for t in transition_decisions:
            dec = getattr(t, "decision", "BLOCK")
            if dec == "BLOCKED" or dec == "BLOCK":
                reason = getattr(t, "reason", "Sector transition blocked.")
                return "BLOCKED", f"Sector engine blocked: {reason}", []
            if dec == "HUMAN_REVIEW_REQUIRED" or dec == "NEEDS_HUMAN_REVIEW":
                return "HUMAN_REVIEW_REQUIRED", "Sector transition requires human review.", ["Sector review required"]

        for c in consistency_decisions:
            dec = getattr(c, "decision", "BLOCK")
            if dec == "BLOCKED" or dec == "BLOCK":
                reason = getattr(c, "reason", "Consistency gate blocked.")
                return "BLOCKED", f"Consistency gate blocked: {reason}", []
            if dec == "HUMAN_REVIEW_REQUIRED" or dec == "NEEDS_HUMAN_REVIEW":
                return "HUMAN_REVIEW_REQUIRED", "Consistency gate requires human review.", ["Consistency review required"]

        # Collect guard limitations
        for b in boundary_decisions:
            limitations.extend(getattr(b, "limitations", ()))
            limitations.extend(getattr(b, "required_evidence", ()))

        for t in transition_decisions:
            limitations.extend(getattr(t, "limitations", ()))
            limitations.extend(getattr(t, "required_evidence", ()))

        for c in consistency_decisions:
            limitations.extend(getattr(c, "limitations", ()))
            limitations.extend(getattr(c, "required_evidence", ()))

        # 3. Assess status/limitations
        guard_decisions_with_limits = (
            any(getattr(b, "decision", "") in ("ALLOW_WITH_LIMITATIONS", "APPROVED_WITH_LIMITATIONS") for b in boundary_decisions)
            or any(getattr(t, "decision", "") in ("ALLOW_WITH_LIMITATIONS", "APPROVED_WITH_LIMITATIONS") for t in transition_decisions)
            or any(getattr(c, "decision", "") in ("ALLOW_WITH_LIMITATIONS", "APPROVED_WITH_LIMITATIONS") for c in consistency_decisions)
        )
        
        guard_limitations: list[str] = []
        for b in boundary_decisions:
            guard_limitations.extend(getattr(b, "limitations", ()))
            guard_limitations.extend(getattr(b, "required_evidence", ()))
        for t in transition_decisions:
            guard_limitations.extend(getattr(t, "limitations", ()))
            guard_limitations.extend(getattr(t, "required_evidence", ()))
        for c in consistency_decisions:
            guard_limitations.extend(getattr(c, "limitations", ()))
            guard_limitations.extend(getattr(c, "required_evidence", ()))

        has_limitations = guard_decisions_with_limits or len(guard_limitations) > 0

        # 4. Assess sector-level hypothesis
        is_hypothesis = any(
            getattr(t, "target_sector", None) in (EpistemicSector.HYPOTHESIS, "HYPOTHESIS", "CREATIVE")
            for t in transition_decisions
        ) or any(
            getattr(t, "decision", "") in ("ALLOW_AS_HYPOTHESIS", "APPROVED_AS_HYPOTHESIS")
            for t in transition_decisions
        )

        unique_limits = sorted(list(set(limitations)))

        if is_hypothesis:
            return "ANSWER_AS_HYPOTHESIS", "Output admitted within exploratory hypothesis sector.", unique_limits

        if has_limitations:
            return "ANSWER_WITH_LIMITATIONS", "Output allowed under explicit security compuertas.", unique_limits

        return "ANSWER", "All trust modules verified content successfully.", unique_limits
