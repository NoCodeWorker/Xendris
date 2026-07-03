# Codex Prompt — Phygn v2.5 LOG_BOUNDARY Synthetic Benchmark Execution

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
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
```

Therefore v2.5 starts at:

```txt
148
```

---

# 1. Read first

Read these v2.5 specs:

```txt
docs/148_PHYGN_V2_5_LOG_BOUNDARY_SYNTHETIC_EXECUTION_docs/status/GOAL.md
docs/149_PHYGN_LOG_BOUNDARY_NUMERICAL_SWEEP_PROTOCOL.md
docs/150_PHYGN_LOG_BOUNDARY_SYNTHETIC_DETECTABILITY_REPORT.md
docs/151_PHYGN_LOG_BOUNDARY_LOOP_FEEDBACK_PROTOCOL.md
```

Also read:

```txt
docs/147_PHYGN_V2_4_CLOSED_LOOP_META_IMPROVEMENT_RESULTS.md
docs/141_PHYGN_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_RESULTS.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect:

```txt
phyng/synthetic_benchmark_design/
phyng/closed_loop/
phyng/heuristic_discovery/
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
523 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.5:

```txt
LOG_BOUNDARY Synthetic Benchmark Execution
Numerical Sweep
Visibility Curve Computation
max_abs_delta Computation
Detectability Classification
Parameter Reasonableness Classification
Failure Condition Recording
Canonical Report Sections
Closed Loop Feedback into v2.4
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

Add if needed:

```txt
execution.py
numerics.py
sweep.py
loop_feedback.py
```

Create campaign:

```txt
phyng/campaigns/log_boundary_synthetic_execution.py
```

---

# 5. Schemas

Implement:

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

Use:

```txt
CanonicalStatusRecord
CanonicalReportContract
CandidateLoopInput
CandidateLoopResult
```

where appropriate.

---

# 6. Numerical implementation

Implement:

```python
compute_boundary_coordinates(m_kg: float, L_m: float) -> BoundaryCoordinates
```

Using:

```txt
lambda_C = hbar / (m*c)
r_g = G*m/c^2
Q = lambda_C / L
B = r_g / L
q = log(Q)
b = log(B)
u = (q+b)/2
w = (b-q)/2
```

Implement overflow-safe:

```python
sigmoid(x)
```

Implement:

```python
compute_phi_log(u, w, k, k2, u0, w0) -> float
```

Implement:

```python
compute_visibility_curves(...)
compute_max_abs_delta(...)
```

---

# 7. Sweep

Implement:

```python
run_log_boundary_sweep(spec: LogBoundaryCandidateSpec) -> LogBoundarySweepResult
```

Use declared v2.3 grid:

```txt
alpha_values: [0.1, 1.0, 3.0, 10.0]
k_values: [0.5, 1.0, 2.0, 5.0]
k2_values: [0.5, 1.0, 2.0, 5.0]
u0_values: [-90.0, -70.0, -50.0]
w0_values: [-40.0, -20.0, 0.0]
Gamma_env_values: [0.01, 0.05, 0.1]
m_kg = 1e-17
L_m = 1e-7
t_grid = 101 points over [0, 10]
epsilon_exp = 1e-6
```

Total default sweep count should be:

```txt
4 * 4 * 4 * 3 * 3 * 3 = 1728
```

---

# 8. Classify result

Implement:

```python
classify_log_boundary_detectability(sweep_result) -> LogBoundaryExecutionResult
```

Statuses:

```txt
LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
LOG_BOUNDARY_EXECUTION_BLOCKED
```

Rules:

```txt
max_abs_delta > epsilon_exp -> detectable synthetic delta
all values inside declared v2.3 grid -> declared toy range
post-hoc values -> post-hoc tuning failure
extreme values -> extreme parameter failure
no finite result -> execution blocked
```

---

# 9. Canonical mapping

Add v2.5 statuses to compatibility map if needed:

```txt
LOG_BOUNDARY_DETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_UNDETECTABLE_SYNTHETIC_DELTA
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
LOG_BOUNDARY_DETECTABLE_ONLY_WITH_POST_HOC_TUNING
LOG_BOUNDARY_EXECUTION_BLOCKED
```

