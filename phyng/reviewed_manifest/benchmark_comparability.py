"""Benchmark comparability for reviewed manifest extract packs."""

from __future__ import annotations

from phyng.reviewed_manifest.schemas import ReviewedBenchmarkComparabilityResult, ReviewedSlotCoverageMatrix


def assess_reviewed_benchmark_comparability(
    coverage: ReviewedSlotCoverageMatrix,
) -> ReviewedBenchmarkComparabilityResult:
    comparable = [
        record for record in coverage.records
        if record.slot_id == "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"
        and record.coverage_status == "SLOT_BENCHMARK_COMPARABLE"
    ]
    if comparable:
        return ReviewedBenchmarkComparabilityResult(
            status="BENCHMARK_COMPARABLE_REAL_RECORD_FOUND",
            comparable_records=len(comparable),
        )
    return ReviewedBenchmarkComparabilityResult(
        status="BENCHMARK_COMPARABLE_RECORD_MISSING",
        comparable_records=0,
        missing_requirements=[
            "observable match",
            "mass range",
            "length/separation range",
            "time range",
            "visibility/decoherence measure",
        ],
    )
