from pathlib import Path

from phyng.campaigns.phi_gradient_real_literature_ingestion import run_phi_gradient_real_literature_ingestion_campaign


def test_reports_include_fixture_separation(tmp_path):
    result = run_phi_gradient_real_literature_ingestion_campaign(tmp_path)
    manifest_text = Path(result.report_paths["manifest"]).read_text(encoding="utf-8")

    assert "FIXTURE_ONLY_DOES_NOT_COUNT_AS_REAL_SUPPORT" in manifest_text
    assert "TEST_DOUBLE_REAL_SOURCE_FORMAT" in manifest_text


def test_reports_include_canonical_section(tmp_path):
    result = run_phi_gradient_real_literature_ingestion_campaign(tmp_path)

    for path in result.report_paths.values():
        text = Path(path).read_text(encoding="utf-8")
        assert "## Canonical Status" in text
        assert "Only experiments can raise physical truth" in text
