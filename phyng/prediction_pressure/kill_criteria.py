"""
Phygn v1.3 — Kill / Pivot Criteria

Evaluates whether the theory (Frontera C) should remain on the predictive track,
or be demoted/pivoted to an epistemic/structural framework.
"""

from __future__ import annotations

from phyng.prediction_pressure.schemas import KillPivotResult

def evaluate_kill_or_pivot(
    has_detectable_candidate: bool,
    has_benchmark_gain: bool,
    negative_bounds_only: bool,
    claim_blocking_useful: bool,
    structural_atlas_useful: bool,
) -> KillPivotResult:
    """
    Evaluates the theory status based on positive prediction pressure.
    """
    if has_detectable_candidate:
        return KillPivotResult(
            status="CONTINUE_PREDICTIVE_TRACK",
            conclusion="Frontera C remains on the predictive track.",
            rationale="A detectable candidate model with positive prediction has been defined."
        )
        
    if negative_bounds_only:
        if not has_detectable_candidate and not has_benchmark_gain:
            if claim_blocking_useful:
                return KillPivotResult(
                    status="CLAIM_GATING_ARCHITECTURE",
                    conclusion="Frontera C is pivoted to a Claim Gating Architecture.",
                    rationale="The theory does not produce positive predictions but is useful for blocking invalid physical claims."
                )
            elif structural_atlas_useful:
                return KillPivotResult(
                    status="STRUCTURAL_FRAMEWORK_ONLY",
                    conclusion="Frontera C is pivoted to a Structural Framework Only.",
                    rationale="The theory does not produce positive predictions but provides a useful structural signature atlas."
                )
            else:
                return KillPivotResult(
                    status="NOT_PREDICTIVE_CURRENTLY",
                    conclusion="Frontera C is currently not a predictive physical theory.",
                    rationale="The theory only produces negative bounds with no detectable candidate or benchmark gain."
                )
                
    # Fallback
    return KillPivotResult(
        status="NOT_PREDICTIVE_CURRENTLY",
        conclusion="Frontera C is currently not a predictive physical theory.",
        rationale="No positive predictive candidate model or benchmark gain exists."
    )
PostivePredictionRoadmap = [
    "v1.4 — Source Pack Ingestion Attempt",
    "v1.5 — Candidate Model Definition",
    "v1.6 — Candidate vs Baseline Benchmark",
    "v1.7 — Detectability & Failure Report",
]
