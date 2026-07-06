# API Surface Audit v0.2.2

**Date:** 2026-07-06  
**Package version:** `xendris.__version__ == "0.2.0"`  
**Baseline tag:** `v0.1.0-baseline`  
**Release tag:** `v0.2.2`

---

## Classification legend

| Label | Meaning |
|-------|---------|
| **PUBLIC_STABLE** | Safe to import. Semver guarantees. Breaking changes only in major version. |
| **PUBLIC_EXPERIMENTAL** | Usable but may change without notice. Deprecation warning before removal. |
| **PRIVATE** | Internal. Not intended for external consumers. Imports may break at any time. |
| **STUB** | Placeholder implementation for import compatibility. Full version on `experimental-trust-layers` branch. |
| **EMPTY** | No importable symbols. Directory marker only. |

---

## Module classification

### 1. `xendris` — PUBLIC_STABLE

```python
__version__ = "0.2.0"
__all__ = ["frontera_c"]
```

Top-level namespace. Exports `frontera_c` subpackage. Version string is stable.

---

### 2. `xendris.frontera_c` — PUBLIC_STABLE

Re-exports from `phyng` scientific engine. 19 symbols in `__all__`.

| Category | Symbols |
|----------|---------|
| Constants | `C`, `HBAR`, `G`, `planck_length`, `planck_mass`, `planck_area` |
| Enums | `ClaimType`, `Layer`, `TraceType` |
| Physics | `validate_compton_gravity_invariant`, `compton_wavelength`, `gravitational_radius`, `schwarzschild_radius`, `OperationalScale`, `review_operational_scale`, `frontier_signature`, `predictive_gain`, `epistemic_trace` |
| Gatekeeper | `Claim`, `evaluate_claim` |
| Errors | `InvalidMassError` |

---

### 3. `xendris.core.rag` — PUBLIC_STABLE

Re-exports from `phyng.rag`, `phyng.ytrue_extraction`, `phyng.real_source_acquisition`.

```python
from xendris.core.rag import SourceRecord, ClaimRecord, add_source, add_claim, audit_claim_support
```

9 symbols in `__all__`.

---

### 4. `xendris.core.response_contract` — PUBLIC_STABLE

Pure structures for response-contract assessment. No model calls, no validation.

```python
from xendris.core.response_contract import assess_response_contract, ClaimAssessment, ResponseContractAssessment
```

12 symbols in `__all__`.

---

### 5. `xendris.core.campaigns` — PUBLIC_EXPERIMENTAL

Re-exports from `phyng.campaigns` and `phyng.atlas`. Stable re-exports, but the campaign API may evolve as validation science matures.

7 symbols in `__all__`.

---

### 6. `xendris.benchmarking` — PUBLIC_EXPERIMENTAL

A/B benchmarking suite. Functional and tested but API is still evolving.

```python
from xendris.benchmarking import run_ab_benchmark, BenchmarkEvidenceRegistry, assess_benchmark_excellence
```

33 symbols in `__all__` across 6 submodules.

**Submodule structure:**
- `types` — `ABComparisonResult`, `ABRunSummary`, `BenchmarkSample`, `SystemRunResult`
- `ab_runner` — `run_ab_benchmark`, `summarize_ab_results`
- `ablation` — ablation run types and functions
- `frontier_gap` — frontier gap comparison
- `excellence_gate` — benchmark excellence assessment
- `evidence_registry` — evidence registry management
- `scoring` — `score_result_against_expected`
- `export_jsonl` — JSONL serialization

---

### 7. `xendris.core.runtime` — PUBLIC_EXPERIMENTAL (STUB-DEPENDENT)

Agentic Trust Runtime. Depends on 6 STUB modules from the `experimental-trust-layers` branch.

```python
from xendris.core.runtime import AgenticTrustRuntime, RuntimeRequest, ProviderAdapterSandbox
```

