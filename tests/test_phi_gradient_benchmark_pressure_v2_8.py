from phyng.source_pressure.benchmark_pressure import assess_benchmark_pressure
from phyng.source_pressure.phi_gradient_audit import benchmark_candidate_limited_fixture, benchmark_not_comparable_fixture


def test_benchmark_requires_comparable_observable():
    result = assess_benchmark_pressure(benchmark_candidate_limited_fixture())

    assert result.status == "BENCHMARK_SUPPORTS_CANDIDATE_LIMITED"
    assert result.counts_as_benchmark_support


def test_benchmark_not_comparable_is_rejected():
    result = assess_benchmark_pressure(benchmark_not_comparable_fixture())

    assert result.status == "BENCHMARK_REJECTED_NOT_COMPARABLE"
    assert not result.counts_as_benchmark_support


def test_benchmark_data_found_requires_comparable_record():
    comparable = assess_benchmark_pressure(benchmark_candidate_limited_fixture())
    rejected = assess_benchmark_pressure(benchmark_not_comparable_fixture())

    assert comparable.canonical_status.domain_status == "PHI_GRADIENT_BENCHMARK_DATA_FOUND"
    assert rejected.canonical_status.domain_status != "PHI_GRADIENT_BENCHMARK_DATA_FOUND"
