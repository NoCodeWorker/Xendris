from __future__ import annotations

import hashlib
import json
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized.direct_transport import (
    direct_provider_adapter,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_audit import (
    run_audit,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_types import (
    CalibrationTrace,
    RuntimeAuditDecision,
    RuntimeTrace,
)
from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_config import (
    COST_FRONTIER_DECISIONS,
    CostFrontierConfig,
)
from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_gate import (
    evaluate_cost_frontier_preflight,
)
from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_report import (
    build_cost_frontier_report,
)
from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_scoring import (
    aggregate_by_variant,
    compute_cost_frontier,
    score_cost_frontier_response,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_runner import (
    XENDRIS_ADMISSIBILITY_PROMPT,
    _build_wrapper_task,
    _perform_calibration_pass,
    _calibrated_claim_classification,
    _calibrated_evidence_resolution,
    _calibrated_confidence_banding,
    _calibrated_language_selection,
)

FAMILIES = [
    "algorithmic_reasoning",
    "stateful_refactor",
    "edge_case_handling",
    "api_design_consistency",
    "performance_constraints",
]

AUTHORIZED_CLAIMS: list[str] = [
    "This run compares cheaper calibrated runtime variants against next-step base models in a controlled n=30 diagnostic benchmark.",
    "Cost frontier can be discussed for this run only.",
    "Efficient frontier decisions are diagnostic-only.",
]

PROHIBITED_CLAIMS: list[str] = [
    "universal superiority",
    "statistical superiority",
    "production readiness",
    "provider ranking outside this dataset",
    "cost superiority outside this run",
    "general coding superiority",
    "external benchmark performance",
]


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_dataset(dataset_path: Path) -> list[dict[str, Any]]:
    tasks_dir = dataset_path / "tasks"
    tasks: list[dict[str, Any]] = []
    for p in sorted(tasks_dir.glob("*.json")):
        tasks.append(json.loads(p.read_text(encoding="utf-8")))
    return tasks


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = "\n".join(json.dumps(r, sort_keys=True) for r in records)
    path.write_text(lines + "\n", encoding="utf-8")


def _build_base_task(task: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": task["task_id"],
        "prompt": task["prompt"],
        "constraints": task.get("constraints", []),
        "public_contract": task.get("public_contract", ""),
    }


def _build_calibrated_runtime_task(task: dict[str, Any]) -> dict[str, Any]:
    return _build_wrapper_task(task)


def run_cost_frontier(
    config: CostFrontierConfig,
    adapter: Callable | None = None,
) -> dict[str, Any]:
    dataset = _load_dataset(config.dataset_path)
    dataset_hash = ""
    manifest_hash = ""
    hashes_path = config.dataset_path / "dataset_hashes.json"
    manifest_path = config.dataset_path / "dataset_manifest.json"
    if hashes_path.exists():
        dataset_hash = _file_hash(hashes_path)
    if manifest_path.exists():
        manifest_hash = _file_hash(manifest_path)

    preflight = evaluate_cost_frontier_preflight(
        config, dataset_hash, manifest_hash, len(dataset),
    )

    if not preflight.can_execute:
        return {
            "config": config,
            "dataset": dataset,
            "preflight": preflight.to_dict(),
            "final_decision": COST_FRONTIER_DECISIONS["BLOCKED"],
        }

    outdir = config.output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    _write_json(outdir / "preflight.json", preflight.to_dict())

    records: list[dict[str, Any]] = []
    scored_records: list = []
    metadata: list[dict[str, Any]] = []
    traces: list[RuntimeTrace] = []
    calibration_traces: list[CalibrationTrace] = []
    errors: list[dict[str, Any]] = []
    total_cost: float = 0.0
    total_attempted: int = 0
    total_completed: int = 0
    total_failed: int = 0

    for variant in config.variants:
        is_calibrated = variant.execution_method == "CALIBRATED_RUNTIME"
        is_runtime = is_calibrated

        for task in dataset:
            task_id = task.get("task_id", "")
            task_family = task.get("family", "unknown")
            total_attempted += 1

            try:
                base_adapter = adapter if adapter is not None else direct_provider_adapter
                if is_calibrated:
                    wrapped = _build_calibrated_runtime_task(task)
                    result = base_adapter(variant, wrapped, config)
                else:
                    base_task = _build_base_task(task)
                    result = base_adapter(variant, base_task, config)

                cost = getattr(result, "estimated_cost_usd", 0.0)
                total_cost += cost
                total_completed += 1

                record = {
                    "run_id": config.run_id,
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": getattr(result, "provider_reported_model", variant.model_name),
                    "provider_mode": config.provider_mode,
                    "task_id": task_id,
                    "task_family": task_family,
                    "status": "COMPLETED",
                    "response_text": getattr(result, "raw_response_text", ""),
                    "normalized_response_text": " ".join(getattr(result, "raw_response_text", "").split()),
                    "error_type": None,
                    "error_message_sanitized": None,
                    "prompt_tokens": getattr(result, "prompt_tokens", None),
                    "completion_tokens": getattr(result, "completion_tokens", None),
                    "total_tokens": getattr(result, "total_tokens", None),
                    "estimated_cost_usd": cost,
                }

                response_text = getattr(result, "raw_response_text", "")

                if is_calibrated:
                    audit = run_audit(response_text, task)
                    trace = RuntimeTrace(
                        task_id=task_id,
                        provider_name=variant.provider_name,
                        variant_name=variant.variant_name,
                        initial_response=response_text,
                        initial_audit=audit,
                        audit_decision=audit.decision,
                        repair_attempted=False,
                        repair_response=None,
                        repair_audit=None,
                        final_response=response_text,
                        final_audit=audit,
                        prompt_tokens=record["prompt_tokens"],
                        completion_tokens=record["completion_tokens"],
                        total_tokens=record["total_tokens"],
                        estimated_cost_usd=cost,
                    )
                    traces.append(trace)

                    calibration_prompt = XENDRIS_ADMISSIBILITY_PROMPT
                    claim_classification = _calibrated_claim_classification(response_text, calibration_prompt)
                    evidence_status = _calibrated_evidence_resolution(response_text, calibration_prompt)
                    confidence_band = _calibrated_confidence_banding(response_text)
                    allowed_lang, blocked_lang = _calibrated_language_selection(response_text)
                    calibrated_final = _perform_calibration_pass(
                        response_text, claim_classification, evidence_status,
                        confidence_band, allowed_lang,
                    )

                    calibration_trace = CalibrationTrace(
                        task_id=task_id,
                        provider_name=variant.provider_name,
                        variant_name=variant.variant_name,
                        initial_response=response_text,
                        claim_classification=claim_classification,
                        evidence_status=evidence_status,
                        confidence_band=confidence_band,
                        allowed_language=allowed_lang,
                        blocked_language=blocked_lang,
                        final_calibrated_response=calibrated_final,
                        estimated_cost_usd=cost,
                    )
                    calibration_traces.append(calibration_trace)

                    record["response_text"] = calibrated_final
                    record["normalized_response_text"] = " ".join(calibrated_final.split())

                records.append(record)

                meta = {k: v for k, v in record.items() if k not in ("response_text", "normalized_response_text")}
                metadata.append(meta)

                final_text = calibrated_final if is_calibrated else response_text
                sr = score_cost_frontier_response(
                    variant.variant_name,
                    variant.provider_name,
                    variant.model_name,
                    task_id,
                    task_family,
                    final_text,
                    estimated_cost_usd=cost,
                )
                scored_records.append(sr)

            except Exception as exc:
                total_failed += 1
                errors.append({
                    "task_id": task_id,
                    "variant_name": variant.variant_name,
                    "error_type": type(exc).__name__,
                    "error_message_sanitized": str(exc)[:200],
                })
                records.append({
                    "run_id": config.run_id,
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": variant.model_name,
                    "provider_mode": config.provider_mode,
                    "task_id": task_id,
                    "task_family": task_family,
                    "status": "FAILED",
                    "response_text": "",
                    "normalized_response_text": "",
                    "error_type": type(exc).__name__,
                    "error_message_sanitized": str(exc)[:200],
                })

    aggregates = aggregate_by_variant(scored_records)
    cost_frontier = compute_cost_frontier(scored_records, aggregates)

    evidence_integrity = _compute_evidence_integrity(
        records, scored_records, traces, calibration_traces, errors, config,
    )

    integr_ready = evidence_integrity.get("evidence_integrity_ready", False)

    if not integr_ready:
        final_decision = COST_FRONTIER_DECISIONS["PARTIAL"]
    elif total_failed == 0 and total_completed == config.expected_attempts:
        final_decision = COST_FRONTIER_DECISIONS["COMPLETED"]
    else:
        final_decision = COST_FRONTIER_DECISIONS["PARTIAL"]

    _write_jsonl(outdir / "responses.jsonl", records)
    _write_jsonl(outdir / "scores.jsonl", [sr.to_dict() for sr in scored_records])
    _write_jsonl(outdir / "metadata.jsonl", metadata)
    _write_jsonl(outdir / "errors.jsonl", errors)

    costs_payload = {
        "total_cost_usd": round(total_cost, 8),
        "budget_cap_usd": config.budget_cap_usd,
        "cost_by_variant": {
            v.variant_name: round(
                sum(r.estimated_cost_usd or 0.0 for r in scored_records if r.variant_name == v.variant_name),
                8,
            )
            for v in config.variants
        },
        "within_budget": total_cost <= config.budget_cap_usd,
    }
    _write_json(outdir / "costs.json", costs_payload)
    _write_json(outdir / "cost_frontier.json", cost_frontier)

    task_level_frontier = _build_task_level_frontier(records, config)
    _write_jsonl(outdir / "task_level_frontier.jsonl", task_level_frontier)

    if traces:
        _write_jsonl(outdir / "runtime_traces.jsonl", [t.to_dict() for t in traces])
    if calibration_traces:
        _write_jsonl(outdir / "calibration_traces.jsonl", [ct.to_dict() for ct in calibration_traces])
        _write_jsonl(outdir / "audit_decisions.jsonl", [{"task_id": ct.task_id, "variant_name": ct.variant_name} for ct in calibration_traces])
        _write_jsonl(outdir / "repair_attempts.jsonl", [])
        _write_jsonl(outdir / "claim_status.jsonl", [{"task_id": ct.task_id, "variant_name": ct.variant_name, "claim_classification": ct.claim_classification} for ct in calibration_traces])
        _write_jsonl(outdir / "confidence_bands.jsonl", [{"task_id": ct.task_id, "variant_name": ct.variant_name, "confidence_band": ct.confidence_band} for ct in calibration_traces])
        _write_jsonl(outdir / "allowed_blocked_language.jsonl", [{"task_id": ct.task_id, "variant_name": ct.variant_name, "allowed_language": ct.allowed_language, "blocked_language": ct.blocked_language} for ct in calibration_traces])
        _write_jsonl(outdir / "calibrated_final_responses.jsonl", [{"task_id": ct.task_id, "variant_name": ct.variant_name, "final_calibrated_response": ct.final_calibrated_response} for ct in calibration_traces])

    _write_json(outdir / "evidence_integrity.json", evidence_integrity)

    gate = {
        "gate_decision": final_decision,
        "preflight_decision": preflight.decision,
        "evidence_integrity_ready": integr_ready,
        "total_expected": config.expected_attempts,
        "total_completed": total_completed,
        "total_failed": total_failed,
    }
    _write_json(outdir / "gate.json", gate)

    summary = _build_summary(config, preflight, dataset, records, scored_records, traces, calibration_traces, errors, costs_payload, cost_frontier, evidence_integrity, final_decision)
    _write_json(outdir / "summary.json", summary)

    report = build_cost_frontier_report(summary, cost_frontier)
    (outdir / "report.md").write_text(report, encoding="utf-8")

    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight.to_dict(),
        "records": records,
        "scored": scored_records,
        "traces": traces,
        "calibration_traces": calibration_traces,
        "costs": costs_payload,
        "cost_frontier": cost_frontier,
        "summary": summary,
        "final_decision": final_decision,
    }


def write_cost_frontier_artifacts(
    run_result: dict[str, Any],
) -> dict[str, Any]:
    return run_result.get("summary", {})


def _build_task_level_frontier(
    records: list[dict[str, Any]],
    config: CostFrontierConfig,
) -> list[dict[str, Any]]:
    by_task: dict[str, dict[str, float]] = {}
    for r in records:
        if r.get("status") == "COMPLETED":
            by_task.setdefault(r["task_id"], {})[r["variant_name"]] = r.get("estimated_cost_usd", 0.0)
    rows: list[dict[str, Any]] = []
    for tid in sorted(by_task.keys()):
        row = {"task_id": tid}
        for v in config.variants:
            row[v.variant_name + "_cost"] = by_task[tid].get(v.variant_name, 0.0)
        rows.append(row)
    return rows


def _compute_evidence_integrity(
    records: list[dict],
    scored: list,
    traces: list,
    calibration_traces: list,
    errors: list,
    config: CostFrontierConfig,
) -> dict[str, Any]:
    responses_count = len(records)
    scores_count = len(scored)
    total_completed = sum(1 for r in records if r.get("status") == "COMPLETED")
    total_failed = sum(1 for r in records if r.get("status") == "FAILED")
    trace_count = len(traces)
    cal_trace_count = len(calibration_traces)

    integrity = {
        "responses_count": responses_count,
        "scores_count": scores_count,
        "metadata_count": responses_count,
        "trace_count": trace_count,
        "calibration_trace_count": cal_trace_count,
        "errors_count": len(errors),
        "total_completed": total_completed,
        "total_failed": total_failed,
        "responses_match_180": responses_count == 180,
        "scores_match_180": scores_count == 180,
        "traces_match_60": trace_count == 60,
        "calibration_traces_match_60": cal_trace_count == 60,
        "errors_match_0": len(errors) == 0,
        "evidence_integrity_ready": (
            responses_count == 180
            and scores_count == 180
            and trace_count == 60
            and cal_trace_count == 60
            and len(errors) == 0
            and total_completed == 180
            and total_failed == 0
        ),
    }
    return integrity


def _build_summary(
    config: CostFrontierConfig,
    preflight: Any,
    dataset: list,
    records: list,
    scored: list,
    traces: list,
    calibration_traces: list,
    errors: list,
    costs_payload: dict,
    cost_frontier: dict,
    evidence_integrity: dict,
    final_decision: str,
) -> dict[str, Any]:
    total_cost = costs_payload.get("total_cost_usd", 0.0)
    total_completed = sum(1 for r in records if r.get("status") == "COMPLETED")
    total_failed = sum(1 for r in records if r.get("status") == "FAILED")
    mean_score = sum(s.score_total for s in scored) / len(scored) if scored else 0.0

    agg = aggregate_by_variant(scored)

    family_scores: dict[str, dict[str, list[float]]] = {}
    for s in scored:
        family_scores.setdefault(s.task_family, {}).setdefault(s.variant_name, []).append(s.score_total)
    family_lift_data: dict[str, dict[str, float]] = {}
    for family, variants in family_scores.items():
        entry: dict[str, float] = {}
        for vn, vals in variants.items():
            entry[vn] = round(sum(vals) / len(vals), 6) if vals else 0.0
        family_lift_data[family] = entry

    return {
        "benchmark_name": config.benchmark_name,
        "benchmark_version": config.benchmark_version,
        "run_id": config.run_id,
        "experiment_type": "cost_frontier_model_step",
        "dataset_name": config.dataset_name,
        "dataset_version": config.dataset_version,
        "dataset_size": len(dataset),
        "provider_mode": config.provider_mode,
        "final_decision": final_decision,
        "total_expected": config.expected_attempts,
        "total_attempted": len(records),
        "total_completed": total_completed,
        "total_failed": total_failed,
        "total_cost_usd": round(total_cost, 8),
        "budget_cap_usd": config.budget_cap_usd,
        "budget_decision": "WITHIN_BUDGET" if total_cost <= config.budget_cap_usd else "EXCEEDED",
        "mean_score_overall": round(mean_score, 6),
        "runtime_variant_trace_count": len(traces),
        "calibration_trace_count": len(calibration_traces),
        "cost_by_variant": costs_payload.get("cost_by_variant", {}),
        "aggregates": [a.to_dict() for a in agg],
        "family_lift": family_lift_data,
        "authorized_claims": list(AUTHORIZED_CLAIMS),
        "prohibited_claims": list(PROHIBITED_CLAIMS),
    }
