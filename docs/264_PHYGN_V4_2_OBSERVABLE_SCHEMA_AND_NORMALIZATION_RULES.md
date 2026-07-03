# Phygn v4.2 — Observable Schema & Normalization Rules

## 0. Purpose

This document defines how source-pressure-derived benchmark rows become normalized observable targets.

---

## 1. Observable schema

Create:

```txt
data/observables/phi_gradient_observable_schema_v4_2.json
```

Schema:

```python
class ObservableSchemaRecord(BaseModel):
    observable_class: str
    canonical_name: str
    allowed_units: list[str]
    expected_data_type: str
    valid_range_description: str
    source_slots: list[str]
    measurement_requirement: str
    y_true_definition: str
    notes: list[str]
```

---

## 2. Normalized observable target

Create:

```txt
data/observables/phi_gradient_normalized_observable_targets_v4_2.json
```

Schema:

```python
class NormalizedObservableTarget(BaseModel):
    target_id: str
    benchmark_id: str
    source_id: str
    extract_id: str
    observable_class: str
    observable_name: str
    source_observable_text: str
    normalized_variable_name: str
    unit: str | None
    expected_dtype: str
    measurement_context: str
    regime_fields: dict[str, str | None]
    candidate_model_fields: list[str]
    baseline_model_fields: list[str]
    y_true_required: bool
    y_true_status: str
    slot4_debt_status: str
    predictive_gain_allowed: bool
    notes: list[str]
```

---

## 3. Normalization rules

### VISIBILITY

Map source phrases:

```txt
visibility
fringe visibility
contrast
interference visibility
```

to:

```txt
observable_class = VISIBILITY
normalized_variable_name = visibility
unit = dimensionless
expected_dtype = float
valid range = [0, 1]
```

### COHERENCE_LOSS

Map:

```txt
loss of coherence
decoherence effect
coherence reduction
```

to:

```txt
observable_class = COHERENCE_LOSS
normalized_variable_name = coherence_loss
unit = dimensionless or rate-dependent
```

### DECOHERENCE_RATE

Map:

```txt
decoherence rate
gamma
Gamma
decay constant
```

to:

```txt
observable_class = DECOHERENCE_RATE
normalized_variable_name = decoherence_rate
unit = s^-1
```

### CONTRAST_DECAY

Map:

```txt
contrast decay
visibility decay
exponential visibility loss
```

to:

```txt
observable_class = CONTRAST_DECAY
normalized_variable_name = contrast_decay_rate
unit = s^-1 or dimensionless per time
```

### MASS/TIME/SEPARATION/TEMPERATURE/PRESSURE REGIMES

Create regime fields rather than direct y_true labels unless observed values exist.

---

## 4. Parameter bounds

SLOT_5 parameter constraints become:

```txt
observable_class = PARAMETER_BOUND
```

They are constraints, not observed outcomes.

---

## 5. Limitations

SLOT_6 limitations become:

```txt
observable_class = LIMITATION_FLAG
```

They are flags for exclusion, stress tests or model restrictions.

---

## 6. PredictiveGain rule

For every target:

```txt
predictive_gain_allowed = false
```

unless:

```txt
y_true_status = Y_TRUE_AVAILABLE
```

and an observed numeric outcome is present.

---

## 7. Final principle

```txt
Normalize observables.
Do not normalize hope into truth.
```
