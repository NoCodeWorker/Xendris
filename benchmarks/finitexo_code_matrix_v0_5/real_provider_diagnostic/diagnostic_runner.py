"""Diagnostic-only real-provider execution runner for v0.5.3."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter
from typing import Callable, Protocol

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.budget_guard import BudgetDecision, BudgetGuard
from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import load_frozen_dataset

from .diagnostic_config import DiagnosticProviderSpec, RealProviderDiagnosticConfig
from .diagnostic_gate import evaluate_diagnostic_preflight
from .diagnostic_types import DiagnosticProviderRecord


@dataclass(frozen=True)
class DiagnosticProviderResult:
    raw_response_text: str
    normalized_response_text: str | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    total_tokens: int | None = None
    estimated_cost_usd: float | None = None
    provider_reported_model: str | None = None


class DiagnosticProviderAdapter(Protocol):
    def __call__(
        self,
        provider: DiagnosticProviderSpec,
        task: dict,
        config: RealProviderDiagnosticConfig,
    ) -> DiagnosticProviderResult:
        ...


def sanitize_error(message: str | None) -> str | None:
    if message is None:
        return None
    return message.replace("sk-", "[redacted-key-prefix]").replace("Bearer ", "[redacted-bearer] ")


def normalize_response_text(text: str) -> str:
    return " ".join(text.split())


def _missing_adapter(_: DiagnosticProviderSpec, __: dict, ___: RealProviderDiagnosticConfig) -> DiagnosticProviderResult:
    raise RuntimeError("real provider diagnostic adapter is not configured")


def run_real_provider_diagnostic(
    config: RealProviderDiagnosticConfig,
    adapter: DiagnosticProviderAdapter | None = None,
    preflight_evaluator: Callable[[RealProviderDiagnosticConfig], object] = evaluate_diagnostic_preflight,
) -> dict:
    preflight = preflight_evaluator(config)
    dataset = load_frozen_dataset(config.dataset_path)
    guard = BudgetGuard(config.budget_cap_usd)
    records: list[DiagnosticProviderRecord] = []
    provider_errors: list[dict] = []
    request_metadata: list[dict] = []
    budget_blocked = 0

    if not preflight.can_execute:
        return {
            "config": config,
            "dataset": dataset,
            "preflight": preflight,
            "records": records,
            "provider_errors": provider_errors,
            "request_metadata": request_metadata,
            "task_attempts_expected": preflight.task_attempts_expected,
            "task_attempts_skipped": preflight.task_attempts_expected,
            "task_attempts_budget_blocked": 0,
            "total_estimated_cost_usd": 0.0,
            "budget_decision": "BLOCKED",
            "mock_fallback_used": False,
        }

    call_adapter = adapter or _missing_adapter
    for provider in config.providers:
        for task in dataset.tasks:
            budget_status = guard.check_before_task(provider.estimated_cost_per_task_usd)
            request_metadata.append(
                {
                    "run_id": config.run_id,
                    "provider_name": provider.provider_name,
                    "model_name": provider.model_name,
                    "provider_mode": config.provider_mode,
                    "task_id": task["task_id"],
                    "temperature": config.temperature,
                    "max_tokens": config.max_tokens,
                    "max_attempts": config.max_attempts_per_provider_task_pair,
                    "budget_status": budget_status.value,
                    "dataset_hash": dataset.dataset_hash,
                    "manifest_hash": dataset.manifest_hash,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )
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
                continue

            start = perf_counter()
            try:
                result = call_adapter(provider, task, config)
                latency_ms = round((perf_counter() - start) * 1000, 3)
                normalized = result.normalized_response_text or normalize_response_text(result.raw_response_text)
                estimated_cost = (
                    result.estimated_cost_usd
                    if result.estimated_cost_usd is not None
                    else provider.estimated_cost_per_task_usd
                )
                guard.record_cost(estimated_cost)
                records.append(
                    DiagnosticProviderRecord(
                        run_id=config.run_id,
                        provider_name=provider.provider_name,
                        model_name=result.provider_reported_model or provider.model_name,
                        provider_mode=config.provider_mode,
                        task_id=task["task_id"],
                        task_version=task["task_version"],
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
                        estimated_cost_usd=estimated_cost,
                        budget_status=budget_status.value,
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
                    DiagnosticProviderRecord(
                        run_id=config.run_id,
                        provider_name=provider.provider_name,
                        model_name=provider.model_name,
                        provider_mode=config.provider_mode,
                        task_id=task["task_id"],
                        task_version=task["task_version"],
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
                        budget_status=budget_status.value,
                        created_at=datetime.now(timezone.utc).isoformat(),
                        dataset_hash=dataset.dataset_hash,
                        manifest_hash=dataset.manifest_hash,
                        frozen_task_hash=task["content_hash"],
                        scoring_status="PENDING",
                    )
                )

    return {
        "config": config,
        "dataset": dataset,
        "preflight": preflight,
        "records": records,
        "provider_errors": provider_errors,
        "request_metadata": request_metadata,
        "task_attempts_expected": preflight.task_attempts_expected,
        "task_attempts_skipped": 0,
        "task_attempts_budget_blocked": budget_blocked,
        "total_estimated_cost_usd": round(guard.total_estimated_cost_usd, 8),
        "budget_decision": (
            BudgetDecision.BUDGET_EXHAUSTED.value
            if guard.total_estimated_cost_usd >= config.budget_cap_usd
            else BudgetDecision.WITHIN_BUDGET.value
        ),
        "mock_fallback_used": False,
    }
