import json

from scripts.audit_benchmark_suite_excellence import (
    audit_summary_file,
    build_suite_audit,
    discover_summary_files,
    infer_report_path,
    main,
)


def _valid_summary() -> dict[str, object]:
    return {
        "metadata": {
            "dataset_hash": "a" * 64,
            "dataset_hash_algorithm": "sha256",
            "dataset_name": "Trust Traps v0.1",
            "dataset_version": "0.1",
            "execution_mode": "dry-run",
            "external_data_disclosure": "No external data sent.",
            "provider": "mock",
            "model": "deepseek-chat",
            "pricing_assumptions": "Dry-run placeholder costs.",
            "run_date": "2026-07-06",
            "temperature": 0.0,
            "max_tokens": 1024,
            "xendris_version": "0.2.0",
            "python_version": "3.11.9",
        },
        "total_samples": 100,
        "average_score_deepseek": 0.1,
        "average_score_xendris": 0.9,
        "average_delta": 0.8,
        "systems": {
            "deepseek_base": {"estimated_cost_usd": 0.01, "latency_average_ms": 100.0},
            "xendris_deepseek": {"estimated_cost_usd": 0.012, "latency_average_ms": 101.0},
        },
    }


def test_discover_summary_files(tmp_path):
    runs = tmp_path / "runs"
    runs.mkdir()
    (runs / "a_summary.json").write_text("{}", encoding="utf-8")
    (runs / "b.json").write_text("{}", encoding="utf-8")

    paths = discover_summary_files(runs)

    assert [path.name for path in paths] == ["a_summary.json"]


def test_infer_known_programming_report_path(tmp_path):
    report = infer_report_path(
        tmp_path / "deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json",
        tmp_path / "docs",
    )

    assert report is not None
    assert report.name == "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md"


def test_audit_summary_file_ready(tmp_path):
    runs = tmp_path / "runs"
    docs = tmp_path / "docs"
    runs.mkdir()
    docs.mkdir()
    summary = runs / "deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json"
    report = docs / "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md"
    summary.write_text(json.dumps(_valid_summary()), encoding="utf-8")
    report.write_text("No Universal Superiority Warning\nCost\nLatency\nLimitations\n", encoding="utf-8")

    record = audit_summary_file(summary, docs)

    assert record["decision"] == "READY_FOR_INTERPRETATION"
    assert record["has_blockers"] is False
    assert record["report_path"] == str(report)


def test_build_suite_audit_counts_ready_and_blocked():
    payload = build_suite_audit(
        [
            {"decision": "READY_FOR_INTERPRETATION", "has_blockers": False, "issues": []},
            {"decision": "BLOCKED_FOR_INTERPRETATION", "has_blockers": True, "issues": []},
        ]
    )

    assert payload["summary_count"] == 2
    assert payload["ready_count"] == 1
    assert payload["blocked_count"] == 1


def test_cli_writes_audit_outputs(tmp_path):
    runs = tmp_path / "runs"
    docs = tmp_path / "docs"
    output_json = tmp_path / "audit.json"
    output_md = tmp_path / "audit.md"
    runs.mkdir()
    docs.mkdir()
    (runs / "deepseek_vs_xendris_programming_reliability_v0_1_2026_07_04_summary.json").write_text(
        json.dumps(_valid_summary()),
        encoding="utf-8",
    )
    (docs / "RUN_DEEPSEEK_VS_XENDRIS_PROGRAMMING_RELIABILITY_V0_1_2026_07_04.md").write_text(
        "No Universal Superiority Warning\nCost\nLatency\nLimitations\n",
        encoding="utf-8",
    )

    exit_code = main(
        [
            "--runs-dir",
            str(runs),
            "--docs-dir",
            str(docs),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
        ]
    )
    payload = json.loads(output_json.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert output_md.exists()
    assert payload["ready_count"] == 1


def test_cli_can_fail_on_blockers(tmp_path):
    runs = tmp_path / "runs"
    docs = tmp_path / "docs"
    output_json = tmp_path / "audit.json"
    output_md = tmp_path / "audit.md"
    runs.mkdir()
    docs.mkdir()
    (runs / "bad_summary.json").write_text(json.dumps({"metadata": {}}), encoding="utf-8")

    exit_code = main(
        [
            "--runs-dir",
            str(runs),
            "--docs-dir",
            str(docs),
            "--output-json",
            str(output_json),
            "--output-md",
            str(output_md),
            "--fail-on-blockers",
        ]
    )

    assert exit_code == 1
