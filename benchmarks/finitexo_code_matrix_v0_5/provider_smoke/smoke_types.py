"""Types for provider smoke execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ProviderMode(str, Enum):
    MOCK = "mock"
    REAL = "real"


class SmokeStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class LoadedFrozenDataset:
    dataset_path: str
    dataset_version: str
    dataset_hash: str
    manifest_hash: str
    manifest: dict[str, Any]
    tasks: tuple[dict[str, Any], ...]
    hashes: dict[str, Any]


@dataclass(frozen=True)
class ProviderResponseRecord:
    run_id: str
    provider_name: str
    model_name: str
    provider_mode: str
    task_id: str
    task_version: str
    status: str
    response_text: str
    error_type: str | None
    error_message_sanitized: str | None
    latency_ms: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    estimated_cost_usd: float | None
    created_at: str
    dataset_hash: str
    manifest_hash: str
    frozen_task_hash: str
    scoring_status: str

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()
