"""Benchmark comparability pressure for PHI_GRADIENT."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.source_pressure.schemas import BenchmarkPressureRecord, PhiGradientBenchmarkPressureResult


def assess_benchmark_pressure(record: BenchmarkPressureRecord) -> PhiGradientBenchmarkPressureResult:
    required_ranges = {"m_kg", "L_m", "t_s"}
    has_required_ranges = required_ranges.issubset(record.parameter_ranges)
    has_required_fields = bool(
        record.observable
        and has_required_ranges
        and record.has_visibility_or_decoherence_measure
        and record.has_environmental_baseline
        and record.citation_or_path
    )
    if not record.comparable_to_phi_gradient or not has_required_fields:
        status = "BENCHMARK_REJECTED_NOT_COMPARABLE"
        counts = False
        reasons = ["Benchmark lacks comparable observable, ranges, baseline, measure or citation/path."]
    elif record.status == "CONTRADICTS" or "contradicts candidate" in {item.lower() for item in record.limitations}:
        status = "BENCHMARK_CONTRADICTS_CANDIDATE"
        counts = False
        reasons = ["Benchmark contradicts candidate component or required parameter range."]
    elif record.supports_candidate_component and record.constrains_alpha:
        status = "BENCHMARK_SUPPORTS_CANDIDATE_LIMITED"
        counts = True
        reasons = ["Benchmark is comparable, supports candidate component and constrains alpha."]
    elif record.supports_candidate_component:
        status = "BENCHMARK_SUPPORTS_COMPONENT_LIMITED"
        counts = True
        reasons = ["Benchmark supports component but does not constrain alpha."]
    elif record.constrains_alpha:
        status = "BENCHMARK_CONSTRAINS_ALPHA"
        counts = True
        reasons = ["Benchmark constrains alpha-like parameter."]
    elif record.supports_baseline:
        status = "BENCHMARK_BASELINE_ONLY"
        counts = False
        reasons = ["Benchmark supports baseline only."]
    else:
        status = "BENCHMARK_SUPPORTS_OBSERVABLE_ONLY"
        counts = False
        reasons = ["Benchmark supports observable only."]

    return PhiGradientBenchmarkPressureResult(
        benchmark_id=record.benchmark_id,
        status=status,
        counts_as_benchmark_support=counts and status == "BENCHMARK_SUPPORTS_CANDIDATE_LIMITED",
        canonical_status=normalize_status(
            "PHI_GRADIENT_BENCHMARK_DATA_FOUND" if counts and status == "BENCHMARK_SUPPORTS_CANDIDATE_LIMITED" else "PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE",
            domain="source_pressure",
        ),
        reasons=reasons,
        limitations=list(record.limitations),
    )
