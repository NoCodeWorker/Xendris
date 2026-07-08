from __future__ import annotations

import math
import statistics
from typing import Any

from benchmarks.finitexo_code_matrix_v0_9.runtime_evidence_gate.evidence_gate_config import (
    COMPARISON_SPECS,
    EXPECTED_FAMILIES,
    RuntimeEvidenceGateConfig,
)


class _LCG:
    """Linear congruential generator for deterministic pseudo-random numbers."""

    def __init__(self, seed: int) -> None:
        self.state = seed & 0x7FFFFFFF

    def next(self) -> int:
        self.state = (self.state * 1103515245 + 12345) & 0x7FFFFFFF
        return self.state

    def randint(self, low: int, high: int) -> int:
        span = high - low + 1
        return low + (self.next() % span)


def _compute_bootstrap_ci(
    lifts: list[float],
    iterations: int,
    seed: int,
) -> tuple[float, float]:
    n = len(lifts)
    means: list[float] = []
    rng = _LCG(seed)
    for _ in range(iterations):
        total = 0.0
        for _ in range(n):
            idx = rng.randint(0, n - 1)
            total += lifts[idx]
        means.append(total / n)
    means.sort()
    low_idx = int(round(iterations * 0.025))
    high_idx = int(round(iterations * 0.975))
    low_idx = max(0, min(low_idx, iterations - 1))
    high_idx = max(0, min(high_idx, iterations - 1))
    return (means[low_idx], means[high_idx])


def compute_comparison(
    control_scores: list[dict[str, Any]],
    treatment_scores: list[dict[str, Any]],
    control_name: str,
    treatment_name: str,
    config: RuntimeEvidenceGateConfig,
) -> dict[str, Any]:
    score_map_control: dict[str, float] = {
        s["task_id"]: s["score_total"] for s in control_scores
    }
    score_map_treatment: dict[str, float] = {
        s["task_id"]: s["score_total"] for s in treatment_scores
    }

    common_tasks = set(score_map_control.keys()) & set(score_map_treatment.keys())
    lifts: list[float] = []
    for task_id in sorted(common_tasks):
        lifts.append(score_map_treatment[task_id] - score_map_control[task_id])
    n = len(lifts)
    if n == 0:
        return {"error": "no_common_tasks", "n": 0}

    mean_lift = statistics.mean(lifts)
    sorted_lifts = sorted(lifts)
    median_lift = statistics.median(lifts)
    min_lift = sorted_lifts[0]
    max_lift = sorted_lifts[-1]

    wins = sum(1 for L in lifts if L > 0)
    losses = sum(1 for L in lifts if L < 0)
    ties = sum(1 for L in lifts if L == 0)
    win_rate_excluding_ties = wins / (wins + losses) if (wins + losses) > 0 else 0.5
    non_negative_rate = (wins + ties) / n if n > 0 else 0.0

    variance = statistics.variance(lifts) if n > 1 else 0.0
    std_dev = math.sqrt(variance)
    std_error = std_dev / math.sqrt(n)

    bootstrap_ci_low, bootstrap_ci_high = _compute_bootstrap_ci(
        lifts, config.bootstrap_iterations, config.random_seed
    )

    sign_p = _sign_test_two_sided(lifts)

    family_lifts: dict[str, dict[str, Any]] = {}
    family_wlt: dict[str, dict[str, int]] = {}
    for family in EXPECTED_FAMILIES:
        fam_control_scores = {
            s["task_id"]: s["score_total"]
            for s in control_scores
            if s.get("task_family") == family
        }
        fam_treatment_scores = {
            s["task_id"]: s["score_total"]
            for s in treatment_scores
            if s.get("task_family") == family
        }
        fam_common = set(fam_control_scores.keys()) & set(fam_treatment_scores.keys())
        fam_lifts = [fam_treatment_scores[t] - fam_control_scores[t] for t in fam_common]
        if fam_lifts:
            f_mean = statistics.mean(fam_lifts)
            f_wins = sum(1 for L in fam_lifts if L > 0)
            f_losses = sum(1 for L in fam_lifts if L < 0)
            f_ties = sum(1 for L in fam_lifts if L == 0)
        else:
            f_mean = 0.0
            f_wins = f_losses = f_ties = 0
        family_lifts[family] = {"mean_lift": f_mean}
        family_wlt[family] = {"wins": f_wins, "losses": f_losses, "ties": f_ties}

    outliers = _compute_outlier_sensitivity(lifts)

    comparison = {
        "control": control_name,
        "treatment": treatment_name,
        "n": n,
        "mean_lift": mean_lift,
        "median_lift": median_lift,
        "min_lift": min_lift,
        "max_lift": max_lift,
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "win_rate_excluding_ties": win_rate_excluding_ties,
        "non_negative_rate": non_negative_rate,
        "standard_deviation_lift": std_dev,
        "standard_error_lift": std_error,
        "bootstrap_ci_95_low": bootstrap_ci_low,
        "bootstrap_ci_95_high": bootstrap_ci_high,
        "bootstrap_iterations": config.bootstrap_iterations,
        "random_seed": config.random_seed,
        "sign_test_two_sided_p_value": sign_p,
        "family_mean_lifts": family_lifts,
        "family_win_loss_tie": family_wlt,
        "outlier_sensitivity": outliers,
    }

    comparison["signal"] = classify_signal(comparison)
    return comparison


