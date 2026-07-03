# Phygn Autonomous Validation Loop — Goal

## 0. Purpose

This package upgrades the Frontera C master Goal into a true autonomous validation loop.

The agent must not simply stop when the next capability is missing.

It must attempt to create the missing capability under the scientific rails, then retry the gate.

---

## 1. Core idea

The current human/AI workflow is:

```txt
Codex runs a gate.
Codex stops at blocker.
Human reports result to ChatGPT.
ChatGPT diagnoses blocker.
ChatGPT writes next protocol/prompt.
Human gives prompt to Codex.
Codex retries.
```

This package internalizes that loop inside Codex:

```txt
Gate fails.
Agent diagnoses blocker.
Agent identifies missing capability.
Agent provisions tool/knowledge/protocol/test/data pathway.
Agent retries the gate.
Agent continues or stops honestly.
```

---

## 2. Master instruction

```txt
Validate Frontera C if and only if the scientific architecture permits it.

Do not stop at a removable blocker.

If a blocker appears, identify the missing capability, build or acquire that capability under the rails, add tests, rerun the gate, and continue.

Stop only if the blocker is non-removable, requires human review, requires external evidence, requires a new experiment, is exhausted after bounded retries, or falsifies the current-domain candidate.
```

---

## 3. Core rule

```txt
Do not stop because the next capability is missing.
Build the capability under the rails, then retry the gate.
```

---

## 4. Current project state

Current benchmark state after the master run:

```txt
accepted_ytrue_count = 10
independent_source_count = 5
benchmark_readiness = READY_FOR_MULTI_SOURCE_BENCHMARK
first_failed_gate = candidate_family_selection
blocker_type = MODEL_BLOCKER
terminal_status = NO_CANDIDATE_WITH_REALITY_CONTACT
```

However:

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT
```

must not be considered terminal until candidate-construction capability has been attempted under v5.9 or equivalent.

---

## 5. Immediate implication

The agent must attempt:

```txt
candidate family construction
candidate feature schema derivation
leakage screen
prediction rule formalization
baseline comparator definition
control plan definition
C-structure ablation plan definition
```

before emitting:

```txt
NO_CANDIDATE_WITH_REALITY_CONTACT
```

---

## 6. Terminal statuses

The autonomous loop may stop only with one of:

```txt
FRONTERA_C_VALIDATION_CANDIDATE_READY
FRONTERA_C_BLOCKED_BY_INSUFFICIENT_DATA
FRONTERA_C_BLOCKED_BY_BENCHMARK_FAILURE
FRONTERA_C_BLOCKED_NO_PREDICTIVE_GAIN
FRONTERA_C_BLOCKED_BY_NEGATIVE_CONTROLS
FRONTERA_C_BLOCKED_BY_C_STRUCTURE_ABLATION_FAILURE
FRONTERA_C_BLOCKED_BY_SCIENTIFIC_DEBT
FRONTERA_C_REQUIRES_NEW_EXPERIMENT
FRONTERA_C_FALSIFIED_IN_CURRENT_DOMAIN
NO_CANDIDATE_WITH_REALITY_CONTACT_AFTER_CONSTRUCTION_LOOP
SELF_PROVISIONING_LOOP_EXHAUSTED
HUMAN_REVIEW_REQUIRED
EXTERNAL_SOURCE_REQUIRED
```

---

## 7. Final principle

```txt
The agent may build tools.
The agent may learn from local knowledge.
The agent may formalize missing candidate rules.
But the agent may not grant itself scientific permission.
```
