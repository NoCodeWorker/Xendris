# Phygn v2.9 — Real Source Acquisition & Manifest Protocol

## 0. Purpose

This document defines how v2.9 acquires and records real sources for PHI_GRADIENT.

The manifest must distinguish:

```txt
real sources
fixture sources
local benchmark records
unavailable sources
candidate sources not yet ingested
```

---

## 1. Real source manifest schema

```python
class RealSourceManifestEntry(BaseModel):
    source_id: str
    title: str
    authors: list[str]
    year: int | None
    source_type: str
    acquisition_method: str
    url: str | None
    local_path: str | None
    doi: str | None
    arxiv_id: str | None
    slots_targeted: list[str]
    acquisition_status: str
    ingestion_status: str
    notes: list[str]
```

---

## 2. Acquisition statuses

```txt
REAL_SOURCE_CANDIDATE_IDENTIFIED
REAL_SOURCE_AVAILABLE_LOCAL
REAL_SOURCE_AVAILABLE_URL
REAL_SOURCE_METADATA_ONLY
REAL_SOURCE_UNAVAILABLE
REAL_SOURCE_DUPLICATE
REAL_SOURCE_REJECTED_OUT_OF_SCOPE
```

---

## 3. Ingestion statuses

```txt
REAL_SOURCE_NOT_INGESTED
REAL_SOURCE_INGESTED
REAL_SOURCE_EXTRACTED
REAL_SOURCE_EXTRACTION_FAILED
REAL_SOURCE_REQUIRES_MANUAL_REVIEW
REAL_SOURCE_REJECTED_DECORATIVE_ANALOGY
REAL_SOURCE_REJECTED_NOT_COMPARABLE
```

---

## 4. Priority acquisition targets

Search/acquire sources in this priority order:

```txt
1. visibility decay / decoherence baseline
2. mesoscopic interferometry benchmark data
3. gravitational decoherence models
4. gradient or transition operators in effective models
5. log or scale-space formulations
6. alpha-like parameter constraints
7. negative/conflicting sources
```

Reason:

```txt
Observable and benchmark comparability must be fixed before abstract analogies.
```

---

## 5. Real source minimum requirements

A real source may be counted only if it has:

```txt
source_id
title
authors or responsible entity
year or publication status
path/url/doi/arxiv id
targeted slot
extracted claim or explicit rejection reason
```

---

## 6. Fixture separation

Fixtures from v2.8 must be marked:

```txt
FIXTURE_ONLY_DOES_NOT_COUNT_AS_REAL_SUPPORT
```

No fixture may be used to produce:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

---

## 7. Final principle

```txt
A manifest is not bibliography.
It is an audit trail of what was acquired, rejected, extracted or left unresolved.
```
