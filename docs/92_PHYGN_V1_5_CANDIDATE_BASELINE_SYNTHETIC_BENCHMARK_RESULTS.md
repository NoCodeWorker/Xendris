# Phygn v1.5 — Candidate vs Baseline Synthetic Benchmark Results

Date: 2026-06-30

Source prompt:

```txt
docs/91_PHYGN_CODEX_V1_5_CANDIDATE_BASELINE_SYNTHETIC_BENCHMARK_PROMPT.md
```

Supporting specs:

```txt
docs/87_PHYGN_V1_5_CANDIDATE_BASELINE_SYNTHETIC_BENCHMARK_docs/status/GOAL.md
docs/88_PHYGN_SYNTHETIC_BENCHMARK_DESIGN_FOR_CANDIDATE.md
docs/89_PHYGN_DELTA_AND_DETECTABILITY_PROTOCOL.md
docs/90_PHYGN_CANDIDATE_FAILURE_REPORT_PROTOCOL.md
```

Prior session:

```txt
docs/86_PHYGN_V1_4_CANDIDATE_MODEL_OPERATIONALIZATION_RESULTS.md
```

---

## 1. Completion Status

Status: **COMPLETE UNDER THE v1.5 PROMPT SPECIFICATIONS AND ACCEPTANCE CRITERIA**

All acceptance criteria from §14 of the prompt are satisfied:

| Criterion | Result |
|---|---|
| `pytest -q` passes | ✅ **339 passed, 0 failed** (297 baseline + 42 new) |
| Benchmark computation works | ✅ V_base vs V_candidate computed via exact exponential |
| Delta and detectability computed | ✅ max_abs_delta and detectability_status evaluated |
| Alpha sweep works | ✅ 7-point sweep over [1e0..1e40] |
| alpha_min estimate works | ✅ First-order estimate: ≈ 2.22e+30 |
| Failure report generated | ✅ `CAND-FC-B-NEGCTRL-001_failure_report_v1_5.md` |
| Default candidate remains physically blocked | ✅ All physical claims remain BLOCKED |
| Reports generated | ✅ 5 reports written |

---

## 2. New Modules Implemented (v1.5)

### Candidate Layer

- [synthetic_benchmark.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/synthetic_benchmark.py)
  — `CandidateSyntheticBenchmarkInput`, `CandidateSyntheticBenchmarkResult`, `run_synthetic_benchmark()`.
  Core V_base / V_candidate computation using pure Python `math.exp`.

- [detectability.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/detectability.py)
  — `classify_detectability()`, `classify_alpha_reasonableness()`, `estimate_alpha_min_for_detectability()`.

- [alpha_sweep.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/alpha_sweep.py)
  — `run_alpha_sweep()`, `find_first_detectable_alpha()`. Default sweep: [1e0, 1e10, 1e20, 1e30, 1e35, 1e38, 1e40].

