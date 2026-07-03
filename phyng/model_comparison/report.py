from pathlib import Path

from phyng.model_comparison.schemas import ModelComparisonResult, ModelComparisonSpec


def generate_model_comparison_report(
    spec: ModelComparisonSpec,
    result: ModelComparisonResult,
    root_dir: Path,
) -> Path:
    report_dir = root_dir / "reports" / "model_comparison"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{result.comparison_id}.md"

    lines = [
        f"# Model Comparison Report: {result.comparison_id}",
        "",
        "## Input",
        f"- Campaign: {result.campaign_id}",
        f"- System: {result.system_id}",
        f"- Mode: {spec.status}",
        f"- Evidence Level: {result.evidence_level}",
        f"- Maximum Allowed Claim Level: {result.maximum_allowed_claim_level}",
        "",
        "## Models",
        f"- Base: {spec.model_base_name}",
        f"- Base description: {spec.model_base_description}",
        f"- Candidate: {spec.model_candidate_name}",
        f"- Candidate description: {spec.model_candidate_description}",
        "",
        "## Observable",
        f"- Observable: {result.observable}",
        "",
        "## Parameters",
        *[f"- {key}: {value}" for key, value in spec.parameters.items()],
        "",
        "## Source Status",
        "- REQUIRES_SOURCE_FOR_PHYSICAL_INTERPRETATION",
        f"- Linked source IDs: {', '.join(spec.source_ids) if spec.source_ids else 'none'}",
        "",
        "## Series Summary",
        f"- Points: {len(result.y_base)}",
        f"- Max abs delta: {result.max_abs_delta:.6e}",
        "",
        "## Error Metric",
        f"- Metric: {spec.error_metric}",
        f"- Error base: {result.error_base if result.error_base is not None else 'undefined without y_true'}",
        f"- Error candidate: {result.error_candidate if result.error_candidate is not None else 'undefined without y_true'}",
        "",
        "## Gain_C",
        f"- Gain_C: {result.gain_c if result.gain_c is not None else 'undefined without y_true'}",
        f"- Predictive status: {result.predictive_status}",
        "",
        "## Detectability",
        f"- Epsilon: {spec.epsilon_exp if spec.epsilon_exp is not None else 'not provided'}",
        f"- Status: {result.detectability_status}",
        "",
        "## Allowed Claims",
        *[f"- {claim}" for claim in result.allowed_claims],
        "",
        "## Blocked Claims",
        *[f"- {claim}" for claim in result.blocked_claims],
        "",
        "## Limitations",
        "- This is a toy model comparison.",
        "- No physical decoherence prediction is claimed.",
        "- No source-backed physical interpretation is allowed until RAG support exists.",
        "",
        "## Next Tasks",
        *[f"- {task}" for task in result.required_next_steps],
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path
