from phyng.real_source_ingestion.extract_validation import (
    default_extract_doubles,
    real_source_component_extract_double,
    real_source_negative_double,
    real_source_observable_extract_double,
)
from phyng.real_source_ingestion.manifest import build_real_source_manifest, default_manifest_entries
from phyng.real_source_ingestion.phi_gradient_real_source_gate import run_phi_gradient_real_source_gate


def test_negative_extract_blocks_upgrade():
    manifest = build_real_source_manifest(default_manifest_entries())
    gate = run_phi_gradient_real_source_gate(manifest, [real_source_negative_double()], [])

    assert gate.status == "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    assert gate.negative_extracts


def test_real_source_backed_limited_requires_observable_and_component():
    manifest = build_real_source_manifest([])
    observable = real_source_observable_extract_double().model_copy(update={"is_test_double": False, "source_id": "REAL-OBS"})
    component = real_source_component_extract_double().model_copy(update={"is_test_double": False, "source_id": "REAL-COMP"})
    gate = run_phi_gradient_real_source_gate(manifest, [observable, component], [])

    assert gate.status == "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED"
    assert set(gate.accepted_real_support_extracts) == {"EXT-DOUBLE-OBS", "EXT-DOUBLE-COMP"}


def test_missing_benchmark_keeps_benchmark_blocked():
    manifest = build_real_source_manifest(default_manifest_entries())
    gate = run_phi_gradient_real_source_gate(manifest, default_extract_doubles(), [])

    assert gate.status == "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE"
    assert "real_comparable_benchmark_record" in gate.missing_requirements
