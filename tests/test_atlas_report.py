from pathlib import Path

from phyng.atlas.atlas_builder import build_atlas
from phyng.atlas.atlas_report import generate_atlas_report
from phyng.atlas.schemas import AtlasThresholds, PhysicalSystemSpec


def test_atlas_report_generates_required_artifacts(tmp_path: Path):
    spec = PhysicalSystemSpec(
        system_id="SYS-REPORT-MESO",
        label="Report mesoscopic point",
        description="Mesoscopic point for report artifact validation",
        m_kg=1e-17,
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="interferometric path separation",
        observer_channel="matter-wave interference readout",
        justification="Within configured mesoscopic range",
        allowed_range_m=(1e-8, 1e-6),
        arbitrariness_risk="LOW",
    )

    atlas = build_atlas([spec], AtlasThresholds())
    report_path = generate_atlas_report(atlas, tmp_path)
    atlas_dir = tmp_path / "reports" / "atlas"

    assert report_path == atlas_dir / "invariant_boundary_atlas.md"
    assert report_path.exists()
    assert (atlas_dir / "atlas_points.json").exists()
    assert (atlas_dir / "claim_exclusion_matrix.md").exists()

    report = report_path.read_text(encoding="utf-8")
    matrix = (atlas_dir / "claim_exclusion_matrix.md").read_text(encoding="utf-8")

    assert "QB = \\left(\\frac{\\ell_P}{L}\\right)^2" in report
    assert "SYS-REPORT-MESO" in report
    assert "NEGATIVE_GRAVITY_BOUND" in matrix
