# Phygn v3.8 — Extract Candidate Review & Validation-Ready Pack Assembly Goal

## 0. Context

The latest confirmed document is:

```txt
D:\BIOCULTOR\PHYNG\docs\225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
```

Therefore, v3.8 starts at:

```txt
226
```

v3.7 performed exact PDF/text extraction over locally registered, hashed source files.

v3.7 final status:

```txt
PHI_GRADIENT_PDF_EXTRACTION_PARTIAL
```

v3.7 produced:

```txt
5 hashed sources seen
4 sources extracted
1 source blocked: SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
33 extraction candidates
0 validated source support
0 benchmark support
0 physical claim
```

v3.8 now reviews the raw extraction candidates and assembles a validation-ready exact extract pack.

---

## 1. Core thesis

```txt
Raw extraction is contact.
Reviewed extraction is evidence-ready.
Validated extraction is pressure.
```

v3.8 does not decide whether PHI_GRADIENT has support.

v3.8 decides whether extracted candidates are clean enough to enter the next validation gate.

---

## 2. Hard rule

```txt
No reviewed extract without source hash.
No reviewed extract without exact location.
No validation-ready extract without exact content.
No garbage extraction enters the pack.
No candidate text becomes support in v3.8.
No physical claim.
```

---

## 3. Inputs

v3.8 must load:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/source_hashes_v3_6.json
```

If candidate files are missing:

```txt
PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES
```

---

## 4. Outputs

Create:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json
data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json
data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json
data/real_sources/extracts/phi_gradient_v3_8_next_validation_gate_inputs.json
```

---

## 5. Possible v3.8 statuses

```txt
PHI_GRADIENT_EXTRACT_REVIEW_COMPLETED
PHI_GRADIENT_EXTRACT_REVIEW_PARTIAL
PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION
PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_EXTRACT_REVIEW_NO_VALIDATION_READY_EXTRACTS
PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES
```

---

## 6. Validation-ready requirements

A candidate becomes a validation-ready exact extract only if:

```txt
source_id is known
sha256 is present
page_number or exact location is present
candidate_type is meaningful
extracted_text is non-empty
text is not obvious garbage
component role is assigned
manual review is resolved or explicitly marked safe
limitations are recorded
```

---

## 7. Component roles

Map reviewed candidates to one of:

```txt
DECOHERENCE_BASELINE
VISIBILITY_DECAY_OBSERVABLE
GRADIENT_COMPONENT
BENCHMARK_MODEL
PARAMETER_CONSTRAINT
NEGATIVE_CONSTRAINT
LIMITATION
ANALOGY_ONLY
REJECTED_GARBAGE
REQUIRES_MANUAL_REVIEW
```

---

## 8. v3.8 does not validate support

Blocked in v3.8:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT physically validated
Frontera C validated
```

Those belong to v3.9 or later.

---

## 9. Acceptance criteria

v3.8 is complete when:

```txt
v3.7 candidates loaded
review decision rules implemented
garbage candidates rejected
manual review queue produced
validation-ready pack produced if possible
reports generated
tests pass
physical claims remain blocked
```

---

## 10. Final principle

```txt
A validation-ready extract is not support.
It is an object ready to be judged.
```
