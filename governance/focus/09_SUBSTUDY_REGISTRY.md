# Auxiliary Substudy Registry

## Purpose

This registry prevents auxiliary studies from taking over the main project.

## Registry Rule

Every non-core study must be registered here before development.

## Current Registered Substudies

### Thermal-Optical Signal Degradation

```yaml
id: AUX_THERMAL_OPTICAL_001
classification: AUXILIARY
status: AUXILIARY_ONLY
core_relevance: indirect
may_validate_frontera_c_mayor: false
primary_variables:
  - heating_power_W
  - visibility
  - contrast
  - optical_degradation
allowed_use:
  - analogy for information degradation
  - local model of recoverability loss
  - bridge candidate only if explicitly connected to coherence/information
forbidden_use:
  - validating Frontera C-Mayor
  - replacing c with heat
  - replacing causal observability with image visibility
  - driving project roadmap
freeze_condition:
  - if it consumes more work than CORE documents
  - if it appears in next actions without bridge justification
```

## Required Bridge Before Expansion

Before expanding this substudy, create:

```text
BRIDGE_AUX_THERMAL_TO_FRONTERA_C.md
```

with:

```markdown
# Bridge: Thermal-Optical Degradation to Frontera C-Mayor

## What it models

## What it does not model

## Why it is auxiliary

## Which core concept it illuminates

## Why it cannot validate Frontera C-Mayor

## Promotion criteria from AUXILIARY to BRIDGE

## Stop criteria
```

## Substudy Expansion Gate

A substudy may expand only if:

```yaml
has_bridge_document: true
classification_reviewed: true
does_not_replace_core: true
next_action_mentions_core: true
```

## Substudy Freeze Rule

Freeze a substudy if:

- it becomes the main source of tasks,
- it generates application lists,
- it creates validation claims,
- it does not mention `c`,
- it does not connect to causal-informational membranes.

## Current Freeze Recommendation

```yaml
AUX_THERMAL_OPTICAL_001:
  recommended_state: FROZEN_UNTIL_CORE_RESTORED
  reason: Project drift occurred when this auxiliary study was treated as the main validation path.
```
