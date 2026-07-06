# Xendris API Surface Audit v0.2.1

## Purpose

This skeleton documents the current API boundary for the v0.2.1 release hygiene
work. It does not promote experimental modules into the stable public API.

## Stable Public Imports

The stable public import surface remains intentionally minimal:

```python
import xendris
import xendris.frontera_c
import xendris.core.rag
import xendris.core.response_contract
```

The package/API version remains:

```txt
0.2.0
```

## Experimental Imports

The following modules are operational but experimental unless separately
audited and promoted:

- `xendris.benchmarking`
- `xendris.core.trust`
- `xendris.core.runtime`
- `xendris.core.router`
- `xendris.core.fingerprints`
- `xendris.core.ledger`
- `xendris.core.representations`
- `xendris.core.algebra`
- `xendris.core.boundary`
- `xendris.core.local`
- `xendris.core.sectors`

These modules may be used internally by benchmarks and research workflows, but
their current existence does not make them stable public API.

## Not-Yet-Public Modules

The following areas require future review before public API promotion:

- runtime provider orchestration;
- router and model-selection logic;
- fingerprint structures;
- ledger/audit structures;
- benchmark runners and evidence tools;
- trust reasoning internals;
- frontend product shell APIs;
- formal/Lean artifacts.

## Modules Requiring Future Audit

Before any promotion, each candidate module needs:

- import contract review;
- type and dataclass stability review;
- documentation of supported use cases;
- backward-compatibility policy;
- tests that exercise public imports;
- explicit non-claim language for scientific or benchmark interpretation.

## Explicit Boundary

Runtime, router, fingerprint, ledger, trust, and benchmark modules remain
experimental unless separately promoted by a future API audit. The v0.2.1
release hygiene work does not promote them.

## Release Impact

This document supports release hygiene only. It does not change code behavior,
provider integrations, benchmark scores, or stable package version.
