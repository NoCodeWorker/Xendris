"""Backward-compatible import wrapper for Benchmark Excellence Gate."""

from __future__ import annotations

from .excellence_gate import (
    BenchmarkExcellenceAssessment,
    BenchmarkExcellenceDecision,
    BenchmarkExcellenceIssue,
    BenchmarkExcellenceIssueSeverity,
    assess_benchmark_excellence,
)

BenchmarkExcellenceSeverity = BenchmarkExcellenceIssueSeverity

__all__ = [
    "BenchmarkExcellenceAssessment",
    "BenchmarkExcellenceDecision",
    "BenchmarkExcellenceIssue",
    "BenchmarkExcellenceIssueSeverity",
    "BenchmarkExcellenceSeverity",
    "assess_benchmark_excellence",
]
