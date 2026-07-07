from __future__ import annotations

import json
import os

import pytest

SUMMARY_PATH = os.path.join(
    "runs", "agentic_programming_v0_1_dry_run", "summary.json"
)
REPORT_PATH = os.path.join(
    "runs", "agentic_programming_v0_1_dry_run", "report.md"
)


@pytest.fixture
def summary() -> dict:
    if not os.path.isfile(SUMMARY_PATH):
        pytest.skip(f"Summary not found: {SUMMARY_PATH}")
    with open(SUMMARY_PATH, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def report_text() -> str:
    if not os.path.isfile(REPORT_PATH):
        pytest.skip(f"Report not found: {REPORT_PATH}")
    with open(REPORT_PATH, encoding="utf-8") as f:
        return f.read()


class TestCanonicalSummarySchema:
    def test_execution_mode_present(self, summary: dict):
        assert "execution_mode" in summary

    def test_execution_mode_is_dry_run(self, summary: dict):
        assert summary["execution_mode"] == "dry-run"

    def test_provider_mode_present(self, summary: dict):
        assert "provider_mode" in summary

    def test_provider_mode_is_mock(self, summary: dict):
        assert summary["provider_mode"] == "mock"

    def test_variants_listed(self, summary: dict):
        variants = summary.get("variants", [])
        assert "base_agent" in variants
        assert "xendris_agent" in variants
        assert "xendris_calibrated_agent" in variants

    def test_dataset_size_is_20(self, summary: dict):
        assert summary.get("dataset_size") == 20

    def test_total_results_60(self, summary: dict):
        assert summary.get("total_results") == 60

    def test_limitations_present(self, summary: dict):
        limitations = summary.get("limitations", [])
        assert len(limitations) > 0

    def test_no_real_provider_warning_present(self, summary: dict):
        warning = summary.get("no_real_provider_performance_warning", "")
        assert len(warning) > 0
        assert "no real provider" in warning.lower()

    def test_no_universal_superiority_warning_present(self, summary: dict):
        warning = summary.get("no_universal_superiority_warning", "")
        assert len(warning) > 0
        assert "universal superiority" in warning.lower()

    def test_variants_not_empty(self, summary: dict):
        assert len(summary.get("variants", [])) > 0

    def test_dataset_name_present(self, summary: dict):
        assert "dataset_name" in summary

    def test_scoring_formula_present(self, summary: dict):
        assert "scoring_formula" in summary

    def test_excellence_gate_decisions_present(self, summary: dict):
        assert "excellence_gate_decisions" in summary

    def test_commercial_metrics_present(self, summary: dict):
        assert "commercial_metrics" in summary

    def test_category_breakdown_present(self, summary: dict):
        assert "category_breakdown" in summary

    def test_scores_by_variant_present(self, summary: dict):
        assert "scores_by_variant" in summary

    def test_benchmark_name_present(self, summary: dict):
        assert summary.get("benchmark_name") == "Agentic Programming Reliability"


class TestCanonicalReport:
    def test_report_contains_execution_mode(self, report_text: str):
        assert "dry-run" in report_text

    def test_report_contains_provider_mode(self, report_text: str):
        assert "mock" in report_text

    def test_report_contains_limitations(self, report_text: str):
        assert "Limitations" in report_text

    def test_report_contains_no_real_provider_warning(self, report_text: str):
        assert "No Real Provider" in report_text

    def test_report_contains_no_superiority_warning(self, report_text: str):
        assert "No Superiority Claim" in report_text or "superiority" in report_text.lower()

    def test_report_contains_excellence_gate(self, report_text: str):
        assert "Excellence Gate" in report_text

    def test_report_contains_scores_table(self, report_text: str):
        assert "Total Score" in report_text
        assert "Pass Rate" in report_text


class TestEvidenceInterpretation:
    def test_evidence_interpretation_present(self, summary: dict):
        assert "evidence_interpretation" in summary

    def test_evidence_not_real_provider(self, summary: dict):
        interpretation = summary.get("evidence_interpretation", "")
        assert "dry-run" in interpretation.lower()
        assert "not admissible" in interpretation.lower() or "not evidence" in interpretation.lower()

    def test_gate_blocks_on_dry_run(self, summary: dict):
        decisions = summary.get("excellence_gate_decisions", {})
        for variant, decision in decisions.items():
            assert decision == "BLOCKED_FOR_INTERPRETATION", (
                f"{variant} should be BLOCKED in dry-run, got {decision}"
            )

    def test_summary_declares_mock_provider(self, summary: dict):
        assert summary.get("provider_mode") == "mock"
