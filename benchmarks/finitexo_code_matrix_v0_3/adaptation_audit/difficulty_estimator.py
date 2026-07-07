"""Conservative heuristic difficulty estimator."""

from __future__ import annotations

from typing import Any, Mapping

from .adaptation_types import DifficultyLevel


def estimate_difficulty(metadata: Mapping[str, Any]) -> DifficultyLevel:
    score = 0
    score += int(metadata.get("expected_files_changed", 1))
    score += 2 if metadata.get("api_contract_sensitive") else 0
    score += 2 if metadata.get("hidden_tests_relevant") else 0
    score += 2 if metadata.get("cross_file_reasoning") else 0
    score += 2 if metadata.get("dependency_complexity") else 0
    score += 2 if metadata.get("ambiguous") else 0
    score += 2 if metadata.get("security_sensitive") else 0
    score += 1 if metadata.get("minimal_patch_required") else 0
    if score <= 1:
        return DifficultyLevel.TRIVIAL
    if score <= 3:
        return DifficultyLevel.EASY
    if score <= 6:
        return DifficultyLevel.MEDIUM
    if score <= 10:
        return DifficultyLevel.HARD
    return DifficultyLevel.EXTREME

