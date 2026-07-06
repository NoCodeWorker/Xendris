"""ContrarianGuard — generates counterarguments when sycophancy is detected."""
from __future__ import annotations

from xendris.core.council.models import GuardResult, GuardOutput


class ContrarianGuard:
    """Validates that sycophantic answers include a counterargument."""

    MIN_COUNTERARGUMENT_LENGTH = 60

    COUNTERARGUMENT_MARKERS = [
        "however",
        "but",
        "on the other hand",
        "counterargument",
        "alternative view",
        "opposing perspective",
        "critical consideration",
        "it should also be noted",
        "a potential drawback",
        "one could argue",
        "an alternative interpretation",
    ]

    def evaluate(self, user_input: str, model_output: str, sycophancy_flagged: bool = False) -> GuardOutput:
        if not sycophancy_flagged:
            return GuardOutput(
                guard_name="ContrarianGuard",
                result=GuardResult.PASS,
                reason="No sycophancy flagged, counterargument not required",
            )

        lower = model_output.lower()
        has_counterargument = any(marker in lower for marker in self.COUNTERARGUMENT_MARKERS)
        is_long_enough = len(model_output.strip()) >= self.MIN_COUNTERARGUMENT_LENGTH

        if has_counterargument and is_long_enough:
            return GuardOutput(
                guard_name="ContrarianGuard",
                result=GuardResult.PASS,
                reason="Counterargument present and substantive",
                details={"has_counterargument": True, "is_long_enough": True},
            )

        reasons = []
        if not has_counterargument:
            reasons.append("No counterargument found in sycophantic response")
        if not is_long_enough:
            reasons.append(f"Response too short ({len(model_output.strip())} < {self.MIN_COUNTERARGUMENT_LENGTH})")

        return GuardOutput(
            guard_name="ContrarianGuard",
            result=GuardResult.FLAG,
            reason="; ".join(reasons),
            details={
                "has_counterargument": has_counterargument,
                "is_long_enough": is_long_enough,
            },
        )
