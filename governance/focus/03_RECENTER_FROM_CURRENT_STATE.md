# Recenter From Current State

## Purpose

This prompt is designed to be run immediately from the current project state, after the project has drifted toward thermal-optical benchmarking.

## Current Problem

The project has partially drifted from:

```text
Frontera C-Mayor:
c as causal-informational membrane
```

toward:

```text
AUXILIARY thermal-optical study:
heating_power_W → visibility/contrast
```

This drift must be corrected without deleting useful work.

## Immediate Instruction to Codex

Stop continuing the thermal/visibility benchmark as the main path.

Do not discard it.

Reclassify it as:

```yaml
THERMAL_OPTICAL_STUDY:
  classification: AUXILIARY
  status: AUXILIARY_ONLY
  may_validate_frontera_c_mayor: false
  permitted_use: analogy_or_local_model_of_information_degradation
```

## Required Recenter Actions

Perform these actions in order:

1. Read the current project structure.
2. Identify all existing artifacts.
3. Classify them as CORE, BRIDGE, AUXILIARY, or OFF-TRACK.
4. Create or update `docs/frontera_c/FRONTERA_C_MAYOR.md`.
5. Create or update `docs/status/PROJECT_STATUS.md`.
6. Create `docs/audits/AUXILIARY_STUDIES_MAP.md`.
7. Move or mark thermal/contrast work as auxiliary.
8. Do not optimize auxiliary code.
9. Do not add new thermal/visibility applications.
10. Return a recentering report.

## Required Output

Produce:

```markdown
# Recenter Report

## FOCUS CHECK

- Current objective:
- Classification:
- Drift corrected:
- Main hypothesis restored:

## 1. What drift occurred

## 2. What has been reclassified

## 3. What remains useful

## 4. What must not be treated as validation

## 5. New project hierarchy

## 6. Files created or updated

## 7. Current status

## 8. Next action
```

## Explicit Prohibition

Do not continue with:

- camera applications,
- thermal camera examples,
- LiDAR applications,
- visibility datasets,
- contrast restoration,
- optical benchmark optimization,
- commercial sensor applications.

Unless explicitly ordered later, these are frozen as auxiliary.

## Primary Recovery Target

Restore this sentence as the active project center:

> **Frontera C-Mayor investigates whether `c` can be modeled as a causal-informational membrane separating domains of physical reality by their ability to exchange coherent, causal, measurable information with an observer.**
