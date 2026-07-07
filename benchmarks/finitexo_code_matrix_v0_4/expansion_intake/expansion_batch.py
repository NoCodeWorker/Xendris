"""Batch loading and validation for v0.4.1 expansion candidates."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from .expansion_candidate import ExpansionCandidate
from .expansion_scoring import score_expansion_candidate
from .expansion_types import ExpansionBatchDecision, ExpansionReadiness
from .expansion_validation import validate_expansion_candidate


ROOT = Path("benchmarks/finitexo_code_matrix_v0_4")
CANDIDATES_DIR = ROOT / "expansion_candidates"


def load_expansion_candidates(candidates_dir: Path = CANDIDATES_DIR) -> list[ExpansionCandidate]:
    candidates = []
    for path in sorted(candidates_dir.glob("expansion_candidate_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        candidates.append(ExpansionCandidate.from_dict(data))
    return candidates


def validate_expansion_batch(candidates: list[ExpansionCandidate] | None = None) -> dict[str, Any]:
    validated = [validate_expansion_candidate(candidate) for candidate in (candidates or load_expansion_candidates())]
    readiness_counts = Counter(candidate.expansion_readiness.value for candidate in validated)
    ready_count = readiness_counts[ExpansionReadiness.READY_FOR_FUTURE_FREEZE.value]
    human_review_count = readiness_counts[ExpansionReadiness.READY_WITH_HUMAN_REVIEW.value]
    blocked_count = readiness_counts[ExpansionReadiness.BLOCKED.value] + readiness_counts[ExpansionReadiness.DO_NOT_FREEZE.value]
    future_ready_count = ready_count + human_review_count

    decision = ExpansionBatchDecision.EXPANSION_INTAKE_ONLY_NO_FREEZE
    if future_ready_count >= 8:
        decision = ExpansionBatchDecision.EXPANSION_POOL_READY_FOR_REVIEW
    elif blocked_count == len(validated):
        decision = ExpansionBatchDecision.EXPANSION_POOL_BLOCKED
    elif future_ready_count < 8:
        decision = ExpansionBatchDecision.EXPANSION_POOL_INSUFFICIENT

    scores = [score_expansion_candidate(candidate) for candidate in validated]
    return {
        "batch_decision": decision.value,
        "candidates": [candidate.to_dict() | {"diagnostic_expansion_score": score_expansion_candidate(candidate)} for candidate in validated],
        "readiness_counts": dict(readiness_counts),
        "ready_for_future_freeze": ready_count,
        "ready_with_human_review": human_review_count,
        "blocked_or_rejected": blocked_count,
        "diagnostic_mean_expansion_score": round(sum(scores) / len(scores), 4) if scores else 0.0,
    }
