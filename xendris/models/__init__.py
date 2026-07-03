"""
xendris.models — Typed data contracts shared across all Xendris modules.

Aggregates Pydantic models from both the benchmark and frontera_c layers
so callers can import everything from one place.

Usage:
    from xendris.models import BenchmarkCase, ModelResponse, Claim
"""

# Frontera C claim types
from xendris.frontera_c import Claim  # noqa: F401

# Benchmark types
from xendris.benchmarks.false_formality.core.types import (  # noqa: F401
    BenchmarkCase,
    ModelResponse,
    RubricScore,
    BenchmarkResult,
    BenchmarkSummary,
)

__all__ = [
    "Claim",
    "BenchmarkCase",
    "ModelResponse",
    "RubricScore",
    "BenchmarkResult",
    "BenchmarkSummary",
]
