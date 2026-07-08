# Finitexo Code Matrix v0.8.0 — Hard Programming Dataset n=30

## Why v0.8.0 Exists

v0.7.0 executed the paired Xendris lift with the v0.6.0 controlled run n=30 dataset. Observed mean scores:

| Variant | Mean Score |
|---|---|
| deepseek_base | 0.89038 |
| deepseek_xendris | 0.90064 |
| openai_base | 0.88460 |
| openai_xendris | 0.88716 |

The lift was positive but small. The base models already scored ~0.88–0.89, leaving limited headroom for lift measurement. v0.8.0 creates a technically harder programming dataset to reduce these ceiling effects.

## The Dataset Is Harder, Not a Trap

The tasks are hard because of genuine programming complexity, not hidden epistemic traps:

- They require reasoning about edge cases, state, and design tradeoffs.
- They include realistic constraints a developer would encounter.
- They do not include trick questions, adversarial traps, or Xendris-specific bait.
- No canonical solutions or answer keys are exposed in the task files.
- No hidden tests, model-specific hints, or fake benchmark content.

## Task Families

5 families with 6 tasks each = 30 tasks:

| Family | Focus |
|---|---|
| algorithmic_reasoning | Non-trivial algorithmic reasoning, conflict detection, cycle reporting, stable grouping, parser-like transformation, diff/patch planning |
| stateful_refactor | Refactoring stateful code while preserving behavior, separating validation from mutation, fixing shared mutable state, making retry state explicit, avoiding global-state leakage |
| edge_case_handling | Empty inputs, duplicate keys, mixed casing, malformed records, timezone-like ordering without libraries, stable multi-key sort with missing fields |
| api_design_consistency | Backward-compatible parameter addition, preserving JSON schema, avoiding renamed exports, backward-compatible defaults, specific exception handling, avoiding broad exception swallowing |
| performance_constraints | O(n) duplicate detection, map-based join, caching serialization, streaming aggregation, memory-conscious filtering, single-pass normalization |

## Authorized Claims

- A harder programming dataset n=30 was created.
- The dataset is deterministic and hash-tracked.
- The dataset is intended to reduce ceiling effects.
- The dataset has documented provenance and family distribution.
- No providers were called during dataset creation.

## Prohibited Claims

- Model superiority — not authorized.
- Xendris superiority — not evaluated here.
- Statistical significance — not measured.
- Production readiness — not evaluated.
- External benchmark validity — not validated.
- The dataset is unbiased in any universal sense — not claimed.
- Harder means objectively harder for every model — not asserted.

## Status

- v0.8.0 is a dataset-only release.
- No live execution has been performed with this dataset.
- No providers were called.
- v0.8.1 (hard paired lift) is the next planned step.
