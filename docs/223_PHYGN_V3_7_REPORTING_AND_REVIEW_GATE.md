# Phygn v3.7 — Reporting & Review Gate

## 0. Purpose

This document defines reports and transition from extraction to reviewed exact extracts.

---

## 1. Required reports

Generate:

```txt
reports/pdf_text_extraction/phi_gradient_pdf_extraction_manifest_v3_7.md
reports/pdf_text_extraction/phi_gradient_pdf_source_coverage_v3_7.md
reports/pdf_text_extraction/phi_gradient_pdf_quote_candidates_v3_7.md
reports/pdf_text_extraction/phi_gradient_pdf_equation_candidates_v3_7.md
reports/pdf_text_extraction/phi_gradient_pdf_table_range_candidates_v3_7.md
reports/pdf_text_extraction/phi_gradient_pdf_negative_constraint_candidates_v3_7.md
reports/pdf_text_extraction/phi_gradient_pdf_extraction_next_gate_v3_7.md
reports/campaigns/PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7.md
```

---

## 2. Report requirements

Reports must include:

```txt
hashed input sources
extracted sources
blocked sources
pages extracted
quote candidate count
equation candidate count
range/table candidate count
negative candidate count
manual-review candidate count
source coverage by priority source
canonical status
blocked claims
next actions
discipline note
```

---

## 3. Canonical status

If no hashed sources:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: NO_EVIDENCE
SupportLevel: UNSUPPORTED
BlockedReasons:
  LOCAL_SOURCE_TEXT_MISSING
  EXTRACTION_BLOCKED
```

If extraction produces candidates:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: SYNTHETIC_ONLY
SupportLevel: SYNTHETIC
BlockedReasons:
  REVIEW_PENDING
  VALIDATION_PENDING
  MISSING_VALIDATED_SOURCE_SUPPORT
  MISSING_BENCHMARK
```

If extraction fails but files exist:

```txt
CanonicalPermission: REVIEW_REQUIRED
EvidenceLevel: NO_EVIDENCE
SupportLevel: UNSUPPORTED
BlockedReasons:
  EXTRACTION_FAILED
  MANUAL_REVIEW_REQUIRED
```

---

## 4. Allowed claims

Allowed:

```txt
PDF/text extraction was performed on hashed local sources.
Candidate quotes/equations/ranges were generated.
Candidates require review before validation.
```

Blocked:

```txt
Extracted candidate text validates PHI_GRADIENT.
Extracted equation candidate is source support.
Extracted benchmark candidate is benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

---

## 5. Next phase

Recommended next phase:

```txt
v3.8 — Extract Candidate Review & Validation-Ready Pack Assembly
```

v3.8 must:

```txt
select candidate snippets
confirm exact location
confirm equation/observable/range role
reject garbage extraction
create validation-ready exact extract pack
preserve manual review requirements where needed
```

---

## 6. Final principle

```txt
v3.7 gives raw contact.
v3.8 gives reviewed contact.
v3.9 decides pressure.
```
