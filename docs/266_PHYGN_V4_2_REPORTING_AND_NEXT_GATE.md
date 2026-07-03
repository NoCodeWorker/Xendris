# Phygn v4.2 — Reporting & Next Gate

## 0. Purpose

This document defines reports and transition logic after observable normalization.

---

## 1. Required reports

Generate:

```txt
reports/observables/phi_gradient_observable_schema_v4_2.md
reports/observables/phi_gradient_normalized_observable_targets_v4_2.md
reports/observables/phi_gradient_y_true_acquisition_plan_v4_2.md
reports/observables/phi_gradient_dataset_source_registry_v4_2.md
reports/observables/phi_gradient_measurement_readiness_matrix_v4_2.md
reports/observables/phi_gradient_quality_control_rules_v4_2.md
reports/campaigns/PHI-GRADIENT-OBSERVABLE-DATASET-YTRUE-PLAN-v4_2.md
```

---

## 2. Report requirements

Reports must include:

```txt
input benchmark row count
normalized target count
observable class coverage
y_true status counts
acquisition method counts
measurement readiness summary
PredictiveGain status
SLOT_4 debt status
allowed claims
blocked claims
next recommended phase
canonical status
discipline note
```

---

## 3. Canonical statuses

Add:

```txt
PHI_GRADIENT_OBSERVABLE_DATASET_NORMALIZED
PHI_GRADIENT_YTRUE_ACQUISITION_PLAN_READY
PHI_GRADIENT_YTRUE_PLAN_PARTIAL
PHI_GRADIENT_YTRUE_PLAN_BLOCKED_MISSING_MODEL_COMPARISON
PHI_GRADIENT_YTRUE_PLAN_NO_ACQUIRABLE_TARGETS
PHI_GRADIENT_YTRUE_PLAN_REQUIRES_EXPERIMENTAL_DATA
```

Suggested mapping:

```txt
Canonical Permission: REVIEW_REQUIRED
Evidence Level: REAL_SOURCE_PRESSURE_LIMITED
Support Level: LIMITED
Risk Level: SCIENTIFIC_RISK
```

Blocked claims remain:

```txt
PHI_GRADIENT is predictively validated.
PHI_GRADIENT has PredictiveGain.
Gradient mechanism is supported.
Frontera C is validated.
Invariant is empirically confirmed.
```

---

## 4. Allowed claims

Allowed:

```txt
Observable targets were normalized.
A y_true acquisition plan was generated.
PredictiveGain remains undefined until observed truth exists.
SLOT_4 debt remains blocking for mechanism claims.
```

---

## 5. Possible next phases

If public/manual data appears acquirable:

```txt
v4.3 — Real y_true Extraction & Dataset Assembly
```

If most targets require experiment:

```txt
v4.3 — Experimental Observable Design & Feasibility Gate
```

Parallel:

```txt
v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review
```

---

## 6. Final principle

```txt
The next gate must bring numbers, not just structure.
```
