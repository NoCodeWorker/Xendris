"""Orchestrate real y_true extraction and dataset assembly campaign."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from phyng.core.compatibility import normalize_status
from phyng.ytrue_extraction.dataset_assembly import assemble_y_true_dataset
from phyng.ytrue_extraction.extraction_candidates import extract_candidates
from phyng.ytrue_extraction.extraction_queues import build_queues
from phyng.ytrue_extraction.loader import load_extraction_inputs
from phyng.ytrue_extraction.quality_report import build_quality_report
from phyng.ytrue_extraction.reports import write_ytrue_reports
from phyng.ytrue_extraction.schemas import (
    AssembledDatasetPayload,
    DatasetQualityReport,
    ExtractionCampaignResult,
    ExtractionGateResult,
    NextPredictiveGainInputs,
)
from phyng.ytrue_extraction.source_coverage_audit import run_source_coverage_audit

OUTPUT_PATHS = {
    "audit": Path("data/y_true/phi_gradient_source_coverage_audit_v4_3.json"),
    "candidates": Path("data/y_true/phi_gradient_y_true_extraction_candidates_v4_3.json"),
    "table_q": Path("data/y_true/phi_gradient_manual_table_extraction_queue_v4_3.json"),
    "fig_q": Path("data/y_true/phi_gradient_figure_digitization_queue_v4_3.json"),
    "pub_q": Path("data/y_true/phi_gradient_public_dataset_lookup_queue_v4_3.json"),
    "supp_q": Path("data/y_true/phi_gradient_supplementary_lookup_queue_v4_3.json"),
    "assembled": Path("data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json"),
    "blocked": Path("data/y_true/phi_gradient_blocked_y_true_targets_v4_3.json"),
    "quality": Path("data/y_true/phi_gradient_dataset_quality_report_v4_3.json"),
    "next_inputs": Path("data/y_true/phi_gradient_v4_3_next_predictive_gain_inputs.json"),
}


def run_phi_gradient_real_ytrue_extraction_campaign(
    root: str | Path = ".",
) -> ExtractionCampaignResult:
    repo_root = Path(root)
    inputs = load_extraction_inputs(repo_root)

    if inputs.blocked_reason:
        gate = _blocked_gate(inputs.blocked_reason)
        result = ExtractionCampaignResult(status=inputs.blocked_reason, gate_result=gate)
        result.report_paths = write_ytrue_reports(result, repo_root / "reports")
        return result

    # 1. Inputs
    targets = inputs.normalized_targets.get("normalized_targets", [])
    hashes = inputs.source_hashes
    rows = inputs.benchmark_rows.get("benchmark_rows", [])
    predictions = inputs.model_predictions

    # 2. Source coverage audit
    audit_records = run_source_coverage_audit(targets, hashes, rows, repo_root)

    # 3. Extraction candidates
    candidates = extract_candidates(targets)

    # 4. Actionable queues
    table_q, fig_q, pub_q, supp_q = build_queues(
        targets, [c.model_dump() for c in candidates]
    )

    # 5. Assemble dataset
    assembled, blocked_list, next_inputs = assemble_y_true_dataset(
        targets, [c.model_dump() for c in candidates], hashes, predictions
    )

    # 6. Quality report
    quality = build_quality_report(
        targets,
        [c.model_dump() for c in candidates],
        [b.model_dump() for b in blocked_list],
        table_q,
        fig_q,
        pub_q,
        supp_q,
        assembled.y_true_record_count,
        assembled.ready_for_predictive_gain,
    )

    # 7. Status mapping
    if assembled.ready_for_predictive_gain:
        status = "PHI_GRADIENT_YTRUE_DATASET_READY_FOR_PREDICTIVE_GAIN"
    elif assembled.y_true_record_count > 0:
        status = "PHI_GRADIENT_YTRUE_EXTRACTION_PARTIAL"
    elif len(table_q) > 0:
        status = "PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_MANUAL_TABLE_REVIEW"
    elif len(fig_q) > 0:
        status = "PHI_GRADIENT_YTRUE_EXTRACTION_REQUIRES_FIGURE_DIGITIZATION"
    else:
        status = "PHI_GRADIENT_YTRUE_EXTRACTION_NO_VALUES_FOUND"

    allowed = [
        "A y_true extraction attempt was performed.",
        "A source-coverage audit was generated.",
        "A y_true dataset was assembled if accepted records exist.",
        "PredictiveGain remains undefined unless the minimum viable y_true threshold is met.",
    ]
    blocked = [
        "PHI_GRADIENT is predictively validated.",
        "PHI_GRADIENT has PredictiveGain.",
        "Gradient mechanism is supported.",
        "SLOT_4 debt is resolved.",
        "Frontera C is validated.",
        "Invariant is empirically confirmed.",
    ]

    gate = ExtractionGateResult(
        status=status,
        canonical_status=normalize_status(status, domain="observable_dataset"),
        source_coverage_audit=audit_records,
        extraction_candidates=candidates,
        manual_table_extraction_queue=table_q,
        figure_digitization_queue=fig_q,
        public_dataset_lookup_queue=pub_q,
        supplementary_lookup_queue=supp_q,
        assembled_y_true_dataset=assembled,
        blocked_y_true_targets=blocked_list,
        dataset_quality_report=quality,
        next_predictive_gain_inputs=next_inputs,
        allowed_claims=allowed,
        blocked_claims=blocked,
    )

    # 8. Write outputs
    _write_outputs(repo_root, gate)

    # 9. Write reports
    result = ExtractionCampaignResult(status=status, gate_result=gate)
    result.report_paths = write_ytrue_reports(result, repo_root / "reports")

    return result


def _blocked_gate(reason: str) -> ExtractionGateResult:
    status_rec = normalize_status(reason, domain="observable_dataset")
    empty_assembled = AssembledDatasetPayload(
        created_at="2026-07-01",
        source_plan_ref="data/observables/phi_gradient_y_true_acquisition_plan_v4_2.json",
        target_count=0,
        y_true_record_count=0,
        records=[],
        ready_for_predictive_gain=False,
        slot4_debt_status="OPEN_BLOCKING_FOR_GRADIENT_CLAIMS",
        physical_claim_permission="BLOCKED",
    )
    empty_quality = DatasetQualityReport(
        target_count=0,
        candidate_count=0,
        accepted_y_true_count=0,
        blocked_count=0,
        manual_table_queue_count=0,
        figure_digitization_queue_count=0,
        public_dataset_lookup_count=0,
        supplementary_lookup_count=0,
        qc_pass_count=0,
        qc_fail_count=0,
        unit_normalization_issues=0,
        source_coverage_issues=0,
        prediction_matching_issues=0,
        readiness_status="YTRUE_DATASET_EMPTY_NEEDS_EXTRACTION",
    )
    empty_next = NextPredictiveGainInputs(
        ready_for_predictive_gain=False,
        y_true_dataset_path="data/y_true/phi_gradient_assembled_y_true_dataset_v4_3.json",
        prediction_dataset_path="data/model_comparison/phi_gradient_model_predictions_v4_1.json",
        matched_prediction_count=0,
        minimum_viable_y_true_count=3,
        recommended_next_phase="v4.4 — Manual Data Extraction Sprint",
    )
    return ExtractionGateResult(
        status=reason,
        canonical_status=status_rec,
        assembled_y_true_dataset=empty_assembled,
        dataset_quality_report=empty_quality,
        next_predictive_gain_inputs=empty_next,
        allowed_claims=[],
        blocked_claims=["y_true extraction is blocked."],
    )


def _write_outputs(root: Path, gate: ExtractionGateResult) -> None:
    paths = {key: root / value for key, value in OUTPUT_PATHS.items()}
    paths["audit"].parent.mkdir(parents=True, exist_ok=True)

    _write_json(paths["audit"], {
        "source_coverage_audit": [r.model_dump(mode="json") for r in gate.source_coverage_audit],
        "total_targets_audited": len(gate.source_coverage_audit),
    })
    _write_json(paths["candidates"], {
        "extraction_candidates": [c.model_dump(mode="json") for c in gate.extraction_candidates],
        "candidate_count": len(gate.extraction_candidates),
    })
    _write_json(paths["table_q"], {
        "manual_table_extraction_queue": [i.model_dump(mode="json") for i in gate.manual_table_extraction_queue],
        "queue_item_count": len(gate.manual_table_extraction_queue),
    })
    _write_json(paths["fig_q"], {
        "figure_digitization_queue": [i.model_dump(mode="json") for i in gate.figure_digitization_queue],
        "queue_item_count": len(gate.figure_digitization_queue),
    })
    _write_json(paths["pub_q"], {
        "public_dataset_lookup_queue": [i.model_dump(mode="json") for i in gate.public_dataset_lookup_queue],
        "queue_item_count": len(gate.public_dataset_lookup_queue),
    })
    _write_json(paths["supp_q"], {
        "supplementary_lookup_queue": [i.model_dump(mode="json") for i in gate.supplementary_lookup_queue],
        "queue_item_count": len(gate.supplementary_lookup_queue),
    })
    _write_json(paths["assembled"], gate.assembled_y_true_dataset.model_dump(mode="json"))
    _write_json(paths["blocked"], {
        "blocked_y_true_targets": [b.model_dump(mode="json") for b in gate.blocked_y_true_targets],
        "blocked_target_count": len(gate.blocked_y_true_targets),
    })
    _write_json(paths["quality"], gate.dataset_quality_report.model_dump(mode="json"))
    _write_json(paths["next_inputs"], gate.next_predictive_gain_inputs.model_dump(mode="json"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
