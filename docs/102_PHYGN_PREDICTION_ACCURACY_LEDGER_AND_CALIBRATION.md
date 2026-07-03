# Phygn v1.7 — Prediction Accuracy Ledger & Calibration

## 0. Purpose

This document defines how Phygn measures whether passing its filters improves real predictive quality.

A gatekeeper that never audits its own outcomes can become dogma.

Phygn must track:

```txt
what it allowed
what it blocked
what happened later
whether its confidence was calibrated
whether passing filters improved results
```

---

## 1. PredictionRecord

```python
class PredictionRecord(BaseModel):
    prediction_id: str
    hypothesis_id: str | None
    claim_id: str | None
    mode: str
    ladder_level: str
    domain: str
    prediction_text: str
    target_variable: str
    predicted_direction: str | None
    predicted_value: float | None
    predicted_probability: float | None
    time_horizon: str
    baseline_reference: str | None
    evidence_level: str
    gate_status: str
    confidence_score: float | None
    created_at: str
    resolution_due_at: str | None
```

---

## 2. PredictionOutcome

```python
class PredictionOutcome(BaseModel):
    prediction_id: str
    resolved: bool
    actual_value: float | None
    actual_direction: str | None
    success: bool | None
    error_value: float | None
    benchmark_value: float | None
    benchmark_success: bool | None
    resolved_at: str | None
    notes: str | None
```

---

## 3. Core metrics

Phygn must compute:

```txt
hit_rate
base_rate
accuracy_lift
precision
recall
false_positive_rate
false_negative_rate
Brier score
expected calibration error
mean absolute error
benchmark_relative_error
```

Domain-specific metrics may include:

```txt
profit/loss
max drawdown
Sharpe/Sortino if appropriate
information coefficient
directional accuracy
```

---

## 4. Filter usefulness test

Compute:

```txt
accuracy_given_pass
accuracy_given_low_level
accuracy_given_blocked_if_simulated
lift_over_baseline
```

If:

```txt
accuracy_given_pass <= baseline_accuracy
```

then:

```txt
FILTER_NOT_PREDICTIVELY_USEFUL_YET
```

If:

```txt
accuracy_given_pass > baseline_accuracy
```

then:

```txt
FILTER_SHOWS_PREDICTIVE_LIFT
```

---

## 5. Calibration

For probabilistic predictions:

```txt
predicted_probability
actual outcome
```

Compute:

```txt
Brier score
calibration bins
expected calibration error
overconfidence index
```

If confidence is high but accuracy low:

```txt
OVERCONFIDENT_GATE
```

If confidence is low but accuracy high:

```txt
UNDERCONFIDENT_GATE
```

---

## 6. Ladder-level analysis

Track outcomes by:

```txt
DREAM
HYPOTHESIS_SEED
TESTABLE_HYPOTHESIS
SYNTHETIC_SUPPORT
SOURCE_BACKED_LIMITED
BENCHMARK_SUPPORTED
OPERATIONALLY_ACTIONABLE
```

Expected pattern:

```txt
higher ladder levels should show better reliability
```

If not:

```txt
LADDER_NOT_PREDICTIVELY_ORDERED
```

This is a serious system warning.

---

## 7. Post-mortem loop

Every resolved prediction should generate:

```txt
what was predicted
what happened
was the baseline beaten
which evidence was useful
which claim failed
which gate was too strict/too loose
what should be changed
```

---

## 8. Reports

Generate:

```txt
reports/prediction_accuracy/prediction_ledger_v1_7.md
reports/prediction_accuracy/calibration_report_v1_7.md
reports/prediction_accuracy/filter_lift_report_v1_7.md
reports/prediction_accuracy/post_mortem_report_v1_7.md
```

---

## 9. Final principle

```txt
Phygn must not only judge hypotheses.
It must judge the quality of its own judgments.
```
