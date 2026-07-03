from phyng.campaigns.log_boundary_synthetic_execution import run_log_boundary_synthetic_execution_campaign


def test_reports_include_canonical_section(tmp_path):
    result = run_log_boundary_synthetic_execution_campaign(tmp_path)

    for path in result.report_paths.values():
        text = (tmp_path / path).read_text(encoding="utf-8") if not str(path).startswith(str(tmp_path)) else None
        if text is None:
            from pathlib import Path

            text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "Synthetic signal may update search priority" in text
        assert "Physical" in text or "physical" in text
