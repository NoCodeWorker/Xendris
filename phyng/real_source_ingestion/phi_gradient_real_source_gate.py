"""PHI_GRADIENT real source gate."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.real_source_ingestion.extract_validation import validate_real_source_extract
from phyng.real_source_ingestion.schemas import (
    PhiGradientRealSourceGateResult,
    RealBenchmarkRecord,
    RealSourceExtract,
    RealSourceManifest,
)


def run_phi_gradient_real_source_gate(
    manifest: RealSourceManifest,
    extracts: list[RealSourceExtract],
    benchmarks: list[RealBenchmarkRecord],
) -> PhiGradientRealSourceGateResult:
    validations = [validate_real_source_extract(extract) for extract in extracts]
    real_validations = [item for item in validations if item.counts_as_real_support]
    negative = [item for item in validations if item.status == "EXTRACT_VALID_CONTRADICTS_CANDIDATE"]
    analogy = [item for item in validations if item.status == "EXTRACT_REJECTED_ANALOGY_ONLY"]
    accepted = [item.extract_id for item in real_validations]
    has_observable_or_baseline = any(
        item.status in {"EXTRACT_VALID_SUPPORTS_OBSERVABLE", "EXTRACT_VALID_SUPPORTS_BASELINE"}
        for item in real_validations
    )
    has_component = any(item.status == "EXTRACT_VALID_SUPPORTS_COMPONENT" for item in real_validations)
    has_real_benchmark = any(
        benchmark.comparable_to_phi_gradient and benchmark.data_table_or_values and not benchmark.is_fixture and not benchmark.is_test_double
        for benchmark in benchmarks
    )
    missing: list[str] = []
    if not has_observable_or_baseline:
        missing.append("real_observable_or_baseline_extract")
    if not has_component:
        missing.append("real_component_extract")
    if not has_real_benchmark:
        missing.append("real_comparable_benchmark_record")

    if negative and any(item.counts_as_real_support for item in negative):
        status = "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    elif has_real_benchmark:
        status = "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"
    elif has_observable_or_baseline and has_component:
        status = "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
    elif analogy and not real_validations and len(analogy) == len(validations):
        status = "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY"
    elif not manifest.entries:
        status = "PHI_GRADIENT_REAL_SOURCE_ACQUISITION_FAILED"
    else:
        status = "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"

    return PhiGradientRealSourceGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="real_source_ingestion"),
        manifest=manifest,
        validations=validations,
        benchmarks=benchmarks,
        accepted_real_support_extracts=accepted,
        rejected_analogy_extracts=[item.extract_id for item in analogy],
        negative_extracts=[item.extract_id for item in negative],
        missing_requirements=missing,
        actual_real_sources_ingested=manifest.actual_real_sources_ingested,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(),
        next_actions=_next_actions(status, manifest.actual_real_sources_ingested),
    )


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED":
        return ["PHI_GRADIENT has limited real-source extract support."]
    if status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        return ["PHI_GRADIENT has limited real benchmark support."]
    return ["PHI_GRADIENT real source ingestion was assessed."]


def _blocked_claims() -> list[str]:
    return [
        "PHI_GRADIENT is physically validated.",
        "Real source ingestion proves Frontera C.",
        "Test doubles count as real literature.",
        "A source-backed limited claim is experimental proof.",
    ]


def _next_actions(status: str, actual_real_sources_ingested: bool) -> list[str]:
    if not actual_real_sources_ingested:
        return ["ingest actual real sources", "replace test doubles with real extracts", "keep physical claims blocked"]
    if status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        return ["schedule benchmark comparison campaign", "prepare parameter alignment protocol", "keep experimental claims blocked"]
    if status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED":
        return ["schedule benchmark data acquisition", "keep physical claims blocked"]
    if status == "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED":
        return ["record contradiction", "trigger post-mortem", "consider down-ranking PHI_GRADIENT"]
    return ["search more precise sources", "block source upgrade"]
