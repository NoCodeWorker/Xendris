# Phygn v4.0 — Debt-Aware Benchmark & Scientific Debt Results

Date: 2026-07-01

Source prompt:
```txt
docs/255_PHYGN_CODEX_V4_0_DEBT_AWARE_BENCHMARK_PROMPT.md
```

Supporting specs:
```txt
docs/251_PHYGN_V4_0_DEBT_AWARE_BENCHMARK_docs/status/GOAL.md
docs/252_PHYGN_V4_0_BENCHMARK_DATASET_SCHEMA.md
docs/253_PHYGN_V4_0_SLOT4_DEBT_OBJECT_AND_RESOLUTION_PLAN.md
docs/254_PHYGN_V4_0_REPORTING_AND_NEXT_GATE.md
```

---

## 1. Completion Status
Status: **COMPLETE UNDER v4.0 PROMPT SPECIFICATIONS**

Final Campaign Status:
```txt
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY
```

Concurrent Scientific Debt Status:
```txt
DEBT-SLOT4-GRADIENT-COMPONENT-GAP = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

Tests run:
```txt
41 passed (27 v3.9 tests + 14 v4.0 tests) in 1.55s
```

---

## 2. Track A: Benchmark Construction Results
From the 29 validation-ready extracts from v3.8.3, 28 extracts survived v3.9 source pressure.
- **Row count**: 28
- **Observable alignment count**: 28
- **Negative-control count**: 6

No extracts from the missing `SLOT_4` (gradient component) were included. All benchmark rows have `gradient_claim_allowed = False` hardcoded.
Regime alignment details (mass, time, length/separation, temperature/pressure) were parsed and registered.

### Negative-Control Plan:
Includes:
1. `BASELINE_ONLY_CONTROL` (using SLOT_1 extracts)
2. `OBSERVABLE_ONLY_CONTROL` (using SLOT_2 extracts)
3. `BENCHMARK_RANGE_CONTROL` (using SLOT_3 extracts)
4. `PARAMETER_CONSTRAINT_CONTROL` (using SLOT_5 extracts)
5. `LIMITATION_STRESS_CONTROL` (using SLOT_6 extracts)
6. `NO_SLOT4_CONTROL` (always included to stress-test the model with slot 4 dynamics zeroed out)

---

## 3. Track B: Scientific Debt Registry & Resolution Plan
The unresolved evidence gap for `SLOT_4` is formalized.

- **Debt ID**: `DEBT-SLOT4-GRADIENT-COMPONENT-GAP`
- **Severity**: `HIGH`
- **Opened by**: `v3.9 source pressure decision`
- **Blocks**:
  - `PHI_GRADIENT as physical gradient mechanism`
  - `Frontera C empirical validation`
  - `invariant empirical confirmation`
  - `gradient-component source-backed claim`
- **Allowed work**:
  - `benchmark construction`
  - `observable alignment`
  - `baseline model comparison`
  - `negative-control design`
  - `SLOT_4 source acquisition`
  - `Pedernales manual review`
  - `candidate revision`
  - `kill/pivot analysis`

### Resolution tasks:
1. Pedernales manual review
2. Targeted SLOT_4 source acquisition
3. Exact SLOT_4 extraction
4. v3.8.3-style promotion
5. v3.9-style source pressure rerun
6. Keep/revise/kill gradient mechanism

---

## 4. Generated Data Artifacts
The following JSON files were created under `data/`:
- `data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json`
- `data/benchmarks/phi_gradient_observable_alignment_v4_0.json`
- `data/benchmarks/phi_gradient_benchmark_rows_v4_0.json`
- `data/benchmarks/phi_gradient_negative_control_plan_v4_0.json`
- `data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json`
- `data/debts/slot4_resolution_plan_v4_0.json`
- `data/benchmarks/phi_gradient_v4_0_next_gate_inputs.json`

---

## 5. Generated Reports
The following reports were created under `reports/` (all containing the appended `## Canonical Status` section):
- `reports/benchmark_construction/phi_gradient_benchmark_dataset_manifest_v4_0.md`
- `reports/benchmark_construction/phi_gradient_observable_alignment_v4_0.md`
- `reports/benchmark_construction/phi_gradient_benchmark_rows_v4_0.md`
- `reports/benchmark_construction/phi_gradient_negative_control_plan_v4_0.md`
- `reports/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.md`
- `reports/debts/slot4_resolution_plan_v4_0.md`
- `reports/campaigns/PHI-GRADIENT-DEBT-AWARE-BENCHMARK-v4_0.md`

---

## 6. Allowed and Blocked Claims

### Allowed Claims:
- `A debt-aware benchmark dataset was constructed.`
- `Observable alignment was created from source-pressure-limited extracts.`
- `SLOT_4 gradient-component debt remains open and blocking for mechanism claims.`

### Blocked Claims:
- `PHI_GRADIENT is validated.`
- `Frontera C is validated.`
- `The gradient mechanism is source-backed.`
- `The invariant has empirical confirmation.`
- `Benchmark construction proves physics.`

---

## 7. Next Phase Recommendation
- **Recommended next phase**: `v4.1 — Benchmark Model Comparison Without Gradient Claim`
- **Parallel track**: `v4.1-SLOT4 — Targeted SLOT_4 Source Acquisition & Manual Review`
