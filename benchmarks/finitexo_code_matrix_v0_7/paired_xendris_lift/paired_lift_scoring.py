"""Scoring and paired-lift aggregation for v0.7.0."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from benchmarks.finitexo_code_matrix_v0_6.real_provider_controlled_run.controlled_run_scoring import (
    score_response as v0_6_score_response,
    ScoredRecord as V06ScoredRecord,
)


@dataclass
class PairedLiftScoredRecord:
    variant_name: str
    provider_name: str
    model_name: str
    task_id: str
    score_total: float
    score_components: dict[str, float]
    verified_success: bool
    estimated_cost_usd: float | None = None
    normalized_response_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_name": self.variant_name,
            "provider_name": self.provider_name,
            "model_name": self.model_name,
            "task_id": self.task_id,
            "score_total": self.score_total,
            "score_components": dict(self.score_components),
            "verified_success": self.verified_success,
            "estimated_cost_usd": self.estimated_cost_usd,
        }


@dataclass
class PairedLiftVariantAggregate:
    variant_name: str
    provider_name: str
    task_count: int
    mean_score: float
    component_means: dict[str, float]
    min_score: float
    max_score: float
    verified_count: int
    total_cost_usd: float
    cost_per_mean_score_point: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "variant_name": self.variant_name,
            "provider_name": self.provider_name,
            "task_count": self.task_count,
            "mean_score": self.mean_score,
            "component_means": dict(self.component_means),
            "min_score": self.min_score,
            "max_score": self.max_score,
            "verified_count": self.verified_count,
            "total_cost_usd": self.total_cost_usd,
            "cost_per_mean_score_point": self.cost_per_mean_score_point,
        }


def score_paired_lift_response(
    variant_name: str,
    provider_name: str,
    model_name: str,
    task_id: str,
    response_text: str,
    estimated_cost_usd: float | None = None,
) -> PairedLiftScoredRecord:
    v6 = v0_6_score_response(response_text)
    return PairedLiftScoredRecord(
        variant_name=variant_name,
        provider_name=provider_name,
        model_name=model_name,
        task_id=task_id,
        score_total=v6.score_total,
        score_components=dict(v6.score_components),
        verified_success=v6.verified_success,
        estimated_cost_usd=estimated_cost_usd,
        normalized_response_text=" ".join(response_text.split()),
    )


def aggregate_by_variant(
    scored: list[PairedLiftScoredRecord],
) -> list[PairedLiftVariantAggregate]:
    groups: dict[str, list[PairedLiftScoredRecord]] = {}
    for s in scored:
        groups.setdefault(s.variant_name, []).append(s)

    aggregates: list[PairedLiftVariantAggregate] = []
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
            PairedLiftVariantAggregate(
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
    scored: list[PairedLiftScoredRecord],
    aggregates: list[PairedLiftVariantAggregate],
) -> dict[str, Any]:
    by_task: dict[str, dict[str, float]] = {}
    by_task_cost: dict[str, dict[str, float]] = {}
    for r in scored:
        by_task.setdefault(r.task_id, {})[r.variant_name] = r.score_total
        by_task_cost.setdefault(r.task_id, {})[r.variant_name] = r.estimated_cost_usd or 0.0

    task_lifts: list[dict[str, Any]] = []
    ds_lifts: list[float] = []
    oa_lifts: list[float] = []
    ds_cost_deltas: list[float] = []
    oa_cost_deltas: list[float] = []

    for task_id, variants in sorted(by_task.items()):
        ds_base = variants.get("deepseek_base", 0.0)
        ds_xendris = variants.get("deepseek_xendris", 0.0)
        oa_base = variants.get("openai_base", 0.0)
        oa_xendris = variants.get("openai_xendris", 0.0)

        ds_lift = ds_xendris - ds_base
        oa_lift = oa_xendris - oa_base
        ds_lifts.append(ds_lift)
        oa_lifts.append(oa_lift)

        costs = by_task_cost.get(task_id, {})
        ds_cost_deltas.append(costs.get("deepseek_xendris", 0.0) - costs.get("deepseek_base", 0.0))
        oa_cost_deltas.append(costs.get("openai_xendris", 0.0) - costs.get("openai_base", 0.0))

        task_lifts.append({
            "task_id": task_id,
            "deepseek_base_score": ds_base,
            "deepseek_xendris_score": ds_xendris,
            "openai_base_score": oa_base,
            "openai_xendris_score": oa_xendris,
            "deepseek_lift": round(ds_lift, 6),
            "openai_lift": round(oa_lift, 6),
        })

    ds_mean_lift = sum(ds_lifts) / len(ds_lifts) if ds_lifts else 0.0
    oa_mean_lift = sum(oa_lifts) / len(oa_lifts) if oa_lifts else 0.0
    ds_total_cost_delta = sum(ds_cost_deltas)
    oa_total_cost_delta = sum(oa_cost_deltas)

    ds_agg = next((a for a in aggregates if a.variant_name == "deepseek_xendris"), None)
    oa_agg = next((a for a in aggregates if a.variant_name == "openai_xendris"), None)

    ds_comp_lift: dict[str, float] = {}
    oa_comp_lift: dict[str, float] = {}
    if aggregates:
        components = list(aggregates[0].component_means.keys())
        for comp in components:
            ds_base_comp = _component_mean(scored, "deepseek_base", comp)
            ds_xend_comp = _component_mean(scored, "deepseek_xendris", comp)
            oa_base_comp = _component_mean(scored, "openai_base", comp)
            oa_xend_comp = _component_mean(scored, "openai_xendris", comp)
            ds_comp_lift[comp] = round(ds_xend_comp - ds_base_comp, 6)
            oa_comp_lift[comp] = round(oa_xend_comp - oa_base_comp, 6)

    return {
        "deepseek_xendris_minus_base": round(ds_mean_lift, 6),
        "openai_xendris_minus_base": round(oa_mean_lift, 6),
        "xendris_lift_by_component_deepseek": ds_comp_lift,
        "xendris_lift_by_component_openai": oa_comp_lift,
        "cost_delta_xendris_vs_base_deepseek": round(ds_total_cost_delta, 8),
        "cost_delta_xendris_vs_base_openai": round(oa_total_cost_delta, 8),
        "cost_per_lift_point_deepseek": (
            round(abs(ds_total_cost_delta) / ds_mean_lift, 8) if ds_mean_lift > 0 else None
        ),
        "cost_per_lift_point_openai": (
            round(abs(oa_total_cost_delta) / oa_mean_lift, 8) if oa_mean_lift > 0 else None
        ),
        "task_level_lifts": task_lifts,
    }


def _component_mean(
    scored: list[PairedLiftScoredRecord],
    variant_name: str,
    component: str,
) -> float:
    vals = [
        r.score_components.get(component, 0.0)
        for r in scored
        if r.variant_name == variant_name
    ]
    return sum(vals) / len(vals) if vals else 0.0
