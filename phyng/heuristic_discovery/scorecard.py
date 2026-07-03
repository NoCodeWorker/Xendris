"""Heuristic scorecard helpers."""

from __future__ import annotations

from phyng.heuristic_discovery.prioritizer import compute_priority_score
from phyng.heuristic_discovery.schemas import HeuristicCandidate, HeuristicScorecard


def build_heuristic_scorecard(candidate: HeuristicCandidate) -> HeuristicScorecard:
    scores = candidate.heuristic_scores
    return HeuristicScorecard(
        candidate_id=candidate.candidate_id,
        detectability_potential=scores.get("detectability_potential", 0.0),
        non_ad_hoc_score=scores.get("non_ad_hoc_score", 0.0),
        dimensional_consistency=scores.get("dimensional_consistency", 0.0),
        falsifiability=scores.get("falsifiability", 0.0),
        benchmarkability=scores.get("benchmarkability", 0.0),
        source_searchability=scores.get("source_searchability", 0.0),
        simplicity=scores.get("simplicity", 0.0),
        novelty=scores.get("novelty", 0.0),
        cost_to_test_inverse=scores.get("cost_to_test_inverse", 0.0),
        risk_penalty=scores.get("risk_penalty", 0.0),
        priority_score=compute_priority_score(scores),
    )
