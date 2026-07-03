# Phygn v1.1 — Baseline Literature Source Acquisition Goal

## 0. Purpose

Phygn v1.0 proved that the evidence gate works:

```txt
empty source pack -> BASELINE_REQUIRES_SOURCE
URL-only source -> not ingested
formula + observable local support -> BASELINE_SOURCE_BACKED_LIMITED in tests
candidate prediction -> still blocked
```

v1.1 has a different mission:

```txt
prepare a real literature source pack that can be placed in sources/baseline/
and processed by the v1.0 ingestion pipeline.
```

This phase does not prove Frontera C.  
It does not validate the boundary-aware candidate.  
It does not claim physical decoherence prediction.

It prepares admissible evidence.

---

## 1. Current state

Last operational result:

```txt
61_PHYGN_V1_0_BASELINE_SOURCE_PACK_INGESTION_RESULTS.md
```

Current baseline status:

```txt
BASELINE_REQUIRES_SOURCE
```

Current campaign:

```txt
BASELINE-SRC-PACK-001
linked to CAMPAIGN-002
```

Current limitation:

```txt
No actual local baseline sources have been ingested.
```

---

## 2. Goal v1.1

Create:

```txt
canonical source selection guide
local file acquisition checklist
source_manifest authoring protocol
extract and support tagging protocol
Codex implementation prompt
```

The goal is to enable a later run of:

```txt
python -m phyng.campaigns.baseline_source_pack_ingestion d:\BIOCULTOR\PHYNG
```

with actual local files.

---

## 3. What counts as success

v1.1 is complete if it produces:

```txt
1. a list of canonical source categories;
2. a manifest schema ready for real sources;
3. an extract protocol for FORMULA_SUPPORT and OBSERVABLE_SUPPORT;
4. support tagging rules;
5. a no-fake-metadata checklist;
6. a prompt instructing the IDE to prepare and validate local source packs;
7. tests for manifest/extract validation if implemented.
```

---

## 4. What v1.1 may unlock

v1.1 may unlock only readiness for ingestion.

Allowed:

```txt
Phygn is ready to ingest a baseline literature source pack.
The required source categories are explicit.
The local source preparation protocol is defined.
```

Not allowed:

```txt
The baseline is source-backed.
Frontera C is validated.
Phygn predicts decoherence.
The candidate is validated.
```

The baseline can become source-backed only after the actual v1.0/v1.1 ingestion runner sees real local files and audits them.

---

## 5. Source categories needed

Minimum categories:

```txt
VISIBILITY_DECAY
ENVIRONMENTAL_DECOHERENCE
MATTER_WAVE_INTERFEROMETRY
DETECTABILITY_OR_VISIBILITY_THRESHOLD
OPTIONAL_PARAMETER_OR_RATE_SUPPORT
```

Minimum for LIMITED:

```txt
FORMULA_SUPPORT
OBSERVABLE_SUPPORT
HIGH or PRIMARY trust
PASSED_LIMITED citation audit
```

---

## 6. Key discipline

A source pack is not a bibliography.

A source pack is a structured claim-permission artifact.

Each source must be evaluated by:

```txt
what claim does it support?
what support type does it provide?
what does it not support?
what remains blocked?
```

---

## 7. No fake source rule

Do not invent:

```txt
paper title
authors
year
DOI
journal
page number
quote
experimental result
```

If unknown:

```txt
null
[]
UNKNOWN
```

---

## 8. Expected folders

```txt
sources/baseline/
  source_manifest.json
  papers/
  extracts/
  notes/
  rejected/
```

---

## 9. Reports expected after actual ingestion

```txt
reports/rag/baseline_source_pack_v1_1.md
reports/rag/source_manifest_validation_v1_1.md
reports/rag/extract_support_tags_v1_1.md
reports/campaigns/BASELINE-SRC-PACK-001_v1_1_readiness.md
```

---

## 10. Final principle

```txt
The next scientific object is not a claim.
It is a well-prepared evidence package.
```
