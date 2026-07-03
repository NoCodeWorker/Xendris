# Project Status Schema — Frontera C

## Purpose

This schema prevents Codex from mixing different kinds of progress.

## Required Status File

Codex must maintain:

```text
docs/status/PROJECT_STATUS.md
```

using the schema below.

## Schema

```yaml
project_name: Frontera C
primary_hypothesis: c_as_causal_informational_membrane

frontera_c_mayor:
  status: NOT_VALIDATED
  conceptual_definition_status: DRAFT / STABLE / AMBIGUOUS / NEEDS_REVISION
  mathematical_form_status: NONE / SKETCH / PARTIAL / FORMAL
  known_physics_alignment_status: NONE / PARTIAL / STRONG / CONFLICTING
  novelty_status: UNDEFINED / PARTIAL / DIFFERENTIATED / NOT_NOVEL
  falsifiability_status: NONE / PARTIAL / CLEAR
  validation_status: NOT_VALIDATED / PARTIAL_SUPPORT / VALIDATED / FALSIFIED

bridge_layer:
  information_theory_status:
  decoherence_status:
  observer_measurement_status:
  horizon_connection_status:
  recoverability_status:

auxiliary_studies:
  thermal_optical:
    status: AUXILIARY_ONLY
    may_validate_main_hypothesis: false
    current_state:
    last_result:
  other_auxiliary:
    status:

artifact_counts:
  core:
  bridge:
  auxiliary:
  off_track:

drift_control:
  last_audit:
  drift_detected:
  main_drift_risk:
  frozen_branches:
  required_recenter_action:

next_action:
  priority:
  classification:
  reason:
```

## Validation State Rules

### NOT_VALIDATED

Default state.

Use unless a clear validation criterion is met.

### PARTIAL_SUPPORT

Allowed only if:

1. the claim is directly linked to Frontera C-Mayor,
2. the relation to known physics is explicit,
3. the result is not merely auxiliary,
4. the support is reproducible or logically formalized.

### VALIDATED

Do not use unless:

1. there is a precise mathematical formulation,
2. there is a differentiated claim beyond existing physics,
3. the claim is falsifiable,
4. evidence supports it,
5. alternative explanations have been addressed.

### FALSIFIED

Use if the central claim is shown to be inconsistent, redundant, or experimentally contradicted.

## Auxiliary Progress Rule

Progress in:

- thermal optics,
- visibility,
- contrast,
- image degradation,
- sensors,
- camera models,

does not change:

```yaml
frontera_c_mayor.validation_status
```

unless a formal bridge document is produced and approved.
