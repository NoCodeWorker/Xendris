"""Benchmark alignment assessment for v3.9."""

from __future__ import annotations

from phyng.source_pressure_decision.schemas import (
    BenchmarkAlignmentRecord,
    ExtractPressureRecord,
)


def assess_benchmark_alignment(records: list[ExtractPressureRecord]) -> BenchmarkAlignmentRecord:
    """Assess whether extracts provide benchmark-relevant alignment."""
    benchmark_extracts = [
        r.extract_id for r in records if r.pressure_class == "SUPPORTS_BENCHMARK_ALIGNMENT"
    ]
    observable_extracts = [
        r.extract_id for r in records if r.pressure_class == "SUPPORTS_OBSERVABLE_ONLY"
    ]
    range_extracts = [
        r.extract_id for r in records
        if r.pressure_class == "SUPPORTS_BENCHMARK_ALIGNMENT"
        and _has_range_data(r.exact_text.lower())
    ]

    missing = _missing_fields(records)
    decision = _benchmark_decision(benchmark_extracts, observable_extracts, range_extracts, missing)
    limitations = _limitations(decision, missing)

    return BenchmarkAlignmentRecord(
        benchmark_extracts=benchmark_extracts,
        observable_alignment=observable_extracts,
        range_alignment=range_extracts,
        missing_benchmark_fields=missing,
        benchmark_decision=decision,
        limitations=limitations,
    )


def _has_range_data(text: str) -> bool:
    import re
    return bool(re.search(r"\d", text)) and any(
        term in text for term in ["mass", "time", "temperature", "pressure", "mbar", "amu", "nm", "regime"]
    )


def _missing_fields(records: list[ExtractPressureRecord]) -> list[str]:
    """Check which benchmark fields are absent from any extract."""
    all_text = " ".join(r.exact_text.lower() for r in records if r.pressure_class == "SUPPORTS_BENCHMARK_ALIGNMENT")
    missing: list[str] = []
    for field in ["mass", "time", "temperature", "pressure", "visibility"]:
        if field not in all_text:
            missing.append(field)
    return missing


def _benchmark_decision(
    benchmark: list[str],
    observable: list[str],
    range_data: list[str],
    missing: list[str],
) -> str:
    if not benchmark:
        return "NO_BENCHMARK_EXTRACTS"
    if range_data and observable:
        return "BENCHMARK_WITH_OBSERVABLE_AND_RANGE"
    if range_data:
        return "BENCHMARK_WITH_RANGE_ONLY"
    if observable:
        return "BENCHMARK_WITH_OBSERVABLE_ONLY"
    return "BENCHMARK_EXTRACTS_FOUND_INCOMPLETE"


def _limitations(decision: str, missing: list[str]) -> list[str]:
    limits: list[str] = [
        "Benchmark relevance does not validate physics.",
        "Benchmark alignment is necessary but not sufficient for model comparison.",
    ]
    if missing:
        limits.append(f"Missing benchmark fields: {', '.join(missing)}.")
    return limits
