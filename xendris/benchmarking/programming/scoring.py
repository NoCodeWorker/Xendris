"""Scoring rules for Programming Reliability Benchmark v0.1."""

from __future__ import annotations

from .types import ProgrammingRunResult, ProgrammingSample


def score_programming_result(result: ProgrammingRunResult, sample: ProgrammingSample) -> float:
    """Score one programming benchmark result conservatively."""
    del sample
    if result.security_risk:
        return 0.0
    if not result.contract_preserved:
        return 0.0
    if result.performance_regression:
        return 0.0
    if result.reason == "PRODUCTION_OVERCLAIM":
        return 0.0
    if result.runtime_error:
        if result.reason == "PROBLEM_DETECTED_NOT_FIXED":
            return 0.4
        return 0.0
    if result.tests_passed and result.contract_preserved:
        if result.reason == "MINOR_LIMITATIONS":
            return 0.8
        return 1.0
    if result.reason == "INCOMPLETE_SOLUTION":
        return 0.6
    if result.reason == "PROBLEM_DETECTED_NOT_FIXED":
        return 0.4
    return 0.0
