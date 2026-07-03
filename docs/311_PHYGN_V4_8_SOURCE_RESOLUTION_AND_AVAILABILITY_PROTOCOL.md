# Phygn v4.8 — Source Resolution & Availability Protocol

## 0. Purpose

This document defines how promising PHI_CURVATURE references become resolvable source objects.

---

## 1. Source resolution

Create:

```txt
data/phi_curvature/sources/phi_curvature_source_resolution_v4_8.json
```

Schema:

```python
class SourceResolutionRecord(BaseModel):
    source_ref_raw: str
    source_id: str | None
    title: str | None
    authors: list[str]
    publication: str | None
    year: int | None
    volume: str | None
    page_or_article: str | None
    doi: str | None
    arxiv_id: str | None
    url: str | None
    resolution_status: str
    confidence: str
    blockers: list[str]
```

Resolution statuses:

```txt
RESOLVED_EXACT
RESOLVED_PROBABLE
AMBIGUOUS
UNRESOLVED
REQUIRES_EXTERNAL_LOOKUP
```

Hard rule:

```txt
A raw citation string is not a source.
```

---

## 2. Required seed references

At minimum resolve or reject:

```txt
Phys. Rev. A 102, 022101
Nature Physics 15, 890
```

If exact identity cannot be resolved locally:

```txt
resolution_status = REQUIRES_EXTERNAL_LOOKUP
```

Do not fabricate title, authors, DOI or URL.

---

## 3. Source availability

Create:

```txt
data/phi_curvature/sources/phi_curvature_source_availability_v4_8.json
```

Schema:

```python
class SourceAvailabilityRecord(BaseModel):
    source_id: str
    local_pdf_available: bool
    local_pdf_path: str | None
    local_pdf_hash: str | None
    supplementary_available: bool
    supplementary_paths: list[str]
    external_dataset_available: bool
    external_dataset_paths: list[str]
    availability_status: str
    required_next_action: str
```

Availability statuses:

```txt
LOCAL_PDF_AVAILABLE
SUPPLEMENTARY_AVAILABLE
EXTERNAL_DATASET_AVAILABLE
SOURCE_KNOWN_BUT_NOT_LOCAL
SOURCE_UNRESOLVED
SOURCE_REQUIRES_DOWNLOAD
SOURCE_REQUIRES_HUMAN_LOOKUP
```

---

## 4. Source identity minimum

A source may enter evidence extraction only if it has at least:

```txt
source_id
title or exact citation identity
publication/year
article/page/DOI/arXiv or local PDF hash
```

Otherwise:

```txt
SOURCE_NOT_EXTRACTION_READY
```

---

## 5. Final principle

```txt
A source is evidence-capable only after it has identity and location.
```
