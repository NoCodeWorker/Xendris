"""Strong-baseline comparison for Finitexo Code Matrix v0.3."""

from __future__ import annotations

from typing import Any, Mapping

Decision = str


def _score(result: Mapping[str, Any], key: str) -> float:
    value = result.get(key, {})
    if isinstance(value, Mapping):
        return float(value.get("verified_success_count", 0))
    return float(result.get(f"{key}_verified_success_count", 0))


def _mean(result: Mapping[str, Any], key: str) -> float:
    value = result.get(key, {})
    if isinstance(value, Mapping):
        return float(value.get("mean_raw_score", value.get("average_score", 0.0)))
    return float(result.get(f"{key}_mean_raw_score", 0.0))


def compare_baselines(summary: Mapping[str, Any]) -> dict[str, Any]:
    """Compare strong non-system baseline to system variants conservatively."""

    blockers = list(summary.get("blockers", []))
    if summary.get("adversarial_decision") == "BLOCKED_FOR_INTERPRETATION":
        blockers.append("adversarial_blocked")
    if summary.get("blind_scoring_decision") == "FAILED":
        blockers.append("blind_scoring_failed")
    if not summary.get("strong_non_xendris_agent_available", False):
        blockers.append("strong_baseline_unavailable")
    if blockers:
        return {
            "decision": "BLOCKED_FOR_INTERPRETATION",
            "h0_status": "LIVE",
            "blockers": blockers,
            "interpretation": "Blocked comparison; no positive evidence may be admitted.",
        }

    strong = _score(summary, "strong_non_xendris_agent")
    x_agent = _score(summary, "xendris_agent")
    x_calibrated = _score(summary, "xendris_calibrated_agent")
    best_x = max(x_agent, x_calibrated)
    strong_mean = _mean(summary, "strong_non_xendris_agent")
    best_x_mean = max(_mean(summary, "xendris_agent"), _mean(summary, "xendris_calibrated_agent"))

    if strong > best_x:
        decision = "BASELINE_OUTPERFORMED_XENDRIS"
        interpretation = "Strong baseline outperformed the system variants under this benchmark."
    elif abs(best_x - strong) <= 1:
        decision = "BASELINE_MATCHED_XENDRIS"
        interpretation = "Strong baseline matched the system within the v0.3 tolerance."
    elif best_x > strong and best_x_mean > strong_mean:
        decision = "XENDRIS_ADVANTAGE_OBSERVED_INTERNAL_ONLY"
        interpretation = "System variants exceeded the strong baseline under this internal protocol only."
    else:
        decision = "NO_CLEAR_XENDRIS_ADVANTAGE"
        interpretation = "The evidence does not show a clear advantage."

    return {
        "decision": decision,
        "h0_status": "LIVE",
        "strong_non_xendris_verified_successes": strong,
        "best_xendris_verified_successes": best_x,
        "strong_non_xendris_mean_raw_score": strong_mean,
        "best_xendris_mean_raw_score": best_x_mean,
        "blockers": [],
        "interpretation": interpretation,
    }

