"""Build benchmark dataset manifest for v4.0."""

from __future__ import annotations

from phyng.benchmark_construction.schemas import BenchmarkDatasetManifest


def build_manifest(
    row_count: int,
    alignment_count: int,
    control_count: int,
    status: str,
) -> BenchmarkDatasetManifest:
    """Compile dataset metadata into a formal manifest."""
    return BenchmarkDatasetManifest(
        dataset_id="PHI-GRADIENT-BENCHMARK-DATASET-v4_0",
        candidate_family="LOG_BOUNDARY",
        phi_family="PHI_GRADIENT",
        created_at="2026-07-01",
        source_pressure_ref="data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json",
        validation_pack_ref="data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json",
        debt_registry_ref="data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
        benchmark_row_count=row_count,
        observable_alignment_count=alignment_count,
        negative_control_count=control_count,
        excluded_claims=[
            "PHI_GRADIENT is validated.",
            "Frontera C is validated.",
            "The gradient mechanism is source-backed.",
            "The invariant has empirical confirmation.",
            "Benchmark construction proves physics.",
        ],
        allowed_usage=[
            "Model comparison without gradient claim",
            "Observable regime alignment analysis",
            "Negative-control baseline verification",
        ],
        blocked_usage=[
            "Gradient mechanism validation",
            "Physical predictions validation",
            "Frontera C validation",
        ],
        status=status,
        notes=[
            "Benchmark dataset constructed from v3.9 survived source pressure.",
            "Strictly debt-aware: gradient mechanism support is blocked.",
        ],
    )
