# Phygn v3.0 - PHI_GRADIENT Real Source Acquisition Results

Date: 2026-06-30

Source prompt:

```txt
docs/182_PHYGN_CODEX_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_PROMPT.md
```

Supporting specs:

```txt
docs/178_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_docs/status/GOAL.md
docs/179_PHYGN_REAL_SOURCE_QUERY_PLAN_AND_CANDIDATE_MANIFEST.md
docs/180_PHYGN_REAL_EXTRACT_INGESTION_AND_SLOT_COVERAGE_PROTOCOL.md
docs/181_PHYGN_REAL_SOURCE_CAMPAIGN_REPORT_AND_LOOP_FEEDBACK.md
docs/177_PHYGN_V2_9_PHI_GRADIENT_REAL_LITERATURE_INGESTION_RESULTS.md
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v3.0 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

The v3.0 real source acquisition campaign was implemented as a conservative acquisition-boundary pass.

No web acquisition was performed.

No source candidates were treated as real support.

No physical validation claim was unlocked.

Final campaign status:

```txt
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

Final validation:

```txt
pytest -q
604 passed in 43.56s
```

Baseline before v3.0:

```txt
592 passed
```

Net result:

```txt
592 baseline tests + 12 v3.0 tests = 604 passing tests
```

---

## 2. Implemented Package

Created:

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

Primary responsibilities:

| Module | Responsibility |
|---|---|
| `schemas.py` | v3.0 acquisition, manifest, coverage, benchmark and campaign schemas |
| `query_plan.py` | Deterministic slot-based source query plan |
| `candidate_manifest.py` | Acquisition backend boundary and candidate manifest generation |
| `extract_ingestion.py` | Bridge from acquired candidates to v2.9 extract validation |
| `slot_coverage.py` | Slot coverage matrix over the eight PHI_GRADIENT source-pressure slots |
| `negative_sources.py` | Negative/contradictory source record extraction |
| `benchmark_comparability.py` | Benchmark-comparable real record assessment |
| `campaign_gate.py` | Conservative final gate for v3.0 acquisition status |
| `report.py` | Canonical Markdown reports for acquisition outputs |

Created campaign:

```txt
phyng/campaigns/phi_gradient_real_source_acquisition.py
```

Entrypoint:

```python
run_phi_gradient_real_source_acquisition_campaign(root: str | Path = ".")
```

---

## 3. Schemas Implemented

Implemented in:

```txt
phyng/real_source_acquisition/schemas.py
```

Schemas:

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

Backend boundary:

```python
class SourceAcquisitionBackend(Protocol):
    backend_name: str

    def search(self, query: SlotQuery) -> list[RealSourceCandidate]:
        ...
```

Provided backends:

```txt
NoopSourceAcquisitionBackend
ManifestOnlySourceAcquisitionBackend
```

---

## 4. Query Plan Results

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_query_plan_v3_0.md
```

The query plan covers all eight required slots:

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

Benchmark pressure is explicitly routed through:

```txt
SLOT_5_MESOSCOPIC_INTERFEROMETRY_BENCHMARKS
```

The query plan is a map only.

It is not evidence.

---

## 5. Acquisition Backend Results

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_source_candidate_manifest_v3_0.md
```

Default backend:

```txt
NOOP_SOURCE_ACQUISITION_BACKEND
```

Result:

```txt
actual_real_sources_acquired=False
candidates=[]
```

Interpretation:

```txt
No acquisition backend was available, so no real source support can be claimed.
```

The `ManifestOnlySourceAcquisitionBackend` exists for local candidate manifests, but it preserves the hard boundary:

```txt
metadata candidates are not source support
source candidates require validated extracts before they can raise pressure
```

---

## 6. Extract Ingestion Results

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_extract_validation_v3_0.md
```

Default campaign result:

```txt
actual_real_extracts_validated=False
```

Reason:

```txt
No real source candidates were acquired by the default backend.
```

The ingestion bridge reuses the v2.9 extract validator:

```txt
phyng.real_source_ingestion.extract_validation.validate_real_source_extract
```

Preserved rule:

```txt
fixtures and test doubles do not count as real support
```

---

## 7. Slot Coverage Results

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_slot_coverage_v3_0.md
```

Default coverage:

| Metric | Result |
|---|---:|
| Slots evaluated | 8 |
| Covered slots | 0 |
| Missing slots | 8 |
| Benchmark-comparable slots | 0 |
| Contradicted slots | 0 |

Coverage statuses implemented:

```txt
SLOT_UNTOUCHED
SLOT_CANDIDATES_FOUND
SLOT_ANALOGY_ONLY
SLOT_PARTIALLY_COVERED
SLOT_COVERED_LIMITED
SLOT_CONTRADICTED
SLOT_BENCHMARK_COMPARABLE
```

Default result:

