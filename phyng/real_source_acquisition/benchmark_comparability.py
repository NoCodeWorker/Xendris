"""Benchmark comparability for acquired real sources."""

from __future__ import annotations

from phyng.real_source_acquisition.schemas import BenchmarkComparabilityResult, SlotCoverageMatrix


def assess_benchmark_comparability(coverage: SlotCoverageMatrix) -> BenchmarkComparabilityResult:
    comparable = [
        record
        for record in coverage.records
        if record.slot_id == "SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"
        and record.coverage_status == "SLOT_BENCHMARK_COMPARABLE"
    ]
    if comparable:
        return BenchmarkComparabilityResult(status="BENCHMARK_COMPARABLE_REAL_RECORD_FOUND", comparable_records=len(comparable))
    return BenchmarkComparabilityResult(
        status="BENCHMARK_COMPARABLE_RECORD_MISSING",
        comparable_records=0,
        missing_requirements=["observable", "mass range", "length/separation range", "time range", "visibility/decoherence measure"],
    )
