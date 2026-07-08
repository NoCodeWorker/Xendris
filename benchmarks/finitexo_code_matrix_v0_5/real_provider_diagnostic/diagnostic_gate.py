"""Preflight gate for v0.5.3 real-provider diagnostic execution."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import (
    EXPECTED_DATASET_HASH,
    EXPECTED_MANIFEST_HASH,
    load_frozen_dataset,
)

from .diagnostic_config import RealProviderDiagnosticConfig


RELEASE_GATE_APPROVED = "APPROVED_FOR_EXPLICIT_REAL_PROVIDER_DIAGNOSTIC_EXECUTION"
BLOCKED_PRECONDITION = "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_BLOCKED_PRECONDITION_MISSING"
READY_DECISION = "REAL_PROVIDER_DIAGNOSTIC_EXECUTION_PREFLIGHT_READY"


@dataclass(frozen=True)
class DiagnosticPreflightResult:
    decision: str
    can_execute: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    release_gate_decision: str | None
    provider_key_status: dict[str, str]
    confirmation_status: str
    dataset_hash: str | None
    manifest_hash: str | None
    frozen_task_count: int | None
    task_attempts_expected: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "can_execute": self.can_execute,
            "blockers": list(self.blockers),
            "warnings": list(self.warnings),
            "release_gate_decision": self.release_gate_decision,
            "provider_key_status": self.provider_key_status,
            "confirmation_status": self.confirmation_status,
            "dataset_hash": self.dataset_hash,
            "manifest_hash": self.manifest_hash,
            "frozen_task_count": self.frozen_task_count,
            "task_attempts_expected": self.task_attempts_expected,
        }


def _load_release_gate_decision(config: RealProviderDiagnosticConfig) -> tuple[str | None, str | None]:
    if not config.release_gate_summary_path.exists():
        return None, "release gate summary missing"
    data = json.loads(config.release_gate_summary_path.read_text(encoding="utf-8"))
    return data.get("decision"), None


def evaluate_diagnostic_preflight(config: RealProviderDiagnosticConfig) -> DiagnosticPreflightResult:
    blockers = config.validate_static_boundaries()
    warnings: list[str] = []
    dataset_hash: str | None = None
    manifest_hash: str | None = None
    frozen_task_count: int | None = None

    try:
        dataset = load_frozen_dataset(config.dataset_path)
        dataset_hash = dataset.dataset_hash
        manifest_hash = dataset.manifest_hash
        frozen_task_count = len(dataset.tasks)
        if dataset_hash != EXPECTED_DATASET_HASH:
            blockers.append("dataset hash mismatch")
        if manifest_hash != EXPECTED_MANIFEST_HASH:
            blockers.append("manifest hash mismatch")
        if frozen_task_count != 10:
            blockers.append("frozen task count mismatch")
    except Exception as exc:
        blockers.append(f"frozen dataset validation failed: {type(exc).__name__}")

    release_gate_decision, release_gate_error = _load_release_gate_decision(config)
    if release_gate_error:
        blockers.append(release_gate_error)
    elif release_gate_decision != RELEASE_GATE_APPROVED:
        blockers.append("v0.5.2 release gate is not approved")

    confirmation_value = config.environ.get(config.confirmation_env_var, "")
    confirmation_status = "PRESENT" if confirmation_value.lower() == "true" else "MISSING"
    if confirmation_status != "PRESENT":
        blockers.append(f"{config.confirmation_env_var}=true missing")

    provider_key_status = {
        provider.provider_name: "PRESENT" if bool(config.environ.get(provider.required_env_var)) else "MISSING"
        for provider in config.providers
    }
    missing = [name for name, status in provider_key_status.items() if status == "MISSING"]
    if missing:
        blockers.append(f"provider API key missing for: {', '.join(sorted(missing))}")

    task_attempts_expected = len(config.providers) * (frozen_task_count or 10)
    return DiagnosticPreflightResult(
        decision=READY_DECISION if not blockers else BLOCKED_PRECONDITION,
        can_execute=not blockers,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        release_gate_decision=release_gate_decision,
        provider_key_status=provider_key_status,
        confirmation_status=confirmation_status,
        dataset_hash=dataset_hash,
        manifest_hash=manifest_hash,
        frozen_task_count=frozen_task_count,
        task_attempts_expected=task_attempts_expected,
    )
