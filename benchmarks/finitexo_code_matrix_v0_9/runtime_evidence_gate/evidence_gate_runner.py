from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_claims import (
    build_claim_authorization,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_config import (
    COMPARISON_SPECS,
    EVIDENCE_GATE_DECISIONS,
    RuntimeEvidenceGateConfig,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_integrity import (
    check_evidence_integrity,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_loader import (
    load_run_artifacts,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_report import (
    build_report,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_statistics import (
    compute_all_comparisons,
)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _compute_cost_robustness(
    artifacts: dict[str, Any],
    statistics: dict[str, Any],
) -> dict[str, Any]:
    summary = artifacts.get("summary", {})
    cost_by_variant = summary.get("cost_by_variant", {})

    result: dict[str, Any] = {}
    for treatment_name, control_name in COMPARISON_SPECS:
        key = f"{treatment_name}_vs_{control_name}"
        treatment_cost = cost_by_variant.get(treatment_name, 0)
        control_cost = cost_by_variant.get(control_name, 0)
        cost_delta = treatment_cost - control_cost
        comp = statistics.get(key, {})
        ml = comp.get("mean_lift", 0)
        cost_per_point = (cost_delta / ml) if isinstance(ml, (int, float)) and ml > 0 else None
        result[key] = {
            "cost_delta": cost_delta,
            "cost_per_mean_lift_point": cost_per_point,
            "variant_costs": {
                treatment_name: treatment_cost,
                control_name: control_cost,
            },
            "cost_ratio": (treatment_cost / control_cost) if control_cost > 0 else None,
        }

    result["total_cost_usd"] = summary.get("total_cost_usd", 0)
    result["budget_cap_usd"] = summary.get("budget_cap_usd", 0)
    result["within_budget"] = summary.get("total_cost_usd", 0) <= summary.get("budget_cap_usd", float("inf"))
    return result


def _determine_final_decision(
    integrity_result: dict[str, Any],
    statistics: dict[str, Any],
) -> str:
    if not integrity_result.get("integrity_passed", False):
        return EVIDENCE_GATE_DECISIONS["BLOCKED_INTEGRITY_FAIL"]

    runtime_calibrated_keys = [
        "deepseek_runtime_vs_deepseek_base",
        "deepseek_calibrated_runtime_vs_deepseek_base",
        "deepseek_calibrated_runtime_vs_deepseek_wrapper",
        "deepseek_calibrated_runtime_vs_deepseek_runtime",
        "openai_runtime_vs_openai_base",
        "openai_calibrated_runtime_vs_openai_base",
        "openai_calibrated_runtime_vs_openai_wrapper",
        "openai_calibrated_runtime_vs_openai_runtime",
    ]

    has_signal = False
    for key in runtime_calibrated_keys:
        comp = statistics.get(key)
        if isinstance(comp, dict):
            signal = comp.get("signal", "")
            if signal in ("STRONG_DIAGNOSTIC_SIGNAL", "MODERATE_DIAGNOSTIC_SIGNAL"):
                has_signal = True
                break

    if has_signal:
        return EVIDENCE_GATE_DECISIONS["DIAGNOSTIC_SIGNAL"]
    else:
        return EVIDENCE_GATE_DECISIONS["WEAK_OR_INCONCLUSIVE"]


def run_evidence_gate(
    config: RuntimeEvidenceGateConfig | None = None,
) -> dict[str, Any]:
    if config is None:
        config = RuntimeEvidenceGateConfig()

    output_dir = config.output_dir
    if output_dir.exists() and any(output_dir.iterdir()):
        if not config.allow_overwrite:
            raise FileExistsError(
                f"Output directory {output_dir} already exists and is non-empty. "
                "Set allow_overwrite=True or remove the directory first."
            )

    artifacts = load_run_artifacts(config.source_run_dir)
    integrity_result = check_evidence_integrity(config, artifacts)
    statistics = compute_all_comparisons(artifacts.get("scores", []), config)
    cost_robustness = _compute_cost_robustness(artifacts, statistics)
    claims = build_claim_authorization(integrity_result, statistics)
    final_decision = _determine_final_decision(integrity_result, statistics)
    report = build_report(config, artifacts, integrity_result, statistics, claims, cost_robustness, final_decision)

    output_dir.mkdir(parents=True, exist_ok=True)

    summary_out = {
        "benchmark_version": config.benchmark_version,
        "source_run_id": config.source_run_id,
        "source_run_dir": str(config.source_run_dir),
        "final_decision": final_decision,
        "integrity_decision": integrity_result.get("integrity_decision", "unknown"),
        "statistical_signal_summary": {
            key: comp.get("signal", "unknown") if isinstance(comp, dict) else "error"
            for key, comp in statistics.items()
        },
        "strongest_positive_signals": [
            key for key, comp in statistics.items()
            if isinstance(comp, dict) and comp.get("signal") == "STRONG_DIAGNOSTIC_SIGNAL"
        ],
        "weak_or_inconclusive_signals": [
            key for key, comp in statistics.items()
            if isinstance(comp, dict) and comp.get("signal") == "WEAK_OR_INCONCLUSIVE_SIGNAL"
        ],
        "blocked_claims": claims.get("blocked_claims", []),
        "output_artifacts": [
            "summary.json",
            "integrity.json",
            "statistics.json",
            "cost_robustness.json",
            "claim_authorization.json",
            "report.md",
        ],
    }

    _write_json(output_dir / "summary.json", summary_out)
    _write_json(output_dir / "integrity.json", integrity_result)
    _write_json(output_dir / "statistics.json", statistics)
    _write_json(output_dir / "cost_robustness.json", cost_robustness)
    _write_json(output_dir / "claim_authorization.json", claims)
    (output_dir / "report.md").write_text(report, encoding="utf-8")

    return {
        "summary": summary_out,
        "integrity": integrity_result,
        "statistics": statistics,
        "cost_robustness": cost_robustness,
        "claims": claims,
        "report": report,
        "final_decision": final_decision,
    }
