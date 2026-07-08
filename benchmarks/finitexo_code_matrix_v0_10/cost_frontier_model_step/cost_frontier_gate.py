from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_config import (
    CostFrontierConfig,
)
from benchmarks.finitexo_code_matrix_v0_10.cost_frontier_model_step.cost_frontier_types import (
    CostFrontierPreflight,
    PreflightDecision,
)

SUPPORTED_MODELS = {
    "deepseek-v4-flash",
    "deepseek-v4-pro",
    "gpt-4.1-nano",
    "gpt-4.1-mini",
}


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate_cost_frontier_preflight(
    config: CostFrontierConfig,
    dataset_hash: str | None = None,
    manifest_hash: str | None = None,
    task_count: int | None = None,
) -> CostFrontierPreflight:
    blockers: list[str] = []

    # Dataset exists
    if not config.dataset_path.exists():
        blockers.append("dataset_not_found")
    else:
        dataset_manifest = config.dataset_path / "dataset_manifest.json"
        dataset_hashes = config.dataset_path / "dataset_hashes.json"
        tasks_dir = config.dataset_path / "tasks"

        if not dataset_manifest.exists():
            blockers.append("dataset_manifest_not_found")
        if not dataset_hashes.exists():
            blockers.append("dataset_hashes_not_found")
        if not tasks_dir.is_dir():
            blockers.append("tasks_dir_not_found")

        if not blockers:
            actual_hash = dataset_hash or _file_hash(dataset_hashes)
            if actual_hash != config.expected_dataset_hash:
                blockers.append("dataset_hash_mismatch")

            man_data = json.loads(dataset_manifest.read_text(encoding="utf-8"))
            actual_manifest_hash = manifest_hash or _file_hash(dataset_manifest)
            if actual_manifest_hash != config.expected_manifest_hash:
                blockers.append("manifest_hash_mismatch")

            actual_count = task_count or len(list(tasks_dir.glob("*.json")))
            if actual_count < config.expected_task_count:
                blockers.append(f"insufficient_tasks:got_{actual_count}_expected_{config.expected_task_count}")

    # Confirmation env
    confirm = config.environ.get("FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM")
    if confirm != "true":
        blockers.append("missing_explicit_execution_confirmation")

    # Provider keys
    has_deepseek = bool(config.environ.get("DEEPSEEK_API_KEY"))
    has_openai = bool(config.environ.get("OPENAI_API_KEY"))
    if not has_deepseek:
        blockers.append("missing_provider_key:deepseek")
    if not has_openai:
        blockers.append("missing_provider_key:openai")

    # Variants
    if len(config.variants) != 6:
        blockers.append(f"expected_6_variants_got_{len(config.variants)}")

    variant_names = [v.variant_name for v in config.variants]
    expected_names = [
        "deepseek_v4_flash_base", "deepseek_v4_flash_calibrated_runtime", "deepseek_v4_pro_base",
        "gpt_4_1_nano_base", "gpt_4_1_nano_calibrated_runtime", "gpt_4_1_mini_base",
    ]
    for name in expected_names:
        if name not in variant_names:
            blockers.append(f"missing_variant:{name}")

    # Calibrated runtime methodology guard
    for v in config.variants:
        if v.execution_method == "CALIBRATED_RUNTIME":
            if not v.use_runtime_loop or not v.use_calibrated_runtime:
                blockers.append(f"{v.variant_name}:calibrated_runtime_missing_runtime_loop")

    # Model support
    for v in config.variants:
        if v.model_name not in SUPPORTED_MODELS:
            blockers.append(f"unsupported_model:{v.model_name}_for_{v.variant_name}")

    # Budget
    if config.budget_cap_usd <= 0:
        blockers.append("budget_cap_not_configured")

    # Expected attempts
    expected = config.expected_task_count * len(config.variants)
    if expected != config.expected_attempts:
        blockers.append(f"expected_attempts_mismatch:{config.expected_attempts}_vs_{expected}")

    # Output dir
    if config.output_dir.exists() and any(config.output_dir.iterdir()):
        if not config.allow_overwrite:
            blockers.append("output_dir_not_empty_and_overwrite_not_allowed")

    can_execute = len(blockers) == 0
    decision = PreflightDecision.READY if can_execute else PreflightDecision.BLOCKED

    return CostFrontierPreflight(
        can_execute=can_execute,
        decision=decision.value,
        blockers=blockers,
        expected_attempts=config.expected_attempts,
        task_count=config.expected_task_count,
        dataset_hash=config.expected_dataset_hash,
        manifest_hash=config.expected_manifest_hash,
        budget_cap=config.budget_cap_usd,
    )
