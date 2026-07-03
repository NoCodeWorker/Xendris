# Codex Prompt — Phygn v3.0 PHI_GRADIENT Real Source Acquisition Campaign

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
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
```

Therefore v3.0 starts at:

```txt
178
```

---

# 1. Read first

Read these v3.0 specs:

```txt
docs/178_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_docs/status/GOAL.md
docs/179_PHYGN_REAL_SOURCE_QUERY_PLAN_AND_CANDIDATE_MANIFEST.md
docs/180_PHYGN_REAL_EXTRACT_INGESTION_AND_SLOT_COVERAGE_PROTOCOL.md
docs/181_PHYGN_REAL_SOURCE_CAMPAIGN_REPORT_AND_LOOP_FEEDBACK.md
```

Also read:

```txt
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
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
592 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v3.0:

```txt
Real Source Acquisition Campaign
Slot-Based Query Plan
Source Candidate Manifest
Real Extract Ingestion
Slot Coverage Matrix
Negative Source Handling
Benchmark Comparability
Alpha/Gamma_env/m/L/t Constraint Pressure
Canonical Reports
Closed Loop Feedback
Tests
```

Do not make physical claims.

---

# 4. Extend package

Extend or create:

```txt
phyng/real_source_acquisition/
  __init__.py
  schemas.py
  query_plan.py
  candidate_manifest.py
  extract_ingestion.py
  slot_coverage.py
  benchmark_comparability.py
  negative_sources.py
  campaign_gate.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/phi_gradient_real_source_acquisition.py
```

---

# 5. Schemas

Implement:

```txt
SlotQuery
RealSourceQueryPlan
RealSourceCandidate
RealSourceCandidateManifest
RealExtractIngestionResult
SlotCoverageRecord
SlotCoverageMatrix
NegativeSourceRecord
BenchmarkComparabilityResult
PhiGradientRealSourceAcquisitionResult
PhiGradientRealSourceAcquisitionCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 6. Query plan

Implement deterministic query plan for all slots:

```txt
SLOT_1_DECOHERENCE_BASELINE_MODELS
SLOT_2_GRAVITATIONAL_DECOHERENCE_MODELS
SLOT_3_LOG_OR_SCALE_SPACE_FORMULATIONS
SLOT_4_GRADIENT_TRANSITION_OPERATORS
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
SLOT_6_ALPHA_LIKE_PARAMETER_CONSTRAINTS
SLOT_7_NEGATIVE_OR_CONFLICTING_SOURCES
SLOT_8_OBSERVABLE_VISIBILITY_DECAY_SUPPORT
```

The code may not actually call the web unless an external acquisition backend exists.

If no backend exists, it must produce:

```txt
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

or:

```txt
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
```

without pretending real sources were acquired.

---

# 7. Acquisition backend boundary

Implement a backend interface:

```python
class SourceAcquisitionBackend(Protocol):
    def search(self, query: SlotQuery) -> list[RealSourceCandidate]:
        ...
```

Provide:

```txt
NoopSourceAcquisitionBackend
ManifestOnlySourceAcquisitionBackend
```

Noop backend result:

```txt
actual_real_sources_acquired = False
```

Do not use test doubles as real support.

---

# 8. Extract ingestion

If real sources are available locally or through a backend:

```txt
ingest them
extract candidate text
validate extracts using v2.9 rules
fill slot coverage matrix
```

If not:

```txt
report acquisition gap
preserve blocked source status
```

---

# 9. Slot coverage

Implement coverage matrix.

Coverage statuses:

```txt
SLOT_UNTOUCHED
SLOT_CANDIDATES_FOUND
SLOT_ANALOGY_ONLY
SLOT_PARTIALLY_COVERED
SLOT_COVERED_LIMITED
SLOT_CONTRADICTED
SLOT_BENCHMARK_COMPARABLE
```

---

# 10. Campaign final statuses

Add if needed:

```txt
PHI_GRADIENT_REAL_SOURCE_CANDIDATES_FOUND
PHI_GRADIENT_REAL_SOURCES_ACQUIRED
PHI_GRADIENT_REAL_EXTRACTS_VALIDATED
PHI_GRADIENT_REAL_SOURCE_ANALOGY_ONLY
PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
PHI_GRADIENT_REAL_SOURCE_CONTRADICTED
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
PHI_GRADIENT_REAL_ACQUISITION_FAILED
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

---

# 11. Reports

Generate:

```txt
reports/real_source_acquisition/phi_gradient_query_plan_v3_0.md
reports/real_source_acquisition/phi_gradient_source_candidate_manifest_v3_0.md
reports/real_source_acquisition/phi_gradient_extract_validation_v3_0.md
reports/real_source_acquisition/phi_gradient_slot_coverage_v3_0.md
reports/real_source_acquisition/phi_gradient_negative_sources_v3_0.md
reports/real_source_acquisition/phi_gradient_benchmark_comparability_v3_0.md
reports/real_source_acquisition/phi_gradient_real_source_gate_v3_0.md
reports/real_source_acquisition/phi_gradient_loop_feedback_v3_0.md
reports/campaigns/PHI-GRADIENT-REAL-SOURCE-ACQUISITION-v3_0.md
```

Reports must include:

```txt
canonical status section
actual_real_sources_acquired
backend status
slot coverage
missing requirements
blocked claims
next actions
discipline note
```

---

# 12. Tests

Create:

```txt
tests/test_real_source_query_plan_v3_0.py
tests/test_real_source_acquisition_backend_v3_0.py
tests/test_real_source_candidate_manifest_v3_0.py
tests/test_real_source_slot_coverage_v3_0.py
tests/test_real_source_acquisition_reports_v3_0.py
tests/test_phi_gradient_real_source_acquisition_campaign_v3_0.py
```

Minimum tests:

```txt
test_query_plan_covers_all_slots
test_noop_backend_does_not_create_real_sources
test_manifest_only_backend_marks_sources_as_candidates_not_support
test_no_backend_keeps_source_pressure_inconclusive
test_slot_coverage_records_missing_requirements
test_benchmark_support_not_granted_without_comparable_record
test_negative_sources_can_block_upgrade
test_reports_include_backend_status
test_reports_include_canonical_section
test_physical_claims_remain_blocked
test_campaign_generates_reports
test_existing_v2_9_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
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

# 14. Do not overclaim

Do not write:

```txt
PHI_GRADIENT has real literature support if backend is missing.
PHI_GRADIENT is physically validated.
Acquisition candidates are source support.
A query plan is evidence.
```

Allowed:

```txt
The campaign produced a query plan and/or source candidates.
Real source support remains missing until validated extracts exist.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
query plan works
backend boundary works
manifest works
slot coverage works
reports generated
loop feedback generated
physical claims blocked
no acquisition backend cannot fake real support
```

Expected test count:

```txt
592 + new v3.0 tests
```

---

# 16. Final discipline

```txt
A query plan is a map.
A source extract is pressure.
A benchmark comparison is pain.
Only pain teaches the candidate.
```
