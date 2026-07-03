# Artifact Audit Protocol — Frontera C

## Purpose

Codex must periodically audit generated work to prevent conceptual drift.

This protocol separates useful work from drift.

## Audit Trigger

Run this protocol:

- after every 3 generated artifacts,
- after every major benchmark result,
- after any state change,
- after any claim of progress,
- after any new subdirectory is created,
- after 30 minutes of autonomous work,
- before declaring a milestone,
- before computing any validation score,
- before moving to a new research branch,
- whenever `heating_power_W`, visibility, contrast, cameras, or sensors appear.

## Audit Inputs

Codex must inspect:

- documentation files,
- source files,
- generated reports,
- benchmarks,
- JSON results,
- notebooks,
- scripts,
- status files,
- README files,
- logs,
- planning files.

## Classification

Every artifact must be classified:

```yaml
classification:
  allowed_values:
    - CORE
    - BRIDGE
    - AUXILIARY
    - OFF_TRACK
```

## Classification Rules

### CORE

An artifact is CORE only if it directly addresses Frontera C-Mayor.

Required connection to at least one:

- `c`,
- relativistic causality,
- light cones,
- horizons,
- causal accessibility,
- information transfer constrained by `c`,
- observer-dependent physical access,
- causal-informational membrane.

### BRIDGE

An artifact is BRIDGE if it connects CORE concepts to:

- information theory,
- decoherence,
- coherence loss,
- measurement,
- entropy,
- recoverability,
- inference from inaccessible domains.

### AUXILIARY

An artifact is AUXILIARY if it concerns:

- signal degradation,
- thermal models,
- visibility,
- contrast,
- optical turbulence,
- image restoration,
- benchmarks unrelated to `c`,
- local experiments,
- cameras,
- LiDAR,
- sensors.

### OFF_TRACK

An artifact is OFF_TRACK if it does not help the primary hypothesis or an explicitly approved bridge.

## Required Artifact Table

Generate a table:

| Artifact | Path | Classification | Reason | Keep/Move/Archive | Required Action |
|---|---|---|---|---|---|

## Required Warnings

If any AUXILIARY artifact is being treated as CORE, emit:

```text
CONTRACT WARNING: AUXILIARY PROMOTED TO CORE WITHOUT BRIDGE
```

If any OFF_TRACK artifact is expanding, emit:

```text
DRIFT WARNING: OFF-TRACK WORK EXPANDING
```

## Required Summary

At the end, include:

```yaml
audit_summary:
  core_count:
  bridge_count:
  auxiliary_count:
  off_track_count:
  drift_detected:
  main_risk:
  immediate_recenter_action:
```

## Required Files

After audit, update:

- `docs/audits/ARTIFACT_AUDIT.md`
- `docs/status/PROJECT_STATUS.md`
- `docs/audits/AUXILIARY_STUDIES_MAP.md`
- `docs/audits/DRIFT_LOG.md`

## Audit Completion Rule

The audit is incomplete unless it states clearly:

```text
Frontera C-Mayor validation status remains separate from all auxiliary progress.
```
