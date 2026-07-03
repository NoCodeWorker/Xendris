# Xendris Baseline Status

Date: 2026-07-03

## Status

```txt
BASELINE_STABLE_MINIMAL
```

## Scope

This baseline prepares the repository for a stable Xendris framework layer while retaining `phyng` as the internal scientific engine.

No new scientific functionality was added.

## Architecture Boundary

```txt
xendris/ = public framework namespace
phyng/   = internal / legacy scientific engine
docs/    = historical and project documentation
tests/   = verification contracts and legacy suite
formal/  = Lean formalization workspace
frontend/ = Xendris AI interface
```

## Packaging

`pyproject.toml` now packages:

```txt
xendris*
phyng*
```

Project package name:

```txt
xendris
```

Compatibility note:

```txt
phyng remains importable.
```

## Verification Commands

Focused Xendris contract suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_benchmark_contract.py tests\test_pipeline_contract.py tests\test_scorer_contract.py tests\test_xendris_false_formality.py
```

Result:

```txt
12 passed in 9.08s
```

Full Python suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```txt
1070 passed, 4 warnings in 108.94s
```

Warnings:

```txt
Deprecation warnings for legacy phyng modules retained for compatibility:
phyng.baselines
phyng.copilot
phyng.closed_loop
phyng.synthetic_benchmark_design
```

Focused minimal contract subset:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_benchmark_contract.py tests\test_pipeline_contract.py tests\test_scorer_contract.py
```

Result:

```txt
6 passed in 0.48s
```

Import smoke:

```powershell
.\.venv\Scripts\python.exe -c "import xendris, phyng; from xendris.benchmarks.false_formality.runner import load_cases; print(xendris.__version__); print(phyng.__file__); print(load_cases('xendris/benchmarks/false_formality/cases.json')[0].id)"
```

Result:

```txt
0.3.0
D:\BIOCULTOR\PHYNG\phyng\__init__.py
FF-001
```

## Lean Status

Command attempted:

```powershell
lake build
```

Result:

```txt
NOT_RUN_LAKE_UNAVAILABLE_IN_PATH
```

PowerShell reported:

```txt
The term 'lake' is not recognized as a name of a cmdlet, function, script file, or executable program.
```

Interpretation:

```txt
Lean/Lake environment setup is currently blocking formal verification.
This is not evidence of a Lean source failure.
```

## Frontend Status

Command:

```powershell
cd frontend
npm run build
```

Result:

```txt
Compiled successfully.
```

Routes:

```txt
/
/_not-found
/api/chat
/api/chat/stream
/x
```

## Known Baseline Limits

- The repository still contains substantial historical `phyng` research artifacts.
- Large physical/scientific modules were not moved.
- Generated data and reports remain in place.
- Root Git tracking currently contains only the frontend commit history unless explicitly expanded.

## Allowed Claims

- Xendris has a minimal public Python namespace.
- Phyng remains available as the internal scientific engine.
- The focused Xendris False Formality benchmark contracts pass.
- The full Python test suite passes in the current local environment.
- The frontend production build passes in the current local environment.
- The package configuration now includes both `xendris` and `phyng`.

## Forbidden Claims

- Xendris is scientifically validated.
- Xendris is superior to any model in general.
- Lean verification passed in this environment.
- Historical Phyng artifacts have been fully reorganized.

## Next Safe Step

Run one of:

```txt
1. Lean/Lake PATH repair and formal build check.
2. Git baseline expansion strategy: decide whether the repo should track only frontend or the full scientific workspace.
3. Controlled deprecation map for legacy phyng modules that emitted warnings.
```
