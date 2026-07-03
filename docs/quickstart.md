# Xendris Quickstart

## Status

- Xendris is currently a research/framework baseline.
- Stable import surface for v0.2.0 is intentionally minimal.
- Scientific validation claims must be treated separately from API stability.
- `phyng` remains the internal scientific engine and legacy compatibility layer.

## Installation

In editable mode:

```bash
python -m pip install -e .
```

With development dependencies:

```bash
python -m pip install -e ".[dev]"
```

On this Windows workspace, the validated local command uses the virtual environment interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Minimal Import Check

The stable public import surface for v0.2.0 is:

```txt
xendris
xendris.frontera_c
xendris.core.rag
```

Run:

```powershell
.\.venv\Scripts\python.exe -c "import xendris; import xendris.frontera_c; import xendris.core.rag; print('IMPORT_OK', xendris.__version__, xendris.__all__)"
```

Expected result:

```txt
IMPORT_OK 0.2.0 ['frontera_c']
```

`xendris.core.rag` is intentionally importable by direct path. It is not exported through `xendris.__all__`.

## Frontera C Bridge Example

`xendris.frontera_c` is a stable bridge over selected `phyng` scientific primitives. Importability does not imply scientific validation.

```python
from xendris.frontera_c import (
    C,
    Claim,
    ClaimType,
    evaluate_claim,
    planck_length,
)

print(C)
print(planck_length())
```

Use this layer for stable access to selected constants, claim-gatekeeper contracts, and compatibility wrappers.

## Source And Claim Registry Example

`xendris.core.rag` exposes source and claim registry helpers from the internal engine.

```python
from xendris.core.rag import (
    SourceRecord,
    ClaimRecord,
    add_source,
    list_sources,
    audit_claim_support,
)
```

This layer is a registry/audit helper surface. It does not make raw sources into evidence and does not create scientific validation by itself.

## Experimental Namespaces

The following namespaces remain importable by direct path for backward compatibility, but are not stable public API for v0.2.0:

```txt
xendris.core.campaigns
xendris.models
xendris.benchmarks
xendris.benchmarks.false_formality
xendris.prompts
xendris.outputs
xendris.scripts
formal/
```

Do not build external integrations against these namespaces until they receive explicit API documentation and contract tests.

## Validation

Focused Xendris contracts:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_xendris_imports.py tests\test_benchmark_contract.py tests\test_pipeline_contract.py tests\test_scorer_contract.py tests\test_xendris_false_formality.py
```

Full Python suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Current latest local validation for the v0.2.0 API boundary:

```txt
1070 passed, 4 warnings
```

## Lean Status

Lean formalization is outside the Python runtime API. If Lean/Lake is installed:

```powershell
lake build
```

If `lake` is not available in `PATH`, that is an environment blocker, not a demonstrated failure of the Python package.

## Frontend Status

The Next.js frontend is separate from the Python framework API. If needed:

```powershell
cd frontend
npm run build
```

Frontend build success does not change the Python API stability status.

## Non-Claims

This quickstart does not claim:

- scientific validation,
- model superiority,
- empirical support,
- physical confirmation,
- stable benchmark API,
- stable CLI API.

It only documents the minimal reproducible import and validation path for Xendris v0.2.0.

## Next Step

Before tagging a v0.2.0 release, review package metadata alignment in `pyproject.toml` and confirm whether its version should match `xendris.__version__`.
