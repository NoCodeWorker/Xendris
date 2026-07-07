from __future__ import annotations

import pytest

from xendris.benchmarking.agentic_programming.excellence_gate import (
    EXCELLENCE_THRESHOLD_BLOCKED,
    EXCELLENCE_THRESHOLD_READY,
    ExcellenceGateDecision,
    evaluate_excellence_gate,
)


class TestExcellenceGateConstants:
    def test_thresholds_ordered(self):
        assert EXCELLENCE_THRESHOLD_BLOCKED < EXCELLENCE_THRESHOLD_READY


class TestEvaluateExcellenceGate:
    def test_ready(self):
        scores = {
            "agent_a": {"total_score": 0.85, "pass_rate": 0.70},
            "agent_b": {"total_score": 0.90, "pass_rate": 0.80},
        }
        decisions = evaluate_excellence_gate(scores)
        assert decisions["agent_a"] == "READY_FOR_INTERPRETATION"
        assert decisions["agent_b"] == "READY_FOR_INTERPRETATION"

    def test_ready_at_threshold(self):
        scores = {
            "agent_a": {"total_score": 0.80, "pass_rate": 0.60},
        }
        decisions = evaluate_excellence_gate(scores)
        assert decisions["agent_a"] == "READY_FOR_INTERPRETATION"

    def test_blocked(self):
        scores = {
            "agent_a": {"total_score": 0.30, "pass_rate": 0.10},
            "agent_b": {"total_score": 0.50, "pass_rate": 0.15},
        }
        decisions = evaluate_excellence_gate(scores)
        assert decisions["agent_a"] == "BLOCKED_FOR_INTERPRETATION"
        assert decisions["agent_b"] == "BLOCKED_FOR_INTERPRETATION"

    def test_blocked_at_threshold(self):
        scores = {
            "agent_a": {"total_score": 0.39, "pass_rate": 0.19},
        }
        decisions = evaluate_excellence_gate(scores)
        assert decisions["agent_a"] == "BLOCKED_FOR_INTERPRETATION"

    def test_warnings(self):
        scores = {
            "agent_a": {"total_score": 0.60, "pass_rate": 0.40},
            "agent_b": {"total_score": 0.70, "pass_rate": 0.30},
        }
        decisions = evaluate_excellence_gate(scores)
        assert decisions["agent_a"] == "WARNINGS_PRESENT"
        assert decisions["agent_b"] == "WARNINGS_PRESENT"

    def test_empty_scores(self):
        assert evaluate_excellence_gate({}) == {}

    def test_mixed_decisions(self):
        scores = {
            "base_agent": {"total_score": 0.20, "pass_rate": 0.10},
            "xendris_agent": {"total_score": 0.85, "pass_rate": 0.70},
            "xendris_calibrated_agent": {"total_score": 0.65, "pass_rate": 0.50},
        }
        decisions = evaluate_excellence_gate(scores)
        assert decisions["base_agent"] == "BLOCKED_FOR_INTERPRETATION"
        assert decisions["xendris_agent"] == "READY_FOR_INTERPRETATION"
        assert decisions["xendris_calibrated_agent"] == "WARNINGS_PRESENT"
