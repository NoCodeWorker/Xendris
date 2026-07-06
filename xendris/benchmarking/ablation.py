"""Ablation benchmark utilities for Xendris benchmarking.

This module is intentionally provider-agnostic. It accepts injected callables
for each variant and does not perform network calls by itself.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import inspect
import json
from pathlib import Path
import time
from typing import Any, Callable, Iterable, Mapping, Sequence

from .scoring import score_result_against_expected
from .types import BenchmarkSample, SystemRunResult


DEFAULT_ABLATION_VARIANT_ORDER = [
    "deepseek_base",
    "deepseek_response_contract",
    "deepseek_trust_reasoning",
    "deepseek_benchmark_gate",
    "xendris_full",
]

HUMAN_REVIEW_MARKERS = {"HUMAN_REVIEW_REQUIRED", "HUMAN_REVIEW_POLICY"}


@dataclass(frozen=True)
class AblationVariant:
    """Callable wrapper for one ablation variant."""

    name: str
    runner: Callable[..., Mapping[str, Any] | SystemRunResult]


@dataclass(frozen=True)
class AblationRunResult:
    """Result for one sample executed against one ablation variant."""

    sample_id: str
    category: str
    system_name: str
    answer: str
    decision: str | None
    reason: str | None
    scoring_allowed: bool
    latency_ms: float
    estimated_cost_usd: float
    fingerprint: str
    score: float
    counts_as_valid_correct: bool
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation."""
        return asdict(self)


def compute_ablation_fingerprint(
    sample_id: str,
    system_name: str,
    answer: str,
    decision: str | None,
    reason: str | None,
    scoring_allowed: bool,
) -> str:
    """Return a stable fingerprint for a variant result.

    Runtime-specific fields such as latency and cost are deliberately excluded.
    """
    payload = {
        "answer": answer,
        "decision": decision,
        "reason": reason,
        "sample_id": sample_id,
        "scoring_allowed": scoring_allowed,
        "system_name": system_name,
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:16]


def run_ablation_benchmark(
    samples: Sequence[BenchmarkSample],
    variants: Mapping[str, Callable[..., Mapping[str, Any] | SystemRunResult]]
    | Iterable[AblationVariant],
    config: Mapping[str, Any] | None = None,
) -> list[AblationRunResult]:
    """Run all samples against all ablation variants.

    Variant failures are captured as failed results and do not abort the full
    benchmark.
    """
    config = config or {}
    normalized_variants = _normalize_variants(variants)
    results: list[AblationRunResult] = []

    for sample in samples:
        for variant in normalized_variants:
            results.append(_run_variant(sample, variant, config))

    return results


