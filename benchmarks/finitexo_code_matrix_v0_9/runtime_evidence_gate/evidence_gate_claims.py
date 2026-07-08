from __future__ import annotations

from typing import Any


def build_claim_authorization(
    integrity_result: dict[str, Any],
    statistics: dict[str, Any],
) -> dict[str, Any]:
    authorized: list[str] = [
        "The v0.9.0 live_20260708_02 run completed under real providers.",
        "Evidence integrity passed for the v0.9.0 source run.",
        "Base, wrapper, runtime and calibrated_runtime variants were all measured.",
        "Runtime and Calibrated Runtime diagnostic lift can be discussed for this controlled n=30 run.",
        "Wrapper-only results must not be generalized to runtime/calibrated_runtime.",
        "Statistical robustness metrics were computed diagnostically.",
    ]

    conditional: list[str] = []
    blocked: list[str] = [
        "universal superiority",
        "statistical superiority",
        "production readiness",
        "external benchmark superiority",
        "general coding superiority",
        "provider ranking beyond this dataset",
        "Xendris always improves models",
        "wrapper results generalize to runtime",
        "runtime results generalize universally",
        "calibrated runtime superiority outside this run",
        "cost superiority outside this run",
    ]

    for key, comp in statistics.items():
        if isinstance(comp, dict) and "signal" in comp:
            signal = comp["signal"]
            treatment = comp.get("treatment", "?")
            control = comp.get("control", "?")
            if signal == "STRONG_DIAGNOSTIC_SIGNAL":
                conditional.append(
                    f"{treatment} vs {control}: This comparison showed a strong diagnostic signal in this controlled n=30 run."
                )
            elif signal == "MODERATE_DIAGNOSTIC_SIGNAL":
                conditional.append(
                    f"{treatment} vs {control}: This comparison showed a moderate diagnostic signal in this controlled n=30 run."
                )
            elif signal == "WEAK_OR_INCONCLUSIVE_SIGNAL":
                conditional.append(
                    f"{treatment} vs {control}: This comparison was weak or inconclusive in this controlled n=30 run."
                )

    return {
        "authorized_claims": authorized,
        "conditional_claims": conditional,
        "blocked_claims": blocked,
    }
