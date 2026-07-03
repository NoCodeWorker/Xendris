"""Phygn v2.4 closed-loop meta-improvement campaign."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.guards import run_loop_guards
from phyng.closed_loop.meta_loop import propose_meta_improvement
from phyng.closed_loop.report import write_closed_loop_reports
from phyng.closed_loop.schemas import CandidateLoopInput, ClosedLoopCampaignResult, MetaImprovementResult, MetaObservation
from phyng.closed_loop.shadow_mode import run_shadow_mode
from phyng.closed_loop.versioning import create_versioned_update_record
from phyng.core.compatibility import normalize_status


def run_closed_loop_meta_improvement_campaign(root: str | Path = ".") -> ClosedLoopCampaignResult:
    repo_root = Path(root)
    candidate_loop = run_candidate_learning_loop(
        CandidateLoopInput(
            loop_id="LOOP-V2-4-LOG-BOUNDARY",
            input_type="SYNTHETIC_BENCHMARK_RESULT",
            domain="physical_candidate",
            candidate_id="HEUR-PHY-003",
            candidate_family="LOG_BOUNDARY",
            previous_status="HEURISTIC_TEST_DESIGN_READY",
            result_status="SYNTHETIC_BENCHMARK_DESIGNED",
        )
    )
    observation = MetaObservation(
        observation_id="META-OBS-V2-4-001",
        source="v2.3 benchmark design report",
        observation_type="REPORT_COMPLETENESS",
        summary="Closed-loop reports need blocked claims and rollback records.",
        evidence={"change_type": "REPORT_TEMPLATE_CHANGE", "affected_modules": ["phyng.closed_loop.report"]},
    )
    proposal = propose_meta_improvement(observation)
    shadow = run_shadow_mode(
        proposal,
        sample_cases=[
            {
                "current_output": {"canonical_permission": "TEST_DESIGN_ALLOWED", "blocked_reasons": ["MISSING_SOURCE_SUPPORT"]},
                "shadow_output": {"canonical_permission": "TEST_DESIGN_ALLOWED", "blocked_reasons": ["MISSING_SOURCE_SUPPORT"]},
            }
        ],
    )
    guards = run_loop_guards(
        proposal,
        source_status="HEURISTIC_ONLY",
        target_permission="TEST_DESIGN_ALLOWED",
        has_source_or_benchmark=False,
        synthetic_to_physical=False,
        shadow_mode_ran=True,
        report_has_blocked_claims=True,
        audit_event_present=True,
    )
    meta_result = MetaImprovementResult(
        observation=observation,
        proposal=proposal,
        shadow_result=shadow,
        guard_results=guards,
        canonical_status=proposal.canonical_status,
    )
    versioned = create_versioned_update_record(
        proposal,
        previous_config={"report_template": "v2.3"},
        new_config={"report_template": "v2.4_closed_loop_blocked_claims"},
        reason="Ensure loop reports include blocked claims/actions.",
        tests_required=["pytest -q", "tests/test_closed_loop_meta_improvement_campaign_v2_4.py"],
        rollback_path="Revert to previous report template config.",
        impact_summary="Low-risk report template improvement; no gate behavior change.",
    )
    result = ClosedLoopCampaignResult(
        campaign_id="CLOSED-LOOP-META-IMPROVEMENT-v2_4",
        status="META_CHANGE_APPROVED_LOW_RISK",
        candidate_loop_result=candidate_loop,
        meta_improvement_result=meta_result,
        shadow_mode_result=shadow,
        guard_results=guards,
        versioned_record=versioned,
    )
    result.report_paths = write_closed_loop_reports(result, repo_root / "reports")
    return result
