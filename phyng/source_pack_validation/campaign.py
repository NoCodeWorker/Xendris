"""Campaign orchestration for PHI_GRADIENT source-pack validation v3.3."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.source_pack_validation.extract_validator import validate_source_pack_extracts, validated_extracts
from phyng.source_pack_validation.final_gate import build_blocked_gate, build_final_gate
from phyng.source_pack_validation.loader import load_seed_pack
from phyng.source_pack_validation.report import write_source_pack_validation_reports
from phyng.source_pack_validation.schemas import PhiGradientSourcePackValidationCampaignResult
from phyng.source_pack_validation.slot_scoring import score_slot_coverage


def run_phi_gradient_source_pack_validation_campaign(root: str | Path = ".") -> PhiGradientSourcePackValidationCampaignResult:
    repo_root = Path(root)
    manifest, extract_pack, blocked_reason = load_seed_pack(repo_root)
    if blocked_reason or manifest is None or extract_pack is None:
        gate = build_blocked_gate(blocked_reason or "Seed pack could not be loaded.")
    else:
        validations = validate_source_pack_extracts(manifest, extract_pack)
        validated = validated_extracts(validations)
        coverage = score_slot_coverage(manifest, extract_pack, validations)
        gate = build_final_gate(manifest, extract_pack, validations, validated, coverage)

    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3",
        input_type="SOURCE_PACK_VALIDATION_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_SOURCE_PACK_POPULATED",
        result_status=gate.status,
        payload={
            "validated_support_count": gate.validated_support_count,
            "manual_review_count": gate.manual_review_count,
            "negative_pressure_count": gate.negative_pressure.negative_pressure_count,
            "benchmark_comparable_count": gate.benchmark_scoring.benchmark_comparable_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3-{gate.status}",
        proposal_type="SOURCE_PACK_VALIDATION_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Source-pack extract validation completed under strict manual-review and benchmark gates.",
        proposed_change={
            "status": gate.status,
            "validated_support_count": gate.validated_support_count,
            "manual_review_count": gate.manual_review_count,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=["authorize physical claim", "validate Frontera C", "count manual-review extract as support"],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientSourcePackValidationCampaignResult(
        campaign_id="PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3",
        status=gate.status,
        gate_result=gate,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_source_pack_validation_reports(result, repo_root / "reports")
    return result
