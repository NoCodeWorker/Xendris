# Codex Prompt — Phygn v3.7 Exact PDF/Text Extraction: Quotes, Equations, Tables & Ranges

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab / Signphy Product Layer
```

Current confirmed latest document:

```txt
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
```

Therefore v3.7 starts at:

```txt
220
```

---

# 1. Read first

Read these v3.7 specs:

```txt
docs/220_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_docs/status/GOAL.md
docs/221_PHYGN_PDF_EXTRACTION_BOUNDARY_AND_METHOD_PROTOCOL.md
docs/222_PHYGN_EXTRACTION_CANDIDATE_CLASSIFICATION_AND_OUTPUTS.md
docs/223_PHYGN_V3_7_REPORTING_AND_REVIEW_GATE.md
```

Also read:

```txt
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
docs/213_PHYGN_V3_5_PRIORITY_EXACT_FILL_RESULTS.md
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
```

Inspect:

```txt
phyng/local_source_text/
phyng/priority_exact_fill/
phyng/exact_extract_review/
phyng/source_pack_validation/
phyng/source_pack_population/
phyng/core/
phyng/closed_loop/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
682 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.7:

```txt
Exact PDF/Text Extraction
Hashed Source Boundary Enforcement
Page-Level Text Extraction
Quote Candidate Extraction
Equation Candidate Extraction
Table/Range Candidate Extraction
Negative Constraint Candidate Extraction
Extraction Manifest
Canonical Reports
Next Review Gate
Tests
```

Do not validate PHI_GRADIENT.

Do not make physical claims.

---

# 4. Input registry

Load:

```txt
data/real_sources/local_text_registry_v3_6.json
data/real_sources/source_file_manifest_v3_6.json
data/real_sources/source_hashes_v3_6.json
data/real_sources/source_availability_v3_6.json
```

Only extract from files that are:

```txt
exists = true
sha256 != null
file_type supported
local_path under data/real_sources/pdfs/
```

---

# 5. Extend package

Create or extend:

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

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_pdf_text_extraction.py
```

---

# 6. PDF/text extraction

Use available lightweight libraries.

Preferred order:

```txt
pypdf
PyMuPDF / fitz
pdfplumber
plain text fallback
```

If no PDF reader is available:

```txt
PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW
```

Do not add heavy dependencies without approval.

Do not OCR by default.

---

# 7. Output files

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

# 8. Candidate rules

Every candidate must include:

```txt
candidate_id
source_id
sha256
page_number
location_type
location_value
candidate_type
extracted_text
confidence
requires_manual_review
notes
```

Do not output long full-page text in reports.

Use JSON artifacts for full candidate records.

Reports should summarize.

---

# 9. Candidate types

```txt
QUOTE_CANDIDATE
EQUATION_CANDIDATE
OBSERVABLE_CANDIDATE
PARAMETER_RANGE_CANDIDATE
BENCHMARK_RANGE_CANDIDATE
TABLE_CAPTION_CANDIDATE
FIGURE_CAPTION_CANDIDATE
NEGATIVE_CONSTRAINT_CANDIDATE
LIMITATION_CANDIDATE
```

---

# 10. Campaign statuses

If registry missing:

```txt
PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_REGISTRY_MISSING
```

If no hashed files:

```txt
PHI_GRADIENT_PDF_EXTRACTION_BLOCKED_NO_HASHED_FILES
```

If files exist but text cannot be extracted:

```txt
PHI_GRADIENT_PDF_EXTRACTION_NO_TEXT_FOUND
```

If extraction partially succeeds:

```txt
PHI_GRADIENT_PDF_EXTRACTION_PARTIAL
```

If extraction produces candidates:

```txt
PHI_GRADIENT_PDF_EXTRACTION_COMPLETED
```

If extraction requires manual review:

```txt
PHI_GRADIENT_PDF_EXTRACTION_REQUIRES_MANUAL_REVIEW
```

---

# 11. Reports

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

Reports must include:

```txt
canonical status section
hashed input source count
extracted source count
blocked source count
candidate counts
manual review count
blocked claims
next actions
discipline note
```

---

# 12. Tests

Create:

```txt
tests/test_pdf_text_extraction_registry_boundary_v3_7.py
tests/test_pdf_text_extraction_page_reader_v3_7.py
tests/test_pdf_text_extraction_candidate_detection_v3_7.py
tests/test_pdf_text_extraction_reports_v3_7.py
tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py
```

Minimum tests:

```txt
test_registry_required_for_extraction
test_unhashed_file_is_not_extracted
test_missing_files_block_extraction
test_hashed_pdf_can_be_queued_for_extraction
test_page_text_extraction_records_source_hash
test_candidate_contains_location_and_source_id
test_equation_candidate_requires_extracted_text
test_range_candidate_requires_units_or_numbers
test_negative_candidate_requires_negative_keywords
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_existing_v3_6_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing v3.6 local source registry behavior
existing v3.5 priority exact fill behavior
existing v3.4 exact extract review behavior
existing v3.3 source pack validation behavior
existing v3.2 source pack population behavior
existing historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
PDF extraction validates PHI_GRADIENT.
Extracted quote candidate is source support.
Equation candidate is physical support.
Benchmark candidate is benchmark support.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
PDF/text extraction ran on hashed local sources.
Extraction candidates were generated.
Candidates require review and validation before source pressure.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
hashed boundary enforced
PDF/text extraction implemented
candidate files generated
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
682 + new v3.7 tests
```

---

# 16. Final discipline

```txt
Extraction is contact, not belief.
```
