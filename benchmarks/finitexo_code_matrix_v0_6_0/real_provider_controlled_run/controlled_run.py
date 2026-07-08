"""Real-provider controlled diagnostic run for Finitexo Code Matrix v0.6.0.

This module preserves the v0.5.x safety boundary: no mock fallback, process-env
credentials only, deterministic task ordering, diagnostic-only scoring, and no
claims beyond local diagnostic evidence.
"""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Callable, Protocol

from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized.authorized_runner import (
    sanitize_error,
)
from benchmarks.finitexo_code_matrix_v0_5.real_provider_authorized.direct_transport import (
    direct_provider_adapter,
)
from benchmarks.finitexo_code_matrix_v0_5.scoring import score_provider_responses


EXPECTED_DATASET_HASH = "a48e5da1ff9d480efea20965eea12af5b1bff2e996470ba18e6eb01fb7b3d3a4"
EXPECTED_MANIFEST_HASH = "6c1a0873bafbb23b7145b81d26c426cd70c3ab2025b1c3250cba9f11efa7152e"
READY_V057 = "REAL_PROVIDER_REPORT_ADMISSIBILITY_APPROVED_DIAGNOSTIC_ONLY"

COMPLETED = "REAL_PROVIDER_CONTROLLED_RUN_COMPLETED_DIAGNOSTIC_ONLY"
PARTIAL = "REAL_PROVIDER_CONTROLLED_RUN_PARTIAL_DIAGNOSTIC_ONLY"
BLOCKED_PREFLIGHT = "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_PREFLIGHT"
BLOCKED_BUDGET = "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_BUDGET_CAP"
BLOCKED_INSUFFICIENT_TASKS = "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_INSUFFICIENT_TASKS"
BLOCKED_PROVIDER_CONFIGURATION = "REAL_PROVIDER_CONTROLLED_RUN_BLOCKED_PROVIDER_CONFIGURATION"


@dataclass(frozen=True)
class ControlledProviderSpec:
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float
    endpoint_url: str


@dataclass(frozen=True)
class ControlledRunConfig:
    run_id: str = "finitexo_v0_6_0_real_provider_controlled_run_n30"
    execution_mode: str = "live"
    provider_mode: str = "real"
    providers: tuple[ControlledProviderSpec, ...] = field(
        default_factory=lambda: (
            ControlledProviderSpec(
                "deepseek",
                "deepseek-v4-flash",
                "DEEPSEEK_API_KEY",
                0.00035,
                "https://api.deepseek.com/chat/completions",
            ),
            ControlledProviderSpec(
                "openai",
                "gpt-4.1-nano",
                "OPENAI_API_KEY",
                0.00008,
                "https://api.openai.com/v1/chat/completions",
            ),
        )
    )
    dataset_path: Path = Path("benchmarks/finitexo_code_matrix_v0_4_3")
    readiness_summary_path: Path = Path(
        "runs/finitexo_code_matrix_v0_5_7_real_provider_report_admissibility_gate/report_admissibility_summary.json"
    )
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30")
    confirmation_env_var: str = "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"
    expected_task_count: int = 30
    budget_cap_usd: float = 0.50
    soft_target_usd: float = 0.20
    max_attempts_per_provider_task_pair: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    request_timeout_seconds: float = 45.0
    allow_mock_fallback: bool = False
    expected_dataset_hash: str = EXPECTED_DATASET_HASH
    expected_manifest_hash: str = EXPECTED_MANIFEST_HASH
    environ: dict[str, str] = field(default_factory=lambda: dict(os.environ))


@dataclass(frozen=True)
class ControlledProviderResult:
    raw_response_text: str
    normalized_response_text: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    estimated_cost_usd: float | None = None
    provider_reported_model: str | None = None


@dataclass(frozen=True)
class LoadedControlledDataset:
    dataset_path: str
    dataset_name: str
    dataset_version: str
    dataset_hash: str
    manifest_hash: str
    manifest: dict
    tasks: tuple[dict, ...]


