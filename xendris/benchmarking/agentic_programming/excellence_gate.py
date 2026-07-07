from __future__ import annotations

import enum


class ExcellenceGateDecision(enum.Enum):
    READY_FOR_INTERPRETATION = "READY_FOR_INTERPRETATION"
    WARNINGS_PRESENT = "WARNINGS_PRESENT"
    BLOCKED_FOR_INTERPRETATION = "BLOCKED_FOR_INTERPRETATION"


EXCELLENCE_THRESHOLD_READY = 0.80
EXCELLENCE_THRESHOLD_BLOCKED = 0.40


def evaluate_excellence_gate(
    scores: dict[str, dict[str, float]],
) -> dict[str, str]:
    decisions: dict[str, str] = {}
    for variant, data in scores.items():
        score = data["total_score"]
        pass_rate = data["pass_rate"]

        if score >= EXCELLENCE_THRESHOLD_READY and pass_rate >= 0.60:
            decisions[variant] = ExcellenceGateDecision.READY_FOR_INTERPRETATION.value
        elif score < EXCELLENCE_THRESHOLD_BLOCKED or pass_rate < 0.20:
            decisions[variant] = ExcellenceGateDecision.BLOCKED_FOR_INTERPRETATION.value
        else:
            decisions[variant] = ExcellenceGateDecision.WARNINGS_PRESENT.value

    return decisions
