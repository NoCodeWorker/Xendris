# Phygn v1.3 — Filled Source Manifest Draft

## 0. Purpose

This document provides a draft manifest for real source candidates.

Important:

```txt
This is a draft.
It is not source ingestion.
Local paths must point to real local files before ingestion.
Metadata must be verified.
```

## 1. Draft `sources/baseline/source_manifest.json`

```json
[
  {
    "source_candidate_id": "SRC-BASE-DECOH-001",
    "requirement_id": "BSP-001",
    "title": "Decoherence, the measurement problem, and interpretations of quantum mechanics",
    "authors": ["Maximilian Schlosshauer"],
    "year": "2003",
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-DECOH-001.pdf",
    "url": "https://arxiv.org/abs/quant-ph/0312059",
    "trust_level": "HIGH",
    "intended_support_types": ["CONTEXT_SUPPORT", "ASSUMPTION_SUPPORT", "FORMULA_SUPPORT"],
    "notes": "Candidate. Verify local file and extract exact support before audit."
  },
  {
    "source_candidate_id": "SRC-BASE-DECOH-002",
    "requirement_id": "BSP-001",
    "title": "Environment--Induced Decoherence, Classicality and Consistency of Quantum Histories",
    "authors": ["Juan Pablo Paz", "Wojciech Hubert Zurek"],
    "year": "1993",
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-DECOH-002.pdf",
    "url": "https://arxiv.org/abs/gr-qc/9304031",
    "trust_level": "HIGH",
    "intended_support_types": ["CONTEXT_SUPPORT", "ASSUMPTION_SUPPORT", "PARAMETER_SUPPORT"],
    "notes": "Candidate. Use only for claims explicitly supported by extract."
  },
  {
    "source_candidate_id": "SRC-BASE-MWI-001",
    "requirement_id": "BSP-004",
    "title": "Macroscopic quantum resonators (MAQRO)",
    "authors": ["Rainer Kaltenbaek", "Gerald Hechenblaikner", "Nikolai Kiesel", "Oriol Romero-Isart", "Keith C. Schwab", "Ulrich Johann", "Markus Aspelmeyer"],
    "year": "2012",
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-MWI-001.pdf",
    "url": "https://arxiv.org/abs/1201.4756",
    "trust_level": "HIGH",
    "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Candidate for MAQRO/mesoscopic context and visibility-decoherence connection."
  },
  {
    "source_candidate_id": "SRC-BASE-MWI-002",
    "requirement_id": "BSP-004",
    "title": "Macroscopic Quantum Resonators (MAQRO): 2015 update",
    "authors": [],
    "year": "2015",
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-MWI-002.pdf",
    "url": "https://arxiv.org/abs/1503.02640",
    "trust_level": "HIGH",
    "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT"],
    "notes": "Candidate. Verify full authors and support locally before audit."
  },
  {
    "source_candidate_id": "SRC-BASE-VIS-001",
    "requirement_id": "BSP-002",
    "title": null,
    "authors": [],
    "year": "2024",
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-VIS-001.pdf",
    "url": "https://arxiv.org/pdf/2410.20910",
    "trust_level": "HIGH",
    "intended_support_types": ["OBSERVABLE_SUPPORT", "CONTEXT_SUPPORT"],
    "notes": "Candidate for visibility loss/contrast from matter-wave decoherence/dephasing. Verify metadata."
  },
  {
    "source_candidate_id": "SRC-BASE-VIS-002",
    "requirement_id": "BSP-002",
    "title": "Decoherence in a Talbot-Lau interferometer: the influence of molecular scattering",
    "authors": [],
    "year": null,
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-VIS-002.pdf",
    "url": null,
    "trust_level": "HIGH",
    "intended_support_types": ["FORMULA_SUPPORT", "OBSERVABLE_SUPPORT", "BENCHMARK_SUPPORT"],
    "notes": "Candidate for exponential decrease of fringe visibility. Verify bibliographic metadata and source URL."
  },
  {
    "source_candidate_id": "SRC-BASE-EXP-001",
    "requirement_id": "BSP-004",
    "title": "Experimental decoherence in molecule interferometry",
    "authors": ["Markus Arndt"],
    "year": "2021",
    "source_type": "LOCAL_FILE",
    "local_path": "sources/baseline/papers/SRC-BASE-EXP-001.pdf",
    "url": "https://arxiv.org/abs/2101.08216",
    "trust_level": "HIGH",
    "intended_support_types": ["CONTEXT_SUPPORT", "OBSERVABLE_SUPPORT", "EXPERIMENTAL_CONTEXT"],
    "notes": "Candidate. Verify full authors and explicit support."
  }
]
```

## 2. Important warning

This draft includes candidate metadata from search results and must be verified locally.

Before ingestion:

```txt
download or place local file
verify title
verify authors
verify year
write extracts
remove null/unknown if verified
keep null/unknown if not verified
```

## 3. Minimum local file set

Recommended first local files:

```txt
SRC-BASE-DECOH-001.pdf
SRC-BASE-MWI-001.pdf
SRC-BASE-VIS-002.pdf
```

If `SRC-BASE-VIS-002` cannot be verified quickly, use `SRC-BASE-VIS-001` as observable support candidate and keep formula support pending.

## 4. Final principle

```txt
A filled manifest draft is still not evidence.
It becomes useful only after local audit.
```