Mappings:

```txt
detectable synthetic:
  CLAIM_LIMITED_ALLOWED
  evidence: SYNTHETIC_ONLY
  support: SYNTHETIC
  blocked: MISSING_SOURCE_SUPPORT, MISSING_EXPERIMENTAL_DATA

undetectable:
  CLAIM_BLOCKED
  evidence: SYNTHETIC_ONLY
  support: SYNTHETIC
  blocked: UNDETECTABLE_DELTA, MISSING_EXPERIMENTAL_DATA

extreme/post-hoc:
  CLAIM_BLOCKED or REVIEW_REQUIRED
  blocked: UNPHYSICAL_PARAMETER or HUMAN_REVIEW_REQUIRED

execution blocked:
  REVIEW_REQUIRED or CLAIM_BLOCKED
```

Ensure report language still blocks physical claims.

---

# 10. Loop feedback

Implement:

```python
generate_log_boundary_loop_feedback(execution_result) -> LogBoundaryLoopFeedbackResult
```

It must create or prepare:

```txt
CandidateLoopInput
CandidateLoopResult
update proposals
next actions
blocked claims
```

Allowed feedback:

```txt
source search pressure
benchmark data search
candidate priority update
select next family
```

Forbidden feedback:

```txt
physical claim authorization
Frontera C validation
experimental confirmation
```

---

# 11. Reports

Generate:

```txt
reports/synthetic_benchmark_execution/log_boundary_numerical_sweep_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_detectability_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_failure_conditions_v2_5.md
reports/synthetic_benchmark_execution/log_boundary_loop_feedback_v2_5.md
reports/campaigns/LOG-BOUNDARY-SYNTHETIC-EXECUTION-v2_5.md
```

Reports must include canonical status sections and blocked physical claims.

---

# 12. Tests

Create:

```txt
tests/test_log_boundary_numerics_v2_5.py
tests/test_log_boundary_sweep_v2_5.py
tests/test_log_boundary_detectability_classification_v2_5.py
tests/test_log_boundary_loop_feedback_v2_5.py
tests/test_log_boundary_synthetic_execution_reports_v2_5.py
tests/test_log_boundary_synthetic_execution_campaign_v2_5.py
```

Minimum tests:

```txt
test_boundary_coordinates_are_finite
test_phi_log_is_bounded
test_visibility_curves_have_matching_lengths
test_max_abs_delta_non_negative
test_default_sweep_has_expected_count
test_sweep_finds_best_point
test_detectability_classification_uses_epsilon
test_undetectable_maps_to_claim_blocked
test_detectable_synthetic_does_not_authorize_physical_claim
test_extreme_parameters_block_claim
test_loop_feedback_blocks_physical_claim
test_loop_feedback_generates_next_actions
test_reports_include_canonical_section
test_campaign_generates_reports
test_existing_v2_4_behavior_preserved
```

---

# 13. Behavior preservation

Do not alter:

```txt
existing v2.4 closed loop outputs
existing v2.3 benchmark design outputs
existing v2.2 heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing v1.5 candidate benchmark outputs
existing business/candidate/copilot gates
historical reports
```

---

# 14. Do not overclaim

Do not write:

```txt
LOG_BOUNDARY predicts decoherence.
LOG_BOUNDARY validates Frontera C.
Synthetic detectability proves a physical effect.
```

Allowed:

```txt
LOG_BOUNDARY produced/did not produce a detectable synthetic delta under declared toy parameters.
LOG_BOUNDARY may proceed to source/benchmark pressure if detectable.
Physical claims remain blocked.
```

---

# 15. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
numerics work
sweep works
detectability classification works
failure conditions recorded
canonical reports generated
closed-loop feedback generated
physical claims remain blocked
```

Expected test count:

```txt
523 + new v2.5 tests
```

---

# 16. Final discipline

```txt
If LOG_BOUNDARY shows signal, it earns pressure.
If it does not, it earns humility.
Neither outcome earns truth.
```
