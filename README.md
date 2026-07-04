# Xendris

Xendris is the public framework layer of this repository.

It provides a controlled research and evaluation shell around an internal scientific engine, `phyng`. The current stable baseline keeps the boundary explicit:

```txt
Xendris = public framework, contracts, benchmark entry points
Phyng   = internal / legacy scientific engine
```

This repository does not claim scientific validation, model superiority, or universal correctness. Its stable role is to make claims, benchmarks, and computational experiments easier to audit.

## Current Baseline

Status: `BASELINE_STABLE_MINIMAL`

Verified:

- `xendris` imports from the project root.
- `phyng` remains importable as the internal engine.
- The False Formality benchmark contracts pass.
- The full Python suite passes locally.
- The frontend production build passes locally.
- The package configuration includes both `xendris*` and `phyng*`.

Known environment blocker:

- Lean/Lake verification cannot run unless `lake` is available in `PATH`.

See [docs/status/BASELINE_STATUS.md](docs/status/BASELINE_STATUS.md) for the current verification record.

## Repository Boundary

### `xendris/`

Public framework namespace.

Expected responsibilities:

- framework-level contracts
- benchmark families
- public orchestration boundaries
- reusable prompts and outputs
- stable compatibility wrappers over internal scientific logic

### `phyng/`

Internal scientific engine and legacy research lab.

Expected responsibilities:

- physical and epistemic rules
- historical campaigns
- source-processing experiments
- scientific audit utilities
- legacy modules retained for compatibility

`phyng` should not be treated as the public product surface.

### `frontend/`

Next.js frontend for the Xendris AI chat interface.

The frontend is independent from the Python scientific baseline and has its own build pipeline.

### `formal/`

Lean formalization workspace.

The formalization is abstract and does not validate any physical claim by itself.

## Python Setup

Use Python 3.11+.

```powershell
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

## Minimal Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_benchmark_contract.py tests\test_pipeline_contract.py tests\test_scorer_contract.py tests\test_xendris_false_formality.py
```

Current result:

```txt
12 passed
```

Full local Python suite:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Current result:

```txt
1142 passed, 4 warnings
```

## Lean Verification

If Lean/Lake is installed:

```powershell
lake build
```

If PowerShell reports `lake` is not recognized, the blocker is environment setup, not a demonstrated formalization failure.

## Frontend Verification

```powershell
cd frontend
npm run build
```

Current result:

```txt
Compiled successfully.
```

## Refactor Discipline

The repository is mid-transition. Do not move large historical modules without:

1. contract tests,
2. import compatibility,
3. documented rollback,
4. verification output.

The current baseline intentionally favors stability over aggressive cleanup.
