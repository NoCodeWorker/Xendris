# Finitexo Code Matrix v0.3 - Falsification Policy

The benchmark is successful if it can honestly report that Xendris did not show a clear advantage.

A result where strong_non_xendris_agent matches Xendris is not a benchmark failure. It is valuable evidence that the observed improvement may be explained by prompt quality, task discipline, or baseline weakness rather than Xendris architecture.

A result where strong_non_xendris_agent outperforms Xendris must be preserved, reported, and must not be hidden or reinterpreted as success.

H0 remains live by default.

## Allowed Outcomes

- Xendris advantage observed internally only.
- No clear advantage.
- Strong baseline matched the system.
- Strong baseline outperformed the system.
- Benchmark inconclusive.
- Blocked for interpretation.

## Forbidden Reinterpretations

Do not convert baseline match, baseline outperformance, inconclusive evidence,
or blocked evidence into a success claim.

