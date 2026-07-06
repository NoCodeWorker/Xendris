import json

from scripts.build_benchmark_evidence_registry import main
from xendris.benchmarking import (
    build_benchmark_evidence_registry,
    render_benchmark_evidence_registry_markdown,
)


def _audit_payload() -> dict[str, object]:
    return {
        "records": [
            {
                "summary_path": "runs/ready_summary.json",
                "report_path": "docs/ready.md",
                "decision": "READY_FOR_INTERPRETATION",
                "has_blockers": False,
                "blocker_count": 0,
                "warning_count": 0,
                "issues": [],
            },
            {
                "summary_path": "runs/blocked_summary.json",
                "report_path": "docs/blocked.md",
                "decision": "BLOCKED_FOR_INTERPRETATION",
                "has_blockers": True,
                "blocker_count": 1,
                "warning_count": 2,
                "issues": [
                    {
                        "code": "missing_dataset_hash",
                        "severity": "BLOCKER",
                        "message": "Dataset hash is required.",
                    }
                ],
            },
        ]
    }


def test_registry_admits_only_ready_artifacts():
    registry = build_benchmark_evidence_registry(_audit_payload())

    assert registry.total_count == 2
    assert registry.admitted_count == 1
    assert registry.rejected_count == 1
    assert registry.admitted[0].summary_path == "runs/ready_summary.json"
    assert registry.rejected[0].reason == "missing_dataset_hash"


def test_registry_to_dict_is_json_ready():
    payload = build_benchmark_evidence_registry(_audit_payload()).to_dict()

    assert payload["admitted_count"] == 1
    assert payload["rejected_count"] == 1
    assert payload["admitted"][0]["status"] == "ADMITTED"
    assert payload["rejected"][0]["status"] == "REJECTED"


def test_registry_markdown_states_admitted_and_rejected():
    markdown = render_benchmark_evidence_registry_markdown(
        build_benchmark_evidence_registry(_audit_payload())
    )

    assert "Benchmark Evidence Registry" in markdown
    assert "runs/ready_summary.json" in markdown
    assert "runs/blocked_summary.json" in markdown
    assert "missing_dataset_hash" in markdown


def test_cli_builds_registry_outputs(tmp_path):
    audit = tmp_path / "audit.json"
    output_json = tmp_path / "registry.json"
    output_md = tmp_path / "registry.md"
    audit.write_text(json.dumps(_audit_payload()), encoding="utf-8")

    exit_code = main(
        [
            "--audit-json",
            str(audit),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--require-admitted",
        ]
    )
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_md.exists()
    assert payload["admitted_count"] == 1


def test_cli_can_fail_when_no_artifacts_are_admitted(tmp_path):
    audit = tmp_path / "audit.json"
    output_json = tmp_path / "registry.json"
    output_md = tmp_path / "registry.md"
    audit.write_text(
        json.dumps({"records": [{**_audit_payload()["records"][1]}]}),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--audit-json",
            str(audit),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--require-admitted",
        ]
    )

    assert exit_code == 1
