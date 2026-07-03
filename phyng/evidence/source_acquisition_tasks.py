"""
Phygn v1.1 — Source Acquisition Tasks

Generates research task JSON files for missing baseline source categories.
Written to rag/research_tasks/ so they can be tracked and resolved.

Task generation does NOT claim sources have been ingested.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

# ── Category definitions ───────────────────────────────────────────────────

ALL_CATEGORIES = [
    "VISIBILITY_DECAY",
    "ENVIRONMENTAL_DECOHERENCE",
    "MATTER_WAVE_INTERFEROMETRY",
    "DETECTABILITY_OR_VISIBILITY_THRESHOLD",
    "OPTIONAL_PARAMETER_OR_RATE_SUPPORT",
]

_CATEGORY_META = {
    "VISIBILITY_DECAY": {
        "task_id": "RT-V1-1-SRC-VISIBILITY_DECAY",
        "description": (
            "Acquire at least one source providing FORMULA_SUPPORT for "
            "visibility/coherence exponential decay V(t)=exp(-Γt) as a "
            "phenomenological model."
        ),
        "desired_support_types": ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
        "suggested_queries": [
            "coherence exponential decay decoherence rate",
            "visibility exponential decay decoherence",
            "phenomenological decoherence exponential model",
        ],
        "requirement_id": "BSP-001",
        "priority": "HIGH",
    },
    "ENVIRONMENTAL_DECOHERENCE": {
        "task_id": "RT-V1-1-SRC-ENVIRONMENTAL_DECOHERENCE",
        "description": (
            "Acquire at least one source covering environment-induced decoherence, "
            "decoherence rate or timescale. May provide CONTEXT_SUPPORT, "
            "FORMULA_SUPPORT, or PARAMETER_SUPPORT."
        ),
        "desired_support_types": ["CONTEXT_SUPPORT", "FORMULA_SUPPORT", "PARAMETER_SUPPORT"],
        "suggested_queries": [
            "environment induced decoherence review",
            "decoherence timescale quantum systems review",
            "quantum decoherence exponential decay coherence",
        ],
        "requirement_id": "BSP-003",
        "priority": "HIGH",
    },
    "MATTER_WAVE_INTERFEROMETRY": {
        "task_id": "RT-V1-1-SRC-MATTER_WAVE_INTERFEROMETRY",
        "description": (
            "Acquire at least one source covering matter-wave or nanoparticle "
            "interferometry for mesoscopic system context. May provide "
            "OBSERVABLE_SUPPORT or CONTEXT_SUPPORT."
        ),
        "desired_support_types": ["OBSERVABLE_SUPPORT", "CONTEXT_SUPPORT"],
        "suggested_queries": [
            "matter wave interferometry massive particles decoherence",
            "nanoparticle matter wave interferometry visibility decoherence",
            "macroscopic quantum resonators MAQRO decoherence interferometry",
        ],
        "requirement_id": "BSP-004",
        "priority": "HIGH",
    },
    "DETECTABILITY_OR_VISIBILITY_THRESHOLD": {
        "task_id": "RT-V1-1-SRC-DETECTABILITY_OR_VISIBILITY_THRESHOLD",
        "description": (
            "Acquire at least one source providing experimental visibility uncertainty "
            "or detectability threshold (epsilon_exp). May provide BENCHMARK_SUPPORT "
            "or PARAMETER_SUPPORT."
        ),
        "desired_support_types": ["BENCHMARK_SUPPORT", "PARAMETER_SUPPORT", "OBSERVABLE_SUPPORT"],
        "suggested_queries": [
            "matter wave interferometry visibility uncertainty",
            "nanoparticle interferometry visibility measurement error",
            "interferometric visibility experimental uncertainty decoherence",
        ],
        "requirement_id": "BSP-006",
        "priority": "MEDIUM",
    },
    "OPTIONAL_PARAMETER_OR_RATE_SUPPORT": {
        "task_id": "RT-V1-1-SRC-OPTIONAL_PARAMETER_OR_RATE_SUPPORT",
        "description": (
            "Acquire an optional source covering Γ (decoherence rate), decay constant, "
            "or timescale values to ground PARAMETER_SUPPORT for the baseline."
        ),
        "desired_support_types": ["PARAMETER_SUPPORT", "ASSUMPTION_SUPPORT"],
        "suggested_queries": [
            "decoherence rate quantum system environment",
            "decoherence timescale experimental value",
            "coherence decay constant matter wave experiment",
        ],
        "requirement_id": "BSP-005",
        "priority": "LOW",
    },
}


# ── Models ─────────────────────────────────────────────────────────────────

class SourceAcquisitionTask(BaseModel):
    task_id: str
    category: str
    description: str
    desired_support_types: list[str] = Field(default_factory=list)
    suggested_queries: list[str] = Field(default_factory=list)
    requirement_id: str
    priority: str
    status: str = "OPEN"
    resolved_by: str | None = None


# ── Core function ──────────────────────────────────────────────────────────

def generate_source_acquisition_tasks(
    project_root: Path,
    covered_categories: list[str] | None = None,
) -> list[SourceAcquisitionTask]:
    """
    Generate task JSON files for all missing source categories.

    Args:
        project_root: Project root path.
        covered_categories: Categories already covered by audited local sources.
                            Tasks for covered categories are skipped.

    Returns:
        List of SourceAcquisitionTask for each task written.
    """
    covered = set(covered_categories or [])
    out_dir = project_root / "rag" / "research_tasks"
    out_dir.mkdir(parents=True, exist_ok=True)

    tasks: list[SourceAcquisitionTask] = []

    for category in ALL_CATEGORIES:
        meta = _CATEGORY_META[category]
        task = SourceAcquisitionTask(
            task_id=meta["task_id"],
            category=category,
            description=meta["description"],
            desired_support_types=meta["desired_support_types"],
            suggested_queries=meta["suggested_queries"],
            requirement_id=meta["requirement_id"],
            priority=meta["priority"],
            status="RESOLVED" if category in covered else "OPEN",
            resolved_by=None,
        )
        # Write JSON
        fname = f"{meta['task_id']}.json"
        fpath = out_dir / fname
        fpath.write_text(
            json.dumps(task.model_dump(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        tasks.append(task)

    return tasks


def get_missing_categories(tasks: list[SourceAcquisitionTask]) -> list[str]:
    """Return category names that are still OPEN (not covered)."""
    return [t.category for t in tasks if t.status == "OPEN"]
