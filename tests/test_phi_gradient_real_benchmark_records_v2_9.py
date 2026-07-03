from phyng.real_source_ingestion.benchmark_ingestion import comparable_real_benchmark_record_double
from phyng.real_source_ingestion.extract_validation import real_source_benchmark_extract_double
from phyng.real_source_ingestion.manifest import build_real_source_manifest
from phyng.real_source_ingestion.phi_gradient_real_source_gate import run_phi_gradient_real_source_gate


def test_real_benchmark_data_found_requires_comparable_record():
    manifest = build_real_source_manifest([])
    benchmark_extract = real_source_benchmark_extract_double().model_copy(update={"is_test_double": False, "source_id": "REAL-BENCH"})
    benchmark = comparable_real_benchmark_record_double().model_copy(update={"is_test_double": False, "source_id": "REAL-BENCH"})
    gate = run_phi_gradient_real_source_gate(manifest, [benchmark_extract], [benchmark])

    assert gate.status == "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND"


def test_missing_experimental_data_blocks_physical_validation():
    manifest = build_real_source_manifest([])
    benchmark_extract = real_source_benchmark_extract_double().model_copy(update={"is_test_double": False, "source_id": "REAL-BENCH"})
    benchmark = comparable_real_benchmark_record_double().model_copy(update={"is_test_double": False, "source_id": "REAL-BENCH"})
    gate = run_phi_gradient_real_source_gate(manifest, [benchmark_extract], [benchmark])

    assert gate.canonical_status.canonical_permission.value == "CLAIM_LIMITED_ALLOWED"
    assert "MISSING_EXPERIMENTAL_DATA" in {reason.value for reason in gate.canonical_status.blocked_reasons}
