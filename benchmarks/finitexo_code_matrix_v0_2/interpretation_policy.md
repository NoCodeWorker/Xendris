# Finitexo Code Matrix v0.2 - Interpretation Policy

## Decisions

| Decision | Meaning |
|---|---|
| READY_FOR_INTERPRETATION | Evidence is structurally complete for bounded interpretation. |
| WARNINGS_PRESENT | Evidence can be discussed only with explicit limitations. |
| BLOCKED_FOR_INTERPRETATION | Do not use the result as benchmark evidence. |
| HUMAN_REVIEW_REQUIRED | Manual review is required before interpretation. |
| BUDGET_VALIDATION_ONLY | Small run used only to validate cost/mechanics. |
| SIGNAL_REPLICATION_ONLY | Small run can discuss repeated signal only, not performance. |

## Thresholds

- `n < 20`: budget validation or signal replication only.
- `n >= 20`: internal strong-signal discussion may begin if other gates pass.
- `n >= 50`: preliminary comparative discussion may begin.
- `n >= 100`: public claims may be considered only if all gates pass.

## Conditions for READY_FOR_INTERPRETATION

- dataset hash valid;
- scoring contract hash valid;
- anti-ad-hoc decision is not BLOCKED;
- no unauthorized run-time modifications;
- evidence contract is INTERPRETABLE;
- sample threshold is compatible with the intended interpretation.

## Forbidden Interpretations

- Xendris is superior.
- Xendris programs better in general.
- Xendris is production-ready.
- Results generalize beyond this benchmark.
- Results transfer to providers or models that were not measured.
