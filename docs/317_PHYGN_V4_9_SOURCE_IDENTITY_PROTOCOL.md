# Phygn v4.9 — Source Identity Protocol

## 0. Purpose

This document defines source identity resolution for candidate preflight.

---

## 1. Candidate family source inventory

Create:

```txt
data/preflight/source_identity/candidate_family_source_inventory_v4_9.json
```

Schema:

```python
class CandidateFamilySourceInventory(BaseModel):
    family_id: str
    previous_status: str | None
    raw_source_refs: list[str]
    known_resolved_sources: list[str]
    local_pdf_refs: list[str]
    supplementary_refs: list[str]
    dataset_refs: list[str]
    inventory_status: str
    notes: list[str]
```

Inventory statuses:

```txt
HAS_RESOLVED_SOURCES
HAS_RAW_REFS_ONLY
HAS_LOCAL_ARTIFACTS
NO_SOURCE_REFS
REQUIRES_HUMAN_LOOKUP
```

---

## 2. Source identity resolution matrix

Create:

```txt
data/preflight/source_identity/source_identity_resolution_matrix_v4_9.json
```

Schema:

```python
class SourceIdentityResolutionRecord(BaseModel):
    family_id: str
    source_ref_raw: str
    source_id: str | None
    title: str | None
    authors: list[str]
    publication: str | None
    year: int | None
    doi: str | None
    arxiv_id: str | None
    url: str | None
    local_hash: str | None
    resolution_status: str
    confidence: str
    identity_complete: bool
    blockers: list[str]
```

Resolution statuses:

```txt
RESOLVED_LOCAL
RESOLVED_EXTERNAL_IDENTITY
RESOLVED_PROBABLE
RAW_REF_ONLY
AMBIGUOUS
UNRESOLVED
REQUIRES_HUMAN_LOOKUP
```

---

## 3. Identity completeness

Identity is complete if:

```txt
source_id exists
and at least one of title/exact citation identity exists
and publication/year exists
and at least one of DOI/arXiv/URL/local_hash exists
```

Identity is incomplete if:

```txt
only raw citation string exists
only journal/volume/page exists without title/DOI/hash
only author/year exists without locator
only local filename exists without hash
```

---

## 4. No fabrication rule

If the identity cannot be resolved from local artifacts and existing metadata:

```txt
resolution_status = REQUIRES_HUMAN_LOOKUP
```

Do not fabricate:

```txt
title
authors
DOI
arXiv
URL
dataset location
```

---

## 5. Availability matrix

Create:

```txt
data/preflight/source_identity/source_availability_matrix_v4_9.json
```

Schema:

```python
class SourceAvailabilityMatrixRecord(BaseModel):
    family_id: str
    source_id: str | None
    identity_complete: bool
    local_pdf_available: bool
    local_pdf_path: str | None
    local_pdf_hash: str | None
    supplementary_available: bool
    dataset_available: bool
    availability_status: str
    required_next_action: str
```

Availability statuses:

```txt
AVAILABLE_LOCAL_PDF
AVAILABLE_SUPPLEMENTARY
AVAILABLE_DATASET
IDENTITY_ONLY_REQUIRES_DOWNLOAD
IDENTITY_INCOMPLETE
NOT_AVAILABLE
```

---

## 6. Final principle

```txt
Identity before extraction.
Extraction before evidence.
Evidence before claim.
```
