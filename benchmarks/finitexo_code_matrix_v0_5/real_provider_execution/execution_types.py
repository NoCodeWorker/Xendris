"""Types for v0.5.2 real-provider execution records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RealProviderExecutionRecord:
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

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
