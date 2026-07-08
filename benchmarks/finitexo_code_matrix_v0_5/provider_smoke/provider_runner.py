"""Conservative provider smoke runner."""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter

from .budget_guard import BudgetDecision, BudgetGuard
from .dataset_loader import load_frozen_dataset
from .smoke_config import SmokeConfig
from .smoke_types import ProviderResponseRecord


def _sanitize_error(message: str | None) -> str | None:
    if message is None:
        return None
    return message.replace("sk-", "[redacted-key-prefix]")


def _mock_response(task: dict) -> str:
    return (
        f"Proposed diagnostic response for {task['task_id']}. "
        "Preserve the public API contract, avoid touching forbidden files, "
        "and treat this as smoke output rather than verified benchmark success."
    )


def run_provider_smoke(config: SmokeConfig) -> dict:
    config.validate()
    dataset = load_frozen_dataset(config.dataset_path)
    guard = BudgetGuard(config.budget_cap_usd)
    records: list[ProviderResponseRecord] = []
    provider_errors: list[dict] = []
    projected_cost = 0.00001 if config.provider_mode == "mock" else None

    for provider in config.providers:
        model = config.provider_models.get(provider, "unknown-model")
        for task in dataset.tasks:
            decision = guard.check_before_task(projected_cost)
            if decision in {BudgetDecision.WOULD_EXCEED_BUDGET, BudgetDecision.BUDGET_EXHAUSTED, BudgetDecision.BLOCKED}:
                provider_errors.append(
                    {
                        "provider_name": provider,
                        "task_id": task["task_id"],
                        "error_type": decision.value,
                        "error_message_sanitized": "Budget guard blocked task before provider execution.",
                    }
                )
                continue
            start = perf_counter()
            try:
                if config.provider_mode != "mock":
                    raise RuntimeError("real provider mode is not configured in this smoke run")
                response_text = _mock_response(task)
                status = "COMPLETED"
                error_type = None
                error_message = None
                prompt_tokens = len(task["prompt"].split())
                completion_tokens = len(response_text.split())
                total_tokens = prompt_tokens + completion_tokens
                estimated_cost = projected_cost
            except Exception as exc:  # pragma: no cover - defensive path
                response_text = ""
                status = "FAILED"
                error_type = type(exc).__name__
                error_message = _sanitize_error(str(exc))
                prompt_tokens = None
                completion_tokens = None
                total_tokens = None
                estimated_cost = None
                provider_errors.append(
                    {
                        "provider_name": provider,
                        "task_id": task["task_id"],
                        "error_type": error_type,
                        "error_message_sanitized": error_message,
                    }
                )
            latency_ms = round((perf_counter() - start) * 1000, 3)
            guard.record_cost(estimated_cost)
            records.append(
                ProviderResponseRecord(
                    run_id=config.run_id,
                    provider_name=provider,
                    model_name=model,
                    provider_mode=config.provider_mode,
                    task_id=task["task_id"],
                    task_version=task["task_version"],
                    status=status,
                    response_text=response_text,
                    error_type=error_type,
                    error_message_sanitized=error_message,
                    latency_ms=latency_ms,
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=total_tokens,
                    estimated_cost_usd=estimated_cost,
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
        "records": records,
        "provider_errors": provider_errors,
        "total_estimated_cost_usd": round(guard.total_estimated_cost_usd, 8),
        "budget_decision": BudgetDecision.WITHIN_BUDGET.value,
    }
