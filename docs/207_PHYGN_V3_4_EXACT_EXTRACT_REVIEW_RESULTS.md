# Phygn v3.4 - PHI_GRADIENT Exact Extract Review Results

Date: 2026-06-30

Source prompt:

```txt
docs/206_PHYGN_CODEX_V3_4_EXACT_EXTRACT_REVIEW_PROMPT.md
```

Supporting specs:

```txt
docs/202_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_docs/status/GOAL.md
docs/203_PHYGN_EXACT_EXTRACT_SCHEMA_AND_LOCATION_CONTRACT.md
docs/204_PHYGN_EQUATION_OBSERVABLE_PARAMETER_MAPPING.md
docs/205_PHYGN_V3_4_REPORTING_AND_NEXT_GATE.md
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v3.4 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v3.4 loaded the v3.2 seed source pack and generated quote-level exact extract review artifacts.

No source text was fetched by code.

No quotes, equations, page numbers, sections or ranges were fabricated.

No paraphrase was promoted to an exact extract.

No physical validation claim was unlocked.

Final campaign status:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
```

Final validation:

```txt
pytest -q
658 passed in 44.67s
```

Baseline before v3.4:

```txt
645 passed
```

Net result:

```txt
645 baseline tests + 13 v3.4 tests = 658 passing tests
```

---

## 2. Implemented Package

Created:

```txt
phyng/exact_extract_review/
  __init__.py
  schemas.py
  loader.py
  exact_extracts.py
  location_validation.py
  equation_observable_map.py
  parameter_range_map.py
  review_gate.py
  report.py
  campaign.py
```

Created campaign wrapper:

```txt
phyng/campaigns/phi_gradient_exact_extract_review.py
```

Entrypoint:

```python
run_phi_gradient_exact_extract_review_campaign(root: str | Path = ".")
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
| Seed manifest entries | 13 |
| Seed extract candidates | 8 |
| Manual review debt before | 8 |

---

## 4. Output Files Generated

Created:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_4.reviewed.json
data/real_sources/extracts/phi_gradient_exact_extract_locations_v3_4.json
data/real_sources/extracts/phi_gradient_equation_observable_map_v3_4.json
data/real_sources/extracts/phi_gradient_parameter_range_map_v3_4.json
```

Default output summary:

| Metric | Result |
|---|---:|
| Exact review records | 8 |
| Validation-ready extracts | 0 |
| Unresolved extracts | 8 |
| Equation map count | 0 |
| Observable map count | 0 |
| Parameter range count | 0 |
| Benchmark range count | 0 |
| Negative constraint count | 0 |
| Manual review debt after | 8 |

Interpretation:

```txt
The files are unresolved review templates. They do not contain fabricated exact content.
```

---

## 5. Exact Extract Contract

Implemented in:

```txt
phyng/exact_extract_review/schemas.py
phyng/exact_extract_review/location_validation.py
```

Validation-ready extract requirements:

```txt
source_id exists in manifest
slot_id is valid
location_type is known
location_value is non-empty
at least one exact content field is non-empty
manual_review_required=false
```

Exact content fields:

```txt
exact_quote
equation_text
observable_text
parameter_range_text
benchmark_range_text
negative_constraint_text
```

Default seed-derived outputs fail validation-readiness because:

```txt
location_type=UNKNOWN_LOCATION_REQUIRES_REVIEW
location_value=""
exact content fields are empty
manual_review_required=true
```

---

## 6. Mapping Results

Implemented in:

```txt
phyng/exact_extract_review/equation_observable_map.py
phyng/exact_extract_review/parameter_range_map.py
```

Default maps:

```txt
equation_observable_map.entries=[]
parameter_range_map.entries=[]
```

Reason:

```txt
No extract is validation-ready and no exact equation, observable, parameter range or benchmark range exists.
```

---

## 7. Reports Generated

The v3.4 campaign generated:

```txt
reports/exact_extract_review/phi_gradient_exact_extracts_v3_4.md
reports/exact_extract_review/phi_gradient_exact_extract_locations_v3_4.md
reports/exact_extract_review/phi_gradient_equation_observable_map_v3_4.md
reports/exact_extract_review/phi_gradient_parameter_ranges_v3_4.md
reports/exact_extract_review/phi_gradient_manual_review_resolution_v3_4.md
reports/exact_extract_review/phi_gradient_next_gate_v3_4.md
reports/campaigns/PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4.md
```

This document consolidates the result into:

```txt
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
```

---

## 8. Gate Results

Final status:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
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
Exact extract review templates were generated and unresolved review debt was measured.
```

Blocked claims:

```txt
Exact extract review validates PHI_GRADIENT.
A located quote is source support by itself.
A located benchmark mention is benchmark data.
PHI_GRADIENT has real source support.
PHI_GRADIENT has benchmark support.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
```

---

## 9. New Tests

Created:

```txt
tests/test_exact_extract_schema_v3_4.py
tests/test_exact_extract_location_validation_v3_4.py
tests/test_exact_extract_mapping_v3_4.py
tests/test_exact_extract_review_gate_v3_4.py
tests/test_exact_extract_reports_v3_4.py
tests/test_phi_gradient_exact_extract_review_campaign_v3_4.py
```

Focused v3.4 verification:

```txt
pytest -q tests/test_exact_extract_schema_v3_4.py tests/test_exact_extract_location_validation_v3_4.py tests/test_exact_extract_mapping_v3_4.py tests/test_exact_extract_review_gate_v3_4.py tests/test_exact_extract_reports_v3_4.py tests/test_phi_gradient_exact_extract_review_campaign_v3_4.py
13 passed in 0.86s
```

Full-suite verification:

```txt
pytest -q
658 passed in 44.67s
```

---

## 10. Behavior Preservation

v3.4 explicitly preserved v3.3 behavior:

```txt
test_existing_v3_3_behavior_preserved
```

Result:

```txt
PHI_GRADIENT_EXTRACT_VALIDATION_COMPLETED
validated_support_count=0
```

Historical behavior preservation remains covered by the existing suite for:

```txt
v3.2 source pack population
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

v3.4 prepared the exact-extract review layer, but did not resolve manual-review debt because no exact reviewed source text was supplied.

Correct current state:

```txt
exact review templates generated
validation-ready extracts = 0
manual review debt before = 8
manual review debt after = 8
real source support = 0
benchmark support = 0
physical claims blocked
```

The next meaningful move is:

```txt
Manually fill exact quotes, locations, equations, observables, parameter ranges,
benchmark ranges and limitations in the v3.4 reviewed extract pack, then run v3.5.
```

Final discipline note:

```txt
Exactness is the price a source pays to become pressure.
```
