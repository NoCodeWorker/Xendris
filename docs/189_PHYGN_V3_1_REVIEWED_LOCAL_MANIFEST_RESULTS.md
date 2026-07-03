# Phygn v3.1 - Reviewed Local Manifest & Real Source Extract Pack Results

Date: 2026-06-30

Source prompt:

```txt
docs/188_PHYGN_CODEX_V3_1_REVIEWED_LOCAL_MANIFEST_PROMPT.md
```

Supporting specs:

```txt
docs/184_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_docs/status/GOAL.md
docs/185_PHYGN_REVIEWED_LOCAL_MANIFEST_SCHEMA_AND_VALIDATION.md
docs/186_PHYGN_REAL_SOURCE_EXTRACT_PACK_AND_SLOT_COVERAGE.md
docs/187_PHYGN_REVIEWED_MANIFEST_REPORTING_AND_LOOP_FEEDBACK.md
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v3.1 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v3.1 implemented a reviewed local manifest and extract-pack boundary.

No autonomous web acquisition was performed.

No real sources were invented.

No manifest entry was treated as evidence without a validated extract.

No physical validation claim was unlocked.

Final campaign status:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
```

Final validation:

```txt
pytest -q
620 passed in 44.31s
```

Baseline before v3.1:

```txt
604 passed
```

Net result:

```txt
604 baseline tests + 16 v3.1 tests = 620 passing tests
```

---

## 2. Implemented Package

Created:

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

Created campaign:

```txt
phyng/campaigns/phi_gradient_reviewed_local_manifest.py
```

Entrypoint:

```python
run_phi_gradient_reviewed_local_manifest_campaign(root: str | Path = ".")
```

---

## 3. Input Templates

The repository did not contain reviewed local source files before v3.1 execution.

The campaign created empty JSON templates:

```txt
data/real_sources/phi_gradient_reviewed_manifest_v3_1.json
data/real_sources/extracts/phi_gradient_extract_pack_v3_1.json
```

Template result:

```txt
manifest_created=True
extract_pack_created=True
manifest_count=0
validated_extract_count=0
```

Interpretation:

```txt
The evidence gate is prepared, but no real source support exists yet.
```

---

## 4. Schemas Implemented

Implemented in:

```txt
phyng/reviewed_manifest/schemas.py
```

Schemas:

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
PhiGradientReviewedManifestGateResult
PhiGradientReviewedManifestCampaignResult
```

---

## 5. Manifest Validation

Implemented in:

```txt
phyng/reviewed_manifest/manifest_validation.py
```

Rules enforced:

```txt
entry must have DOI/arXiv/URL/local_path
entry must target at least one valid PHI_GRADIENT source slot
fixture/test-double entries cannot count as support
empty manifest cannot claim source pressure
manifest can be valid but still non-evidential without extracts
```

Manifest validation statuses supported:

```txt
REVIEWED_MANIFEST_VALID
REVIEWED_MANIFEST_EMPTY
REVIEWED_MANIFEST_CONTAINS_ONLY_FIXTURES
REVIEWED_MANIFEST_CONTAINS_UNTRACEABLE_ENTRIES
REVIEWED_MANIFEST_REQUIRES_MANUAL_REVIEW
```

Default result:

```txt
REVIEWED_MANIFEST_EMPTY
```

---

## 6. Extract Pack Validation

Implemented in:

```txt
phyng/reviewed_manifest/extract_validation_bridge.py
```

v3.1 reuses the v2.9 validator:

```txt
phyng.real_source_ingestion.extract_validation.validate_real_source_extract
```

Additional v3.1 checks:

```txt
extract source_id must exist in manifest
extract slot_id must be a valid PHI_GRADIENT slot
fixtures and test doubles remain non-evidential
manual-review extracts cannot silently count as support
analogy-only extracts are rejected
negative extracts block upgrade
benchmark extracts require comparability fields
```

Default result:

```txt
extract_count=0
validated_extract_count=0
```

---

## 7. Slot Coverage and Benchmark Comparability

Implemented in:

```txt
phyng/reviewed_manifest/slot_coverage.py
phyng/reviewed_manifest/benchmark_comparability.py
```

v3.1 reuses the v3.0 slot coverage model.

Default coverage:

| Metric | Result |
|---|---:|
| Slots evaluated | 8 |
| Covered slots | 0 |
| Missing slots | 8 |
| Negative sources | 0 |
| Benchmark comparable records | 0 |

Benchmark status:

```txt
BENCHMARK_COMPARABLE_RECORD_MISSING
```

---

## 8. Campaign Gate Results

Implemented in:

```txt
phyng/reviewed_manifest/campaign_gate.py
```

Default final status:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
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
Reviewed manifest and extract-pack templates were created.
```

Blocked claims:

```txt
A reviewed manifest proves PHI_GRADIENT.
A source candidate is evidence.
A benchmark candidate is benchmark support.
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
PHI_GRADIENT has benchmark-comparable real support.
```

---

## 9. Reports Generated

The v3.1 campaign generated:

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

This document consolidates the result into:

```txt
docs/189_PHYGN_V3_1_REVIEWED_LOCAL_MANIFEST_RESULTS.md
```

---

## 10. New Tests

Created:

```txt
tests/test_reviewed_manifest_schema_v3_1.py
tests/test_reviewed_manifest_validation_v3_1.py
tests/test_reviewed_extract_pack_v3_1.py
tests/test_reviewed_slot_coverage_v3_1.py
tests/test_reviewed_manifest_reports_v3_1.py
tests/test_phi_gradient_reviewed_local_manifest_campaign_v3_1.py
```

Focused v3.1 verification:

```txt
pytest -q tests/test_reviewed_manifest_schema_v3_1.py tests/test_reviewed_manifest_validation_v3_1.py tests/test_reviewed_extract_pack_v3_1.py tests/test_reviewed_slot_coverage_v3_1.py tests/test_reviewed_manifest_reports_v3_1.py tests/test_phi_gradient_reviewed_local_manifest_campaign_v3_1.py
16 passed in 0.74s
```

Full-suite verification:

```txt
pytest -q
620 passed in 44.31s
```

---

## 11. Behavior Preservation

v3.1 explicitly preserved v3.0 behavior:

```txt
test_existing_v3_0_behavior_preserved
```

Result:

```txt
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
actual_real_sources_acquired=False
```

Historical behavior preservation also remains covered by the existing suite for:

```txt
v2.9 real source ingestion
v2.8 source pressure
v2.7 phi search outputs
v2.6 ablation outputs
v2.5 synthetic execution
v2.4 closed loop
v2.3 benchmark design
v2.2 heuristic discovery
v2.1 canonical mapping
```

---

## 12. Final Assessment

v3.1 created the bridge between acquisition planning and real evidence pressure:

```txt
reviewed manifest -> extract pack -> v2.9 extract validation -> v3.0 slot coverage -> benchmark comparability -> closed loop feedback
```

The current repository has only empty reviewed-manifest templates.

Therefore the correct status is:

```txt
PHI_GRADIENT_REVIEWED_MANIFEST_CREATED
```

The next meaningful move is:

```txt
Populate the reviewed manifest with traceable real sources, then add extract-pack entries with equations, observables, parameter constraints, benchmark ranges, limitations and negative-source coverage.
```

Final discipline note:

```txt
A reviewed manifest can open the evidence gate.
Only validated extracts can walk through it.
```
