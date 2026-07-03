# Phygn v3.3 - PHI_GRADIENT Source Pack Extract Validation & Slot Coverage Results

Date: 2026-06-30

Source prompt:

```txt
docs/200_PHYGN_CODEX_V3_3_SOURCE_PACK_VALIDATION_PROMPT.md
```

Supporting specs:

```txt
docs/196_PHYGN_V3_3_SOURCE_PACK_EXTRACT_VALIDATION_docs/status/GOAL.md
docs/197_PHYGN_EXTRACT_VALIDATION_DECISION_RULES.md
docs/198_PHYGN_SLOT_COVERAGE_SCORING_PROTOCOL.md
docs/199_PHYGN_V3_3_REPORTING_AND_LOOP_FEEDBACK.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v3.3 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v3.3 loaded the v3.2 seed source pack and ran strict extract validation and slot coverage scoring.

No manual-review seed extract was promoted to support.

No benchmark candidate was promoted to benchmark support.

No physical validation claim was unlocked.

Final campaign status:

```txt
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
```

Final validation:

```txt
pytest -q
645 passed in 44.70s
```

Baseline before v3.3:

```txt
633 passed
```

Net result:

```txt
633 baseline tests + 12 v3.3 tests = 645 passing tests
```

---

## 2. Implemented Package

Created:

```txt
phyng/source_pack_validation/
  __init__.py
  schemas.py
  loader.py
  extract_validator.py
  slot_scoring.py
  analogy_rejection.py
  negative_pressure.py
  benchmark_scoring.py
  final_gate.py
  report.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_source_pack_validation.py
