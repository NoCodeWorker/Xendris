"""Build v5.7.2 source download manifests from v5.7.1 queue artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from phyng.source_download.failures import classify_missing_source
from phyng.source_download.hashing import is_pdf_object, modified_time_utc, sha256_file
from phyng.source_download.schemas import (
    SourceDownloadFailureRecord,
    SourceDownloadManifestRecord,
    SourceHashRegistryUpdateRecord,
)


def build_source_download_records(root: str | Path = ".") -> tuple[list[SourceDownloadManifestRecord], list[SourceHashRegistryUpdateRecord], list[SourceDownloadFailureRecord]]:
    repo_root = Path(root)
    identity_records = _load_records(repo_root / "data/frontera_c/source_acquisition/visibility_decoherence_candidate_source_identity_matrix_v5_7_1.json")
    download_records = _load_records(repo_root / "data/frontera_c/source_acquisition/visibility_decoherence_download_priority_queue_v5_7_1.json")
    previous_hashes = _load_previous_hashes(repo_root / "data/real_sources/source_hashes_v3_6.json")
    identity_by_id = {item["source_candidate_id"]: item for item in identity_records}

    manifest: list[SourceDownloadManifestRecord] = []
    hashes: list[SourceHashRegistryUpdateRecord] = []
    failures: list[SourceDownloadFailureRecord] = []
    for download in download_records:
        source_candidate_id = download["source_candidate_id"]
        identity = identity_by_id.get(source_candidate_id, {})
        local_rel = download.get("target_local_path")
        local_path = repo_root / local_rel if local_rel else None
        exists = bool(local_path and local_path.exists())
        verified = bool(local_path and is_pdf_object(local_path))
        source_id = source_candidate_id
        previous_hash = previous_hashes.get(source_id)
        sha256 = sha256_file(local_path) if verified and local_path else None
        size = local_path.stat().st_size if verified and local_path else None
        mtime = modified_time_utc(local_path) if verified and local_path else None
        identity_complete = bool(identity.get("identity_complete"))
        status = _download_status(download, verified, exists)
        notes = ["Downloaded or existing bytes are not evidence and do not create y_true."]
        if exists and not verified:
            notes.append("Local target exists but is not a verified PDF source object.")
        if verified:
            notes.append("Local PDF bytes verified and SHA256 computed.")
        manifest.append(
            SourceDownloadManifestRecord(
                source_candidate_id=source_candidate_id,
                source_id=source_id,
                title=identity.get("title") or source_candidate_id,
                authors=identity.get("authors") or [],
                year=identity.get("year"),
                external_identity=_external_identity(identity),
                preferred_url=download.get("preferred_url"),
                expected_filename=download.get("expected_filename"),
                local_pdf_path=local_rel if exists else None,
                local_pdf_hash=sha256,
                download_status=status,
                file_verified=verified and identity_complete,
                source_identity_complete=identity_complete,
                notes=notes,
            )
        )
        hashes.append(
            SourceHashRegistryUpdateRecord(
                source_id=source_id,
                local_pdf_path=local_rel if verified else None,
                sha256=sha256,
                file_size_bytes=size,
                modified_time_utc=mtime,
                hash_status=_hash_status(verified, previous_hash, sha256),
                previous_hash_if_any=previous_hash,
            )
        )
        if not (verified and identity_complete):
            reason = classify_missing_source(
                bool(download.get("requires_paywall_access")),
                bool(download.get("requires_supplementary_download")),
                exists,
            )
            failures.append(
                SourceDownloadFailureRecord(
                    source_candidate_id=source_candidate_id,
                    title=identity.get("title") or source_candidate_id,
                    preferred_url=download.get("preferred_url"),
                    doi_or_arxiv=identity.get("doi") or identity.get("arxiv") or identity.get("url"),
                    expected_filename=download.get("expected_filename"),
                    target_local_path=local_rel,
                    reason=reason,
                    priority=download.get("download_priority", "MEDIUM"),
                    required_next_action=_next_action(reason),
                )
            )
    return manifest, hashes, failures


def _load_records(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("records", []))


def _load_previous_hashes(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    previous = {}
    for item in records:
        source_id = item.get("source_id")
        sha = item.get("sha256")
        if source_id and sha:
            previous[source_id] = sha
    return previous


def _external_identity(identity: dict) -> str | None:
    return identity.get("doi") or identity.get("arxiv") or identity.get("url")


def _download_status(download: dict, verified: bool, exists: bool) -> str:
    if verified:
        return "LOCAL_AVAILABLE"
    if exists:
        return "REJECTED_NOT_SOURCE_OBJECT"
    if download.get("requires_paywall_access"):
        return "REQUIRES_PAYWALL_ACCESS"
    if download.get("requires_supplementary_download"):
        return "REQUIRES_SUPPLEMENTARY_DOWNLOAD"
    return "REQUIRES_MANUAL_DOWNLOAD"


def _hash_status(verified: bool, previous_hash: str | None, sha256: str | None) -> str:
    if not verified:
        return "NO_LOCAL_FILE"
    if previous_hash and previous_hash != sha256:
        return "HASH_MISMATCH"
    if previous_hash:
        return "HASHED_EXISTING"
    return "HASHED_NEW"


def _next_action(reason: str) -> str:
    if reason == "PAYWALL":
        return "Acquire source object through legitimate library or publisher access."
    if reason == "SUPPLEMENTARY_REQUIRED":
        return "Manually verify source PDF and any required supplementary material."
    if reason == "REJECTED_NOT_SOURCE_OBJECT":
        return "Replace target path with a valid PDF source object."
    return "Download the expected source PDF to the target local path."
