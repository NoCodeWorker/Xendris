"""Generate Markdown reports for v4.1 model comparison."""

from __future__ import annotations

from pathlib import Path

from phyng.core.report_contract import append_canonical_status_section, build_report_contract
from phyng.model_comparison.schemas import ModelComparisonCampaignResult


def write_model_comparison_reports(
    result: ModelComparisonCampaignResult,
    reports_dir: str | Path = "reports",
) -> dict[str, str]:
    root = Path(reports_dir)
    mc_dir = root / "model_comparison"
    campaigns_dir = root / "campaigns"

    mc_dir.mkdir(parents=True, exist_ok=True)
    campaigns_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "registry": mc_dir / "phi_gradient_model_registry_v4_1.md",
        "predictions": mc_dir / "phi_gradient_model_predictions_v4_1.md",
        "scores": mc_dir / "phi_gradient_benchmark_comparison_scores_v4_1.md",
        "controls": mc_dir / "phi_gradient_negative_control_results_v4_1.md",
        "claim_permission": mc_dir / "phi_gradient_claim_permission_update_v4_1.md",
        "campaign": campaigns_dir / "PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1.md",
    }

    renderers = {
        "registry": _render_registry,
        "predictions": _render_predictions,
        "scores": _render_scores,
        "controls": _render_controls,
        "claim_permission": _render_claim_permission,
    }

    for key, renderer in renderers.items():
        paths[key].write_text(_canonical(renderer(result), result), encoding="utf-8")

    path_map = {key: str(path) for key, path in paths.items()}
    result.report_paths = path_map

    # Write campaign report
    paths["campaign"].write_text(
        _canonical(_render_campaign(result), result, list(path_map.values())), encoding="utf-8"
    )

    return path_map


def _canonical(
    markdown: str,
    result: ModelComparisonCampaignResult,
    reports_generated: list[str] | None = None,
) -> str:
    gate = result.gate_result
    contract = build_report_contract(
        title="PHI_GRADIENT Debt-Bounded Model Comparison v4.1",
        campaign_id=result.campaign_id,
        domain_status=result.status,
        domain="model_comparison",
        reports_generated=reports_generated or [],
        next_actions=[
            "v4.2 — Observable Dataset Normalization & Real y_true Acquisition Plan",
            "v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review",
        ],
        discipline_note="A model may win a benchmark and still lose permission to make a claim.",
    )
    return append_canonical_status_section(markdown, contract)


def _render_registry(result: ModelComparisonCampaignResult) -> str:
    gate = result.gate_result
    models = gate.models
    lines = [
        "# PHI_GRADIENT Model Registry v4.1",
        "",
        f"- model_count: `{len(models)}`",
        "",
    ]
    for m in models:
        lines.extend([
            f"## Model: `{m.model_id}` ({m.model_name})",
            "",
            f"- family: `{m.model_family}`",
            f"- uses_slot4_gradient_mechanism: `{m.uses_slot4_gradient_mechanism}`",
            f"- slot4_debt_compliant: `{m.slot4_debt_compliant}`",
            f"- allowed_claim_scope: {m.allowed_claim_scope}",
            "",
            "### Blocked Claims",
            "",
            *[f"- {c}" for c in m.blocked_claims],
            "",
        ])
    return "\n".join(lines)


def _render_predictions(result: ModelComparisonCampaignResult) -> str:
    gate = result.gate_result
    preds = gate.predictions
    lines = [
        "# PHI_GRADIENT Model Predictions v4.1",
        "",
        f"- prediction_record_count: `{len(preds)}`",
        "",
    ]
    for p in preds[:40]:
        lines.extend([
            f"### Prediction `{p.prediction_id}` - Model: `{p.model_id}`",
            f"- benchmark_id: `{p.benchmark_id}`",
            f"- source_id: `{p.source_id}`",
            f"- observable_type: `{p.observable_type}`",
            f"- predicted_behavior: {p.predicted_behavior}",
            f"- prediction_basis: {p.prediction_basis}",
            f"- uses_real_y_true: `{p.uses_real_y_true}`",
            f"- y_true_available: `{p.y_true_available}`",
            f"- comparison_allowed: `{p.comparison_allowed}`",
            "",
        ])
    return "\n".join(lines)


