# Phygn v3.6 — Reporting & Next Extraction Gate

## 0. Purpose

This document defines reporting and the transition to exact extraction.

---

## 1. Required reports

Generate:

```txt
reports/local_source_text/phi_gradient_local_source_registry_v3_6.md
reports/local_source_text/phi_gradient_source_file_manifest_v3_6.md
reports/local_source_text/phi_gradient_source_hashes_v3_6.md
reports/local_source_text/phi_gradient_source_availability_v3_6.md
reports/local_source_text/phi_gradient_manual_download_tasks_v3_6.md
reports/local_source_text/phi_gradient_next_exact_extraction_v3_6.md
reports/campaigns/PHI-GRADIENT-LOCAL-SOURCE-TEXT-REGISTRY-v3_6.md
```

---

## 2. Report requirements

Reports must include:

```txt
priority source count
available local file count
missing local file count
hashed file count
unsupported file count
manual download task count
source_id to local_path mapping
source_id to sha256 mapping
canonical status
blocked claims
next actions
discipline note
```

---

## 3. Canonical status

If no files are available:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: NO_EVIDENCE
SupportLevel: UNSUPPORTED
BlockedReasons:
  LOCAL_SOURCE_TEXT_MISSING
  MISSING_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

If some files are available:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  EXTRACTION_PENDING
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

If all priority files are available and hashed:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  EXACT_EXTRACTION_PENDING
  VALIDATION_PENDING
  MISSING_EXPERIMENTAL_DATA
```

---

## 4. Allowed claims

Allowed:

```txt
Local source registry was created.
Priority files were checked.
Available files were hashed.
Missing files were converted into manual download tasks.
```

Blocked:

```txt
Local file availability validates PHI_GRADIENT.
A PDF hash is source support.
A registered file is benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

---

## 5. Next phase

Recommended next phase:

```txt
v3.7 — Exact PDF/Text Extraction: Quotes, Equations, Tables & Ranges
```

v3.7 must:

```txt
load local source registry
open available PDFs/text files
extract exact quotes
extract equations or equation references
extract observables
extract parameter ranges
extract benchmark ranges
extract negative constraints
write validation-ready extract pack
keep physical claims blocked
```

---

## 6. Final principle

```txt
v3.6 gives Phygn hands.
v3.7 uses them to touch the text.
```
