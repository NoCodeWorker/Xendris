"""Tests for v4.0 scientific debt and resolution plan."""

from __future__ import annotations

from phyng.scientific_debt.debt_registry import create_slot4_debt_object
from phyng.scientific_debt.slot4_resolution import create_slot4_resolution_plan


def test_slot4_debt_created_as_open_blocking() -> None:
    debt = create_slot4_debt_object()
    assert debt.debt_id == "DEBT-SLOT4-GRADIENT-COMPONENT-GAP"
    assert debt.status == "OPEN_BLOCKING_FOR_GRADIENT_CLAIMS"
    assert debt.severity == "HIGH"


def test_slot4_debt_blocks_gradient_claims() -> None:
    debt = create_slot4_debt_object()
    assert "PHI_GRADIENT as physical gradient mechanism" in debt.blocks
    assert "gradient-component source-backed claim" in debt.blocks
    assert "PHI_GRADIENT is source-backed as a gradient mechanism." in debt.prohibited_claims


def test_slot4_debt_does_not_block_benchmark_construction() -> None:
    debt = create_slot4_debt_object()
    assert "benchmark dataset construction" in debt.does_not_block
    assert "benchmark construction" in debt.allowed_work
    assert "observable alignment" in debt.allowed_work


def test_slot4_resolution_plan_contains_correct_tasks() -> None:
    plan = create_slot4_resolution_plan()
    assert plan.debt_id == "DEBT-SLOT4-GRADIENT-COMPONENT-GAP"
    assert plan.status == "SLOT4_DEBT_OPEN"
    assert len(plan.tasks) == 6

    task_names = {t.name for t in plan.tasks}
    expected_tasks = {
        "Pedernales manual review",
        "targeted SLOT_4 source acquisition",
        "exact SLOT_4 extraction",
        "v3.8.3-style promotion",
        "v3.9-style source pressure rerun",
        "keep/revise/kill gradient mechanism",
    }
    assert task_names == expected_tasks
