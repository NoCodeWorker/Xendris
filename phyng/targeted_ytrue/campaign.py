"""Campaign orchestration for v5.7.3 targeted y_true extraction."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.targeted_ytrue.candidate_builder import build_candidates
from phyng.targeted_ytrue.dataset_assembly import assemble_dataset
from phyng.targeted_ytrue.dataset_quality import build_dataset_quality
from phyng.targeted_ytrue.deduplication import accept_with_dedup
from phyng.targeted_ytrue.loader import load_inputs
from phyng.targeted_ytrue.next_gate import build_next_gate
from phyng.targeted_ytrue.reports import write_reports
from phyng.targeted_ytrue.schemas import TargetedYTrueCampaignResult


def run_frontera_c_targeted_ytrue_extraction_campaign(root: str | Path = ".") -> TargetedYTrueCampaignResult:
    repo_root = Path(root)
    inputs = load_inputs(repo_root)
    candidates, rejected_qc, audit = build_candidates(inputs)
    accepted, rejected_dupes = accept_with_dedup(candidates, inputs["existing_ytrue"], audit)
    rejected = rejected_qc + rejected_dupes
    dataset = assemble_dataset(inputs["existing_ytrue"], accepted)
    human_review_count = sum(1 for item in candidates if "REQUIRES_HUMAN_FIGURE_REVIEW" in item.limitations)
    quality = build_dataset_quality(dataset, len(accepted), human_review_count)
    next_gate = build_next_gate(quality, len(rejected))
    result = TargetedYTrueCampaignResult(
        status=next_gate["final_status"],
        candidates=candidates,
        accepted=accepted,
        rejected=rejected,
        audit_trail=audit,
        expanded_dataset=dataset,
        dataset_quality=quality,
        next_gate_decision=next_gate,
    )
    result.output_paths = write_outputs(repo_root, result)
    result.report_paths = write_reports(result, repo_root / "reports")
    write_final_doc(repo_root, result)
    return result


def write_outputs(root: Path, result: TargetedYTrueCampaignResult) -> dict[str, str]:
    base = root / "data" / "frontera_c" / "targeted_ytrue"
    base.mkdir(parents=True, exist_ok=True)
    paths = {
        "candidates": base / "targeted_ytrue_candidates_v5_7_3.json",
        "accepted": base / "targeted_accepted_ytrue_v5_7_3.json",
        "rejected": base / "targeted_rejected_ytrue_v5_7_3.json",
        "audit": base / "targeted_ytrue_extraction_audit_trail_v5_7_3.json",
        "dataset": base / "visibility_decoherence_expanded_ytrue_dataset_v5_7_3.json",
        "quality": base / "visibility_decoherence_dataset_quality_v5_7_3.json",
        "next_gate": base / "v5_7_3_next_gate_decision.json",
    }
    payloads = {
        "candidates": {"candidate_count": len(result.candidates), "records": [item.model_dump() for item in result.candidates]},
        "accepted": {"accepted_ytrue_count": len(result.accepted), "records": [item.model_dump() for item in result.accepted]},
        "rejected": {"rejected_ytrue_count": len(result.rejected), "records": [item.model_dump() for item in result.rejected]},
        "audit": {"audit_record_count": len(result.audit_trail), "records": [item.model_dump() for item in result.audit_trail]},
        "dataset": result.expanded_dataset,
        "quality": result.dataset_quality.model_dump() if result.dataset_quality else {},
        "next_gate": result.next_gate_decision,
    }
    for key, path in paths.items():
        path.write_text(json.dumps(payloads[key], indent=2, sort_keys=True), encoding="utf-8")
    return {key: path.relative_to(root).as_posix() for key, path in paths.items()}


def write_final_doc(root: Path, result: TargetedYTrueCampaignResult) -> str:
    from phyng.core.report_contract import append_canonical_status_section, build_report_contract

    path = root / "docs" / "356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Phygn v5.7.3 - Targeted y_true Extraction Results",
        "",
        "Date: 2026-07-02",
        "",
        "Source prompt:",
        "",
        "```txt",
        "docs/355_PHYGN_CODEX_V5_7_3_TARGETED_YTRUE_EXTRACTION_PROMPT.md",
        "```",
        "",
        "## Completion Status",
        "",
        f"Final campaign status: `{result.status}`",
        f"Observed candidates evaluated: `{len(result.candidates)}`",
        f"New accepted y_true: `{len(result.accepted)}`",
        f"Rejected y_true candidates: `{len(result.rejected)}`",
        f"Total accepted y_true in expanded dataset: `{result.next_gate_decision.get('total_accepted_ytrue_count')}`",
        f"Independent source count: `{result.next_gate_decision.get('independent_source_count')}`",
        f"Benchmark readiness: `{result.next_gate_decision.get('benchmark_readiness')}`",
        f"Allowed next phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
        "",
        "No PredictiveGain was computed. No benchmark was built. No Frontera C or physical claim was upgraded. LOG_BOUNDARY was not reactivated.",
        "",
        "## Created Artifacts",
        "",
        *[f"- `{path_value}`" for path_value in result.output_paths.values()],
        *[f"- `{path_value}`" for path_value in result.report_paths.values()],
        "",
        "## Blocked Claims",
        "",
        "- Frontera C is validated.",
        "- LOG_BOUNDARY is reactivated.",
        "- Accepted y_true equals PredictiveGain.",
        "- Dataset expansion equals validation.",
        "- Physical claim.",
        "- Invariant confirmation.",
        "",
        "Final discipline:",
        "",
        "```txt",
        "A number without provenance is not truth.",
        "A figure without extracted values is not y_true.",
        "```",
    ]
    contract = build_report_contract(
        title="Targeted y_true Extraction Results v5.7.3",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="targeted_ytrue_extraction",
        reports_generated=list(result.report_paths.values()),
        next_actions=[result.next_gate_decision.get("allowed_next_phase") or "Resolve y_true extraction blockers."],
        discipline_note="No accepted y_true, no benchmark. No benchmark, no PredictiveGain.",
    )
    path.write_text(append_canonical_status_section("\n".join(lines) + "\n", contract), encoding="utf-8")
    return path.relative_to(root).as_posix()
