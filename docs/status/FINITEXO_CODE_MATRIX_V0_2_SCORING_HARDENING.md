# Finitexo Code Matrix v0.2 - Scoring Hardening

## Objective

Harden the v0.2 scoring contract so a high diagnostic score cannot be treated
as verified success without mandatory evidence gates.

## What Changed

- `raw_score` is now explicitly diagnostic.
- `verified_success` requires mandatory gates plus interpretable evidence.
- `evidence_decision` is now a first-class admission gate.
- Missing or unknown evidence is treated conservatively.
- Non-admissible high-score cases are documented.
- The scoring contract hash in `dataset_manifest.json` was updated.

## raw_score vs verified_success vs evidence_decision

`raw_score` is the local numeric score from benchmark components. It can be
useful for diagnosis and comparison, but it is not admissibility.

`verified_success` is true only when:

- `raw_score >= 0.85`;
- hidden tests pass;
- API contract is preserved;
- forbidden files are untouched;
- no false success claim exists;
- anti-ad-hoc integrity is true;
- `evidence_decision = INTERPRETABLE`.

`evidence_decision` records whether the evidence layer is admissible. If it is
`INSUFFICIENT`, `BLOCKED`, `UNKNOWN`, or `MISSING`, verified success is false.

## Why High Score Without Evidence Does Not Count

A high score may come from visible tests, partial checks, or diagnostic
components while critical evidence is absent. Finitexo v0.2 must avoid turning
that into a positive claim. The benchmark therefore treats missing evidence as
non-admissible by default.

## Tests Executed

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_2.py -q
```

Result:

```txt
14 passed
```

Additional validation:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking -q
git diff --check
```

Result:

```txt
443 passed
git diff --check passed with existing LF/CRLF warnings
```

Full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```txt
1809 passed, 5 warnings
```

## Claims Still Prohibited

- Universal capability claims.
- General coding-superiority claims.
- Production-readiness claims.
- Provider superiority claims.
- Model superiority claims.
- Public marketing claims.

## Decision

`IMPLEMENTED_SCORING_HARDENED`
