"""Acquisition backend boundary and candidate manifest construction."""

from __future__ import annotations

from phyng.real_source_acquisition.schemas import (
    RealSourceCandidate,
    RealSourceCandidateManifest,
    RealSourceQueryPlan,
    SlotQuery,
)


class NoopSourceAcquisitionBackend:
    backend_name = "NOOP_SOURCE_ACQUISITION_BACKEND"

    def search(self, query: SlotQuery) -> list[RealSourceCandidate]:
        return []


class ManifestOnlySourceAcquisitionBackend:
    backend_name = "MANIFEST_ONLY_SOURCE_ACQUISITION_BACKEND"

    def __init__(self, candidates: list[RealSourceCandidate]):
        self._candidates = candidates

    def search(self, query: SlotQuery) -> list[RealSourceCandidate]:
        return [candidate for candidate in self._candidates if query.slot_id in candidate.targeted_slots]


def build_candidate_manifest(plan: RealSourceQueryPlan, backend) -> RealSourceCandidateManifest:
    candidates: list[RealSourceCandidate] = []
    for query in [*plan.slot_queries, *plan.negative_queries]:
        candidates.extend(backend.search(query))
    unique: dict[str, RealSourceCandidate] = {}
    for candidate in candidates:
        unique[candidate.source_id] = candidate
    actual_acquired = any(
        candidate.acquisition_status in {"REAL_SOURCE_AVAILABLE_LOCAL", "REAL_SOURCE_AVAILABLE_URL"}
        and bool(candidate.local_path or candidate.url or candidate.doi or candidate.arxiv_id)
        for candidate in unique.values()
    )
    return RealSourceCandidateManifest(
        candidates=list(unique.values()),
        actual_real_sources_acquired=actual_acquired,
        backend_status=getattr(backend, "backend_name", "UNKNOWN_BACKEND"),
        notes=["Acquisition candidates are not support until extracts validate slots."],
    )


def manifest_only_candidate_fixture() -> RealSourceCandidate:
    return RealSourceCandidate(
        source_id="SRC-CAND-MANIFEST-ONLY-001",
        title="Candidate metadata only fixture",
        authors=["Manifest Fixture"],
        year=2026,
        source_type="paper",
        targeted_slots=["SLOT_1_DECOHERENCE_BASELINE_MODELS"],
        expected_components=["visibility_decay_observable"],
        acquisition_status="REAL_SOURCE_CANDIDATE_IDENTIFIED",
        reason_for_inclusion="Tests manifest-only backend boundary.",
        analogy_risk="MEDIUM",
        is_support=False,
    )
