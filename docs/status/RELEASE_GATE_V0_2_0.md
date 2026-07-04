# Xendris Release Gate v0.2.0

## Objective

Decidir si el estado actual de `main` puede etiquetarse como `v0.2.0-framework-api`.

## Git state

Gate executed on `main`.

```txt
git status --short
```

Result:

```txt
M README.md
M docs/quickstart.md
?? docs/status/RELEASE_GATE_V0_2_0.md
?? docs/status/TRUST_EVIDENCE_V0_3_1.md
?? docs/status/TRUST_KERNEL_V0_3_0.md
?? tests/core/
?? xendris/core/trust/
```

```txt
git status
```

Result:

```txt
On branch main
Your branch is up to date with 'origin/main'.
Changes not staged for commit are present.
Untracked files are present.
```

Latest commits reviewed:

```txt
df86fc7 feat: add response contract core
f6a5cde feat: add response contract core types
02c6375 docs: update v0.2.0 roadmap progress
c539ebe docs: define xendris response contract
0bcd785 chore: align package version with xendris api
a772615 docs: add xendris quickstart
530dd4f refactor: define minimal public xendris api
58af1d0 docs: add v0.2.0 roadmap
9ba100c chore: finalize repository baseline cleanup
74cfd51 refactor: clean legacy frontend xendris components
```

## Version validation

Module version:

```txt
MODULE_VERSION 0.2.0
```

Package metadata version:

```txt
PKG_VERSION 0.2.0
```

Version validation result:

```txt
PASS
```

## Public API validation

Command:

```powershell
.\.venv\Scripts\python.exe -c "import xendris; import xendris.frontera_c; import xendris.core.rag; import xendris.core.response_contract as rc; print('API_OK', xendris.__version__, rc.ClaimType.STANDARD_KNOWLEDGE.value)"
```

Result:

```txt
API_OK 0.2.0 STANDARD_KNOWLEDGE
```

Public API validation result:

```txt
PASS
```

## Response Contract validation

Command:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_xendris_response_contract.py -q
```

Result:

```txt
10 passed in 0.14s
```

Response Contract validation result:

```txt
PASS
```

## Test results

Full Python suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```txt
1098 passed, 4 warnings in 93.52s
```

Warnings are existing deprecation warnings around legacy `phyng` compatibility paths.

Git whitespace check:

```txt
git diff --check
```

Result:

```txt
PASS
```

## Documentation review

Reviewed:

- `README.md`
- `docs/quickstart.md`
- `docs/governance/RESPONSE_CONTRACT_V0_2_0.md`
- `docs/status/ROADMAP_V0_2_0.md`
- `docs/status/API_AUDIT_V0_2_0.md`

Coverage found:

- Minimal public API is documented in `docs/quickstart.md` and `docs/status/API_AUDIT_V0_2_0.md`.
- Version `0.2.0` is documented in `docs/quickstart.md`, `docs/status/API_AUDIT_V0_2_0.md`, and `docs/status/ROADMAP_V0_2_0.md`.
- Quickstart exists at `docs/quickstart.md`.
- Response Contract is documented in `docs/governance/RESPONSE_CONTRACT_V0_2_0.md`.
- Response Contract Core import example is documented in `docs/quickstart.md`.
- Non-claims and scientific validation limits are documented in `README.md` and `docs/quickstart.md`.
- Experimental namespaces are documented in `docs/quickstart.md` and `docs/status/API_AUDIT_V0_2_0.md`.

Documentation issues found:

```txt
README.md reports the current release-gate validation count:
1098 passed, 4 warnings.

docs/quickstart.md currently reports:
1098 passed, 4 warnings.

Current release-gate validation is:
1098 passed, 4 warnings.
```

Release documentation is aligned with the current test count, but the working tree is not clean.

## Known limitations

- `phyng/` remains the internal and legacy scientific engine.
- `xendris.core.response_contract` is a pure contract posture layer. It does not validate factual truth, scientific truth, or model superiority.
- `xendris.core.response_contract` does not call models, perform retrieval, rewrite responses, or replace human review.
- Experimental namespaces remain importable but are not stable public API for `v0.2.0`.
- Lean/Lake remains environment-dependent and is not part of this Python release gate.

## Release decision

```txt
BLOCKED
```

Reason:

```txt
Release validation, API validation, Python tests, and documentation counts pass, but the working tree is not clean because unrelated pending work is present.
```

Required remediation before tagging:

```txt
Resolve or explicitly scope the unrelated pending work:
docs/status/TRUST_EVIDENCE_V0_3_1.md
docs/status/TRUST_KERNEL_V0_3_0.md
tests/core/
xendris/core/trust/

Commit, stash, or otherwise resolve the unrelated pending work before tagging.
```

## Recommended tag

```txt
v0.2.0-framework-api
```

Tagging is not recommended until the documentation blocker above is resolved and the release gate is rerun or updated.