@dataclass(frozen=True)
class ControlledProviderRecord:
    run_id: str
    provider_name: str
    model_name: str
    provider_mode: str
    task_id: str
    task_version: str
    status: str
    response_text: str
    raw_provider_response_text: str
    normalized_response_text: str
    error_type: str | None
    error_message_sanitized: str | None
    latency_ms: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    estimated_cost_usd: float | None
    budget_status: str
    created_at: str
    dataset_hash: str
    manifest_hash: str
    frozen_task_hash: str
    scoring_status: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


class ControlledProviderAdapter(Protocol):
    def __call__(
        self,
        provider: ControlledProviderSpec,
        task: dict,
        config: ControlledRunConfig,
    ) -> ControlledProviderResult:
        ...


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    text = "\n".join(json.dumps(row, ensure_ascii=False, sort_keys=True) for row in rows)
    path.write_text(text + ("\n" if rows else ""), encoding="utf-8")


def _load_dataset(config: ControlledRunConfig) -> LoadedControlledDataset:
    hashes = _load_json(config.dataset_path / "frozen_dataset_hashes.json")
    manifest = _load_json(config.dataset_path / "frozen_dataset_manifest.json")
    task_paths = sorted((config.dataset_path / "tasks").glob("frozen_task_*.json"))
    tasks = tuple(_load_json(path) for path in task_paths)
    return LoadedControlledDataset(
        dataset_path=str(config.dataset_path),
        dataset_name=manifest.get("dataset_name", "finitexo_code_matrix"),
        dataset_version=manifest.get("dataset_version", "unknown"),
        dataset_hash=hashes.get("dataset_hash", ""),
        manifest_hash=hashes.get("manifest_hash", ""),
        manifest=manifest,
        tasks=tasks,
    )


def _provider_names(config: ControlledRunConfig) -> list[str]:
    return [provider.provider_name for provider in config.providers]


def _evaluate_preflight(config: ControlledRunConfig, dataset: LoadedControlledDataset | None = None) -> tuple[bool, str, list[str], LoadedControlledDataset | None]:
    blockers: list[str] = []
    loaded = dataset
    if config.execution_mode != "live":
        blockers.append("execution_mode_not_live")
    if config.provider_mode != "real":
        blockers.append("provider_mode_not_real")
    if config.allow_mock_fallback:
        blockers.append("mock_fallback_not_allowed")
    if config.budget_cap_usd <= 0:
        blockers.append("missing_budget_cap")
    if config.max_attempts_per_provider_task_pair != 1:
        blockers.append("max_attempts_must_be_one")
    if config.temperature != 0.0:
        blockers.append("temperature_must_be_zero")
    if _provider_names(config) != ["deepseek", "openai"]:
        blockers.append("providers_must_be_exactly_deepseek_openai")
    if config.confirmation_env_var not in config.environ or config.environ.get(config.confirmation_env_var) != "true":
        blockers.append("missing_explicit_execution_confirmation")
    for provider in config.providers:
        if not config.environ.get(provider.required_env_var):
            blockers.append(f"missing_provider_key:{provider.provider_name}")
    if not config.readiness_summary_path.exists():
        blockers.append("missing_v0_5_7_readiness_summary")
    else:
        readiness = _load_json(config.readiness_summary_path)
        if readiness.get("ready_for_v0_6_0_controlled_run") is not True:
            blockers.append("v0_5_7_not_ready_for_v0_6_0")
        if readiness.get("final_decision") != READY_V057:
            blockers.append("v0_5_7_final_decision_not_approved")
    try:
        loaded = loaded or _load_dataset(config)
        if loaded.dataset_hash != config.expected_dataset_hash:
            blockers.append("dataset_hash_mismatch")
        if loaded.manifest_hash != config.expected_manifest_hash:
            blockers.append("manifest_hash_mismatch")
        if len(loaded.tasks) < config.expected_task_count:
            blockers.append("insufficient_tasks")
    except Exception as exc:
        blockers.append(f"dataset_load_failed:{type(exc).__name__}")
    if "insufficient_tasks" in blockers:
        return False, BLOCKED_INSUFFICIENT_TASKS, blockers, loaded
    if any(item.startswith("missing_provider_key") for item in blockers) or "providers_must_be_exactly_deepseek_openai" in blockers:
        return False, BLOCKED_PROVIDER_CONFIGURATION, blockers, loaded
    return not blockers, (BLOCKED_PREFLIGHT if blockers else "READY"), blockers, loaded


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _controlled_adapter(provider: ControlledProviderSpec, task: dict, config: ControlledRunConfig) -> ControlledProviderResult:
    # Reuse the authorized direct transport path by structural compatibility.
    result = direct_provider_adapter(provider, task, config)  # type: ignore[arg-type]
    return ControlledProviderResult(
        raw_response_text=result.raw_response_text,
        normalized_response_text=result.normalized_response_text,
        prompt_tokens=result.prompt_tokens,
        completion_tokens=result.completion_tokens,
        total_tokens=result.total_tokens,
        estimated_cost_usd=result.estimated_cost_usd,
        provider_reported_model=result.provider_reported_model,
    )


