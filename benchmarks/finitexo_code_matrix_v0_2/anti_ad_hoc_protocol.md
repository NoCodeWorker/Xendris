# Finitexo Code Matrix v0.2 - Anti-Ad-Hoc Protocol

## Purpose

The protocol detects whether a run is structurally safe to interpret or whether
the result may be contaminated by benchmark tailoring, mutable tasks, scoring
drift, answer leakage, or overclaiming.

## Required Checks

1. Dataset frozen hash valid.
2. Task hashes valid.
3. No task generated after run start.
4. No scoring contract modified during run.
5. No benchmark config modified during run.
6. No prompt contains answer leakage.
7. No task explicitly mentions Xendris-only behavior.
8. No evaluator imports agent internals.
9. No provider-specific favorable branch unless documented.
10. No positive claim if sample count is below threshold.

## Decisions

| Decision | Meaning |
|---|---|
| PASS | Required structural checks passed. |
| WARNINGS_PRESENT | Non-blocking weaknesses must be disclosed. |
| BLOCKED | Result must not be interpreted as benchmark evidence. |

Passing this protocol does not make a benchmark scientifically conclusive.
