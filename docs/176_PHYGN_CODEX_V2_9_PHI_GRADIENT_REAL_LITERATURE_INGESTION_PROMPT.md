# Codex Prompt — Phygn v2.9 Real Literature Acquisition & Source Extract Ingestion for PHI_GRADIENT

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
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
```

Therefore v2.9 starts at:

```txt
172
```

---

# 1. Read first

Read these v2.9 specs:

```txt
docs/172_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_docs/status/GOAL.md
docs/173_PHYGN_REAL_SOURCE_ACQUISITION_AND_MANIFEST_PROTOCOL.md
docs/174_PHYGN_REAL_SOURCE_EXTRACT_VALIDATION_PROTOCOL.md
docs/175_PHYGN_PHI_GRADIENT_REAL_SOURCE_GATE_AND_LOOP_FEEDBACK.md
```

Also read:

```txt
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect:

```txt
phyng/source_pressure/
phyng/source_grounding/
phyng/evidence/
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
579 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.9:

```txt
Real Literature Acquisition Manifest
Real Source Extract Ingestion
Extract Validation
Fixture-vs-Real Source Separation
PHI_GRADIENT Real Source Gate
Real Benchmark Record Handling
Negative Source Handling
Canonical Reports
Closed Loop Feedback
Tests
```

Do not treat v2.8 fixtures as real support.

---

# 4. Extend package

Extend or create:

```txt
phyng/real_source_ingestion/
  __init__.py
  schemas.py
  manifest.py
  extract_validation.py
  phi_gradient_real_source_gate.py
  benchmark_ingestion.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/phi_gradient_real_literature_ingestion.py
```

---

# 5. Schemas

Implement:

```txt
RealSourceManifestEntry
RealSourceManifest
RealSourceExtract
RealSourceExtractValidationResult
RealBenchmarkRecord
PhiGradientRealSourceGateResult
PhiGradientRealLiteratureCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 6. Real source manifest

Implement:

```python
build_real_source_manifest(...)
```

Statuses:

```txt
REAL_SOURCE_CANDIDATE_IDENTIFIED
REAL_SOURCE_AVAILABLE_LOCAL
REAL_SOURCE_AVAILABLE_URL
REAL_SOURCE_METADATA_ONLY
REAL_SOURCE_UNAVAILABLE
REAL_SOURCE_DUPLICATE
REAL_SOURCE_REJECTED_OUT_OF_SCOPE
```

Manifest must explicitly mark fixtures:

```txt
FIXTURE_ONLY_DOES_NOT_COUNT_AS_REAL_SUPPORT
```

---

# 7. Extract validation

Implement:

```python
validate_real_source_extract(extract: RealSourceExtract) -> RealSourceExtractValidationResult
```

Validation statuses:

```txt
EXTRACT_VALID_SUPPORTS_OBSERVABLE
EXTRACT_VALID_SUPPORTS_BASELINE
EXTRACT_VALID_SUPPORTS_COMPONENT
EXTRACT_VALID_CONSTRAINS_PARAMETER
EXTRACT_VALID_PROVIDES_BENCHMARK_DATA
EXTRACT_VALID_CONTRADICTS_CANDIDATE
EXTRACT_REJECTED_ANALOGY_ONLY
EXTRACT_REJECTED_NO_COMPONENT_SUPPORT
EXTRACT_REJECTED_NO_OBSERVABLE
EXTRACT_REJECTED_NOT_COMPARABLE
EXTRACT_REQUIRES_MANUAL_REVIEW
```

---

# 8. PHI_GRADIENT real source gate

Implement:

```python
run_phi_gradient_real_source_gate(
    manifest: RealSourceManifest,
    extracts: list[RealSourceExtract],
    benchmarks: list[RealBenchmarkRecord],
) -> PhiGradientRealSourceGateResult
```

Rules:

```txt
fixtures do not count
source-backed limited requires observable/baseline + component support
benchmark data found requires comparable benchmark record
analogy-only blocks upgrade
negative contradiction blocks upgrade
missing alpha constraint remains warning or block depending severity
```

---

# 9. Canonical statuses

