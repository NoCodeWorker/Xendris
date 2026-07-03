"""Cross-validation utilities."""

from __future__ import annotations


def leave_one_out_indices(n: int) -> list[dict]:
    return [{"train": [j for j in range(n) if j != i], "test": [i]} for i in range(n)]


def out_of_source_ready(source_ids: list[str]) -> bool:
    return len(set(source_ids)) >= 2
