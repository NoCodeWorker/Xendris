# Forensic Note — Finitexo v0.5.4 Artifact Drift

## Inspection

- **Date**: 2026-07-08
- **Inspector**: automated git-hygiene check before v0.6.0 controlled-run execution
- **Context**: Working tree contained uncommitted modifications to v0.5.4 run artifacts alongside new untracked v0.6.0 implementation files.

## Files Observed as Modified

| File | HEAD (committed) | Working tree (drifted) |
|---|---|---|
| `runs/.../real_provider_diagnostic_summary.json` | `deepseek: 0.85, openai: 0.8611` | `deepseek: 0.8611, openai: 0.8611` |
| `runs/.../real_provider_responses.jsonl` | 20 records from first real execution | 20 records from second real execution (different timestamps, different LLM response text) |
| `runs/.../real_provider_scores.jsonl` | `task_007: deepseek score=0.75` | `task_007: deepseek score=0.8611` |
| `runs/.../provider_request_metadata.jsonl` | timestamps from first execution | timestamps from second execution |

## Drift Classification

**Type: Accidental rerun/overwrite (category c)**

The v0.5.4 `run_authorized_diagnostic()` was executed twice against live DeepSeek and OpenAI APIs:

1. **First execution** (committed to HEAD): `created_at` range ~07:58 UTC. DeepSeek returned no response for task_007 (`response_present=0`), producing `score=0.75` for that record. DeepSeek mean: 0.85.

2. **Second execution** (working tree, from current session): Different timestamps, different LLM responses. DeepSeek returned a valid response for task_007 (`response_present=1`), producing `score=0.8611` for that record. All tasks scored uniformly at 0.8611.

**Root cause**: The v0.5.4 `write_authorized_diagnostic_artifacts()` overwrote the existing output directory (`runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/`) without checking whether the directory already contained committed evidence.

## Impact

- Historical evidence was mutated in place — the first execution's responses and scores are no longer retrievable from the working tree.
- The score difference is minor (0.85→0.8611, +1.3%) but represents a real scoring variance due to nondeterministic LLM responses.
- No test outcomes, frozen dataset artifacts, or provider-independent configurations were affected.

## Policy

Historical run artifacts (files under `runs/`) must not be silently mutated after they have been committed. Re-execution of a runner must go to a new output directory or explicitly confirm overwrite intent.

## Remediation

The 4 modified files under `runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/` were restored to their HEAD (committed) state using:

```powershell
git restore runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/provider_request_metadata.jsonl
git restore runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/real_provider_diagnostic_summary.json
git restore runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/real_provider_responses.jsonl
git restore runs/finitexo_code_matrix_v0_5_4_real_provider_diagnostic_authorized/real_provider_scores.jsonl
```

## Status After Remediation

- All historical v0.5.4 artifacts restored to HEAD.
- Working tree clean for all `runs/` files.
- v0.6.0 implementation files are staged and ready for commit.
- v0.6.0 execution was intentionally blocked until drift resolution.

## Prevention for v0.6.0

The v0.6.0 `ControlledRunConfig` includes `allow_overwrite: bool = False` by default. The preflight gate checks `output_dir_not_empty_and_overwrite_not_allowed` and blocks execution if the output directory exists and is non-empty. This prevents the same accidental overwrite pattern.
