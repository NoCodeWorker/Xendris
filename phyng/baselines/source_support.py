"""
Phygn v0.8 — Baseline Source Support Matrix

Tracks how each ingested source supports (or limits) the baseline model.
If no sources are available, returns AWAITING_SOURCE_INGESTION state.
"""

from __future__ import annotations

from pathlib import Path

from phyng.baselines.schemas import BaselineSourceRequirement, BaselineSourceSupport
from phyng.rag.source_registry import list_sources


# Default baseline source requirements (without real ingestion)
BASELINE_SOURCE_REQUIREMENTS_DEF: list[dict] = [
    {
        "requirement_id": "BSR-001",
        "topic": "Visibility Decay Formula",
        "baseline_role": "FORMULA_SUPPORT",
        "reason": "The baseline formula V(t)=exp(-Gamma*t) requires a source grounding it as a phenomenological model for matter-wave coherence loss.",
        "required_for": ["VisibilityDecayBaselineSpec"],
        "linked_model_ids": ["V_BASE_EXP_DECAY_001"],
        "linked_claim_ids": ["CLAIM-DECOH-001"],
        "required_trust_level": "HIGH",
        "suggested_queries": [
            "matter wave interferometry visibility decoherence exponential decay",
            "quantum decoherence visibility loss interferometry exponential model",
        ],
    },
    {
        "requirement_id": "BSR-002",
        "topic": "Environmental Decoherence Rate",
        "baseline_role": "PARAMETER_SUPPORT",
        "reason": "Gamma_env must be grounded by a source to transition parameter status from PARAMETER_TOY.",
        "required_for": ["VisibilityDecayBaselineSpec"],
        "linked_model_ids": ["V_BASE_EXP_DECAY_001"],
        "linked_claim_ids": [],
        "required_trust_level": "HIGH",
        "suggested_queries": [
            "environmental decoherence rate matter wave interferometry nanoparticle",
            "decoherence rate matter wave interferometry visibility",
        ],
    },
    {
        "requirement_id": "BSR-003",
        "topic": "Experimental Visibility Threshold",
        "baseline_role": "OBSERVABLE_SUPPORT",
        "reason": "epsilon_exp requires source support to be physically meaningful.",
        "required_for": ["Campaign002BaselineUpgradeResult"],
        "linked_model_ids": [],
        "linked_claim_ids": [],
        "required_trust_level": "HIGH",
        "suggested_queries": [
            "matter wave interferometry visibility measurement uncertainty",
            "nanoparticle interferometry decoherence experimental visibility threshold",
        ],
    },
    {
        "requirement_id": "BSR-004",
        "topic": "Mesoscopic Interferometry Context",
        "baseline_role": "CONTEXT_SUPPORT",
        "reason": "Nanoparticle mass and scale selection needs contextual grounding.",
        "required_for": ["Campaign002BaselineUpgradeResult"],
        "linked_model_ids": [],
        "linked_claim_ids": [],
        "required_trust_level": "MEDIUM",
        "suggested_queries": [
            "macroscopic quantum resonators MAQRO nanoparticle interferometry decoherence",
            "matter wave interferometry massive nanoparticles decoherence visibility",
        ],
    },
]


def build_baseline_source_requirements() -> list[BaselineSourceRequirement]:
    """Return the full set of baseline source requirements."""
    return [BaselineSourceRequirement(**d) for d in BASELINE_SOURCE_REQUIREMENTS_DEF]


def build_source_support_matrix(root_dir: Path) -> list[BaselineSourceSupport]:
    """
    Build the source support matrix from ingested sources.
    Returns empty list if no sources are available (AWAITING_SOURCE_INGESTION).
    """
    sources = list_sources(root_dir)
    matrix: list[BaselineSourceSupport] = []

    for src in sources:
        src_text = f"{src.title} {' '.join(src.topics)} {src.notes or ''}".lower()
        if any(kw in src_text for kw in ["visibility", "decoherence", "exponential", "coherence"]):
            matrix.append(
                BaselineSourceSupport(
                    source_id=src.source_id,
                    support_level="FORMULA_SUPPORT",
                    trust_level=src.trust_level,
                    note="Auto-matched on visibility/decoherence keyword.",
                )
            )
        elif any(kw in src_text for kw in ["nanoparticle", "interferometry", "maqro"]):
            matrix.append(
                BaselineSourceSupport(
                    source_id=src.source_id,
                    support_level="CONTEXT_SUPPORT",
                    trust_level=src.trust_level,
                    note="Auto-matched on mesoscopic interferometry keyword.",
                )
            )

    return matrix
