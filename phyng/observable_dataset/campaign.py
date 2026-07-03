"""Orchestrate observable dataset and y_true planning for v4.2."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.core.compatibility import normalize_status
from phyng.observable_dataset.dataset_registry import build_dataset_source_registry
from phyng.observable_dataset.loader import load_observable_ytrue_inputs
from phyng.observable_dataset.normalization import normalize_benchmark_rows
from phyng.observable_dataset.observable_schema import get_observable_schema_records
from phyng.observable_dataset.quality_control import get_quality_control_rules
from phyng.observable_dataset.readiness import evaluate_readiness
from phyng.observable_dataset.reports import write_observable_ytrue_reports
from phyng.observable_dataset.schemas import (
    ObservableYTrueCampaignResult,
    ObservableYTrueGateResult,
    QualityControlRules,
)
from phyng.observable_dataset.ytrue_acquisition import build_acquisition_plan

OUTPUT_PATHS = {
    "schema": Path("data/observables/phi_gradient_observable_schema_v4_2.json"),
    "targets": Path("data/observables/phi_gradient_normalized_observable_targets_v4_2.json"),
    "plan": Path("data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json"),
    "registry": Path("data/observables/phi_gradient_dataset_source_registry_v4_2.json"),
    "readiness": Path("data/observables/phi_gradient_measurement_readiness_matrix_v4_2.json"),
    "qc": Path("data/observables/phi_gradient_quality_control_rules_v4_2.json"),
}


def run_phi_gradient_observable_ytrue_plan_campaign(
    root: str | Path = ".",
) -> ObservableYTrueCampaignResult:
    repo_root = Path(root)
    inputs = load_observable_ytrue_inputs(repo_root)

    if inputs.blocked_reason:
        gate = _blocked_gate(inputs.blocked_reason)
        result = ObservableYTrueCampaignResult(status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_observable_ytrue_reports(result, repo_root / "reports")
        return result

    # 1. Schemas
    schema_records = get_observable_schema_records()

    # 2. Get rows
    rows = inputs.benchmark_rows.get("benchmark_rows", [])

    # 3. Normalize targets
    targets = normalize_benchmark_rows(rows)

    # 4. Acquisition plan
    plan = build_acquisition_plan(targets)

    # 5. Dataset source registry
    registry = build_dataset_source_registry(targets)

    # 6. Readiness matrix
    readiness = evaluate_readiness(targets)

    # 7. QC rules
    qc = get_quality_control_rules()

    # 8. Set status
    status = "PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY"

    allowed = [
        "Observable targets were normalized.",
        "A y_true acquisition plan was generated.",
        "PredictiveGain remains undefined until observed truth exists.",
        "SLOT_4 debt remains blocking for mechanism claims.",
    ]
    blocked = [
        "PHI_GRADIENT is predictively validated.",
        "PHI_GRADIENT has PredictiveGain.",
        "Gradient mechanism is supported.",
        "Frontera C is validated.",
        "Invariant is empirically confirmed.",
    ]

    gate = ObservableYTrueGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="observable_dataset"),
        schema_records=schema_records,
        normalized_targets=targets,
        y_true_acquisition_plan=plan,
        source_registry=registry,
        readiness_matrix=readiness,
        qc_rules=qc,
        allowed_claims=allowed,
        blocked_claims=blocked,
    )

    # 9. Write outputs
    output_paths = _write_outputs(repo_root, gate)
    gate.output_paths = output_paths

    # 10. Write reports
    result = ObservableYTrueCampaignResult(status=status, gate_result=gate)
    result.report_paths = write_observable_ytrue_reports(result, repo_root / "reports")

    return result


def _blocked_gate(reason: str) -> ObservableYTrueGateResult:
    status_rec = normalize_status(reason, domain="observable_dataset")
    return ObservableYTrueGateResult(
        status=reason,
        canonical_status=status_rec,
        qc_rules=QualityControlRules(rules=[], notes=["Quality control blocked by missing inputs."]),
        allowed_claims=[],
        blocked_claims=["y_true planning is blocked."],
    )


def _write_outputs(root: Path, gate: ObservableYTrueGateResult) -> dict[str, str]:
    paths = {key: root / value for key, value in OUTPUT_PATHS.items()}
    paths["schema"].parent.mkdir(parents=True, exist_ok=True)

    _write_json(paths["schema"], {
        "schemas": [s.model_dump(mode="json") for s in gate.schema_records],
        "schema_count": len(gate.schema_records),
    })
    _write_json(paths["targets"], {
        "normalized_targets": [t.model_dump(mode="json") for t in gate.normalized_targets],
        "target_count": len(gate.normalized_targets),
    })
    _write_json(paths["plan"], {
        "y_true_acquisition_plan": [p.model_dump(mode="json") for p in gate.y_true_acquisition_plan],
        "acquisition_item_count": len(gate.y_true_acquisition_plan),
    })
    _write_json(paths["registry"], {
        "dataset_source_registry": [r.model_dump(mode="json") for r in gate.source_registry],
        "registered_sources_count": len(gate.source_registry),
    })
    _write_json(paths["readiness"], {
        "readiness_matrix": [m.model_dump(mode="json") for m in gate.readiness_matrix],
        "readiness_rows_count": len(gate.readiness_matrix),
    })
    _write_json(paths["qc"], gate.qc_rules.model_dump(mode="json"))

    return {key: str(path.relative_to(root)) for key, path in paths.items()}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
