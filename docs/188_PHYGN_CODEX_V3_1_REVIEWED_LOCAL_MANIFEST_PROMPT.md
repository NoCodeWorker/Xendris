# Codex Prompt — Phygn v3.1 Reviewed Local Manifest & Real Source Extract Pack

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
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
```

Therefore v3.1 starts at:

```txt
184
```

---

# 1. Read first

Read these v3.1 specs:

```txt
docs/184_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_docs/status/GOAL.md
docs/185_PHYGN_REVIEWED_LOCAL_MANIFEST_SCHEMA_AND_VALIDATION.md
docs/186_PHYGN_REAL_SOURCE_EXTRACT_PACK_AND_SLOT_COVERAGE.md
docs/187_PHYGN_REVIEWED_MANIFEST_REPORTING_AND_LOOP_FEEDBACK.md
```

Also read:

```txt
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
```

Inspect:

```txt
phyng/real_source_acquisition/
phyng/real_source_ingestion/
phyng/source_pressure/
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
604 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.1:

```txt
Reviewed Local Manifest
Manifest Schema and Validation
Real Source Extract Pack
Extract Pack Validation
Fixture/Test-Double Exclusion
Slot Coverage Matrix
Negative Source Handling
Benchmark Comparability
Canonical Reports
Closed Loop Feedback
Tests
```

Do not make physical claims.

---

# 4. Extend package

Extend or create:

```txt
phyng/reviewed_manifest/
  __init__.py
  schemas.py
  manifest_loader.py
  manifest_validation.py
  extract_pack.py
  extract_validation_bridge.py
  slot_coverage.py
  benchmark_comparability.py
  campaign_gate.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/phi_gradient_reviewed_local_manifest.py
```

---

# 5. Input files

Expected reviewed manifest:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_1.yaml
```

or:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_1.json
```

Expected extract pack:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_1.yaml
```

or:

```txt
data/real_sources/extracts/phi_gradient_extract_pack_v3_1.json
```

If no files exist, create empty template files and return:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
```

or:

```txt
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

Do not invent real sources.

---

# 6. Schemas

Implement:

```txt
ReviewedSourceManifestEntry
ReviewedSourceManifest
ReviewedSourceManifestValidationResult
ReviewedSourceExtract
ReviewedSourceExtractPack
ReviewedSourceExtractValidationResult
ReviewedSlotCoverageRecord
ReviewedSlotCoverageMatrix
ReviewedBenchmarkComparabilityResult
PhiGradientReviewedManifestCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 7. Manifest validation

Rules:

```txt
entry must have DOI/arXiv/URL/local_path
entry must target at least one valid slot
fixture/test-double entries cannot count as support
manifest cannot be empty if claiming source pressure
manifest can be valid but still not evidential without extracts
```

Statuses:

```txt
REVIEWED_MANIFEST_VALID
REVIEWED_MANIFEST_EMPTY
REVIEWED_MANIFEST_INVALID_SCHEMA
REVIEWED_MANIFEST_CONTAINS_ONLY_FIXTURES
REVIEWED_MANIFEST_CONTAINS_UNTRACEABLE_ENTRIES
REVIEWED_MANIFEST_REQUIRES_MANUAL_REVIEW
```

---

# 8. Extract pack validation

Rules:

```txt
extract source_id must exist in manifest
extract must target valid slot
extract must support or contradict concrete component
analogy-only extract rejected
benchmark extract requires comparable observable/ranges/data
negative extract blocks upgrade unless addressed
```

Reuse:

```txt
phyng.real_source_ingestion.extract_validation.validate_real_source_extract
```

or preserve equivalent strictness.

---

# 9. Campaign gate

Final status rules:

```txt
No manifest or empty manifest:
  PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
  or PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE

Manifest valid but no extracts:
  PHI_GRADIENT_REVIEWED_MANIFEST_LOADED
  with REVIEW_REQUIRED

Extracts valid but incomplete:
  PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE

Observable/baseline + component extract:
  PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED

Comparable benchmark extract:
  PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND

Unaddressed contradiction:
  PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
```

---

# 10. Reports

Generate:

```txt
reports/reviewed_manifest/phi_gradient_reviewed_manifest_v3_1.md
reports/reviewed_manifest/phi_gradient_manifest_validation_v3_1.md
reports/reviewed_manifest/phi_gradient_extract_pack_v3_1.md
reports/reviewed_manifest/phi_gradient_extract_validation_v3_1.md
reports/reviewed_manifest/phi_gradient_slot_coverage_v3_1.md
reports/reviewed_manifest/phi_gradient_negative_sources_v3_1.md
reports/reviewed_manifest/phi_gradient_benchmark_comparability_v3_1.md
reports/reviewed_manifest/phi_gradient_real_source_gate_v3_1.md
reports/reviewed_manifest/phi_gradient_loop_feedback_v3_1.md
reports/campaigns/PHI-GRADIENT-REVIEWED-LOCAL-MANIFEST-v3_1.md
```

Reports must include:

```txt
canonical status section
manifest count
traceable identifier coverage
extract validation results
slot coverage
negative source handling
benchmark comparability
fixture/test-double exclusion
blocked claims
next actions
discipline note
```

---

# 11. Tests

Create:

```txt
tests/test_reviewed_manifest_schema_v3_1.py
tests/test_reviewed_manifest_validation_v3_1.py
tests/test_reviewed_extract_pack_v3_1.py
tests/test_reviewed_slot_coverage_v3_1.py
tests/test_reviewed_manifest_reports_v3_1.py
tests/test_phi_gradient_reviewed_local_manifest_campaign_v3_1.py
```

Minimum tests:

```txt
test_empty_manifest_creates_template_without_claiming_support
test_manifest_entry_requires_traceable_identifier
test_manifest_entry_requires_valid_slot
test_fixture_entry_cannot_count_as_real_support
test_extract_source_must_exist_in_manifest
test_analogy_extract_is_rejected
test_observable_and_component_extracts_allow_source_backed_limited
test_benchmark_extract_requires_comparability
test_negative_extract_blocks_upgrade
test_missing_extract_keeps_source_pressure_inconclusive
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v3_0_behavior_preserved
```

---

# 12. Behavior preservation

Do not alter:

```txt
existing v3.0 real source acquisition behavior
existing v2.9 real source ingestion behavior
existing v2.8 source pressure behavior
existing v2.7 phi search outputs
existing v2.6 ablation results
existing v2.5 synthetic execution outputs
existing v2.4 closed loop outputs
existing v2.3 benchmark design outputs
existing v2.2 heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing business/candidate/copilot gates
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
A reviewed manifest proves PHI_GRADIENT.
A source candidate is evidence.
A benchmark candidate is benchmark support.
PHI_GRADIENT is physically validated.
```

Allowed:

```txt
A reviewed manifest was loaded or created.
Validated extracts provide limited source or benchmark pressure if strict requirements are met.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
manifest schema works
manifest validation works
extract pack validation works
slot coverage works
reports generated
loop feedback generated
physical claims blocked
no manifest entry can fake evidence without extract
```

Expected test count:

```txt
604 + new v3.1 tests
```

---

# 15. Final discipline

```txt
A reviewed manifest can open the evidence gate.
Only validated extracts can walk through it.
```
