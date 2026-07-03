# Phygn Master Goal — Frontera C Validation, Blockage or Falsification

## 0. Current state

Latest confirmed result:

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
```

Current state:

```txt
TARGETED_YTRUE_EXTRACTION_PARTIAL
observed_candidates_evaluated = 10
new_accepted_ytrue = 3
rejected_ytrue_candidates = 7
total_accepted_ytrue = 7
independent_source_count = 4
benchmark_readiness = PARTIAL_MULTI_SOURCE_N_SMALL
```

Current blocker:

```txt
MISSING_EXPERIMENTAL_DATA
MISSING_BENCHMARK
```

Current allowed next work:

```txt
v5.7.4 — Targeted Human Figure/Table Review or Additional Source Download & y_true Expansion
```

Current forbidden work:

```txt
PredictiveGain claim
Frontera C validation
physical claim
C-structure ablation
LOG_BOUNDARY reactivation
```

---

## 1. Master objective

The master objective is:

```txt
Advance Phygn autonomously from the current v5.7.3 state toward a Frontera C validation decision.
```

The terminal outcome must be exactly one of:

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
FRONTERA_C_BLOCKED_BY_NEGATIVE_CONTROLS
FRONTERA_C_BLOCKED_BY_C_STRUCTURE_ABLATION_FAILURE
FRONTERA_C_BLOCKED_BY_SCIENTIFIC_DEBT
FRONTERA_C_REQUIRES_NEW_EXPERIMENT
FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN
NO_CANDIDATE_WITH_REALITY_CONTACT
```

---

## 2. Important distinction

The goal is not:

```txt
Validate Frontera C no matter what.
```

The goal is:

```txt
Reach the first honest validation, blockage or falsification gate.
```

---

## 3. Core epistemic contract

```txt
A theory that cannot lose cannot win scientifically.
```

Therefore the AI must preserve all kill paths.

If evidence blocks Frontera C, the correct final result is a block.

If controls destroy a candidate, the correct result is a block.

If C-structure ablation fails, the correct result is a block.

If independent data never reaches benchmark readiness, the correct result is a block or new experiment requirement.

---

## 4. Current empirical asset

The project now has:

```txt
7 accepted y_true records
4 independent sources
visibility/decoherence domain
partial multi-source dataset
```

This is stronger than the previous single-source N=4 Hackermueller fixture.

But the threshold for multi-source benchmark remains:

```txt
total_accepted_ytrue_count >= 10
independent_source_count >= 2
```

Thus only 3 additional accepted y_true records are needed to open the first multi-source benchmark gate.

---

## 5. Master route

The autonomous route is:

```txt
v5.7.4  Targeted Human Figure/Table Review & Missing Source Completion
v5.8    Multi-Source Benchmark & Out-of-Source Control Gate
v5.9    Candidate Family Reprioritization Against Expanded Dataset
v6.0    Candidate Prediction Alignment & PredictiveGain Gate
v6.1    Negative Controls, Leakage and Simplicity Tests
v6.2    C-Structure Ablation Gate
v6.3    Scientific Debt and Claim Permission Gate
v6.4    Frontera C Validation Candidate Report or Terminal Block
```

The AI may execute these stages autonomously, but only if each gate permits the next.

---

## 6. Final discipline

```txt
The AI may run fast.
The gates must not.
```
