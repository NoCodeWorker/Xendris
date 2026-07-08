"""Preflight gate for v0.6.0 controlled run n=30."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .controlled_run_config import ControlledRunConfig


READY_V057 = "REAL_PROVIDER_REPORT_ADMISSIBILITY_APPROVED_DIAGNOSTIC_ONLY"
CONTROLLED_RUN_READY = "CONTROLLED_RUN_PREFLIGHT_READY"
BLOCKED_PREFLIGHT = "CONTROLLED_RUN_BLOCKED_PREFLIGHT"


@dataclass(frozen=True)
class ControlledRunPreflight:
    can_execute: bool
    decision: str
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    dataset_hash: str | None
    manifest_hash: str | None
    task_count: int | None
    task_attempts_expected: int
    providers_configured: list[str]
    provider_key_status: dict[str, str]
    confirmation_status: str
    readiness_decision: str | None
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
            "task_attempts_expected": self.task_attempts_expected,
            "providers_configured": self.providers_configured,
            "provider_key_status": self.provider_key_status,
            "confirmation_status": self.confirmation_status,
            "readiness_decision": self.readiness_decision,
            "budget_cap_usd": self.budget_cap_usd,
        }


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _provider_names(config: ControlledRunConfig) -> list[str]:
    return [p.provider_name for p in config.providers]


def evaluate_controlled_run_preflight(
    config: ControlledRunConfig,
    dataset_hash: str | None = None,
    manifest_hash: str | None = None,
    task_count: int | None = None,
) -> ControlledRunPreflight:
    blockers: list[str] = []
    warnings: list[str] = []

    if config.provider_mode != "real":
        blockers.append("provider_mode_not_real")
    if config.allow_mock_fallback:
        blockers.append("mock_fallback_not_allowed")
    if config.max_attempts_per_provider_task_pair != 1:
        blockers.append("max_attempts_must_be_one")
    if config.temperature != 0.0:
        blockers.append("temperature_must_be_zero")
    if config.budget_cap_usd <= 0:
        blockers.append("missing_budget_cap")
    if config.expected_task_count <= 0:
        blockers.append("invalid_expected_task_count")

    # Provider key checks
    provider_key_status: dict[str, str] = {}
    for provider in config.providers:
        key_present = bool(config.environ.get(provider.required_env_var))
        provider_key_status[provider.provider_name] = "PRESENT" if key_present else "MISSING"
        if not key_present:
            blockers.append(f"missing_provider_key:{provider.provider_name}")

    # Confirmation env var
    confirmation_val = config.environ.get(config.confirmation_env_var, "")
    confirmation_status = "PRESENT" if confirmation_val.lower() == "true" else "MISSING"
    if confirmation_status != "PRESENT":
        blockers.append("missing_explicit_execution_confirmation")

    # Readiness gate from v0.5.7
    readiness_decision: str | None = None
    if not config.readiness_summary_path.exists():
        blockers.append("missing_v0_5_7_readiness_summary")
    else:
        readiness = _load_json(config.readiness_summary_path)
        readiness_decision = readiness.get("final_decision", "UNKNOWN")
        if readiness_decision != READY_V057:
            blockers.append("v0_5_7_final_decision_not_approved")
        if readiness.get("ready_for_v0_6_0_controlled_run") is not True:
            blockers.append("v0_5_7_not_ready_for_v0_6_0")

    # Dataset checks
    ds_hash = dataset_hash
    manifest_h = manifest_hash
    task_cnt = task_count
    if task_cnt is not None and task_cnt < config.expected_task_count:
        blockers.append("insufficient_tasks")
    if config.expected_dataset_hash and ds_hash and ds_hash != config.expected_dataset_hash:
        blockers.append("dataset_hash_mismatch")
    if config.expected_manifest_hash and manifest_h and manifest_h != config.expected_manifest_hash:
        blockers.append("manifest_hash_mismatch")

    # Output dir overwrite check
    if config.output_dir.exists() and any(config.output_dir.iterdir()) and not config.allow_overwrite:
        blockers.append("output_dir_not_empty_and_overwrite_not_allowed")

    task_attempts_expected = len(config.providers) * config.expected_task_count
    decision = CONTROLLED_RUN_READY if not blockers else BLOCKED_PREFLIGHT

    return ControlledRunPreflight(
        can_execute=not blockers,
        decision=decision,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        dataset_hash=ds_hash,
        manifest_hash=manifest_h,
        task_count=task_cnt,
        task_attempts_expected=task_attempts_expected,
        providers_configured=_provider_names(config),
        provider_key_status=provider_key_status,
        confirmation_status=confirmation_status,
        readiness_decision=readiness_decision,
        budget_cap_usd=config.budget_cap_usd,
    )
