# Xendris API Audit v0.2.0

## Objective

Auditar la superficie pública mínima de `xendris/` para la fase `v0.2.0`, separando API estable candidata, bridges legacy hacia `phyng`, módulos experimentales y piezas internas.

Esta auditoría no cambia código ni comportamiento. Su función es definir una propuesta conservadora para estabilizar la primera API pública del framework Xendris sin renombrar `phyng/`, eliminar módulos legacy ni introducir nuevos claims científicos.

## Current package structure

Estructura Python actual revisada:

```txt
xendris/
  __init__.py
  frontera_c/
    __init__.py
  core/
    __init__.py
    rag/
      __init__.py
    campaigns/
      __init__.py
  benchmarks/
    __init__.py
    false_formality/
      __init__.py
      cases.json
      rubric.json
      runner.py
      evaluator.py
      scorer.py
      report.py
      core/
        __init__.py
        base_model_client.py
        mock_engine.py
        types.py
        xendris_pipeline.py
  models/
    __init__.py
  prompts/
    __init__.py
  outputs/
    __init__.py
  scripts/
    __init__.py
```

The package is intentionally layered over `phyng/`, which remains the scientific engine and legacy implementation layer.

## Current public exports

### `xendris`

Current metadata:

```python
__version__ = "0.2.0"
__all__ = ["frontera_c"]
```

Assessment:

- `xendris` is importable.
- The top-level namespace now advertises only `frontera_c` as a stable top-level export.
- `xendris.core.rag` remains a stable API candidate by direct import path rather than top-level star export.
- Experimental namespaces remain importable by direct path for backward compatibility.

### `xendris.frontera_c`

Current exports:

```txt
C
HBAR
G
planck_length
planck_mass
planck_area
ClaimType
Layer
TraceType
InvalidMassError
validate_compton_gravity_invariant
compton_wavelength
gravitational_radius
OperationalScale
review_operational_scale
frontier_signature
predictive_gain
epistemic_trace
Claim
evaluate_claim
```

Assessment:

- Import validation passes.
- This is a direct bridge to `phyng` scientific primitives.
- It is the strongest candidate for public API, but the surface is broad.
- Some names, especially `predictive_gain`, `frontier_signature`, and `epistemic_trace`, carry legacy scientific semantics and should be documented carefully before being declared stable.

### `xendris.core.rag`

Current exports:

```txt
SourceRecord
ClaimRecord
ClaimSourceLink
add_source
list_sources
add_claim
list_claims
link_claim_to_source
audit_claim_support
```

Assessment:

- Import validation passes.
- This is a direct bridge to `phyng.rag`.
- It is a reasonable public API candidate if documented as source/claim registry helpers rather than as a full RAG product layer.

### `xendris.core.campaigns`

Current exports:

```txt
Campaign002Input
CampaignInput
run_campaign_002_decoherence_model_comparison
run_mesoscopic_boundary_campaign
build_atlas
PhysicalSystemSpec
AtlasThresholds
```

Assessment:

- Import validation passes.
- This is a legacy bridge to campaign orchestration in `phyng`.
- It exposes historical campaign semantics and should remain experimental/internal for `v0.2.0`.

### `xendris.models`

Current exports:

```txt
Claim
BenchmarkCase
ModelResponse
RubricScore
BenchmarkResult
BenchmarkSummary
```

Assessment:

- Import validation passes.
- The namespace mixes Frontera C claim types with benchmark-specific contracts.
- It should not be declared stable until the model boundary is split into public scientific contracts and benchmark-only contracts.

### `xendris.benchmarks`

Current exports:

```txt
false_formality
```

### `xendris.benchmarks.false_formality`

Current exports:

```txt
load_cases
run_benchmark
```

### `xendris.benchmarks.false_formality.core`

Current exports:

```txt
BenchmarkCase
BenchmarkResult
BenchmarkSummary
ModelResponse
RubricScore
```

Assessment:

- Focused tests cover false-formality contracts.
- This benchmark suite is useful and reproducible, but it should remain experimental for `v0.2.0`.
- Benchmark outputs are intentionally excluded from Git via `**/outputs/`.

### `xendris.prompts`

Current state:

- Placeholder package.
- No public symbols.

Assessment:

- Internal/experimental until prompt contracts exist.

### `xendris.outputs`

Current state:

- Directory marker only.
- No importable symbols.

Assessment:

- Internal marker only.
- Not a public logic API.

### `xendris.scripts`

Current state:

- Script/CLI utility namespace marker.
- No public symbols.

Assessment:

- Internal until a CLI contract is defined.

## Legacy bridges to Phyng

Confirmed bridge modules:

```txt
xendris.frontera_c      -> phyng.constants, phyng.enums, phyng.errors, phyng.frontier_lengths, phyng.operational_scale, phyng.signature, phyng.predictive_gain, phyng.epistemic_trace, phyng.claim_gatekeeper
xendris.core.rag        -> phyng.rag
xendris.core.campaigns  -> phyng.campaigns, phyng.atlas
xendris.models          -> xendris.frontera_c plus false_formality benchmark types
```

Bridge policy recommended for `v0.2.0`:

- Keep bridges in place for backward compatibility.
- Do not rename `phyng/`.
- Do not remove legacy modules.
- Document bridge status explicitly so public callers understand that `phyng` remains the scientific engine.

## Candidate stable API

Recommended minimal stable API for `v0.2.0`:

```txt
xendris
xendris.frontera_c
xendris.core.rag
```

