import json

from scripts.check_benchmark_evidence_citations import (
    check_rejected_artifact_citations,
    load_rejected_artifacts,
    main,
)


def _write_registry(path):
    path.write_text(
        json.dumps(
            {
                "admitted": [
                    {
                        "summary_path": "runs/ready_summary.json",
                        "report_path": "docs/benchmarks/READY.md",
                        "status": "ADMITTED",
                    }
                ],
                "rejected": [
                    {
                        "summary_path": "runs/bad_summary.json",
                        "report_path": "docs/benchmarks/BAD.md",
                        "status": "REJECTED",
                        "reason": "missing_dataset_hash",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_load_rejected_artifacts(tmp_path):
    registry = tmp_path / "registry.json"
    _write_registry(registry)

    rejected = load_rejected_artifacts(registry)

    assert len(rejected) == 1
    assert rejected[0].summary_path == "runs/bad_summary.json"
    assert rejected[0].report_path == "docs/benchmarks/BAD.md"


def test_checker_blocks_public_evidence_reference_to_rejected_summary(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    _write_registry(registry)
    (docs / "report.md").write_text(
        "This benchmark evidence uses runs/bad_summary.json as support.\n",
        encoding="utf-8",
    )

    violations = check_rejected_artifact_citations(load_rejected_artifacts(registry), docs)

    assert len(violations) == 1
    assert violations[0].artifact_path == "runs/bad_summary.json"


def test_checker_allows_rejected_artifact_section(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    _write_registry(registry)
    (docs / "registry.md").write_text(
        "## Rejected Artifacts\n\n"
        "- `runs/bad_summary.json` is rejected because metadata is incomplete.\n",
        encoding="utf-8",
    )

    violations = check_rejected_artifact_citations(load_rejected_artifacts(registry), docs)

    assert violations == []


def test_checker_allows_historical_blocked_context(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    _write_registry(registry)
    (docs / "history.md").write_text(
        "## Historical blocked runs\n\n"
        "The older docs/benchmarks/BAD.md report is blocked and not admitted as evidence.\n",
        encoding="utf-8",
    )

    violations = check_rejected_artifact_citations(load_rejected_artifacts(registry), docs)

    assert violations == []


def test_checker_ignores_admitted_artifacts(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    _write_registry(registry)
    (docs / "report.md").write_text(
        "Current evidence uses runs/ready_summary.json.\n",
        encoding="utf-8",
    )

    violations = check_rejected_artifact_citations(load_rejected_artifacts(registry), docs)

    assert violations == []


def test_cli_returns_nonzero_when_violations_exist(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    docs.mkdir()
    _write_registry(registry)
    (docs / "report.md").write_text(
        "Evidence path: runs/bad_summary.json.\n",
        encoding="utf-8",
    )

    exit_code = main(["--registry", str(registry), "--docs-dir", str(docs)])

    assert exit_code == 1


def test_cli_writes_json_and_passes_when_only_rejected_section_cites_artifact(tmp_path):
    registry = tmp_path / "registry.json"
    docs = tmp_path / "docs"
    output = tmp_path / "citations.json"
    docs.mkdir()
    _write_registry(registry)
    (docs / "registry.md").write_text(
        "## Rejected Artifacts\n\n"
        "`runs/bad_summary.json` remains rejected.\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--registry",
            str(registry),
            "--docs-dir",
            str(docs),
            "--output-json",
            str(output),
        ]
    )
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert payload["violation_count"] == 0
