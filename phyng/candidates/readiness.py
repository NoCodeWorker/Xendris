"""
Phygn v1.4 — Candidate Readiness Evaluator

Determines the readiness status of a candidate model spec based on its
operationalization, admissibility, and failures.
"""

from __future__ import annotations

from phyng.candidates.schemas import CandidatePredictionSpec

def evaluate_candidate_readiness(
    candidate: CandidatePredictionSpec,
    admissibility: str,
    failures: list[str]
) -> str:
    """
    Evaluates the readiness status of a candidate model.
    """
    # 1. Check if core operationalization fields are missing
    if (not candidate.observable or 
        not candidate.baseline_model or 
        not candidate.candidate_model or 
        not candidate.candidate_term or 
        not candidate.expected_pattern or 
        candidate.detectability_threshold is None):
        return "CANDIDATE_NOT_OPERATIONALIZED"
        
    # 2. Check if admissibility is blocked
    if admissibility in ("BLOCKED_DIMENSIONAL_INCOMPLETE", "BLOCKED_AS_AD_HOC_CANDIDATE", "UNDERIDENTIFIED_CANDIDATE"):
        return "CANDIDATE_BLOCKED"
        
    # 3. Check evidence and benchmark presence
    has_sources = "FAIL_NO_SOURCE_SUPPORT" not in failures
    has_benchmark = "FAIL_NO_BENCHMARK" not in failures
    
    if not has_sources and not has_benchmark:
        return "CANDIDATE_REQUIRES_EVIDENCE"
        
    if not has_sources and has_benchmark:
        return "CANDIDATE_READY_FOR_SYNTHETIC_BENCHMARK"
        
    if has_sources and has_benchmark:
        return "CANDIDATE_READY_FOR_SOURCE_BACKED_BENCHMARK"
        
    if admissibility == "ADMISSIBLE_TOY_CANDIDATE":
        return "CANDIDATE_TOY_OPERATIONALIZED"
        
    return "CANDIDATE_REQUIRES_EVIDENCE"
