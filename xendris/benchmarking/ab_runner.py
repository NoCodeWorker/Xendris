"""A/B Runner for measuring improvements of Xendris over DeepSeek."""

from __future__ import annotations

import hashlib
import time
from typing import Any, Callable, Mapping

from .types import ABComparisonResult, ABRunSummary, BenchmarkSample, SystemRunResult
from .scoring import score_result_against_expected


def compute_result_fingerprint(sample_id: str, system_name: str, answer: str) -> str:
    """Generate a stable 12-char SHA256 fingerprint for a run result."""
    payload = f"{sample_id}:{system_name}:{answer}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]


def run_ab_benchmark(
    samples: list[BenchmarkSample],
    deepseek_callable: Callable[[BenchmarkSample], dict[str, Any]],
    xendris_callable: Callable[[BenchmarkSample], dict[str, Any]],
    config: Mapping[str, Any] | None = None,
) -> list[ABComparisonResult]:
    """Execute each sample against both systems and return the comparison results.

    Errors from callables are captured and recorded in the result without aborting.
    """
    config = config or {}
    comparisons = []

    for sample in samples:
        # 1. Execute DeepSeek base
        start_ds = time.perf_counter()
        try:
            ds_raw = deepseek_callable(sample)
            latency_ds = ds_raw.get("latency_ms") or int((time.perf_counter() - start_ds) * 1000.0)
            ds_result = SystemRunResult(
                sample_id=sample.sample_id,
                system_name="deepseek",
                base_model=ds_raw.get("base_model", "deepseek-chat"),
                answer=ds_raw.get("answer", ""),
                decision=ds_raw.get("decision"),
                reason=ds_raw.get("reason"),
                scoring_allowed=ds_raw.get("scoring_allowed", True),
                latency_ms=latency_ds,
                input_tokens=ds_raw.get("input_tokens"),
                output_tokens=ds_raw.get("output_tokens"),
                estimated_cost_usd=ds_raw.get("estimated_cost_usd", 0.0),
                error=ds_raw.get("error"),
                fingerprint=compute_result_fingerprint(sample.sample_id, "deepseek", ds_raw.get("answer", "")),
            )
        except Exception as e:
            ds_result = SystemRunResult(
                sample_id=sample.sample_id,
                system_name="deepseek",
                base_model="deepseek-chat",
                answer="",
                error=str(e),
                scoring_allowed=False,
                fingerprint=compute_result_fingerprint(sample.sample_id, "deepseek", ""),
            )

        # 2. Execute Xendris
        start_xe = time.perf_counter()
        try:
            xe_raw = xendris_callable(sample)
            latency_xe = xe_raw.get("latency_ms") or int((time.perf_counter() - start_xe) * 1000.0)
            xe_result = SystemRunResult(
                sample_id=sample.sample_id,
                system_name="xendris",
                base_model=xe_raw.get("base_model", "deepseek-chat"),
                answer=xe_raw.get("answer", ""),
                decision=xe_raw.get("decision"),
                reason=xe_raw.get("reason"),
                scoring_allowed=xe_raw.get("scoring_allowed", False),
                latency_ms=latency_xe,
                input_tokens=xe_raw.get("input_tokens"),
                output_tokens=xe_raw.get("output_tokens"),
                estimated_cost_usd=xe_raw.get("estimated_cost_usd", 0.0),
                error=xe_raw.get("error"),
                fingerprint=compute_result_fingerprint(sample.sample_id, "xendris", xe_raw.get("answer", "")),
            )
        except Exception as e:
            xe_result = SystemRunResult(
                sample_id=sample.sample_id,
                system_name="xendris",
                base_model="deepseek-chat",
                answer="",
                error=str(e),
                scoring_allowed=False,
                fingerprint=compute_result_fingerprint(sample.sample_id, "xendris", ""),
            )

        # 3. Score results against expected targets
        ds_score = score_result_against_expected(ds_result, sample)
        xe_score = score_result_against_expected(xe_result, sample)
        delta = xe_score - ds_score

        # Determine winner
        if delta > 0:
            winner = "xendris"
        elif delta < 0:
            winner = "deepseek"
        else:
            winner = "tie"

        comparisons.append(
            ABComparisonResult(
                sample_id=sample.sample_id,
                category=sample.category,
                deepseek_result=ds_result,
                xendris_result=xe_result,
                deepseek_score=ds_score,
                xendris_score=xe_score,
                delta_score=delta,
                winner=winner,
                notes=xe_result.error or ds_result.error,
            )
        )

    return comparisons


