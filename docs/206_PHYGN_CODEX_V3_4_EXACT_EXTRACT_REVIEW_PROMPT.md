# Codex Prompt — Phygn v3.4 Exact Extract Acquisition & Quote-Level Source Review

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
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
```

Therefore v3.4 starts at:

```txt
202
```

---

# 1. Read first

Read these v3.4 specs:

```txt
docs/202_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_docs/status/GOAL.md
docs/203_PHYGN_EXACT_EXTRACT_SCHEMA_AND_LOCATION_CONTRACT.md
docs/204_PHYGN_EQUATION_OBSERVABLE_PARAMETER_MAPPING.md
docs/205_PHYGN_V3_4_REPORTING_AND_NEXT_GATE.md
```

Also read:

```txt
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
```

Inspect:

```txt
phyng/source_pack_validation/
phyng/source_pack_population/
phyng/reviewed_manifest/
phyng/real_source_ingestion/
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
645 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.4:

```txt
Exact Extract Acquisition
Quote-Level Source Review
Location Contract
Equation/Observable Mapping
Parameter/Benchmark Range Mapping
Manual Review Debt Resolution
Canonical Reports
Next Gate Preparation
Tests
```

Do not make physical claims.

---

# 4. Input files

Load:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_2.seed.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_2.seed.json
```

If missing, return:

```txt
PHI_GRADIENT_EXACT_EXTRACT_REVIEW_BLOCKED
```

Do not invent replacement sources.

---

# 5. Extend package

Create or extend:

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

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_exact_extract_review.py
```

---

# 6. Schemas

Implement:

```txt
ExactReviewedExtract
ExactReviewedExtractPack
ExactExtractLocationValidationResult
EquationObservableMapEntry
EquationObservableMap
ParameterRangeMapEntry
ParameterRangeMap
PhiGradientExactExtractReviewGateResult
PhiGradientExactExtractReviewCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 7. Important implementation boundary

Do not browse the web from inside the code unless an approved acquisition backend already exists.

If only seed paraphrases exist, create a reviewed extract pack that preserves unresolved debt:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
```

If exact extracts are manually supplied, validate their location and exact fields.

Do not fabricate quotes, equations, page numbers or ranges.

---

# 8. Exact extract rules

A validation-ready extract requires:

```txt
source_id exists in manifest
slot_id is valid
location_type is not UNKNOWN_LOCATION_REQUIRES_REVIEW
location_value is non-empty
at least one exact content field is non-empty
manual_review_required is false
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

---

# 9. Mapping rules

Create:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_4.reviewed.json
data/real_sources/extracts/phi_gradient_exact_extract_locations_v3_4.json
data/real_sources/extracts/phi_gradient_equation_observable_map_v3_4.json
data/real_sources/extracts/phi_gradient_parameter_range_map_v3_4.json
```

If no exact content exists, these files may be empty or unresolved templates, but reports must say so explicitly.

---

# 10. Campaign status rules

If seed files missing:

```txt
PHI_GRADIENT_EXACT_EXTRACT_REVIEW_BLOCKED
```

If exact extracts absent:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_REQUIRE_MORE_REVIEW
```

If some exact extracts acquired but incomplete:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_PARTIAL
```

If exact extracts acquired and validation-ready:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_ACQUIRED
```

If exact content has no validatable component:

```txt
PHI_GRADIENT_EXACT_EXTRACTS_NO_VALIDATABLE_CONTENT
```

---

# 11. Reports

Generate:

```txt
reports/exact_extract_review/phi_gradient_exact_extracts_v3_4.md
reports/exact_extract_review/phi_gradient_exact_extract_locations_v3_4.md
reports/exact_extract_review/phi_gradient_equation_observable_map_v3_4.md
reports/exact_extract_review/phi_gradient_parameter_ranges_v3_4.md
reports/exact_extract_review/phi_gradient_manual_review_resolution_v3_4.md
reports/exact_extract_review/phi_gradient_next_gate_v3_4.md
reports/campaigns/PHI-GRADIENT-EXACT-EXTRACT-REVIEW-v3_4.md
```

Reports must include:

```txt
canonical status section
manual review debt before
manual review debt after
validation-ready extracts
unresolved extracts
equation map count
observable map count
parameter range count
benchmark range count
negative constraint count
blocked claims
next actions
discipline note
```

---

# 12. Tests

Create:

```txt
tests/test_exact_extract_schema_v3_4.py
tests/test_exact_extract_location_validation_v3_4.py
tests/test_exact_extract_mapping_v3_4.py
tests/test_exact_extract_review_gate_v3_4.py
tests/test_exact_extract_reports_v3_4.py
tests/test_phi_gradient_exact_extract_review_campaign_v3_4.py
```

Minimum tests:

```txt
test_seed_paraphrases_do_not_become_exact_extracts
test_exact_extract_requires_location
test_exact_extract_requires_exact_content
test_validation_ready_requires_manual_review_false
test_equation_observable_map_requires_exact_extract
test_parameter_range_map_requires_exact_values
test_no_fabricated_quote_or_range
test_missing_seed_files_blocks_review
test_exact_extracts_partial_status_when_some_ready
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v3_3_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing v3.3 source pack validation behavior
existing v3.2 source pack population behavior
existing v3.1 reviewed manifest behavior
existing v3.0 real source acquisition behavior
existing v2.9 real source ingestion behavior
existing v2.8 source pressure behavior
existing v2.7 phi search outputs
existing v2.6 ablation results
existing v2.5 synthetic execution outputs
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Exact extract review validates PHI_GRADIENT.
A located quote is source support by itself.
A located benchmark mention is benchmark data.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
Exact extracts were acquired or remain unresolved.
Some extracts may be validation-ready for the next gate.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
seed files are loaded
exact extract schema works
location validation works
mapping files generated
reports generated
loop feedback generated
physical claims blocked
paraphrases do not auto-promote
```

Expected test count:

```txt
645 + new v3.4 tests
```

---

# 16. Final discipline

```txt
Exactness is the price a source pays to become pressure.
```