```

Entrypoint:

```python
run_phi_gradient_source_pack_validation_campaign(root: str | Path = ".")
```

---

## 3. Inputs Loaded

Loaded:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

Input summary:

| Metric | Result |
|---|---:|
| Manifest sources | 13 |
| Extract candidates | 8 |
| Manual-review seed extracts | 8 |
| Exact reviewed support extracts | 0 |

---

## 4. Extract Validation Results

Generated report:

```txt
reports/source_pack_validation/phi_gradient_extract_validation_v3_3.md
```

Default seed validation result:

| Metric | Result |
|---|---:|
| Extract candidates validated | 8 |
| Validated support count | 0 |
| Manual review count | 8 |
| Rejected analogy count | 0 |
| Negative pressure count | 0 |
| Benchmark comparable count | 0 |

All default v3.2 seed extracts had:

```txt
manual_review_required=true
initial_validation_status=EXTRACT_CANDIDATE_REQUIRES_REVIEW
exact_quote_available=false
```

Therefore all default seed extracts remained:

```txt
EXTRACT_REQUIRES_MANUAL_REVIEW
```

Preserved rule:

```txt
Manual-review extract counts as support = false
```

---

## 5. Slot Coverage Scoring

Generated report:

```txt
reports/source_pack_validation/phi_gradient_slot_coverage_v3_3.md
```

Slot coverage summary:

| Metric | Result |
|---|---:|
| Source pressure score | 0.0 |
| Manual review debt | 8 |
| Validated support slots | 0 |
| Benchmark comparable slots | 0 |
| Contradicted slots | 0 |

Coverage statuses include:

```txt
SLOT_UNTOUCHED
SLOT_CANDIDATES_FOUND
SLOT_ANALOGY_ONLY
SLOT_REQUIRES_MANUAL_REVIEW
SLOT_PARTIALLY_COVERED
SLOT_COVERED_LIMITED
SLOT_CONTRADICTED
SLOT_BENCHMARK_COMPARABLE
```

Default interpretation:

```txt
The topology contains candidate pressure and manual-review debt, but no validated slot support.
```

---

## 6. Analogy, Negative and Benchmark Results

Generated reports:

```txt
reports/source_pack_validation/phi_gradient_analogy_rejections_v3_3.md
reports/source_pack_validation/phi_gradient_negative_pressure_v3_3.md
reports/source_pack_validation/phi_gradient_benchmark_comparability_v3_3.md
```

Default results:

```txt
rejected_analogy_count=0
negative_pressure_count=0
benchmark_comparable_count=0
benchmark_status=BENCHMARK_COMPARABLE_RECORD_MISSING
```

Important limitation:

```txt
Negative candidate sources and benchmark candidate sources exist in the v3.2 seed pack,
but v3.3 does not count them until exact extracts survive validation.
```

---

## 7. Final Gate

Generated report:

```txt
reports/source_pack_validation/phi_gradient_final_gate_v3_3.md
```

Final status:

```txt
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
```

Canonical interpretation:

```txt
permission=REVIEW_REQUIRED
evidence_level=SYNTHETIC_ONLY
support_level=SYNTHETIC
blocked_reasons=MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK
```

Allowed claim:

```txt
Extract validation was completed; manual review debt remains.
```

Blocked claims:

```txt
Seed extract validation proves PHI_GRADIENT.
Manual-review extract counts as support.
Benchmark candidate counts as benchmark data.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
Experimental confirmation.
Benchmark-supported claim.
Source-backed claim.
```

---

## 8. Reports Generated

The v3.3 campaign generated:

```txt
reports/source_pack_validation/phi_gradient_extract_validation_v3_3.md
reports/source_pack_validation/phi_gradient_slot_coverage_v3_3.md
reports/source_pack_validation/phi_gradient_analogy_rejections_v3_3.md
reports/source_pack_validation/phi_gradient_negative_pressure_v3_3.md
reports/source_pack_validation/phi_gradient_benchmark_comparability_v3_3.md
reports/source_pack_validation/phi_gradient_final_gate_v3_3.md
reports/source_pack_validation/phi_gradient_loop_feedback_v3_3.md
reports/campaigns/PHI-GRADIENT-SOURCE-PACK-VALIDATION-v3_3.md
```

This document consolidates the result into:

```txt
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
```

---

## 9. New Tests

Created:

```txt
tests/test_source_pack_validation_extracts_v3_3.py
tests/test_source_pack_validation_slot_scoring_v3_3.py
tests/test_source_pack_validation_negative_pressure_v3_3.py
tests/test_source_pack_validation_benchmark_scoring_v3_3.py
tests/test_source_pack_validation_reports_v3_3.py
tests/test_phi_gradient_source_pack_validation_campaign_v3_3.py
```

Focused v3.3 verification:

```txt
pytest -q tests/test_source_pack_validation_extracts_v3_3.py tests/test_source_pack_validation_slot_scoring_v3_3.py tests/test_source_pack_validation_negative_pressure_v3_3.py tests/test_source_pack_validation_benchmark_scoring_v3_3.py tests/test_source_pack_validation_reports_v3_3.py tests/test_phi_gradient_source_pack_validation_campaign_v3_3.py
12 passed in 0.89s
```

Full-suite verification:

```txt
pytest -q
645 passed in 44.70s
```

---

## 10. Behavior Preservation

v3.3 explicitly preserved v3.2 behavior:

```txt
test_existing_v3_2_behavior_preserved
```

Result:

```txt
PHI_GRADIENT_SOURCE_PACK_POPULATED
extract_count=8
```

Historical behavior preservation remains covered by the existing suite for:

```txt
v3.1 reviewed manifest
v3.0 real source acquisition
v2.9 real source ingestion
v2.8 source pressure
v2.7 phi search outputs
v2.6 ablation outputs
v2.5 synthetic execution
```

---

## 11. Final Assessment

v3.3 successfully moved the system from source-pack population to source-pack validation.

The current source pack still has no validated support because all v3.2 extracts are manual-review seed paraphrases.

Correct current state:

```txt
validation completed
validated source support = 0
benchmark comparable support = 0
manual review debt = 8
physical claims blocked
```

The next meaningful move is:

```txt
Replace seed paraphrases with exact reviewed extracts, quotes, equations,
observables, parameter ranges, benchmark values and limitations, then rerun v3.3.
```

Final discipline note:

```txt
A candidate source becomes evidence pressure only when its extract survives the gate.
```
