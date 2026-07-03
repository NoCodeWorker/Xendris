# Codex Prompt — Phygn v3.5 Priority Exact Extract Fill: Baseline, Benchmark & Gradient Review

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
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
```

Therefore v3.5 starts at:

```txt
208
```

---

# 1. Read first

Read these v3.5 specs:

```txt
docs/208_PHYGN_V3_5_PRIORITY_EXACT_EXTRACT_FILL_docs/status/GOAL.md
docs/209_PHYGN_PRIORITY_SOURCE_REVIEW_PROTOCOL.md
docs/210_PHYGN_PRIORITY_EXACT_FILL_SCHEMA_AND_FILES.md
docs/211_PHYGN_V3_5_REPORTING_AND_NEXT_DECISION.md
```

Also read:

```txt
docs/207_PHYGN_V3_4_EXACT_EXTRACT_REVIEW_RESULTS.md
docs/201_PHYGN_V3_3_SOURCE_PACK_VALIDATION_RESULTS.md
docs/195_PHYGN_V3_2_REVIEWED_REAL_SOURCE_PACK_RESULTS.md
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
```

Inspect:

```txt
phyng/exact_extract_review/
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
658 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.5:

```txt
Priority Source Review
Priority Exact Extract Fill
Source Text Availability Classification
Exact Location/Quote/Equation/Range Fill Records
Equation/Observable Mapping
Parameter/Benchmark Range Mapping
Risk and Negative Pressure Notes
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
data/real_sources/extracts/phi_gradient_extract_pack_v3_4.reviewed.json
```

If missing, return:

```txt
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED
```

Do not invent replacement sources.

---

# 5. Priority sources

Prioritize:

```txt
SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE
SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE
SRC-NIMMRICHTER-2011-CSL-MATTER-WAVE-TEST
SRC-SCHRINSKI-2020-QC-HYPOTHESIS-TESTS
SRC-PEDERNALES-2019-MOTIONAL-DYNAMICAL-DECOUPLING
```

Do not process all sources unless the priority set is complete.

---

# 6. Extend package

Create or extend:

```txt
phyng/priority_exact_fill/
  __init__.py
  schemas.py
  loader.py
  source_availability.py
  priority_fill.py
  equation_observable_map.py
  parameter_range_map.py
  review_gate.py
  report.py
  campaign.py
```

Create campaign wrapper:

```txt
phyng/campaigns/phi_gradient_priority_exact_fill.py
```

---

# 7. Output files

Create:

```txt
data/real_sources/extracts/phi_gradient_priority_exact_extracts_v3_5.json
data/real_sources/extracts/phi_gradient_priority_exact_extract_locations_v3_5.json
data/real_sources/extracts/phi_gradient_priority_equation_observable_map_v3_5.json
data/real_sources/extracts/phi_gradient_priority_parameter_range_map_v3_5.json
data/real_sources/extracts/phi_gradient_priority_review_notes_v3_5.md
```

---

# 8. Source text boundary

Do not browse the web or fabricate source text.

If source text is not locally available or manually supplied, create unresolved records:

```txt
source_text_status = SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD
review_status = EXACT_FILL_REQUIRES_SOURCE_TEXT
validation_ready = false
```

If exact source text is available locally, extract only from that text.

---

# 9. Validation-ready rule

A fill record is validation-ready only if:

```txt
source_text_status indicates available text
location_type is known
location_value is non-empty
at least one exact content field is non-empty
review_status is not unresolved
validation_ready = true
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

# 10. Campaign status rules

If seed files missing:

```txt
PHI_GRADIENT_PRIORITY_EXTRACT_FILL_BLOCKED
```

If all priority sources require source text:

```txt
PHI_GRADIENT_PRIORITY_EXTRACTS_REQUIRE_SOURCE_TEXT
```

If some exact fills are ready:

```txt
PHI_GRADIENT_PRIORITY_EXTRACTS_PARTIAL
```

If all priority fills are ready:

```txt
PHI_GRADIENT_PRIORITY_EXTRACTS_ACQUIRED
```

If reviewed exact content has no validatable component:

```txt
PHI_GRADIENT_PRIORITY_EXTRACTS_NO_VALIDATABLE_CONTENT
```

---

# 11. Reports

Generate:

```txt
reports/priority_exact_fill/phi_gradient_priority_source_review_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_exact_extracts_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_locations_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_equation_observable_map_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_parameter_ranges_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_risk_and_negative_pressure_v3_5.md
reports/priority_exact_fill/phi_gradient_priority_next_gate_v3_5.md
reports/campaigns/PHI-GRADIENT-PRIORITY-EXACT-FILL-v3_5.md
```

Reports must include:

```txt
canonical status section
priority sources processed
source text availability
validation-ready count
unresolved count
risk flags
negative candidates
blocked claims
next actions
discipline note
```

---

# 12. Tests

Create:

```txt
tests/test_priority_exact_fill_schema_v3_5.py
tests/test_priority_source_availability_v3_5.py
tests/test_priority_exact_fill_records_v3_5.py
tests/test_priority_exact_fill_mapping_v3_5.py
tests/test_priority_exact_fill_reports_v3_5.py
tests/test_phi_gradient_priority_exact_fill_campaign_v3_5.py
```

Minimum tests:

```txt
test_priority_sources_are_selected
test_source_text_unavailable_does_not_fabricate_extract
test_unresolved_priority_record_requires_source_text
test_validation_ready_requires_exact_content
test_no_quote_or_range_fabrication
test_partial_status_when_some_sources_ready
test_all_unavailable_status_requires_source_text
test_reports_include_canonical_section
test_campaign_generates_reports
test_physical_claims_remain_blocked
test_existing_v3_4_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing v3.4 exact extract review behavior
existing v3.3 source pack validation behavior
existing v3.2 source pack population behavior
existing v3.1 reviewed manifest behavior
existing v3.0 real source acquisition behavior
existing v2.9 real source ingestion behavior
existing historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
Priority exact fill validates PHI_GRADIENT.
Unresolved priority records count as source support.
Availability of a source URL counts as exact source text.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
Priority exact fill was attempted.
Some priority sources require source text.
Some exact fills may be validation-ready if exact content exists.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
priority source selection works
source availability classification works
unresolved records are created when text is unavailable
exact content is never fabricated
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
658 + new v3.5 tests
```

---

# 16. Final discipline

```txt
The smallest useful exact extract is worth more than a large decorative bibliography.
```
