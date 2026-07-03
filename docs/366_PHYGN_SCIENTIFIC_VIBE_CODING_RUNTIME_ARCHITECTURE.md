# Phygn — Scientific Vibe Coding Runtime Architecture

## 0. Purpose

This document describes the runtime architecture for an autonomous AI coding agent pursuing Frontera C validation under scientific gates.

---

## 1. Runtime components

The autonomous agent should maintain these components:

```txt
State Reader
Gate Selector
Gate Executor
Blocker Classifier
Improvement Planner
Implementation Agent
Test Runner
Artifact Validator
Scientific Permission Checker
Decision Reporter
```

---

## 2. State Reader

Responsibilities:

```txt
find latest result document
load JSON artifacts
load gate decision files
summarize current counts
detect allowed next phase
detect blocked claims
```

Must output:

```txt
current_status
latest_doc
accepted_ytrue_count
independent_source_count
benchmark_readiness
candidate_statuses
current_blockers
allowed_next_phase
```

---

## 3. Gate Selector

Selects next gate from the mandatory order:

```txt
dataset expansion
benchmark readiness
candidate selection
prediction alignment
PredictiveGain
negative controls
leakage tests
C-structure ablation
scientific debt
claim permission
validation report
```

The selector must not skip gates.

---

## 4. Gate Executor

Executes the active gate and emits:

```txt
passed
failed
partial
blocker
artifacts
reports
tests
```

---

## 5. Blocker Classifier

Classifies failure using taxonomy from:

```txt
365_PHYGN_BLOCKER_TAXONOMY_AND_MINIMAL_IMPROVEMENT_PROTOCOL.md
```

---

## 6. Improvement Planner

Creates exactly one bounded improvement plan.

Schema:

```python
class ImprovementPlan(BaseModel):
    blocker_id: str
    blocker_type: str
    target_gate: str
    minimal_improvement: str
    expected_artifacts: list[str]
    tests_to_add: list[str]
    forbidden_actions: list[str]
    stop_condition: str
```

---

## 7. Implementation Agent

Allowed to edit code and docs only within the scope of the improvement plan.

Forbidden:

```txt
broad refactors
renaming historical artifacts
deleting evidence
overwriting accepted y_true
reactivating archived candidates
```

---

## 8. Test Runner

Must run:

```txt
unit tests
campaign tests
schema validation
artifact presence checks
forbidden artifact checks
blocked claim checks
```

---

## 9. Artifact Validator

Validates:

```txt
JSON validity
schema conformance
hash/path consistency
deduplication
numeric/unit integrity
gate decision consistency
```

---

## 10. Scientific Permission Checker

Checks whether the next scientific claim is allowed.

For example:

```txt
y_true permission
benchmark permission
PredictiveGain permission
control survival permission
C-ablation permission
validation candidate permission
```

If not allowed, it must block.

---

## 11. Decision Reporter

At every stop, create a result document with:

```txt
final_status
last_completed_gate
first_failed_gate
blocker_type
artifacts_created
tests_run
allowed_next_phase
blocked_claims
allowed_claims
next human action if any
```

---

## 12. Recommended libraries

Use:

```txt
pandas
numpy
scikit-learn
scipy
pydantic
pytest
matplotlib
pymupdf
pdfplumber
pypdf
```

Do not use deep learning unless:

```txt
dataset size is large enough
simple baselines are exhausted
out-of-source validation exists
controls survive
```

---

## 13. Final principle

```txt
A passing CI pipeline is not a passing scientific gate.
```