def summarize_ablation_results(
    results: Sequence[AblationRunResult],
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Summarize ablation results by variant and category."""
    config = config or {}
    base_variant = str(config.get("base_variant", "deepseek_base"))
    grouped = _group_by_variant(results)
    variant_order = [name for name in DEFAULT_ABLATION_VARIANT_ORDER if name in grouped]
    variant_order.extend(name for name in grouped if name not in variant_order)

    variant_scores = {
        name: _mean([result.score for result in grouped[name]])
        for name in variant_order
    }
    base_score = variant_scores.get(base_variant, 0.0)

    by_variant: dict[str, dict[str, Any]] = {}
    previous_score: float | None = None

    for name in variant_order:
        variant_results = grouped[name]
        total_cost = sum(result.estimated_cost_usd for result in variant_results)
        valid_results = [result for result in variant_results if result.scoring_allowed]
        human_review_count = sum(_is_human_review(result) for result in variant_results)
        exclusion_count = sum(not result.scoring_allowed for result in variant_results)
        average_score = variant_scores[name]
        wins, ties, losses = _compare_against_base(results, name, base_variant)

        by_variant[name] = {
            "system_name": name,
            "sample_count": len(variant_results),
            "mean_score": round(average_score, 4),
            "wins_vs_deepseek_base": wins,
            "ties_vs_deepseek_base": ties,
            "losses_vs_deepseek_base": losses,
            "delta_vs_deepseek_base": round(average_score - base_score, 4),
            "delta_vs_previous_variant": (
                0.0 if previous_score is None else round(average_score - previous_score, 4)
            ),
            "exclusion_rate": round(exclusion_count / len(variant_results), 4)
            if variant_results
            else 0.0,
            "human_review_rate": round(human_review_count / len(variant_results), 4)
            if variant_results
            else 0.0,
            "estimated_cost_usd": round(total_cost, 8),
            "average_latency_ms": round(_mean([r.latency_ms for r in variant_results]), 4),
            "cost_per_valid_response": (
                round(total_cost / len(valid_results), 8) if valid_results else None
            ),
            "valid_correct_count": sum(r.counts_as_valid_correct for r in variant_results),
            "breakdown_by_category": _breakdown_by_category(variant_results),
        }
        previous_score = average_score

    return {
        "base_variant": base_variant,
        "variant_order": variant_order,
        "total_results": len(results),
        "variants": by_variant,
        "breakdown_by_category": _global_breakdown_by_category(results),
    }


def write_ablation_results_jsonl(results: Sequence[AblationRunResult], path: str | Path) -> None:
    """Write ablation results as JSON Lines."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for result in results:
            handle.write(json.dumps(result.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")


def write_ablation_results_json(results: Sequence[AblationRunResult], path: str | Path) -> None:
    """Write ablation results as a JSON array."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = [result.to_dict() for result in results]
    with destination.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)


def _normalize_variants(
    variants: Mapping[str, Callable[..., Mapping[str, Any] | SystemRunResult]]
    | Iterable[AblationVariant],
) -> list[AblationVariant]:
    if isinstance(variants, Mapping):
        normalized = [AblationVariant(name=name, runner=runner) for name, runner in variants.items()]
    else:
        normalized = list(variants)

    names = [variant.name for variant in normalized]
    duplicate_names = sorted({name for name in names if names.count(name) > 1})
    if duplicate_names:
        raise ValueError(f"Ablation variant names must be unique: {', '.join(duplicate_names)}")
    return normalized


def _run_variant(
    sample: BenchmarkSample,
    variant: AblationVariant,
    config: Mapping[str, Any],
) -> AblationRunResult:
    start = time.perf_counter()
    try:
        raw = _call_variant(variant.runner, sample, config)
        latency_ms = _coerce_float(_raw_get(raw, "latency_ms"), None)
        if latency_ms is None:
            latency_ms = (time.perf_counter() - start) * 1000.0
        result = _build_result(sample, variant.name, raw, latency_ms, error=None)
    except Exception as exc:  # noqa: BLE001 - benchmark must isolate variant failures.
        latency_ms = (time.perf_counter() - start) * 1000.0
        raw_error = {
            "answer": "",
            "decision": "ERROR",
            "reason": exc.__class__.__name__,
            "scoring_allowed": False,
            "estimated_cost_usd": 0.0,
        }
        result = _build_result(sample, variant.name, raw_error, latency_ms, error=str(exc))
    return result


def _call_variant(
    runner: Callable[..., Mapping[str, Any] | SystemRunResult],
    sample: BenchmarkSample,
    config: Mapping[str, Any],
) -> Mapping[str, Any] | SystemRunResult:
    parameters = inspect.signature(runner).parameters
    if len(parameters) >= 2:
        return runner(sample, config)
    return runner(sample)


def _build_result(
    sample: BenchmarkSample,
    system_name: str,
    raw: Mapping[str, Any] | SystemRunResult,
    latency_ms: float,
    error: str | None,
) -> AblationRunResult:
    answer = str(_raw_get(raw, "answer", "") or "")
    decision = _optional_string(_raw_get(raw, "decision"))
    reason = _optional_string(_raw_get(raw, "reason"))
    scoring_allowed = bool(_raw_get(raw, "scoring_allowed", True))
    estimated_cost_usd = _coerce_float(_raw_get(raw, "estimated_cost_usd"), 0.0) or 0.0

    system_result = SystemRunResult(
        sample_id=sample.sample_id,
        system_name=system_name,
        base_model=str(_raw_get(raw, "base_model", "unknown") or "unknown"),
        answer=answer,
        decision=decision,
        reason=reason,
        scoring_allowed=scoring_allowed,
        latency_ms=int(round(latency_ms)),
        estimated_cost_usd=estimated_cost_usd,
        error=error or _optional_string(_raw_get(raw, "error")),
    )
    score = _coerce_float(_raw_get(raw, "score"), None)
    if score is None:
        score = score_result_against_expected(system_result, sample)

    fingerprint = compute_ablation_fingerprint(
        sample.sample_id,
        system_name,
        answer,
        decision,
        reason,
        scoring_allowed,
    )
    counts_as_valid_correct = scoring_allowed and score >= 1.0 and not error

    return AblationRunResult(
        sample_id=sample.sample_id,
        category=sample.category,
        system_name=system_name,
        answer=answer,
        decision=decision,
        reason=reason,
        scoring_allowed=scoring_allowed,
        latency_ms=round(latency_ms, 4),
        estimated_cost_usd=estimated_cost_usd,
        fingerprint=fingerprint,
        score=round(score, 4),
        counts_as_valid_correct=counts_as_valid_correct,
        error=error or _optional_string(_raw_get(raw, "error")),
    )


def _raw_get(raw: Mapping[str, Any] | SystemRunResult, key: str, default: Any = None) -> Any:
    if isinstance(raw, SystemRunResult):
        return getattr(raw, key, default)
    return raw.get(key, default)


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _coerce_float(value: Any, default: float | None) -> float | None:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _group_by_variant(results: Sequence[AblationRunResult]) -> dict[str, list[AblationRunResult]]:
    grouped: dict[str, list[AblationRunResult]] = {}
    for result in results:
        grouped.setdefault(result.system_name, []).append(result)
    return grouped


def _group_by_sample(results: Sequence[AblationRunResult]) -> dict[str, dict[str, AblationRunResult]]:
    grouped: dict[str, dict[str, AblationRunResult]] = {}
    for result in results:
        grouped.setdefault(result.sample_id, {})[result.system_name] = result
    return grouped


def _compare_against_base(
    results: Sequence[AblationRunResult],
    variant_name: str,
    base_variant: str,
) -> tuple[int, int, int]:
    wins = ties = losses = 0
    for sample_results in _group_by_sample(results).values():
        variant = sample_results.get(variant_name)
        base = sample_results.get(base_variant)
        if variant is None or base is None:
            continue
        if variant.score > base.score:
            wins += 1
        elif variant.score < base.score:
            losses += 1
        else:
            ties += 1
    return wins, ties, losses


def _is_human_review(result: AblationRunResult) -> bool:
    decision = (result.decision or "").upper()
    reason = (result.reason or "").upper()
    return decision in HUMAN_REVIEW_MARKERS or reason in HUMAN_REVIEW_MARKERS


def _breakdown_by_category(results: Sequence[AblationRunResult]) -> dict[str, dict[str, Any]]:
    categories = sorted({result.category for result in results})
    breakdown: dict[str, dict[str, Any]] = {}
    for category in categories:
        category_results = [result for result in results if result.category == category]
        breakdown[category] = {
            "sample_count": len(category_results),
            "mean_score": round(_mean([result.score for result in category_results]), 4),
            "exclusion_rate": round(
                sum(not result.scoring_allowed for result in category_results) / len(category_results),
                4,
            )
            if category_results
            else 0.0,
            "human_review_rate": round(
                sum(_is_human_review(result) for result in category_results) / len(category_results),
                4,
            )
            if category_results
            else 0.0,
            "average_latency_ms": round(_mean([result.latency_ms for result in category_results]), 4),
            "estimated_cost_usd": round(
                sum(result.estimated_cost_usd for result in category_results),
                8,
            ),
        }
    return breakdown


def _global_breakdown_by_category(results: Sequence[AblationRunResult]) -> dict[str, dict[str, Any]]:
    categories = sorted({result.category for result in results})
    breakdown: dict[str, dict[str, Any]] = {}
    for category in categories:
        category_results = [result for result in results if result.category == category]
        breakdown[category] = _breakdown_by_category(category_results)[category]
    return breakdown
