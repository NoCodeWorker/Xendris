"""Campaign orchestrator for v4.5 external evidence sprint."""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

from phyng.external_evidence.loader import load_evidence_sprint_inputs
from phyng.external_evidence.table_review import run_table_review
from phyng.external_evidence.supplementary_search import run_supplementary_search
from phyng.external_evidence.public_dataset_search import run_public_dataset_search
from phyng.external_evidence.ytrue_candidates import process_external_candidates
from phyng.external_evidence.dataset_update import update_assembled_dataset
from phyng.external_evidence.freeze_decision import evaluate_freeze_decision
from phyng.external_evidence.reports import generate_sprint_reports


def run_phi_gradient_external_evidence_sprint_campaign(root: str | Path = ".") -> dict[str, Any]:
    root_path = Path(root)

    try:
        inputs = load_evidence_sprint_inputs(root_path)
    except FileNotFoundError:
        return {
            "status": "PHI_GRADIENT_EXTERNAL_EVIDENCE_BLOCKED_MISSING_PRIOR_ARTIFACTS",
            "accepted_records": 0,
            "blocked_targets": 0,
            "ready_for_predictive_gain": False,
        }

    # 1. Table Review
    table_results = run_table_review(inputs, root_path)

    # 2. Supplementary Search
    supp_results = run_supplementary_search(inputs, root_path)

    # 3. Public Dataset Search
    pub_results = run_public_dataset_search(inputs, root_path)

    # 4. Candidates and acceptance
    candidates, accepted, rejected = process_external_candidates(
        table_results, supp_results, pub_results, inputs
    )

    # 5. Dataset update
    assembled, next_inputs = update_assembled_dataset(inputs, accepted)

    # 6. Freeze decision
    freeze = evaluate_freeze_decision(assembled)

    # 7. Campaign status resolution
    if assembled.ready_for_predictive_gain:
        campaign_status = "PHI_GRADIENT_EXTERNAL_EVIDENCE_YTRUE_THRESHOLD_REACHED"
    elif len(accepted) > 0:
        campaign_status = "PHI_GRADIENT_EXTERNAL_EVIDENCE_SPRINT_PARTIAL"
    elif freeze.freeze_status == "FROZEN_NO_YTRUE_AVAILABLE":
        campaign_status = "PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE"
    else:
        campaign_status = "PHI_GRADIENT_EXTERNAL_EVIDENCE_NO_YTRUE_FOUND"

    # Helper to write JSON files
    def _write_json(rel_path: str, data: Any):
        abs_path = root_path / rel_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(abs_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)

    # Write output JSON files
    _write_json(
        "data/external_evidence/phi_gradient_table_review_results_v4_5.json",
        [r.model_dump() for r in table_results],
    )
    _write_json(
        "data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json",
        [r.model_dump() for r in supp_results],
    )
    _write_json(
        "data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json",
        [r.model_dump() for r in pub_results],
    )
    _write_json(
        "data/external_evidence/phi_gradient_external_y_true_candidates_v4_5.json",
        [c.model_dump() for c in candidates],
    )
    _write_json(
        "data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json",
        [a.model_dump() for a in accepted],
    )
    _write_json(
        "data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json",
        [r.model_dump() for r in rejected],
    )
    _write_json(
        "data/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.json",
        {
            "sprint_completed_at": datetime.date.today().isoformat(),
            "table_review_count": len(table_results),
            "supplementary_search_count": len(supp_results),
            "public_dataset_search_count": len(pub_results),
            "total_candidates": len(candidates),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
        },
    )
    _write_json("data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json", assembled.model_dump())
    _write_json("data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json", next_inputs.model_dump())
    _write_json("data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json", freeze.model_dump())

    # Generate Markdown reports
    report_paths = generate_sprint_reports(
        table_results,
        supp_results,
        pub_results,
        candidates,
        accepted,
        rejected,
        assembled,
        next_inputs,
        freeze,
        campaign_status,
        root_path,
    )

    return {
        "status": campaign_status,
        "accepted_records": len(accepted),
        "blocked_targets": len(rejected),
        "ready_for_predictive_gain": assembled.ready_for_predictive_gain,
        "report_paths": report_paths,
        "freeze_status": freeze.freeze_status,
    }
