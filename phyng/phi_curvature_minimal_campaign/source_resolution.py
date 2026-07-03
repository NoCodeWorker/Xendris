"""Source reference resolution for v4.8."""

from __future__ import annotations

import re
from pathlib import Path

from phyng.phi_curvature_minimal_campaign.schemas import SourceResolutionRecord


def resolve_seed_references(root: str | Path, known_refs: list[str]) -> list[SourceResolutionRecord]:
    repo_root = Path(root)
    return [resolve_reference(repo_root, ref) for ref in known_refs]


def resolve_reference(root: Path, raw_ref: str) -> SourceResolutionRecord:
    local_identity = _find_local_identity(root, raw_ref)
    parsed = _parse_citation(raw_ref)
    if local_identity:
        return SourceResolutionRecord(
            source_ref_raw=raw_ref,
            source_id=_source_id_from_ref(raw_ref),
            title=None,
            authors=[],
            publication=parsed.get("publication"),
            year=None,
            volume=parsed.get("volume"),
            page_or_article=parsed.get("page_or_article"),
            resolution_status="RESOLVED_PROBABLE",
            confidence="LOW",
            blockers=["LOCAL_IDENTITY_HAS_CITATION_ONLY_NO_TITLE_AUTHORS_DOI"],
        )
    return SourceResolutionRecord(
        source_ref_raw=raw_ref,
        source_id=_source_id_from_ref(raw_ref),
        title=None,
        authors=[],
        publication=parsed.get("publication"),
        year=None,
        volume=parsed.get("volume"),
        page_or_article=parsed.get("page_or_article"),
        resolution_status="REQUIRES_EXTERNAL_LOOKUP",
        confidence="LOW",
        blockers=["NO_LOCAL_TITLE_AUTHORS_DOI_OR_HASHED_SOURCE_OBJECT"],
    )


def source_identity_is_extraction_ready(record: SourceResolutionRecord) -> bool:
    has_identity = bool(record.source_id and (record.title or record.source_ref_raw) and record.publication)
    has_locator = bool(record.page_or_article or record.doi or record.arxiv_id)
    return record.resolution_status in {"RESOLVED_EXACT", "RESOLVED_PROBABLE"} and has_identity and has_locator and not record.blockers


def _find_local_identity(root: Path, raw_ref: str) -> bool:
    escaped = re.escape(raw_ref)
    for directory in (
        root / "data" / "real_sources",
        root / "data" / "external_datasets",
    ):
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            match = re.search(escaped, text)
            if match:
                start = max(match.start() - 500, 0)
                end = min(match.end() + 500, len(text))
                local_window = text[start:end]
                if any(marker in local_window for marker in ("title", "doi", "authors", "source_hash", "sha256")):
                    return True
    return False


def _parse_citation(raw_ref: str) -> dict[str, str | None]:
    if raw_ref.startswith("Phys. Rev. A"):
        match = re.search(r"Phys\. Rev\. A\s+([^,]+),\s*(.+)", raw_ref)
        return {"publication": "Phys. Rev. A", "volume": match.group(1) if match else None, "page_or_article": match.group(2) if match else None}
    if raw_ref.startswith("Nature Physics"):
        match = re.search(r"Nature Physics\s+([^,]+),\s*(.+)", raw_ref)
        return {"publication": "Nature Physics", "volume": match.group(1) if match else None, "page_or_article": match.group(2) if match else None}
    return {"publication": None, "volume": None, "page_or_article": None}


def _source_id_from_ref(raw_ref: str) -> str:
    slug = re.sub(r"[^A-Z0-9]+", "-", raw_ref.upper()).strip("-")
    return f"SRC-PHI-CURVATURE-{slug}"
