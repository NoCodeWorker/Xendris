"""Scoring and lift aggregation for v0.9.0 runtime paired lift."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .runtime_lift_types import (
    RuntimeAuditResult,
    RuntimeScoredRecord,
    RuntimeTrace,
    RuntimeVariantAggregate,
)

FAMILIES = [
    "algorithmic_reasoning",
    "stateful_refactor",
    "edge_case_handling",
    "api_design_consistency",
    "performance_constraints",
]


def score_runtime_response(
    variant_name: str,
    provider_name: str,
    model_name: str,
    task_id: str,
    task_family: str,
    response_text: str,
    estimated_cost_usd: float | None = None,
) -> RuntimeScoredRecord:
    from benchmarks.finitexo_code_matrix_v0_6.real_provider_controlled_run.controlled_run_scoring import (
        score_response as v0_6_score_response,
    )
    v6 = v0_6_score_response(response_text)
    return RuntimeScoredRecord(
        variant_name=variant_name,
        provider_name=provider_name,
        model_name=model_name,
        task_id=task_id,
        task_family=task_family,
        score_total=v6.score_total,
        score_components=dict(v6.score_components),
        verified_success=v6.verified_success,
        estimated_cost_usd=estimated_cost_usd,
        normalized_response_text=" ".join(response_text.split()),
    )


def aggregate_by_variant(
    scored: list[RuntimeScoredRecord],
) -> list[RuntimeVariantAggregate]:
    groups: dict[str, list[RuntimeScoredRecord]] = {}
    for s in scored:
        groups.setdefault(s.variant_name, []).append(s)

    aggregates: list[RuntimeVariantAggregate] = []
    for variant_name, group in sorted(groups.items()):
        scores = [r.score_total for r in group]
        components = list(group[0].score_components.keys())
        component_means: dict[str, float] = {}
        for comp in components:
            vals = [r.score_components.get(comp, 0.0) for r in group]
            component_means[comp] = sum(vals) / len(vals) if vals else 0.0

        total_cost = sum(r.estimated_cost_usd or 0.0 for r in group)
        mean_score = sum(scores) / len(scores) if scores else 0.0
        cost_per_point = total_cost / mean_score if mean_score > 0 else 0.0

        aggregates.append(
            RuntimeVariantAggregate(
                variant_name=variant_name,
                provider_name=group[0].provider_name,
                task_count=len(group),
                mean_score=mean_score,
                component_means=component_means,
                min_score=min(scores),
                max_score=max(scores),
                verified_count=sum(1 for r in group if r.verified_success),
                total_cost_usd=total_cost,
                cost_per_mean_score_point=cost_per_point,
            )
        )
    return aggregates


def compute_paired_lift(
    scored: list[RuntimeScoredRecord],
    aggregates: list[RuntimeVariantAggregate],
) -> dict[str, Any]:
    by_task: dict[str, dict[str, float]] = {}
    by_task_cost: dict[str, dict[str, float]] = {}
    for r in scored:
        by_task.setdefault(r.task_id, {})[r.variant_name] = r.score_total
        by_task_cost.setdefault(r.task_id, {})[r.variant_name] = r.estimated_cost_usd or 0.0

    task_lifts: list[dict[str, Any]] = []

    def _pair_lift(base_name: str, compared_name: str, label: str) -> dict[str, Any]:
        lifts: list[float] = []
        cost_deltas: list[float] = []
        task_level: list[dict[str, Any]] = []
        for task_id, variants in sorted(by_task.items()):
            base = variants.get(base_name, 0.0)
            compared = variants.get(compared_name, 0.0)
            lift = compared - base
            lifts.append(lift)
            costs = by_task_cost.get(task_id, {})
            cost_deltas.append(costs.get(compared_name, 0.0) - costs.get(base_name, 0.0))
            task_level.append({
                "task_id": task_id,
                f"{base_name}_score": base,
                f"{compared_name}_score": compared,
                f"{label}_lift": round(lift, 6),
            })
        mean_lift = sum(lifts) / len(lifts) if lifts else 0.0
        total_cost_delta = sum(cost_deltas)
        cost_per_lift = round(abs(total_cost_delta) / mean_lift, 8) if mean_lift > 0 else None
        return {
            f"{label}_mean_lift": round(mean_lift, 6),
            f"{label}_cost_delta": round(total_cost_delta, 8),
            f"{label}_cost_per_lift_point": cost_per_lift,
            f"{label}_task_level_lifts": task_level,
        }

    result: dict[str, Any] = {}
    # wrapper vs base
    result.update(_pair_lift("deepseek_base", "deepseek_wrapper", "deepseek_wrapper_vs_base"))
    result.update(_pair_lift("openai_base", "openai_wrapper", "openai_wrapper_vs_base"))
    # runtime vs base
    result.update(_pair_lift("deepseek_base", "deepseek_runtime", "deepseek_runtime_vs_base"))
    result.update(_pair_lift("openai_base", "openai_runtime", "openai_runtime_vs_base"))
    # runtime vs wrapper
    result.update(_pair_lift("deepseek_wrapper", "deepseek_runtime", "deepseek_runtime_vs_wrapper"))
    result.update(_pair_lift("openai_wrapper", "openai_runtime", "openai_runtime_vs_wrapper"))
    # calibrated_runtime vs base
    result.update(_pair_lift("deepseek_base", "deepseek_calibrated_runtime", "deepseek_calibrated_runtime_vs_base"))
    result.update(_pair_lift("openai_base", "openai_calibrated_runtime", "openai_calibrated_runtime_vs_base"))
    # calibrated_runtime vs wrapper
    result.update(_pair_lift("deepseek_wrapper", "deepseek_calibrated_runtime", "deepseek_calibrated_runtime_vs_wrapper"))
    result.update(_pair_lift("openai_wrapper", "openai_calibrated_runtime", "openai_calibrated_runtime_vs_wrapper"))
    # calibrated_runtime vs runtime
    result.update(_pair_lift("deepseek_runtime", "deepseek_calibrated_runtime", "deepseek_calibrated_runtime_vs_runtime"))
    result.update(_pair_lift("openai_runtime", "openai_calibrated_runtime", "openai_calibrated_runtime_vs_runtime"))

    # Component lifts
    if aggregates:
        components = list(aggregates[0].component_means.keys())
        for label, variant_a, variant_b in [
            ("wrapper_vs_base_deepseek", "deepseek_wrapper", "deepseek_base"),
            ("wrapper_vs_base_openai", "openai_wrapper", "openai_base"),
            ("runtime_vs_base_deepseek", "deepseek_runtime", "deepseek_base"),
            ("runtime_vs_base_openai", "openai_runtime", "openai_base"),
            ("runtime_vs_wrapper_deepseek", "deepseek_runtime", "deepseek_wrapper"),
            ("runtime_vs_wrapper_openai", "openai_runtime", "openai_wrapper"),
            ("calibrated_vs_base_deepseek", "deepseek_calibrated_runtime", "deepseek_base"),
            ("calibrated_vs_base_openai", "openai_calibrated_runtime", "openai_base"),
            ("calibrated_vs_wrapper_deepseek", "deepseek_calibrated_runtime", "deepseek_wrapper"),
            ("calibrated_vs_wrapper_openai", "openai_calibrated_runtime", "openai_wrapper"),
            ("calibrated_vs_runtime_deepseek", "deepseek_calibrated_runtime", "deepseek_runtime"),
            ("calibrated_vs_runtime_openai", "openai_calibrated_runtime", "openai_runtime"),
        ]:
            comp_lift: dict[str, float] = {}
            for comp in components:
                a_mean = _component_mean(scored, variant_a, comp)
                b_mean = _component_mean(scored, variant_b, comp)
                comp_lift[comp] = round(a_mean - b_mean, 6)
            result[f"lift_by_component_{label}"] = comp_lift

    return result


def _component_mean(
    scored: list[RuntimeScoredRecord],
    variant_name: str,
    component: str,
) -> float:
    vals = [
        r.score_components.get(component, 0.0)
        for r in scored if r.variant_name == variant_name
    ]
    return sum(vals) / len(vals) if vals else 0.0


def aggregate_by_family_variant(
    scored: list[RuntimeScoredRecord],
) -> dict[str, dict[str, float]]:
    family_scores: dict[str, dict[str, list[float]]] = {}
    for r in scored:
        family_scores.setdefault(r.task_family, {}).setdefault(r.variant_name, []).append(r.score_total)

    result: dict[str, dict[str, float]] = {}
    for family in FAMILIES:
        if family not in family_scores:
            continue
        variant_means: dict[str, float] = {}
        for variant_name in (
            "deepseek_base", "deepseek_wrapper", "deepseek_runtime", "deepseek_calibrated_runtime",
            "openai_base", "openai_wrapper", "openai_runtime", "openai_calibrated_runtime",
        ):
            vals = family_scores[family].get(variant_name, [])
            variant_means[variant_name] = sum(vals) / len(vals) if vals else 0.0
        result[family] = variant_means
    return result


def compute_family_lift(
    scored: list[RuntimeScoredRecord],
) -> dict[str, Any]:
    family_scores = aggregate_by_family_variant(scored)

    family_lift: dict[str, dict[str, float]] = {}
    for family, variants in family_scores.items():
        ds_wrapper_lift = variants.get("deepseek_wrapper", 0.0) - variants.get("deepseek_base", 0.0)
        ds_runtime_lift = variants.get("deepseek_runtime", 0.0) - variants.get("deepseek_base", 0.0)
        ds_runtime_vs_wrapper = variants.get("deepseek_runtime", 0.0) - variants.get("deepseek_wrapper", 0.0)
        ds_calibrated_vs_base = variants.get("deepseek_calibrated_runtime", 0.0) - variants.get("deepseek_base", 0.0)
        ds_calibrated_vs_wrapper = variants.get("deepseek_calibrated_runtime", 0.0) - variants.get("deepseek_wrapper", 0.0)
        ds_calibrated_vs_runtime = variants.get("deepseek_calibrated_runtime", 0.0) - variants.get("deepseek_runtime", 0.0)
        oa_wrapper_lift = variants.get("openai_wrapper", 0.0) - variants.get("openai_base", 0.0)
        oa_runtime_lift = variants.get("openai_runtime", 0.0) - variants.get("openai_base", 0.0)
        oa_runtime_vs_wrapper = variants.get("openai_runtime", 0.0) - variants.get("openai_wrapper", 0.0)
        oa_calibrated_vs_base = variants.get("openai_calibrated_runtime", 0.0) - variants.get("openai_base", 0.0)
        oa_calibrated_vs_wrapper = variants.get("openai_calibrated_runtime", 0.0) - variants.get("openai_wrapper", 0.0)
        oa_calibrated_vs_runtime = variants.get("openai_calibrated_runtime", 0.0) - variants.get("openai_runtime", 0.0)
        family_lift[family] = {
            "deepseek_base_mean": round(variants.get("deepseek_base", 0.0), 6),
            "deepseek_wrapper_mean": round(variants.get("deepseek_wrapper", 0.0), 6),
            "deepseek_runtime_mean": round(variants.get("deepseek_runtime", 0.0), 6),
            "deepseek_calibrated_runtime_mean": round(variants.get("deepseek_calibrated_runtime", 0.0), 6),
            "openai_base_mean": round(variants.get("openai_base", 0.0), 6),
            "openai_wrapper_mean": round(variants.get("openai_wrapper", 0.0), 6),
            "openai_runtime_mean": round(variants.get("openai_runtime", 0.0), 6),
            "openai_calibrated_runtime_mean": round(variants.get("openai_calibrated_runtime", 0.0), 6),
            "deepseek_wrapper_lift_vs_base": round(ds_wrapper_lift, 6),
            "deepseek_runtime_lift_vs_base": round(ds_runtime_lift, 6),
            "deepseek_runtime_lift_vs_wrapper": round(ds_runtime_vs_wrapper, 6),
            "deepseek_calibrated_lift_vs_base": round(ds_calibrated_vs_base, 6),
            "deepseek_calibrated_lift_vs_wrapper": round(ds_calibrated_vs_wrapper, 6),
            "deepseek_calibrated_lift_vs_runtime": round(ds_calibrated_vs_runtime, 6),
            "openai_wrapper_lift_vs_base": round(oa_wrapper_lift, 6),
            "openai_runtime_lift_vs_base": round(oa_runtime_lift, 6),
            "openai_runtime_lift_vs_wrapper": round(oa_runtime_vs_wrapper, 6),
            "openai_calibrated_lift_vs_base": round(oa_calibrated_vs_base, 6),
            "openai_calibrated_lift_vs_wrapper": round(oa_calibrated_vs_wrapper, 6),
            "openai_calibrated_lift_vs_runtime": round(oa_calibrated_vs_runtime, 6),
        }

    def _mean_lift(key: str) -> float:
        vals = [v[key] for v in family_lift.values()]
        return round(sum(vals) / len(vals), 6) if vals else 0.0

    return {
        "family_scores": family_scores,
        "family_lift": family_lift,
        "overall_deepseek_wrapper_lift_vs_base_mean": _mean_lift("deepseek_wrapper_lift_vs_base"),
        "overall_deepseek_runtime_lift_vs_base_mean": _mean_lift("deepseek_runtime_lift_vs_base"),
        "overall_deepseek_runtime_lift_vs_wrapper_mean": _mean_lift("deepseek_runtime_lift_vs_wrapper"),
        "overall_deepseek_calibrated_lift_vs_base_mean": _mean_lift("deepseek_calibrated_lift_vs_base"),
        "overall_deepseek_calibrated_lift_vs_wrapper_mean": _mean_lift("deepseek_calibrated_lift_vs_wrapper"),
        "overall_deepseek_calibrated_lift_vs_runtime_mean": _mean_lift("deepseek_calibrated_lift_vs_runtime"),
        "overall_openai_wrapper_lift_vs_base_mean": _mean_lift("openai_wrapper_lift_vs_base"),
        "overall_openai_runtime_lift_vs_base_mean": _mean_lift("openai_runtime_lift_vs_base"),
        "overall_openai_runtime_lift_vs_wrapper_mean": _mean_lift("openai_runtime_lift_vs_wrapper"),
        "overall_openai_calibrated_lift_vs_base_mean": _mean_lift("openai_calibrated_lift_vs_base"),
        "overall_openai_calibrated_lift_vs_wrapper_mean": _mean_lift("openai_calibrated_lift_vs_wrapper"),
        "overall_openai_calibrated_lift_vs_runtime_mean": _mean_lift("openai_calibrated_lift_vs_runtime"),
    }


def compute_repair_metrics(traces: list[RuntimeTrace]) -> dict[str, Any]:
    by_provider: dict[str, dict[str, any]] = {}
    for t in traces:
        if not t.repair_attempted:
            continue
        prov = t.provider_name
        by_provider.setdefault(prov, {"attempts": 0, "successes": 0, "failures": 0, "unknown": 0})
        by_provider[prov]["attempts"] += 1
        if t.repair_audit:
            if t.repair_audit.score > (t.initial_audit.score if t.initial_audit else 0):
                by_provider[prov]["successes"] += 1
            elif t.repair_audit.score < (t.initial_audit.score if t.initial_audit else 0):
                by_provider[prov]["failures"] += 1
            else:
                by_provider[prov]["unknown"] += 1

    result: dict[str, any] = {}
    for prov, data in by_provider.items():
        total = data["attempts"]
        result[prov] = {
            "repair_attempts": total,
            "repair_successes": data["successes"],
            "repair_success_rate": round(data["successes"] / total, 4) if total > 0 else 0.0,
        }
    return result


def compute_audit_decision_distribution(traces: list[RuntimeTrace]) -> dict[str, any]:
    by_provider: dict[str, dict[str, int]] = {}
    for t in traces:
        prov = t.provider_name
        by_provider.setdefault(prov, {})
        dec = t.audit_decision.value
        by_provider[prov][dec] = by_provider[prov].get(dec, 0) + 1
    return by_provider
