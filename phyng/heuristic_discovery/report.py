"""Report writers for heuristic discovery v2.2."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import (
    append_canonical_status_section,
    build_report_contract,
)
from phyng.heuristic_discovery.schemas import HeuristicDiscoveryCampaignResult, HeuristicPipelineResult


def write_heuristic_discovery_reports(
    result: HeuristicDiscoveryCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    heuristic_dir = root / "heuristic_discovery"
    campaigns_dir = root / "campaigns"
    heuristic_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "layer": heuristic_dir / "heuristic_discovery_layer_v2_2.md",
        "generation": heuristic_dir / "candidate_generation_v2_2.md",
        "prioritization": heuristic_dir / "candidate_prioritization_v2_2.md",
        "permission_gate": heuristic_dir / "heuristic_permission_gate_v2_2.md",
        "pipeline": heuristic_dir / "heuristic_to_testable_pipeline_v2_2.md",
        "campaign": campaigns_dir / "HEURISTIC-DISCOVERY-LAYER-v2_2.md",
    }

    pipeline = result.pipeline_result
    paths["layer"].write_text(_with_canonical(_render_layer(pipeline), "HEURISTIC_SEED", result.campaign_id), encoding="utf-8")
    paths["generation"].write_text(_with_canonical(_render_generation(pipeline), "HEURISTIC_SEED", result.campaign_id), encoding="utf-8")
    paths["prioritization"].write_text(_with_canonical(_render_prioritization(pipeline), "HEURISTIC_PRIORITIZED", result.campaign_id), encoding="utf-8")
    gate_status = pipeline.permission_results[0].domain_status if pipeline.permission_results else "HEURISTIC_REVIEW_REQUIRED"
    paths["permission_gate"].write_text(_with_canonical(_render_permission_gate(pipeline), gate_status, result.campaign_id), encoding="utf-8")
    paths["pipeline"].write_text(_with_canonical(_render_pipeline(pipeline), pipeline.canonical_status.domain_status, result.campaign_id), encoding="utf-8")

    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map
    paths["campaign"].write_text(_with_canonical(_render_campaign(result), result.status, result.campaign_id, list(path_map.values())), encoding="utf-8")
    return path_map


def _with_canonical(markdown: str, domain_status: str, campaign_id: str, reports_generated: list[str] | None = None) -> str:
    contract = build_report_contract(
        title="Heuristic Discovery v2.2",
        campaign_id=campaign_id,
        domain_status=domain_status,
        reports_generated=reports_generated or [],
        discipline_note="Heuristics may guide search. They may not grant truth.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_layer(pipeline: HeuristicPipelineResult) -> str:
    return "\n".join([
        "# Heuristic Discovery Layer v2.2",
        "",
        "## Core Rule",
        "",
        "Heuristic discovery prioritizes candidates for testing. It does not validate candidates.",
        "",
        f"- raw_problem: `{pipeline.raw_problem}`",
        f"- domain: `{pipeline.domain}`",
        f"- candidates_generated: `{len(pipeline.candidates)}`",
    ]) + "\n"


def _render_generation(pipeline: HeuristicPipelineResult) -> str:
    lines = [
        "# Candidate Generation v2.2",
        "",
        "| Candidate ID | Family | Hypothesis |",
        "|---|---|---|",
    ]
    for candidate in pipeline.candidates:
        lines.append(f"| `{candidate.candidate_id}` | `{candidate.candidate_family}` | {candidate.proposed_hypothesis} |")
    return "\n".join(lines) + "\n"


def _render_prioritization(pipeline: HeuristicPipelineResult) -> str:
    lines = [
        "# Candidate Prioritization v2.2",
        "",
        "Priority score is not evidence.",
        "",
        "| Rank | Candidate ID | Family | Priority Score |",
        "|---:|---|---|---:|",
    ]
    for index, candidate in enumerate(pipeline.ranking.candidates, 1):
        score = candidate.heuristic_scores.get("priority_score", 0.0)
        lines.append(f"| {index} | `{candidate.candidate_id}` | `{candidate.candidate_family}` | {score:.4f} |")
    return "\n".join(lines) + "\n"


def _render_permission_gate(pipeline: HeuristicPipelineResult) -> str:
    lines = [
        "# Heuristic Permission Gate v2.2",
        "",
        "| Candidate ID | Status | Test Design | Claim Authorized | Missing Fields |",
        "|---|---|---|---|---|",
    ]
    for result in pipeline.permission_results:
        missing = ", ".join(result.missing_fields) if result.missing_fields else "None"
        lines.append(
            f"| `{result.candidate_id}` | `{result.domain_status}` | {result.is_test_design_allowed} | "
            f"{result.is_claim_authorized} | {missing} |"
        )
    return "\n".join(lines) + "\n"


def _render_pipeline(pipeline: HeuristicPipelineResult) -> str:
    top_id = pipeline.top_candidate.candidate_id if pipeline.top_candidate else "None"
    return "\n".join([
        "# Heuristic-to-Testable Pipeline v2.2",
        "",
        f"- top_candidate_id: `{top_id}`",
        f"- canonical_status: `{pipeline.canonical_status.domain_status}`",
        f"- next_best_question: {pipeline.next_best_question}",
        "",
        "## Missing Fields",
        "",
        *([f"- `{field}`" for field in pipeline.missing_fields] if pipeline.missing_fields else ["- None"]),
    ]) + "\n"


def _render_campaign(result: HeuristicDiscoveryCampaignResult) -> str:
    pipeline = result.pipeline_result
    return "\n".join([
        "# Campaign Report - HEURISTIC-DISCOVERY-LAYER-v2_2",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- candidates_generated: `{len(pipeline.candidates)}`",
        f"- top_candidate_id: `{pipeline.ranking.top_candidate_id}`",
        "",
        "## Allowed Claims",
        "",
        "- Heuristic discovery generated and prioritized candidates for testing.",
        "",
        "## Blocked Claims",
        "",
        "- Heuristic priority does not validate candidates.",
        "- Heuristic support is not source, benchmark, or experimental evidence.",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
        "",
        "## Tests",
        "",
        "- `tests/test_heuristic_candidate_schema_v2_2.py`",
        "- `tests/test_heuristic_permission_gate_v2_2.py`",
        "- `tests/test_heuristic_candidate_generation_v2_2.py`",
        "- `tests/test_heuristic_prioritization_v2_2.py`",
        "- `tests/test_heuristic_pipeline_v2_2.py`",
        "- `tests/test_heuristic_discovery_campaign_v2_2.py`",
    ]) + "\n"
