"""Adversarial readiness checks for Finitexo Code Matrix v0.3."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

BENCHMARK_DIR = Path(__file__).resolve().parents[1]
TASK_DIR = BENCHMARK_DIR / "tasks"
FORBIDDEN_TASK_TERMS = ("xendris",)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_task_hash(path: Path) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compute_dataset_hash(task_hashes: Mapping[str, str]) -> str:
    encoded = json.dumps(dict(sorted(task_hashes.items())), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _task_values_text(task: Mapping[str, Any]) -> str:
    values: list[str] = []
    for key, value in task.items():
        if key == "anti_xendris_bias_notes":
            continue
        values.append(json.dumps(value, sort_keys=True))
    return "\n".join(values).lower()


def dataset_mentions_forbidden_system(task_dir: Path = TASK_DIR) -> bool:
    for path in sorted(task_dir.glob("external_task_*.json")):
        task = json.loads(path.read_text(encoding="utf-8"))
        text = _task_values_text(task)
        if any(term in text for term in FORBIDDEN_TASK_TERMS):
            return True
    return False


def assess_adversarial_readiness(
    *,
    manifest: Mapping[str, Any],
    benchmark_dir: Path = BENCHMARK_DIR,
    execute_requested: bool = False,
    provider_execution_attempted: bool = False,
    report_text: str | None = None,
) -> dict[str, Any]:
    """Assess whether v0.3 artifacts are ready for cautious interpretation."""

    blockers: list[str] = []
    warnings: list[str] = []

    tasks = sorted((benchmark_dir / "tasks").glob("external_task_*.json"))
    actual_task_hashes = {path.name: canonical_task_hash(path) for path in tasks}
    actual_dataset_hash = compute_dataset_hash(actual_task_hashes)
    scoring_hash = sha256_file(benchmark_dir / "scoring_contract.md")

    if manifest.get("dataset_hash") != actual_dataset_hash:
        blockers.append("dataset_hash_invalid")
    if manifest.get("task_hashes") != actual_task_hashes:
        blockers.append("task_hashes_invalid")
    if manifest.get("scoring_contract_hash") != scoring_hash:
        blockers.append("scoring_contract_hash_invalid")
    if not manifest.get("blind_scoring_required"):
        blockers.append("blind_scoring_not_required")
    if not manifest.get("strong_baseline_required"):
        blockers.append("strong_baseline_not_required")
    if not (benchmark_dir / "baselines" / "strong_non_xendris_agent.md").exists():
        blockers.append("strong_non_xendris_agent_unavailable")
    if dataset_mentions_forbidden_system(benchmark_dir / "tasks"):
        blockers.append("dataset_mentions_system_under_evaluation")
    if provider_execution_attempted and not execute_requested:
        blockers.append("provider_execution_without_execute_flag")
    if report_text and "universal superiority" in report_text.lower() and "not authorize" not in report_text.lower():
        blockers.append("overclaim_detected")

    if not execute_requested:
        warnings.append("NO_PROVIDER_EXECUTION")
    if any(json.loads(path.read_text(encoding="utf-8")).get("origin") != "EXTERNAL" for path in tasks):
        warnings.append("SEMI_EXTERNAL_OR_MUTATED_TASKS_PRESENT")

    return {
        "adversarial_decision": "BLOCKED_FOR_INTERPRETATION" if blockers else "READY_FOR_ADVERSARIAL_INTERPRETATION",
        "h0_status": "LIVE",
        "blind_scoring_decision": "REQUIRED",
        "strong_baseline_decision": "REQUIRED",
        "task_hashes": actual_task_hashes,
        "dataset_hash": actual_dataset_hash,
        "scoring_contract_hash": scoring_hash,
        "warnings": warnings,
        "blockers": blockers,
    }

