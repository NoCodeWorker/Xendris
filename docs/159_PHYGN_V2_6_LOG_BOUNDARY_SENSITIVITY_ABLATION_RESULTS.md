# Phygn v2.6 - LOG_BOUNDARY Sensitivity & Ablation Results

Date: 2026-06-30

Source prompt:

```txt
docs/158_PHYGN_CODEX_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_PROMPT.md
```

Supporting specs:

```txt
docs/154_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_docs/status/GOAL.md
docs/155_PHYGN_LOG_BOUNDARY_ABLATION_CONTROL_PROTOCOL.md
docs/156_PHYGN_LOG_BOUNDARY_SENSITIVITY_METRICS_AND_DECISION_RULES.md
docs/157_PHYGN_LOG_BOUNDARY_ABLATION_LOOP_FEEDBACK_PROTOCOL.md
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.6 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.6 executed LOG_BOUNDARY synthetic sensitivity and ablation controls against the v2.5 detected synthetic signal.

Final classification:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

Meaning:

```txt
The v2.5 synthetic signal is explained by phi_log saturation and the constant phi=1 control.
The current LOG_BOUNDARY phi formulation does not earn increased source-pressure priority.
Physical claims remain blocked.
```

Final validation:

```txt
pytest -q
553 passed in 26.43s
```

Baseline before v2.6 implementation:

```txt
pytest -q
538 passed in 23.46s
```

Net result:

```txt
538 baseline tests + 15 v2.6 tests = 553 passing tests
```

---

## 2. New Ablation Layer

Extended:

```txt
phyng/synthetic_benchmark_design/
  ablation.py
  sensitivity.py
  ablation_report.py
```

Created campaign:

```txt
phyng/campaigns/log_boundary_sensitivity_ablation.py
```

Primary responsibilities:

| Module | Responsibility |
|---|---|
| `ablation.py` | Constant phi, coordinate removal, threshold, alpha, steepness and no-log controls |
| `sensitivity.py` | Sensitivity metrics, classification and loop feedback |
| `ablation_report.py` | v2.6 canonical report generation |
| `log_boundary_sensitivity_ablation.py` | Campaign runner and report orchestration |

Campaign entrypoint:

```python
run_log_boundary_sensitivity_ablation_campaign(root: str | Path = ".")
```

---

## 3. Schemas Added

Extended:

```txt
phyng/synthetic_benchmark_design/schemas.py
```

New schemas:

```txt
LogBoundaryAblationControl
LogBoundaryAblationResult
LogBoundarySensitivityMetrics
LogBoundaryAblationClassification
LogBoundaryAblationLoopFeedbackResult
LogBoundarySensitivityAblationCampaignResult
```

---

## 4. Ablation Controls

Generated report:

```txt
reports/synthetic_benchmark_execution/log_boundary_ablation_controls_v2_6.md
```

Control summary:

| Control | Delta | Phi | Status |
|---|---:|---:|---|
| `CONTROL_CONSTANT_PHI_ONE` | `0.7152665915101674` | `1.0` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_CONSTANT_PHI_MEAN` | `0.6260264663798746` | `0.6191750426941809` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_RANDOM_U0_W0` | `0.6218931390361411` | `0.6065333887511951` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_REMOVE_U` | `0.5823512050329686` | `0.5` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_REMOVE_W` | `0.5823512050329686` | `0.5` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_ALPHA_ONE` | `0.2386512185411911` | `1.0` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_LOW_STEEPNESS` | `0.7152662055684518` | `0.9999977465561599` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |
| `CONTROL_NO_LOG_COORDINATES` | `0.5823512050329686` | `0.5` | `LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA` |

Interpretation:

```txt
The synthetic signal remains detectable under simple controls.
The candidate does not beat the constant phi=1 control.
Low-steepness still saturates.
The current phi formulation is not doing enough distinct log-boundary work.
```

---

## 5. Sensitivity Metrics

Generated report:

```txt
reports/synthetic_benchmark_execution/log_boundary_sensitivity_metrics_v2_6.md
```

Metrics:

| Metric | Value |
|---|---:|
| candidate_delta | `0.7152665915101674` |
| constant_phi_delta | `0.7152665915101674` |
| mean_phi_delta | `0.6260264663798746` |
| remove_u_delta | `0.5823512050329686` |
| remove_w_delta | `0.5823512050329686` |
| no_log_coordinates_delta | `0.5823512050329686` |
| alpha_1_delta | `0.2386512185411911` |
| saturation_ratio | `1.0` |
| control_gain | `0.0` |
| coordinate_contribution_score | `0.1329153864771988` |
| threshold_sensitivity_score | `0.1305435673667963` |

Warnings:

```txt
WARN_PHI_SATURATION
WARN_CONSTANT_CONTROL_MATCH
```

Decision-relevant fact:

```txt
candidate_delta == constant_phi_delta
control_gain == 0.0
saturation_ratio == 1.0
```

---

## 6. Classification

Generated report:

```txt
reports/synthetic_benchmark_execution/log_boundary_ablation_classification_v2_6.md
```

Classification:

```txt
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
```

Reason:

```txt
Candidate delta matches the constant phi=1 control while phi_log is saturated.
```

Canonical status:

| Field | Value |
|---|---|
| Domain Status | `LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT` |
| Canonical Permission | `CLAIM_BLOCKED` |
| Evidence Level | `SYNTHETIC_ONLY` |
| Support Level | `SYNTHETIC` |
| Blocked Reasons | `UNPHYSICAL_PARAMETER`, `MISSING_EXPERIMENTAL_DATA` |
| Allowed Uses | synthetic artifact report, alternative phi search |
| Blocked Uses | source-pressure upgrade, physical prediction, Frontera C validation |

Allowed claims:

```txt
Synthetic ablation result reporting.
```

Blocked claims:

```txt
LOG_BOUNDARY predicts physical decoherence.
LOG_BOUNDARY validates Frontera C.
Synthetic ablation proves a real-world effect.
```

---

## 7. Loop Feedback

Generated report:

```txt
reports/synthetic_benchmark_execution/log_boundary_ablation_loop_feedback_v2_6.md
```

Loop feedback summary:

| Field | Result |
|---|---|
| loop_event_id | `LOG-BOUNDARY-ABLATION-v2_6-AUDIT-001` |
| ablation_status | `LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT` |

Allowed updates:

```txt
block source-pressure upgrade
```

Blocked updates:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
canonical permission semantic change
```

