# Phygn v3.8 - Extract Candidate Review Results

Date: 2026-07-01

Source prompt:

```txt
docs/230_PHYGN_CODEX_V3_8_EXTRACT_CANDIDATE_REVIEW_PROMPT.md
```

Supporting specs:

```txt
docs/226_PHYGN_V3_8_EXTRACT_CANDIDATE_REVIEW_docs/status/GOAL.md
docs/227_PHYGN_V3_8_REVIEW_DECISION_RULES.md
docs/228_PHYGN_V3_8_VALIDATION_READY_EXTRACT_PACK_SCHEMA.md
docs/229_PHYGN_V3_8_REPORTING_AND_NEXT_PRESSURE_GATE.md
docs/225_PHYGN_V3_7_EXACT_PDF_TEXT_EXTRACTION_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER v3.8 PROMPT SPECIFICATIONS WITH MANUAL REVIEW REQUIRED**

Final campaign status:

```txt
PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED
```

Interpretation:

```txt
The v3.7 extraction candidate files were loaded.
The v3.6 source hash boundary was preserved.
Raw candidates were reviewed into rejected and manual-review buckets.
No candidate was promoted to source support.
No validation-ready extract was accepted from the current real extraction output.
Pedernales remains a high-priority manual-review bottleneck.
No physical claim was upgraded.
```

Validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_pdf_text_extraction_registry_boundary_v3_7.py tests/test_pdf_text_extraction_page_reader_v3_7.py tests/test_pdf_text_extraction_candidate_detection_v3_7.py tests/test_pdf_text_extraction_reports_v3_7.py tests/test_phi_gradient_pdf_text_extraction_campaign_v3_7.py tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py
24 passed in 1.03s
```

Focused v3.8 validation:

```txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_extract_candidate_review_loader_v3_8.py tests/test_extract_candidate_review_rules_v3_8.py tests/test_extract_candidate_review_role_assignment_v3_8.py tests/test_extract_candidate_review_pack_v3_8.py tests/test_extract_candidate_review_reports_v3_8.py tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py
11 passed in 0.67s
```

Full-suite note:

```txt
The full pytest suite remains locally blocked by the pre-existing .venv NumPy C-extension DLL import error.
This is unrelated to v3.8 and occurs during collection of older tests.
```

---

## 2. New Package and Campaign

