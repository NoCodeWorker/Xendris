"""Next model update recommendations for v3.9."""

from __future__ import annotations

from phyng.source_pressure_decision.schemas import (
    SourcePressureDecision,
    ContradictionLimitationMap,
)


def build_recommendations(
    decision: SourcePressureDecision,
    contradiction_map: ContradictionLimitationMap,
) -> dict:
    """Build the recommendations artifact payload."""
    return {
        "decision_id": decision.decision_id,
        "primary_decision": decision.primary_decision,
        "gradient_component_support": decision.gradient_component_support,
        "recommendations": decision.next_recommendations,
        "possible_next_phases": _next_phases(decision),
        "notes": [
            "These recommendations are derived from the source-pressure decision.",
            "They do not constitute validation or approval.",
            "Physical claims remain blocked.",
        ],
    }


def _next_phases(decision: SourcePressureDecision) -> list[str]:
    phases: list[str] = []
    if "PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND" in decision.global_decisions:
        phases.append("v4.0 — Benchmark Dataset Construction & Observable Alignment")
    if "PHI_GRADIENT_REAL_SOURCE_CONTRADICTED" in decision.global_decisions:
        phases.append("v4.0 — Candidate Revision or Kill/Pivot Gate")
    if "PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY" in decision.global_decisions:
        phases.append("v4.0 — Literature Gap Expansion for SLOT_4")
    if "PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE" in decision.global_decisions:
        phases.append("v4.0 — Targeted Source Acquisition & Manual Review")
    if not phases:
        phases.append("v4.0 — Next decision gate (to be determined by primary decision).")
    return phases
