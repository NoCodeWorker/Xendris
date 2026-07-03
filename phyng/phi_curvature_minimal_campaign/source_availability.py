"""Local source availability checks for v4.8."""

from __future__ import annotations

import hashlib
from pathlib import Path

from phyng.phi_curvature_minimal_campaign.schemas import SourceAvailabilityRecord, SourceResolutionRecord


def assess_source_availability(root: str | Path, resolutions: list[SourceResolutionRecord]) -> list[SourceAvailabilityRecord]:
    repo_root = Path(root)
    return [availability_for_source(repo_root, record) for record in resolutions]


def availability_for_source(root: Path, record: SourceResolutionRecord) -> SourceAvailabilityRecord:
    if record.resolution_status not in {"RESOLVED_EXACT", "RESOLVED_PROBABLE"}:
        return SourceAvailabilityRecord(
            source_id=record.source_id or "UNRESOLVED_SOURCE",
            availability_status="SOURCE_REQUIRES_HUMAN_LOOKUP",
            required_next_action="Resolve source title/authors/DOI and download local PDF or dataset.",
        )
    pdf = _find_pdf(root, record)
    supplementary = _find_related_files(root / "data/real_sources/supplementary", record)
    datasets = _find_related_files(root / "data/external_datasets", record)
    if pdf:
        return SourceAvailabilityRecord(
            source_id=record.source_id or "UNKNOWN_SOURCE",
            local_pdf_available=True,
            local_pdf_path=pdf.relative_to(root).as_posix(),
            local_pdf_hash=_sha256(pdf),
            supplementary_available=bool(supplementary),
            supplementary_paths=[path.relative_to(root).as_posix() for path in supplementary],
            external_dataset_available=bool(datasets),
            external_dataset_paths=[path.relative_to(root).as_posix() for path in datasets],
            availability_status="LOCAL_PDF_AVAILABLE",
            required_next_action="Run manual table/figure extraction with exact page/table/figure locations.",
        )
    return SourceAvailabilityRecord(
        source_id=record.source_id or "UNKNOWN_SOURCE",
        supplementary_available=bool(supplementary),
        supplementary_paths=[path.relative_to(root).as_posix() for path in supplementary],
        external_dataset_available=bool(datasets),
        external_dataset_paths=[path.relative_to(root).as_posix() for path in datasets],
        availability_status="SOURCE_REQUIRES_DOWNLOAD" if record.resolution_status.startswith("RESOLVED") else "SOURCE_UNRESOLVED",
        required_next_action="Download exact source PDF or locate supplementary/public dataset.",
    )


def _find_pdf(root: Path, record: SourceResolutionRecord) -> Path | None:
    pdf_dir = root / "data/real_sources/pdfs"
    if not pdf_dir.exists():
        return None
    tokens = [token for token in (record.publication, record.volume, record.page_or_article) if token]
    for path in pdf_dir.glob("*.pdf"):
        name = path.name.lower()
        if record.source_id and record.source_id.lower().replace("src-phi-curvature-", "").replace("-", "_") in name:
            return path
        if tokens and all(str(token).lower().replace(" ", "_").replace(".", "") in name.replace(".", "") for token in tokens[:1]):
            return path
    return None


def _find_related_files(directory: Path, record: SourceResolutionRecord) -> list[Path]:
    if not directory.exists():
        return []
    tokens = [str(token).lower().replace(" ", "_").replace(".", "") for token in (record.volume, record.page_or_article) if token]
    matches: list[Path] = []
    for path in directory.rglob("*"):
        if path.is_file() and tokens and any(token in path.name.lower().replace(".", "") for token in tokens):
            matches.append(path)
    return matches


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
