"""Real benchmark record handling for PHI_GRADIENT."""

from __future__ import annotations

from phyng.real_source_ingestion.schemas import RealBenchmarkRecord


def comparable_real_benchmark_record_double() -> RealBenchmarkRecord:
    return RealBenchmarkRecord(
        benchmark_id="RBM-DOUBLE-COMP",
        source_id="RS-DOUBLE-BENCH",
        observable="visibility_decay",
        parameter_ranges={"m_kg": (1e-20, 1e-14), "L_m": (1e-9, 1e-5), "t_s": (0.0, 10.0)},
        comparison_variable="max_abs_delta",
        data_table_or_values="test-double table with visibility decay values",
        limitations=["TEST_DOUBLE_REAL_SOURCE_FORMAT", "does not count as real benchmark support"],
        comparable_to_phi_gradient=True,
        is_test_double=True,
    )


def non_comparable_real_benchmark_record_double() -> RealBenchmarkRecord:
    return RealBenchmarkRecord(
        benchmark_id="RBM-DOUBLE-NOT-COMP",
        source_id="RS-DOUBLE-BENCH",
        observable="unrelated_observable",
        parameter_ranges={"temperature_K": (1.0, 10.0)},
        comparison_variable=None,
        data_table_or_values=None,
        limitations=["not comparable to PHI_GRADIENT"],
        comparable_to_phi_gradient=False,
        is_test_double=True,
    )


def default_benchmark_doubles() -> list[RealBenchmarkRecord]:
    return [comparable_real_benchmark_record_double(), non_comparable_real_benchmark_record_double()]
