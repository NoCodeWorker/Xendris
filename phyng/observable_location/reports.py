"""Markdown reports for v5.7.2 observable-location review."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.observable_location.schemas import ObservableLocationCampaignResult


def write_observable_location_reports(result: ObservableLocationCampaignResult, reports_root: str | Path = "reports") -> dict[str, str]:
    root = Path(reports_root)
    report_dir = root / "frontera_c" / "observable_location"
    report_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "candidates": report_dir / "targeted_observable_location_candidates_v5_7_2.md",
        "observed": report_dir / "targeted_observed_measurement_candidates_v5_7_2.md",
        "rejected": report_dir / "targeted_rejected_location_records_v5_7_2.md",
        "next_gate": report_dir / "v5_7_2_next_gate_decision.md",
    }
    paths["candidates"].write_text(_canonical(_render_candidates(result), result), encoding="utf-8")
    paths["observed"].write_text(_canonical(_render_observed(result), result), encoding="utf-8")
    paths["rejected"].write_text(_canonical(_render_rejected(result), result), encoding="utf-8")
    paths["next_gate"].write_text(_canonical(_render_next_gate(result), result), encoding="utf-8")
    return {key: str(path) for key, path in paths.items()}


def _canonical(markdown: str, result: ObservableLocationCampaignResult) -> str:
    contract = build_report_contract(
        title="Targeted Observable Location Review v5.7.2",
        campaign_id="FRONTERA-C-TARGETED-SOURCE-DOWNLOAD-OBSERVABLE-LOCATION-v5_7_2",
        domain_status=result.status,
        domain="targeted_source_download_observable_location",
        next_actions=["Proceed to v5.7.3 only if observed measurement candidates exist."],
        discipline_note="Observable location is permission to review y_true, not y_true itself.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_candidates(result: ObservableLocationCampaignResult) -> str:
    lines = ["# Targeted Observable Location Candidates v5.7.2", "", f"- candidate_location_count: `{len(result.location_candidates)}`", ""]
    for item in result.location_candidates:
        lines.append(f"- `{item.location_id}`: source=`{item.source_candidate_id}`, page=`{item.page_number}`, class=`{item.classification}`")
    return "\n".join(lines) + "\n"


def _render_observed(result: ObservableLocationCampaignResult) -> str:
    lines = ["# Targeted Observed Measurement Candidates v5.7.2", "", f"- observed_measurement_candidate_count: `{len(result.observed_measurement_candidates)}`", ""]
    for item in result.observed_measurement_candidates:
        lines.append(f"- `{item.location_id}`: source=`{item.source_candidate_id}`, page=`{item.page_number}`, observable=`{item.observable_class}`, value_text=`{item.numeric_value_text}`")
    return "\n".join(lines) + "\n"


def _render_rejected(result: ObservableLocationCampaignResult) -> str:
    lines = ["# Targeted Rejected Location Records v5.7.2", "", f"- rejected_location_count: `{len(result.rejected_location_records)}`", ""]
    for item in result.rejected_location_records:
        lines.append(f"- `{item.location_id}`: source=`{item.source_candidate_id}`, class=`{item.classification}`, blockers=`{', '.join(item.extraction_blockers)}`")
    return "\n".join(lines) + "\n"


def _render_next_gate(result: ObservableLocationCampaignResult) -> str:
    return "\n".join(
        [
            "# v5.7.2 Next Gate Decision",
            "",
            f"- final_status: `{result.next_gate_decision.get('final_status')}`",
            f"- verified_source_object_count: `{result.next_gate_decision.get('verified_source_object_count')}`",
            f"- candidate_location_count: `{result.next_gate_decision.get('candidate_location_count')}`",
            f"- observed_measurement_candidate_count: `{result.next_gate_decision.get('observed_measurement_candidate_count')}`",
            f"- allowed_next_phase: `{result.next_gate_decision.get('allowed_next_phase')}`",
            f"- no_ytrue_extracted: `{result.next_gate_decision.get('no_ytrue_extracted')}`",
            f"- no_predictive_gain_computed: `{result.next_gate_decision.get('no_predictive_gain_computed')}`",
        ]
    ) + "\n"
