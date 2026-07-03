# Phygn v2.3 - Heuristic Candidate to Synthetic Benchmark Design Results

Date: 2026-06-30

Source prompt:

```txt
docs/140_PHYGN_CODEX_V2_3_HEURISTIC_CANDIDATE_BENCHMARK_PROMPT.md
```

Supporting specs:

```txt
docs/136_PHYGN_V2_3_HEURISTIC_CANDIDATE_SYNTHETIC_BENCHMARK_docs/status/GOAL.md
docs/137_PHYGN_LOG_BOUNDARY_CANDIDATE_FORMALIZATION.md
docs/138_PHYGN_LOG_BOUNDARY_DETECTABILITY_AND_FAILURE_PROTOCOL.md
docs/139_PHYGN_HEURISTIC_TO_BENCHMARK_REPORT_CONTRACT.md
docs/135_PHYGN_V2_2_HEURISTIC_DISCOVERY_RESULTS.md
docs/129_PHYGN_V2_1_CANONICAL_STATUS_MAPPING_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v2.3 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

v2.3 converted the top-ranked v2.2 heuristic candidate:

```txt
HEUR-PHY-003 / LOG_BOUNDARY
```

into an explicit synthetic benchmark design.

No physical validation was claimed.

No existing heuristic discovery outputs were changed.

No existing v2.1 canonical mapping behavior was broken.

No existing v1.5 candidate benchmark outputs were changed.

No business/candidate/copilot gates were changed.

Final validation:

```txt
pytest -q
510 passed in 20.77s
```

Baseline before v2.3:

```txt
pytest -q
497 passed in 19.98s
```

Net result:

```txt
497 baseline tests + 13 v2.3 tests = 510 passing tests
```

---

## 2. New Package and Campaign

Created:

```txt
phyng/synthetic_benchmark_design/
  __init__.py
  schemas.py
  log_boundary.py
  admissibility.py
  detectability_protocol.py
  report.py
