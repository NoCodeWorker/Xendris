from pathlib import Path

from phyng.phi_curvature_minimal_campaign.schemas import SourceResolutionRecord
from phyng.phi_curvature_minimal_campaign.source_availability import availability_for_source


def test_missing_local_pdf_requires_download(tmp_path: Path):
    record = SourceResolutionRecord(
        source_ref_raw="Phys. Rev. A 102, 022101",
        source_id="SRC-PHI-CURVATURE-PHYS-REV-A-102-022101",
        publication="Phys. Rev. A",
        volume="102",
        page_or_article="022101",
        resolution_status="RESOLVED_EXACT",
        confidence="HIGH",
    )

    availability = availability_for_source(tmp_path, record)

    assert availability.availability_status == "SOURCE_REQUIRES_DOWNLOAD"
    assert availability.local_pdf_available is False
    assert availability.local_pdf_hash is None
