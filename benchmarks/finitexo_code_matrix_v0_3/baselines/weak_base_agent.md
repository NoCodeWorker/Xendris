# weak_base_agent

## Purpose

Minimal direct baseline for diagnostic comparison only.

This baseline must not be used to support advantage claims. It is useful for
detecting whether a task is trivial or whether benchmark machinery works.

## Behavior

- Read the task prompt.
- Produce a direct patch.
- Do not perform explicit hidden-test reasoning.
- Do not add verification discipline beyond the visible prompt.

## Interpretation

If any system beats this baseline, the result is not sufficient evidence of an
architectural advantage.

