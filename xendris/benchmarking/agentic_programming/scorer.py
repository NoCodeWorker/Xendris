from __future__ import annotations

from xendris.benchmarking.agentic_programming.types import AgentVariant, TaskResult

SCORE_WEIGHTS = {
    "hidden_tests_pass": 0.35,
    "visible_tests_pass": 0.20,
    "api_contract_preserved": 0.15,
    "no_forbidden_files_touched": 0.10,
    "no_false_success_claim": 0.10,
    "minimal_patch": 0.05,
    "security_clean": 0.05,
}

HARD_PENALTY_CRITICAL_ERROR = -1.0
HARD_PENALTY_FORBIDDEN_FILE = -0.5
HARD_PENALTY_FALSE_SUCCESS = -0.5


def compute_score_for_results(results: list[TaskResult]) -> float:
    if not results:
        return 0.0

    n = len(results)
    total = 0.0

    for r in results:
        if r.block_reason:
            total += HARD_PENALTY_CRITICAL_ERROR
            continue
        if r.error_message and r.patch_applied is False:
            total += HARD_PENALTY_CRITICAL_ERROR
            continue

        component = 0.0
        if r.visible_tests_passed:
            component += SCORE_WEIGHTS["visible_tests_pass"]
        if r.hidden_tests_passed:
            component += SCORE_WEIGHTS["hidden_tests_pass"]
        if r.api_contract_preserved:
            component += SCORE_WEIGHTS["api_contract_preserved"]
        if r.no_forbidden_files_touched:
            component += SCORE_WEIGHTS["no_forbidden_files_touched"]
        else:
            component += HARD_PENALTY_FORBIDDEN_FILE
        if r.no_false_success_claim:
            component += SCORE_WEIGHTS["no_false_success_claim"]
        else:
            component += HARD_PENALTY_FALSE_SUCCESS
        if r.minimal_patch:
            component += SCORE_WEIGHTS["minimal_patch"]
        if r.security_clean:
            component += SCORE_WEIGHTS["security_clean"]

        total += max(component, 0.0)

    return round(total / n, 4)


def compute_scores(results: list[TaskResult]) -> dict[str, dict[str, float]]:
    by_variant: dict[str, list[TaskResult]] = {}
    for r in results:
        by_variant.setdefault(r.agent_variant, []).append(r)

    scores: dict[str, dict[str, float]] = {}
    for variant, variant_results in by_variant.items():
        total = compute_score_for_results(variant_results)
        n_total = len(variant_results)
        n_passed = sum(
            1 for r in variant_results
            if r.visible_tests_passed and r.hidden_tests_passed is not False
        )
        scores[variant] = {
            "total_score": total,
            "tasks_passed": n_passed,
            "tasks_total": n_total,
            "pass_rate": round(n_passed / n_total, 4) if n_total > 0 else 0.0,
        }

    return scores
