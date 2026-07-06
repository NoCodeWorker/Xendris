# Xendris Governance Index

Date: 2026-07-06

## Purpose

This index is the navigation layer for Xendris governance documents. It keeps
the product goal, response discipline, benchmark evidence rules, artifact
quarantine, and release gates connected.

## North Star

- [Xendris Product Goal](XENDRIS_PRODUCT_GOAL.md)

Defines Xendris as an epistemic trust runtime and cognitive-certainty membrane
for AI outputs, agents, model calls, and benchmark evidence.

## Response Governance

- [Response Contract v0.2.0](RESPONSE_CONTRACT_V0_2_0.md)

Defines domain-agnostic rules for correctness, calibrated confidence, explicit
limits, and non-overclaiming.

## Evidence Governance

- [Benchmark Evidence Registry](../benchmarks/BENCHMARK_EVIDENCE_REGISTRY.md)
- [Benchmark Excellence Gate](../benchmarks/BENCHMARK_EXCELLENCE_GATE_V0_1.md)
- [Benchmark Suite Excellence Audit](../benchmarks/BENCHMARK_SUITE_EXCELLENCE_AUDIT.md)
- [Historical Rejected Benchmark Artifacts](../benchmarks/HISTORICAL_REJECTED_ARTIFACTS.md)

These documents define which benchmark artifacts may be used as evidence and
which must remain historical-only.

## Output and Artifact Policies

- [Generated Output Policy](../policies/GENERATED_OUTPUT_POLICY.md)
- [Historical Artifact Quarantine Policy](../policies/HISTORICAL_ARTIFACT_QUARANTINE_POLICY.md)

These policies prevent generated outputs, incomplete summaries, and rejected
benchmark artifacts from contaminating public evidence.

## Current Status Documents

- [Current Development Map](../status/XENDRIS_DEVELOPMENT_MAP_CURRENT.md)
- [v0.2.0 Roadmap](../status/ROADMAP_V0_2_0.md)
- [v0.2.0 API Audit](../status/API_AUDIT_V0_2_0.md)
- [v0.2.2 Release Gate](../status/HISTORICAL_ARTIFACT_QUARANTINE_AND_RELEASE_GATE_V0_2_2.md)

## Governance Rule

No benchmark result, model comparison, API stability claim, runtime claim, or
commercial claim should be treated as public evidence unless it can be traced
through the relevant governance document and evidence gate.

## Current Priority

The immediate governance priority is:

```txt
clean working tree
-> admitted evidence only
-> release gate without active blockers
-> taggable framework baseline
```
