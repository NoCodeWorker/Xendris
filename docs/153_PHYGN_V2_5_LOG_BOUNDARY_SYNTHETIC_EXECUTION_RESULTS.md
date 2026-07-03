# Phygn v2.5 - LOG_BOUNDARY Synthetic Execution Results

Date: 2026-06-30

Source prompt:

```txt
docs/152_PHYGN_CODEX_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_PROMPT.md
```

Supporting specs:

```txt
docs/148_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_docs/status/GOAL.md
docs/149_PHYGN_LOG_BOUNDARY_NUMERICAL_SWEEP_PROTOCOL.md
docs/150_PHYGN_LOG_BOUNDARY_SYNTHETIC_DETECTABILITY_REPORT.md
docs/151_PHYGN_LOG_BOUNDARY_LOOP_FEEDBACK_PROTOCOL.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.5 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.5 executed the previously designed LOG_BOUNDARY synthetic benchmark under the declared toy sweep.

No physical claim was authorized.

No source support, benchmark data, or experimental evidence was invented.

Final validation:

```txt
pytest -q
538 passed in 22.48s
```

Baseline before v2.5 implementation:

```txt
pytest -q
523 passed in 20.17s
```

Net result:

```txt
523 baseline tests + 15 v2.5 tests = 538 passing tests
```

---

## 2. New Execution Layer

Extended:

```txt
phyng/synthetic_benchmark_design/
  numerics.py
  sweep.py
  execution.py
  loop_feedback.py
