# Finitexo Code Matrix v0.3 - External Adversarial Validation

## Purpose

Finitexo Code Matrix v0.3 tests whether prior Xendris programming-agent
signals survive a more adversarial benchmark design.

The benchmark is designed to preserve the null hypothesis by default:

```txt
H0: Xendris does not show a clear advantage over a strong non-Xendris baseline.
```

The benchmark is successful if it can honestly report no clear advantage,
baseline match, baseline outperformance, inconclusive results, or blocked
interpretation.

## Scope

This package provides infrastructure only:

- semi-external task fixtures;
- manifest and hash integrity;
- blind scoring primitives;
- strong-baseline comparison;
- evidence-contract checks;
- conservative report generation;
- plan-only and dry-run runners.

Provider execution is disabled by default and requires an explicit `--execute`
flag plus safe budget and blind-scoring conditions.

## Dataset Status

No verified third-party external dataset is bundled in this repository. The
current v0.3 seed tasks are marked as `SEMI_EXTERNAL_SYNTHETIC`. They are
designed to resemble external maintenance tasks without reusing v0.1 or v0.2
fixtures.

## Claims Not Authorized

This benchmark does not authorize:

- universal superiority claims;
- general coding superiority claims;
- production-readiness claims;
- provider superiority claims;
- claims based on weak baselines;
- claims from non-blind scoring.

## Default Decision

Until real external execution and blind scoring produce interpretable evidence,
the expected implementation decision is:

```txt
IMPLEMENTED_SEMI_EXTERNAL_ADVERSARIAL_INFRASTRUCTURE
```

