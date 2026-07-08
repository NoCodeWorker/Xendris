"""Runner for v0.5.1 real-provider smoke execution.

Provider calls are injected through adapters. The default path performs only
gate evaluation and artifact generation; tests use stub adapters to exercise
real-mode semantics without network access.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
from typing import Callable, Protocol

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.budget_guard import BudgetDecision, BudgetGuard
from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import load_frozen_dataset
from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.smoke_types import ProviderResponseRecord

from .real_provider_gate import evaluate_real_provider_gate
from .real_smoke_config import RealProviderSpec, RealSmokeConfig


@dataclass(frozen=True)
class RealProviderCallResult:
    response_text: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    estimated_cost_usd: float | None = None
    provider_reported_model: str | None = None


class RealProviderAdapter(Protocol):
    def __call__(self, provider: RealProviderSpec, task: dict, config: RealSmokeConfig) -> RealProviderCallResult:
        ...


def _sanitize_error(message: str | None) -> str | None:
    if message is None:
        return None
    return message.replace("sk-", "[redacted-key-prefix]").replace("Bearer ", "[redacted-bearer] ")


def _missing_adapter(_: RealProviderSpec, __: dict, ___: RealSmokeConfig) -> RealProviderCallResult:
    raise RuntimeError("real provider adapter is not configured")


def run_real_provider_smoke(
    config: RealSmokeConfig,
    adapter: RealProviderAdapter | None = None,
    gate_evaluator: Callable[[RealSmokeConfig], object] = evaluate_real_provider_gate,
) -> dict:
    gate = gate_evaluator(config)
    dataset = load_frozen_dataset(config.dataset_path)
    records: list[ProviderResponseRecord] = []
    provider_errors: list[dict] = []
    skipped = 0
    budget_blocked = 0
    guard = BudgetGuard(config.budget_cap_usd)

    if not gate.can_execute:
        return {
            "config": config,
            "dataset": dataset,
            "gate": gate,
            "records": records,
            "provider_errors": provider_errors,
            "task_attempts_skipped": len(config.providers) * len(dataset.tasks),
            "task_attempts_budget_blocked": 0,
            "total_estimated_cost_usd": 0.0,
            "budget_decision": "BLOCKED",
            "mock_fallback_used": False,
        }

    call_adapter = adapter or _missing_adapter
    for provider in config.providers:
        for task in dataset.tasks:
            budget_status = guard.check_before_task(provider.estimated_cost_per_task_usd)
            if budget_status in {
                BudgetDecision.WOULD_EXCEED_BUDGET,
                BudgetDecision.BUDGET_EXHAUSTED,
                BudgetDecision.BLOCKED,
            }:
                budget_blocked += 1
                provider_errors.append(
                    {
                        "provider_name": provider.provider_name,
                        "model_name": provider.model_name,
                        "task_id": task["task_id"],
                        "error_type": budget_status.value,
                        "error_message_sanitized": "Budget guard blocked task before provider execution.",
                    }
                )
                if config.stop_on_budget_exhaustion:
                    continue
            start = perf_counter()
            try:
                result = call_adapter(provider, task, config)
                latency_ms = round((perf_counter() - start) * 1000, 3)
                estimated_cost = (
                    result.estimated_cost_usd
                    if result.estimated_cost_usd is not None
                    else provider.estimated_cost_per_task_usd
                )
                guard.record_cost(estimated_cost)
                records.append(
                    ProviderResponseRecord(
                        run_id=config.run_id,
                        provider_name=provider.provider_name,
                        model_name=result.provider_reported_model or provider.model_name,
                        provider_mode=config.provider_mode,
                        task_id=task["task_id"],
                        task_version=task["task_version"],
                        status="COMPLETED",
                        response_text=result.response_text,
                        error_type=None,
                        error_message_sanitized=None,
                        latency_ms=latency_ms,
                        prompt_tokens=result.prompt_tokens,
                        completion_tokens=result.completion_tokens,
                        total_tokens=result.total_tokens,
                        estimated_cost_usd=estimated_cost,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        dataset_hash=dataset.dataset_hash,
                        manifest_hash=dataset.manifest_hash,
                        frozen_task_hash=task["content_hash"],
                        scoring_status="PENDING",
                    )
                )
            except Exception as exc:
                latency_ms = round((perf_counter() - start) * 1000, 3)
                error_type = type(exc).__name__
                error_message = _sanitize_error(str(exc))
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
                    ProviderResponseRecord(
                        run_id=config.run_id,
                        provider_name=provider.provider_name,
                        model_name=provider.model_name,
                        provider_mode=config.provider_mode,
                        task_id=task["task_id"],
                        task_version=task["task_version"],
                        status="FAILED",
                        response_text="",
                        error_type=error_type,
                        error_message_sanitized=error_message,
                        latency_ms=latency_ms,
                        prompt_tokens=None,
                        completion_tokens=None,
                        total_tokens=None,
                        estimated_cost_usd=None,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        dataset_hash=dataset.dataset_hash,
                        manifest_hash=dataset.manifest_hash,
                        frozen_task_hash=task["content_hash"],
                        scoring_status="PENDING",
                    )
                )
                if not config.allow_partial_provider_failure:
                    skipped += len(dataset.tasks) - (len(records) % len(dataset.tasks))
                    break

    budget_decision = (
        BudgetDecision.BUDGET_EXHAUSTED.value
        if guard.total_estimated_cost_usd >= config.budget_cap_usd
        else BudgetDecision.WITHIN_BUDGET.value
    )
    return {
        "config": config,
        "dataset": dataset,
        "gate": gate,
        "records": records,
        "provider_errors": provider_errors,
        "task_attempts_skipped": skipped,
        "task_attempts_budget_blocked": budget_blocked,
        "total_estimated_cost_usd": round(guard.total_estimated_cost_usd, 8),
        "budget_decision": budget_decision,
        "mock_fallback_used": False,
    }
