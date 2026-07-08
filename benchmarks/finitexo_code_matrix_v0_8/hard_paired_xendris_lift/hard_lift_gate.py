"""Preflight gate for v0.8.1 hard paired Xendris lift n=30."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .hard_lift_config import HardLiftConfig


HARD_LIFT_READY = "HARD_LIFT_PREFLIGHT_READY"
BLOCKED_PREFLIGHT = "HARD_LIFT_BLOCKED_PREFLIGHT"


@dataclass(frozen=True)
class HardLiftPreflight:
    can_execute: bool
    decision: str
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    dataset_hash: str | None
    manifest_hash: str | None
    task_count: int | None
    expected_attempts: int
    variants_configured: list[str]
    provider_key_status: dict[str, str]
    confirmation_status: str
    budget_cap_usd: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "can_execute": self.can_execute,
            "decision": self.decision,
            "blockers": list(self.blockers),
            "warnings": list(self.warnings),
            "dataset_hash": self.dataset_hash,
            "manifest_hash": self.manifest_hash,
            "task_count": self.task_count,
            "expected_attempts": self.expected_attempts,
            "variants_configured": self.variants_configured,
            "provider_key_status": self.provider_key_status,
            "confirmation_status": self.confirmation_status,
            "budget_cap_usd": self.budget_cap_usd,
        }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_hard_lift_preflight(
    config: HardLiftConfig,
    dataset_hash: str | None = None,
    manifest_hash: str | None = None,
    task_count: int | None = None,
) -> HardLiftPreflight:
    blockers: list[str] = []
    warnings: list[str] = []

    if config.provider_mode != "real":
        blockers.append("provider_mode_not_real")
    if config.allow_mock_fallback:
        blockers.append("mock_fallback_not_allowed")
    if config.max_attempts_per_task_pair != 1:
        blockers.append("max_attempts_per_task_pair_must_be_one")
    if config.temperature != 0.0:
        blockers.append("temperature_must_be_zero")
    if config.budget_cap_usd <= 0:
        blockers.append("missing_budget_cap")
    if config.expected_task_count <= 0:
        blockers.append("invalid_expected_task_count")

    provider_key_status: dict[str, str] = {}
    configured_providers = sorted({v.provider_name for v in config.variants})
    for provider_name in configured_providers:
        env_var = _required_env_for_provider(config, provider_name)
        key_present = bool(config.environ.get(env_var))
        provider_key_status[provider_name] = "PRESENT" if key_present else "MISSING"
        if not key_present:
            blockers.append(f"missing_provider_key:{provider_name}")

    confirmation_val = config.environ.get(config.confirmation_env_var, "")
    confirmation_status = "PRESENT" if confirmation_val.lower() == "true" else "MISSING"
    if confirmation_status != "PRESENT":
        blockers.append("missing_explicit_execution_confirmation")

    ds_hash = dataset_hash
    manifest_h = manifest_hash
    task_cnt = task_count

    if not config.dataset_path.exists():
        blockers.append("dataset_path_missing")
    if task_cnt is not None and task_cnt < config.expected_task_count:
        blockers.append("insufficient_tasks")
    if config.expected_dataset_hash and ds_hash and ds_hash != config.expected_dataset_hash:
        blockers.append("dataset_hash_mismatch")
    if config.expected_manifest_hash and manifest_h and manifest_h != config.expected_manifest_hash:
        blockers.append("manifest_hash_mismatch")

    expected_attempts = len(config.variants) * config.expected_task_count
    if config.expected_attempts != expected_attempts:
        blockers.append("expected_attempts_mismatch")

    if config.output_dir.exists() and any(config.output_dir.iterdir()) and not config.allow_overwrite:
        blockers.append("output_dir_not_empty_and_overwrite_not_allowed")

    decision = HARD_LIFT_READY if not blockers else BLOCKED_PREFLIGHT

    return HardLiftPreflight(
        can_execute=not blockers,
        decision=decision,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        dataset_hash=ds_hash,
        manifest_hash=manifest_h,
        task_count=task_cnt,
        expected_attempts=expected_attempts,
        variants_configured=[v.variant_name for v in config.variants],
        provider_key_status=provider_key_status,
        confirmation_status=confirmation_status,
        budget_cap_usd=config.budget_cap_usd,
    )


def _required_env_for_provider(config: HardLiftConfig, provider_name: str) -> str:
    for v in config.variants:
        if v.provider_name == provider_name:
            return v.required_env_var
    return ""
