"""Runner for v0.6.0 real-provider controlled run n=30."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Protocol

from .controlled_run_config import ControlledProviderSpec, ControlledRunConfig
from .controlled_run_gate import (
    CONTROLLED_RUN_READY,
    ControlledRunPreflight,
    evaluate_controlled_run_preflight,
)
from .controlled_run_report import build_controlled_run_report
from .controlled_run_scoring import (
    ScoredRecord,
    aggregate_by_provider,
    compute_overall_mean,
    score_provider_responses,
)


AUTHORIZED_CLAIMS = [
    "Real providers executed under controlled conditions.",
    "Budget was respected and tracked per provider.",
    "Provider failures were observed or not observed.",
    "Diagnostic scores computed according to the documented scorer with 13 components.",
    "No broad superiority claim is authorized.",
    "This is a diagnostic-only controlled run.",
]

PROHIBITED_CLAIMS = [
    "Universal model superiority — not authorized.",
    "Production readiness — not authorized.",
    "Statistically significant superiority — not authorized.",
    "Provider quality ranking — diagnostic-only, not generalizable.",
    "Xendris improvement without paired Xendris/base variant — not measured.",
    "General coding ability — not evaluated by this benchmark.",
    "External benchmark performance — not validated here.",
]

COMPLETED = "CONTROLLED_RUN_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "CONTROLLED_RUN_PARTIAL_DIAGNOSTIC_ONLY"
BLOCKED_PREFLIGHT = "CONTROLLED_RUN_BLOCKED_PREFLIGHT"
BLOCKED_BUDGET = "CONTROLLED_RUN_BLOCKED_BUDGET"


class ControlledProviderAdapter(Protocol):
    def __call__(self, provider: ControlledProviderSpec, task: dict, config: ControlledRunConfig) -> Any: ...


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + ("\n" if rows else ""), encoding="utf-8")


def _sanitize_error(message: str | None) -> str | None:
    if message is None:
        return None
    return message.replace("sk-", "[redacted-key-prefix]").replace("Bearer ", "[redacted-bearer] ")


def _load_dataset(config: ControlledRunConfig) -> dict[str, Any]:
    hash_path = config.dataset_path / "dataset_hashes.json"
    manifest_path = config.dataset_path / "dataset_manifest.json"
    tasks_dir = config.dataset_path / "tasks"

    hashes = _load_json(hash_path) if hash_path.exists() else {}
    manifest = _load_json(manifest_path) if manifest_path.exists() else {}
    task_paths = sorted(tasks_dir.glob("task_*.json")) if tasks_dir.exists() else []
    tasks = [_load_json(p) for p in task_paths]

    return {
        "dataset_name": manifest.get("dataset_name", "finitexo_code_matrix_controlled_n30"),
        "dataset_version": manifest.get("dataset_version", "0.6.0"),
        "dataset_hash": hashes.get("dataset_hash", ""),
        "manifest_hash": hashes.get("manifest_hash", ""),
        "manifest": manifest,
        "tasks": tasks,
    }


def _build_summary(
    config: ControlledRunConfig,
    preflight: ControlledRunPreflight,
    dataset: dict[str, Any],
    records: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    request_metadata: list[dict[str, Any]],
    scored: list[ScoredRecord],
    aggregates: list,
    overall_mean: float,
    budget_decision: str,
    final_decision: str,
) -> dict[str, Any]:
    task_count = len(dataset.get("tasks", []))
    attempted = len(records)
    completed = sum(1 for r in records if r.get("status") == "COMPLETED")
    failed = sum(1 for r in records if r.get("status") == "FAILED")
    budget_blocked = sum(1 for r in records if r.get("budget_status") in ("BUDGET_EXHAUSTED", "BLOCKED", "WOULD_EXCEED_BUDGET"))

    total_cost = sum(r.get("estimated_cost_usd") or 0.0 for r in records)
    cost_by_provider: dict[str, float] = defaultdict(float)
    for r in records:
        p = r.get("provider_name", "unknown")
        cost_by_provider[p] += r.get("estimated_cost_usd") or 0.0

    providers = [p.provider_name for p in config.providers]

    return {
        "run_id": config.run_id,
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.6.0",
        "dataset_name": dataset.get("dataset_name", ""),
        "dataset_version": dataset.get("dataset_version", ""),
        "dataset_size": task_count,
        "dataset_hash": dataset.get("dataset_hash", ""),
        "manifest_hash": dataset.get("manifest_hash", ""),
        "provider_mode": config.provider_mode,
        "providers": providers,
        "total_expected": preflight.task_attempts_expected,
        "total_attempted": attempted,
        "total_completed": completed,
        "total_failed": failed,
        "total_budget_blocked": budget_blocked,
        "total_cost_usd": round(total_cost, 8),
        "cost_by_provider": {k: round(v, 8) for k, v in sorted(cost_by_provider.items())},
        "budget_cap_usd": config.budget_cap_usd,
        "budget_decision": budget_decision,
        "mean_score_overall": overall_mean,
        "aggregates": [a.to_dict() for a in aggregates],
        "authorized_claims": list(AUTHORIZED_CLAIMS),
        "prohibited_claims": list(PROHIBITED_CLAIMS),
        "preflight_decision": preflight.decision,
        "preflight_blockers": list(preflight.blockers),
        "final_decision": final_decision,
    }


def _empty_result(
    config: ControlledRunConfig,
    dataset: dict[str, Any],
    preflight: ControlledRunPreflight,
    final_decision: str,
) -> dict[str, Any]:
    task_count = len(dataset.get("tasks", []))
    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight.to_dict(),
        "records": [],
        "provider_errors": [],
        "request_metadata": [],
        "summary": _build_summary(
            config, preflight, dataset, [], [], [], [], [], 0.0, "BLOCKED", final_decision,
        ),
    }


def run_controlled_provider_benchmark(
    config: ControlledRunConfig,
    adapter: ControlledProviderAdapter | None = None,
    skip_dataset_load: bool = False,
    preloaded_dataset: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if preloaded_dataset is not None:
        dataset = preloaded_dataset
    elif skip_dataset_load:
        dataset = {"dataset_name": "", "dataset_version": "", "dataset_hash": "", "manifest_hash": "", "tasks": []}
    else:
        dataset = _load_dataset(config)

    ds_hash = dataset.get("dataset_hash", None)
    manifest_h = dataset.get("manifest_hash", None)
    task_cnt = len(dataset.get("tasks", []))

    preflight = evaluate_controlled_run_preflight(config, ds_hash, manifest_h, task_cnt)
    if not preflight.can_execute:
        return _empty_result(config, dataset, preflight, BLOCKED_PREFLIGHT)

    selected_tasks = dataset["tasks"][: config.expected_task_count]
    estimated_projected = (
        sum(p.estimated_cost_per_task_usd for p in config.providers) * len(selected_tasks)
    )
    if estimated_projected > config.budget_cap_usd:
        return _empty_result(config, dataset, preflight, BLOCKED_BUDGET)

    # Build adapter
    if adapter is None:
        from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized.direct_transport import (
            direct_provider_adapter,
        )
        adapter = direct_provider_adapter  # type: ignore

    records: list[dict[str, Any]] = []
    provider_errors: list[dict[str, Any]] = []
    request_metadata: list[dict[str, Any]] = []
    budget_blocked = 0
    total_cost: float = 0.0
    budget_exhausted = False

    for provider in config.providers:
        for task in selected_tasks:
            if budget_exhausted:
                budget_blocked += 1
                continue

            est_cost = provider.estimated_cost_per_task_usd
            if total_cost + est_cost > config.budget_cap_usd:
                budget_blocked += 1
                budget_exhausted = True
                continue

            meta = {
                "run_id": config.run_id,
                "provider_name": provider.provider_name,
                "model_name": provider.model_name,
                "task_id": task.get("task_id", ""),
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dataset_hash": ds_hash,
                "manifest_hash": manifest_h,
            }
            request_metadata.append(meta)

            start = perf_counter()
            try:
                result = adapter(provider, task, config)
                latency_ms = round((perf_counter() - start) * 1000, 3)
                raw_text = getattr(result, "raw_response_text", result if isinstance(result, str) else "")
                cost = getattr(result, "estimated_cost_usd", est_cost) or est_cost
                total_cost += cost
                records.append({
                    "run_id": config.run_id,
                    "provider_name": provider.provider_name,
                    "model_name": getattr(result, "provider_reported_model", provider.model_name),
                    "provider_mode": config.provider_mode,
                    "task_id": task.get("task_id", ""),
                    "task_version": task.get("task_version", ""),
                    "status": "COMPLETED",
                    "response_text": raw_text,
                    "normalized_response_text": " ".join(raw_text.split()),
                    "error_type": None,
                    "error_message_sanitized": None,
                    "latency_ms": latency_ms,
                    "prompt_tokens": getattr(result, "prompt_tokens", None),
                    "completion_tokens": getattr(result, "completion_tokens", None),
                    "total_tokens": getattr(result, "total_tokens", None),
                    "estimated_cost_usd": cost,
                    "budget_status": "WITHIN_BUDGET",
                    "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                })
            except Exception as exc:
                latency_ms = round((perf_counter() - start) * 1000, 3)
                error_type = type(exc).__name__
                error_msg = _sanitize_error(str(exc))
                provider_errors.append({
                    "provider_name": provider.provider_name,
                    "model_name": provider.model_name,
                    "task_id": task.get("task_id", ""),
                    "error_type": error_type,
                    "error_message_sanitized": error_msg,
                })
                records.append({
                    "run_id": config.run_id,
                    "provider_name": provider.provider_name,
                    "model_name": provider.model_name,
                    "provider_mode": config.provider_mode,
                    "task_id": task.get("task_id", ""),
                    "task_version": task.get("task_version", ""),
                    "status": "FAILED",
                    "response_text": "",
                    "normalized_response_text": "",
                    "error_type": error_type,
                    "error_message_sanitized": error_msg,
                    "latency_ms": latency_ms,
                    "prompt_tokens": None,
                    "completion_tokens": None,
                    "total_tokens": None,
                    "estimated_cost_usd": None,
                    "budget_status": "WITHIN_BUDGET",
                    "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                })

    budget_decision = "WITHIN_BUDGET" if total_cost <= config.budget_cap_usd and not budget_exhausted else "BUDGET_EXHAUSTED"

    scored = score_provider_responses(records)
    aggregates = aggregate_by_provider(scored)
    overall_mean = compute_overall_mean(aggregates)

    has_failures = any(r["status"] == "FAILED" for r in records)
    final_decision = COMPLETED if not has_failures and not budget_exhausted else PARTIAL

    summary = _build_summary(
        config, preflight, dataset, records, provider_errors, request_metadata,
        scored, aggregates, overall_mean, budget_decision, final_decision,
    )

    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight.to_dict(),
        "records": records,
        "provider_errors": provider_errors,
        "request_metadata": request_metadata,
        "scored": scored,
        "aggregates": aggregates,
        "summary": summary,
    }


def write_controlled_run_artifacts(run_result: dict[str, Any]) -> dict[str, Any]:
    summary = run_result["summary"]
    outdir = run_result["config"].output_dir
    outdir.mkdir(parents=True, exist_ok=True)

    _write_json(outdir / "summary.json", summary)
    (outdir / "report.md").write_text(build_controlled_run_report(summary), encoding="utf-8")
    _write_jsonl(outdir / "responses.jsonl", run_result["records"])
    _write_jsonl(outdir / "scores.jsonl", [s.to_dict() for s in run_result["scored"]])
    _write_json(outdir / "costs.json", {
        "total_cost_usd": summary.get("total_cost_usd"),
        "cost_by_provider": summary.get("cost_by_provider"),
        "budget_cap_usd": summary.get("budget_cap_usd"),
        "budget_decision": summary.get("budget_decision"),
    })
    _write_jsonl(outdir / "errors.jsonl", run_result["provider_errors"])
    _write_jsonl(outdir / "metadata.jsonl", run_result["request_metadata"])
    _write_json(outdir / "preflight.json", run_result["preflight"])
    _write_json(outdir / "gate.json", {
        "preflight": run_result["preflight"],
        "final_decision": summary.get("final_decision"),
    })
    return summary


def main() -> int:
    config = ControlledRunConfig()
    result = run_controlled_provider_benchmark(config)
    summary = write_controlled_run_artifacts(result)
    print(summary.get("final_decision"))
    return 0 if summary.get("final_decision") in (COMPLETED, PARTIAL) else 1


if __name__ == "__main__":
    raise SystemExit(main())
