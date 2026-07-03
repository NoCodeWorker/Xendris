# Phygn — Evidence-Gated Self-Correction Loop

## 0. Purpose

This document defines the autonomous self-correction / vibe-coding loop for Phygn.

The loop allows an AI agent to improve the repository, tooling, data pipeline, tests, benchmark stack, model registry, control suite and ablation suite while pursuing the Frontera C validation decision.

But the loop is evidence-gated.

The AI may self-correct the software.

It may not self-authorize the science.

---

## 1. Core distinction

A standard vibe-coding loop checks whether code works.

Phygn requires two levels of correctness:

```txt
software correctness
scientific correctness
```

Software correctness asks:

```txt
Does it run?
Do tests pass?
Are artifacts valid?
Are schemas respected?
```

Scientific correctness asks:

```txt
Are sources real?
Are source objects hashed?
Are observables located?
Are y_true records accepted under QC?
Is benchmark readiness satisfied?
Is PredictiveGain permitted?
Did controls survive?
Did C-structure ablation survive?
Are claims allowed?
```

---

## 2. Master loop

The autonomous loop is:

```txt
while terminal_status not reached:

    current_state = read_latest_state()
    gate = select_active_gate(current_state)

    result = execute_gate(gate)

    if result.passed:
        advance_to_next_gate()
        continue

    blocker = classify_blocker(result)

    if blocker.requires_human_review:
        create_human_review_packet()
        stop_with(blocker)

    if blocker.requires_external_source:
        create_source_acquisition_or_download_packet()
        stop_with(blocker)

    if blocker.requires_new_experiment:
        create_minimal_experiment_design()
        stop_with(blocker)

    improvement = design_minimal_improvement(blocker)

    implement(improvement)

    add_or_update_tests(improvement)

    rerun_result = rerun_same_gate(gate)

    if rerun_result.passed:
        advance_to_next_gate()
        continue

    if repeated_blocker_count >= max_cycles_per_gate:
        stop_with(SELF_IMPROVEMENT_LOOP_EXHAUSTED, blocker)

    continue
```

---

## 3. Active gate order

The gate order is mandatory:

```txt
source identity
source availability
observable location
accepted y_true
dataset threshold
benchmark readiness
prediction alignment
PredictiveGain
negative controls
leakage tests
C-structure ablation
scientific debt review
claim permission
validation candidate report
```

No later gate may run before the previous gate passes.

---

## 4. Current start state

The loop starts from:

```txt
docs/356_PHYGN_V5_7_3_TARGETED_YTRUE_EXTRACTION_RESULTS.md
```

Current known state:

```txt
TARGETED_YTRUE_EXTRACTION_PARTIAL
total_accepted_ytrue_count = 7
independent_source_count = 4
benchmark_readiness = PARTIAL_MULTI_SOURCE_N_SMALL
```

Current immediate blocker:

```txt
MISSING_EXPERIMENTAL_DATA
MISSING_BENCHMARK
```

Current immediate task:

```txt
reach total_accepted_ytrue_count >= 10
```

Needed:

```txt
3 additional accepted y_true
```

---

## 5. Allowed self-improvement actions

The AI may improve:

```txt
source acquisition pipeline
source download and hashing pipeline
PDF parsing and figure/table review tools
observable-location scanner
y_true extraction/QC pipeline
unit normalization
deduplication
dataset quality checks
benchmarking stack
baseline models
negative controls
cross-validation
leakage detection
C-structure ablation suite
claim permission logic
test coverage
schema validation
reports
```

Only when the improvement directly targets the current blocker.

---

## 6. Forbidden self-improvement actions

The AI must not perform:

```txt
architecture-only refactors
new governance phases with no blocker removal
aesthetic cleanup unrelated to evidence
new candidate creation before dataset permission
PredictiveGain before benchmark readiness
C-structure ablation before PredictiveGain and controls
validation report before claim permission
deep learning before dataset size justifies it
```

---

## 7. Bounded cycles

The loop is bounded:

```txt
max_self_improvement_cycles_per_gate = 3
```

If the same blocker persists after three cycles:

```txt
SELF_IMPROVEMENT_LOOP_EXHAUSTED
```

The system must emit:

```txt
exact_blocker
last_attempted_improvement
artifacts_created
tests_added
why blocker persists
recommended human action or experiment design
```

---

## 8. Final principle

```txt
Self-correction may remove blockers.
It may not create permission.
```
