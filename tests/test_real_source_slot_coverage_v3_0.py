from phyng.real_source_acquisition.benchmark_comparability import assess_benchmark_comparability
from phyng.real_source_acquisition.campaign_gate import run_phi_gradient_real_source_acquisition


def test_slot_coverage_records_missing_requirements():
    result = run_phi_gradient_real_source_acquisition()

    assert len(result.slot_coverage.records) == 8
    assert len(result.slot_coverage.missing_slots) == 8
    assert all(record.missing_requirements for record in result.slot_coverage.records)


def test_benchmark_support_not_granted_without_comparable_record():
    result = run_phi_gradient_real_source_acquisition()
    benchmark = assess_benchmark_comparability(result.slot_coverage)

    assert benchmark.status == "BENCHMARK_COMPARABLE_RECORD_MISSING"
    assert benchmark.comparable_records == 0
    assert result.status == "PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING"
