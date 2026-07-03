"""Real source manifest builder and deterministic test doubles."""

from __future__ import annotations

from phyng.real_source_ingestion.schemas import RealSourceManifest, RealSourceManifestEntry


FIXTURE_NOTE = "FIXTURE_ONLY_DOES_NOT_COUNT_AS_REAL_SUPPORT"
TEST_DOUBLE_NOTE = "TEST_DOUBLE_REAL_SOURCE_FORMAT"


def build_real_source_manifest(entries: list[RealSourceManifestEntry]) -> RealSourceManifest:
    fixture_entries = [entry.source_id for entry in entries if entry.is_fixture]
    test_double_entries = [entry.source_id for entry in entries if entry.is_test_double]
    real_entries = [entry.source_id for entry in entries if not entry.is_fixture and not entry.is_test_double]
    actual_ingested = any(
        entry.source_id in real_entries and entry.ingestion_status in {"REAL_SOURCE_INGESTED", "REAL_SOURCE_EXTRACTED"}
        for entry in entries
    )
    if actual_ingested:
        status = "PHI_GRADIENT_REAL_SOURCES_ACQUIRED"
    elif entries:
        status = "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    else:
        status = "PHI_GRADIENT_REAL_SOURCE_ACQUISITION_FAILED"
    return RealSourceManifest(
        entries=entries,
        fixture_entries=fixture_entries,
        real_entries=real_entries,
        test_double_entries=test_double_entries,
        actual_real_sources_ingested=actual_ingested,
        status=status,
    )


def fixture_source_from_v2_8_double() -> RealSourceManifestEntry:
    return RealSourceManifestEntry(
        source_id="SRC-FIX-V2-8",
        title="v2.8 fixture source carried forward for separation test",
        authors=["Fixture"],
        year=2026,
        source_type="FIXTURE",
        acquisition_method="deterministic_fixture",
        slots_targeted=["SLOT_4_GRADIENT_TRANSITION_OPERATORS"],
        acquisition_status="REAL_SOURCE_REJECTED_OUT_OF_SCOPE",
        ingestion_status="REAL_SOURCE_NOT_INGESTED",
        notes=[FIXTURE_NOTE],
        is_fixture=True,
    )


def real_source_observable_manifest_double() -> RealSourceManifestEntry:
    return _test_double_entry("RS-DOUBLE-OBS", "Observable extract test double", ["SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT"])


def real_source_component_manifest_double() -> RealSourceManifestEntry:
    return _test_double_entry("RS-DOUBLE-COMP", "Component extract test double", ["SLOT_4_GRADIENT_TRANSITION_OPERATORS"])


def real_source_benchmark_manifest_double() -> RealSourceManifestEntry:
    return _test_double_entry("RS-DOUBLE-BENCH", "Benchmark extract test double", ["SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS"])


def real_source_negative_manifest_double() -> RealSourceManifestEntry:
    return _test_double_entry("RS-DOUBLE-NEG", "Negative extract test double", ["SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES"])


def default_manifest_entries() -> list[RealSourceManifestEntry]:
    return [
        fixture_source_from_v2_8_double(),
        real_source_observable_manifest_double(),
        real_source_component_manifest_double(),
        real_source_benchmark_manifest_double(),
    ]


def _test_double_entry(source_id: str, title: str, slots: list[str]) -> RealSourceManifestEntry:
    return RealSourceManifestEntry(
        source_id=source_id,
        title=title,
        authors=["Test Double"],
        year=2026,
        source_type="TEST_DOUBLE",
        acquisition_method="deterministic_test_double",
        local_path=f"test-double://{source_id}",
        slots_targeted=slots,
        acquisition_status="REAL_SOURCE_AVAILABLE_LOCAL",
        ingestion_status="REAL_SOURCE_EXTRACTED",
        notes=[TEST_DOUBLE_NOTE],
        is_test_double=True,
    )
