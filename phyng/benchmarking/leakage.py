"""Leakage labeling helpers."""

from __future__ import annotations


def label_same_source_leakage(source_ids: list[str]) -> str:
    return "HIGH" if len(set(source_ids)) < 2 else "MEDIUM"


def label_direct_interpolation(parameter_count: int, row_count: int) -> str:
    return "BLOCKING" if parameter_count >= row_count else "MEDIUM"
