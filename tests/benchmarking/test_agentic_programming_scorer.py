from __future__ import annotations

import pytest

from xendris.benchmarking.agentic_programming.scorer import (
    SCORE_WEIGHTS,
    compute_score_for_results,
    compute_scores,
)
from xendris.benchmarking.agentic_programming.types import TaskResult


def _make_result(
    variant: str = "base_agent",
    visible_ok: bool = True,
    hidden_ok: bool = True,
    api_ok: bool = True,
    forbidden_ok: bool = True,
    false_success: bool = True,
    minimal: bool = True,
    security_ok: bool = True,
    error: str | None = None,
    patch_applied: bool = True,
) -> TaskResult:
    return TaskResult(
        sample_id="AP-TEST",
        agent_variant=variant,
        patch_applied=patch_applied,
        visible_tests_passed=visible_ok,
        hidden_tests_passed=hidden_ok,
        api_contract_preserved=api_ok,
        no_forbidden_files_touched=forbidden_ok,
        no_false_success_claim=false_success,
        minimal_patch=minimal,
        security_clean=security_ok,
        iterations_used=1,
        error_message=error,
        patch_content="",
    )


class TestScoreWeights:
    def test_weights_sum_to_one(self):
        total = sum(SCORE_WEIGHTS.values())
        assert abs(total - 1.0) < 0.001, f"Weights sum to {total}, expected 1.0"


class TestComputeScoreForResults:
    def test_all_good(self):
        result = _make_result()
        score = compute_score_for_results([result])
        expected = sum(SCORE_WEIGHTS.values())
        assert score == pytest.approx(expected, rel=0.01)

    def test_all_bad(self):
        result = _make_result(
            visible_ok=False, hidden_ok=False, api_ok=False,
            forbidden_ok=False, false_success=False, minimal=False, security_ok=False,
        )
        score = compute_score_for_results([result])
        assert score >= 0.0

    def test_critical_error_penalty(self):
        result = _make_result(error="crash", patch_applied=False)
        score = compute_score_for_results([result])
        assert score < 0

    def test_forbidden_file_penalty(self):
        result = _make_result(forbidden_ok=False, false_success=True)
        score = compute_score_for_results([result])
        visible_weight = SCORE_WEIGHTS["visible_tests_pass"]
        hidden_weight = SCORE_WEIGHTS["hidden_tests_pass"]
        api_weight = SCORE_WEIGHTS["api_contract_preserved"]
        false_weight = SCORE_WEIGHTS["no_false_success_claim"]
        minimal_weight = SCORE_WEIGHTS["minimal_patch"]
        security_weight = SCORE_WEIGHTS["security_clean"]
        forbidden_penalty = -0.5
        expected_base = visible_weight + hidden_weight + api_weight + false_weight + minimal_weight + security_weight
        expected = max(expected_base + forbidden_penalty, 0.0)
        assert score == pytest.approx(expected, rel=0.01)

    def test_empty_results_returns_zero(self):
        assert compute_score_for_results([]) == 0.0

    def test_average_multiple_results(self):
        r1 = _make_result()
        r2 = _make_result(visible_ok=False, hidden_ok=False)
        score = compute_score_for_results([r1, r2])
        full = sum(SCORE_WEIGHTS.values())
        partial = SCORE_WEIGHTS["api_contract_preserved"] + SCORE_WEIGHTS["no_forbidden_files_touched"] + SCORE_WEIGHTS["no_false_success_claim"] + SCORE_WEIGHTS["minimal_patch"] + SCORE_WEIGHTS["security_clean"]
        expected = (full + partial) / 2.0
        assert score == pytest.approx(expected, rel=0.01)


class TestComputeScores:
    def test_groups_by_variant(self):
        results = [
            _make_result(variant="base_agent"),
            _make_result(variant="base_agent"),
            _make_result(variant="xendris_agent"),
        ]
        scores = compute_scores(results)
        assert "base_agent" in scores
        assert "xendris_agent" in scores
        assert scores["base_agent"]["tasks_total"] == 2
        assert scores["xendris_agent"]["tasks_total"] == 1

    def test_empty_results(self):
        assert compute_scores([]) == {}

    def test_pass_rate_calculation(self):
        results = [
            _make_result(variant="agent_a", visible_ok=True, hidden_ok=True),
            _make_result(variant="agent_a", visible_ok=True, hidden_ok=True),
            _make_result(variant="agent_a", visible_ok=True, hidden_ok=True),
            _make_result(variant="agent_a", visible_ok=True, hidden_ok=False),
        ]
        scores = compute_scores(results)
        assert scores["agent_a"]["tasks_passed"] == 3
        assert scores["agent_a"]["tasks_total"] == 4
        assert scores["agent_a"]["pass_rate"] == 0.75
