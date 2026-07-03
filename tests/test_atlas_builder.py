import tempfile
from pathlib import Path
from phyng.atlas.schemas import PhysicalSystemSpec, AtlasThresholds
from phyng.atlas.atlas_builder import build_atlas
from phyng.atlas.atlas_report import generate_atlas_report


def test_atlas_builder_and_reporting():
    spec = PhysicalSystemSpec(
        system_id="SYS-ATLAS",
        label="Nanoparticle spec",
        description="Mesoscopic interferometer nanoparticle spec",
        m_kg=1e-17,
        L_value_m=1e-7,
        L_type="L_INT",
        physical_role="separation",
        observer_channel="readout",
        justification="Verified range",
        allowed_range_m=(1e-8, 1e-6),
        arbitrariness_risk="LOW"
    )
    
    thresholds = AtlasThresholds()
    atlas = build_atlas([spec], thresholds)
    
    assert len(atlas.points) == 1
    assert atlas.points[0].system_id == "SYS-ATLAS"
    
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        report_path = generate_atlas_report(atlas, tmp_path)
        
        # Verify files exist
        assert report_path.exists()
        assert (tmp_path / "reports" / "atlas" / "atlas_points.json").exists()
        assert (tmp_path / "reports" / "atlas" / "claim_exclusion_matrix.md").exists()
