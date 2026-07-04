# Xendris v0.3.1 Evidence Binding Layer

## Purpose

Add a minimal deterministic evidence layer to the Xendris Trust Kernel.

The layer lets declared claims reference immutable evidence objects and gives the evaluator enough structure to prevent factual, calculated, and code-state claims from being treated as verified without sufficient support.

## Scope

Added:

- `EvidenceType`
- `Evidence`
- `EvidenceBinding`
- `compute_support_score`
- `bind_evidence_to_claim`
- evidence-aware `TrustKernelEvaluator`

The implementation is deterministic and local. It does not call models, crawl files, access networks, retrieve sources, or validate factual truth.

## New modules

```txt
xendris/core/trust/evidence.py
tests/core/test_trust_evidence.py
```

Updated:

```txt
xendris/core/trust/__init__.py
xendris/core/trust/evaluators.py
```

## Evidence model

`Evidence` contains:

```txt
evidence_id
evidence_type
source
content_hash
excerpt
confidence
metadata
```

Validation:

- `evidence_id` must not be empty.
- `source` must not be empty.
- `content_hash` must not be empty.
- `confidence` must be between `0.0` and `1.0`.
- `evidence_type` must be a valid `EvidenceType`.
- `metadata` is stored as an immutable mapping.

## Deterministic support scoring

`compute_support_score(claim, evidence_items)` currently uses a simple v0.3.1 rule:

- no evidence returns `0.0`;
- otherwise support is the average evidence confidence;
- the score is clamped to `[0.0, 1.0]`.

This is intentionally minimal. It is not a semantic evidence evaluator.

## Evaluator behavior

The evaluator now enforces:

- `FACTUAL`, `CALCULATED`, and `CODE_STATE` claims marked `VERIFIED` require support score `>= 0.75`.
- insufficiently supported verified claims trigger `HUMAN_REVIEW_REQUIRED` with `HIGH` risk.
- high-confidence unsupported claims still require human review.
- lower-confidence unsupported claims are approved only with limitations.
- `USER_PROVIDED` claims can pass without external evidence, but only with limitations.

## Deterministic guarantees

The layer:

- is pure Python;
- uses no external services;
- performs no network calls;
- performs no file-system crawling;
- adds no dependencies;
- preserves existing Trust Kernel call compatibility by making evidence bindings optional.

## Deferred work

Not implemented in v0.3.1:

- contradiction detection from evidence content;
- source weighting;
- cryptographic provenance;
- source hash verification;
- RAG integration;
- automatic claim extraction;
- model-based evidence review;
- provider-specific evidence adapters.

Contradictory evidence handling remains explicit/manual through `ClaimStatus.CONTRADICTED`.

## Tests

Focused tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_kernel.py tests/core/test_trust_evidence.py -q
```

Coverage includes:

- evidence creation;
- invalid confidence rejection;
- empty evidence identifier/source/hash rejection;
- no-evidence support score;
- average support score;
- factual verified claim without evidence requiring review;
- factual verified claim with strong evidence being approvable;
- user-provided claims passing with limitations;
- public imports from `xendris.core.trust`.

## Current status

```txt
IMPLEMENTED_NOT_RELEASED
```

This is a v0.3.1 development milestone. It does not declare a release, tag, benchmark result, or model-quality claim.
