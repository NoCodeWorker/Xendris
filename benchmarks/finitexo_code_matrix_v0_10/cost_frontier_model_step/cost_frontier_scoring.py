from __future__ import annotations

import statistics
from typing import Any

from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_scoring import (
    score_runtime_response as v0_9_score,
    aggregate_by_variant as v0_9_aggregate,
    compute_family_lift as v0_9_family_lift,
    FAMILIES,
)


def score_cost_frontier_response(
    variant_name: str,
    provider_name: str,
    model_name: str,
    task_id: str,
    task_family: str,
    response_text: str,
    estimated_cost_usd: float | None = None,
) -> Any:
    return v0_9_score(
        variant_name, provider_name, model_name,
        task_id, task_family, response_text,
        estimated_cost_usd=estimated_cost_usd,
    )


def aggregate_by_variant(
    scored: list,
) -> list:
    return v0_9_aggregate(scored)


def compute_cost_frontier(
    scored: list,
    aggregates: list,
) -> dict[str, Any]:
    by_task: dict[str, dict[str, float]] = {}
    by_task_cost: dict[str, dict[str, float]] = {}
    for r in scored:
        by_task.setdefault(r.task_id, {})[r.variant_name] = r.score_total
        by_task_cost.setdefault(r.task_id, {})[r.variant_name] = r.estimated_cost_usd or 0.0

    agg_map: dict[str, Any] = {}
    for a in aggregates:
        agg_map[a.variant_name] = a

    comparisons = [
        # DeepSeek
        ("flash_calibrated_vs_flash_base", "deepseek_v4_flash_base", "deepseek_v4_flash_calibrated_runtime"),
        ("pro_base_vs_flash_base", "deepseek_v4_flash_base", "deepseek_v4_pro_base"),
        ("flash_calibrated_vs_pro_base", "deepseek_v4_pro_base", "deepseek_v4_flash_calibrated_runtime"),
        # OpenAI
        ("nano_calibrated_vs_nano_base", "gpt_4_1_nano_base", "gpt_4_1_nano_calibrated_runtime"),
        ("mini_base_vs_nano_base", "gpt_4_1_nano_base", "gpt_4_1_mini_base"),
        ("nano_calibrated_vs_mini_base", "gpt_4_1_mini_base", "gpt_4_1_nano_calibrated_runtime"),
    ]

    results: list[dict[str, Any]] = []
    for comp_name, control_name, treatment_name in comparisons:
        result = _compute_single_comparison(
            comp_name, control_name, treatment_name,
            by_task, by_task_cost, agg_map,
        )
        results.append(result)

    return {"comparisons": results}


def _compute_single_comparison(
    comp_name: str,
    control_name: str,
    treatment_name: str,
    by_task: dict[str, dict[str, float]],
    by_task_cost: dict[str, dict[str, float]],
    agg_map: dict[str, Any],
) -> dict[str, Any]:
    common_tasks = [
        tid for tid in sorted(by_task.keys())
        if control_name in by_task[tid] and treatment_name in by_task[tid]
    ]

    scores_control: list[float] = []
    scores_treatment: list[float] = []
    deltas: list[float] = []

    for tid in common_tasks:
        sc = by_task[tid][control_name]
        st = by_task[tid][treatment_name]
        scores_control.append(sc)
        scores_treatment.append(st)
        deltas.append(st - sc)

    n = len(deltas)
    if n == 0:
        return {"comparison_name": comp_name, "error": "no_common_tasks"}

    mean_delta = sum(deltas) / n
    sorted_deltas = sorted(deltas)
    median_delta = statistics.median(deltas)
    wins = sum(1 for d in deltas if d > 0)
    losses = sum(1 for d in deltas if d < 0)
    ties = sum(1 for d in deltas if d == 0)
    wr = wins / (wins + losses) if (wins + losses) > 0 else 0.5

    mean_control = sum(scores_control) / n
    mean_treatment = sum(scores_treatment) / n

    control_agg = agg_map.get(control_name)
    treatment_agg = agg_map.get(treatment_name)

    cost_control = control_agg.total_cost_usd if control_agg else 0.0
    cost_treatment = treatment_agg.total_cost_usd if treatment_agg else 0.0
    cost_delta = cost_treatment - cost_control
    cost_ratio = cost_treatment / cost_control if cost_control > 0 else float("inf")

    cost_per_task_control = cost_control / n if n > 0 else 0.0
    cost_per_task_treatment = cost_treatment / n if n > 0 else 0.0
    cpp_control = control_agg.cost_per_mean_score_point if control_agg else 0.0
    cpp_treatment = treatment_agg.cost_per_mean_score_point if treatment_agg else 0.0
    cost_per_lift = (cost_delta / mean_delta) if mean_delta > 0 else None

    # Efficient frontier decision
    frontier = _efficient_frontier_decision(comp_name, mean_delta, cost_delta)

    return {
        "comparison_name": comp_name,
        "control_variant": control_name,
        "treatment_variant": treatment_name,
        "n": n,
        "control_mean": round(mean_control, 6),
        "treatment_mean": round(mean_treatment, 6),
        "mean_delta": round(mean_delta, 6),
        "median_delta": round(median_delta, 6),
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate_excluding_ties": round(wr, 4),
        "cost_a": round(cost_control, 8),
        "cost_b": round(cost_treatment, 8),
        "cost_delta": round(cost_delta, 8),
        "cost_ratio": round(cost_ratio, 4),
        "cost_per_task_a": round(cost_per_task_control, 8),
        "cost_per_task_b": round(cost_per_task_treatment, 8),
        "cost_per_mean_score_point_a": round(cpp_control, 8),
        "cost_per_mean_score_point_b": round(cpp_treatment, 8),
        "cost_per_lift_point": round(cost_per_lift, 8) if cost_per_lift is not None else None,
        "efficient_frontier_decision": frontier,
    }


def _efficient_frontier_decision(
    comp_name: str,
    mean_delta: float,
    cost_delta: float,
) -> str:
    if abs(mean_delta) < 0.005:
        return "INCONCLUSIVE"

    score_improved = mean_delta > 0
    cost_increased = cost_delta > 0

    if score_improved and not cost_increased:
        return "CHEAP_CALIBRATED_DOMINATES_NEXT_MODEL"
    elif score_improved and cost_increased:
        return "CHEAP_CALIBRATED_HIGHER_QUALITY_HIGHER_COST"
    elif not score_improved and not cost_increased:
        return "TRADEOFF_CHEAP_CALIBRATED_LOWER_COST_LOWER_SCORE"
    else:
        return "NEXT_MODEL_DOMINATES_CHEAP_CALIBRATED"