- [failure_report_v1_5.py](file:///d:/BIOCULTOR/PHYNG/phyng/candidates/failure_report_v1_5.py)
  — `evaluate_v1_5_failure_conditions()`, `classify_candidate_survival()`.

### Campaign Layer

- [candidate_baseline_synthetic_benchmark.py](file:///d:/BIOCULTOR/PHYNG/phyng/campaigns/candidate_baseline_synthetic_benchmark.py)
  — Full orchestrator: runs benchmark, alpha sweep, and writes all 5 reports.

---

## 3. Benchmark Results (CAND-FC-B-NEGCTRL-001, default alpha=1.0)

| Metric | Value |
|---|---|
| B | 7.426160269118667e-38 |
| gamma_env | 0.05 |
| alpha (default) | 1.0 |
| DeltaGamma_C | ~7.43e-38 |
| max_abs_delta | ~0.0 (< epsilon_fp) |
| epsilon_exp | 1e-6 |
| detectability_status | `UNDETECTABLE_SYNTHETIC_DELTA` |
| synthetic_gain_status | `NOT_COMPUTABLE_WITHOUT_Y_TRUE` |
| candidate_survival | `SURVIVES_AS_TOY_NEGATIVE_CONTROL` |

### alpha_min estimate

```txt
alpha_min ≈ 2.22e+30  →  ALPHA_EXTREME
```

The B-suppressed candidate requires an extreme (toy-unphysical) alpha to be synthetically detectable.

---

## 4. Alpha Sweep Summary

| alpha | detectability_status | alpha_reasonableness |
|---|---|---|
| 1e0 | UNDETECTABLE_SYNTHETIC_DELTA | ALPHA_REASONABLE_TOY |
| 1e10 | UNDETECTABLE_SYNTHETIC_DELTA | ALPHA_LARGE |
| 1e20 | UNDETECTABLE_SYNTHETIC_DELTA | ALPHA_LARGE |
| 1e30 | UNDETECTABLE_SYNTHETIC_DELTA | ALPHA_EXTREME |
| 1e35 | UNDETECTABLE_SYNTHETIC_DELTA | ALPHA_EXTREME |
| 1e38 | DETECTABLE_SYNTHETIC_DELTA | ALPHA_UNPHYSICAL_OR_UNCONSTRAINED |
| 1e40 | DETECTABLE_SYNTHETIC_DELTA | ALPHA_UNPHYSICAL_OR_UNCONSTRAINED |

The candidate becomes detectable only at `ALPHA_UNPHYSICAL_OR_UNCONSTRAINED` scale. This triggers `REQUIRES_UNPHYSICAL_ALPHA`.

---

## 5. Failure Conditions Triggered

```txt
FAIL_UNDETECTABLE_DELTA
FAIL_NO_BENCHMARK
FAIL_NO_SOURCE_SUPPORT
REQUIRES_UNPHYSICAL_ALPHA
```

---

## 6. Reports Generated (5 total)

```txt
reports/benchmarks/BENCH-CAND-FC-B-NEGCTRL-001-SYNTH-001.md
reports/candidates/CAND-FC-B-NEGCTRL-001_synthetic_benchmark_v1_5.md
reports/candidates/CAND-FC-B-NEGCTRL-001_alpha_sweep_v1_5.md
reports/prediction_pressure/CAND-FC-B-NEGCTRL-001_failure_report_v1_5.md
reports/campaigns/CANDIDATE-BASELINE-SYNTHETIC-BENCHMARK-v1_5.md
```

---

## 7. Test Verification Summary

```
======================== 339 passed in 2.31s ========================
```

Previous baseline (v1.4): 297 passed → **+42 new tests added**.

### New test files (v1.5)

| File | Tests | All Pass |
|---|---|---|
| [test_candidate_synthetic_benchmark_v1_5.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_synthetic_benchmark_v1_5.py) | 8 | ✅ |
| [test_candidate_detectability_v1_5.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_detectability_v1_5.py) | 11 | ✅ |
| [test_candidate_alpha_sweep_v1_5.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_alpha_sweep_v1_5.py) | 7 | ✅ |
| [test_candidate_failure_report_v1_5.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_failure_report_v1_5.py) | 9 | ✅ |
| [test_candidate_baseline_synthetic_campaign_v1_5.py](file:///d:/BIOCULTOR/PHYNG/tests/test_candidate_baseline_synthetic_campaign_v1_5.py) | 7 | ✅ |

---

## 8. Physical Claims

Physical claims remain **BLOCKED**.

Allowed statements:
- The candidate was synthetically benchmarked.
- The candidate is `UNDETECTABLE_SYNTHETIC_DELTA` under declared toy parameters.
- The candidate requires extreme alpha (≈ 2.22e+30) for synthetic detectability.
- Physical claims remain blocked.

Blocked statements:
- Phygn predicts decoherence.
- Frontera C is validated.
- Candidate has physical PredictiveGain.
- Synthetic delta proves physical effect.

---

## 9. Scientific Discipline Note

> The candidate entered the ring.
> It did not win by faith.
> It bled numbers.

The B-suppressed candidate `CAND-FC-B-NEGCTRL-001` is quantitatively confirmed as a negative control: under all physically plausible alpha values, it produces an undetectable synthetic delta. Detectability requires alpha ~ 1e38, which is flagged as `ALPHA_UNPHYSICAL_OR_UNCONSTRAINED`.

This is the expected and correct result. The system is working as designed.
