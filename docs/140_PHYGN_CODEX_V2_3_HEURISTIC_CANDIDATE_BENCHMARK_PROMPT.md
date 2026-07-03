# Codex Prompt — Phygn v2.3 Heuristic Candidate to Synthetic Benchmark Design

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
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
```

Therefore v2.3 starts at:

```txt
136
```

---

# 1. Read first

Read these v2.3 specs:

```txt
docs/136_PHYGN_V2_3_HEURISTIC_CANDIDATE_SYNTHETIC_BENCHMARK_docs/status/GOAL.md
docs/137_PHYGN_LOG_BOUNDARY_CANDIDATE_FORMALIZATION.md
docs/138_PHYGN_LOG_BOUNDARY_DETECTABILITY_AND_FAILURE_PROTOCOL.md
docs/139_PHYGN_HEURISTIC_TO_BENCHMARK_REPORT_CONTRACT.md
```

Also read:

```txt
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

Inspect:

```txt
phyng/heuristic_discovery/
phyng/core/
phyng/candidates/
phyng/model_comparison/
```

---

# 2. First action

Run:

```bash
pytest -q
```

Expected baseline:

```txt
497 passed, 0 failed
```

If tests fail, fix baseline first.

---

# 3. Mission

Implement v2.3:

```txt
LOG_BOUNDARY candidate formalization
synthetic benchmark design schemas
dimensionless equation admissibility checks
no-ad-hoc scale checks
detectability/failure protocol
canonical report contract integration
campaign runner
tests
```

Do not claim physical validation.

---

# 4. New package or module

Create:

```txt
phyng/synthetic_benchmark_design/
  __init__.py
  schemas.py
  log_boundary.py
  admissibility.py
  detectability_protocol.py
  report.py
```

Create campaign:

```txt
phyng/campaigns/heuristic_candidate_synthetic_benchmark.py
```

---

# 5. Schemas

Implement:

```txt
LogBoundaryCandidateSpec
SyntheticBenchmarkDesign
EquationAdmissibilityResult
DetectabilityProtocolSpec
SyntheticBenchmarkDesignResult
HeuristicToBenchmarkCampaignResult
```

Use v2.1:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

# 6. LOG_BOUNDARY formalization

Implement:

```python
create_log_boundary_candidate_spec(...) -> LogBoundaryCandidateSpec
```

Default candidate:

```txt
candidate_id: HEUR-PHY-003
candidate_family: LOG_BOUNDARY
observable: visibility_decay
baseline_equation: V_base(t)=exp(-Gamma_env*t)
candidate_equation: V_log(t)=exp(-(Gamma_env + DeltaGamma_log)*t)
DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)
```

Allowed toy phi default:

```txt
phi_log = sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2
```

---

# 7. Dimensionless/admissibility checks

Implement:

```python
check_log_boundary_admissibility(spec: LogBoundaryCandidateSpec) -> EquationAdmissibilityResult
```

Checks:

```txt
observable exists
baseline equation exists
candidate equation exists
dimensionless variables declared
log arguments dimensionless
DeltaGamma_log has units compatible with rate
failure conditions exist
parameter ranges declared
scale L is declared and not post-hoc
```

Block if:

```txt
dimensionful log
missing observable
missing failure condition
ad hoc scale
unbounded parameters
```

---

# 8. Synthetic benchmark design

Implement:

```python
design_synthetic_benchmark(spec: LogBoundaryCandidateSpec) -> SyntheticBenchmarkDesignResult
```

It must produce:

```txt
baseline model
candidate model
delta metric
t_grid
parameter sweep plan
epsilon_exp
failure condition list
canonical status
allowed claims
blocked claims
next actions
```

Status:

```txt
SYNTHETIC_BENCHMARK_DESIGNED
```

Canonical permission:

```txt
TEST_DESIGN_ALLOWED
```

Evidence/support:

```txt
HEURISTIC_ONLY / HEURISTIC
```

Blocked reasons:

```txt
MISSING_SOURCE_SUPPORT
MISSING_BENCHMARK
MISSING_EXPERIMENTAL_DATA
```

---

# 9. Detectability protocol

Implement:

```python
build_detectability_protocol(spec: LogBoundaryCandidateSpec) -> DetectabilityProtocolSpec
```

Must define:

```txt
V_base
V_log
delta(t)
max_abs_delta
epsilon_exp
alpha sweep
k/u0/w0 sweep
detectability classification
failure classification
```

Do not execute full physical validation.

---

# 10. Reports

Generate:

```txt
reports/synthetic_benchmark_design/log_boundary_candidate_formalization_v2_3.md
reports/synthetic_benchmark_design/log_boundary_synthetic_benchmark_design_v2_3.md
reports/synthetic_benchmark_design/log_boundary_detectability_failure_protocol_v2_3.md
reports/synthetic_benchmark_design/heuristic_to_benchmark_canonical_contract_v2_3.md
reports/campaigns/HEURISTIC-CANDIDATE-SYNTHETIC-BENCHMARK-v2_3.md
```

Reports must include canonical status section.

---

# 11. Tests

Create:

```txt
tests/test_log_boundary_candidate_formalization_v2_3.py
tests/test_log_boundary_admissibility_v2_3.py
tests/test_synthetic_benchmark_design_v2_3.py
tests/test_log_boundary_detectability_protocol_v2_3.py
tests/test_heuristic_to_benchmark_report_contract_v2_3.py
tests/test_heuristic_candidate_synthetic_benchmark_campaign_v2_3.py
```

Minimum tests:

```txt
test_log_boundary_candidate_has_explicit_equation
test_log_boundary_uses_dimensionless_variables
test_delta_gamma_log_has_rate_units_by_construction
test_missing_observable_blocks_admissibility
test_missing_failure_condition_blocks_admissibility
test_ad_hoc_scale_blocks_admissibility
test_synthetic_benchmark_design_has_delta_metric
test_synthetic_benchmark_design_permission_is_test_design_allowed
test_synthetic_benchmark_does_not_authorize_physical_claim
test_detectability_protocol_defines_max_abs_delta
test_reports_include_canonical_section
test_campaign_generates_reports
```

---

# 12. Behavior preservation

Do not alter:

```txt
existing heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing v1.5 candidate benchmark outputs
existing business/candidate/copilot gates
historical reports
```

---

# 13. Do not overclaim

Do not write:

```txt
LOG_BOUNDARY predicts decoherence.
LOG_BOUNDARY validates Frontera C.
Synthetic design proves the effect.
```

Allowed:

```txt
LOG_BOUNDARY has an explicit synthetic benchmark design.
LOG_BOUNDARY is ready for synthetic execution.
LOG_BOUNDARY remains unsupported by sources/data.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
baseline remains intact
LOG_BOUNDARY formalization exists
admissibility checks work
synthetic benchmark design exists
detectability protocol exists
canonical report sections exist
campaign reports generated
no physical claim is authorized
```

Expected test count:

```txt
497 + new v2.3 tests
```

---

# 15. Final discipline

```txt
Now that the heuristic chose a door,
the benchmark design makes that door pay mathematical rent.
```