**Stub dependencies:** `xendris.core.local.context`, `xendris.core.algebra.claim_object`, `xendris.core.sectors.sector`, `xendris.core.sectors.transition_engine`, `xendris.core.trust.types`, `xendris.core.boundary.contamination_guard`

**Import status:** WORKS with stubs. Full functionality requires merging `experimental-trust-layers` branch.

10 symbols in `__all__`.

---

### 8. `xendris.core.ledger` — PUBLIC_EXPERIMENTAL

Trust Ledger with append-only hash chain. Functional, JSONL-backed.

```python
from xendris.core.ledger import TrustLedgerWriter, TrustLedgerReader, record_boundary_decision
```

12 symbols in `__all__` including 5 helper `record_*` functions.

---

### 9. `xendris.core.fingerprints` — PUBLIC_EXPERIMENTAL (STUB-DEPENDENT)

Model epistemic fingerprint profiling. Depends on `xendris.core.trust.types` stub.

6 symbols in `__all__`. Full functionality requires merging `experimental-trust-layers` branch.

---

### 10. `xendris.core.router` — PUBLIC_EXPERIMENTAL (STUB-DEPENDENT)

Multi-Model Selector with cost/risk routing. Depends on 3 stub modules.

9 symbols in `__all__`. Full functionality requires merging `experimental-trust-layers` branch.

---

### 11. `xendris.core.representations` — PUBLIC_EXPERIMENTAL (STUB-DEPENDENT)

Representation Consistency Gate. Depends on 5 stub modules.

7 symbols in `__all__`. Full functionality requires merging `experimental-trust-layers` branch.

---

### 12. `xendris.benchmarks` — PUBLIC_EXPERIMENTAL

Benchmark suite registry. Currently contains `false_formality` subpackage.

```python
from xendris.benchmarks import false_formality
```

Placeholder for future benchmark suites. Experimental.

---

### 13. `xendris.models` — PUBLIC_STABLE (AGGREGATOR)

Aggregator for Pydantic models from other modules. Stable because all re-exported symbols are stable.

```python
from xendris.models import Claim, BenchmarkCase, ModelResponse
```

5 symbols in `__all__`.

---

### 14. `xendris.prompts` — EMPTY

Repository for system-prompt strings. No importable symbols yet. Documented placeholder.

**Prefer:** importing prompt strings from their specific module until this namespace is populated.

---

### 15. `xendris.outputs` — EMPTY

Directory marker for generated report artifacts. No importable symbols.

**Do not import.** This is a filesystem directory, not a code module.

---

### 16. `xendris.scripts` — EMPTY

Documented as one-off runners. No importable symbols.

**Do not import.** Scripts should be invoked via `python -m`.

---

## Deprecation policy

### For EMPTY namespaces (`xendris.prompts`, `xendris.outputs`, `xendris.scripts`)

- **v0.3.0:** Add `DeprecationWarning` on import
- **v0.4.0:** Remove from package (move to `xendris.core` if needed)
- **Migration:** Import from specific submodules instead

### For PUBLIC_EXPERIMENTAL modules moving to PUBLIC_STABLE

- Announce in release notes 2 minor versions before promotion
- Preserve backward-compatible imports for 1 minor version after promotion
- Full semver: breaking changes only in major version bumps

---

## Import tests summary

`tests/test_public_imports.py` verifies:

| Test | Coverage |
|------|----------|
| `test_stable_imports` | `xendris`, `frontera_c`, `core.rag`, `core.response_contract`, `models` |
| `test_experimental_imports` | All PUBLIC_EXPERIMENTAL modules (12) |
| `test_empty_namespace_imports` | `prompts`, `outputs`, `scripts` — expect ImportWarning |
| `test_experimental_imports_from_tests` | All `tests/core/` test files import their modules |
| `test_benchmarking_submodules` | All 6 internal submodules of `xendris.benchmarking` |
| `test_ledger_record_functions` | All 5 `record_*` helpers in `xendris.core.ledger` |
