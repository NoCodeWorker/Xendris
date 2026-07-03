"""Source pool construction for v5.7."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.dataset_expansion.schemas import SourcePoolRecord


TARGET_SOURCE_IDS = {
    "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE",
    "SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE",
    "SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST",
    "SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS",
    "SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING",
}


def build_source_pool(root: str | Path = ".") -> list[SourcePoolRecord]:
    root = Path(root)
    identities = json.loads((root / "data/preflight/source_identity/source_identity_resolution_integrated_v5_1.json").read_text(encoding="utf-8"))
    hashes = json.loads((root / "data/real_sources/source_hashes_v3_6.json").read_text(encoding="utf-8")).get("hashes", [])
    hash_by_source = {item["source_id"]: item for item in hashes}
    records: list[SourcePoolRecord] = []
    for item in identities.get("records", []):
        source_id = item.get("source_id")
        if source_id not in TARGET_SOURCE_IDS:
            continue
        hash_record = hash_by_source.get(source_id, {})
        local_path = item.get("local_pdf_path")
        local_available = bool(local_path and (root / local_path).exists() and hash_record.get("sha256"))
        records.append(
            SourcePoolRecord(
                source_id=source_id,
                title=item.get("title") or source_id,
                year=item.get("publication_year"),
                authority=item.get("publication_authority"),
                external_identity=item.get("doi") or item.get("arxiv_id") or item.get("url"),
                local_pdf_path=local_path,
                local_pdf_hash=hash_record.get("sha256") or item.get("sha256"),
                source_status="LOCAL_AVAILABLE" if local_available else "REQUIRES_DOWNLOAD",
                candidate_relevance=["visibility/decoherence source pool"],
                observable_targets=["VISIBILITY", "FRINGE_VISIBILITY", "INTERFERENCE_CONTRAST", "DECOHERENCE_RATE"],
                notes=[] if local_available else ["Local source object is not hashable/available."],
            )
        )
    return records
