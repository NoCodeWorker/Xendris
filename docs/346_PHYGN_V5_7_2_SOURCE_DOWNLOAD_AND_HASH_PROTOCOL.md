# Phygn v5.7.2 — Source Download & Hash Protocol

## 0. Purpose

This document defines source download, local availability, SHA256 hashing and manifest update rules.

---

## 1. Source download manifest

Create:

```txt
data/frontera_c/source_download/source_download_manifest_v5_7_2.json
```

Schema:

```python
class SourceDownloadManifestRecord(BaseModel):
    source_candidate_id: str
    source_id: str | None
    title: str
    authors: list[str]
    year: int | None
    external_identity: str | None
    preferred_url: str | None
    expected_filename: str | None
    local_pdf_path: str | None
    local_pdf_hash: str | None
    download_status: str
    file_verified: bool
    source_identity_complete: bool
    notes: list[str]
```

Download statuses:

```txt
LOCAL_AVAILABLE
DOWNLOADED_AND_HASHED
REQUIRES_MANUAL_DOWNLOAD
REQUIRES_PAYWALL_ACCESS
REQUIRES_SUPPLEMENTARY_DOWNLOAD
FAILED_NOT_FOUND
REJECTED_NOT_SOURCE_OBJECT
```

---

## 2. Hash registry update

Create:

```txt
data/frontera_c/source_download/source_hash_registry_update_v5_7_2.json
```

Fields:

```txt
source_id
local_pdf_path
sha256
file_size_bytes
modified_time_utc
hash_status
previous_hash_if_any
```

Hash statuses:

```txt
HASHED_NEW
HASHED_EXISTING
HASH_MISMATCH
NO_LOCAL_FILE
```

---

## 3. Download failures

Create:

```txt
data/frontera_c/source_download/source_download_failures_v5_7_2.json
```

Failure reasons:

```txt
MISSING_LOCAL_FILE
PAYWALL
URL_UNAVAILABLE
PDF_NOT_FOUND
SUPPLEMENTARY_REQUIRED
AMBIGUOUS_SOURCE_IDENTITY
MANUAL_DOWNLOAD_REQUIRED
```

---

## 4. Manual download rule

If the system cannot download a file automatically or the file is not present locally, it must not fabricate the file.

It must create an actionable manual-download entry with:

```txt
source_candidate_id
title
preferred_url
doi_or_arxiv
expected_filename
target_local_path
reason
priority
```

---

## 5. Local object verification

A source object is verified only if:

```txt
local_pdf_path exists
sha256 computed
source identity complete
file is non-empty
```

---

## 6. Final principle

```txt
A citation becomes a source object only when identity and bytes meet.
```
