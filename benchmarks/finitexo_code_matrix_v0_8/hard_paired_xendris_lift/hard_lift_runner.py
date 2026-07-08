"""Runner for v0.8.1 hard paired Xendris lift n=30."""

from __future__ import annotations

import json
import os
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Protocol

from .hard_lift_config import HardLiftConfig, HardLiftVariantSpec
from .hard_lift_gate import (
    HARD_LIFT_READY,
    HardLiftPreflight,
    evaluate_hard_lift_preflight,
)
from .hard_lift_report import build_hard_lift_report
from .hard_lift_scoring import (
    FAMILIES,
    HardLiftScoredRecord,
    HardLiftVariantAggregate,
    aggregate_by_family_variant,
    aggregate_by_variant,
    compute_family_lift,
    compute_paired_lift,
    score_hard_lift_response,
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

COMPLETED = "HARD_LIFT_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "HARD_LIFT_PARTIAL_DIAGNOSTIC_ONLY"
BLOCKED_PREFLIGHT = "HARD_LIFT_BLOCKED_PREFLIGHT"
BLOCKED_BUDGET = "HARD_LIFT_BLOCKED_BUDGET"

AUTHORIZED_CLAIMS = [
    "Real providers executed under controlled hard paired conditions.",
    "Hard programming dataset n=30 was used.",
    "Xendris wrapper was applied consistently to paired variants.",
    "Diagnostic scores were computed using the documented scorer.",
    "Paired lift was measured on this hard n=30 controlled dataset.",
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


class HardLiftProviderAdapter(Protocol):
    def __call__(self, provider: HardLiftVariantSpec, task: dict, config: HardLiftConfig) -> Any: ...


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


def _load_dataset(config: HardLiftConfig) -> dict[str, Any]:
    hash_path = config.dataset_path / "dataset_hashes.json"
    manifest_path = config.dataset_path / "dataset_manifest.json"
    tasks_dir = config.dataset_path / "tasks"

    hashes = _load_json(hash_path) if hash_path.exists() else {}
    manifest = _load_json(manifest_path) if manifest_path.exists() else {}
    task_paths = sorted(tasks_dir.glob("task_*.json")) if tasks_dir.exists() else []
    tasks = [_load_json(p) for p in task_paths]

    return {
        "dataset_name": manifest.get("dataset_name", "finitexo_code_matrix_hard_programming_n30"),
        "dataset_version": manifest.get("dataset_version", "0.8.0"),
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
    config: HardLiftConfig,
    preflight: HardLiftPreflight,
    dataset: dict[str, Any],
    records: list[dict[str, Any]],
    provider_errors: list[dict[str, Any]],
    metadata: list[dict[str, Any]],
    scored: list[HardLiftScoredRecord],
    aggregates: list[HardLiftVariantAggregate],
    paired_lift: dict[str, Any],
    family_lift: dict[str, Any],
    budget_decision: str,
    final_decision: str,
) -> dict[str, Any]:
    total_attempts = len(records)
    total_completed = sum(1 for r in records if r.get("status") == "COMPLETED")
    total_failed = sum(1 for r in records if r.get("status") == "FAILED")
    total_cost = sum(r.get("estimated_cost_usd") or 0.0 for r in records)

    cost_by_variant: dict[str, float] = defaultdict(float)
    for r in records:
        cost_by_variant[r.get("variant_name", "unknown")] += r.get("estimated_cost_usd") or 0.0

    return {
        "run_id": config.run_id,
        "benchmark_name": "Finitexo Code Matrix",
        "benchmark_version": "v0.8.1",
        "experiment_type": "hard_paired_xendris_lift",
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
        "family_lift": {k: round(v, 6) if isinstance(v, float) else v for k, v in family_lift.items()}
        if isinstance(family_lift.get("overall_deepseek_lift_by_family_mean"), float) else family_lift,
        "authorized_claims": list(AUTHORIZED_CLAIMS),
        "prohibited_claims": list(PROHIBITED_CLAIMS),
        "preflight_decision": preflight.decision,
        "preflight_blockers": list(preflight.blockers),
        "final_decision": final_decision,
    }


def _empty_result(
    config: HardLiftConfig,
    dataset: dict[str, Any],
    preflight: HardLiftPreflight,
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
        "family_lift": {},
        "summary": _build_summary(
            config, preflight, dataset, [], [], [], [], [], {}, {},
            "BLOCKED", final_decision,
        ),
    }


def run_hard_paired_xendris_lift(
    config: HardLiftConfig,
    adapter: HardLiftProviderAdapter | None = None,
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

    preflight = evaluate_hard_lift_preflight(config, ds_hash, manifest_h, task_cnt)
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
            task_family = task.get("family", "unknown")

            meta = {
                "run_id": config.run_id,
                "variant_name": variant.variant_name,
                "provider_name": variant.provider_name,
                "model_name": variant.model_name,
                "task_id": task.get("task_id", ""),
                "task_family": task_family,
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
                    "task_family": task_family,
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
                    "task_family": task_family,
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
                    "task_family": task_family,
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

    scored: list[HardLiftScoredRecord] = []
    for r in records:
        sr = score_hard_lift_response(
            variant_name=r["variant_name"],
            provider_name=r["provider_name"],
            model_name=r["model_name"],
            task_id=r["task_id"],
            task_family=r.get("task_family", "unknown"),
            response_text=r.get("response_text", ""),
            estimated_cost_usd=r.get("estimated_cost_usd"),
        )
        scored.append(sr)

    aggregates = aggregate_by_variant(scored)
    paired_lift = compute_paired_lift(scored, aggregates)
    family_lift = compute_family_lift(scored)

    has_failures = any(r["status"] == "FAILED" for r in records)
    final_decision = COMPLETED if not has_failures and not budget_exhausted else PARTIAL

    summary = _build_summary(
        config, preflight, dataset, records, provider_errors, request_metadata,
        scored, aggregates, paired_lift, family_lift, budget_decision, final_decision,
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
        "family_lift": family_lift,
        "summary": summary,
    }


def write_hard_lift_artifacts(run_result: dict[str, Any]) -> dict[str, Any]:
    summary = run_result["summary"]
    outdir = run_result["config"].output_dir
    outdir.mkdir(parents=True, exist_ok=True)

    _write_json(outdir / "summary.json", summary)
    (outdir / "report.md").write_text(
        build_hard_lift_report(summary), encoding="utf-8"
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
    _write_json(outdir / "gate.json", {
        "preflight": run_result["preflight"],
        "final_decision": summary.get("final_decision"),
    })

    if run_result.get("paired_lift"):
        _write_json(outdir / "paired_lift.json", run_result["paired_lift"])

    task_lifts = run_result.get("paired_lift", {}).get("task_level_lifts", [])
    if not task_lifts and run_result.get("scored"):
        lift_data = compute_paired_lift(run_result["scored"], run_result["aggregates"])
        task_lifts = lift_data.get("task_level_lifts", [])
    if task_lifts:
        _write_jsonl(outdir / "task_level_lift.jsonl", task_lifts)

    if run_result.get("family_lift"):
        _write_json(outdir / "family_lift.json", run_result["family_lift"])

    _check_integrity(run_result, outdir)

    return summary


def _check_integrity(run_result: dict[str, Any], outdir: Path) -> None:
    records = run_result.get("records", [])
    scored = run_result.get("scored", [])
    metadata = run_result.get("request_metadata", [])
    task_lifts = run_result.get("paired_lift", {}).get("task_level_lifts", [])
    errors = run_result.get("provider_errors", [])

    responses_count = len(records)
    scores_count = len(scored)
    metadata_count = len(metadata)
    task_lift_count = len(task_lifts)

    integrity = {
        "responses_count": responses_count,
        "scores_count": scores_count,
        "metadata_count": metadata_count,
        "task_level_lift_count": task_lift_count,
        "errors_count": len(errors),
        "responses_match_120": responses_count == 120,
        "scores_match_120": scores_count == 120,
        "metadata_match_120": metadata_count == 120,
        "task_level_lifts_match_30": task_lift_count == 30,
        "evidence_integrity_ready": (
            responses_count == 120
            and scores_count == 120
            and metadata_count == 120
            and task_lift_count == 30
        ),
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
    suffix = os.environ.get("FINITEXO_HARD_LIFT_RUN_ID_SUFFIX", "").strip()
    base_config = HardLiftConfig()
    config = base_config.with_run_id_suffix(suffix) if suffix else base_config
    result = run_hard_paired_xendris_lift(config)
    summary = write_hard_lift_artifacts(result)
    print(summary.get("final_decision"))
    return 0 if summary.get("final_decision") in (COMPLETED, PARTIAL) else 1


if __name__ == "__main__":
    raise SystemExit(main())
