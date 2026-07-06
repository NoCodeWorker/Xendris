"""Domain and execution-mode primitives for intervention calibration.

This module is experimental. It only defines deterministic labels used by
policy code. It does not call models, change responses, or validate benchmark
quality.
"""

from __future__ import annotations

from enum import Enum


class ExecutionMode(str, Enum):
    """Operational context in which an intervention would be applied."""

    EXPLORATION = "EXPLORATION"
    BENCHMARK_EXECUTION = "BENCHMARK_EXECUTION"
    CODE_SANDBOX = "CODE_SANDBOX"
    PRODUCTION = "PRODUCTION"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    PUBLIC_CLAIM = "PUBLIC_CLAIM"


class Domain(str, Enum):
    """High-level domain where calibration policy is evaluated."""

    GENERAL = "GENERAL"
    PROGRAMMING = "PROGRAMMING"
    BENCHMARK = "BENCHMARK"
    TRUST_TRAPS = "TRUST_TRAPS"
    PRODUCT_STRATEGY = "PRODUCT_STRATEGY"
    SAFETY_SECURITY = "SAFETY_SECURITY"


class ProgrammingCategory(str, Enum):
    """Programming Reliability benchmark category labels."""

    API_CONTRACTS = "API_CONTRACTS"
    BUG_FIXING = "BUG_FIXING"
    EDGE_CASES = "EDGE_CASES"
    NORMAL_CONTROL = "NORMAL_CONTROL"
    PERFORMANCE = "PERFORMANCE"
    REFACTOR_SAFETY = "REFACTOR_SAFETY"
    SECURITY_BASICS = "SECURITY_BASICS"
    UNIT_TESTS = "UNIT_TESTS"


__all__ = ["Domain", "ExecutionMode", "ProgrammingCategory"]
