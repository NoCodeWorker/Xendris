# Phygn v5.9 — Reporting & Next Gate

## 0. Purpose

This document defines reports and next-gate decision for candidate family selection.

---

## 1. Required reports

Generate:

```txt
reports/frontera_c/candidates/candidate_family_registry_v5_9.md
reports/frontera_c/candidates/candidate_feature_schema_v5_9.md
reports/frontera_c/candidates/candidate_prediction_rules_v5_9.md
reports/frontera_c/candidates/candidate_reality_contact_screen_v5_9.md
reports/frontera_c/candidates/candidate_leakage_screen_v5_9.md
reports/frontera_c/candidates/candidate_selection_decision_v5_9.md
reports/campaigns/FRONTERA-C-REALITY-CONTACT-CANDIDATE-FAMILY-CONSTRUCTION-v5_9.md
```

---

## 2. Final result document

Create:

```txt
docs/374_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_RESULTS.md
```

Note:

```txt
Spec pack occupies 369-373.
Campaign result should occupy 374.
```

---

## 3. Final statuses

Emit exactly one:

```txt
CANDIDATE_FAMILY_SELECTED_FOR_PREDICTIVE_GATE
NO_CANDIDATE_WITH_REALITY_CONTACT
CANDIDATE_SELECTION_REQUIRES_THEORY_REFORMULATION
CANDIDATE_SELECTION_REQUIRES_NEW_OBSERVABLES
CANDIDATE_SELECTION_REQUIRES_NEW_EXPERIMENT
CANDIDATE_SELECTION_BLOCKED_BY_LEAKAGE
CANDIDATE_SELECTION_BLOCKED_BY_MISSING_FEATURES
CANDIDATE_SELECTION_BLOCKED_BY_SCIENTIFIC_DEBT
```

---

## 4. Gate rules

If:

```txt
passed_candidate_count >= 1
selected_candidate_family is not None
selected_rule_id is not None
```

then permit:

```txt
v6.0 — Candidate Prediction Alignment & PredictiveGain Gate
```

If no candidate passes:

```txt
allowed_next_phase = None
```

and emit exact blocker.

---

## 5. Blocked claims

Always blocked:

```txt
Frontera C is validated
candidate has PredictiveGain
candidate has physical support
candidate selection equals validation
LOG_BOUNDARY is reactivated
invariant confirmation
```

---

## 6. Allowed claims

Allowed if true:

```txt
candidate family registry was created
candidate feature schema was created
candidate prediction rules were screened
candidate leakage screen was run
one candidate was selected for predictive gate
or no candidate has reality contact
```

---

## 7. Final principle

```txt
Selection is permission to test.
Nothing more.
```
