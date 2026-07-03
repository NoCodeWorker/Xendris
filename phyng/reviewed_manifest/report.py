"""Reports for PHI_GRADIENT reviewed local manifest v3.1."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.reviewed_manifest.schemas import PhiGradientReviewedManifestCampaignResult


def write_phi_gradient_reviewed_manifest_reports(
    result: PhiGradientReviewedManifestCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    report_dir = root / "reviewed_manifest"
    campaigns_dir = root / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "reviewed_manifest": report_dir / "phi_gradient_reviewed_manifest_v3_1.md",
        "manifest_validation": report_dir / "phi_gradient_manifest_validation_v3_1.md",
        "extract_pack": report_dir / "phi_gradient_extract_pack_v3_1.md",
        "extract_validation": report_dir / "phi_gradient_extract_validation_v3_1.md",
        "slot_coverage": report_dir / "phi_gradient_slot_coverage_v3_1.md",
        "negative_sources": report_dir / "phi_gradient_negative_sources_v3_1.md",
        "benchmark_comparability": report_dir / "phi_gradient_benchmark_comparability_v3_1.md",
        "real_source_gate": report_dir / "phi_gradient_real_source_gate_v3_1.md",
        "loop_feedback": report_dir / "phi_gradient_loop_feedback_v3_1.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1.md",
    }
    renderers = {
        "reviewed_manifest": _render_manifest,
        "manifest_validation": _render_manifest_validation,
        "extract_pack": _render_extract_pack,
        "extract_validation": _render_extract_validation,
        "slot_coverage": _render_slot_coverage,
        "negative_sources": _render_negative_sources,
        "benchmark_comparability": _render_benchmark,
        "real_source_gate": _render_gate,
        "loop_feedback": _render_loop,
    }
    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")
    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8")
    return path_map


def _canonical(
    markdown: str,
    result: PhiGradientReviewedManifestCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    contract = build_report_contract(
        title="PHI_GRADIENT Reviewed Local Manifest v3.1",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="reviewed_manifest",
        reports_generated=reports_generated or [],
        next_actions=result.gate_result.next_actions,
        discipline_note="A reviewed manifest can open the evidence gate. Only validated extracts can walk through it.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_manifest(result: PhiGradientReviewedManifestCampaignResult) -> str:
    gate = result.gate_result
    manifest = gate.manifest
    return "\n".join([
        "# PHI_GRADIENT Reviewed Manifest v3.1",
        "",
        f"- manifest_id: `{manifest.manifest_id}`",
        f"- entry_count: `{len(manifest.entries)}`",
        f"- manifest_created: `{gate.manifest_created}`",
        f"- traceable_identifier_coverage: `{gate.manifest_validation.traceable_entry_count}/{gate.manifest_validation.entry_count}`",
        "",
        "## Entries",
        "",
        *_or_none([
            f"- `{entry.source_id}`: `{entry.review_status}`, slots=`{', '.join(entry.target_slots)}`, fixture=`{entry.is_fixture}`, test_double=`{entry.is_test_double}`"
            for entry in manifest.entries
        ]),
        "",
        "## Fixture/Test-Double Exclusion",
        "",
        "- Fixture and test-double entries are recorded but cannot count as real support.",
    ]) + "\n"


def _render_manifest_validation(result: PhiGradientReviewedManifestCampaignResult) -> str:
    validation = result.gate_result.manifest_validation
    return "\n".join([
        "# PHI_GRADIENT Manifest Validation v3.1",
        "",
        f"- status: `{validation.status}`",
        f"- manifest_count: `{validation.entry_count}`",
        f"- traceable_identifier_coverage: `{validation.traceable_entry_count}/{validation.entry_count}`",
        f"- accepted_entries: `{', '.join(validation.accepted_entry_ids)}`",
        f"- rejected_entries: `{', '.join(validation.rejected_entry_ids)}`",
        "",
        "## Warnings",
        "",
        *_or_none([f"- {warning}" for warning in validation.warnings]),
        "",
        "## Errors",
        "",
        *_or_none([f"- {error}" for error in validation.errors]),
    ]) + "\n"


def _render_extract_pack(result: PhiGradientReviewedManifestCampaignResult) -> str:
    pack = result.gate_result.extract_pack
    return "\n".join([
        "# PHI_GRADIENT Extract Pack v3.1",
        "",
        f"- extract_pack_id: `{pack.extract_pack_id}`",
        f"- manifest_id: `{pack.manifest_id}`",
        f"- extract_count: `{len(pack.extracts)}`",
        f"- extract_pack_created: `{result.gate_result.extract_pack_created}`",
        "",
        "## Extracts",
        "",
        *_or_none([f"- `{extract.extract_id}`: `{extract.source_id}` -> `{extract.slot_id}`" for extract in pack.extracts]),
    ]) + "\n"


def _render_extract_validation(result: PhiGradientReviewedManifestCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Extract Validation v3.1",
        "",
        f"- validated_extract_count: `{gate.validated_extract_count}`",
        f"- rejected_analogy_count: `{gate.rejected_analogy_count}`",
        "",
        "## Results",
        "",
        *_or_none([
            f"- `{validation.extract_id}`: `{validation.status}`, counts_as_real_support=`{validation.counts_as_real_support}`"
            for validation in gate.extract_validations
        ]),
    ]) + "\n"


def _render_slot_coverage(result: PhiGradientReviewedManifestCampaignResult) -> str:
    coverage = result.gate_result.slot_coverage
    return "\n".join([
        "# PHI_GRADIENT Slot Coverage v3.1",
        "",
        "## Slot Coverage Matrix",
        "",
        *[
            f"- `{record.slot_id}`: `{record.coverage_status}`, candidates=`{len(record.candidate_sources)}`, accepted=`{record.accepted_support_count}`, missing=`{', '.join(record.missing_requirements)}`"
            for record in coverage.records
        ],
        "",
        "## Missing Slots",
        "",
        *_or_none([f"- `{slot}`" for slot in coverage.missing_slots]),
    ]) + "\n"


def _render_negative_sources(result: PhiGradientReviewedManifestCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Negative Sources v3.1",
        "",
        f"- negative_source_count: `{len(result.gate_result.negative_source_ids)}`",
        "",
        "## Negative Sources",
        "",
        *_or_none([f"- `{source_id}`" for source_id in result.gate_result.negative_source_ids]),
    ]) + "\n"


def _render_benchmark(result: PhiGradientReviewedManifestCampaignResult) -> str:
    benchmark = result.gate_result.benchmark_comparability
    return "\n".join([
        "# PHI_GRADIENT Benchmark Comparability v3.1",
        "",
        f"- status: `{benchmark.status}`",
        f"- benchmark_comparable_count: `{benchmark.comparable_records}`",
        "",
        "## Missing Requirements",
        "",
        *_or_none([f"- {item}" for item in benchmark.missing_requirements]),
    ]) + "\n"


def _render_gate(result: PhiGradientReviewedManifestCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# PHI_GRADIENT Real Source Gate v3.1",
        "",
        f"- status: `{gate.status}`",
        f"- manifest_count: `{gate.manifest_validation.entry_count}`",
        f"- validated_extract_count: `{gate.validated_extract_count}`",
        f"- negative_source_count: `{len(gate.negative_source_ids)}`",
        f"- benchmark_comparable_count: `{gate.benchmark_comparability.comparable_records}`",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in gate.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in gate.blocked_claims],
        "",
        "## Next Actions",
        "",
        *[f"- {action}" for action in gate.next_actions],
    ]) + "\n"


def _render_loop(result: PhiGradientReviewedManifestCampaignResult) -> str:
    return "\n".join([
        "# PHI_GRADIENT Loop Feedback v3.1",
        "",
        f"- loop_event_id: `{result.loop_result.audit_event_id}`",
        f"- result_status: `{result.status}`",
        "",
        "## Update Proposals",
        "",
        *[f"- `{proposal.proposal_type}`: {proposal.description}" for proposal in result.update_proposals],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in result.gate_result.blocked_claims],
    ]) + "\n"


def _render_campaign(result: PhiGradientReviewedManifestCampaignResult) -> str:
    gate = result.gate_result
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- manifest_count: `{gate.manifest_validation.entry_count}`",
        f"- validated_extract_count: `{gate.validated_extract_count}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"


def _or_none(items: list[str]) -> list[str]:
    return items if items else ["- None"]
