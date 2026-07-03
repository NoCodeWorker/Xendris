"""Heuristic candidate prioritization."""

from __future__ import annotations

from phyng.core.compatibility import normalize_status
from phyng.heuristic_discovery.schemas import HeuristicCandidate, HeuristicRankingResult


HEURISTIC_PRIORITY_WEIGHTS = {
    "detectability_potential": 0.20,
    "non_ad_hoc_score": 0.15,
    "dimensional_consistency": 0.15,
    "falsifiability": 0.15,
    "benchmarkability": 0.10,
    "source_searchability": 0.10,
    "simplicity": 0.05,
    "novelty": 0.05,
    "cost_to_test_inverse": 0.05,
    "risk_penalty": -0.10,
}


def rank_heuristic_candidates(candidates: list[HeuristicCandidate]) -> HeuristicRankingResult:
    ranked: list[HeuristicCandidate] = []
    warnings = ["Priority score is not evidence and does not authorize claims."]
    for candidate in candidates:
        score = compute_priority_score(candidate.heuristic_scores)
        updated_scores = dict(candidate.heuristic_scores)
        updated_scores["priority_score"] = score
        ranked.append(
            candidate.model_copy(
                update={
                    "heuristic_scores": updated_scores,
                    "canonical_status": normalize_status("HEURISTIC_PRIORITIZED", domain="heuristic_discovery"),
                },
                deep=True,
            )
        )

    ranked.sort(key=lambda item: item.heuristic_scores.get("priority_score", 0.0), reverse=True)
    top_candidate_id = ranked[0].candidate_id if ranked else None
    return HeuristicRankingResult(
        candidates=ranked,
        ranking_method="weighted_heuristic_priority_v2_2",
        weights=HEURISTIC_PRIORITY_WEIGHTS,
        top_candidate_id=top_candidate_id,
        warnings=warnings,
        canonical_status=normalize_status("HEURISTIC_PRIORITIZED", domain="heuristic_discovery"),
    )


def compute_priority_score(scores: dict[str, float]) -> float:
    total = 0.0
    for key, weight in HEURISTIC_PRIORITY_WEIGHTS.items():
        total += weight * _bounded(scores.get(key, 0.0))
    return round(total, 4)


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
