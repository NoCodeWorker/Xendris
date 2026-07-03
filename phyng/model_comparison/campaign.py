"""Orchestrate model comparison for v4.1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.core.compatibility import normalize_status
from phyng.model_comparison.claim_permission import build_claim_permission_update
from phyng.model_comparison.loader import load_model_comparison_inputs
from phyng.model_comparison.model_registry import get_registered_models
from phyng.model_comparison.negative_controls import evaluate_negative_controls
from phyng.model_comparison.prediction_builder import build_prediction_records
from phyng.model_comparison.reports import write_model_comparison_reports
from phyng.model_comparison.schemas import (
    ClaimPermissionUpdate,
    ModelComparisonCampaignResult,
    ModelComparisonGateResult,
)
from phyng.model_comparison.scoring import compute_comparison_scores

OUTPUT_PATHS = {
    "registry": Path("data/model_comparison/phi_gradient_model_registry_v4_1.json"),
    "predictions": Path("data/model_comparison/phi_gradient_model_predictions_v4_1.json"),
    "scores": Path("data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json"),
    "controls": Path("data/model_comparison/phi_gradient_negative_control_results_v4_1.json"),
    "claim_permission": Path("data/model_comparison/phi_gradient_claim_permission_update_v4_1.json"),
}


def run_phi_gradient_debt_bounded_model_comparison_campaign(
    root: str | Path = ".",
) -> ModelComparisonCampaignResult:
    repo_root = Path(root)
    inputs = load_model_comparison_inputs(repo_root)

    if inputs.blocked_reason:
        gate = _blocked_gate(inputs.blocked_reason)
        result = ModelComparisonCampaignResult(status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_model_comparison_reports(result, repo_root / "reports")
        return result

    # 1. Register models
    models = get_registered_models()

    # 2. Get benchmark rows
    rows = inputs.benchmark_rows.get("benchmark_rows", [])

    # 3. Generate predictions
    predictions = build_prediction_records(models, rows)

    # 4. Compute scores
    scores = compute_comparison_scores(models, rows)

    # 5. Evaluate negative controls
    control_results = evaluate_negative_controls(inputs.negative_control_plan)

    # 6. Build claim permission update
    claim_permission = build_claim_permission_update()

    # 7. Set status
    status = "PHI_GRADIENT_MODEL_COMPARISON_COMPLETED"

    gate = ModelComparisonGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="model_comparison"),
        models=models,
        predictions=predictions,
        comparison_scores=scores,
        negative_control_results=control_results,
        claim_permission_update=claim_permission,
        allowed_claims=claim_permission.allowed_claims,
        blocked_claims=claim_permission.blocked_claims,
    )

    # 8. Write outputs
    output_paths = _write_outputs(repo_root, gate)
    gate.output_paths = output_paths

    # 9. Write reports
    result = ModelComparisonCampaignResult(status=status, gate_result=gate)
    result.report_paths = write_model_comparison_reports(result, repo_root / "reports")

    return result


def _blocked_gate(reason: str) -> ModelComparisonGateResult:
    status_rec = normalize_status(reason, domain="model_comparison")
    claim_permission = ClaimPermissionUpdate(
        source_pressure_ref="",
        benchmark_ref="",
        debt_ref="",
        model_comparison_ref="",
        physical_claim_permission="BLOCKED",
        gradient_mechanism_claim_permission="BLOCKED_BY_SLOT4_DEBT",
        benchmark_claim_permission="BLOCKED",
        next_required_gate="Restore input benchmark artifacts",
    )
    return ModelComparisonGateResult(
        status=reason,
        canonical_status=status_rec,
        claim_permission_update=claim_permission,
        allowed_claims=[],
        blocked_claims=["Model comparison is blocked."],
    )


def _write_outputs(root: Path, gate: ModelComparisonGateResult) -> dict[str, str]:
    paths = {key: root / value for key, value in OUTPUT_PATHS.items()}
    paths["registry"].parent.mkdir(parents=True, exist_ok=True)

    _write_json(paths["registry"], {
        "models": [m.model_dump(mode="json") for m in gate.models],
        "model_count": len(gate.models),
    })
    _write_json(paths["predictions"], {
        "predictions": [p.model_dump(mode="json") for p in gate.predictions],
        "prediction_count": len(gate.predictions),
    })
    _write_json(paths["scores"], {
        "scores": [s.model_dump(mode="json") for s in gate.comparison_scores],
        "score_count": len(gate.comparison_scores),
    })
    _write_json(paths["controls"], {
        "negative_control_results": [c.model_dump(mode="json") for c in gate.negative_control_results],
        "control_count": len(gate.negative_control_results),
    })
    _write_json(paths["claim_permission"], gate.claim_permission_update.model_dump(mode="json"))

    return {key: str(path.relative_to(root)) for key, path in paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
