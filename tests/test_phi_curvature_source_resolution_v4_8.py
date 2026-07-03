from pathlib import Path

from phyng.phi_curvature_minimal_campaign.source_resolution import resolve_reference, source_identity_is_extraction_ready


def test_raw_citation_is_not_source(tmp_path: Path):
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "raw_ref.md").write_text("Phys. Rev. A 102, 022101\nsha256: fake", encoding="utf-8")

    record = resolve_reference(tmp_path, "Phys. Rev. A 102, 022101")

    assert record.resolution_status == "REQUIRES_EXTERNAL_LOOKUP"
    assert source_identity_is_extraction_ready(record) is False


def test_unresolved_source_cannot_enter_extraction(tmp_path: Path):
    record = resolve_reference(tmp_path, "Nature Physics 15, 890")

    assert record.resolution_status == "REQUIRES_EXTERNAL_LOOKUP"
    assert record.blockers == ["NO_LOCAL_TITLE_AUTHORS_DOI_OR_HASHED_SOURCE_OBJECT"]


def test_generated_v48_outputs_do_not_resolve_source_identity(tmp_path: Path):
    output_dir = tmp_path / "data" / "phi_curvature" / "sources"
    output_dir.mkdir(parents=True)
    (output_dir / "phi_curvature_source_resolution_v4_8.json").write_text(
        '{"source_ref_raw":"Phys. Rev. A 102, 022101","title":null,"doi":null,"sha256":null}',
        encoding="utf-8",
    )

    record = resolve_reference(tmp_path, "Phys. Rev. A 102, 022101")

    assert record.resolution_status == "REQUIRES_EXTERNAL_LOOKUP"
