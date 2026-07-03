# Phygn v2.8 - PHI_GRADIENT Source-Support & Benchmark-Data Pressure Results

Date: 2026-06-30

Source prompt:

```txt
docs/170_PHYGN_CODEX_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_PROMPT.md
```

Supporting specs:

```txt
docs/166_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_docs/status/GOAL.md
docs/167_PHYGN_PHI_GRADIENT_SOURCE_SLOT_REGISTRY.md
docs/168_PHYGN_SOURCE_SUPPORT_VS_ANALOGY_GATE.md
docs/169_PHYGN_PHI_GRADIENT_BENCHMARK_DATA_PRESSURE_PROTOCOL.md
docs/165_PHYGN_V2_7_LOG_BOUNDARY_NON_SATURATING_PHI_RESULTS.md
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.8 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.8 applied deterministic source-support and benchmark-data pressure to:

```txt
candidate_family: LOG_BOUNDARY
phi_family: PHI_GRADIENT
previous_status: PHI_CANDIDATE_SURVIVES_CONTROLS
```

Final campaign status:

```txt
PHI_GRADIENT_BENCHMARK_DATA_FOUND
```

Important limitation:

```txt
The v2.8 campaign used deterministic fixtures.
Real literature acquisition is still required.
Fixture-backed benchmark pressure is not physical validation.
```

Final validation:

```txt
pytest -q
579 passed in 42.23s
```

Baseline before v2.8 implementation:

```txt
pytest -q
566 passed in 38.52s
```

Net result:

```txt
566 baseline tests + 13 v2.8 tests = 579 passing tests
```

---

## 2. New Source Pressure Package

Created:

```txt
phyng/source_pressure/
  __init__.py
  schemas.py
  slots.py
  source_gate.py
  benchmark_pressure.py
  phi_gradient_audit.py
  report.py
