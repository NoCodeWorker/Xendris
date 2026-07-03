"""Source identity resolution matrix for v4.9."""

from __future__ import annotations

import re
import hashlib
from pathlib import Path

from phyng.source_identity_preflight.schemas import CandidateFamilySourceInventory, SourceIdentityResolutionRecord


def build_source_identity_resolution_matrix(inventory: list[CandidateFamilySourceInventory], root: str | Path = ".") -> list[SourceIdentityResolutionRecord]:
    repo_root = Path(root)
    matrix: list[SourceIdentityResolutionRecord] = []
    for item in inventory:
        refs = item.raw_source_refs or item.local_pdf_refs or [""]
        for raw_ref in refs:
            matrix.append(resolve_inventory_ref(item.family_id, raw_ref, repo_root))
    return matrix


def resolve_inventory_ref(family_id: str, raw_ref: str, root: str | Path = ".") -> SourceIdentityResolutionRecord:
    repo_root = Path(root)
    source_id = _source_id(family_id, raw_ref)
    publication, year = _publication_year(raw_ref)
    local_hash = _hash_from_local_ref(raw_ref, repo_root)
    identity_complete = _identity_complete(
        source_id=source_id,
        raw_ref=raw_ref,
        publication=publication,
        year=year,
        doi=None,
        arxiv_id=None,
        url=None,
        local_hash=local_hash,
    )
    if identity_complete and local_hash:
        status = "RESOLVED_LOCAL"
        blockers: list[str] = []
    elif identity_complete:
        status = "RESOLVED_EXTERNAL_IDENTITY"
        blockers = []
    elif raw_ref:
        status = "RAW_REF_ONLY" if publication else "REQUIRES_HUMAN_LOOKUP"
        blockers = ["IDENTITY_REQUIRES_DOI_ARXIV_URL_OR_LOCAL_HASH", "IDENTITY_REQUIRES_PUBLICATION_YEAR"]
        if local_hash:
            blockers = ["LOCAL_FILE_HASHED_BUT_IDENTITY_REQUIRES_PUBLICATION_AUTHORITY"]
    else:
        status = "UNRESOLVED"
        blockers = ["NO_SOURCE_REFS"]
    return SourceIdentityResolutionRecord(
        family_id=family_id,
        source_ref_raw=raw_ref,
        source_id=source_id if raw_ref else None,
        publication=publication,
        year=year,
        local_hash=local_hash,
        resolution_status=status,
        confidence="LOW" if not identity_complete else "MEDIUM",
        identity_complete=identity_complete,
        blockers=blockers,
    )


def _identity_complete(
    *,
    source_id: str | None,
    raw_ref: str,
    publication: str | None,
    year: int | None,
    doi: str | None,
    arxiv_id: str | None,
    url: str | None,
    local_hash: str | None,
) -> bool:
    has_identity_name = bool(raw_ref)
    has_locator = bool(doi or arxiv_id or url or local_hash)
    has_publication_authority = bool(publication and publication != "LOCAL_PDF_FILENAME")
    return bool(source_id and has_identity_name and has_publication_authority and year and has_locator)


def _source_id(family_id: str, raw_ref: str) -> str | None:
    if not raw_ref:
        return None
    slug = re.sub(r"[^A-Z0-9]+", "-", raw_ref.upper()).strip("-")
    return f"SRC-PREFLIGHT-{family_id}-{slug[:80]}"


def _publication_year(raw_ref: str) -> tuple[str | None, int | None]:
    if raw_ref.startswith("Phys. Rev. A"):
        return "Phys. Rev. A", None
    if raw_ref.startswith("Nature Physics"):
        return "Nature Physics", None
    if raw_ref.lower().endswith(".pdf"):
        year_match = re.search(r"(19|20)\d{2}", raw_ref)
        return "LOCAL_PDF_FILENAME", int(year_match.group(0)) if year_match else None
    return None, None


def _hash_from_local_ref(raw_ref: str, root: Path) -> str | None:
    if not raw_ref.lower().endswith(".pdf"):
        return None
    path = Path(raw_ref)
    if not path.is_absolute():
        path = root / raw_ref
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
    return None
