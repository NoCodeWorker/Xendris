"""Completion validator that reuses v0.4.1 expansion intake validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from benchmarks.finitexo_code_matrix_v0_4.expansion_intake import (
    load_expansion_candidates,
    validate_expansion_batch,
)
from .completion_policy import evaluate_pool_completion


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_completion_policy(root: Path = ROOT) -> dict[str, Any]:
    manifest = _load_json(root / "expansion_completion_manifest.json")
    frozen_hashes = _load_json(root / "frozen_dataset_hashes.json")
    batch = validate_expansion_batch(load_expansion_candidates(root / "expansion_candidates"))
    frozen_hashes_unchanged = (
        manifest["base_frozen_dataset_hash"] == frozen_hashes["dataset_hash"]
        and manifest["base_manifest_hash"] == frozen_hashes["manifest_hash"]
    )
    policy = evaluate_pool_completion(
        current_frozen_task_count=manifest["base_frozen_task_count"],
        target_frozen_task_count=manifest["target_frozen_task_count"],
        additional_ready_candidates_required=manifest["additional_ready_candidates_required"],
        ready_for_future_freeze=batch["ready_for_future_freeze"],
        ready_with_human_review=batch["ready_with_human_review"],
        frozen_hashes_unchanged=frozen_hashes_unchanged,
        providers_executed=False,
    )
    candidates = batch["candidates"]
    excluded = [
        candidate["expansion_candidate_id"]
        for candidate in candidates
        if candidate["expansion_readiness"] not in {"READY_FOR_FUTURE_FREEZE", "READY_WITH_HUMAN_REVIEW"}
    ]
    return {
        **batch,
        **policy,
        "manifest": manifest,
        "frozen_hashes_unchanged": frozen_hashes_unchanged,
        "excluded_from_readiness_count": excluded,
        "effective_ready_count": batch["ready_for_future_freeze"],
        "effective_mixed_ready_count": batch["ready_for_future_freeze"] + batch["ready_with_human_review"],
        "providers_executed": False,
        "model_comparison_run": False,
        "network_required": False,
        "env_read": False,
        "secrets_printed": False,
    }
