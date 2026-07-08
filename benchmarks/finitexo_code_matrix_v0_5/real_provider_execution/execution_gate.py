"""Deterministic gate for v0.5.2 real-provider execution."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_5.provider_smoke.dataset_loader import (
    EXPECTED_DATASET_HASH,
    EXPECTED_MANIFEST_HASH,
    load_frozen_dataset,
)

from .execution_config import RealProviderExecutionConfig


CONFIGURATION_MISSING_DECISION = "REAL_PROVIDER_SMOKE_CONFIGURATION_MISSING_NO_EXECUTION"
READY_DECISION = "REAL_PROVIDER_SMOKE_EXECUTION_GATE_READY"


@dataclass(frozen=True)
class RealProviderExecutionGateResult:
    decision: str
    can_execute: bool
    blockers: tuple[str, ...]
    warnings: tuple[str, ...]
    provider_key_status: dict[str, str]
    confirmation_status: str
    dataset_hash: str | None
    manifest_hash: str | None
    frozen_task_count: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "can_execute": self.can_execute,
            "blockers": list(self.blockers),
            "warnings": list(self.warnings),
            "provider_key_status": self.provider_key_status,
            "confirmation_status": self.confirmation_status,
            "dataset_hash": self.dataset_hash,
            "manifest_hash": self.manifest_hash,
            "frozen_task_count": self.frozen_task_count,
        }


def _load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_real_provider_execution_gate(config: RealProviderExecutionConfig) -> RealProviderExecutionGateResult:
    blockers: list[str] = []
    warnings: list[str] = []
    provider_key_status: dict[str, str] = {}
    dataset_hash: str | None = None
    manifest_hash: str | None = None
    frozen_task_count: int | None = None

    try:
        config.validate_static_boundaries()
    except ValueError as exc:
        blockers.append(str(exc))

    manifest = _load_manifest(config.manifest_path)
    checks = {
        "benchmark_version": "v0.5.2",
        "input_dataset_version": "v0.4.3",
        "expected_dataset_hash": EXPECTED_DATASET_HASH,
        "expected_manifest_hash": EXPECTED_MANIFEST_HASH,
        "expected_frozen_task_count": 10,
        "provider_mode": "real",
        "mock_fallback_allowed": False,
        "statistical_claim_authorized": False,
        "provider_superiority_claim_authorized": False,
        "xendris_superiority_claim_authorized": False,
    }
    for key, expected in checks.items():
        if manifest.get(key) != expected:
            blockers.append(f"manifest field {key} mismatch")

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

    confirmation_value = config.environ.get(config.confirmation_env_var, "")
    confirmation_status = "PRESENT" if confirmation_value.lower() == "true" else "MISSING"
    if confirmation_status != "PRESENT":
        blockers.append(f"{config.confirmation_env_var}=true missing")

    for provider in config.providers:
        provider_key_status[provider.provider_name] = (
            "PRESENT" if bool(config.environ.get(provider.required_env_var)) else "MISSING"
        )
    missing = [name for name, status in provider_key_status.items() if status == "MISSING"]
    if missing:
        blockers.append(f"provider API key missing for: {', '.join(sorted(missing))}")

    return RealProviderExecutionGateResult(
        decision=READY_DECISION if not blockers else CONFIGURATION_MISSING_DECISION,
        can_execute=not blockers,
        blockers=tuple(blockers),
        warnings=tuple(warnings),
        provider_key_status=provider_key_status,
        confirmation_status=confirmation_status,
        dataset_hash=dataset_hash,
        manifest_hash=manifest_hash,
        frozen_task_count=frozen_task_count,
    )