Add if needed:

```txt
PHI_GRADIENT_REAL_SOURCES_ACQUIRED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_REAL_SOURCE_ACQUISITION_FAILED
PHI_GRADIENT_REAL_SOURCE_INGESTION_BLOCKED
```

Mapping:

```txt
REAL_SOURCE_BACKED_LIMITED:
  CLAIM_LIMITED_ALLOWED
  SOURCE_BACKED_LIMITED
  SOURCE_LIMITED
  blocked: MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA

REAL_BENCHMARK_DATA_FOUND:
  CLAIM_LIMITED_ALLOWED
  BENCHMARK_SUPPORTED
  BENCHMARK
  blocked: MISSING_EXPERIMENTAL_DATA

REAL_SOURCE_ANALOGY_ONLY:
  CLAIM_BLOCKED or REVIEW_REQUIRED
  SYNTHETIC_ONLY
  blocked: MISSING_SOURCE_SUPPORT

REAL_SOURCE_CONTRADICTED:
  CLAIM_BLOCKED
  blocked: CONTRADICTION
```

---

# 10. Deterministic test data

Because real web acquisition may not be available in every environment, include deterministic local fixtures clearly marked as real-source test doubles.

Important:

```txt
TEST_DOUBLE_REAL_SOURCE_FORMAT
```

does not mean real scientific support.

It only tests the ingestion path.

Create test doubles:

```txt
real_source_observable_extract_double
real_source_component_extract_double
real_source_benchmark_extract_double
real_source_analogy_only_double
real_source_negative_double
fixture_source_from_v2_8_double
```

Campaign report must state whether actual real sources were ingested or only test doubles were used.

---

# 11. Reports

Generate:

```txt
reports/real_source_ingestion/phi_gradient_real_source_manifest_v2_9.md
reports/real_source_ingestion/phi_gradient_real_extract_validation_v2_9.md
reports/real_source_ingestion/phi_gradient_real_source_gate_v2_9.md
reports/real_source_ingestion/phi_gradient_real_benchmark_records_v2_9.md
reports/real_source_ingestion/phi_gradient_real_source_loop_feedback_v2_9.md
reports/campaigns/PHI-GRADIENT-REAL-LITERATURE-INGESTION-v2_9.md
```

Reports must include:

```txt
canonical status section
fixture separation
real/test-double distinction
validated extracts
rejected analogies
negative sources
benchmark comparability
blocked claims
next actions
discipline note
```

---

# 12. Tests

Create:

```txt
tests/test_real_source_manifest_v2_9.py
tests/test_real_source_extract_validation_v2_9.py
tests/test_phi_gradient_real_source_gate_v2_9.py
tests/test_phi_gradient_real_benchmark_records_v2_9.py
tests/test_phi_gradient_real_source_reports_v2_9.py
tests/test_phi_gradient_real_literature_campaign_v2_9.py
```

Minimum tests:

```txt
test_real_source_manifest_marks_fixtures_as_non_real_support
test_fixture_support_cannot_promote_real_source_status
test_valid_extract_requires_supported_component
test_analogy_extract_is_rejected
test_negative_extract_blocks_upgrade
test_real_source_backed_limited_requires_observable_and_component
test_real_benchmark_data_found_requires_comparable_record
test_missing_benchmark_keeps_benchmark_blocked
test_missing_experimental_data_blocks_physical_validation
test_reports_include_fixture_separation
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v2_8_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
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

# 14. Do not overclaim

Do not write:

```txt
PHI_GRADIENT is physically validated.
Real source ingestion proves Frontera C.
Test doubles count as real literature.
A source-backed limited claim is experimental proof.
```

Allowed:

```txt
Real source extracts were ingested and classified.
The candidate is source-backed limited, benchmark-supported, contradicted, analogy-only, or inconclusive according to the gate.
Physical claims remain blocked without experimental evidence.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
manifest works
extract validation works
fixture-vs-real separation works
real source gate works
benchmark records work
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
579 + new v2.9 tests
```

---

# 16. Final discipline

```txt
Real sources may raise pressure.
Only experiments can raise physical truth.
```
