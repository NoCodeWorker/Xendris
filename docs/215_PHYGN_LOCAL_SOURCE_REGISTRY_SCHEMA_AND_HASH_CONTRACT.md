# Phygn v3.6 — Local Source Registry Schema & Hash Contract

## 0. Purpose

This document defines the local source text registry.

The registry is the bridge between source metadata and exact extraction.

---

## 1. Source file registry schema

```python
class LocalSourceFileRecord(BaseModel):
    source_id: str
    canonical_filename: str
    local_path: str
    exists: bool
    file_type: str
    size_bytes: int | None
    sha256: str | None
    text_extractable: bool | None
    registry_status: str
    notes: list[str]
```

---

## 2. Registry schema

```python
class LocalSourceTextRegistry(BaseModel):
    registry_id: str
    candidate_family: str
    phi_family: str
    created_at: str
    source_records: list[LocalSourceFileRecord]
    available_count: int
    missing_count: int
    hash_count: int
    registry_status: str
```

---

## 3. Registry statuses

```txt
LOCAL_SOURCE_FILE_READY
LOCAL_SOURCE_FILE_MISSING
LOCAL_SOURCE_FILE_UNSUPPORTED_TYPE
LOCAL_SOURCE_FILE_HASHED
LOCAL_SOURCE_FILE_HASH_FAILED
LOCAL_SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD
LOCAL_SOURCE_FILE_REQUIRES_TEXT_EXTRACTION_TEST
```

---

## 4. Campaign statuses

```txt
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_CREATED
PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL
PHI_GRADIENT_LOCAL_SOURCE_FILES_READY
PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING
PHI_GRADIENT_LOCAL_SOURCE_REGISTRY_BLOCKED
```

---

## 5. Hash requirement

For every existing file:

```txt
compute sha256
record size_bytes
record file_type
record local_path
```

If hash fails:

```txt
registry_status = LOCAL_SOURCE_FILE_HASH_FAILED
```

No existing local file may be considered reproducibly registered without:

```txt
sha256
```

---

## 6. File type handling

Initial supported types:

```txt
.pdf
.txt
.md
.html
```

For `.pdf`:

```txt
text_extractable = unknown or requires extraction test
```

v3.6 does not need to extract PDF text.

It only registers the file.

---

## 7. Anti-fabrication rule

Do not create fake PDFs.

Do not mark unavailable sources as available.

Do not infer local source text from URL/arXiv/DOI metadata.

---

## 8. Final principle

```txt
Hashing is the boundary between a reference and a reproducible source object.
```
