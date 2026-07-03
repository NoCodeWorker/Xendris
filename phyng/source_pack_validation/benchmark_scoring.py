"""Benchmark comparability scoring for source-pack validation."""

from __future__ import annotations

from phyng.source_pack_validation.schemas import SourcePackBenchmarkScoringResult, SourcePackExtractValidationResult


def score_benchmark_comparability(results: list[SourcePackExtractValidationResult]) -> SourcePackBenchmarkScoringResult:
    comparable = [result for result in results if result.status == "EXTRACT_VALID_PROVIDES_BENCHMARK_DATA"]
    if comparable:
        return SourcePackBenchmarkScoringResult(
            status="BENCHMARK_COMPARABLE_REAL_RECORD_FOUND",
            benchmark_comparable_count=len(comparable),
            benchmark_score=1.0,
        )
    return SourcePackBenchmarkScoringResult(
        status="BENCHMARK_COMPARABLE_RECORD_MISSING",
        benchmark_comparable_count=0,
        benchmark_score=0.0,
        missing_requirements=["observable", "mass range", "length/separation range", "time range", "visibility/decoherence measure", "limitations"],
    )
