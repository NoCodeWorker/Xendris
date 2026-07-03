# Auxiliary Studies Map

Date: 2026-07-02

## Registry

### AUX_THERMAL_OPTICAL_001

```yaml
id: AUX_THERMAL_OPTICAL_001
name: Thermal-Optical Signal Degradation
classification: AUXILIARY
status: AUXILIARY_ONLY
current_state: FROZEN_UNTIL_CORE_RESTORED
may_validate_frontera_c_mayor: false
primary_variables:
  - heating_power_W
  - visibility
  - contrast
  - optical_degradation
  - laser_power_W
  - interference_contrast
related_artifacts:
  - docs/380_PHYGN_V5_9_2_COMMON_CONDITION_AXIS_RECOVERY_RESULTS.md
  - docs/381_PHYGN_V5_9_3_TARGETED_HEATING_POWER_AXIS_EXPANSION_RESULTS.md
  - phyng/candidates/common_axis_recovery.py
  - phyng/candidates/heating_power_axis_expansion.py
  - data/frontera_c/candidates/common_condition_axis_recovery_v5_9_2.json
  - data/frontera_c/candidates/heating_power_axis_expansion_v5_9_3.json
allowed_use:
  - analogy for information degradation
  - local model of recoverability loss
  - bridge candidate only after BRIDGE_AUX_THERMAL_TO_FRONTERA_C.md exists and is approved
forbidden_use:
  - validating Frontera C-Mayor
  - replacing c with heat
  - replacing causal observability with image visibility
  - driving the main roadmap
  - enabling PredictiveGain as a main validation claim
freeze_condition:
  - consumes more work than CORE documents
  - appears in next actions without bridge justification
  - produces application or sensor claims
```

## Bridge Requirement

Before expanding any thermal, optical, visibility, contrast, camera, sensor, or LiDAR branch, create:

```txt
BRIDGE_AUX_THERMAL_TO_FRONTERA_C.md
```

The bridge must state what core concept it illuminates, what it does not prove, why it is auxiliary, why it cannot validate Frontera C-Mayor, and stop criteria.

## Frozen Topics

- `heating_power_W` axis expansion
- visibility/contrast benchmark optimization
- thermal-optical datasets
- camera/sensor/LiDAR applications
- commercial applications

## Allowed Auxiliary Preservation

Existing artifacts may remain as archived auxiliary work. They may be referenced only with this status:

```yaml
classification: AUXILIARY
primary_goal_relevance: indirect
may_validate_main_hypothesis: false
```
