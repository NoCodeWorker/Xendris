"""Source availability matrix for v4.9."""

from __future__ import annotations

from phyng.source_identity_preflight.schemas import SourceAvailabilityMatrixRecord, SourceIdentityResolutionRecord


def build_source_availability_matrix(identity_matrix: list[SourceIdentityResolutionRecord]) -> list[SourceAvailabilityMatrixRecord]:
    return [availability_for_identity(record) for record in identity_matrix]


def availability_for_identity(record: SourceIdentityResolutionRecord) -> SourceAvailabilityMatrixRecord:
    if not record.identity_complete:
        return SourceAvailabilityMatrixRecord(
            family_id=record.family_id,
            source_id=record.source_id,
            identity_complete=False,
            local_pdf_available=bool(record.local_hash),
            local_pdf_path=record.source_ref_raw if record.local_hash else None,
            local_pdf_hash=record.local_hash,
            availability_status="IDENTITY_INCOMPLETE",
            required_next_action="Resolve title/publication year and DOI/arXiv/URL/local hash before availability can pass.",
        )
    if record.local_hash:
        return SourceAvailabilityMatrixRecord(
            family_id=record.family_id,
            source_id=record.source_id,
            identity_complete=True,
            local_pdf_available=True,
            local_pdf_hash=record.local_hash,
            availability_status="AVAILABLE_LOCAL_PDF",
            required_next_action="Proceed only to exact source-location review.",
        )
    return SourceAvailabilityMatrixRecord(
        family_id=record.family_id,
        source_id=record.source_id,
        identity_complete=True,
        availability_status="IDENTITY_ONLY_REQUIRES_DOWNLOAD",
        required_next_action="Download or register the exact source object before extraction.",
    )