def _empty_result(config: ControlledRunConfig, dataset: LoadedControlledDataset | None, decision: str, blockers: list[str]) -> dict:
    task_count = len(dataset.tasks) if dataset else 0
    expected = config.expected_task_count * len(config.providers)
    return {
        "config": config,
        "dataset": dataset,
        "preflight": {
            "can_execute": False,
            "decision": decision,
            "blockers": blockers,
            "task_count": task_count,
            "task_attempts_expected": expected,
            "providers_expected": _provider_names(config),
        },
        "records": [],
        "provider_errors": [],
        "request_metadata": [],
        "provider_attempts": {
            "providers_expected": _provider_names(config),
            "providers_attempted": [],
            "providers_completed": [],
            "task_attempts_expected": expected,
            "task_attempts_attempted": 0,
            "task_attempts_skipped": expected,
        },
        "total_estimated_cost_usd": 0.0,
        "budget_decision": "BLOCKED",
        "final_decision": decision,
    }


def run_controlled_provider_benchmark(
    config: ControlledRunConfig,
    adapter: ControlledProviderAdapter | None = None,
) -> dict:
    can_execute, preflight_decision, blockers, dataset = _evaluate_preflight(config)
    if not can_execute:
        return _empty_result(config, dataset, preflight_decision, blockers)

    assert dataset is not None
    selected_tasks = dataset.tasks[: config.expected_task_count]
    estimated_projected = sum(provider.estimated_cost_per_task_usd for provider in config.providers) * len(selected_tasks)
    if estimated_projected > config.budget_cap_usd:
        return _empty_result(config, dataset, BLOCKED_BUDGET, ["projected_cost_exceeds_budget_cap"])

    call_adapter = adapter or _controlled_adapter
    records: list[ControlledProviderRecord] = []
    provider_errors: list[dict] = []
    request_metadata: list[dict] = []
    total_cost = 0.0
    budget_blocked = 0

    for provider in config.providers:
        for task in selected_tasks:
            projected_next = total_cost + provider.estimated_cost_per_task_usd
            budget_status = "WITHIN_BUDGET" if projected_next <= config.budget_cap_usd else "WOULD_EXCEED_BUDGET"
            metadata = {
                "run_id": config.run_id,
                "provider_name": provider.provider_name,
                "model_name": provider.model_name,
                "provider_mode": config.provider_mode,
                "execution_mode": config.execution_mode,
                "task_id": task["task_id"],
                "temperature": config.temperature,
                "max_tokens": config.max_tokens,
                "max_attempts": config.max_attempts_per_provider_task_pair,
                "budget_status": budget_status,
                "dataset_hash": dataset.dataset_hash,
                "manifest_hash": dataset.manifest_hash,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            request_metadata.append(metadata)
            if budget_status != "WITHIN_BUDGET":
                budget_blocked += 1
                provider_errors.append(
                    {
                        "provider_name": provider.provider_name,
                        "model_name": provider.model_name,
                        "task_id": task["task_id"],
                        "error_type": "BUDGET_CAP",
                        "error_message_sanitized": "Budget cap blocked provider execution.",
                    }
                )
                continue
            start = perf_counter()
            try:
                result = call_adapter(provider, task, config)
                latency_ms = round((perf_counter() - start) * 1000, 3)
                cost = result.estimated_cost_usd if result.estimated_cost_usd is not None else provider.estimated_cost_per_task_usd
                total_cost += cost
                normalized = result.normalized_response_text or _normalize(result.raw_response_text)
                records.append(
                    ControlledProviderRecord(
                        run_id=config.run_id,
                        provider_name=provider.provider_name,
                        model_name=result.provider_reported_model or provider.model_name,
                        provider_mode=config.provider_mode,
                        task_id=task["task_id"],
                        task_version=task.get("task_version", dataset.dataset_version),
                        status="COMPLETED",
                        response_text=normalized,
                        raw_provider_response_text=result.raw_response_text,
                        normalized_response_text=normalized,
                        error_type=None,
                        error_message_sanitized=None,
                        latency_ms=latency_ms,
                        prompt_tokens=result.prompt_tokens,
                        completion_tokens=result.completion_tokens,
                        total_tokens=result.total_tokens,
                        estimated_cost_usd=cost,
                        budget_status=budget_status,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        dataset_hash=dataset.dataset_hash,
                        manifest_hash=dataset.manifest_hash,
                        frozen_task_hash=task.get("content_hash", ""),
                        scoring_status="PENDING",
                    )
                )
            except Exception as exc:
                latency_ms = round((perf_counter() - start) * 1000, 3)
                error_type = type(exc).__name__
                error_message = sanitize_error(str(exc))
                provider_errors.append(
                    {
                        "provider_name": provider.provider_name,
                        "model_name": provider.model_name,
                        "task_id": task["task_id"],
                        "error_type": error_type,
                        "error_message_sanitized": error_message,
                    }
                )
                records.append(
                    ControlledProviderRecord(
                        run_id=config.run_id,
                        provider_name=provider.provider_name,
                        model_name=provider.model_name,
                        provider_mode=config.provider_mode,
                        task_id=task["task_id"],
                        task_version=task.get("task_version", dataset.dataset_version),
                        status="FAILED",
                        response_text="",
                        raw_provider_response_text="",
                        normalized_response_text="",
                        error_type=error_type,
                        error_message_sanitized=error_message,
                        latency_ms=latency_ms,
                        prompt_tokens=None,
                        completion_tokens=None,
                        total_tokens=None,
                        estimated_cost_usd=None,
                        budget_status=budget_status,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        dataset_hash=dataset.dataset_hash,
                        manifest_hash=dataset.manifest_hash,
                        frozen_task_hash=task.get("content_hash", ""),
                        scoring_status="PENDING",
                    )
                )

    expected_attempts = len(config.providers) * len(selected_tasks)
    completed = sum(1 for record in records if record.status == "COMPLETED")
    failed = sum(1 for record in records if record.status == "FAILED")
    if budget_blocked and not records:
        final_decision = BLOCKED_BUDGET
    elif failed or budget_blocked or completed != expected_attempts:
        final_decision = PARTIAL
    else:
        final_decision = COMPLETED
    return {
        "config": config,
        "dataset": dataset,
        "preflight": {
            "can_execute": True,
            "decision": "READY",
            "blockers": [],
            "task_count": len(selected_tasks),
            "task_attempts_expected": expected_attempts,
            "providers_expected": _provider_names(config),
        },
        "records": records,
        "provider_errors": provider_errors,
        "request_metadata": request_metadata,
        "provider_attempts": {
            "providers_expected": _provider_names(config),
            "providers_attempted": sorted({record.provider_name for record in records}),
            "providers_completed": sorted({record.provider_name for record in records if record.status == "COMPLETED"}),
            "task_attempts_expected": expected_attempts,
            "task_attempts_attempted": len(records),
            "task_attempts_skipped": expected_attempts - len(records),
            "task_attempts_budget_blocked": budget_blocked,
        },
        "total_estimated_cost_usd": round(total_cost, 8),
        "budget_decision": "WITHIN_BUDGET" if total_cost <= config.budget_cap_usd else "EXCEEDED",
        "final_decision": final_decision,
    }


def _build_summary(run_result: dict, score_rows: list[dict]) -> dict:
    config: ControlledRunConfig = run_result["config"]
    dataset: LoadedControlledDataset | None = run_result["dataset"]
    records = run_result["records"]
    provider_response_counts = Counter(record.provider_name for record in records if record.status == "COMPLETED")
    provider_score_counts = Counter(row["provider_name"] for row in score_rows)
    provider_metadata_counts = Counter(row["provider_name"] for row in run_result["request_metadata"])
    provider_costs: dict[str, float] = defaultdict(float)
    for record in records:
        if record.estimated_cost_usd is not None:
            provider_costs[record.provider_name] += record.estimated_cost_usd
    task_count = run_result["preflight"]["task_count"]
    expected = config.expected_task_count * len(config.providers)
    return {
        "gate": "finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30",
        "final_decision": run_result["final_decision"],
        "diagnostic_only": True,
        "execution_mode": config.execution_mode,
        "provider_mode": config.provider_mode,
        "dataset_name": dataset.dataset_name if dataset else None,
        "dataset_version": dataset.dataset_version if dataset else None,
        "dataset_hash": dataset.dataset_hash if dataset else None,
        "manifest_hash": dataset.manifest_hash if dataset else None,
        "dataset_hash_verified": bool(dataset and dataset.dataset_hash == config.expected_dataset_hash),
        "manifest_hash_verified": bool(dataset and dataset.manifest_hash == config.expected_manifest_hash),
        "task_count": task_count,
        "providers_expected": _provider_names(config),
        "providers_attempted": run_result["provider_attempts"]["providers_attempted"],
        "providers_completed": run_result["provider_attempts"]["providers_completed"],
        "expected_responses": expected,
        "responses_count": len([record for record in records if record.status == "COMPLETED"]),
        "scores_count": len(score_rows),
        "metadata_rows_count": len(run_result["request_metadata"]),
        "provider_response_counts": dict(sorted(provider_response_counts.items())),
        "provider_score_counts": dict(sorted(provider_score_counts.items())),
        "provider_metadata_counts": dict(sorted(provider_metadata_counts.items())),
        "budget_cap_usd": config.budget_cap_usd,
        "soft_target_usd": config.soft_target_usd,
        "actual_cost_usd": run_result["total_estimated_cost_usd"],
        "cost_breakdown_usd": {
            **{provider: round(cost, 8) for provider, cost in sorted(provider_costs.items())},
            "total": run_result["total_estimated_cost_usd"],
        },
        "budget_decision": run_result["budget_decision"],
        "preflight": run_result["preflight"],
        "provider_failure_count": len(run_result["provider_errors"]),
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
        "production_readiness_claim_authorized": False,
        "universal_benchmark_claim_authorized": False,
        "ready_for_v0_6_1_evidence_integrity": run_result["final_decision"] in {COMPLETED, PARTIAL},
    }


def _build_report(summary: dict) -> str:
    cost_total = summary["actual_cost_usd"]
    return "\n".join(
        [
            "# Finitexo Code Matrix v0.6.0 - Real Provider Controlled Run n=30",
            "",
            "## Purpose",
            "",
            "Run a controlled real-provider diagnostic benchmark with strict diagnostic-only interpretation.",
            "",
            "## Relation to v0.5.4-v0.5.7",
            "",
            "This phase follows the v0.5.4 authorized execution path, v0.5.5 evidence integrity, v0.5.6 scoring consistency, and v0.5.7 report admissibility gates.",
            "",
            "## Preflight Result",
            "",
            f"- Decision: `{summary['preflight']['decision']}`",
            f"- Blockers: `{summary['preflight']['blockers']}`",
            "",
            "## Dataset and Task Selection",
            "",
            f"- Dataset: `{summary['dataset_name']}`",
            f"- Version: `{summary['dataset_version']}`",
            f"- Task count selected: `{summary['task_count']}`",
            f"- Expected responses: `{summary['expected_responses']}`",
            "",
            "## Providers Executed",
            "",
            f"- Expected: `{summary['providers_expected']}`",
            f"- Attempted: `{summary['providers_attempted']}`",
            f"- Completed: `{summary['providers_completed']}`",
            "",
            "## Counts",
            "",
            "| Metric | Value |",
            "|---|---:|",
            f"| Responses | {summary['responses_count']} |",
            f"| Scores | {summary['scores_count']} |",
            f"| Metadata rows | {summary['metadata_rows_count']} |",
            f"| Provider failures | {summary['provider_failure_count']} |",
            "",
            "## Cost",
            "",
            f"- Budget cap USD: `{summary['budget_cap_usd']}`",
            f"- Soft target USD: `{summary['soft_target_usd']}`",
            f"- Actual cost USD: `{cost_total}`",
            f"- Budget decision: `{summary['budget_decision']}`",
            "",
            "## Scoring Summary",
            "",
            "Scores are diagnostic-only and use the existing deterministic scoring path.",
            "",
            "## Failures",
            "",
            "Provider failures are recorded in `provider_failures.json`.",
            "",
            "## Explicit Non-Authorization",
            "",
            "- No statistical claim is authorized.",
            "- No provider superiority claim is authorized.",
            "- No Xendris superiority claim is authorized.",
            "- No production readiness claim is authorized.",
            "- No universal benchmark claim is authorized.",
            "",
            "## Final Decision",
            "",
            "```txt",
            summary["final_decision"],
            "```",
            "",
            "## Next Recommended Phase",
            "",
            "v0.6.1 Real Provider Evidence Integrity Gate n=30.",
            "",
        ]
    )


def write_controlled_run_artifacts(run_result: dict) -> dict:
    config: ControlledRunConfig = run_result["config"]
    outdir = config.output_dir
    outdir.mkdir(parents=True, exist_ok=True)
    records = run_result["records"]
    scores = score_provider_responses(records)
    response_rows = [record.to_dict() for record in records]
    score_rows = [score.to_dict() for score in scores]
    summary = _build_summary(run_result, score_rows)
    costs = {
        "budget_cap_usd": config.budget_cap_usd,
        "soft_target_usd": config.soft_target_usd,
        "actual_cost_usd": summary["actual_cost_usd"],
        "cost_breakdown_usd": summary["cost_breakdown_usd"],
        "budget_decision": summary["budget_decision"],
    }
    manifest = {
        "run_id": config.run_id,
        "dataset_hash": summary["dataset_hash"],
        "manifest_hash": summary["manifest_hash"],
        "task_ids": [record.task_id for record in records] or [],
        "providers_expected": summary["providers_expected"],
        "diagnostic_only": True,
        "final_decision": summary["final_decision"],
    }
    _write_jsonl(outdir / "responses.jsonl", response_rows)
    _write_jsonl(outdir / "scores.jsonl", score_rows)
    _write_jsonl(outdir / "metadata.jsonl", run_result["request_metadata"])
    _write_json(outdir / "real_provider_costs.json", costs)
    _write_json(outdir / "provider_attempts.json", run_result["provider_attempts"])
    _write_json(outdir / "provider_failures.json", {"failures": run_result["provider_errors"]})
    _write_json(outdir / "run_manifest.json", manifest)
    _write_json(outdir / "controlled_run_summary.json", summary)
    (outdir / "controlled_run_report.md").write_text(_build_report(summary), encoding="utf-8")
    return summary


def main() -> int:
    summary = write_controlled_run_artifacts(run_controlled_provider_benchmark(ControlledRunConfig()))
    print(summary["final_decision"])
    return 0 if summary["final_decision"] == COMPLETED else 1


if __name__ == "__main__":
    raise SystemExit(main())
