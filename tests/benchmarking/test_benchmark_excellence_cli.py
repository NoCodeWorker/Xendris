import json

from scripts.validate_benchmark_excellence import main


def _summary_payload() -> dict[str, object]:
    return {
        "metadata": {
            "dataset_hash": "a" * 64,
            "dataset_hash_algorithm": "sha256",
            "dataset_name": "Trust Traps v0.1",
            "dataset_version": "0.1",
            "execution_mode": "dry-run",
            "external_data_disclosure": "No external data sent.",
            "model": "deepseek-chat",
            "pricing_assumptions": "Dry-run placeholder costs.",
            "provider": "mock",
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


def test_cli_writes_ready_assessment(tmp_path):
    summary_path = tmp_path / "summary.json"
    report_path = tmp_path / "report.md"
    output_path = tmp_path / "assessment.json"
    summary_path.write_text(json.dumps(_summary_payload()), encoding="utf-8")
    report_path.write_text(
        "No Universal Superiority Warning\nCost\nLatency\nLimitations\n",
        encoding="utf-8",
    )

    exit_code = main([str(summary_path), "--report", str(report_path), "--output", str(output_path)])
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert payload["decision"] == "READY_FOR_INTERPRETATION"
    assert payload["has_blockers"] is False


def test_cli_blocks_incomplete_summary(tmp_path):
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps({"metadata": {}, "total_samples": 1}), encoding="utf-8")

    exit_code = main([str(summary_path)])

    assert exit_code == 1


def test_cli_allow_blockers_keeps_decision_but_returns_zero(tmp_path):
    summary_path = tmp_path / "summary.json"
    output_path = tmp_path / "assessment.json"
    summary_path.write_text(json.dumps({"metadata": {}, "total_samples": 1}), encoding="utf-8")

    exit_code = main([str(summary_path), "--allow-blockers", "--output", str(output_path)])
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert payload["decision"] == "BLOCKED_FOR_INTERPRETATION"
    assert payload["has_blockers"] is True
