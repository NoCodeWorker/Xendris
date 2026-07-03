# Review Response Classifier — Frontera C-Mayor

## Purpose

Classify external reviewer feedback and map it to conservative project-state updates.

Current baseline:

```yaml
accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
validation_status: NOT_VALIDATED
novelty_status: UNRESOLVED
redundancy_risk: MEDIUM_HIGH
core_theory_candidate: false
bridge_framework: true
partial_support: false
```

No reviewer response may directly create validation or partial support. Reviewer feedback can only change classification and next required work.

## 1. Classification Categories

```txt
REDUNDANT_WITH_KNOWN_PHYSICS
USEFUL_BRIDGE_FRAMEWORK
FORMAL_THEOREM_CANDIDATE
NEEDS_MAJOR_REWRITE
CONCEPTUAL_ERROR
REVIEWER_REQUESTS_CLARIFICATION
```

## 2. `REDUNDANT_WITH_KNOWN_PHYSICS`

Use when the reviewer says the framework adds no formal value beyond known causal structure, measurement theory, information theory, decoherence, or recoverability.

Project status update:

```yaml
frontera_c_mayor:
  accepted_status: REDUNDANT_WITH_KNOWN_PHYSICS
  novelty_status: REJECTED_AS_NON_NOVEL
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: false
  partial_support: false
  redundancy_risk: MAXIMAL
next_action:
  priority: close_or_rewrite_core_hypothesis
  classification: CORE_GOVERNANCE
```

Allowed claim:

```txt
External review judged the current framework redundant with known physics.
```

Forbidden claim:

```txt
The framework was validated or falsified empirically.
```

## 3. `USEFUL_BRIDGE_FRAMEWORK`

Use when the reviewer says the framework is useful for organization or pedagogy but not novel theory.

Project status update:

```yaml
frontera_c_mayor:
  accepted_status: BRIDGE_FORMAL_FRAMEWORK_CREATED
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: true
  partial_support: false
  redundancy_risk: MEDIUM_HIGH
next_action:
  priority: refine_bridge_or_prepare_interpretive_frame_decision
  classification: CORE_BRIDGE
```

Allowed claim:

```txt
External review supports retaining the framework as bridge formalism.
```

## 4. `FORMAL_THEOREM_CANDIDATE`

Use when the reviewer identifies a plausible non-redundant theorem path.

Project status update:

```yaml
frontera_c_mayor:
  accepted_status: CORE_THEORY_CANDIDATE
  novelty_status: POTENTIALLY_DIFFERENTIATED
  validation_status: NOT_VALIDATED
  core_theory_candidate: true
  bridge_framework: true
  partial_support: false
  redundancy_risk: MEDIUM
next_action:
  priority: write_formal_theorem_candidate_and_failure_conditions
  classification: CORE
```

Allowed claim:

```txt
External review identified a possible theorem path.
```

Forbidden claim:

```txt
The theorem is proven, validated, or physically confirmed.
```

## 5. `NEEDS_MAJOR_REWRITE`

Use when the reviewer says the framework is not ready for formal judgment because definitions, scope, or terms are unclear.

Project status update:

```yaml
frontera_c_mayor:
  accepted_status: REWRITE_REQUIRED
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: provisional
  partial_support: false
  redundancy_risk: HIGH
next_action:
  priority: rewrite_definitions_before_any_theorem_or_benchmark
  classification: CORE
```

## 6. `CONCEPTUAL_ERROR`

Use when the reviewer identifies a conflict with established physics, category error, circularity, or misleading premise.

Project status update:

```yaml
frontera_c_mayor:
  accepted_status: CONCEPTUAL_ERROR_REVIEW_REQUIRED
  novelty_status: BLOCKED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: false
  partial_support: false
  redundancy_risk: CRITICAL
next_action:
  priority: resolve_conceptual_error_or_archive_framework
  classification: CORE_GOVERNANCE
```

Allowed claim:

```txt
External review identified a conceptual blocker requiring resolution.
```

## 7. `REVIEWER_REQUESTS_CLARIFICATION`

Use when the reviewer cannot classify the framework without more definitions, examples, or constraints.

Project status update:

```yaml
frontera_c_mayor:
  accepted_status: CLARIFICATION_REQUIRED
  novelty_status: UNRESOLVED
  validation_status: NOT_VALIDATED
  core_theory_candidate: false
  bridge_framework: true
  partial_support: false
  redundancy_risk: MEDIUM_HIGH
next_action:
  priority: answer_reviewer_clarifications_without_expanding_claims
  classification: CORE_BRIDGE
```

## 8. Reviewer Feedback Intake Template

```yaml
reviewer_role:
review_date:
raw_decision:
classifier_category:
main_critique:
non_redundant_path_identified:
redundancy_or_error_identified:
requested_clarifications:
status_update:
claims_allowed_after_review:
claims_forbidden_after_review:
```

## 9. Hard Boundary

Regardless of classifier category:

```yaml
validation_status: NOT_VALIDATED
partial_support: false
no_predictive_gain: true
no_auxiliary_validation: true
no_application_claims: true
```
