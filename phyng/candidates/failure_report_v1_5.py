"""
Phygn v1.5 — Failure Report Evaluator

Evaluates v1.5-specific failure conditions for the synthetic benchmark.
"""

from __future__ import annotations


def evaluate_v1_5_failure_conditions(
    max_abs_delta: float,
    epsilon_exp: float | None,
    y_true: list[float] | None,
    alpha_min: float | None,
    detectability_status: str,
) -> list[str]:
    """
    Evaluate v1.5 failure conditions.

    Returns a list of triggered failure condition codes.

    Failure codes:
        FAIL_UNDETECTABLE_DELTA
        FAIL_NO_BENCHMARK
        FAIL_NO_SOURCE_SUPPORT
        REQUIRES_UNPHYSICAL_ALPHA
    """
    failures: list[str] = []

    # 1. Undetectable under declared threshold
    if detectability_status == "UNDETECTABLE_SYNTHETIC_DELTA":
        failures.append("FAIL_UNDETECTABLE_DELTA")

    # 2. No experimental y_true → benchmark not computable
    if y_true is None:
        failures.append("FAIL_NO_BENCHMARK")

    # 3. No source support (always true for synthetic benchmark of this candidate)
    # This will be explicitly set by the campaign; default to triggered for toy context
    failures.append("FAIL_NO_SOURCE_SUPPORT")

    # 4. Alpha required is unphysical
    if alpha_min is not None and alpha_min > 1e35:
        failures.append("REQUIRES_UNPHYSICAL_ALPHA")

    return failures


def classify_candidate_survival(triggered_failures: list[str]) -> str:
    """
    Classify candidate survival based on triggered failure conditions.

    Statuses:
        SURVIVES_AS_TOY_NEGATIVE_CONTROL
        SURVIVES_PENDING_BENCHMARK
        FAILS_DEFAULT_DETECTABILITY
        FAILS_PARAMETER_REASONABLENESS
        BLOCKED_PHYSICAL_INTERPRETATION
    """
    if "REQUIRES_UNPHYSICAL_ALPHA" in triggered_failures:
        return "FAILS_PARAMETER_REASONABLENESS"

    if "FAIL_UNDETECTABLE_DELTA" in triggered_failures:
        if "FAIL_NO_SOURCE_SUPPORT" in triggered_failures:
            return "SURVIVES_AS_TOY_NEGATIVE_CONTROL"
        return "FAILS_DEFAULT_DETECTABILITY"

    if "FAIL_NO_BENCHMARK" in triggered_failures:
        return "SURVIVES_PENDING_BENCHMARK"

    if "FAIL_NO_SOURCE_SUPPORT" in triggered_failures:
        return "BLOCKED_PHYSICAL_INTERPRETATION"

    return "SURVIVES_AS_TOY_NEGATIVE_CONTROL"
