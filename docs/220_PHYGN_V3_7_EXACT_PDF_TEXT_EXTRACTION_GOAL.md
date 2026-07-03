# Phygn v3.7 — Exact PDF/Text Extraction: Quotes, Equations, Tables & Ranges Goal

## 0. Context

The latest assumed result document is:

```txt
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
```

Therefore, v3.7 starts at:

```txt
220
```

v3.6 created a local source registry for the five priority sources.

The next correct step is exact extraction only if the priority files are locally present and hashed.

v3.7 must operate only on locally registered source files.

---

## 1. Core thesis

```txt
Hash and local presence enable extraction.
Extraction enables review.
Review may enable pressure.
None of them enables physical truth.
```

v3.7 extracts exact source material.

It does not validate PHI_GRADIENT.

It does not grant source-backed support.

It does not grant benchmark support.

It does not unlock physical claims.

---

## 2. Hard rule

```txt
No local hash, no extraction.
No extraction outside registered source files.
No OCR unless text extraction fails and manual review is required.
No fabricated quote.
No fabricated equation.
No fabricated table value.
No physical claim.
```

---

## 3. Inputs

v3.7 must load:

```txt
data/real_sources/local_text_registry_v3_6.json
data/real_sources/source_file_manifest_v3_6.json
data/real_sources/source_hashes_v3_6.json
data/real_sources/source_availability_v3_6.json
```

And operate only on registered files under:

```txt
data/real_sources/pdfs/
```

Priority files:

```txt
Hornberger_2003_Collisional_Decoherence.pdf
Hackermueller_2004_Thermal_Emission_Decoherence.pdf
Nimmrichter_2011_CSL_Matter_Wave_Test.pdf
Schrinski_2020_QC_Hypothesis_Tests.pdf
Pedernales_2019_Motional_Dynamical_Decoupling.pdf
```

---

## 4. Extraction targets

For each available hashed PDF, extract candidate records for:

```txt
short exact quotes
equation text or equation references
observable definitions
mass/length/time ranges
visibility/decoherence measures
environmental conditions
parameter constraints
benchmark table/figure references
negative or exclusion constraints
limitations
```

---

## 5. Output files

Create:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
```

---

## 6. Possible v3.7 statuses

```txt
PHI_GRADIENT_PDF_EXTRACTION_COMPLETED
PHI_GRADIENT_PDF_EXTRACTION_PARTIAL
PHI_GRADIENT_PDF_EXTRACTION_READY_FOR_REVIEW
PHI_GRADIENT_PDF_EXTRACTION_NO_TEXT_FOUND
PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW
PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES
PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING
```

---

## 7. What v3.7 may allow

Allowed:

```txt
Exact PDF/text extraction was performed.
Candidate quotes/equations/ranges were extracted.
Some extracted records require review.
Some PDFs may require manual extraction.
```

Blocked:

```txt
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT physically validated
Frontera C validated
```

---

## 8. Next phase

Recommended next phase:

```txt
v3.8 — Extract Candidate Review & Validation-Ready Pack Assembly
```

v3.8 must convert extraction candidates into reviewed exact extracts.

v3.9 may then run:

```txt
Exact Extract Validation & First Source-Pressure Decision
```

---

## 9. Acceptance criteria

v3.7 is complete when:

```txt
local registry loaded
hashed file boundary enforced
PDF/text extraction attempted only on registered files
quote candidates generated
equation candidates generated
table/range candidates generated
negative constraint candidates generated
extraction manifest generated
reports generated
tests pass
physical claims remain blocked
```

---

## 10. Final principle

```txt
Extraction is contact, not belief.
```
