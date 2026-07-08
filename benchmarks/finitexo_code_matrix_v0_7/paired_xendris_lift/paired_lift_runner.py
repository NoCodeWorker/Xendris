"""Runner for v0.7.0 paired Xendris lift n=30."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Protocol

from .paired_lift_config import PairedLiftConfig, PairedLiftVariantSpec
from .paired_lift_gate import (
    PAIRED_LIFT_READY,
    PairedLiftPreflight,
    evaluate_paired_lift_preflight,
)
from .paired_lift_report import build_paired_lift_report
from .paired_lift_scoring import (
    PairedLiftScoredRecord,
    PairedLiftVariantAggregate,
    aggregate_by_variant,
    compute_paired_lift,
    score_paired_lift_response,
)

XENDRIS_ADMISSIBILITY_PROMPT = (
    "You are a diagnostic code assistant with strict admissibility discipline.\n\n"
    "Admissibility rules:\n"
    "- Preserve the requested API contract and output format.\n"
    "- Do not claim success unless you have evidence.\n"
    "- Expose limitations when relevant.\n"
    "- Give an actionable, direct answer.\n"
    "- Keep responses concise and structured.\n"
    "- Use deterministic formatting.\n"
    "- Do not expose secrets or credentials.\n"
    "- Do not modify or delete files that the task says are forbidden.\n"
    "- If the task asks for code, provide it. If explanation, provide it.\n"
    "- If unsure or cannot complete the task, state that clearly.\n\n"
    "Now respond to the following task:"
)

COMPLETED = "PAIRED_LIFT_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "PAIRED_LIFT_PARTIAL_DIAGNOSTIC_ONLY"
BLOCKED_PREFLIGHT = "PAIRED_LIFT_BLOCKED_PREFLIGHT"
BLOCKED_BUDGET = "PAIRED_LIFT_BLOCKED_BUDGET"

AUTHORIZED_CLAIMS = [
    "Real providers executed under controlled paired conditions.",
    "Xendris wrapper was applied consistently to paired variants.",
    "Diagnostic scores were computed using the documented scorer.",
    "Paired lift was measured on this n=30 controlled dataset.",
    "Budget was tracked per variant.",
    "Provider failures were observed or not observed.",
]

PROHIBITED_CLAIMS = [
    "Universal model superiority — not authorized.",
    "Statistically significant superiority — not authorized without separate statistical gate.",
    "Production readiness — not authorized.",
    "General coding ability — not evaluated by this benchmark.",
    "External benchmark performance — not validated here.",
    "Xendris universal improvement — not authorized outside this controlled diagnostic run.",
    "Provider ranking — diagnostic-only, not generalizable.",
]


class PairedLiftProviderAdapter(Protocol):
    def __call__(self, provider: PairedLiftVariantSpec, task: dict, config: PairedLiftConfig) -> Any: ...


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + ("\n" if rows else ""), encoding="utf-8")


def _sanitize_error(message: str | None) -> str | None:
    if message is None:
        return None
    return message.replace("sk-", "[redacted-key-prefix]").replace("Bearer ", "[redacted-bearer] ")


def _load_dataset(config: PairedLiftConfig) -> dict[str, Any]:
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


def _build_xendris_task(task: dict) -> dict[str, Any]:
    original_prompt = task.get("prompt", "")
    wrapped_prompt = XENDRIS_ADMISSIBILITY_PROMPT + "\n\n" + original_prompt
    return {**task, "prompt": wrapped_prompt}


def _build_summary(
    config: PairedLiftConfig,
    preflight: PairedLiftPreflight,
    dataset: dict[str, Any],
    records: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    request_metadata: list[dict[str, Any]],
    scored: list[PairedLiftScoredRecord],
    aggregates: list[PairedLiftVariantAggregate],
    paired_lift: dict[str, Any],
    budget_decision: str,
    final_decision: str,
) -> dict[str, Any]:
    total_attempts = len(records)
    total_completed = sum(1 for r in records if r.get("status") == "COMPLETED")
    total_failed = sum(1 for r in records if r.get("status") == "FAILED")
    total_cost = sum(r.get("estimated_cost_usd") or 0.0 for r in records)

    cost_by_variant: dict[str, float] = defaultdict(float)
    for r in records:
        v = r.get("variant_name", "unknown")
        cost_by_variant[v] += r.get("estimated_cost_usd") or 0.0

    return {
        "run_id": config.run_id,
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.7.0",
        "experiment_type": "paired_xendris_lift",
        "dataset_name": dataset.get("dataset_name", ""),
        "dataset_version": dataset.get("dataset_version", ""),
        "dataset_size": len(dataset.get("tasks", [])),
        "dataset_hash": dataset.get("dataset_hash", ""),
        "manifest_hash": dataset.get("manifest_hash", ""),
        "provider_mode": config.provider_mode,
        "variants": [v.variant_name for v in config.variants],
        "total_expected": preflight.expected_attempts,
        "total_attempted": total_attempts,
        "total_completed": total_completed,
        "total_failed": total_failed,
        "total_cost_usd": round(total_cost, 8),
        "cost_by_variant": {k: round(v, 8) for k, v in sorted(cost_by_variant.items())},
        "budget_cap_usd": config.budget_cap_usd,
        "budget_decision": budget_decision,
        "mean_score_overall": (
            sum(a.mean_score for a in aggregates) / len(aggregates) if aggregates else 0.0
        ),
        "aggregates": [a.to_dict() for a in aggregates],
        "paired_lift": paired_lift,
        "authorized_claims": list(AUTHORIZED_CLAIMS),
        "prohibited_claims": list(PROHIBITED_CLAIMS),
        "preflight_decision": preflight.decision,
        "preflight_blockers": list(preflight.blockers),
        "final_decision": final_decision,
    }


def _empty_result(
    config: PairedLiftConfig,
    dataset: dict[str, Any],
    preflight: PairedLiftPreflight,
    final_decision: str,
) -> dict[str, Any]:
    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight.to_dict(),
        "records": [],
        "provider_errors": [],
        "request_metadata": [],
        "scored": [],
        "aggregates": [],
        "paired_lift": {},
        "summary": _build_summary(
            config, preflight, dataset, [], [], [], [], [], {},
            "BLOCKED", final_decision,
        ),
    }


def run_paired_xendris_lift(
    config: PairedLiftConfig,
    adapter: PairedLiftProviderAdapter | None = None,
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

    preflight = evaluate_paired_lift_preflight(config, ds_hash, manifest_h, task_cnt)
    if not preflight.can_execute:
        return _empty_result(config, dataset, preflight, BLOCKED_PREFLIGHT)

    selected_tasks = dataset["tasks"][: config.expected_task_count]
    estimated_projected = (
        sum(v.estimated_cost_per_task_usd for v in config.variants) * len(selected_tasks)
    )
    if estimated_projected > config.budget_cap_usd:
        return _empty_result(config, dataset, preflight, BLOCKED_BUDGET)

    if adapter is None:
        from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized.direct_transport import (
            direct_provider_adapter,
        )
        base_adapter = direct_provider_adapter
    else:
        base_adapter = adapter

    records: list[dict[str, Any]] = []
    provider_errors: list[dict[str, Any]] = []
    request_metadata: list[dict[str, Any]] = []
    total_cost: float = 0.0
    budget_exhausted = False

    for variant in config.variants:
        for task in selected_tasks:
            if budget_exhausted:
                continue

            est_cost = variant.estimated_cost_per_task_usd
            if total_cost + est_cost > config.budget_cap_usd:
                budget_exhausted = True
                continue

            task_payload = _build_xendris_task(task) if variant.use_xendris_wrapper else task

            meta = {
                "run_id": config.run_id,
                "variant_name": variant.variant_name,
                "provider_name": variant.provider_name,
                "model_name": variant.model_name,
                "task_id": task.get("task_id", ""),
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "dataset_hash": ds_hash,
                "manifest_hash": manifest_h,
                "use_xendris_wrapper": variant.use_xendris_wrapper,
            }
            request_metadata.append(meta)

            start = perf_counter()
            try:
                result = base_adapter(variant, task_payload, config)
                latency_ms = round((perf_counter() - start) * 1000, 3)
                raw_text = getattr(result, "raw_response_text", result if isinstance(result, str) else "")
                cost = getattr(result, "estimated_cost_usd", est_cost) or est_cost
                total_cost += cost
                records.append({
                    "run_id": config.run_id,
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": getattr(result, "provider_reported_model", variant.model_name),
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
                    "budget_status": "WITHIN_BUDGET" if not budget_exhausted else "BUDGET_EXHAUSTED",
                    "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                    "use_xendris_wrapper": variant.use_xendris_wrapper,
                })
            except Exception as exc:
                latency_ms = round((perf_counter() - start) * 1000, 3)
                error_type = type(exc).__name__
                error_msg = _sanitize_error(str(exc))
                provider_errors.append({
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": variant.model_name,
                    "task_id": task.get("task_id", ""),
                    "error_type": error_type,
                    "error_message_sanitized": error_msg,
                })
                records.append({
                    "run_id": config.run_id,
                    "variant_name": variant.variant_name,
                    "provider_name": variant.provider_name,
                    "model_name": variant.model_name,
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
                    "budget_status": "WITHIN_BUDGET" if not budget_exhausted else "BUDGET_EXHAUSTED",
                    "frozen_task_hash": task.get("content_hash", task.get("task_id", "")),
                    "use_xendris_wrapper": variant.use_xendris_wrapper,
                })

    budget_decision = "WITHIN_BUDGET" if total_cost <= config.budget_cap_usd and not budget_exhausted else "BUDGET_EXHAUSTED"

    scored: list[PairedLiftScoredRecord] = []
    for r in records:
        sr = score_paired_lift_response(
            variant_name=r["variant_name"],
            provider_name=r["provider_name"],
            model_name=r["model_name"],
            task_id=r["task_id"],
            response_text=r.get("response_text", ""),
            estimated_cost_usd=r.get("estimated_cost_usd"),
        )
        scored.append(sr)

    aggregates = aggregate_by_variant(scored)
    paired_lift = compute_paired_lift(scored, aggregates)

    has_failures = any(r["status"] == "FAILED" for r in records)
    final_decision = COMPLETED if not has_failures and not budget_exhausted else PARTIAL

    summary = _build_summary(
        config, preflight, dataset, records, provider_errors, request_metadata,
        scored, aggregates, paired_lift, budget_decision, final_decision,
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
        "paired_lift": paired_lift,
        "summary": summary,
    }


def write_paired_lift_artifacts(run_result: dict[str, Any]) -> dict[str, Any]:
    summary = run_result["summary"]
    outdir = run_result["config"].output_dir
    outdir.mkdir(parents=True, exist_ok=True)

    _write_json(outdir / "summary.json", summary)
    (outdir / "report.md").write_text(
        build_paired_lift_report(summary), encoding="utf-8"
    )
    _write_jsonl(outdir / "responses.jsonl", run_result["records"])
    _write_jsonl(
        outdir / "scores.jsonl",
        [s.to_dict() for s in run_result["scored"]],
    )
    _write_json(outdir / "costs.json", {
        "total_cost_usd": summary.get("total_cost_usd"),
        "cost_by_variant": summary.get("cost_by_variant"),
        "budget_cap_usd": summary.get("budget_cap_usd"),
        "budget_decision": summary.get("budget_decision"),
    })
    _write_jsonl(outdir / "errors.jsonl", run_result["provider_errors"])
    _write_jsonl(outdir / "metadata.jsonl", run_result["request_metadata"])
    _write_json(outdir / "preflight.json", run_result["preflight"])

    gate_payload = {
        "preflight": run_result["preflight"],
        "final_decision": summary.get("final_decision"),
    }
    _write_json(outdir / "gate.json", gate_payload)

    if run_result.get("paired_lift"):
        _write_json(outdir / "paired_lift.json", run_result["paired_lift"])

    task_lifts = run_result.get("paired_lift", {}).get("task_level_lifts", [])
    if not task_lifts and run_result.get("scored"):
        from .paired_lift_scoring import compute_paired_lift
        lift_data = compute_paired_lift(run_result["scored"], run_result["aggregates"])
        task_lifts = lift_data.get("task_level_lifts", [])
    if task_lifts:
        _write_jsonl(outdir / "task_level_lift.jsonl", task_lifts)

    _check_integrity(run_result, outdir)

    return summary


def _check_integrity(run_result: dict[str, Any], outdir: Path) -> None:
    responses_count = len(run_result.get("records", []))
    scores_count = len(run_result.get("scored", []))
    integrity = {
        "responses_count": responses_count,
        "scores_count": scores_count,
        "evidence_integrity_ready": responses_count == scores_count and responses_count > 0,
        "errors_count": len(run_result.get("provider_errors", [])),
    }
    _write_json(outdir / "evidence_integrity.json", integrity)


def _load_dotenv_for_main() -> None:
    dotenv_path = Path("frontend/.env.local")
    if not dotenv_path.exists():
        return
    for line in dotenv_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip("\"'")
        if key in ("DEEPSEEK_API_KEY", "OPENAI_API_KEY", "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"):
            os.environ.setdefault(key, value)


def main() -> int:
    _load_dotenv_for_main()
    suffix = os.environ.get("FINITEXO_PAIRED_LIFT_RUN_ID_SUFFIX", "").strip()
    base_config = PairedLiftConfig()
    config = base_config.with_run_id_suffix(suffix) if suffix else base_config
    result = run_paired_xendris_lift(config)
    summary = write_paired_lift_artifacts(result)
    print(summary.get("final_decision"))
    return 0 if summary.get("final_decision") in (COMPLETED, PARTIAL) else 1


if __name__ == "__main__":
    raise SystemExit(main())
