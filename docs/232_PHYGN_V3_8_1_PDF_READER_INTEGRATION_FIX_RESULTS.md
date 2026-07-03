# Phygn v3.8.1 - PDF Reader Integration Fix & Pedernales Recovery Results

Date: 2026-07-01

Context:

```txt
pypdf, pdfplumber, and pymupdf were installed in .venv, but v3.7 still reported PDF readers as unavailable and left Pedernales blocked.
```

Correction scope:

```txt
Reader availability detection and extraction priority only.
No evidence gate was relaxed.
No URL/arXiv/DOI metadata was treated as local text.
No PDF content was invented.
No extraction candidate was converted into source support.
No physical claim was upgraded.
```

---

## 1. Runtime Reader Confirmation

Confirmed in the active virtual environment:

```txt
.\.venv\Scripts\python.exe
```

Imports available:

```txt
pypdf = 6.14.2
pdfplumber = 0.11.10
fitz/PyMuPDF = 1.28.0
```

---

## 2. Technical Fix

Updated:

```txt
phyng/pdf_text_extraction/pdf_reader.py
phyng/pdf_text_extraction/schemas.py
phyng/pdf_text_extraction/extraction_manifest.py
phyng/pdf_text_extraction/report.py
phyng/extract_candidate_review/campaign.py
phyng/campaigns/phi_gradient_pdf_text_extraction.py
phyng/campaigns/phi_gradient_extract_candidate_review.py
```

Reader priority is now:

```txt
1. pymupdf / fitz
2. pdfplumber
3. pypdf
4. internal_pdf_stream_parser
```

The internal parser is now used only as a fallback after installed readers are attempted.

Each source summary records:

```txt
reader_used
reader_availability
extraction_status
pages_extracted
candidate_count
blocked_reason
requires_manual_review
```

---

## 3. v3.7 Rerun Result

Command:

```txt
.\.venv\Scripts\python.exe -m phyng.campaigns.phi_gradient_pdf_text_extraction
```

Result:

```txt
status = PHI_GRADIENT_PDF_EXTRACTION_COMPLETED
hashed_sources_seen = 5
sources_extracted = 5
sources_blocked = 0
total_pages_extracted = 44
total_candidates = 548
```

Reader availability in:

```txt
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
```

is now:

```txt
fitz = true
pdfplumber = true
pymupdf = true
pypdf = true
```

Per-source extraction:

| Source ID | Status | Reader | Pages | Candidates | Blocked |
|---|---|---|---:|---:|---|
| `SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE` | `TEXT_EXTRACTED_PYMUPDF` | `pymupdf` | 4 | 61 | false |
| `SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE` | `TEXT_EXTRACTED_PYMUPDF` | `pymupdf` | 5 | 73 | false |
| `SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST` | `TEXT_EXTRACTED_PYMUPDF` | `pymupdf` | 5 | 79 | false |
| `SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS` | `TEXT_EXTRACTED_PYMUPDF` | `pymupdf` | 13 | 143 | false |
| `SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING` | `TEXT_EXTRACTED_PYMUPDF` | `pymupdf` | 17 | 192 | false |

Pedernales is no longer blocked by reader unavailability.

---

## 4. v3.8 Rerun Result

Command:

```txt
.\.venv\Scripts\python.exe -m phyng.campaigns.phi_gradient_extract_candidate_review
```

Result:

```txt
status = PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED
input_candidate_count = 548
validation_ready_count = 0
rejected_count = 227
manual_review_count = 321
pedernales_blocked = false
```

Interpretation:

```txt
The PDF reader integration recovered Pedernales text extraction.
The review gate still requires manual review.
No validation-ready extract was accepted.
No source support was granted.
```

---

## 5. Tests

Focused validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py
```

Result:

```txt
30 passed in 1.33s
```

Reader integration tests include:

```txt
test_reader_availability_detects_installed_libraries
test_pymupdf_reader_attempted_before_internal_parser
test_pdfplumber_reader_attempted_before_internal_parser
test_pypdf_reader_attempted_before_internal_parser
test_pedernales_block_reason_distinguishes_missing_reader_from_failed_reader
test_internal_parser_only_used_as_fallback
test_physical_claims_remain_blocked
```

Full-suite note:

```txt
The full pytest suite remains locally blocked by the pre-existing .venv NumPy C-extension DLL import error during older test collection.
This is unrelated to v3.8.1.
```

---

## 6. Final Discipline Note

```txt
Installed reader is not used reader.
Used reader is not clean extraction.
Clean extraction is not source support.
```

