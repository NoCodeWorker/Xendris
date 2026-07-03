# Phygn v4.0 — Debt-Aware Benchmark Construction & SLOT_4 Resolution Plan Goal

## 0. Context

The latest confirmed document is:

```txt
docs/250_PHYGN_V3_9_SOURCE_PRESSURE_DECISION_GATE_RESULTS.md
```

Therefore, v4.0 starts at:

```txt
251
```

v3.9 produced the first source-pressure decision:

```txt
PHI_GRADIENT_SOURCE_PRESSURE_LIMITED_SUPPORT
primary_decision = PHI_GRADIENT_REAL_SOURCE_BACKED_LIMITED
confidence = LOW
gradient_component_support = false
physical_claim_permission = BLOCKED
```

v3.9 found:

```txt
baseline decoherence framing: limited source backing
visibility/coherence observable: limited source backing
benchmark ranges: relevant
parameter constraints: limited source backing
limitations: present
SLOT_4 gradient-transition-effective-dynamics: 0 validation-ready extracts
```

v4.0 must build only from what survived.

---

## 1. Core thesis

```txt
Build the benchmark from what survived.
Do not build the claim from what is missing.
```

v4.0 is not a claim-upgrade phase.

v4.0 is a benchmark construction and debt-management phase.

---

## 2. Hard rule

```txt
No benchmark construction may imply gradient mechanism support.
No SLOT_4 debt closure without validation-ready SLOT_4 extracts.
No physical claim.
No Frontera C validation.
No empirical confirmation of the invariant.
```

---

## 3. Two-track architecture

v4.0 creates two formal tracks:

```txt
Track A — Debt-Aware Benchmark Dataset Construction
Track B — SLOT_4 Gradient-Component Debt Resolution Plan
```

Track A may proceed because v3.9 found benchmark-relevant source pressure.

Track B remains blocking for gradient-mechanism claims.

---

## 4. Track A: allowed construction

Track A may use:

```txt
SLOT_1_DECOHERENCE_BASELINE
SLOT_2_VISIBILITY_COHERENCE_OBSERVABLE
SLOT_3_BENCHMARK_RANGES
SLOT_5_PARAMETER_CONSTRAINTS
SLOT_6_NEGATIVE_CONSTRAINTS_LIMITATIONS
SLOT_7_EXPERIMENTAL_CONTEXT
```

Track A must not use:

```txt
SLOT_4 as source-backed mechanism
```

---

## 5. Track B: explicit debt

Create debt object:

```txt
DEBT-SLOT4-GRADIENT-COMPONENT-GAP
```

Debt status:

```txt
OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

Blocks:

```txt
PHI_GRADIENT as physical gradient mechanism
Frontera C empirical validation
invariant empirical confirmation
gradient-component source-backed claim
```

Does not block:

```txt
benchmark dataset construction
observable alignment
baseline decoherence modeling
negative-control comparisons
targeted SLOT_4 source acquisition
Pedernales manual review
```

---

## 6. Inputs

Load:

```txt
data/real_sources/source_pressure/phi_gradient_source_pressure_decision_v3_9.json
data/real_sources/source_pressure/phi_gradient_extract_pressure_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_slot_pressure_summary_v3_9.json
data/real_sources/source_pressure/phi_gradient_benchmark_alignment_v3_9.json
data/real_sources/source_pressure/phi_gradient_contradiction_and_limitation_map_v3_9.json
data/real_sources/source_pressure/phi_gradient_next_model_update_recommendations_v3_9.json
data/real_sources/extracts/phi_gradient_validation_ready_extract_pack_v3_8_3.json
data/real_sources/source_hashes_v3_6.json
```

---

## 7. Outputs

Create:

```txt
data/benchmarks/phi_gradient_benchmark_dataset_manifest_v4_0.json
data/benchmarks/phi_gradient_observable_alignment_v4_0.json
data/benchmarks/phi_gradient_benchmark_rows_v4_0.json
data/benchmarks/phi_gradient_negative_control_plan_v4_0.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/debts/slot4_resolution_plan_v4_0.json
data/benchmarks/phi_gradient_v4_0_next_gate_inputs.json
```

---

## 8. v4.0 statuses

```txt
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_PARTIAL
PHI_GRADIENT_SLOT4_DEBT_OPEN_BLOCKING
PHI_GRADIENT_BENCHMARK_BLOCKED_MISSING_SOURCE_PRESSURE
PHI_GRADIENT_BENCHMARK_BLOCKED_NO_OBSERVABLE_ALIGNMENT
```

Expected active status:

```txt
PHI_GRADIENT_DEBT_AWARE_BENCHMARK_READY
```

with concurrent debt status:

```txt
DEBT-SLOT4-GRADIENT-COMPONENT-GAP = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

---

## 9. Acceptance criteria

v4.0 is complete when:

```txt
v3.9 source pressure loaded
benchmark-relevant extracts selected
observable alignment dataset created
benchmark rows generated or queued
negative-control plan generated
SLOT_4 debt object created
SLOT_4 resolution plan created
reports generated
tests pass
physical claims remain blocked
```

---

## 10. Final principle

```txt
A rigorous roadmap does not hide debt.
It gives debt authority over claims.
```