```

Created campaign:

```txt
phyng/campaigns/heuristic_candidate_synthetic_benchmark.py
```

Campaign entrypoint:

```python
run_heuristic_candidate_synthetic_benchmark_campaign(root: str | Path = ".")
```

Campaign status:

```txt
SYNTHETIC_BENCHMARK_DESIGNED
```

---

## 3. Schemas Implemented

Implemented in:

```txt
phyng/synthetic_benchmark_design/schemas.py
```

Schemas:

```txt
LogBoundaryCandidateSpec
SyntheticBenchmarkDesign
EquationAdmissibilityResult
DetectabilityProtocolSpec
SyntheticBenchmarkDesignResult
HeuristicToBenchmarkCampaignResult
```

v2.1 integration:

```txt
CanonicalStatusRecord
CanonicalReportContract
```

---

## 4. Canonical Mapping Added

Added v2.3 statuses to the v2.1 compatibility layer:

```txt
SYNTHETIC_BENCHMARK_DESIGNED
SYNTHETIC_BENCHMARK_BLOCKED
```

Canonical interpretation:

| Status | Permission | Evidence | Support | Blocked Reasons |
|---|---|---|---|---|
| `SYNTHETIC_BENCHMARK_DESIGNED` | `TEST_DESIGN_ALLOWED` | `HEURISTIC_ONLY` | `HEURISTIC` | `MISSING_SOURCE_SUPPORT`, `MISSING_BENCHMARK`, `MISSING_EXPERIMENTAL_DATA` |
| `SYNTHETIC_BENCHMARK_BLOCKED` | `CLAIM_BLOCKED` | `HEURISTIC_ONLY` | `HEURISTIC` | `HUMAN_REVIEW_REQUIRED` |

Hard rule preserved:

```txt
SYNTHETIC_BENCHMARK_DESIGNED permits test design only.
It does not authorize physical prediction, experimental validation, or source-backed claims.
```

---

## 5. LOG_BOUNDARY Formalization

Implemented in:

```txt
phyng/synthetic_benchmark_design/log_boundary.py
```

Function:

```python
create_log_boundary_candidate_spec(...) -> LogBoundaryCandidateSpec
```

Default candidate:

| Field | Value |
|---|---|
| `candidate_id` | `HEUR-PHY-003` |
| `candidate_family` | `LOG_BOUNDARY` |
| `observable` | `visibility_decay` |
| `baseline_equation` | `V_base(t)=exp(-Gamma_env*t)` |
| `candidate_equation` | `V_log(t)=exp(-(Gamma_env + DeltaGamma_log)*t)` |
| `delta_gamma_equation` | `DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)` |
| `phi_function` | `sigmoid(k * (u - u0)) * tanh(k2 * (w - w0))^2` |

Dimensionless variables declared:

```txt
q
b
u
w
alpha
k
k2
u0
w0
```

Parameter ranges declared:

```txt
alpha
k
k2
u0
w0
Gamma_env
m_kg
L_m
```

Dimensional construction:

```txt
DeltaGamma_log = alpha * Gamma_env * phi_log(q,b,u,w)
```

Because `alpha` and `phi_log` are dimensionless and `Gamma_env` has rate units, `DeltaGamma_log` has rate units by construction.

---

## 6. Admissibility Checks

Implemented in:

```txt
phyng/synthetic_benchmark_design/admissibility.py
```

Function:

```python
check_log_boundary_admissibility(spec: LogBoundaryCandidateSpec) -> EquationAdmissibilityResult
```

Checks:

```txt
observable exists
baseline equation exists
candidate equation exists
dimensionless variables declared
log arguments dimensionless / no dimensionful log detected
DeltaGamma_log has rate units by construction
failure conditions exist
parameter ranges declared
scale L is declared and not post-hoc
```

Blocks:

```txt
FAIL_NO_OBSERVABLE
FAIL_NO_EXPLICIT_EQUATION
FAIL_DIMENSIONAL_INCONSISTENCY
FAIL_NO_FAILURE_CONDITION
FAIL_UNBOUNDED_PARAMETERS
FAIL_AD_HOC_SCALE
```

Default LOG_BOUNDARY result:

```txt
admissible: true
```

---

## 7. Synthetic Benchmark Design

Implemented in:

```txt
phyng/synthetic_benchmark_design/log_boundary.py
```

Function:

```python
design_synthetic_benchmark(spec: LogBoundaryCandidateSpec) -> SyntheticBenchmarkDesignResult
```

Benchmark design:

| Field | Value |
|---|---|
| Baseline model | `V_base(t)=exp(-Gamma_env*t)` |
| Candidate model | `V_log(t)=exp(-(Gamma_env + DeltaGamma_log)*t)` |
| Delta metric | `max_abs_delta = max_t |V_log(t) - V_base(t)|` |
| t grid count | `101` |
| epsilon threshold | `1e-06` |

Parameter sweep plan:

```txt
alpha_values: [0.1, 1.0, 3.0, 10.0]
k_values: [0.5, 1.0, 2.0, 5.0]
k2_values: [0.5, 1.0, 2.0, 5.0]
u0_values: [-90.0, -70.0, -50.0]
w0_values: [-40.0, -20.0, 0.0]
Gamma_env_values: [0.01, 0.05, 0.1]
```

Allowed claims:

```txt
LOG_BOUNDARY has an explicit toy equation.
LOG_BOUNDARY has declared parameter ranges.
LOG_BOUNDARY has a synthetic benchmark design.
LOG_BOUNDARY may proceed to synthetic execution.
```

Blocked claims:

```txt
Physical prediction
Experimental validation
Source-backed claim
Benchmark-supported claim without benchmark execution/data
```

---

## 8. Detectability Protocol

Implemented in:

```txt
phyng/synthetic_benchmark_design/detectability_protocol.py
```

Function:

```python
build_detectability_protocol(spec: LogBoundaryCandidateSpec) -> DetectabilityProtocolSpec
```

Protocol definitions:

```txt
V_base(t)=exp(-Gamma_env*t)
V_log(t)=exp(-(Gamma_env + DeltaGamma_log)*t)
delta(t) = V_log(t) - V_base(t)
max_abs_delta = max_t |delta(t)|
epsilon_exp = 1e-06
```

Detectability classification:

```txt
DETECTABLE_SYNTHETIC_DELTA if max_abs_delta > epsilon_exp;
otherwise UNDETECTABLE_SYNTHETIC_DELTA
```

Failure classification rules:

```txt
FAIL_NO_EXPLICIT_EQUATION
FAIL_DIMENSIONAL_INCONSISTENCY
FAIL_NO_OBSERVABLE
FAIL_NO_FAILURE_CONDITION
FAIL_AD_HOC_SCALE
FAIL_UNDETECTABLE_DELTA
FAIL_DETECTABLE_ONLY_WITH_EXTREME_PARAMETERS
FAIL_NO_SOURCE_SUPPORT
FAIL_NO_BENCHMARK
FAIL_NO_EXPERIMENTAL_DATA
```

---

## 9. Reports Generated

Generated:

```txt
reports/synthetic_benchmark_design/log_boundary_candidate_formalization_v2_3.md
reports/synthetic_benchmark_design/log_boundary_synthetic_benchmark_design_v2_3.md
reports/synthetic_benchmark_design/log_boundary_detectability_failure_protocol_v2_3.md
reports/synthetic_benchmark_design/heuristic_to_benchmark_canonical_contract_v2_3.md
reports/campaigns/HEURISTIC-CANDIDATE-SYNTHETIC-BENCHMARK-v2_3.md
```

Report safety:

```txt
All v2.3 reports include a canonical status section.
All v2.3 reports preserve the distinction between synthetic design and physical validation.
```

Campaign report blocked claims:

```txt
LOG_BOUNDARY predicts decoherence.
LOG_BOUNDARY validates Frontera C.
Synthetic design proves the effect.
```

---

## 10. Tests

Created:

```txt
tests/test_log_boundary_candidate_formalization_v2_3.py
tests/test_log_boundary_admissibility_v2_3.py
tests/test_synthetic_benchmark_design_v2_3.py
tests/test_log_boundary_detectability_protocol_v2_3.py
tests/test_heuristic_to_benchmark_report_contract_v2_3.py
tests/test_heuristic_candidate_synthetic_benchmark_campaign_v2_3.py
```

New v2.3 tests:

| Test | Purpose |
|---|---|
| `test_log_boundary_candidate_has_explicit_equation` | Confirms baseline/candidate/DeltaGamma equations exist |
| `test_log_boundary_uses_dimensionless_variables` | Confirms `q,b,u,w,alpha,k,k2,u0,w0` are declared |
| `test_delta_gamma_log_has_rate_units_by_construction` | Confirms rate units via `Gamma_env` construction |
| `test_missing_observable_blocks_admissibility` | Confirms missing observable blocks design |
| `test_missing_failure_condition_blocks_admissibility` | Confirms missing failure condition blocks design |
| `test_ad_hoc_scale_blocks_admissibility` | Confirms post-hoc scale blocks design |
| `test_synthetic_benchmark_design_has_delta_metric` | Confirms `max_abs_delta` metric exists |
| `test_synthetic_benchmark_design_permission_is_test_design_allowed` | Confirms `TEST_DESIGN_ALLOWED` only |
| `test_synthetic_benchmark_does_not_authorize_physical_claim` | Confirms physical/source/experimental claims remain blocked |
| `test_detectability_protocol_defines_max_abs_delta` | Confirms detectability protocol fields |
| `test_reports_include_canonical_section` | Confirms canonical sections in reports |
| `test_reports_do_not_authorize_physical_claim` | Confirms report language blocks overclaiming |
| `test_campaign_generates_reports` | Confirms campaign report generation |

Focused v2.3 verification:

```txt
pytest -q tests/test_log_boundary_candidate_formalization_v2_3.py tests/test_log_boundary_admissibility_v2_3.py tests/test_synthetic_benchmark_design_v2_3.py tests/test_log_boundary_detectability_protocol_v2_3.py tests/test_heuristic_to_benchmark_report_contract_v2_3.py tests/test_heuristic_candidate_synthetic_benchmark_campaign_v2_3.py
13 passed in 0.81s
```

Final full-suite verification:

```txt
pytest -q
510 passed in 20.77s
```

---

## 11. Behavior Preservation

v2.3 explicitly avoided changing:

```txt
existing heuristic discovery outputs
existing v2.1 canonical mapping behavior
existing v1.5 candidate benchmark outputs
existing business/candidate/copilot gates
historical reports
```

Meaning:

```txt
v2.3 adds a design layer between heuristic discovery and synthetic execution.
It does not execute a physical validation campaign.
```

---

## 12. Final Assessment

v2.3 successfully forces the v2.2 top heuristic candidate to pay mathematical rent:

```txt
explicit equation
dimensionless variables
observable
baseline model
candidate model
parameter ranges
delta metric
detectability threshold
failure conditions
canonical report contract
tests
```

The safe next step is:

```txt
Execute the synthetic benchmark under the declared parameter sweep,
compute max_abs_delta, classify synthetic detectability, and keep all physical
claims blocked until source support, benchmark data, or experimental evidence exists.
```

Final discipline note:

```txt
Now that the heuristic chose a door,
the benchmark design makes that door pay mathematical rent.
```
