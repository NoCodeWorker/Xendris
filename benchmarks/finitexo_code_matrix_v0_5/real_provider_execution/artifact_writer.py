"""Artifact writer for v0.5.2 real-provider execution."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_5.scoring import score_provider_responses

from .report_builder import build_real_provider_execution_report


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.write_text(text + ("\n" if rows else ""), encoding="utf-8")


def _final_decision(run_result: dict, completed: list[str]) -> str:
    if not run_result["gate"].can_execute:
        return "REAL_PROVIDER_SMOKE_CONFIGURATION_MISSING_NO_EXECUTION"
    if completed:
        return "REAL_PROVIDER_SMOKE_EXECUTED_DIAGNOSTIC_ONLY"
    return "REAL_PROVIDER_SMOKE_ATTEMPTED_ALL_PROVIDERS_FAILED_NO_CLAIM"


def build_execution_summary(run_result: dict, score_rows: list[dict[str, Any]]) -> dict[str, Any]:
    records = run_result["records"]
    dataset = run_result["dataset"]
    configured = [provider.provider_name for provider in run_result["config"].providers]
    attempted = sorted({record.provider_name for record in records})
    completed_by_provider = defaultdict(int)
    failed_by_provider = Counter(error["provider_name"] for error in run_result["provider_errors"])
    scores_by_provider: dict[str, list[float]] = defaultdict(list)
    for record in records:
        if record.status == "COMPLETED":
            completed_by_provider[record.provider_name] += 1
    for row in score_rows:
        scores_by_provider[row["provider_name"]].append(row["score_total"])
    completed = [provider for provider in attempted if completed_by_provider[provider] > 0]
    failed = [provider for provider in attempted if failed_by_provider[provider] > 0 and provider not in completed]
    return {
        "run_id": run_result["config"].run_id,
        "dataset_version": dataset.dataset_version,
        "dataset_hash": dataset.dataset_hash,
        "manifest_hash": dataset.manifest_hash,
        "frozen_task_count": len(dataset.tasks),
        "provider_mode": "real",
        "providers_configured": configured,
        "providers_attempted": attempted,
        "providers_completed": completed,
        "providers_failed": failed,
        "task_attempts_total": len(records),
        "task_attempts_completed": sum(1 for record in records if record.status == "COMPLETED"),
        "task_attempts_failed": sum(1 for record in records if record.status == "FAILED"),
        "task_attempts_skipped": run_result["task_attempts_skipped"],
        "task_attempts_budget_blocked": run_result["task_attempts_budget_blocked"],
        "total_estimated_cost_usd": run_result["total_estimated_cost_usd"],
        "budget_cap_usd": run_result["config"].budget_cap_usd,
        "budget_decision": run_result["budget_decision"],
        "mean_smoke_score_by_provider": {
            provider: round(sum(scores) / len(scores), 4) if scores else 0.0
            for provider, scores in scores_by_provider.items()
        },
        "failure_count_by_provider": dict(failed_by_provider),
        "real_provider_configuration_status": run_result["gate"].decision,
        "mock_fallback_used": False,
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
        "external_benchmark_validation_claim_authorized": False,
        "final_decision": _final_decision(run_result, completed),
    }


def write_real_provider_execution_artifacts(run_result: dict) -> dict[str, Any]:
    outdir = run_result["config"].output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    records = run_result["records"]
    scores = score_provider_responses(records)
    response_rows = [record.to_dict() for record in records]
    score_rows = [score.to_dict() for score in scores]
    summary = build_execution_summary(run_result, score_rows)
    costs = {
        "total_estimated_cost_usd": summary["total_estimated_cost_usd"],
        "budget_cap_usd": summary["budget_cap_usd"],
        "budget_decision": summary["budget_decision"],
    }
    _write_jsonl(outdir / "real_provider_responses.jsonl", response_rows)
    _write_jsonl(outdir / "real_provider_scores.jsonl", score_rows)
    _write_jsonl(outdir / "real_provider_errors.jsonl", run_result["provider_errors"])
    _write_jsonl(outdir / "provider_request_metadata.jsonl", run_result["request_metadata"])
    (outdir / "real_provider_costs.json").write_text(json.dumps(costs, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "real_provider_gate.json").write_text(json.dumps(run_result["gate"].to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "real_provider_execution_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "real_provider_execution_report.md").write_text(build_real_provider_execution_report(summary), encoding="utf-8")
    return summary
