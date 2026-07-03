"""
Phygn v0.8 — Visibility Decay Baseline

Implements the exponential visibility-decay baseline:
    V_base(t) = exp(-Gamma_env * t)

Classification follows evidence level. No fake source ingestion.
"""

from __future__ import annotations

import math
from pathlib import Path

from phyng.baselines.schemas import VisibilityDecayBaselineSpec
from phyng.rag.research_planner import list_research_tasks, save_research_task
from phyng.rag.schemas import ResearchTask
from phyng.rag.source_registry import list_sources


def compute_visibility(gamma: float, t: float) -> float:
    """V_base(t) = exp(-gamma * t)."""
    return math.exp(-gamma * t)


def compute_visibility_series(gamma: float, times: list[float]) -> list[float]:
    """Compute visibility at multiple time points."""
    return [compute_visibility(gamma, t) for t in times]


# --- Baseline definitions ------------------------------------------------

BASELINE_SOURCE_REQUIREMENTS = [
    {
        "task_id": "RT-BASELINE-SRC-001",
        "question": "What source supports the exponential visibility decay model V(t)=exp(-Gamma*t) for matter-wave interferometry?",
        "reason": "Baseline formula requires FORMULA_SUPPORT at HIGH trust level.",
        "category": "BASE-SRC-001",
    },
    {
        "task_id": "RT-BASELINE-SRC-002",
        "question": "What source grounds the environmental decoherence rate Gamma_env for mesoscopic matter-wave systems?",
        "reason": "PARAMETER_SOURCE_BACKED requires a sourced decay rate.",
        "category": "BASE-SRC-002",
    },
    {
        "task_id": "RT-BASELINE-SRC-003",
        "question": "What source grounds experimental visibility thresholds (epsilon_exp) for nanoparticle interferometry?",
        "reason": "Detectability requires a source-backed epsilon_exp.",
        "category": "BASE-SRC-005",
    },
    {
        "task_id": "RT-BASELINE-SRC-004",
        "question": "What mesoscopic nanoparticle interferometry experiment provides visibility data?",
        "reason": "BASE-SRC-004 required for system mass/scale context.",
        "category": "BASE-SRC-004",
    },
]


def ensure_baseline_research_tasks(root_dir: Path) -> list[str]:
    """Create ResearchTasks for each missing baseline source category."""
    existing_ids = {t.task_id for t in list_research_tasks(root_dir)}
    created: list[str] = []
    for spec in BASELINE_SOURCE_REQUIREMENTS:
        task_id = spec["task_id"]
        if task_id not in existing_ids:
            save_research_task(
                ResearchTask(
                    task_id=task_id,
                    question=spec["question"],
                    reason=spec["reason"],
                    linked_gap_id=f"GAP_{task_id}",
                    required_source_types=["PAPER", "BOOK"],
                    priority="P1",
                    expected_output="SOURCE_RECORDS",
                    status="AWAITING_SOURCE_INGESTION",
                ),
                root_dir,
            )
        created.append(task_id)
    return created


def build_visibility_decay_baseline(root_dir: Path) -> VisibilityDecayBaselineSpec:
    """
    Construct the baseline spec. Checks existing sources.
    Gamma value is None (PARAMETER_TOY) until sourced.
    """
    sources = list_sources(root_dir)
    source_ids = [s.source_id for s in sources]

    # Determine support_status from available sources
    # (Without real source ingestion, defaults to TOY_INTERNAL)
    support_status = "TOY_INTERNAL"
    parameter_status = "PARAMETER_TOY"

    return VisibilityDecayBaselineSpec(
        model_id="V_BASE_EXP_DECAY_001",
        formula="V_base(t) = exp(-Gamma_env * t)",
        observable="visibility_loss",
        gamma_parameter_name="Gamma_env",
        gamma_value=None,  # arbitrary until sourced
        gamma_units="s^{-1}",
        assumptions=[
            "Environmental noise is Markovian.",
            "Decoherence is exponential in time.",
            "Single dominant decay channel.",
        ],
        source_ids=source_ids,
        support_status=support_status,
        parameter_status=parameter_status,
    )