Rationale:

- These imports are currently available and validated.
- They represent the public framework namespace, the scientific bridge layer, and the source/claim registry bridge.
- They avoid committing benchmark internals, campaign runners, prompt placeholders, output markers, and mixed model namespaces as stable API too early.

Recommended stable surface details:

### `xendris`

Stable candidate:

- package import
- version metadata, after version alignment
- documented namespace map

Action required before release:

- Decide whether `__version__` should be aligned to `0.2.0`.
- Reduce or document `__all__` so experimental namespaces are not accidentally treated as stable.

### `xendris.frontera_c`

Stable candidate:

- constants and physical primitive helpers
- claim gatekeeper types
- operational scale helpers

Requires documentation:

- Which exported symbols are stable contracts.
- Which are legacy scientific bridge symbols.
- Which symbols do not imply validation or scientific support.

### `xendris.core.rag`

Stable candidate:

- source records
- claim records
- source/claim linking helpers
- audit helpers

Requires documentation:

- This is a registry/audit helper layer, not a complete retrieval product surface.
- It does not create evidence by itself.

## Candidate experimental/internal API

Recommended experimental/internal surfaces for `v0.2.0`:

```txt
xendris.core.campaigns
xendris.models
xendris.benchmarks
xendris.benchmarks.false_formality
xendris.benchmarks.false_formality.core
xendris.prompts
xendris.outputs
xendris.scripts
formal/
```

Reasons:

- `xendris.core.campaigns` exposes historical campaign runners and atlas construction that are still tightly coupled to `phyng`.
- `xendris.models` mixes benchmark contracts and Frontera C claim contracts.
- `xendris.benchmarks.false_formality` is useful but still an evaluation suite, not a general public framework API.
- `xendris.prompts` is a placeholder package.
- `xendris.outputs` is a marker for generated artifacts and should not be treated as importable logic.
- `xendris.scripts` is reserved for one-off runners or future CLI utilities.
- Lean formalization remains separate from the Python API and should be documented as formal scaffolding, not runtime API.

## Import validation

Command executed:

```powershell
.\.venv\Scripts\python.exe -c "import xendris; import xendris.frontera_c; import xendris.core.rag; import xendris.core.campaigns; import xendris.benchmarks; import xendris.benchmarks.false_formality; import xendris.models; print('IMPORT_OK', xendris.__version__)"
```

Result:

```txt
IMPORT_OK 0.3.0
```

Validated imports:

```txt
xendris
xendris.frontera_c
xendris.core.rag
xendris.core.campaigns
xendris.benchmarks
xendris.benchmarks.false_formality
xendris.models
```

No import failures were observed.

## Test validation

Command executed:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Result:

```txt
1070 passed, 4 warnings in 76.53s
```

Warnings observed:

```txt
phyng.baselines is deprecated and scheduled for removal. Use xendris.benchmarks for evaluation suites.
phyng.copilot is deprecated and scheduled for removal. Use the main Xendris web interface.
phyng.closed_loop is deprecated and scheduled for removal. Use xendris.benchmarks for evaluation and runner suites.
phyng.synthetic_benchmark_design is deprecated and scheduled for removal. Use xendris.benchmarks.false_formality for test cases.
```

Interpretation:

- The current bridge strategy is functioning.
- Deprecation warnings confirm that `phyng` remains active as a legacy engine, with selected migration targets under `xendris`.
- No test failure blocks the API audit.

## Risks

1. Version drift risk

`xendris.__version__` has been aligned to `0.2.0` for this phase. Future roadmap/tag changes must keep this metadata synchronized.

2. Top-level namespace policy risk

`xendris.__all__` now includes only `frontera_c`. This avoids advertising experimental namespaces as stable, but direct imports such as `xendris.core.rag` must remain documented because `core.rag` is still a stable candidate.

3. Scientific bridge semantics risk

`xendris.frontera_c` exports symbols whose names may imply stronger scientific status than the baseline allows. API documentation must clearly state that stable importability is not scientific validation.

4. Mixed model namespace risk

`xendris.models` combines `Claim` with benchmark result schemas. This should be split or documented before becoming stable.

5. Campaign coupling risk

`xendris.core.campaigns` remains tightly coupled to historical `phyng` campaigns and should not be promoted as public stable API yet.

6. Benchmark scope risk

`false_formality` is useful as an evaluation suite but is not yet a general Xendris framework API.

## Recommendations

1. Declare the `v0.2.0` public API as:

```txt
xendris
xendris.frontera_c
xendris.core.rag
```

2. Treat the following as experimental/internal:

```txt
xendris.core.campaigns
xendris.models
xendris.benchmarks
xendris.prompts
xendris.outputs
xendris.scripts
```

3. Keep version metadata aligned before tagging `v0.2.0`.

4. Add documentation for stable vs experimental namespace boundaries.

5. Do not remove or rename `phyng/` during `v0.2.0`.

6. Do not promote benchmarks to public API until the CLI and fixture/output policy are documented.

7. Preserve backward compatibility while moving public documentation toward `xendris`.

## Proposed next implementation step

Create a small API boundary hardening change for `v0.2.0`:

1. Update documentation to state that the stable API candidate is:

```txt
xendris
xendris.frontera_c
xendris.core.rag
```

2. Keep `xendris.__version__` aligned with the `0.2.0` release phase.

3. Keep experimental namespaces out of `xendris.__all__` until they are documented.

4. Add focused tests that assert the public API boundary without forcing experimental namespaces to be stable.
