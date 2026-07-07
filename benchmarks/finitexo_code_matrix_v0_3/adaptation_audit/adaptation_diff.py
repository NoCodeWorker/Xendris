"""Deterministic adaptation diff heuristics.

These functions are operational signals, not semantic proof.
"""

from __future__ import annotations

import json
import re
from typing import Any, Mapping


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-zA-Z0-9_]+", text.lower()))


def compute_text_similarity(a: str, b: str) -> float:
    left = _tokens(a)
    right = _tokens(b)
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return round(len(left & right) / len(left | right), 6)


def estimate_structural_change(source: Mapping[str, Any], adapted: Mapping[str, Any]) -> float:
    source_keys = set(source)
    adapted_keys = set(adapted)
    if not source_keys and not adapted_keys:
        return 0.0
    overlap = len(source_keys & adapted_keys) / max(len(source_keys | adapted_keys), 1)
    return round(1.0 - overlap, 6)


def estimate_semantic_preservation(source_text: str, adapted_text: str) -> float:
    return compute_text_similarity(source_text, adapted_text)


def estimate_difficulty_shift(source_metadata: Mapping[str, Any], adapted_metadata: Mapping[str, Any]) -> float:
    source_text = json.dumps(source_metadata, sort_keys=True)
    adapted_text = json.dumps(adapted_metadata, sort_keys=True)
    return round(1.0 - compute_text_similarity(source_text, adapted_text), 6)