Created:

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

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_extract_candidate_review.py
```

Entrypoint:

```python
run_phi_gradient_extract_candidate_review_campaign(root: str | Path = ".")
```

---

## 3. Input Candidate Review

Loaded:

```txt
data/real_sources/extracts/phi_gradient_pdf_text_extraction_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_quote_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_equation_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_table_range_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_negative_constraint_candidates_v3_7.json
data/real_sources/extracts/phi_gradient_pdf_extraction_manifest_v3_7.json
data/real_sources/source_hashes_v3_6.json
```

Boundary preserved:

```txt
Candidates whose source_id or sha256 do not match the v3.6 source hash manifest are ignored.
```

---

## 4. Campaign Metrics

Final campaign report:

```txt
reports/campaigns/PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8.md
```

Summary:

| Metric | Result |
|---|---:|
| Input candidates | 33 |
| Validation-ready extracts | 0 |
| Rejected candidates | 25 |
| Manual-review queue items | 9 |
| Pedernales blocked | true |

Component role counts:

| Component role | Count |
|---|---:|
| `BENCHMARK_MODEL` | 6 |
| `REQUIRES_MANUAL_REVIEW` | 2 |
| `REJECTED_GARBAGE` | 25 |
| `GRADIENT_COMPONENT` | 1 |

Interpretation:

```txt
Most raw v3.7 candidates were rejected because PDF stream extraction produced noisy or damaged text.
The reviewable candidates remain manual-review items.
The current real output has no validation-ready extract.
```

---

## 5. Pedernales Handling

v3.8 created the required high-priority manual-review item:

```txt
candidate_id: MANUAL-PEDERNALES-SLOT-4-GRADIENT-COMPONENT
source_id: SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
priority: HIGH
reason: PDF extraction blocked; SLOT_4 gradient-component bottleneck.
suggested_action: install pypdf/pdfplumber or manually extract relevant gradient/transition passages.
```

This item is not evidence support.

---

## 6. Generated Data Artifacts

Created:

```txt
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8.json
data/real_sources/extracts/phi_gradient_rejected_extraction_candidates_v3_8.json
data/real_sources/extracts/phi_gradient_manual_review_queue_v3_8.json
data/real_sources/extracts/phi_gradient_reviewed_candidate_map_v3_8.json
data/real_sources/extracts/phi_gradient_v3_8_next_validation_gate_inputs.json
```

Validation-ready pack result:

```txt
validation_ready_count = 0
extracts = []
```

Manual review queue result:

```txt
manual_review_count = 9
```

Rejected candidate result:

```txt
rejected_count = 25
```

---

## 7. Generated Reports

Created:

```txt
reports/extract_candidate_review/phi_gradient_candidate_review_summary_v3_8.md
reports/extract_candidate_review/phi_gradient_validation_ready_pack_v3_8.md
reports/extract_candidate_review/phi_gradient_rejected_candidates_v3_8.md
reports/extract_candidate_review/phi_gradient_manual_review_queue_v3_8.md
reports/extract_candidate_review/phi_gradient_component_role_map_v3_8.md
reports/extract_candidate_review/phi_gradient_next_pressure_gate_v3_8.md
reports/campaigns/PHI-GRADIENT-EXTRACT-CANDIDATE-REVIEW-v3_8.md
```

All generated reports include the canonical status section.

---

## 8. Canonical Status Mapping

Added conservative canonical statuses in:

```txt
phyng/core/status_mapping.py
```

Statuses:

```txt
PHI_GRADIENT_EXTRACT_REVIEW_COMPLETED
PHI_GRADIENT_EXTRACT_REVIEW_PARTIAL
PHI_GRADIENT_EXTRACT_REVIEW_READY_FOR_VALIDATION
PHI_GRADIENT_EXTRACT_REVIEW_MANUAL_REVIEW_REQUIRED
PHI_GRADIENT_EXTRACT_REVIEW_NO_VALIDATION_READY_EXTRACTS
PHI_GRADIENT_EXTRACT_REVIEW_BLOCKED_MISSING_CANDIDATES
```

The active status maps to:

```txt
Canonical Permission: REVIEW_REQUIRED
Blocked Reasons: HUMAN_REVIEW_REQUIRED, MISSING_SOURCE_SUPPORT
Evidence Level: SYNTHETIC_ONLY
Support Level: SYNTHETIC
Risk Level: TECHNICAL_RISK
```

---

## 9. New Tests

Created:

```txt
tests/test_extract_candidate_review_loader_v3_8.py
tests/test_extract_candidate_review_rules_v3_8.py
tests/test_extract_candidate_review_role_assignment_v3_8.py
tests/test_extract_candidate_review_pack_v3_8.py
tests/test_extract_candidate_review_reports_v3_8.py
tests/test_phi_gradient_extract_candidate_review_campaign_v3_8.py
```

Coverage includes:

| Test | Purpose |
|---|---|
| `test_missing_candidate_files_blocks_review` | Confirms missing inputs block v3.8 |
| `test_empty_or_noise_candidate_rejected` | Confirms garbage rejection |
| `test_candidate_with_source_hash_and_location_can_be_validation_ready` | Confirms clean structural candidate can enter validation-ready pack |
| `test_ambiguous_equation_candidate_requires_manual_review` | Confirms equation ambiguity is queued |
| `test_component_role_assigned_conservatively` | Confirms gradient vs analogy separation |
| `test_pedernales_blocked_creates_high_priority_manual_review_item` | Confirms Pedernales SLOT_4 queue requirement |
| `test_validation_ready_pack_does_not_grant_support` | Confirms pack is not support |
| `test_reports_include_canonical_section` | Confirms report contract integration |
| `test_physical_claims_remain_blocked` | Confirms blocked claim discipline |
| `test_existing_v3_7_behavior_preserved` | Confirms v3.7 status semantics remain unchanged |

---

## 10. Behavior Preservation

v3.8 did not alter:

```txt
v3.7 PDF/text extraction behavior
v3.6 local source registry behavior
v3.5 priority exact fill behavior
v3.4 exact extract review behavior
v3.3 source pack validation behavior
historical reports
```

Preservation evidence:

```txt
24 passed in 1.03s
```

for focused v3.7 + v3.8 tests.

---

## 11. Blocked Claims

The campaign explicitly blocks:

```txt
Reviewed candidate validates PHI_GRADIENT.
Validation-ready extract equals source support.
Equation candidate proves physical component.
Benchmark candidate proves benchmark support.
PHI_GRADIENT is physically validated.
Frontera C is validated.
```

Allowed statements:

```txt
Extraction candidates were reviewed.
A validation-ready extract pack was assembled.
Some candidates were rejected or queued for manual review.
```

---

## 12. Next Gate

Recommended next action:

```txt
Resolve manual-review queue, especially Pedernales SLOT_4, before source-pressure decisions.
```

Recommended technical improvement:

```txt
Install pypdf or pdfplumber, rerun v3.7, then rerun v3.8.
```

Recommended next phase after manual review or cleaner extraction:

```txt
v3.9 - Validation-Ready Extract Gate & First Source-Pressure Decision
```

v3.9 must not proceed as a positive pressure gate until there are validation-ready extracts.

---

## 13. Final Assessment

v3.8 did its job by refusing to convert noisy extraction output into evidence-ready material.

The useful result is:

```txt
Current raw PDF extraction is not clean enough for validation-ready source pressure.
Pedernales remains the key gradient-component bottleneck.
Manual review or better PDF extraction is required before v3.9 can judge source pressure.
```

Final discipline note:

```txt
A validation-ready extract is not support.
It is an object ready to be judged.
```