def summarize_ab_results(results: list[ABComparisonResult]) -> ABRunSummary:
    """Aggregate comparison results and calculate overhead, cost, and rate statistics."""
    total = len(results)
    if total == 0:
        return ABRunSummary(
            total_samples=0, xendris_wins=0, deepseek_wins=0, ties=0,
            average_deepseek_score=0.0, average_xendris_score=0.0, average_delta=0.0,
            xendris_win_rate=0.0, deepseek_win_rate=0.0, tie_rate=0.0,
            average_latency_deepseek_ms=0.0, average_latency_xendris_ms=0.0, latency_overhead_ms=0.0,
            total_cost_deepseek_usd=0.0, total_cost_xendris_usd=0.0, cost_overhead_usd=0.0,
            xendris_exclusion_rate=0.0, xendris_human_review_rate=0.0,
            cost_per_valid_answer_deepseek=0.0, cost_per_valid_answer_xendris=0.0
        )

    wins_xe = sum(1 for r in results if r.winner == "xendris")
    wins_ds = sum(1 for r in results if r.winner == "deepseek")
    ties = sum(1 for r in results if r.winner == "tie")

    sum_ds_score = sum(r.deepseek_score for r in results)
    sum_xe_score = sum(r.xendris_score for r in results)

    # Latencies
    ds_latencies = [r.deepseek_result.latency_ms for r in results if r.deepseek_result.latency_ms is not None]
    xe_latencies = [r.xendris_result.latency_ms for r in results if r.xendris_result.latency_ms is not None]
    avg_lat_ds = sum(ds_latencies) / len(ds_latencies) if ds_latencies else 0.0
    avg_lat_xe = sum(xe_latencies) / len(xe_latencies) if xe_latencies else 0.0

    # Costs
    ds_costs = [r.deepseek_result.estimated_cost_usd for r in results if r.deepseek_result.estimated_cost_usd is not None]
    xe_costs = [r.xendris_result.estimated_cost_usd for r in results if r.xendris_result.estimated_cost_usd is not None]
    tot_cost_ds = sum(ds_costs)
    tot_cost_xe = sum(xe_costs)

    # Exclusion and human review counts for Xendris
    exclusions_xe = 0
    human_reviews_xe = 0
    valid_answers_xe = 0
    valid_answers_ds = 0

    for r in results:
        dec_xe = r.xendris_result.decision
        scoring_xe = r.xendris_result.scoring_allowed

        # Check exclusion
        if dec_xe in {"EXCLUDE", "EXCLUDE_FROM_SCORING"} or scoring_xe is False:
            exclusions_xe += 1
        else:
            valid_answers_xe += 1

        if dec_xe == "HUMAN_REVIEW_REQUIRED":
            human_reviews_xe += 1

        # Check deepseek valid answers
        dec_ds = r.deepseek_result.decision
        scoring_ds = r.deepseek_result.scoring_allowed
        if dec_ds not in {"EXCLUDE", "EXCLUDE_FROM_SCORING"} and scoring_ds is not False:
            valid_answers_ds += 1

    # Cost per valid answer (total cost / valid answers count)
    cost_per_valid_ds = tot_cost_ds / valid_answers_ds if valid_answers_ds > 0 else tot_cost_ds
    cost_per_valid_xe = tot_cost_xe / valid_answers_xe if valid_answers_xe > 0 else tot_cost_xe

    return ABRunSummary(
        total_samples=total,
        xendris_wins=wins_xe,
        deepseek_wins=wins_ds,
        ties=ties,
        average_deepseek_score=round(sum_ds_score / total, 4),
        average_xendris_score=round(sum_xe_score / total, 4),
        average_delta=round((sum_xe_score - sum_ds_score) / total, 4),
        xendris_win_rate=round(wins_xe / total, 4),
        deepseek_win_rate=round(wins_ds / total, 4),
        tie_rate=round(ties / total, 4),
        average_latency_deepseek_ms=round(avg_lat_ds, 2),
        average_latency_xendris_ms=round(avg_lat_xe, 2),
        latency_overhead_ms=round(max(0.0, avg_lat_xe - avg_lat_ds), 2),
        total_cost_deepseek_usd=round(tot_cost_ds, 6),
        total_cost_xendris_usd=round(tot_cost_xe, 6),
        cost_overhead_usd=round(max(0.0, tot_cost_xe - tot_cost_ds), 6),
        xendris_exclusion_rate=round(exclusions_xe / total, 4),
        xendris_human_review_rate=round(human_reviews_xe / total, 4),
        cost_per_valid_answer_deepseek=round(cost_per_valid_ds, 6),
        cost_per_valid_answer_xendris=round(cost_per_valid_xe, 6),
    )
