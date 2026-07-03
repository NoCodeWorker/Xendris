"""Campaign orchestration for PHI_GRADIENT local source text registry v3.6."""

from __future__ import annotations

from pathlib import Path

from phyng.closed_loop.candidate_loop import run_candidate_learning_loop
from phyng.closed_loop.schemas import CandidateLoopInput, CandidateUpdateProposal
from phyng.core.compatibility import normalize_status
from phyng.local_source_text.report import write_local_source_text_reports
from phyng.local_source_text.schemas import (
    LocalSourceTextRegistry,
    PhiGradientLocalSourceTextRegistryCampaignResult,
    PhiGradientLocalSourceTextRegistryResult,
    SourceFileManifest,
    SourceHashManifest,
)
from phyng.local_source_text.source_registry import build_local_source_text_registry, write_local_source_text_outputs
from phyng.local_source_text.availability import build_source_availability_manifest
from phyng.local_source_text.manual_download_tasks import build_manual_download_tasks


def run_phi_gradient_local_source_text_registry_campaign(
    root: str | Path = ".",
) -> PhiGradientLocalSourceTextRegistryCampaignResult:
    repo_root = Path(root)
    specs, registry, file_manifest, hash_manifest, availability, download_tasks, blocked_reason = build_local_source_text_registry(repo_root)
    output_paths = {}
    if blocked_reason is None:
        output_paths = write_local_source_text_outputs(repo_root, registry, file_manifest, hash_manifest, availability, download_tasks)
    else:
        registry.registry_status = "PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED"
    status = registry.registry_status
    registry_result = PhiGradientLocalSourceTextRegistryResult(
        status=status,
        canonical_status=normalize_status(status, domain="local_source_text"),
        priority_sources=specs,
        registry=registry,
        file_manifest=file_manifest,
        hash_manifest=hash_manifest,
        availability_manifest=availability,
        download_tasks=download_tasks,
        available_file_count=registry.available_count,
        missing_file_count=registry.missing_count,
        hash_count=registry.hash_count,
        unsupported_file_count=registry.unsupported_file_count,
        manual_download_task_count=len(download_tasks.tasks),
        blocked_reason=blocked_reason,
        output_paths=output_paths,
        allowed_claims=_allowed_claims(status),
        blocked_claims=_blocked_claims(),
        next_actions=_next_actions(status),
    )
    loop_input = CandidateLoopInput(
        loop_id="PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6",
        input_type="LOCAL_SOURCE_TEXT_REGISTRY_RESULT",
        domain="physical_candidate",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        previous_status="PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT",
        result_status=status,
        payload={
            "available_file_count": registry_result.available_file_count,
            "missing_file_count": registry_result.missing_file_count,
            "hash_count": registry_result.hash_count,
            "manual_download_task_count": registry_result.manual_download_task_count,
        },
    )
    loop_result = run_candidate_learning_loop(loop_input)
    proposal = CandidateUpdateProposal(
        proposal_id=f"PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6-{status}",
        proposal_type="LOCAL_SOURCE_TEXT_REGISTRY_FEEDBACK",
        candidate_id="HEUR-PHY-003",
        candidate_family="PHI_GRADIENT",
        description="Local source text registry executed; file hashes only prepare exact extraction and do not create source support.",
        proposed_change={
            "status": status,
            "available_file_count": registry_result.available_file_count,
            "missing_file_count": registry_result.missing_file_count,
            "hash_count": registry_result.hash_count,
        },
        risk_level="LOW",
        requires_shadow_mode=False,
        requires_human_review=True,
        forbidden_actions=[
            "authorize physical claim",
            "treat PDF hash as source support",
            "treat registered file as benchmark support",
        ],
        canonical_status=normalize_status("LOOP_UPDATE_PROPOSED", domain="closed_loop"),
    )
    result = PhiGradientLocalSourceTextRegistryCampaignResult(
        campaign_id="PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6",
        status=status,
        registry_result=registry_result,
        loop_input=loop_input,
        loop_result=loop_result,
        update_proposals=[proposal],
    )
    result.report_paths = write_local_source_text_reports(result, repo_root / "reports")
    return result


def _allowed_claims(status: str) -> list[str]:
    claims = [
        "Local source registry was created.",
        "Priority files were checked.",
    ]
    if status in {"PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL", "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY"}:
        claims.append("Available files were hashed.")
    if status != "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY":
        claims.append("Missing files were converted into manual download tasks.")
    return claims


def _blocked_claims() -> list[str]:
    return [
        "A registered PDF validates PHI_GRADIENT.",
        "A source hash is source support.",
        "A local file is benchmark support.",
        "PHI_GRADIENT is physically validated.",
        "Frontera C is validated.",
    ]


def _next_actions(status: str) -> list[str]:
    if status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING":
        return ["Download the five priority source files into data/real_sources/pdfs/, then rerun v3.6."]
    if status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL":
        return ["Download remaining missing priority source files and run v3.7 only on hashed available files if partial extraction is acceptable."]
    if status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY":
        return ["Run v3.7 exact PDF/text extraction against hashed local source files."]
    if status == "PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED":
        return ["Restore the v3.2 reviewed seed manifest before rerunning the registry."]
    return ["Review registry completeness before exact extraction."]