def _sign_test_two_sided(lifts: list[float]) -> float | None:
    n_nonzero = sum(1 for L in lifts if L != 0)
    if n_nonzero < 3:
        return None
    n_pos = sum(1 for L in lifts if L > 0)
    n_neg = n_nonzero - n_pos
    k = min(n_pos, n_neg)
    if k == 0:
        return 0.0
    try:
        p = 0.0
        for i in range(k + 1):
            p += _binom_coeff(n_nonzero, i) * (0.5 ** n_nonzero)
        p *= 2.0
        return min(p, 1.0)
    except (OverflowError, ValueError):
        return None


def _binom_coeff(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    result = 1
    for i in range(1, k + 1):
        result = result * (n - k + i) // i
    return result


def _compute_outlier_sensitivity(lifts: list[float]) -> dict[str, Any]:
    if len(lifts) < 3:
        return {
            "mean_lift_without_best_task": None,
            "mean_lift_without_worst_task": None,
            "sign_preserved_without_best_task": None,
            "sign_preserved_without_worst_task": None,
        }
    original_mean = statistics.mean(lifts)
    sorted_vals = sorted(lifts)
    without_best = lifts.copy()
    without_best.remove(sorted_vals[-1])
    without_worst = lifts.copy()
    without_worst.remove(sorted_vals[0])
    mean_without_best = statistics.mean(without_best) if without_best else None
    mean_without_worst = statistics.mean(without_worst) if without_worst else None
    return {
        "mean_lift_without_best_task": mean_without_best,
        "mean_lift_without_worst_task": mean_without_worst,
        "sign_preserved_without_best_task": None if mean_without_best is None else (
            (mean_without_best > 0) == (original_mean > 0)
        ),
        "sign_preserved_without_worst_task": None if mean_without_worst is None else (
            (mean_without_worst > 0) == (original_mean > 0)
        ),
    }


def classify_signal(comparison: dict[str, Any]) -> str:
    ml = comparison.get("mean_lift", 0)
    med = comparison.get("median_lift", 0)
    wins = comparison.get("wins", 0)
    losses = comparison.get("losses", 0)
    ci_low = comparison.get("bootstrap_ci_95_low", 0)
    ci_high = comparison.get("bootstrap_ci_95_high", 0)
    nrr = comparison.get("non_negative_rate", 0)

    if ml < 0 and losses > wins and ci_high < 0:
        return "NEGATIVE_SIGNAL"

    if ml > 0 and med >= 0 and ci_low > 0 and wins > losses and nrr >= 0.70:
        return "STRONG_DIAGNOSTIC_SIGNAL"

    if ml > 0 and med >= 0 and wins >= losses and ci_high > 0 and nrr >= 0.60:
        return "MODERATE_DIAGNOSTIC_SIGNAL"

    return "WEAK_OR_INCONCLUSIVE_SIGNAL"


def compute_all_comparisons(
    scores: list[dict[str, Any]],
    config: RuntimeEvidenceGateConfig,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for s in scores:
        vn = s.get("variant_name", "")
        grouped.setdefault(vn, []).append(s)

    results: dict[str, dict[str, Any]] = {}
    for treatment, control in COMPARISON_SPECS:
        key = f"{treatment}_vs_{control}"
        control_scores = grouped.get(control, [])
        treatment_scores = grouped.get(treatment, [])
        if not control_scores or not treatment_scores:
            results[key] = {"error": "missing_variant_scores", "n": 0}
            continue
        results[key] = compute_comparison(
            control_scores, treatment_scores, control, treatment, config
        )

    return results
