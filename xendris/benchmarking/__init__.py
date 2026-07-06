"""Xendris A/B Benchmarking Suite.

Exposes run, score, summarize, and JSONL serialization helpers.
"""

from __future__ import annotations

from .types import ABComparisonResult, ABRunSummary, BenchmarkSample, SystemRunResult
from .ab_runner import run_ab_benchmark, summarize_ab_results
from .ablation import (
    AblationRunResult,
    AblationVariant,
    compute_ablation_fingerprint,
    run_ablation_benchmark,
    summarize_ablation_results,
    write_ablation_results_json,
    write_ablation_results_jsonl,
)
from .frontier_gap import (
    FrontierGapComparison,
    FrontierGapSystemResult,
    compute_frontier_gap,
    write_frontier_gap_summary_json,
)
from .excellence_gate import (
    BenchmarkExcellenceAssessment,
    BenchmarkExcellenceDecision,
    BenchmarkExcellenceIssue,
    BenchmarkExcellenceIssueSeverity,
    assess_benchmark_excellence,
)
from .calibration_ablation_gate import (
    CalibrationAblationGateAssessment,
    CalibrationAblationGateIssue,
    assess_programming_calibration_ablation,
)
from .evidence_registry import (
    BenchmarkEvidenceRecord,
    BenchmarkEvidenceRegistry,
    build_benchmark_evidence_registry,
    render_benchmark_evidence_registry_markdown,
    write_benchmark_evidence_registry_json,
    write_benchmark_evidence_registry_markdown,
)
from .scoring import score_result_against_expected
from .export_jsonl import read_ab_results_jsonl, write_ab_results_jsonl, write_ab_summary_json

__all__ = [
    "AblationRunResult",
    "AblationVariant",
    "BenchmarkExcellenceAssessment",
    "BenchmarkExcellenceDecision",
    "BenchmarkExcellenceIssue",
    "BenchmarkExcellenceIssueSeverity",
    "BenchmarkEvidenceRecord",
    "BenchmarkEvidenceRegistry",
    "BenchmarkSample",
    "CalibrationAblationGateAssessment",
    "CalibrationAblationGateIssue",
    "FrontierGapComparison",
    "FrontierGapSystemResult",
    "SystemRunResult",
    "ABComparisonResult",
    "ABRunSummary",
    "assess_benchmark_excellence",
    "assess_programming_calibration_ablation",
    "build_benchmark_evidence_registry",
    "compute_ablation_fingerprint",
    "compute_frontier_gap",
    "run_ablation_benchmark",
    "run_ab_benchmark",
    "summarize_ablation_results",
    "summarize_ab_results",
    "score_result_against_expected",
    "write_ablation_results_json",
    "write_ablation_results_jsonl",
    "write_ab_results_jsonl",
    "write_benchmark_evidence_registry_json",
    "write_benchmark_evidence_registry_markdown",
    "write_frontier_gap_summary_json",
    "render_benchmark_evidence_registry_markdown",
    "read_ab_results_jsonl",
    "write_ab_summary_json",
]
