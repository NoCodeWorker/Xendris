"""Test hardening plan from v4.4.1 status-only audit."""

from __future__ import annotations

import re

from phyng.audit_remediation.schemas import TestHardeningPlanItem, TestHardeningResults


def build_test_hardening_plan(test_logic_payload: dict) -> list[TestHardeningPlanItem]:
    items: list[TestHardeningPlanItem] = []
    for issue in test_logic_payload.get("issues", []):
        test_name = _extract_test_name(issue.get("message", ""), issue.get("evidence", "unknown_test"))
        priority = _priority(issue.get("path", ""))
        items.append(
            TestHardeningPlanItem(
                test_file=issue.get("path", ""),
                test_name=test_name,
                issue_type=issue.get("category", "STATUS_ONLY_TEST"),
                current_weakness=issue.get("message", "Status-only assertion."),
                required_negative_fixture=_fixture_for_path(issue.get("path", "")),
                required_assertion_upgrade="Assert blocked claims, permission propagation, or failure under a negative fixture.",
                priority=priority,
                remediation_status="PLANNED_RESIDUAL_HARDENING",
            )
        )
    return items


def build_test_hardening_results(plan: list[TestHardeningPlanItem]) -> TestHardeningResults:
    fixture_classes = {item.required_negative_fixture for item in plan}
    return TestHardeningResults(
        initial_status_only_count=len(plan),
        hardened_test_count=0,
        remaining_status_only_count=len(plan),
        negative_fixture_count_added=7,
        contradiction_fixture_count_added=1 if "claim_leakage_fixture" in fixture_classes else 0,
        debt_bypass_fixture_count_added=1 if "slot4_bypass_fixture" in fixture_classes else 0,
        metric_misuse_fixture_count_added=1 if "benchmark_score_as_predictive_gain_fixture" in fixture_classes else 0,
        recommendations=[
            "Prioritize high-priority pipeline tests before v4.5.",
            "Every status assertion should include at least one boundary-protection assertion.",
            "Keep v4.4.1 negative fixtures as active regression tests.",
        ],
    )


def status_only_tests_are_classified(plan: list[TestHardeningPlanItem]) -> bool:
    return all(item.issue_type and item.required_negative_fixture and item.remediation_status for item in plan)


def _extract_test_name(message: str, fallback: str) -> str:
    match = re.search(r"`([^`]+)`", message)
    return match.group(1) if match else fallback


def _priority(path: str) -> str:
    lowered = path.lower()
    if any(marker in lowered for marker in ("source_pressure", "scientific_debt", "model_comparison", "ytrue", "manual_data", "full_suite")):
        return "HIGH"
    if any(marker in lowered for marker in ("status", "claim", "benchmark", "observable")):
        return "MEDIUM"
    return "LOW"


def _fixture_for_path(path: str) -> str:
    lowered = path.lower()
    if "predictive" in lowered or "model_comparison" in lowered:
        return "predictive_gain_without_ytrue_fixture"
    if "slot4" in lowered or "scientific_debt" in lowered:
        return "slot4_bypass_fixture"
    if "benchmark" in lowered:
        return "benchmark_score_as_predictive_gain_fixture"
    if "ytrue" in lowered or "manual_data" in lowered:
        return "ytrue_without_provenance_fixture"
    if "source_pressure" in lowered:
        return "source_pressure_without_extract_fixture"
    if "negative" in lowered:
        return "negative_control_no_claim_impact_fixture"
    return "claim_leakage_fixture"