```

Created campaign:

```txt
phyng/campaigns/phi_gradient_source_benchmark_pressure.py
```

Primary responsibilities:

| Module | Responsibility |
|---|---|
| `slots.py` | PHI_GRADIENT evidence slot registry |
| `source_gate.py` | Source-support versus decorative analogy gate |
| `benchmark_pressure.py` | Benchmark comparability and candidate-support assessment |
| `phi_gradient_audit.py` | PHI_GRADIENT source pressure audit and deterministic fixtures |
| `report.py` | Canonical source-pressure report generation |
| `phi_gradient_source_benchmark_pressure.py` | v2.8 campaign runner |

---

## 3. Schemas Added

Implemented:

```txt
SourceEvidenceSlot
SourceCandidate
SourceSupportAssessment
BenchmarkPressureRecord
PhiGradientSourcePressureResult
PhiGradientBenchmarkPressureResult
PhiGradientSourceBenchmarkCampaignResult
```

---

## 4. Source Slots

Generated report:

```txt
reports/source_pressure/phi_gradient_source_slots_v2_8.md
```

Slots implemented:

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

Slot rule:

```txt
A slot is not filled by a theme.
It is filled by a constraint.
```

---

## 5. Source Support Gate

Generated report:

```txt
reports/source_pressure/phi_gradient_source_support_gate_v2_8.md
```

Source gate status:

```txt
PHI_GRADIENT_SOURCE_BACKED_LIMITED
```

Fixture assessments:

| Source | Assessment | Counts as support |
|---|---|---|
| `SRC-FIX-ANALOGY-001` | `SOURCE_ANALOGY_ONLY` | `False` |
| `SRC-FIX-OBS-001` | `SOURCE_SUPPORTS_BASELINE` | `True` |
| `SRC-FIX-GRAD-001` | `SOURCE_SUPPORTS_COMPONENT` | `True` |
| `SRC-FIX-ALPHA-001` | `SOURCE_CONSTRAINS_PARAMETER` | `True` |

Canonical source status:

| Field | Value |
|---|---|
| Domain Status | `PHI_GRADIENT_SOURCE_BACKED_LIMITED` |
| Canonical Permission | `CLAIM_LIMITED_ALLOWED` |
| Evidence Level | `SOURCE_BACKED_LIMITED` |
| Support Level | `SOURCE_LIMITED` |
| Blocked Reasons | `MISSING_BENCHMARK`, `MISSING_EXPERIMENTAL_DATA` |
| Blocked Uses | benchmark-supported claim, experimental validation, physical prediction |

Interpretation:

```txt
The fixture source gate distinguishes analogy from support.
Analogy-only source does not count.
Observable/baseline, gradient component and alpha constraint fixtures count as limited source pressure.
```

---

## 6. Benchmark Pressure

Generated report:

```txt
reports/source_pressure/phi_gradient_benchmark_pressure_v2_8.md
```

Benchmark assessments:

| Benchmark | Assessment | Counts as benchmark support |
|---|---|---|
| `BM-FIX-BASELINE-001` | `BENCHMARK_BASELINE_ONLY` | `False` |
| `BM-FIX-CANDIDATE-001` | `BENCHMARK_SUPPORTS_CANDIDATE_LIMITED` | `True` |
| `BM-FIX-NOT-COMPARABLE-001` | `BENCHMARK_REJECTED_NOT_COMPARABLE` | `False` |

Final campaign status:

```txt
PHI_GRADIENT_BENCHMARK_DATA_FOUND
```

Canonical benchmark status:

| Field | Value |
|---|---|
| Domain Status | `PHI_GRADIENT_BENCHMARK_DATA_FOUND` |
| Canonical Permission | `CLAIM_LIMITED_ALLOWED` |
| Evidence Level | `BENCHMARK_SUPPORTED` |
| Support Level | `BENCHMARK` |
| Blocked Reasons | `MISSING_EXPERIMENTAL_DATA` |
| Blocked Uses | experimental validation, physical prediction, Frontera C validation |

---

## 7. Negative Source Handling

Generated report:

```txt
reports/source_pressure/phi_gradient_negative_sources_v2_8.md
```

Default campaign result:

```txt
No unaddressed negative fixture source in campaign seed set.
```

Test coverage includes a negative fixture:

```txt
test_negative_source_blocks_unaddressed_upgrade
```

Result:

```txt
PHI_GRADIENT_CONTRADICTED_BY_SOURCE blocks upgrade when a negative source is present.
```

---

## 8. Loop Feedback

Generated report:

```txt
reports/source_pressure/phi_gradient_source_benchmark_loop_feedback_v2_8.md
```

Loop feedback:

| Field | Result |
|---|---|
| loop_event_id | `PHI-GRADIENT-SOURCE-BENCHMARK-v2_8-AUDIT-001` |
| result_status | `PHI_GRADIENT_BENCHMARK_DATA_FOUND` |

Update proposal:

```txt
PHI_GRADIENT received fixture-based source and benchmark pressure; physical claims remain blocked.
```

Blocked claims:

```txt
PHI_GRADIENT is physically validated.
PHI_GRADIENT proves Frontera C.
A source analogy validates the candidate.
Benchmark pressure confirms the real effect.
```

Next actions:

```txt
replace fixtures with real literature extracts
search benchmark data
keep physical claims blocked
```

---

## 9. Generated Reports

v2.8 generated:

```txt
reports/source_pressure/phi_gradient_source_slots_v2_8.md
reports/source_pressure/phi_gradient_source_support_gate_v2_8.md
reports/source_pressure/phi_gradient_benchmark_pressure_v2_8.md
reports/source_pressure/phi_gradient_negative_sources_v2_8.md
reports/source_pressure/phi_gradient_source_benchmark_loop_feedback_v2_8.md
reports/campaigns/PHI-GRADIENT-SOURCE-BENCHMARK-PRESSURE-v2_8.md
```

This document consolidates all v2.8 results into:

```txt
docs/171_PHYGN_V2_8_PHI_GRADIENT_SOURCE_BENCHMARK_PRESSURE_RESULTS.md
```

---

## 10. New Tests

Created:

```txt
tests/test_phi_gradient_source_slots_v2_8.py
tests/test_source_support_vs_analogy_gate_v2_8.py
tests/test_phi_gradient_source_pressure_audit_v2_8.py
tests/test_phi_gradient_benchmark_pressure_v2_8.py
tests/test_phi_gradient_source_pressure_reports_v2_8.py
tests/test_phi_gradient_source_benchmark_campaign_v2_8.py
```

Focused v2.8 verification:

```txt
pytest -q tests/test_phi_gradient_source_slots_v2_8.py tests/test_source_support_vs_analogy_gate_v2_8.py tests/test_phi_gradient_source_pressure_audit_v2_8.py tests/test_phi_gradient_benchmark_pressure_v2_8.py tests/test_phi_gradient_source_pressure_reports_v2_8.py tests/test_phi_gradient_source_benchmark_campaign_v2_8.py
13 passed in 3.67s
```

Full-suite verification:

```txt
pytest -q
579 passed in 42.23s
```

---

## 11. Behavior Preservation

v2.8 preserved v2.7 behavior:

```txt
PHI_CANDIDATE_SURVIVES_CONTROLS
best_candidate_family = PHI_GRADIENT
```

Behavior preservation test:

```txt
test_existing_v2_7_behavior_preserved
```

Result:

```txt
passed
```

---

## 12. Operational Notes

`git status --short` could not be used in this environment.

Observed output:

```txt
fatal: not a git repository (or any of the parent directories): .git
```

The reliable direct runtime remains:

```txt
C:\Users\usuario\AppData\Local\Programs\Python\Python311\python.exe
```

The final validation source remains:

```txt
pytest -q
```

---

## 13. Final Assessment

v2.8 moved PHI_GRADIENT from pure synthetic control survival into fixture-based source/benchmark pressure.

The result allows:

```txt
limited source-backed component claim
limited benchmark-supported component claim
continued source/benchmark acquisition pressure
```

The result does not allow:

```txt
physical validation
Frontera C validation
experimental confirmation
analogy-based upgrade
source or benchmark requirement reduction
```

Safest next move:

```txt
Replace fixtures with real literature extracts and comparable benchmark records before making any non-fixture source-backed claim.
```
