# Xendris v0.3.0 Trust Kernel

## Purpose

Introduce a minimal auditable reasoning kernel for Xendris.

The Trust Kernel allows an answer to be represented as a set of auditable claims, then evaluated with deterministic support, risk, and decision rules. It is designed as a trust layer above any model output, but it does not call models or external services.

## Scope

This first implementation covers:

- typed claim categories,
- claim support status,
- risk levels,
- audit decisions,
- immutable claim records,
- immutable reasoning audit records,
- deterministic evaluation rules,
- structural audit validation.

It does not include:

- automatic LLM claim extraction,
- RAG or source retrieval,
- provider-specific integrations,
- semantic truth validation,
- benchmark metrics,
- agent workflows.

## New modules

```txt
xendris/core/trust/
  __init__.py
  types.py
  claims.py
  audit.py
  evaluators.py
  contracts.py
```

## Claim model

`Claim` represents one auditable statement:

```txt
text
claim_type
confidence
status
source_refs
notes
```

Rules:

- `text` must not be empty.
- `confidence` must be between `0.0` and `1.0`.
- `source_refs` are stored immutably as a tuple.
- The model is safe for simple serialization through `to_dict()`.

## ReasoningAudit model

`ReasoningAudit` represents the structural audit of an answer:

```txt
answer
claims
global_confidence
risk_level
decision
unsupported_claims
notes
```

Rules:

- `answer` must not be empty.
- `global_confidence` must be between `0.0` and `1.0`.
- unsupported claims must be listed in `unsupported_claims` for a structurally valid audit.
- contradicted claims block approval.
- high or critical risk cannot be approved without explicit notes.

## Decision rules

The initial deterministic evaluator applies these rules:

1. Contradicted claim:
   - `risk_level = HIGH`
   - `decision = BLOCKED`
2. Unsupported claim with `confidence >= 0.70`:
   - `risk_level = HIGH`
   - `decision = HUMAN_REVIEW_REQUIRED`
3. Unsupported claim with low or medium confidence:
   - `risk_level = MEDIUM`
   - `decision = APPROVED_WITH_LIMITATIONS`
4. All claims verified or user-provided:
   - `risk_level = LOW`
   - `decision = APPROVED`
5. No claims:
   - `risk_level = MEDIUM`
   - `decision = HUMAN_REVIEW_REQUIRED`
   - `global_confidence <= 0.5`

## Tests

Focused tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/core/test_trust_kernel.py -q
```

Coverage includes:

- valid claim construction,
- invalid claim rejection,
- approved verified audits,
- unsupported low-confidence claims,
- unsupported high-confidence claims,
- contradicted documentation claims,
- no-claims audits,
- impossible audit rejection.

## Compatibility with v0.2.0

The Trust Kernel is additive.

It does not modify:

- `xendris.__all__`,
- `xendris.frontera_c`,
- `xendris.core.rag`,
- `xendris.core.response_contract`,
- `phyng/`,
- frontend code,
- provider code.

The v0.2.0 import surface remains compatible.

## Current status

Status:

```txt
IMPLEMENTED_NOT_RELEASED
```

This document describes the first deterministic Trust Kernel implementation toward `v0.3.0`. It does not declare `v0.3.0` released and does not create a tag.
