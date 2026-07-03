"""Loader for v4.4.1 audit artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.audit_remediation.schemas import AuditRemediationInputs


REQUIRED_AUDIT_FILES = {
    "full_suite": "data/audits/phygn_full_suite_logic_audit_v4_4_1.json",
    "status_permission": "data/audits/phygn_status_permission_matrix_v4_4_1.json",
    "claim_leakage": "data/audits/phygn_claim_leakage_report_v4_4_1.json",
    "test_logic": "data/audits/phygn_test_logic_audit_v4_4_1.json",
    "debt_boundary": "data/audits/phygn_debt_boundary_audit_v4_4_1.json",
    "metric_integrity": "data/audits/phygn_metric_integrity_audit_v4_4_1.json",
    "remediation_plan": "data/audits/phygn_remediation_plan_v4_4_1.json",
}


def load_audit_remediation_inputs(root: str | Path = ".") -> AuditRemediationInputs:
    repo_root = Path(root)
    payloads: dict[str, dict] = {}
    missing: list[str] = []
    for key, rel_path in REQUIRED_AUDIT_FILES.items():
        path = repo_root / rel_path
        if not path.exists():
            missing.append(rel_path)
            payloads[key] = {}
            continue
        payloads[key] = json.loads(path.read_text(encoding="utf-8"))
    return AuditRemediationInputs(missing_files=missing, **payloads)
