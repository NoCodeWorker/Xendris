# Phygn v4.6 — Candidate Freeze Review & Pivot Decision Goal

## 0. Context

The latest confirmed result document is:

```txt
docs/297_PHYGN_V4_5_EXTERNAL_EVIDENCE_RESULTS.md
```

Therefore, v4.6 starts at:

```txt
298
```

v4.5 produced:

```txt
PHI_GRADIENT_EMPIRICALLY_UNGROUNDED_FREEZE
freeze_status = FROZEN_NO_YTRUE_AVAILABLE
accepted_y_true_count = 0
PredictiveGain = UNDEFINED_INSUFFICIENT_YTRUE
SLOT_4 debt = OPEN_BLOCKING_FOR_GRADIENT_CLAIMS
```

v4.5 attempted:

```txt
TRACK_A_TABLE_REVIEW
TRACK_B_SUPPLEMENTARY_SEARCH
TRACK_C_PUBLIC_DATASET_SEARCH
```

and found:

```txt
no accepted y_true
no supplementary files
no public datasets
no exact page/table/figure locations sufficient for observed numeric truth
```

v4.6 must make a formal candidate decision.

---

## 1. Core thesis

```txt
Freezing a candidate is progress when the alternative is fiction.
```

---

## 2. Hard rule

```txt
No y_true available after external sprint means no more predictive pipeline for this candidate.
```

This means:

```txt
No PredictiveGain phase.
No new benchmark-only scoring.
No new internal governance to keep PHI_GRADIENT alive.
No physical claim upgrade.
No gradient-mechanism claim.
```

---

## 3. Mission

Implement:

```txt
v4.6 — Candidate Freeze Review & Pivot Decision
```

The decision must choose one of:

```txt
FREEZE_AND_ARCHIVE_PHI_GRADIENT
REDEFINE_AS_METHOD_ONLY
REQUIRES_NEW_EXPERIMENT
PIVOT_TO_NEXT_CANDIDATE_FAMILY
```

---

## 4. Candidate decision definitions

### FREEZE_AND_ARCHIVE_PHI_GRADIENT

Use when:

```txt
PHI_GRADIENT has no y_true access
no clear experiment path
no clear source acquisition path
and continued work would be internal recursion
```

### REDEFINE_AS_METHOD_ONLY

Use when:

```txt
PHI_GRADIENT remains useful as a methodological stress-test,
negative control, benchmark-shaping function, or heuristic,
but cannot be claimed as physical model
```

### REQUIRES_NEW_EXPERIMENT

Use when:

```txt
PHI_GRADIENT remains scientifically interesting,
but observable truth requires new experimental design
```

### PIVOT_TO_NEXT_CANDIDATE_FAMILY

Use when:

```txt
another candidate family has better y_true accessibility,
source-location availability,
or experimental observability
```

---

## 5. Inputs

Load:

```txt
data/external_evidence/phi_gradient_candidate_freeze_decision_v4_5.json
data/y_true/phi_gradient_v4_5_next_predictive_gain_inputs.json
data/y_true/phi_gradient_assembled_y_true_dataset_v4_5.json
data/external_evidence/phi_gradient_table_review_results_v4_5.json
data/external_evidence/phi_gradient_supplementary_search_results_v4_5.json
data/external_evidence/phi_gradient_public_dataset_search_results_v4_5.json
data/external_evidence/phi_gradient_external_y_true_accepted_v4_5.json
data/external_evidence/phi_gradient_external_y_true_rejected_v4_5.json
data/external_evidence/phi_gradient_external_evidence_audit_trail_v4_5.json
data/model_comparison/phi_gradient_benchmark_comparison_scores_v4_1.json
data/debts/DEBT-SLOT4-GRADIENT-COMPONENT-GAP_v4_0.json
data/audits/remediation/phygn_v4_4_2_continuation_gate.json
```

Optionally load historical candidate-family artifacts:

```txt
data/closed_loop/
data/synthetic_benchmark_design/
data/source_pressure/
data/benchmarks/
```

If v4.5 freeze decision is missing:

```txt
PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION
```

---

## 6. Outputs

Create:

```txt
data/candidate_decisions/phi_gradient_freeze_review_v4_6.json
data/candidate_decisions/phi_gradient_final_claim_permissions_v4_6.json
data/candidate_decisions/phi_gradient_method_only_redefinition_v4_6.json
data/candidate_decisions/phi_gradient_experiment_requirement_v4_6.json
data/candidate_decisions/next_candidate_family_selection_matrix_v4_6.json
data/candidate_decisions/phygn_v4_6_pivot_decision_v4_6.json
```

---

## 7. Statuses

```txt
PHI_GRADIENT_FREEZE_REVIEW_COMPLETED
PHI_GRADIENT_FREEZE_REVIEW_BLOCKED_MISSING_FREEZE_DECISION
PHI_GRADIENT_ARCHIVED_EMPIRICALLY_UNGROUNDED
PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY
PHI_GRADIENT_REQUIRES_NEW_EXPERIMENT
PHI_GRADIENT_PIVOT_TO_NEXT_CANDIDATE
```

Expected conservative final status:

```txt
PHI_GRADIENT_REDEFINED_AS_METHOD_ONLY
```

or:

```txt
PHI_GRADIENT_PIVOT_TO_NEXT_CANDIDATE
```

unless explicit experiment design is chosen.

---

## 8. Acceptance criteria

v4.6 is complete when:

```txt
v4.5 freeze decision loaded
candidate freeze review generated
final claim permissions generated
method-only redefinition generated if applicable
experiment requirement generated if applicable
next candidate selection matrix generated
pivot decision generated
reports generated
tests pass
PHI_GRADIENT remains blocked for PredictiveGain
PHI_GRADIENT remains blocked for physical claims
SLOT_4 debt remains open unless explicitly archived as irrelevant to active pipeline
```

---

## 9. Final principle

```txt
A frozen candidate is not dead knowledge.
It is protected knowledge.
```
