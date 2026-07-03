# Phygn v3.7 - Exact PDF/Text Extraction Results

Date: 2026-07-01

Source prompt:

```txt
docs/224_PHYGN_CODEX_V3_7_EXACT_PDF_TEXT_EXTRACTION_PROMPT.md
```

Supporting specs:

```txt
docs/220_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_docs/status/GOAL.md
docs/221_PHYGN_PDF_EXTRACTION_BOUNDARY_AND_METHOD_PROTOCOL.md
docs/222_PHYGN_EXTRACTION_CANDIDATE_CLASSIFICATION_AND_OUTPUTS.md
docs/223_PHYGN_V3_7_REPORTING_AND_REVIEW_GATE.md
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v3.7 PROMPT SPECIFICATIONS WITH PARTIAL EXTRACTION**

Final campaign status:

```txt
PHI_GRADIENT_PDF_EXTRACTION_PARTIAL
```

Interpretation:

```txt
The v3.7 hashed-source boundary was enforced.
Five v3.6 hashed local PDFs were seen.
Four PDFs produced embedded-text extraction candidates through the internal PDF stream parser.
One PDF requires an installed PDF reader or manual review.
No extracted candidate was promoted to source support.
No benchmark support was granted.
No physical claim was upgraded.
```

Validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_local_source_registry_schema_v3_6.py tests/test_local_source_file_discovery_v3_6.py tests/test_local_source_hashing_v3_6.py tests/test_local_source_availability_v3_6.py tests/test_local_source_manual_download_tasks_v3_6.py tests/test_phi_gradient_local_source_text_registry_campaign_v3_6.py tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py
25 passed in 1.32s
```

Focused v3.7 validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py
13 passed in 0.60s
```

Full-suite note:

```txt
The full pytest suite is currently blocked by the local .venv NumPy C-extension DLL import error in pre-existing tests:
tests/test_case_quantum_channel.py
tests/test_epistemic_trace.py
tests/test_reporting.py

This failure occurs during collection before v3.7 logic is exercised.
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/pdf_text_extraction/
  __init__.py
  schemas.py
  registry_loader.py
  pdf_reader.py
  page_extraction.py
  candidate_detection.py
  equation_detection.py
  range_detection.py
  negative_detection.py
  extraction_manifest.py
  report.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_pdf_text_extraction.py
```

Entrypoint:

```python
run_phi_gradient_pdf_text_extraction_campaign(root: str | Path = ".")
```

---

## 3. Extraction Boundary

v3.7 loads:

```txt
data/real_sources/local_text_registry_v3_6.json
data/real_sources/source_file_manifest_v3_6.json
data/real_sources/source_hashes_v3_6.json
data/real_sources/source_availability_v3_6.json
```

Extraction is allowed only when:

```txt
exists = true
sha256 != null
file_type is supported
local_path resolves under data/real_sources/pdfs/
source_id is present in the v3.6 hash manifest
```

Preserved rule:

```txt
No local hash, no extraction.
No URL/arXiv/DOI metadata is treated as local source text.
```

---

## 4. Campaign Metrics

Final manifest:

```txt
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
```

Summary:

| Metric | Result |
|---|---:|
| Hashed sources seen | 5 |
| Sources extracted | 4 |
| Sources blocked | 1 |
| Pages/text stream records extracted | 9 |
| Total candidates | 33 |
| Quote/observable candidates | 5 |
| Equation candidates | 16 |
| Table/range candidates | 12 |
| Negative candidates | 0 |
| Manual-review count | 38 |

Source coverage:

| Source ID | Extraction status | Pages | Candidates |
|---|---|---:|---:|
| `SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE` | `TEXT_EXTRACTED_INTERNAL_PDF_STREAMS` | 3 | 7 |
| `SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE` | `TEXT_EXTRACTED_INTERNAL_PDF_STREAMS` | 2 | 6 |
| `SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST` | `TEXT_EXTRACTED_INTERNAL_PDF_STREAMS` | 2 | 6 |
| `SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS` | `TEXT_EXTRACTED_INTERNAL_PDF_STREAMS` | 2 | 14 |
| `SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING` | `EXTRACTION_REQUIRES_PDF_READER_OR_MANUAL_REVIEW` | 0 | 0 |

Pedernales blocked reason:

```txt
No installed PDF reader extracted text and internal stream parsing found no usable text.
```

---

## 5. Generated Data Artifacts

Created:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
```

Candidate records include:

```txt
candidate_id
source_id
sha256
page_number
location_type
location_value
candidate_type
extracted_text
normalized_text
confidence
requires_manual_review
notes
```

All generated candidates require manual review before source-pressure use.

---

## 6. Generated Reports

Created:

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

All generated reports include the canonical status section.

Campaign report:

```txt
reports/campaigns/PHI-GRADIENT-PDF-TEXT-EXTRACTION-v3_7.md
```

---

## 7. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
```

Statuses:

```txt
PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING
PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES
PHI_GRADIENT_PDF_EXTRACTION_NO_TEXT_FOUND
PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW
PHI_GRADIENT_PDF_EXTRACTION_PARTIAL
PHI_GRADIENT_PDF_EXTRACTION_COMPLETED
PHI_GRADIENT_PDF_EXTRACTION_READY_FOR_REVIEW
```

The active status maps to:

```txt
Canonical Permission: REVIEW_REQUIRED
Blocked Reasons: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Risk Level: TECHNICAL_RISK
```

---

## 8. Reader Availability

Checked local reader availability:

```txt
pypdf = false
fitz = false
pdfplumber = false
pdftotext = unavailable
pdftoppm = unavailable
```

Implemented fallback:

```txt
internal_pdf_stream_parser
```

This parser extracts embedded PDF text streams when possible, but every result from it remains manual-review material.

---

## 9. New Tests

Created:

```txt
tests/test_pdf_text_extraction_registry_boundary_v3_7.py
tests/test_pdf_text_extraction_page_reader_v3_7.py
tests/test_pdf_text_extraction_candidate_detection_v3_7.py
tests/test_pdf_text_extraction_reports_v3_7.py
tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py
```

Coverage includes:

| Test | Purpose |
|---|---|
| `test_registry_required_for_extraction` | Confirms registry artifacts are required |
| `test_unhashed_file_is_not_extracted` | Confirms unhashed files are blocked |
| `test_missing_files_block_extraction` | Confirms missing files do not enter extraction |
| `test_hashed_pdf_can_be_queued_for_extraction` | Confirms hash boundary queueing |
| `test_page_text_extraction_records_source_hash` | Confirms extracted page text preserves source hash |
| `test_candidate_contains_location_and_source_id` | Confirms candidate traceability |
| `test_equation_candidate_requires_extracted_text` | Confirms equation candidates have extracted text |
| `test_range_candidate_requires_units_or_numbers` | Confirms range candidates require numbers/units |
| `test_negative_candidate_requires_negative_keywords` | Confirms negative candidate keyword gate |
| `test_reports_include_canonical_section` | Confirms report contract integration |
| `test_physical_claims_remain_blocked` | Confirms blocked claim discipline |
| `test_campaign_generates_outputs` | Confirms campaign artifacts are generated |
| `test_existing_v3_6_behavior_preserved` | Confirms v3.6 status semantics remain unchanged |

---

## 10. Behavior Preservation

v3.7 did not alter:

```txt
v3.6 local source registry behavior
v3.5 priority exact fill behavior
v3.4 exact extract review behavior
v3.3 source pack validation behavior
v3.2 source pack population behavior
historical reports
```

Preservation evidence:

```txt
25 passed in 1.32s
```

for focused v3.6 + v3.7 tests.

---

## 11. Blocked Claims

The campaign explicitly blocks:

```txt
PDF extraction validates PHI_GRADIENT.
Extracted quote candidate is source support.
Equation candidate is physical support.
Benchmark candidate is benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed statements:

```txt
PDF/text extraction was performed on hashed local sources.
Candidate quotes/equations/ranges were generated.
Candidates require review before validation.
```

---

## 12. Next Gate

Recommended next phase:

```txt
v3.8 - Extract Candidate Review & Validation-Ready Pack Assembly
```

Before v3.8 review, improve extraction coverage if desired by installing a lightweight PDF reader:

```txt
pypdf
pdfplumber
```

This is especially relevant for:

```txt
SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

v3.8 must not claim source support until candidates are reviewed, locations are confirmed, and garbage extraction is rejected.

---

## 13. Final Assessment

v3.7 converted hashed local PDFs into raw extraction candidates while preserving the epistemic boundary.

The useful result is:

```txt
Four priority PDFs now have reviewable extraction candidates.
One priority PDF still requires PDF-reader/manual review support.
All candidates remain non-support until v3.8 review.
```

Final discipline note:

```txt
Extraction is contact, not belief.
```
