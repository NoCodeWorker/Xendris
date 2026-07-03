# Phygn v1.1 — Source Manifest Authoring Protocol

## 0. Purpose

This document defines how to author:

```txt
sources/baseline/source_manifest.json
```

for the v1.0/v1.1 ingestion pipeline.

The manifest is not evidence by itself.  
It is a structured map to evidence.

---

## 1. Manifest path

```txt
sources/baseline/source_manifest.json
```

---

## 2. Required JSON shape

```json
[
  {
    "source_candidate_id": "SRC-BASE-VIS-001",
    "requirement_id": "BSP-001",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/source_file.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Metadata pending audit."
  }
]
```

---

## 3. Required fields

```txt
source_candidate_id
requirement_id
title
authors
year
source_type
local_path
url
trust_level
intended_support_types
notes
```

If a field is unknown, use:

```txt
null
[]
UNKNOWN
```

Do not invent.

---

## 4. Allowed source_type values

```txt
LOCAL_FILE
MANUAL_RECORD
EXTERNAL_URL_RECORD
BIBTEX_RECORD
RESEARCH_TASK_ONLY
```

Rules:

```txt
LOCAL_FILE can be ingested if file exists.
EXTERNAL_URL_RECORD cannot count as local ingestion.
MANUAL_RECORD cannot unlock support without audit.
BIBTEX_RECORD needs metadata validation.
RESEARCH_TASK_ONLY never unlocks baseline.
```

---

## 5. Requirement IDs

Recommended:

```txt
BSP-001 = visibility/coherence formula support
BSP-002 = observable support
BSP-003 = environmental decoherence support
BSP-004 = matter-wave / mesoscopic context
BSP-005 = parameter/rate/assumption support
BSP-006 = visibility threshold / uncertainty support
```

---

## 6. Support types

Allowed:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
PARAMETER_SUPPORT
CONTEXT_SUPPORT
BENCHMARK_SUPPORT
ASSUMPTION_SUPPORT
CONTRADICTION
```

Important:

```txt
intended_support_types are hypotheses.
actual support types are assigned only after audit.
```

---

## 7. Trust levels

```txt
PRIMARY
HIGH
MEDIUM
LOW
UNKNOWN
```

Hard rules:

```txt
LOW cannot unlock baseline hard claims.
UNKNOWN cannot unlock baseline hard claims.
```

---

## 8. Local path rules

Paths must be relative to project root:

```txt
sources/baseline/papers/example.pdf
sources/baseline/extracts/example_extracts.md
```

Do not use Windows absolute paths in manifest unless the ingestion pipeline explicitly supports them.

---

## 9. Example minimal manifest for one source

```json
[
  {
    "source_candidate_id": "SRC-BASE-DECOH-001",
    "requirement_id": "BSP-001",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/decoherence_visibility_001.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["FORMULA_SUPPORT"],
    "notes": "Needs extract for formula support."
  },
  {
    "source_candidate_id": "SRC-BASE-VIS-001",
    "requirement_id": "BSP-002",
    "title": null,
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/extracts/visibility_observable_001_extracts.md",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["OBSERVABLE_SUPPORT"],
    "notes": "Manual extract file; verify against original source."
  }
]
```

---

## 10. Manifest validation

The IDE should validate:

```txt
JSON parses
all required fields present
local files exist if source_type = LOCAL_FILE
support types are allowed
trust level is allowed
no fake metadata markers
```

---

## 11. Report

Generate:

```txt
reports/rag/source_manifest_validation_v1_1.md
```

---

## 12. Final principle

```txt
The manifest points to evidence.
It is not evidence.
```
