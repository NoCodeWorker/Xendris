"""Create the resolution plan for SLOT_4 debt."""

from __future__ import annotations

from phyng.scientific_debt.schemas import Slot4ResolutionPlan, Slot4ResolutionTask


def create_slot4_resolution_plan() -> Slot4ResolutionPlan:
    """Build the official resolution plan for closing the SLOT_4 evidence gap."""
    tasks = [
        Slot4ResolutionTask(
            task_id="TASK-SLOT4-001",
            name="Pedernales manual review",
            description="Manual review of the Pedernales SLOT_4 queue to identify potential extracts.",
            status="QUEUED",
            owner="Human reviewer / Principal investigator",
        ),
        Slot4ResolutionTask(
            task_id="TASK-SLOT4-002",
            name="targeted SLOT_4 source acquisition",
            description="Targeted source search and acquisition focusing on spin-motion coupling, gradient transition, and effective dynamics.",
            status="QUEUED",
            owner="Acquisition engine",
        ),
        Slot4ResolutionTask(
            task_id="TASK-SLOT4-003",
            name="exact SLOT_4 extraction",
            description="Extract exact equations and passages from candidate SLOT_4 sources.",
            status="QUEUED",
            owner="Extraction engine",
        ),
        Slot4ResolutionTask(
            task_id="TASK-SLOT4-004",
            name="v3.8.3-style promotion",
            description="Run conservative promotion checks on new SLOT_4 extracts to build a validation-ready pack.",
            status="QUEUED",
            owner="Promotion engine",
        ),
        Slot4ResolutionTask(
            task_id="TASK-SLOT4-005",
            name="v3.9-style source pressure rerun",
            description="Rerun the source pressure decision gate with the expanded validation-ready pack containing SLOT_4.",
            status="QUEUED",
            owner="Decision engine",
        ),
        Slot4ResolutionTask(
            task_id="TASK-SLOT4-006",
            name="keep/revise/kill gradient mechanism",
            description="Decide whether to keep, revise, or kill the gradient mechanism based on source-pressure rerun results.",
            status="QUEUED",
            owner="Principal investigator / Technical committee",
        ),
    ]

    return Slot4ResolutionPlan(
        plan_id="PHI-GRADIENT-SLOT4-RESOLUTION-PLAN-v4_0",
        debt_id="DEBT-SLOT4-GRADIENT-COMPONENT-GAP",
        status="SLOT4_DEBT_OPEN",
        tasks=tasks,
        notes=[
            "Resolution tasks are ordered sequentially.",
            "Each task must be completed and audited to update the debt status.",
        ],
    )
