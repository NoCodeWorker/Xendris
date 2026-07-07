from __future__ import annotations

import json
import os

import pytest

from xendris.benchmarking.agentic_programming.types import AgentVariant
from xendris.benchmarking.agentic_programming.deterministic_agents import (
    bad_agent,
    oracle_agent,
    partial_agent,
)

CONTROLS_PATH = os.path.join(
    "runs", "agentic_programming_v0_1_deterministic_controls", "summary.json"
)
DRY_RUN_PATH = os.path.join(
    "runs", "agentic_programming_v0_1_dry_run", "summary.json"
)


@pytest.fixture
def controls_summary() -> dict:
    if not os.path.isfile(CONTROLS_PATH):
        pytest.skip(f"Controls summary not found: {CONTROLS_PATH}")
    with open(CONTROLS_PATH, encoding="utf-8") as f:
        return json.load(f)


class TestDeterministicVariantsExist:
    def test_oracle_agent_variant_exists(self):
        assert AgentVariant.ORACLE_AGENT is not None
        assert AgentVariant.ORACLE_AGENT.value == "oracle_agent"

    def test_partial_agent_variant_exists(self):
        assert AgentVariant.PARTIAL_AGENT is not None
        assert AgentVariant.PARTIAL_AGENT.value == "partial_agent"

    def test_bad_agent_variant_exists(self):
        assert AgentVariant.BAD_AGENT is not None
        assert AgentVariant.BAD_AGENT.value == "bad_agent"

    def test_deterministic_classification(self):
        assert AgentVariant.is_deterministic(AgentVariant.ORACLE_AGENT)
        assert AgentVariant.is_deterministic(AgentVariant.PARTIAL_AGENT)
        assert AgentVariant.is_deterministic(AgentVariant.BAD_AGENT)
        assert not AgentVariant.is_deterministic(AgentVariant.BASE_AGENT)


class TestDeterministicFunctions:
    def test_oracle_agent_requires_working_dir(self):
        result, error = oracle_agent()
        assert error is not None
        assert "working_dir" in error

    def test_partial_agent_requires_working_dir(self):
        result, error = partial_agent()
        assert error is not None
        assert "working_dir" in error

    def test_bad_agent_requires_working_dir(self):
        result, error = bad_agent()
        assert error is not None
        assert "working_dir" in error


class TestScoringSeparation:
    def test_oracle_scores_above_bad(self, controls_summary: dict):
        scores = controls_summary.get("scores_by_variant", {})
        oracle_score = scores.get("oracle_agent", {}).get("total_score", 0)
        bad_score = scores.get("bad_agent", {}).get("total_score", 0)
        assert oracle_score > bad_score, (
            f"oracle_agent ({oracle_score}) should score above bad_agent ({bad_score})"
        )

    def test_oracle_scores_above_partial(self, controls_summary: dict):
        scores = controls_summary.get("scores_by_variant", {})
        oracle_score = scores.get("oracle_agent", {}).get("total_score", 0)
        partial_score = scores.get("partial_agent", {}).get("total_score", 0)
        assert oracle_score >= partial_score, (
            f"oracle_agent ({oracle_score}) should score at or above partial_agent ({partial_score})"
        )

    def test_bad_agent_has_low_score(self, controls_summary: dict):
        scores = controls_summary.get("scores_by_variant", {})
        bad_score = scores.get("bad_agent", {}).get("total_score", 0)
        assert bad_score < 0.3, (
            f"bad_agent score ({bad_score}) should be low"
        )

    def test_oracle_has_high_pass_rate(self, controls_summary: dict):
        scores = controls_summary.get("scores_by_variant", {})
        oracle_pr = scores.get("oracle_agent", {}).get("pass_rate", 0)
        assert oracle_pr >= 0.5, (
            f"oracle_agent pass_rate ({oracle_pr}) should be at least 0.5"
        )

    def test_bad_has_low_pass_rate(self, controls_summary: dict):
        scores = controls_summary.get("scores_by_variant", {})
        bad_pr = scores.get("bad_agent", {}).get("pass_rate", 0)
        assert bad_pr <= 0.5, (
            f"bad_agent pass_rate ({bad_pr}) should be at most 0.5"
        )


class TestPenaltiesDetected:
    def test_bad_agent_triggers_forbidden_file_penalty(self, controls_summary: dict):
        decisions = controls_summary.get("excellence_gate_decisions", {})
        assert "bad_agent" in decisions
        assert decisions["bad_agent"] == "BLOCKED_FOR_INTERPRETATION"

    def test_bad_agent_has_zero_or_low_score(self, controls_summary: dict):
        scores = controls_summary.get("scores_by_variant", {})
        bad_score = scores.get("bad_agent", {}).get("total_score", 1)
        assert bad_score < 0.3


class TestEvidenceScoping:
    def test_controls_are_not_model_evidence(self, controls_summary: dict):
        warning = controls_summary.get("no_real_provider_performance_warning", "")
        interpretation = controls_summary.get("evidence_interpretation", "")
        combined = (warning + " " + interpretation).lower()
        assert "not evidence" in combined or "not admissible" in combined

    def test_no_real_provider_warning_present(self, controls_summary: dict):
        warning = controls_summary.get("no_real_provider_performance_warning", "")
        assert len(warning) > 0

    def test_no_universal_superiority_warning_present(self, controls_summary: dict):
        warning = controls_summary.get("no_universal_superiority_warning", "")
        assert len(warning) > 0

    def test_controls_use_separate_output_path(self):
        assert os.path.isfile(CONTROLS_PATH), f"Controls output missing: {CONTROLS_PATH}"


class TestHistoricalDryRunUnchanged:
    def test_historical_dry_run_still_exists(self):
        assert os.path.isfile(DRY_RUN_PATH), f"Historical dry-run missing: {DRY_RUN_PATH}"

    def test_historical_dry_run_still_blocked(self):
        with open(DRY_RUN_PATH, encoding="utf-8") as f:
            summary = json.load(f)
        decisions = summary.get("excellence_gate_decisions", {})
        for variant, decision in decisions.items():
            assert decision == "BLOCKED_FOR_INTERPRETATION"


class TestControlsSummarySchema:
    def test_variants_in_controls(self, controls_summary: dict):
        variants = controls_summary.get("variants", [])
        assert "oracle_agent" in variants
        assert "partial_agent" in variants
        assert "bad_agent" in variants

    def test_execution_mode_present(self, controls_summary: dict):
        assert "execution_mode" in controls_summary

    def test_scores_by_variant_present(self, controls_summary: dict):
        assert "scores_by_variant" in controls_summary
        assert "oracle_agent" in controls_summary["scores_by_variant"]

    def test_commercial_metrics_present(self, controls_summary: dict):
        assert "commercial_metrics" in controls_summary
