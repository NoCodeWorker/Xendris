# Phygn v1.4 — Candidate Observable & Parameter Protocol

## 0. Purpose

This protocol defines how a Frontera C candidate becomes operational enough to enter the Positive Prediction Gate.

---

## 1. CandidatePredictionSpec

```python
class CandidatePredictionSpec(BaseModel):
    candidate_id: str
    observable: str
    baseline_model: str
    candidate_model: str
    candidate_term: str
    parameters: dict[str, float | str]
    parameter_status: str
    data_target: str | None
    error_metric: str | None
    expected_pattern: str | None
    detectability_threshold: float | None
    failure_condition: list[str]
    source_ids: list[str]
    benchmark_ids: list[str]
    claim_level_requested: int
```

---

## 2. Required observable

For CAMPAIGN-002:

```txt
observable = visibility_loss
```

or:

```txt
observable = coherence_decay
```

The candidate and baseline must output the same observable.

If not:

```txt
BLOCKED_OBSERVABLE_MISMATCH
```

---

## 3. Parameter statuses

```txt
FIXED_BY_DEFINITION
SOURCE_BACKED
PRE_REGISTERED
FITTED_WITH_PENALTY
FREE_UNCONSTRAINED
AD_HOC
```

Rules:

```txt
FREE_UNCONSTRAINED -> UNDERIDENTIFIED_CANDIDATE
AD_HOC -> BLOCKED_AS_AD_HOC_CANDIDATE
PRE_REGISTERED -> admissible for toy benchmark
SOURCE_BACKED -> admissible for physical interpretation if sources pass
```

---

## 4. Expected pattern

Candidate must state expected pattern before benchmark:

```txt
increased decay rate
decreased visibility
mass dependence
L dependence
Q/B region dependence
threshold behavior
```

If no expected pattern:

```txt
POSITIVE_PREDICTION_NOT_OPERATIONALIZED
```

---

## 5. Detectability threshold

Candidate must declare:

```txt
epsilon_exp
```

or:

```txt
DETECTABILITY_REQUIRES_THRESHOLD
```

Without threshold:

```txt
not detectable
```

---

## 6. Candidate readiness statuses

```txt
CANDIDATE_NOT_OPERATIONALIZED
CANDIDATE_TOY_OPERATIONALIZED
CANDIDATE_REQUIRES_EVIDENCE
CANDIDATE_READY_FOR_SYNTHETIC_BENCHMARK
CANDIDATE_READY_FOR_SOURCE_BACKED_BENCHMARK
CANDIDATE_BLOCKED
```

---

## 7. Reports

Generate:

```txt
reports/prediction_pressure/candidate_model_readiness_v1_4.md
```

---

## 8. Tests

Required tests:

```txt
test_candidate_missing_observable_blocks
test_candidate_observable_mismatch_blocks
test_free_parameters_underidentified
test_ad_hoc_parameters_blocked
test_preregistered_toy_candidate_passes_gate
test_source_backed_required_for_physical_interpretation
```

---

## 9. Final principle

```txt
A candidate without an observable is not a prediction.
It is vocabulary.
```
