"""Orchestrate benchmark construction for v4.0 Track A."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.benchmark_construction.benchmark_rows import build_benchmark_rows
from phyng.benchmark_construction.loader import load_benchmark_construction_inputs
from phyng.benchmark_construction.manifest import build_manifest
from phyng.benchmark_construction.negative_controls import generate_negative_control_plan
from phyng.benchmark_construction.observable_alignment import align_observables
from phyng.benchmark_construction.reports import write_benchmark_construction_reports
from phyng.benchmark_construction.schemas import (
    BenchmarkConstructionCampaignResult,
    BenchmarkConstructionGateResult,
    BenchmarkDatasetManifest,
    NegativeControlPlan,
)
from phyng.core.compatibility import normalize_status

OUTPUT_PATHS = {
    "manifest": Path("data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json"),
    "observable_alignment": Path("data/benchmarks/phi_gradient_observable_alignment_v4_0.json"),
    "benchmark_rows": Path("data/benchmarks/phi_gradient_benchmark_rows_v4_0.json"),
    "negative_control_plan": Path("data/benchmarks/phi_gradient_negative_control_plan_v4_0.json"),
}


def run_phi_gradient_benchmark_construction_campaign(
    root: str | Path = ".",
) -> BenchmarkConstructionCampaignResult:
    repo_root = Path(root)
    inputs = load_benchmark_construction_inputs(repo_root)

    if inputs.blocked_reason:
        # Create blocked result
        gate = _blocked_gate(inputs.blocked_reason)
        result = BenchmarkConstructionCampaignResult(status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_benchmark_construction_reports(result, repo_root / "reports")
        return result

    # Survived extracts logic:
    # We retrieve the classified extract pressure records from inputs.extract_pressure_map
    map_data = inputs.extract_pressure_map
    records = map_data.get("extract_pressure_records", [])

    alignments = align_observables(records)
    rows = build_benchmark_rows(records)
    controls = generate_negative_control_plan(records)

    # Determine status
    if alignments:
        status = "PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY"
    else:
        status = "PHI_GRADIENT_BENCHMARK_BLOCKED_NO_OBSERVABLE_ALIGNMENT"

    manifest = build_manifest(
        row_count=len(rows),
        alignment_count=len(alignments),
        control_count=len(controls.controls),
        status=status,
    )

    allowed = [
        "A debt-aware benchmark dataset was constructed.",
        "Observable alignment was created from source-pressure-limited extracts.",
    ]
    blocked = [
        "PHI_GRADIENT is validated.",
        "Frontera C is validated.",
        "The gradient mechanism is source-backed.",
        "The invariant has empirical confirmation.",
        "Benchmark construction proves physics.",
    ]

    gate = BenchmarkConstructionGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="benchmark_construction"),
        manifest=manifest,
        rows=rows,
        observable_alignment=alignments,
        negative_control_plan=controls,
        allowed_claims=allowed,
        blocked_claims=blocked,
    )

    # Write output JSONs
    output_paths = _write_outputs(repo_root, gate)
    gate.output_paths = output_paths

    result = BenchmarkConstructionCampaignResult(status=status, gate_result=gate)
    result.report_paths = write_benchmark_construction_reports(result, repo_root / "reports")

    return result


def _blocked_gate(reason: str) -> BenchmarkConstructionGateResult:
    status_rec = normalize_status(reason, domain="benchmark_construction")
    manifest = BenchmarkDatasetManifest(
        dataset_id="PHI-GRADIENT-BENCHMARK-DATASET-BLOCKED",
        candidate_family="LOG_BOUNDARY",
        phi_family="PHI_GRADIENT",
        created_at="2026-07-01",
        source_pressure_ref="",
        validation_pack_ref="",
        debt_registry_ref="",
        benchmark_row_count=0,
        observable_alignment_count=0,
        negative_control_count=0,
        status=reason,
    )
    return BenchmarkConstructionGateResult(
        status=reason,
        canonical_status=status_rec,
        manifest=manifest,
        negative_control_plan=NegativeControlPlan(controls=[], notes=["Plan blocked by missing inputs."]),
        allowed_claims=[],
        blocked_claims=["Benchmark comparison is blocked."],
    )


def _write_outputs(root: Path, gate: BenchmarkConstructionGateResult) -> dict[str, str]:
    paths = {key: root / value for key, value in OUTPUT_PATHS.items()}
    paths["manifest"].parent.mkdir(parents=True, exist_ok=True)

    _write_json(paths["manifest"], gate.manifest.model_dump(mode="json"))
    _write_json(
        paths["observable_alignment"],
        {
            "observable_alignments": [a.model_dump(mode="json") for a in gate.observable_alignment],
            "alignment_count": len(gate.observable_alignment),
        },
    )
    _write_json(
        paths["benchmark_rows"],
        {
            "benchmark_rows": [r.model_dump(mode="json") for r in gate.rows],
            "row_count": len(gate.rows),
        },
    )
    _write_json(paths["negative_control_plan"], gate.negative_control_plan.model_dump(mode="json"))

    return {key: str(path.relative_to(root)) for key, path in paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