Next actions:

```txt
down-rank current phi formulation
create simpler control report
search alternative non-saturating phi functions
```

---

## 8. Generated Reports

v2.6 generated:

```txt
reports/synthetic_benchmark_execution/log_boundary_ablation_controls_v2_6.md
reports/synthetic_benchmark_execution/log_boundary_sensitivity_metrics_v2_6.md
reports/synthetic_benchmark_execution/log_boundary_ablation_classification_v2_6.md
reports/synthetic_benchmark_execution/log_boundary_ablation_loop_feedback_v2_6.md
reports/campaigns/LOG-BOUNDARY-SENSITIVITY-ABLATION-v2_6.md
```

This document consolidates all v2.6 results into:

```txt
docs/159_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_RESULTS.md
```

---

## 9. New Tests

Created:

```txt
tests/test_log_boundary_ablation_controls_v2_6.py
tests/test_log_boundary_sensitivity_metrics_v2_6.py
tests/test_log_boundary_ablation_classification_v2_6.py
tests/test_log_boundary_ablation_loop_feedback_v2_6.py
tests/test_log_boundary_ablation_reports_v2_6.py
tests/test_log_boundary_sensitivity_ablation_campaign_v2_6.py
```

Focused v2.6 verification:

```txt
pytest -q tests/test_log_boundary_ablation_controls_v2_6.py tests/test_log_boundary_sensitivity_metrics_v2_6.py tests/test_log_boundary_ablation_classification_v2_6.py tests/test_log_boundary_ablation_loop_feedback_v2_6.py tests/test_log_boundary_ablation_reports_v2_6.py tests/test_log_boundary_sensitivity_ablation_campaign_v2_6.py
15 passed in 3.31s
```

Full-suite verification:

```txt
pytest -q
553 passed in 26.43s
```

---

## 10. Behavior Preservation

v2.6 preserved v2.5 execution behavior:

```txt
LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
sweep_count = 1728
best_max_abs_delta = 0.7152665915101674
```

Behavior preservation test:

```txt
test_existing_v2_5_behavior_preserved
```

Result:

```txt
passed
```

---

## 11. Operational Notes

`git status --short` could not be used in this environment.

Observed output:

```txt
fatal: not a git repository (or any of the parent directories): .git
```

The `python` command resolved to a WindowsApps stub and failed.

The reliable direct campaign runtime was:

```txt
C:\Users\usuario\AppData\Local\Programs\Python\Python311\python.exe
```

The final validation source remains:

```txt
pytest -q
```

---

## 12. Final Assessment

v2.6 turns the v2.5 large synthetic number into a diagnostic failure for the current phi formulation.

The result is not:

```txt
LOG_BOUNDARY is physically false.
```

The result is:

```txt
The current LOG_BOUNDARY toy signal is saturated and matched by the simplest constant control.
It should not receive source-pressure upgrade in its current formulation.
```

Safest next move:

```txt
Down-rank the current saturated phi formulation and search for alternative non-saturating phi functions before any renewed source/benchmark pressure.
```
