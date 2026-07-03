# Phygn — Validate-If-Possible Loop Runtime

## 0. Purpose

This document specifies the runtime loop that tries to validate Frontera C while preserving all kill paths.

---

## 1. Runtime pseudocode

```python
while True:
    state = read_latest_state()
    gate = select_next_required_gate(state)

    result = run_gate(gate)

    if result.passed:
        if gate.name == "claim_permission" and result.validation_candidate_ready:
            emit("FRONTERA_C_VALIDATION_CANDIDATE_READY")
            break
        continue

    blocker = classify_blocker(result)
    capability = classify_missing_capability(blocker)

    if blocker.requires_human_review:
        create_human_review_packet(blocker)
        emit("HUMAN_REVIEW_REQUIRED")
        break

    if blocker.requires_external_source:
        create_external_source_packet(blocker)
        emit("EXTERNAL_SOURCE_REQUIRED")
        break

    if blocker.requires_new_experiment:
        design_minimal_experiment(blocker)
        emit("FRONTERA_C_REQUIRES_NEW_EXPERIMENT")
        break

    if blocker.is_falsification:
        emit("FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN")
        break

    for cycle in range(max_cycles_per_gate):
        improvement = design_minimal_self_provisioning(capability, blocker)
        implement(improvement)
        add_tests(improvement)
        test_result = run_tests()

        if not test_result.passed:
            continue

        retry = rerun_gate(gate)

        if retry.passed:
            break

        blocker = classify_blocker(retry)
        capability = classify_missing_capability(blocker)

    else:
        emit("SELF_PROVISIONING_LOOP_EXHAUSTED")
        break
```

---

## 2. Non-terminal blockers

These blockers are not terminal until a self-provisioning loop has been attempted:

```txt
MODEL_BLOCKER
BENCHMARK_BLOCKER
CONTROL_BLOCKER
LEAKAGE_BLOCKER
ABLATION_BLOCKER
TEST_BLOCKER
TOOLING_BLOCKER
KNOWLEDGE_BLOCKER
CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES
CANDIDATE_SELECTION_REQUIRES_THEORY_REFORMULATION
```

---

## 3. Potentially terminal blockers

These may be terminal if evidence cannot be produced internally:

```txt
SOURCE_AVAILABILITY_BLOCKER
HUMAN_REVIEW_BLOCKER
EXTERNAL_SOURCE_BLOCKER
EXPERIMENT_REQUIRED_BLOCKER
SCIENTIFIC_DEBT_BLOCKER
```

But even these require a clear packet:

```txt
human review packet
source acquisition packet
experiment design
debt map
```

---

## 4. Candidate-specific override

The following status is forbidden as an immediate stop:

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT
```

It may only be emitted as:

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT_AFTER_CONSTRUCTION_LOOP
```

after:

```txt
candidate construction attempted
feature schema inspected
prediction rules attempted
leakage screen run
baseline comparator attempted
control plan attempted
C-ablation plan attempted
self-provisioning cycles exhausted
```

---

## 5. Final principle

```txt
Do not stop because a scientific object is missing.
Attempt to construct it.
Stop only if construction fails under the rails.
```
