import json

from scripts.audit_benchmark_suite_excellence import (
    build_suite_audit,
    load_quarantined_summary_paths,
    mark_quarantined_records,
)
from scripts.check_benchmark_evidence_citations import (
    check_rejected_artifact_citations,
    load_rejected_artifacts,
)
from scripts.release_gate_v0_2_2 import GateStep, decide_status


def _blocked_record(path: str) -> dict[str, object]:
    return {
        "summary_path": path,
        "report_path": "docs/blocked.md",
        "decision": "BLOCKED_FOR_INTERPRETATION",
        "has_blockers": True,
        "is_ready": False,
        "issues": [{"code": "missing_dataset_hash", "severity": "BLOCKER", "message": "missing"}],
        "blocker_count": 1,
        "warning_count": 0,
        "note_count": 0,
        "is_quarantined_historical": False,
    }


def test_quarantined_rejected_artifacts_do_not_count_as_active_blockers(tmp_path):
    manifest = tmp_path / "HISTORICAL_REJECTED_ARTIFACTS.md"
    manifest.write_text(
        "| `runs/bad_summary.json` | `missing_dataset_hash` | yes | none | historical only |\n",
        encoding="utf-8",
    )
    records = mark_quarantined_records(
        [_blocked_record("runs/bad_summary.json")],
        load_quarantined_summary_paths(manifest),
    )
    payload = build_suite_audit(records)

    assert payload["blocked_count"] == 0
    assert payload["quarantined_rejected_count"] == 1
    assert payload["records"][0]["is_quarantined_historical"] is True


def test_non_quarantined_blocked_artifact_still_blocks_release():
    payload = build_suite_audit([_blocked_record("runs/active_bad_summary.json")])

    assert payload["blocked_count"] == 1
    assert payload["quarantined_rejected_count"] == 0


def test_unsafe_reference_to_rejected_artifact_still_fails(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    registry.write_text(
        json.dumps(
            {
                "rejected": [
                    {
                        "summary_path": "runs/bad_summary.json",
                        "report_path": None,
                        "reason": "missing_dataset_hash",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (docs / "report.md").write_text("Evidence uses runs/bad_summary.json.\n", encoding="utf-8")

    violations = check_rejected_artifact_citations(load_rejected_artifacts(registry), docs)

    assert len(violations) == 1


def test_historical_rejected_reference_is_allowed(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    registry.write_text(
        json.dumps(
            {
                "rejected": [
                    {
                        "summary_path": "runs/bad_summary.json",
                        "report_path": None,
                        "reason": "missing_dataset_hash",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (docs / "history.md").write_text(
        "## Historical Rejected Artifacts\n\n"
        "`runs/bad_summary.json` is rejected and not admitted evidence.\n",
        encoding="utf-8",
    )

    violations = check_rejected_artifact_citations(load_rejected_artifacts(registry), docs)

    assert violations == []


def test_admitted_artifacts_remain_required_for_public_claims():
    payload = build_suite_audit([_blocked_record("runs/bad_summary.json")])

    assert payload["ready_count"] == 0
    assert payload["blocked_count"] == 1


def test_release_gate_separates_warnings_from_blockers():
    warning = GateStep(
        name="git_diff_check",
        command=("git", "diff", "--check"),
        returncode=1,
        stdout="",
        stderr="warning: in the working copy of '.gitignore', LF will be replaced by CRLF\n",
        warning_only=True,
    )
    blocker = GateStep(
        name="audit",
        command=("python", "audit.py"),
        returncode=1,
        stdout="blocked",
        stderr="",
    )

    assert decide_status([warning]) == "WARNINGS_PRESENT"
    assert decide_status([warning, blocker]) == "BLOCKED"
