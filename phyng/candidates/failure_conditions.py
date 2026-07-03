"""
Phygn v1.4 — Failure Condition Evaluator

Evaluates failure conditions for a given candidate model.
"""

from __future__ import annotations

from phyng.candidates.schemas import CandidatePredictionSpec

def evaluate_candidate_failure_conditions(
    candidate: CandidatePredictionSpec,
    gain: float | None = None,
    max_abs_delta: float | None = None,
) -> list[str]:
    """
    Evaluates failure conditions for a candidate spec.
    """
    failures = []
    
    # 1. Gain failure
    if gain is not None and gain <= 0:
        failures.append("FAIL_GAIN_NONPOSITIVE")
        
    # 2. Detectability failure
    if max_abs_delta is not None and candidate.detectability_threshold is not None:
        if max_abs_delta <= candidate.detectability_threshold:
            failures.append("FAIL_UNDETECTABLE_DELTA")
            
    # 3. Parameter failure
    if candidate.parameter_status == "FREE_UNCONSTRAINED":
        failures.append("FAIL_PARAMETER_UNDERIDENTIFIED")
        
    # 4. Ad hoc failure
    if candidate.parameter_status == "AD_HOC":
        failures.append("FAIL_AD_HOC_TERM")
        
    # 5. Dimensional failure
    if not candidate.term_units or not candidate.alpha_units or not candidate.dimensionless_core:
        failures.append("FAIL_DIMENSIONAL_INVALID")
        
    # 6. Source failure
    if not candidate.source_ids:
        failures.append("FAIL_NO_SOURCE_SUPPORT")
        
    # 7. Benchmark failure
    if not candidate.benchmark_ids:
        failures.append("FAIL_NO_BENCHMARK")
        
    return failures
