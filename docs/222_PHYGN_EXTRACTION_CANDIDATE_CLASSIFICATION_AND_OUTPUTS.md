# Phygn v3.7 — Extraction Candidate Classification & Outputs

## 0. Purpose

This document defines how extracted candidates are classified and serialized.

---

## 1. Extraction manifest

Create:

```txt
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
```

Fields:

```txt
manifest_id
candidate_family
phi_family
created_at
input_registry_id
hashed_sources_seen
sources_extracted
sources_blocked
total_pages_extracted
total_candidates
status
notes
```

---

## 2. Candidate output files

Create separate files:

```txt
phi_gradient_pdf_quote_candidates_v3_7.json
phi_gradient_pdf_equation_candidates_v3_7.json
phi_gradient_pdf_table_range_candidates_v3_7.json
phi_gradient_pdf_negative_constraint_candidates_v3_7.json
```

And combined file:

```txt
phi_gradient_pdf_text_extraction_v3_7.json
```

---

## 3. Quote candidate rule

A quote candidate should be short and localized.

Required:

```txt
source_id
sha256
page_number or section
extracted_text
candidate_type
requires_manual_review
```

Reports must avoid dumping long text.

---

## 4. Equation candidate rule

Equation candidate detection may include:

```txt
lines containing symbols
equation-number-like patterns
Greek letters
rate equations
visibility expressions
collapse parameter expressions
```

If extraction loses formatting:

```txt
requires_manual_review = true
```

---

## 5. Table/range candidate rule

A table/range candidate must preserve:

```txt
page number
nearby caption or heading
detected numeric ranges
units if visible
manual review flag
```

Units of interest:

```txt
amu
kg
m
nm
s
ms
K
Pa
mbar
Hz
s^-1
```

---

## 6. Negative candidate rule

Negative pressure candidate if text suggests:

```txt
environmental decoherence dominates
candidate-like effect is negligible
parameter regime excluded
benchmark mismatch
observable mismatch
```

All negative candidates require manual review before gate impact.

---

## 7. Confidence levels

```txt
LOW
MEDIUM
HIGH
```

Default confidence:

```txt
LOW
```

unless location and text are clean.

---

## 8. Final principle

```txt
Candidate extraction should maximize recall while preserving epistemic humility.
```
