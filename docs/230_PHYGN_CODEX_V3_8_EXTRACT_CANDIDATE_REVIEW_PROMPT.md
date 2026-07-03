# Codex Prompt — Phygn v3.8 Extract Candidate Review & Validation-Ready Pack Assembly

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
docs/225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
```

Therefore v3.8 starts at:

```txt
226
```

---

# 1. Read first

Read these v3.8 specs:

```txt
docs/226_PHYGN_V3_8_EXTRACT_CANDIDATE_REVIEW_docs/status/GOAL.md
docs/227_PHYGN_V3_8_REVIEW_DECISION_RULES.md
docs/228_PHYGN_V3_8_VALIDATION_READY_EXTRACT_PACK_SCHEMA.md
docs/229_PHYGN_V3_8_REPORTING_AND_NEXT_PRESSURE_GATE.md
```

Also read:

```txt
docs/225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
docs/219_PHYGN_V3_6_LOCAL_SOURCE_TEXT_REGISTRY_RESULTS.md
docs/213_PHYGN_V3_5_PRIORITY_EXACT_FILL_RESULTS.md
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
```

Inspect:

```txt
phyng/pdf_text_extraction/
phyng/local_source_text/
phyng/priority_exact_fill/
phyng/exact_extract_review/
phyng/source_pack_validation/
phyng/core/
phyng/closed_loop/
```

---

# 2. First action

Run focused tests first because the full suite may be locally blocked by unrelated NumPy DLL import errors:

```bash
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py
```

Then run new v3.8 tests after implementation.

Do not treat unrelated NumPy DLL collection failure as v3.8 failure.

---

# 3. Mission

Implement v3.8:

```txt
Extract Candidate Review
Garbage Candidate Rejection
Manual Review Queue
Component Role Mapping
Validation-Ready Extract Pack Assembly
Reviewed Candidate Map
Next Validation Gate Input
Canonical Reports
Tests
```

Do not validate PHI_GRADIENT.

Do not make physical claims.

---

# 4. Input files

Load:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/source_hashes_v3_6.json
```

If missing:

```txt
PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES
```

---

# 5. Extend package

Create or extend:

```txt
phyng/extract_candidate_review/
  __init__.py
  schemas.py
  loader.py
  review_rules.py
  role_assignment.py
  garbage_filter.py
  deduplication.py
  manual_review_queue.py
  validation_ready_pack.py
  report.py
  campaign.py
```

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_extract_candidate_review.py
```

---

# 6. Schemas

Implement:

```txt
ReviewedExtractionCandidate
ValidationReadyExtract
ValidationReadyExtractPack
RejectedExtractionCandidate
ManualReviewQueueItem
ReviewedCandidateMapEntry
PhiGradientExtractCandidateReviewGateResult
PhiGradientExtractCandidateReviewCampaignResult
```

Use existing:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 7. Review logic

Implement strict review logic:

```txt
reject empty/noisy/header/footer candidates
deduplicate repeated candidates
assign component role conservatively
send ambiguous candidates to manual review
accept validation-ready only if source_id, sha256, page/location and exact text are present
do not turn candidate into support
```

---

# 8. Pedernales handling

Because v3.7 blocked:

```txt
SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

v3.8 must create a HIGH priority manual-review item:

```txt
reason: PDF extraction blocked; SLOT_4 gradient-component bottleneck.
suggested_action: install pypdf/pdfplumber or manually extract relevant gradient/transition passages.
```

---

# 9. Output files

Create:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json
data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json
data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json
data/real_sources/extracts/phi_gradient_v3_8_next_validation_gate_inputs.json
```

---

# 10. Reports

Generate:

```txt
reports/extract_candidate_review/phi_gradient_candidate_review_summary_v3_8.md
reports/extract_candidate_review/phi_gradient_validation_ready_pack_v3_8.md
reports/extract_candidate_review/phi_gradient_rejected_candidates_v3_8.md
reports/extract_candidate_review/phi_gradient_manual_review_queue_v3_8.md
reports/extract_candidate_review/phi_gradient_component_role_map_v3_8.md
reports/extract_candidate_review/phi_gradient_next_pressure_gate_v3_8.md
reports/campaigns/PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8.md
```

Reports must include:

```txt
canonical status section
input candidate count
validation-ready count
rejected count
manual review count
component role counts
Pedernales blocked status
blocked claims
next actions
discipline note
```

---

# 11. Campaign statuses

```txt
PHI_GRADIENT_EXTRACT_REVIEW_COMPLETED
PHI_GRADIENT_EXTRACT_REVIEW_PARTIAL
PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION
PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_EXTRACT_REVIEW_NO_VALIDATION_READY_EXTRACTS
PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES
```

---

# 12. Tests

Create:

```txt
tests/test_extract_candidate_review_loader_v3_8.py
tests/test_extract_candidate_review_rules_v3_8.py
tests/test_extract_candidate_review_role_assignment_v3_8.py
tests/test_extract_candidate_review_pack_v3_8.py
tests/test_extract_candidate_review_reports_v3_8.py
tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py
```

Minimum tests:

```txt
test_missing_candidate_files_blocks_review
test_empty_or_noise_candidate_rejected
test_candidate_with_source_hash_and_location_can_be_validation_ready
test_ambiguous_equation_candidate_requires_manual_review
test_component_role_assigned_conservatively
test_pedernales_blocked_creates_high_priority_manual_review_item
test_validation_ready_pack_does_not_grant_support
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_existing_v3_7_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing v3.7 PDF/text extraction behavior
existing v3.6 local source registry behavior
existing v3.5 priority exact fill behavior
existing v3.4 exact extract review behavior
existing v3.3 source pack validation behavior
existing historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Reviewed candidate validates PHI_GRADIENT.
Validation-ready extract equals source support.
Equation candidate proves physical component.
Benchmark candidate proves benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed:

```txt
Extraction candidates were reviewed.
A validation-ready extract pack was assembled.
Candidates require v3.9 validation before source pressure.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
focused v3.7 tests pass
v3.8 tests pass
candidate files loaded
review logic works
manual review queue generated
validation-ready pack generated
reports generated
physical claims blocked
```

Expected focused total:

```txt
v3.7 focused tests + new v3.8 tests
```

---

# 16. Final discipline

```txt
A validation-ready extract is not support.
It is an object ready to be judged.
```
