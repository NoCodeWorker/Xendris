# Codex Prompt — Phygn v2.6 LOG_BOUNDARY Sensitivity & Ablation Analysis

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
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
```

Therefore v2.6 starts at:

```txt
154
```

---

# 1. Read first

Read these v2.6 specs:

```txt
docs/154_PHYGN_V2_6_LOG_BOUNDARY_SENSITIVITY_ABLATION_docs/status/GOAL.md
docs/155_PHYGN_LOG_BOUNDARY_ABLATION_CONTROL_PROTOCOL.md
docs/156_PHYGN_LOG_BOUNDARY_SENSITIVITY_METRICS_AND_DECISION_RULES.md
docs/157_PHYGN_LOG_BOUNDARY_ABLATION_LOOP_FEEDBACK_PROTOCOL.md
```

Also read:

```txt
docs/153_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_RESULTS.md
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect:

```txt
phyng/synthetic_benchmark_design/
phyng/closed_loop/
phyng/core/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
538 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.6:

```txt
LOG_BOUNDARY Sensitivity Analysis
Ablation Controls
Constant Phi Control
Coordinate Removal Controls
Alpha Sensitivity
Threshold Sensitivity
Phi Saturation Detection
Control Gain Metrics
Coordinate Contribution Metrics
Ablation Classification
Closed Loop Feedback
Reports
Campaign Runner
Tests
```

Do not authorize physical claims.

---

# 4. Extend package

Extend:

```txt
phyng/synthetic_benchmark_design/
```

Add:

```txt
ablation.py
sensitivity.py
ablation_report.py
```

Create campaign:

```txt
phyng/campaigns/log_boundary_sensitivity_ablation.py
```

---

# 5. Schemas

Implement or extend:

```txt
LogBoundaryAblationControl
LogBoundaryAblationResult
LogBoundarySensitivityMetrics
LogBoundaryAblationClassification
LogBoundaryAblationLoopFeedbackResult
LogBoundarySensitivityAblationCampaignResult
```

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 6. Ablation controls

Implement controls:

```txt
CONTROL_CONSTANT_PHI_ONE
CONTROL_CONSTANT_PHI_MEAN
CONTROL_RANDOM_U0_W0
CONTROL_REMOVE_U
CONTROL_REMOVE_W
CONTROL_ALPHA_ONE
CONTROL_LOW_STEEPNESS
CONTROL_NO_LOG_COORDINATES
```

Minimum functions:

```python
run_constant_phi_one_control(...)
run_constant_phi_mean_control(...)
run_remove_u_control(...)
run_remove_w_control(...)
run_alpha_sensitivity(...)
run_threshold_sensitivity(...)
run_no_log_coordinates_control(...)
run_log_boundary_ablation_suite(...)
```

---

# 7. Metrics

Compute:

```txt
candidate_delta
constant_phi_delta
mean_phi_delta
remove_u_delta
remove_w_delta
no_log_coordinates_delta
alpha_1_delta
saturation_ratio
control_gain
coordinate_contribution_score
threshold_sensitivity_score
warnings
```

---

# 8. Classification

Implement:

```python
classify_log_boundary_ablation(metrics) -> LogBoundaryAblationClassification
```

Possible statuses:

```txt
LOG_BOUNDARY_SURVIVES_ABLATION
LOG_BOUNDARY_FAILS_CONSTANT_CONTROL
LOG_BOUNDARY_FAILS_COORDINATE_CONTRIBUTION
LOG_BOUNDARY_SIGNAL_IS_SATURATION_ARTIFACT
LOG_BOUNDARY_SIGNAL_REQUIRES_ALPHA_EXTREME
LOG_BOUNDARY_SIGNAL_REQUIRES_THRESHOLD_TUNING
LOG_BOUNDARY_SENSITIVITY_INCONCLUSIVE
LOG_BOUNDARY_ABLATION_BLOCKED
```

Decision priority:

```txt
execution blocked
post-hoc or invalid parameters
saturation artifact
constant control failure
coordinate contribution failure
alpha extreme dependence
threshold tuning dependence
survives ablation
inconclusive
```

---

# 9. Canonical mapping

Add v2.6 statuses to compatibility map if needed.

Survival:

```txt
CanonicalPermission: CLAIM_LIMITED_ALLOWED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: MISSING_SOURCE_SUPPORT, MISSING_BENCHMARK, MISSING_EXPERIMENTAL_DATA
```

Failure/artifact:

```txt
CanonicalPermission: CLAIM_BLOCKED or REVIEW_REQUIRED
Evidence: SYNTHETIC_ONLY
Support: SYNTHETIC
Blocked: HUMAN_REVIEW_REQUIRED, UNPHYSICAL_PARAMETER, MISSING_EXPERIMENTAL_DATA
```

No physical claim is authorized.

---

# 10. Loop feedback

Implement:

```python
generate_log_boundary_ablation_loop_feedback(...)
```

Allowed:

```txt
increase source-search priority only if survives ablation
block source-pressure upgrade if saturation artifact
down-rank current phi formulation
search alternative non-saturating phi functions
compare next candidate family
require alpha justification
require threshold robustness
```

Forbidden:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
source requirement reduction
benchmark requirement reduction
canonical permission semantic changes
```

---

# 11. Reports

Generate:

```txt
reports/synthetic_benchmark_execution/log_boundary_ablation_controls_v2_6.md
reports/synthetic_benchmark_execution/log_boundary_sensitivity_metrics_v2_6.md
reports/synthetic_benchmark_execution/log_boundary_ablation_classification_v2_6.md
reports/synthetic_benchmark_execution/log_boundary_ablation_loop_feedback_v2_6.md
reports/campaigns/LOG-BOUNDARY-SENSITIVITY-ABLATION-v2_6.md
```

Reports must include:

```txt
canonical status section
controls summary
metrics
warnings
allowed claims
blocked claims
loop feedback
discipline note
```

---

# 12. Tests

Create:

```txt
tests/test_log_boundary_ablation_controls_v2_6.py
tests/test_log_boundary_sensitivity_metrics_v2_6.py
tests/test_log_boundary_ablation_classification_v2_6.py
tests/test_log_boundary_ablation_loop_feedback_v2_6.py
tests/test_log_boundary_ablation_reports_v2_6.py
tests/test_log_boundary_sensitivity_ablation_campaign_v2_6.py
```

Minimum tests:

```txt
test_constant_phi_one_control_exists
test_alpha_one_sensitivity_runs
test_remove_u_control_runs
test_remove_w_control_runs
test_no_log_coordinates_control_runs
test_phi_saturation_warning_detected
test_control_gain_computed
test_coordinate_contribution_score_computed
test_saturation_artifact_blocks_source_pressure_upgrade
test_survives_ablation_keeps_physical_claim_blocked
test_loop_feedback_blocks_physical_claim
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v2_5_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
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
LOG_BOUNDARY survives ablation, therefore it is physically true.
LOG_BOUNDARY ablation validates Frontera C.
Synthetic ablation proves a real-world effect.
```

Allowed:

```txt
LOG_BOUNDARY survived or failed synthetic ablation under declared toy controls.
Source/benchmark pressure may or may not be justified.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
ablation controls work
metrics computed
classification works
reports generated
loop feedback generated
physical claims blocked
```

Expected test count:

```txt
538 + new v2.6 tests
```

---

# 16. Final discipline

```txt
If a synthetic signal vanishes under ablation,
it was not a candidate.
It was a decoration.
```
