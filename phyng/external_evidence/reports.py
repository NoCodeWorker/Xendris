"""Report generation for v4.5 external evidence sprint."""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any


def generate_sprint_reports(
    table_results: list,
    supp_results: list,
    pub_results: list,
    candidates: list,
    accepted: list,
    rejected: list,
    assembled: Any,
    next_inputs: Any,
    freeze: Any,
    campaign_status: str,
    root: str | Path = ".",
) -> dict[str, str]:
    root_path = Path(root)

    report_paths = {
        "table_review": "reports/external_evidence/phi_gradient_table_review_results_v4_5.md",
        "supplementary": "reports/external_evidence/phi_gradient_supplementary_search_results_v4_5.md",
        "public_dataset": "reports/external_evidence/phi_gradient_public_dataset_search_results_v4_5.md",
        "candidates": "reports/external_evidence/phi_gradient_external_y_true_candidates_v4_5.md",
        "accepted": "reports/external_evidence/phi_gradient_external_y_true_accepted_v4_5.md",
        "rejected": "reports/external_evidence/phi_gradient_external_y_true_rejected_v4_5.md",
        "audit_trail": "reports/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.md",
        "freeze_decision": "reports/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.md",
        "assembled_dataset": "reports/y_true/phi_gradient_assembled_y_true_dataset_v4_5.md",
        "next_inputs": "reports/y_true/phi_gradient_next_predictive_gain_inputs_v4_5.md",
        "campaign": "reports/campaigns/PHI-GRADIENT-EXTERNAL-EVIDENCE-SPRINT-v4_5.md",
    }

    # Helper to write report
    def _write_report(rel_path: str, title: str, content: str) -> str:
        abs_path = root_path / rel_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        full_content = (
            f"# {title}\n\n"
            f"Generated: {datetime.date.today().isoformat()}\n\n"
            f"{content}\n\n"
            f"## Canonical Status\n"
            f"- Campaign Status: `{campaign_status}`\n"
            f"- Ready for PredictiveGain: `{assembled.ready_for_predictive_gain}`\n"
            f"- Freeze Status: `{freeze.freeze_status}`\n"
            f"- SLOT_4 Debt Status: `{assembled.slot4_debt_status}`\n"
            f"- Physical Claim Permission: `{assembled.physical_claim_permission}`\n\n"
            f"## Allowed and Blocked Claims\n\n"
            f"### Allowed Claims:\n"
            f"- External evidence acquisition was attempted.\n"
            f"- Accepted external y_true records were added if QC passed.\n"
            f"- Candidate was frozen if the y_true threshold was not reached.\n"
            f"- PredictiveGain remains undefined until computed by a later gate.\n\n"
            f"### Blocked Claims:\n"
            f"- PHI_GRADIENT is validated.\n"
            f"- PHI_GRADIENT has PredictiveGain before v4.6.\n"
            f"- Gradient mechanism supports decoherence mitigation.\n"
            f"- SLOT_4 debt is resolved.\n"
            f"- Frontera C is validated.\n"
            f"- Invariant is empirically confirmed.\n\n"
            f"## Discipline Note\n"
            f"Looking for data is not finding data. Finding data is not accepting data. "
            f"Accepting data requires provenance. Freezing a candidate is progress when the alternative is fiction.\n"
        )
        with open(abs_path, "w", encoding="utf-8") as f:
            f.write(full_content)
        return rel_path

    # 1. Table Review
    table_lines = [f"- Target {r.target_id}: Status = `{r.evidence_status}`, Value = `{r.numeric_value} {r.unit}`, PDF = `{r.local_pdf_path}`" for r in table_results]
    _write_report(
        report_paths["table_review"],
        "Phygn v4.5 — Table Review Results",
        f"Audited {len(table_results)} items from manual extraction review queue.\n\n" + "\n".join(table_lines)
    )

    # 2. Supplementary Search
    supp_lines = [f"- Source {r.source_id}: Status = `{r.evidence_status}`, Path = `{r.supplementary_path}`" for r in supp_results]
    _write_report(
        report_paths["supplementary"],
        "Phygn v4.5 — Supplementary Search Results",
        f"Searched local supplementary folders.\n\n" + "\n".join(supp_lines)
    )

    # 3. Public Dataset Search
    pub_lines = [f"- Source {r.source_id}: Status = `{r.evidence_status}`, Local Path = `{r.local_dataset_path}`" for r in pub_results]
    _write_report(
        report_paths["public_dataset"],
        "Phygn v4.5 — Public Dataset Search Results",
        f"Searched local external datasets folder.\n\n" + "\n".join(pub_lines)
    )

    # 4. Candidates
    cand_lines = [f"- Candidate {c.candidate_id} for Target {c.target_id}: Track = `{c.acquisition_track}`, Can Enter = `{c.can_enter_dataset}`, QC = `{c.qc_status}`" for c in candidates]
    _write_report(
        report_paths["candidates"],
        "Phygn v4.5 — External y_true Candidates",
        f"Found {len(candidates)} external y_true candidates.\n\n" + "\n".join(cand_lines)
    )

    # 5. Accepted
    acc_lines = [f"- accepted {a.y_true_id}: target = `{a.target_id}`, value = `{a.value} {a.unit}`" for a in accepted]
    _write_report(
        report_paths["accepted"],
        "Phygn v4.5 — Accepted External y_true Records",
        f"Accepted {len(accepted)} external y_true records.\n\n" + ("\n".join(acc_lines) if acc_lines else "No records accepted.")
    )

    # 6. Rejected
    rej_lines = [f"- Candidate {r.candidate_id}: target = `{r.target_id}`, Reason = `{r.rejection_reason}`" for r in rejected]
    _write_report(
        report_paths["rejected"],
        "Phygn v4.5 — Rejected External y_true Records",
        f"Rejected {len(rejected)} external y_true records.\n\n" + "\n".join(rej_lines)
    )

    # 7. Audit Trail
    _write_report(
        report_paths["audit_trail"],
        "Phygn v4.5 — External Evidence Audit Trail",
        f"Audit trail of external evidence acquisition.\n\n"
        f"- Table Review: evaluated {len(table_results)} items.\n"
        f"- Supplementary Search: evaluated {len(supp_results)} items.\n"
        f"- Public Dataset Search: evaluated {len(pub_results)} items.\n"
        f"- Candidates synthesised: {len(candidates)}.\n"
        f"- Accepted y_true: {len(accepted)}.\n"
        f"- Rejected y_true: {len(rejected)}.\n"
    )

    # 8. Freeze Decision
    _write_report(
        report_paths["freeze_decision"],
        "Phygn v4.5 — Candidate Freeze Decision",
        f"Decision ID: `{freeze.decision_id}`\n"
        f"Freeze Status: `{freeze.freeze_status}`\n"
        f"Freeze Reason: `{freeze.freeze_reason}`\n\n"
        f"### Required to Unfreeze:\n" + "\n".join(f"- {req}" for req in freeze.required_to_unfreeze) + "\n\n"
        f"### Allowed Future Work:\n" + "\n".join(f"- {w}" for w in freeze.allowed_future_work) + "\n\n"
        f"### Blocked Future Work:\n" + "\n".join(f"- {w}" for w in freeze.blocked_future_work)
    )

    # 9. Assembled dataset
    _write_report(
        report_paths["assembled_dataset"],
        "Phygn v4.5 — Assembled y_true Dataset",
        f"Total records in dataset: `{assembled.total_y_true_count}`.\n"
        f"Dataset ID: `{assembled.dataset_id}`\n"
        f"Matched predictions: `{assembled.matched_prediction_count}`.\n"
    )

    # 10. Next Inputs
    _write_report(
        report_paths["next_inputs"],
        "Phygn v4.5 — Next PredictiveGain Inputs",
        f"Ready for PredictiveGain: `{next_inputs.ready_for_predictive_gain}`\n"
        f"Status: `{next_inputs.predictive_gain_status}`\n"
        f"Recommended next phase: `{next_inputs.recommended_next_phase}`\n"
    )

    # 11. Campaign Report
    _write_report(
        report_paths["campaign"],
        "Phygn v4.5 — Campaign Run Summary: PHI-GRADIENT-EXTERNAL-EVIDENCE-SPRINT-v4_5",
        f"Execution Summary:\n\n"
        f"- Status: `{campaign_status}`\n"
        f"- Table Review items: {len(table_results)}\n"
        f"- Supplementary Search items: {len(supp_results)}\n"
        f"- Public Dataset Search items: {len(pub_results)}\n"
        f"- Candidates processed: {len(candidates)}\n"
        f"- Accepted y_true count: {len(accepted)}\n"
        f"- Rejected y_true count: {len(rejected)}\n"
        f"- Freeze Status: `{freeze.freeze_status}`\n"
    )

    return report_paths
