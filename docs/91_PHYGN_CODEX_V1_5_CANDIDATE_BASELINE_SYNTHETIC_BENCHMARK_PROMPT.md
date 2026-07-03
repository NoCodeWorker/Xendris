# Codex Prompt — Phygn v1.5 Candidate vs Baseline Synthetic Benchmark

You are working in:

```txt
d:\BIOCULTOR\PHYNG\
```

Project:

```txt
Phygn — Physical Signatures Lab
```

Current state:

```txt
v1.4 complete.
Candidate families exist.
Default candidate exists: CAND-FC-B-NEGCTRL-001.
Candidate term: DeltaGamma_C = alpha * B.
Positive prediction gate has moved to POSITIVE_PREDICTION_REQUIRES_EVIDENCE.
Physical claims remain blocked.
324 tests passed.
```

Important numbering:

```txt
Previous result:
85_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_RESULTS.md

v1.5 docs:
86_PHYGN_V1_5_CANDIDATE_BASELINE_SYNTHETIC_BENCHMARK_docs/status/GOAL.md
87_PHYGN_SYNTHETIC_BENCHMARK_DESIGN_FOR_CANDIDATE.md
88_PHYGN_DELTA_AND_DETECTABILITY_PROTOCOL.md
89_PHYGN_CANDIDATE_FAILURE_REPORT_PROTOCOL.md
90_PHYGN_CODEX_V1_5_CANDIDATE_BASELINE_SYNTHETIC_BENCHMARK_PROMPT.md
```

---

# 1. Read first

Read:

```txt
docs/86_PHYGN_V1_5_CANDIDATE_BASELINE_SYNTHETIC_BENCHMARK_docs/status/GOAL.md
docs/87_PHYGN_SYNTHETIC_BENCHMARK_DESIGN_FOR_CANDIDATE.md
docs/88_PHYGN_DELTA_AND_DETECTABILITY_PROTOCOL.md
docs/89_PHYGN_CANDIDATE_FAILURE_REPORT_PROTOCOL.md
```

Also read:

```txt
docs/84_PHYGN_CODEX_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_PROMPT.md
docs/85_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_RESULTS.md
```

---

# 2. First action

Run:

```bash
pytest -q
```

If tests fail, fix core first.

---

# 3. Mission

Implement v1.5 support for:

```txt
candidate-vs-baseline synthetic benchmark
delta computation
detectability classification
alpha sweep
alpha_min estimate
failure condition update
candidate survival classification
reports
tests
```

This phase must not unlock physical claims.

---

# 4. New / extended modules

Create or extend:

```txt
phyng/candidates/synthetic_benchmark.py
phyng/candidates/detectability.py
phyng/candidates/alpha_sweep.py
phyng/candidates/failure_report_v1_5.py

phyng/campaigns/candidate_baseline_synthetic_benchmark.py
```

Reuse:

```txt
phyng/candidates/schemas.py
phyng/candidates/failure_conditions.py
phyng/candidates/readiness.py
phyng/benchmarks/schemas.py
phyng/model_comparison/metrics.py
```

---

# 5. Benchmark schema

Implement:

```python
class CandidateSyntheticBenchmarkInput(BaseModel):
    benchmark_id: str
    candidate_id: str
    system_id: str
    m_kg: float
    L_value_m: float
    B: float
    QB: float
    gamma_env: float
    alpha: float
    t_grid: list[float]
    epsilon_exp: float | None
    y_true: list[float] | None
    error_metric: str
    benchmark_provenance: str = "SYNTHETIC"
```

Output:

```python
class CandidateSyntheticBenchmarkResult(BaseModel):
    benchmark_id: str
    candidate_id: str
    v_base: list[float]
    v_candidate: list[float]
    delta: list[float]
    max_abs_delta: float
    detectability_status: str
    alpha_min_for_detectability: float | None
    synthetic_gain_status: str
    triggered_failure_conditions: list[str]
    allowed_claims: list[str]
    blocked_claims: list[str]
```

