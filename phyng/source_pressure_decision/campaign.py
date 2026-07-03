"""Campaign orchestration for PHI_GRADIENT source pressure decision v3.9."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.core.compatibility import normalize_status
from phyng.source_pressure_decision.benchmark_alignment import assess_benchmark_alignment
from phyng.source_pressure_decision.contradiction_map import build_contradiction_map
from phyng.source_pressure_decision.decision_engine import compute_decision
from phyng.source_pressure_decision.loader import load_source_pressure_inputs
from phyng.source_pressure_decision.pressure_classifier import classify_extract
from phyng.source_pressure_decision.recommendations import build_recommendations
from phyng.source_pressure_decision.reports import write_source_pressure_reports
from phyng.source_pressure_decision.schemas import (
    SourcePressureCampaignResult,
    SourcePressureGateResult,
)
from phyng.source_pressure_decision.slot_pressure import compute_slot_pressure


OUTPUT_PATHS = {
    "decision": Path("data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json"),
    "extract_pressure_map": Path("data/real_sources/source_pressure/phi_gradient_extract_pressure_map_v3_9.json"),
    "slot_pressure_summary": Path("data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json"),
    "benchmark_alignment": Path("data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json"),
    "contradiction_map": Path("data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json"),
    "recommendations": Path("data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json"),
}


def run_phi_gradient_source_pressure_decision_campaign(root: str | Path = ".") -> SourcePressureCampaignResult:
    repo_root = Path(root)
    inputs = load_source_pressure_inputs(repo_root)

    if inputs.blocked_reason:
        gate = _blocked_gate(inputs.blocked_reason)
        result = SourcePressureCampaignResult(status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_source_pressure_reports(result, repo_root / "reports")
        return result

    # 1. Load validation-ready extracts
    pack = inputs.validation_ready_pack
    extracts = pack.get("extracts", [])

    # 2. Classify each extract
    records = [classify_extract(ext, inputs.source_hashes) for ext in extracts]

    # 3. Compute slot pressure
    slot_summaries = compute_slot_pressure(records)

    # 4. Assess benchmark alignment
    benchmark = assess_benchmark_alignment(records)

    # 5. Build contradiction map
    contradiction = build_contradiction_map(records)

    # 6. Compute global decision
    decision = compute_decision(records, slot_summaries, benchmark, contradiction)

    # 7. Determine campaign status
    status = _campaign_status(decision.primary_decision)

    # 8. Build gate result
    gate = SourcePressureGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="source_pressure_decision"),
        validation_ready_count=len(records),
        extract_pressure_records=records,
        slot_pressure_summary=slot_summaries,
        benchmark_alignment=benchmark,
        contradiction_map=contradiction,
        decision=decision,
        allowed_claims=decision.allowed_claims,
        blocked_claims=decision.blocked_claims,
        next_recommendations=decision.next_recommendations,
    )

    # 9. Write data artifacts
    recs_payload = build_recommendations(decision, contradiction)
    output_paths = _write_outputs(repo_root, gate, recs_payload)
    gate.output_paths = output_paths

    # 10. Write reports
    result = SourcePressureCampaignResult(status=status, gate_result=gate)
    result.report_paths = write_source_pressure_reports(result, repo_root / "reports")
    return result


def _blocked_gate(reason: str) -> SourcePressureGateResult:
    return SourcePressureGateResult(
        status=reason,
        canonical_status=normalize_status(reason, domain="source_pressure_decision"),
        allowed_claims=[],
        blocked_claims=[
            "PHI_GRADIENT is physically validated.",
            "Frontera C is validated.",
        ],
        next_recommendations=["Restore v3.8.3 validation-ready pack before running v3.9."],
    )


def _campaign_status(primary_decision: str) -> str:
    mapping = {
        "PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED": "PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT",
        "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND": "PHI_GRADIENT_SOURCE_PRESSURE_BENCHMARK_RELEVANT",
        "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED": "PHI_GRADIENT_SOURCE_PRESSURE_CONTRADICTED",
        "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY": "PHI_GRADIENT_SOURCE_PRESSURE_ANALOGY_ONLY",
        "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE": "PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE",
        "PHI_GRADIENT_REAL_SOURCE_PRESSURE_BLOCKED": "PHI_GRADIENT_SOURCE_PRESSURE_BLOCKED_MISSING_VALIDATION_READY_PACK",
    }
    return mapping.get(primary_decision, "PHI_GRADIENT_SOURCE_PRESSURE_INCONCLUSIVE")


def _write_outputs(root: Path, gate: SourcePressureGateResult, recs_payload: dict) -> dict[str, str]:
    paths = {key: root / value for key, value in OUTPUT_PATHS.items()}
    paths["decision"].parent.mkdir(parents=True, exist_ok=True)

    _write_json(paths["decision"], gate.decision.model_dump(mode="json"))
    _write_json(paths["extract_pressure_map"], {
        "extract_pressure_records": [r.model_dump(mode="json") for r in gate.extract_pressure_records],
        "extract_count": len(gate.extract_pressure_records),
    })
    _write_json(paths["slot_pressure_summary"], {
        "slot_pressure_summary": [s.model_dump(mode="json") for s in gate.slot_pressure_summary],
        "slot_count": len(gate.slot_pressure_summary),
    })
    _write_json(paths["benchmark_alignment"], gate.benchmark_alignment.model_dump(mode="json"))
    _write_json(paths["contradiction_map"], gate.contradiction_map.model_dump(mode="json"))
    _write_json(paths["recommendations"], recs_payload)

    return {key: str(path.relative_to(root)) for key, path in paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