```txt
All slots remain SLOT_UNTOUCHED because no acquisition backend returned sources.
```

---

## 8. Negative Source Handling

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_negative_sources_v3_0.md
```

Default campaign:

```txt
negative_sources=[]
```

Contract test behavior:

```txt
A real non-fixture negative extract with EXTRACT_VALID_CONTRADICTS_CANDIDATE blocks upgrade and returns PHI_GRADIENT_REAL_SOURCE_CONTRADICTED.
```

This preserves the rule that negative source pressure must prevent silent candidate promotion.

---

## 9. Benchmark Comparability Results

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_benchmark_comparability_v3_0.md
```

Default status:

```txt
BENCHMARK_COMPARABLE_RECORD_MISSING
```

Missing benchmark requirements:

```txt
observable
mass range
length/separation range
time range
visibility/decoherence measure
```

Therefore v3.0 does not grant:

```txt
PHI_GRADIENT_REAL_BENCHMARK_DATA_FOUND
```

---

## 10. Campaign Gate Results

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_real_source_gate_v3_0.md
```

Campaign status:

```txt
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
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
A deterministic acquisition query plan was produced.
```

Blocked claims:

```txt
PHI_GRADIENT is physically validated.
PHI_GRADIENT validates Frontera C.
A query plan is evidence.
Acquisition candidates count as source support.
PHI_GRADIENT has benchmark-comparable real support.
```

---

## 11. Closed Loop Feedback

Generated report:

```txt
reports/real_source_acquisition/phi_gradient_loop_feedback_v3_0.md
```

Loop input:

```txt
input_type=REAL_SOURCE_ACQUISITION_RESULT
previous_status=PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
result_status=PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

Update proposal:

```txt
REAL_SOURCE_ACQUISITION_FEEDBACK
```

Forbidden actions preserved:

```txt
authorize physical claim
validate Frontera C
count query plan as evidence
count candidates as source support
```

---

## 12. Generated Reports

The v3.0 campaign generated:

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

This document consolidates the result into:

```txt
docs/183_PHYGN_V3_0_PHI_GRADIENT_REAL_SOURCE_ACQUISITION_RESULTS.md
```

---

## 13. New Tests

Created:

```txt
tests/test_real_source_query_plan_v3_0.py
tests/test_real_source_acquisition_backend_v3_0.py
tests/test_real_source_candidate_manifest_v3_0.py
tests/test_real_source_slot_coverage_v3_0.py
tests/test_real_source_acquisition_reports_v3_0.py
tests/test_phi_gradient_real_source_acquisition_campaign_v3_0.py
```

Focused v3.0 verification:

```txt
pytest -q tests/test_real_source_query_plan_v3_0.py tests/test_real_source_acquisition_backend_v3_0.py tests/test_real_source_candidate_manifest_v3_0.py tests/test_real_source_slot_coverage_v3_0.py tests/test_real_source_acquisition_reports_v3_0.py tests/test_phi_gradient_real_source_acquisition_campaign_v3_0.py
12 passed in 1.06s
```

Full-suite verification:

```txt
pytest -q
604 passed in 43.56s
```

Operational note:

```txt
C:\Users\usuario\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q
```

failed during collection due to a local NumPy DLL import error in unrelated legacy tests:

```txt
DLL load failed while importing _multiarray_umath
```

The repository's working `pytest -q` runner passed and was used as the final validation gate.

---

## 14. Behavior Preservation

v3.0 explicitly preserved:

```txt
v2.9 real source ingestion behavior
v2.8 source pressure behavior
v2.7 phi search outputs
v2.6 ablation outputs
v2.5 synthetic execution outputs
v2.4 closed loop behavior
v2.3 benchmark design outputs
v2.2 heuristic discovery behavior
v2.1 canonical mapping behavior
```

Specific preservation test:

```txt
test_existing_v2_9_behavior_preserved
```

Result:

```txt
PHI_GRADIENT_REAL_SOURCE_PRESSURE_INCONCLUSIVE
actual_real_sources_ingested=False
```

---

## 15. Final Assessment

v3.0 converted the real-source acquisition step into an explicit, testable boundary:

```txt
query plan -> acquisition backend -> candidate manifest -> extract validation -> slot coverage -> benchmark comparability -> closed loop feedback
```

The campaign did not acquire real sources because the default backend is intentionally `Noop`.

Therefore the correct final status is:

```txt
PHI_GRADIENT_REAL_ACQUISITION_BACKEND_MISSING
```

The next meaningful move is not to relax the gate.

The next meaningful move is:

```txt
Attach a reviewed real-source acquisition backend or local reviewed manifest,
then ingest real extracts through the existing v2.9 validation rules.
```

Final discipline note:

```txt
A query plan is a map.
A source extract is pressure.
A benchmark comparison is pain.
Only pain teaches the candidate.
```
