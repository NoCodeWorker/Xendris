"""
Phygn v1.2 — Canonical Source Slots

Defines the metadata and slots for canonical baseline literature sources.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

class CanonicalSourceSlot(BaseModel):
    source_candidate_id: str
    requirement_id: str
    purpose: str
    intended_support_types: list[str]
    required_limitation: str
    suggested_queries: list[str] = Field(default_factory=list)

CANONICAL_SLOTS = {
    "SRC-BASE-DECOH-001": CanonicalSourceSlot(
        source_candidate_id="SRC-BASE-DECOH-001",
        requirement_id="BSP-001",
        purpose="Support the idea that coherence can decay over time under environmental interaction.",
        intended_support_types=["FORMULA_SUPPORT", "CONTEXT_SUPPORT", "PARAMETER_SUPPORT"],
        required_limitation="This does not validate Frontera C or the boundary-aware candidate.",
        suggested_queries=[
            "environment induced decoherence review",
            "decoherence timescale quantum systems review",
            "quantum decoherence exponential decay coherence",
        ]
    ),
    "SRC-BASE-VIS-001": CanonicalSourceSlot(
        source_candidate_id="SRC-BASE-VIS-001",
        requirement_id="BSP-002",
        purpose="Support visibility or interference contrast as an observable/readout.",
        intended_support_types=["OBSERVABLE_SUPPORT", "FORMULA_SUPPORT"],
        required_limitation="This supports visibility/contrast as an observable only.",
        suggested_queries=[
            "interferometric visibility decoherence matter wave",
            "matter wave interferometry visibility loss decoherence",
            "visibility contrast decoherence interference experiment",
        ]
    ),
    "SRC-BASE-MWI-001": CanonicalSourceSlot(
        source_candidate_id="SRC-BASE-MWI-001",
        requirement_id="BSP-004",
        purpose="Support relevance to matter-wave or mesoscopic interferometry.",
        intended_support_types=["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT"],
        required_limitation="This supports experimental context, not the boundary-aware candidate.",
        suggested_queries=[
            "matter wave interferometry massive particles decoherence",
            "nanoparticle matter wave interferometry visibility decoherence",
            "macroscopic quantum resonators MAQRO decoherence interferometry",
        ]
    ),
    "SRC-BASE-THRESH-001": CanonicalSourceSlot(
        source_candidate_id="SRC-BASE-THRESH-001",
        requirement_id="BSP-006",
        purpose="Support epsilon_exp or measurement threshold in later detectability analysis.",
        intended_support_types=["BENCHMARK_SUPPORT", "PARAMETER_SUPPORT", "OBSERVABLE_SUPPORT"],
        required_limitation="Do not infer epsilon_exp unless the source gives or constrains it.",
        suggested_queries=[
            "matter wave interferometry visibility uncertainty",
            "nanoparticle interferometry visibility measurement error",
            "interferometric visibility experimental uncertainty decoherence",
        ]
    ),
    "SRC-BASE-PARAM-001": CanonicalSourceSlot(
        source_candidate_id="SRC-BASE-PARAM-001",
        requirement_id="BSP-005",
        purpose="Support interpretation of Gamma as effective rate/timescale.",
        intended_support_types=["PARAMETER_SUPPORT", "ASSUMPTION_SUPPORT"],
        required_limitation="This does not make arbitrary Gamma values physical.",
        suggested_queries=[
            "decoherence rate quantum system environment",
            "decoherence timescale experimental value",
            "coherence decay constant matter wave experiment",
        ]
    )
}
