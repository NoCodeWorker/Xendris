"""PHI_GRADIENT v3.0 real source acquisition gate."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.real_source_acquisition.benchmark_comparability import assess_benchmark_comparability
from phyng.real_source_acquisition.candidate_manifest import (
    NoopSourceAcquisitionBackend,
    build_candidate_manifest,
)
from phyng.real_source_acquisition.extract_ingestion import ingest_candidate_extracts
from phyng.real_source_acquisition.negative_sources import collect_negative_sources
from phyng.real_source_acquisition.query_plan import build_phi_gradient_real_source_query_plan
from phyng.real_source_acquisition.schemas import (
    PhiGradientRealSourceAcquisitionResult,
    RealSourceCandidate,
    RealSourceCandidateManifest,
    SourceAcquisitionBackend,
)
from phyng.real_source_acquisition.slot_coverage import build_slot_coverage_matrix
from phyng.real_source_ingestion.schemas import RealSourceExtract


def run_phi_gradient_real_source_acquisition(
    backend: SourceAcquisitionBackend | None = None,
    extracts_by_source_id: dict[str, RealSourceExtract] | None = None,
) -> PhiGradientRealSourceAcquisitionResult:
    query_plan = build_phi_gradient_real_source_query_plan()
    acquisition_backend = backend or NoopSourceAcquisitionBackend()
    manifest = build_candidate_manifest(query_plan, acquisition_backend)
    ingestion_results = ingest_candidate_extracts(manifest.candidates, extracts_by_source_id)
    slot_coverage = build_slot_coverage_matrix(manifest.candidates, ingestion_results)
    negative_sources = collect_negative_sources(ingestion_results)
    benchmark = assess_benchmark_comparability(slot_coverage)
    status = _determine_status(manifest, negative_sources, benchmark.status, slot_coverage.records)
    actual_extracts_validated = any(
        result.validation is not None and result.validation.counts_as_real_support
        for result in ingestion_results
    )
    return PhiGradientRealSourceAcquisitionResult(
        status=status,
        canonical_status=normalize_status(status, domain="real_source_acquisition"),
        query_plan=query_plan,
        candidate_manifest=manifest,
        ingestion_results=ingestion_results,
        slot_coverage=slot_coverage,
        negative_sources=negative_sources,
        benchmark_comparability=benchmark,
        actual_real_sources_acquired=manifest.actual_real_sources_acquired,
        actual_real_extracts_validated=actual_extracts_validated,
        backend_status=manifest.backend_status,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(status),
        next_actions=_next_actions(status, manifest.candidates),
    )


def _determine_status(
    manifest: RealSourceCandidateManifest,
    negative_sources: list,
    benchmark_status: str,
    records: list,
) -> str:
    if manifest.backend_status == "NOOP_SOURCE_ACQUISITION_BACKEND" and not manifest.candidates:
        return "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING"
    if negative_sources:
        return "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED"
    if not manifest.candidates:
        return "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    if not manifest.actual_real_sources_acquired:
        return "PHI_GRADIENT_REAL_SOURCE_CANDIDATES_FOUND"
    if benchmark_status == "BENCHMARK_COMPARABLE_REAL_RECORD_FOUND":
        return "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"
    if any(record.accepted_support_count > 0 for record in records):
        return "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
    return "PHI_GRADIENT_REAL_SOURCES_ACQUIRED"


def _allowed_claims(status: str) -> list[str]:
    if status == "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING":
        return ["A deterministic acquisition query plan was produced."]
    if status == "PHI_GRADIENT_REAL_SOURCE_CANDIDATES_FOUND":
        return ["Source candidates were identified for review, but not validated as support."]
    if status in {"PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED", "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"}:
        return ["Limited source-pressure statements tied to validated extracts."]
    return ["Campaign executed with conservative source-pressure status."]


def _blocked_claims(status: str) -> list[str]:
    claims = [
        "PHI_GRADIENT is physically validated.",
        "PHI_GRADIENT validates Frontera C.",
        "A query plan is evidence.",
        "Acquisition candidates count as source support.",
    ]
    if status != "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND":
        claims.append("PHI_GRADIENT has benchmark-comparable real support.")
    return claims


def _next_actions(status: str, candidates: list[RealSourceCandidate]) -> list[str]:
    if status == "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING":
        return [
            "Attach a reviewed local or external acquisition backend.",
            "Acquire real source metadata and extracts before any claim promotion.",
            "Keep PHI_GRADIENT physical claims blocked.",
        ]
    if candidates:
        return [
            "Manually review candidate sources.",
            "Extract slot-specific text, equations, observables and benchmark ranges.",
            "Run v2.9 extract validation before counting support.",
        ]
    return ["Repeat acquisition only after a backend or local manifest exists."]
