# Trust Traps Canonical Artifact Policy

## Purpose

Trust Traps v0.1 has several historical benchmark artifacts. Some older
summaries are intentionally retained for audit history, but they are not all
admitted as evidence.

This policy defines which Trust Traps artifacts can be treated as canonical for
current Xendris benchmark interpretation.

## Canonical Generation Rule

Canonical dry-run Trust Traps artifacts must be generated through the
excellence-aware runner path and then admitted by the Benchmark Evidence
Registry.

The current admitted dry-run artifact is:

```txt
runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_summary.json
```

Its paired report is:

```txt
runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_report.md
```

## Historical Artifact Rule

Older Trust Traps summaries may remain in `runs/` and older reports may remain
under `docs/benchmarks/`, but they must not be cited as current evidence unless
they are admitted by `runs/benchmark_evidence_registry.json`.

Rejected artifacts must be discussed only as rejected, historical, blocked, or
not-admitted records.

## Real Provider Rule

This policy does not authorize real-provider runs. Real-provider Trust Traps
artifacts require separate execution, external data disclosure, provider/model
metadata, Benchmark Excellence review, and Evidence Registry admission.

Dry-run artifacts must not be described as real provider performance.

## Current Status

```txt
trust_traps_canonical_dry_run_policy: ACTIVE
real_provider_performance_claims: NOT_ESTABLISHED
universal_superiority_claims: FORBIDDEN
```
