"""Campaign orchestration for PHI_GRADIENT v3.2 source-pack population."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.source_pack_population.report import write_source_pack_population_reports
from phyng.source_pack_population.schemas import PhiGradientSourcePackPopulationCampaignResult, PhiGradientSourcePackPopulationResult
from phyng.source_pack_population.seed_pack import write_seed_pack
from phyng.source_pack_population.validation import validate_seed_pack


def run_phi_gradient_source_pack_population_campaign(root: str | Path = ".") -> PhiGradientSourcePackPopulationCampaignResult:
    repo_root = Path(root)
    manifest, extract_pack, manifest_path, extract_pack_path = write_seed_pack(repo_root)
    validation = validate_seed_pack(manifest, extract_pack)
    status = validation.status
    population_result = PhiGradientSourcePackPopulationResult(
        status=status,
        canonical_status=normalize_status(status, domain="source_pack_population"),
        manifest=manifest,
        extract_pack=extract_pack,
        validation=validation,
        manifest_path=manifest_path,
        extract_pack_path=extract_pack_path,
        allowed_claims=["A reviewed source candidate pack was populated."],
        blocked_claims=[
            "The seed source pack proves PHI_GRADIENT.",
            "A seed extract is validated support.",
            "A candidate benchmark is benchmark support.",
            "PHI_GRADIENT has real source support.",
            "PHI_GRADIENT has benchmark support.",
            "PHI_GRADIENT is physically validated.",
            "PHI_GRADIENT validates Frontera C.",
        ],
        next_actions=[
            "Run v3.3 source-pack extract validation.",
            "Validate extracts with v2.9 rules before changing source-pressure status.",
            "Score slot coverage and negative pressure without relaxing physical claim gates.",
        ],
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2",
        input_type="SOURCE_PACK_POPULATION_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_REVIEWED_MANIFEST_CREATED",
        result_status=status,
        payload={
            "manifest_entry_count": validation.manifest_entry_count,
            "extract_count": validation.extract_count,
            "benchmark_candidate_count": validation.benchmark_candidate_count,
            "negative_candidate_count": validation.negative_candidate_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2-{status}",
        proposal_type="SOURCE_PACK_POPULATION_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Reviewed real source candidate pack populated; all extracts require manual validation.",
        proposed_change={
            "status": status,
            "manifest_entry_count": validation.manifest_entry_count,
            "extract_count": validation.extract_count,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=[
            "authorize physical claim",
            "validate Frontera C",
            "count seed source as support",
            "count seed benchmark as benchmark support",
        ],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientSourcePackPopulationCampaignResult(
        campaign_id="PHI-GRADIENT-REVIEWED-REAL-SOURCE-PACK-v3_2",
        status=status,
        population_result=population_result,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_source_pack_population_reports(result, repo_root / "reports")
    return result
