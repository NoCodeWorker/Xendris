# Periodic Audit Triggers — Codex Governance

## Purpose

This file defines automatic conceptual checkpoints for Codex.

Codex must not run indefinitely without rechecking focus.

## Trigger Group A — Artifact Count

Run `04_ARTIFACT_AUDIT_PROTOCOL.md` when:

```yaml
generated_artifacts_since_last_audit >= 3
```

An artifact includes:

- `.md`,
- `.py`,
- `.json`,
- `.ipynb`,
- `.txt`,
- `.csv`,
- `.yaml`,
- generated report,
- benchmark output.

## Trigger Group B — Time-Based

Run an audit when:

```yaml
autonomous_work_time_minutes >= 30
```

If time measurement is unavailable, approximate by major action count.

## Trigger Group C — Topic Drift Keywords

Run an immediate focus check whenever any of these terms appear:

```yaml
drift_keywords:
  - heating_power_W
  - visibility
  - contrast
  - thermal
  - heat
  - camera
  - LiDAR
  - sensor
  - image restoration
  - optical turbulence
  - benchmark readiness
  - PredictiveGain
```

These terms are not forbidden, but they trigger classification.

Default classification:

```yaml
default_classification_for_drift_keywords: AUXILIARY
```

## Trigger Group D — Validation Claims

Run an audit before any statement like:

- "validated",
- "partially validated",
- "significant progress",
- "ready",
- "unblocked",
- "benchmark passed",
- "predictive gain computed",
- "frontier validated",
- "Frontera C advanced".

## Trigger Group E — State Changes

Run an audit when any status changes:

```yaml
state_change_keywords:
  - NOT_VALIDATED
  - HUMAN_REVIEW_REQUIRED
  - READY
  - BLOCKED
  - UNBLOCKED
  - VALIDATED
  - DEPRECATED
  - AUXILIARY_ONLY
```

## Trigger Group F — New Branch Creation

Run an audit before creating a new research branch:

```yaml
branch_types:
  - experimental
  - benchmark
  - optical
  - thermal
  - information
  - decoherence
  - relativity
  - mathematical
```

## Trigger Group G — Before Next Step Recommendation

Before recommending any next step, Codex must answer:

```markdown
## NEXT STEP FOCUS TEST

- Does this next step strengthen CORE?
- Does it only strengthen AUXILIARY?
- Is a BRIDGE document required first?
- Could this next step cause drift?
```

## Hard Rule

If a trigger fires, Codex must not continue ordinary work until it has completed at least a short audit.

## Short Audit Format

```markdown
## SHORT FOCUS AUDIT

- Trigger:
- Current work:
- Classification:
- Connection to Frontera C-Mayor:
- Drift risk:
- Continue / Recenter / Freeze:
```

## Long Audit Requirement

After three short audits, run the full artifact audit.