```

Created campaign:

```txt
phyng/campaigns/log_boundary_synthetic_execution.py
```

Primary responsibilities:

| Module | Responsibility |
|---|---|
| `numerics.py` | LOG_BOUNDARY coordinates, overflow-safe sigmoid, phi_log, visibility curves and max_abs_delta |
| `sweep.py` | Declared v2.3 parameter grid execution and best-point selection |
| `execution.py` | Detectability classification, failure conditions and v2.5 report generation |
| `loop_feedback.py` | v2.5 synthetic result feedback into the v2.4 candidate loop |
| `log_boundary_synthetic_execution.py` | Campaign entrypoint and report orchestration |

Campaign entrypoint:

```python
run_log_boundary_synthetic_execution_campaign(root: str | Path = ".")
```

---

## 3. Schemas Added

Extended:

```txt
phyng/synthetic_benchmark_design/schemas.py
```

New schemas:

```txt
BoundaryCoordinates
VisibilityCurveResult
LogBoundarySweepPoint
LogBoundarySweepResult
LogBoundaryExecutionResult
ParameterReasonablenessResult
LogBoundaryLoopFeedbackResult
LogBoundarySyntheticExecutionCampaignResult
```

---

## 4. Numerical Execution Results

Generated report:

```txt
reports/synthetic_benchmark_execution/log_boundary_numerical_sweep_v2_5.md
```

Sweep summary:

| Metric | Result |
|---|---:|
| Candidate ID | `HEUR-PHY-003` |
| Candidate family | `LOG_BOUNDARY` |
| Parameter grid size | `1728` |
| epsilon_exp | `1e-06` |
| Best max_abs_delta | `0.7152665915101674` |
| Detectability status | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |

Best parameter record:

| Parameter | Value |
|---|---:|
| alpha | `10.0` |
| k | `2.0` |
| k2 | `1.0` |
| u0 | `-90.0` |
| w0 | `0.0` |
| Gamma_env | `0.05` |
| m_kg | `1e-17` |
| L_m | `1e-07` |
| q | `-42.49131709260482` |
| b | `-85.49322459609193` |
| u | `-63.992270844348376` |
| w | `-21.50095375174356` |
| phi_log | `1.0` |
| DeltaGamma_log | `0.5` |

Interpretation:

```txt
LOG_BOUNDARY produced a detectable synthetic delta under declared toy parameters.
This updates search/benchmark priority only.
It does not authorize physical decoherence, Frontera C validation, or experimental claims.
```

---

## 5. Canonical Status Mapping

Extended:

```txt
phyng/core/status_mapping.py
```

New v2.5 statuses:

```txt
LOG_BOUNDARY_SYNTHETIC_EXECUTED
LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
LOG_BOUNDARY_EXECUTION_BLOCKED
```

Canonical mapping for the observed status:

| Field | Value |
|---|---|
| Domain Status | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| Canonical Permission | `CLAIM_LIMITED_ALLOWED` |
| Evidence Level | `SYNTHETIC_ONLY` |
| Support Level | `SYNTHETIC` |
| Blocked Reasons | `MISSING_SOURCE_SUPPORT`, `MISSING_EXPERIMENTAL_DATA` |
| Allowed Uses | synthetic detectability claim, source-search prioritization, benchmark-pressure prioritization |
| Blocked Uses | physical decoherence prediction, Frontera C validation, experimental confirmation |

---

## 6. Detectability and Failure Conditions

Generated reports:

```txt
reports/synthetic_benchmark_execution/log_boundary_detectability_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_failure_conditions_v2_5.md
```

Allowed synthetic claims:

```txt
LOG_BOUNDARY produced a detectable synthetic delta under declared toy parameters.
LOG_BOUNDARY may proceed to source/benchmark pressure.
Candidate priority may be updated.
```

Always blocked claims:

```txt
LOG_BOUNDARY predicts physical decoherence.
LOG_BOUNDARY validates Frontera C.
Synthetic delta proves a physical effect.
Toy parameter sweep establishes real-world detectability.
```

Failure conditions retained:

```txt
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
FAIL_NO_EXPERIMENTAL_DATA
```

---

## 7. Closed-Loop Feedback

Generated report:

```txt
reports/synthetic_benchmark_execution/log_boundary_loop_feedback_v2_5.md
```

Loop feedback summary:

| Field | Result |
|---|---|
| loop_event_id | `LOG-BOUNDARY-v2_5-AUDIT-001` |
| result_status | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| proposal | `SOURCE_AND_BENCHMARK_PRESSURE_UPDATE` |
| shadow_mode_required | `False` |
| human_review_required | `False` |

Proposed updates:

```txt
increase source-search priority
increase benchmark-pressure priority
schedule source support audit
schedule benchmark data search
keep physical claims blocked
```

Blocked updates:

```txt
claim gate relaxation
source requirement reduction
benchmark requirement reduction
experimental evidence requirement reduction
canonical permission semantic changes
```

---

## 8. Generated Reports

v2.5 generated:

```txt
reports/synthetic_benchmark_execution/log_boundary_numerical_sweep_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_detectability_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_failure_conditions_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_loop_feedback_v2_5.md
reports/campaigns/LOG-BOUNDARY-SYNTHETIC-EXECUTION-v2_5.md
```

This document consolidates all v2.5 results into:

```txt
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
```

---

## 9. New Tests

Created:

```txt
tests/test_log_boundary_numerics_v2_5.py
tests/test_log_boundary_sweep_v2_5.py
tests/test_log_boundary_detectability_classification_v2_5.py
tests/test_log_boundary_loop_feedback_v2_5.py
tests/test_log_boundary_synthetic_execution_reports_v2_5.py
tests/test_log_boundary_synthetic_execution_campaign_v2_5.py
```

Focused v2.5 verification:

```txt
pytest -q tests/test_log_boundary_numerics_v2_5.py tests/test_log_boundary_sweep_v2_5.py tests/test_log_boundary_detectability_classification_v2_5.py tests/test_log_boundary_loop_feedback_v2_5.py tests/test_log_boundary_synthetic_execution_reports_v2_5.py tests/test_log_boundary_synthetic_execution_campaign_v2_5.py
15 passed in 2.57s
```

Full-suite verification:

```txt
pytest -q
538 passed in 22.48s
```

Post-execution technical debt cleanup:

```txt
typed loop feedback schemas
removed arbitrary schema object fields
kept failure_conditions as canonical failure codes
removed loose finite-value helper typing
updated synthetic benchmark schema docstring after v2.5 expansion
```

---

## 10. Operational Notes

`git status --short` could not be used in this environment.

Observed output:

```txt
fatal: not a git repository (or any of the parent directories): .git
```

The explicit Python executable:

```txt
C:\Users\usuario\AppData\Local\Programs\Python\Python311\python.exe -m pytest -q
```

failed during collection because the local repository contains a `numpy/` package that shadows/imports incompatible NumPy compiled extensions when invoked that way.

The project runner:

```txt
pytest -q
```

completed successfully and is the final validation source for v2.5.

---

## 11. Final Assessment

v2.5 converted LOG_BOUNDARY from a designed synthetic benchmark into an executed synthetic benchmark.

The result is numerically detectable inside the declared toy sweep, but epistemically bounded:

```txt
detectable synthetic delta != physical validation
synthetic priority update != claim permission upgrade
benchmark behavior != evidence of nature
```

Safest next move:

```txt
Run source-support and benchmark-data pressure for LOG_BOUNDARY while preserving the physical-claim block.
```
