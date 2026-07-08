"""Artifact writer for provider smoke runs."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_5.scoring import score_provider_responses

from .smoke_report_builder import build_markdown_report


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows) + ("\n" if rows else ""), encoding="utf-8")


def build_summary(run_result: dict, score_rows: list[dict[str, Any]]) -> dict[str, Any]:
    records = run_result["records"]
    dataset = run_result["dataset"]
    providers = sorted({record.provider_name for record in records})
    completed_by_provider = defaultdict(int)
    failed_by_provider = Counter(error["provider_name"] for error in run_result["provider_errors"])
    score_by_provider: dict[str, list[float]] = defaultdict(list)
    for record in records:
        if record.status == "COMPLETED":
            completed_by_provider[record.provider_name] += 1
    for row in score_rows:
        score_by_provider[row["provider_name"]].append(row["score_total"])
    mean_scores = {
        provider: round(sum(scores) / len(scores), 4) if scores else 0.0
        for provider, scores in score_by_provider.items()
    }
    provider_mode = run_result["config"].provider_mode
    final_decision = (
        "PROVIDER_SMOKE_DRY_RUN_COMPLETED_NO_REAL_PROVIDER_CLAIM"
        if provider_mode == "mock"
        else "PROVIDER_SMOKE_ON_FROZEN_N10_COMPLETED_NO_STATISTICAL_CLAIM"
    )
    return {
        "run_id": run_result["config"].run_id,
        "dataset_version": dataset.dataset_version,
        "dataset_hash": dataset.dataset_hash,
        "manifest_hash": dataset.manifest_hash,
        "frozen_task_count": len(dataset.tasks),
        "provider_mode": provider_mode,
        "providers_attempted": providers,
        "providers_completed": [provider for provider in providers if completed_by_provider[provider] > 0],
        "providers_failed": [provider for provider in providers if failed_by_provider[provider] > 0],
        "task_attempts_total": len(records),
        "task_attempts_completed": sum(1 for record in records if record.status == "COMPLETED"),
        "task_attempts_failed": sum(1 for record in records if record.status != "COMPLETED"),
        "total_estimated_cost_usd": run_result["total_estimated_cost_usd"],
        "budget_cap_usd": run_result["config"].budget_cap_usd,
        "budget_decision": run_result["budget_decision"],
        "mean_smoke_score_by_provider": mean_scores,
        "failure_count_by_provider": dict(failed_by_provider),
        "scoring_limitations": [
            "Smoke diagnostics only.",
            "No hidden tests executed by this scorer.",
            "No statistical claim authorized.",
            "No provider superiority claim authorized.",
        ],
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
        "final_decision": final_decision,
    }


def write_smoke_artifacts(run_result: dict) -> dict[str, Any]:
    outdir = run_result["config"].output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    records = run_result["records"]
    scores = score_provider_responses(records)
    response_rows = [record.to_dict() for record in records]
    score_rows = [score.to_dict() for score in scores]
    summary = build_summary(run_result, score_rows)
    costs = {
        "total_estimated_cost_usd": summary["total_estimated_cost_usd"],
        "budget_cap_usd": summary["budget_cap_usd"],
        "budget_decision": summary["budget_decision"],
    }

    _write_jsonl(outdir / "provider_responses.jsonl", response_rows)
    _write_jsonl(outdir / "provider_scores.jsonl", score_rows)
    _write_jsonl(outdir / "provider_errors.jsonl", run_result["provider_errors"])
    (outdir / "provider_costs.json").write_text(json.dumps(costs, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "provider_smoke_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (outdir / "provider_smoke_report.md").write_text(build_markdown_report(summary), encoding="utf-8")
    return summary
