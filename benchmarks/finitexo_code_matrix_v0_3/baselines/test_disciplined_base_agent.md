# test_disciplined_base_agent

## Purpose

Baseline focused on test discipline and contract preservation.

## Behavior

- Infer hidden tests from the prompt and public API.
- Prefer simple, local patches.
- Preserve function signatures and return types.
- Avoid broad rewrites.
- Do not touch forbidden files.
- Report uncertainty when verification is incomplete.

## Interpretation

Matching this baseline weakens claims that improvement comes from anything more
than normal disciplined programming behavior.

