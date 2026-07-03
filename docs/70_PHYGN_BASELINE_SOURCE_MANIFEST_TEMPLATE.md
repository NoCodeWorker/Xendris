# Phygn v1.2 — Baseline Source Manifest Template

## 0. Purpose

This document provides the canonical manifest template for:

```txt
sources/baseline/source_manifest.json
```

It must be edited with real source metadata and real local paths before ingestion.

---

## 1. Template

```json
[
  {
    "source_candidate_id": "SRC-BASE-DECOH-001",
    "requirement_id": "BSP-001",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-DECOH-001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["FORMULA_SUPPORT", "CONTEXT_SUPPORT", "PARAMETER_SUPPORT"],
    "notes": "Replace with real metadata after local source is selected. Do not invent fields."
  },
  {
    "source_candidate_id": "SRC-BASE-VIS-001",
    "requirement_id": "BSP-002",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-VIS-001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["OBSERVABLE_SUPPORT", "FORMULA_SUPPORT"],
    "notes": "Visibility/interference contrast source. Metadata must be real."
  },
  {
    "source_candidate_id": "SRC-BASE-MWI-001",
    "requirement_id": "BSP-004",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-MWI-001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Matter-wave or nanoparticle interferometry context source."
  },
  {
    "source_candidate_id": "SRC-BASE-THRESH-001",
    "requirement_id": "BSP-006",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-THRESH-001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["BENCHMARK_SUPPORT", "PARAMETER_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Optional threshold/uncertainty source."
  },
  {
    "source_candidate_id": "SRC-BASE-PARAM-001",
    "requirement_id": "BSP-005",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-PARAM-001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["PARAMETER_SUPPORT", "ASSUMPTION_SUPPORT"],
    "notes": "Optional Gamma/timescale/assumption support source."
  }
]
```

---

## 2. Important rules

```txt
title = null until known
authors = [] until known
year = null until known
url = null unless explicitly known
local_path must point to a real file before ingestion
```

Do not invent:

```txt
DOI
journal
page numbers
quotes
experimental values
```

---

## 3. Placeholder handling

This template is a scaffold.

The ingestion system must classify missing local files as:

```txt
not ready
```

and must not mark sources as ingested.

---

## 4. Structural validation

The template may validate structurally.

But it should not produce:

```txt
READY_FOR_INGESTION_ATTEMPT
```

until:

```txt
local files exist
extracts exist or content is parseable
support tags are validated
```

---

## 5. Final principle

```txt
A manifest can be valid as structure and still empty as evidence.
```
