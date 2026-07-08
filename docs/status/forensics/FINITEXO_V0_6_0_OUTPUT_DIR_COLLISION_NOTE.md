# Forensic Note — v0.6.0 Canonical Output Directory Collision

## Summary

The canonical v0.6.0 output directory at `runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30/` already contains a tracked blocked-preflight artifact set from an earlier execution attempt. This directory is historical evidence and must not be overwritten or deleted.

## Git Hygiene Incident

A manual move temporarily renamed this directory to:

```
runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30_blocked_preflight_20260708_1117/
```

This caused git to report:
- 9 deleted tracked files under the original path
- 1 untracked renamed directory

The directory was restored to its original path to preserve historical evidence and git hygiene.

## Root Cause

The v0.6.0 runner previously used a fixed output directory with no mechanism to select an alternative path. A live execution would overwrite or mutate the historical blocked-preflight evidence.

## Prevention Mechanism

A new environment variable `FINITEXO_CONTROLLED_RUN_ID_SUFFIX` has been added to the v0.6.0 controlled-run configuration.

When set, this suffix is appended to both `run_id` and `output_dir`, creating a unique output path for each execution.

### Example

```bash
set FINITEXO_CONTROLLED_RUN_ID_SUFFIX=live_20260708_01
```

This produces:
- `run_id`: `finitexo_v0_6_0_real_provider_controlled_run_n30_live_20260708_01`
- `output_dir`: `runs/finitexo_code_matrix_v0_6_0_real_provider_controlled_run_n30_live_20260708_01/`

### Validation

Suffixes are restricted to letters, numbers, underscores, and hyphens. Characters such as `/`, `\`, `.`, ` ` (whitespace), and `..` are rejected with a clear error.

### Preflight Safety

If the effective output directory exists and is non-empty, the preflight gate blocks execution unless `allow_overwrite` is explicitly set to `true`. The default is `false`.

## Status

- v0.6.0 live execution has not been performed.
- The canonical blocked-preflight directory remains intact and tracked.
- No provider calls were made during this fix.
- No provider superiority, Xendris superiority, statistical superiority, production readiness, or universal benchmark claim is authorized.
