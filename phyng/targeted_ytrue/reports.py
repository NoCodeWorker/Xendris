"""Markdown reports for v5.7.3 targeted y_true extraction."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.targeted_ytrue.schemas import TargetedYTrueCampaignResult


def write_reports(result: TargetedYTrueCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "frontera_c" / "targeted_ytrue"
    campaign_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaign_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "candidates": report_dir / "targeted_ytrue_candidates_v5_7_3.md",
        "accepted": report_dir / "targeted_accepted_ytrue_v5_7_3.md",
        "rejected": report_dir / "targeted_rejected_ytrue_v5_7_3.md",
        "audit": report_dir / "targeted_ytrue_extraction_audit_trail_v5_7_3.md",
        "dataset": report_dir / "visibility_decoherence_expanded_ytrue_dataset_v5_7_3.md",
        "quality": report_dir / "visibility_decoherence_dataset_quality_v5_7_3.md",
        "next_gate": report_dir / "v5_7_3_next_gate_decision.md",
        "campaign": campaign_dir / "FRONTERA-C-TARGETED-YTRUE-EXTRACTION-v5_7_3.md",
    }
    paths["candidates"].write_text(_canonical(_render_candidates(result), result), encoding="utf-8")
    paths["accepted"].write_text(_canonical(_render_accepted(result), result), encoding="utf-8")
    paths["rejected"].write_text(_canonical(_render_rejected(result), result), encoding="utf-8")
    paths["audit"].write_text(_canonical(_render_audit(result), result), encoding="utf-8")
    paths["dataset"].write_text(_canonical(_render_dataset(result), result), encoding="utf-8")
    paths["quality"].write_text(_canonical(_render_quality(result), result), encoding="utf-8")
    paths["next_gate"].write_text(_canonical(_render_next_gate(result), result), encoding="utf-8")
    paths["campaign"].write_text(_canonical(_render_campaign(result), result), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def _canonical(markdown: str, result: TargetedYTrueCampaignResult) -> str:
    contract = build_report_contract(
        title="Targeted y_true Extraction v5.7.3",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="targeted_ytrue_extraction",
        next_actions=[result.next_gate_decision.get("allowed_next_phase") or "Resolve y_true blockers."],
        discipline_note="Accepted y_true expands the field. It does not yet judge the theory.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_candidates(result: TargetedYTrueCampaignResult) -> str:
    lines = ["# Targeted y_true Candidates v5.7.3", "", f"- candidate_count: `{len(result.candidates)}`", ""]
    for item in result.candidates:
        lines.append(f"- `{item.ytrue_candidate_id}`: source=`{item.source_id}`, value=`{item.numeric_value}`, qc=`{item.qc_status}`")
    return "\n".join(lines) + "\n"


def _render_accepted(result: TargetedYTrueCampaignResult) -> str:
    lines = ["# Targeted Accepted y_true v5.7.3", "", f"- accepted_count: `{len(result.accepted)}`", ""]
    for item in result.accepted:
        lines.append(f"- `{item.y_true_id}`: source=`{item.source_id}`, value=`{item.value_numeric}`, conditions=`{item.conditions}`")
    return "\n".join(lines) + "\n"


def _render_rejected(result: TargetedYTrueCampaignResult) -> str:
    lines = ["# Targeted Rejected y_true v5.7.3", "", f"- rejected_count: `{len(result.rejected)}`", ""]
    for item in result.rejected:
        lines.append(f"- `{item.ytrue_candidate_id}`: source=`{item.source_id}`, reason=`{item.rejection_reason}`")
    return "\n".join(lines) + "\n"


def _render_audit(result: TargetedYTrueCampaignResult) -> str:
    lines = ["# Targeted y_true Extraction Audit Trail v5.7.3", "", f"- audit_record_count: `{len(result.audit_trail)}`", ""]
    for item in result.audit_trail:
        lines.append(f"- `{item.candidate_id}`: decision=`{item.decision}`, reason=`{item.decision_reason}`")
    return "\n".join(lines) + "\n"


def _render_dataset(result: TargetedYTrueCampaignResult) -> str:
    return "\n".join(
        [
            "# Visibility/Decoherence Expanded y_true Dataset v5.7.3",
            "",
            f"- accepted_ytrue_count: `{result.expanded_dataset.get('accepted_ytrue_count')}`",
            f"- new_accepted_ytrue_count: `{result.expanded_dataset.get('new_accepted_ytrue_count')}`",
            f"- source_count: `{result.expanded_dataset.get('source_count')}`",
            f"- predictive_gain_computed: `{result.expanded_dataset.get('predictive_gain_computed')}`",
        ]
    ) + "\n"


def _render_quality(result: TargetedYTrueCampaignResult) -> str:
    quality = result.dataset_quality
    return "\n".join(
        [
            "# Visibility/Decoherence Dataset Quality v5.7.3",
            "",
            f"- total_accepted_ytrue_count: `{quality.total_accepted_ytrue_count if quality else 0}`",
            f"- new_accepted_ytrue_count: `{quality.new_accepted_ytrue_count if quality else 0}`",
            f"- independent_source_count: `{quality.independent_source_count if quality else 0}`",
            f"- benchmark_readiness: `{quality.benchmark_readiness if quality else None}`",
        ]
    ) + "\n"


def _render_next_gate(result: TargetedYTrueCampaignResult) -> str:
    return "\n".join(
        [
            "# v5.7.3 Next Gate Decision",
            "",
            f"- final_status: `{result.next_gate_decision.get('final_status')}`",
            f"- new_accepted_ytrue_count: `{result.next_gate_decision.get('new_accepted_ytrue_count')}`",
            f"- total_accepted_ytrue_count: `{result.next_gate_decision.get('total_accepted_ytrue_count')}`",
            f"- independent_source_count: `{result.next_gate_decision.get('independent_source_count')}`",
            f"- allowed_next_phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
        ]
    ) + "\n"


def _render_campaign(result: TargetedYTrueCampaignResult) -> str:
    return "\n".join(
        [
            "# Campaign Report - FRONTERA-C-TARGETED-YTRUE-EXTRACTION-v5_7_3",
            "",
            f"- status: `{result.status}`",
            f"- candidates_evaluated: `{len(result.candidates)}`",
            f"- new_accepted_ytrue_count: `{len(result.accepted)}`",
            f"- rejected_ytrue_count: `{len(result.rejected)}`",
            f"- total_accepted_ytrue_count: `{result.next_gate_decision.get('total_accepted_ytrue_count')}`",
            f"- allowed_next_phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
            f"- no_predictive_gain_computed: `{result.next_gate_decision.get('no_predictive_gain_computed')}`",
            f"- physical_claim_created: `{result.next_gate_decision.get('physical_claim_created')}`",
        ]
    ) + "\n"