---

# 6. Core computation

Use:

```python
V_base(t) = exp(-gamma_env * t)
delta_gamma_c = alpha * B
V_candidate(t) = exp(-(gamma_env + delta_gamma_c) * t)
delta = V_candidate - V_base
max_abs_delta = max(abs(delta))
```

---

# 7. Alpha sweep

Implement:

```python
run_alpha_sweep(...)
```

Default:

```txt
alpha_values = [1e0, 1e10, 1e20, 1e30, 1e35, 1e38, 1e40]
```

Return:

```txt
alpha
delta_gamma_c
max_abs_delta
detectability_status
alpha_reasonableness_status
triggered_failures
```

---

# 8. Alpha minimum estimate

Implement:

```python
estimate_alpha_min_for_detectability(B, gamma_env, t_grid, epsilon_exp)
```

Use first-order estimate:

```txt
alpha_min ≈ epsilon_exp / (B * max(t * exp(-gamma_env*t)))
```

If denominator is zero:

```txt
None
```

---

# 9. Detectability

Statuses:

```txt
DETECTABLE_SYNTHETIC_DELTA
UNDETECTABLE_SYNTHETIC_DELTA
NO_THRESHOLD_DECLARED
```

---

# 10. Failure conditions

Trigger:

```txt
FAIL_UNDETECTABLE_DELTA
FAIL_NO_BENCHMARK
FAIL_NO_SOURCE_SUPPORT
REQUIRES_UNPHYSICAL_ALPHA
```

Do not compute physical PredictiveGain.

If y_true is None:

```txt
synthetic_gain_status = NOT_COMPUTABLE_WITHOUT_Y_TRUE
```

---

# 11. Reports

Generate:

```txt
reports/benchmarks/BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001.md
reports/candidates/CAND-FC-B-NEGCTRL-001_synthetic_benchmark_v1_5.md
reports/candidates/CAND-FC-B-NEGCTRL-001_alpha_sweep_v1_5.md
reports/prediction_pressure/CAND-FC-B-NEGCTRL-001_failure_report_v1_5.md
reports/campaigns/CANDIDATE-BASELINE-SYNTHETIC-BENCHMARK-v1_5.md
```

---

# 12. Tests

Add:

```txt
tests/test_candidate_synthetic_benchmark_v1_5.py
tests/test_candidate_detectability_v1_5.py
tests/test_candidate_alpha_sweep_v1_5.py
tests/test_candidate_failure_report_v1_5.py
tests/test_candidate_baseline_synthetic_campaign_v1_5.py
```

Minimum tests:

```txt
test_v_base_and_candidate_shapes_match
test_alpha_zero_or_tiny_produces_near_zero_delta
test_default_b_suppressed_candidate_undetectable
test_detectability_no_threshold
test_alpha_sweep_contains_expected_values
test_alpha_min_estimate_positive
test_unphysical_alpha_classification
test_no_y_true_blocks_predictive_gain
test_no_sources_blocks_physical_interpretation
test_reports_generated
test_campaign_runs
```

---

# 13. Do not overclaim

Do not write:

```txt
Phygn predicts decoherence.
Frontera C is validated.
Candidate has physical PredictiveGain.
Synthetic delta proves physical effect.
```

Allowed:

```txt
The candidate was synthetically benchmarked.
The candidate is undetectable/detectable under declared toy parameters.
The candidate requires extreme alpha for detectability.
Physical claims remain blocked.
```

---

# 14. Acceptance criteria

Complete when:

```txt
pytest -q passes
benchmark computation works
delta and detectability are computed
alpha sweep works
alpha_min estimate works
failure report generated
default candidate remains physically blocked
reports generated
```

---

# 15. Final discipline

```txt
Now the candidate enters the ring.
Not to win by faith, but to bleed numbers.
```
