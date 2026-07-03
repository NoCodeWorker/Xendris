# Phygn v3.7 — PDF Extraction Boundary & Method Protocol

## 0. Purpose

This document defines how Phygn extracts text from local PDFs without overclaiming.

---

## 1. Boundary

Only extract from files satisfying:

```txt
exists = true
sha256 is not null
file_type = .pdf or supported text type
source_id is registered
local_path is inside data/real_sources/pdfs/
```

If a file lacks hash:

```txt
EXTRACTION_BLOCKED_UNHASHED_SOURCE
```

If a file exists but is unsupported:

```txt
EXTRACTION_BLOCKED_UNSUPPORTED_FILE_TYPE
```

---

## 2. Preferred extraction order

Use deterministic extraction in this order:

```txt
1. embedded text extraction
2. page-level text segmentation
3. equation/keyword candidate detection
4. table/figure caption candidate detection
5. manual-review fallback
```

Do not use OCR by default.

If OCR would be needed, mark:

```txt
EXTRACTION_REQUIRES_OCR_OR_MANUAL_REVIEW
```

---

## 3. Extraction libraries

Preferred libraries if available:

```txt
pypdf
PyMuPDF / fitz
pdfplumber
```

Fallback:

```txt
plain text copy if .txt/.md/.html
manual review required
```

Do not add heavy dependencies without project approval.

---

## 4. Page record schema

```python
class ExtractedPageText(BaseModel):
    source_id: str
    sha256: str
    local_path: str
    page_number: int
    text: str
    extraction_method: str
    extraction_status: str
```

---

## 5. Candidate extraction schema

```python
class PDFExtractionCandidate(BaseModel):
    candidate_id: str
    source_id: str
    sha256: str
    page_number: int | None
    location_type: str
    location_value: str
    candidate_type: str
    extracted_text: str
    normalized_text: str | None
    confidence: str
    requires_manual_review: bool
    notes: list[str]
```

Candidate types:

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

## 6. Candidate detection keywords

Baseline/observable:

```txt
visibility
fringe
contrast
decoherence
coherence
interference
rate
loss
```

Benchmark/range:

```txt
mass
amu
separation
distance
time
free fall
temperature
pressure
visibility
decoherence rate
```

Parameter/constraint:

```txt
lambda
collapse
CSL
bound
constraint
exclusion
parameter
Bayesian
hypothesis
```

Gradient/component:

```txt
gradient
field gradient
transition
operator
dynamical decoupling
effective
rate
```

Negative pressure:

```txt
dominates
negligible
excluded
ruled out
background
environmental
thermal
scattering
```

---

## 7. Anti-fabrication rule

The extractor may only output text present in the local file.

If extraction is uncertain:

```txt
requires_manual_review = true
```

---

## 8. Final principle

```txt
The extractor finds candidates.
It does not decide truth.
```
