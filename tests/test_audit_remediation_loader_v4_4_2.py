from __future__ import annotations

from pathlib import Path

from phyng.audit_remediation.loader import REQUIRED_AUDIT_FILES, load_audit_remediation_inputs


def test_missing_audit_blocks_remediation(tmp_path: Path) -> None:
    inputs = load_audit_remediation_inputs(tmp_path)

    assert sorted(inputs.missing_files) == sorted(REQUIRED_AUDIT_FILES.values())