def _render_scores(result: ModelComparisonCampaignResult) -> str:
    gate = result.gate_result
    scores = gate.comparison_scores
    lines = [
        "# PHI_GRADIENT Benchmark Comparison Scores v4.1",
        "",
        f"- benchmark_row_count: `{scores[0].benchmark_row_count if scores else 0}`",
        f"- PredictiveGain status: `{scores[0].predictive_gain_status if scores else 'UNDEFINED'}`",
        "",
        "## Scores Table",
        "",
        "| Model ID | Observable Alignment | Coverage | Parameter Constraints | Controls | Debt Compliance | Aggregate | Verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s in scores:
        lines.append(
            f"| `{s.model_id}` | {s.observable_alignment_score} | {s.benchmark_coverage_score} | {s.parameter_constraint_score} | {s.negative_control_score} | {s.debt_compliance_score} | **{s.aggregate_score}** | {s.verdict} |"
        )
    return "\n".join(lines) + "\n"


def _render_controls(result: ModelComparisonCampaignResult) -> str:
    gate = result.gate_result
    results = gate.negative_control_results
    lines = [
        "# PHI_GRADIENT Negative Control Results v4.1",
        "",
        f"- control_count: `{len(results)}`",
        "",
    ]
    for r in results:
        lines.extend([
            f"## Control ID: `{r.control_id}` - `{r.control_type}`",
            "",
            f"- survival_status: `{r.survival_status}`",
            f"- expected if analogy: {r.expected_result_if_candidate_is_only_analogy}",
            f"- expected if signal: {r.expected_result_if_candidate_has_signal}",
            f"- observed_result: `{r.observed_result}`",
            f"- failure_reason: {r.failure_reason}",
            f"- claim_impact: `{r.claim_impact}`",
            "",
        ])
    return "\n".join(lines)


def _render_claim_permission(result: ModelComparisonCampaignResult) -> str:
    gate = result.gate_result
    u = gate.claim_permission_update
    return "\n".join([
        "# PHI_GRADIENT Claim Permission Update v4.1",
        "",
        f"- physical_claim_permission: `{u.physical_claim_permission}`",
        f"- gradient_mechanism_claim_permission: `{u.gradient_mechanism_claim_permission}`",
        f"- benchmark_claim_permission: `{u.benchmark_claim_permission}`",
        f"- next_required_gate: **{u.next_required_gate}**",
        "",
        "## Allowed Claims",
        "",
        *[f"- {claim}" for claim in u.allowed_claims],
        "",
        "## Blocked Claims",
        "",
        *[f"- {claim}" for claim in u.blocked_claims],
        "",
        "## Conditional Claims",
        "",
        *[f"- {claim}" for claim in u.conditional_claims],
    ]) + "\n"


def _render_campaign(result: ModelComparisonCampaignResult) -> str:
    gate = result.gate_result
    scores = gate.comparison_scores
    return "\n".join([
        "# Campaign Report - PHI-GRADIENT-DEBT-BOUNDED-MODEL-COMPARISON-v4_1",
        "",
        f"- campaign_id: `{result.campaign_id}`",
        f"- status: `{result.status}`",
        f"- model_count: `{len(gate.models)}`",
        f"- prediction_record_count: `{len(gate.predictions)}`",
        f"- PredictiveGain status: `{scores[0].predictive_gain_status if scores else 'UNDEFINED'}`",
        "",
        "## Reports Generated",
        "",
        *[f"- `{path}`" for path in result.report_paths.values()],
    ]) + "\n"
