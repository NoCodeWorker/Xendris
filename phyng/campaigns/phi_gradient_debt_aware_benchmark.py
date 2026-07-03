"""Campaign orchestration for PHI_GRADIENT v4.0 Debt-Aware Benchmark & Scientific Debt."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.benchmark_construction.campaign import run_phi_gradient_benchmark_construction_campaign
from phyng.benchmark_construction.schemas import BenchmarkConstructionCampaignResult
from phyng.scientific_debt.debt_registry import create_slot4_debt_object
from phyng.scientific_debt.reports import write_scientific_debt_reports
from phyng.scientific_debt.slot4_resolution import create_slot4_resolution_plan


def run_phi_gradient_debt_aware_benchmark_campaign(
    root: str | Path = ".",
) -> dict[str, Any]:
    repo_root = Path(root)

    # 1. Run Track A (Benchmark Construction)
    bc_result = run_phi_gradient_benchmark_construction_campaign(repo_root)

    # 2. Run Track B (Scientific Debt)
    debt = create_slot4_debt_object()
    plan = create_slot4_resolution_plan()

    # 3. Write Track B data files if not blocked by missing inputs
    debt_file = repo_root / "data" / "debts" / "DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json"
    plan_file = repo_root / "data" / "debts" / "slot4_resolution_plan_v4_0.json"

    debt_file.parent.mkdir(parents=True, exist_ok=True)
    _write_json(debt_file, debt.model_dump(mode="json"))
    _write_json(plan_file, plan.model_dump(mode="json"))

    # 4. Write Track B reports
    debt_reports = write_scientific_debt_reports(debt, plan, repo_root / "reports")

    # Combine report paths
    all_report_paths = dict(bc_result.report_paths)
    all_report_paths["debt_object"] = debt_reports["debt_object"]
    all_report_paths["slot4_resolution_plan"] = debt_reports["resolution_plan"]

    # 5. Write next gate inputs JSON
    next_gate_inputs_file = repo_root / "data" / "benchmarks" / "phi_gradient_v4_0_next_gate_inputs.json"
    next_gate_inputs_file.parent.mkdir(parents=True, exist_ok=True)

    next_gate_payload = {
        "manifest_path": "data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json",
        "observable_alignment_path": "data/benchmarks/phi_gradient_observable_alignment_v4_0.json",
        "benchmark_rows_path": "data/benchmarks/phi_gradient_benchmark_rows_v4_0.json",
        "negative_control_plan_path": "data/benchmarks/phi_gradient_negative_control_plan_v4_0.json",
        "debt_object_path": "data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json",
        "slot4_resolution_plan_path": "data/debts/slot4_resolution_plan_v4_0.json",
        "status": bc_result.status,
        "ready_for_next_phase": bc_result.status == "PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY",
        "recommended_next_phase": "v4.1 — Benchmark Model Comparison Without Gradient Claim",
        "debt_status": debt.status,
        "notes": [
            "Benchmark construction v4.0 is completed.",
            "SLOT_4 debt remains open and blocking for gradient mechanism claims.",
        ],
    }
    _write_json(next_gate_inputs_file, next_gate_payload)

    return {
        "campaign_id": "PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0",
        "status": bc_result.status,
        "benchmark_construction": bc_result.model_dump(mode="json"),
        "debt_object": debt.model_dump(mode="json"),
        "slot4_resolution_plan": plan.model_dump(mode="json"),
        "report_paths": all_report_paths,
        "next_gate_inputs_path": str(next_gate_inputs_file.relative_to(repo_root)),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


if __name__ == "__main__":
    res = run_phi_gradient_debt_aware_benchmark_campaign(root=".")
    print(
        {
            "status": res["status"],
            "next_gate_inputs_path": res["next_gate_inputs_path"],
            "row_count": res["benchmark_construction"]["gate_result"]["manifest"]["benchmark_row_count"],
            "debt_id": res["debt_object"]["debt_id"],
            "debt_status": res["debt_object"]["status"],
        }
    )
