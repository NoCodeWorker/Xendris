# Finitexo Code Matrix v0.3.1 - External Dataset Intake

## Why This Exists

Finitexo Code Matrix v0.3 created adversarial benchmark infrastructure, but its
seed dataset remained `SEMI_EXTERNAL_SYNTHETIC`.

v0.3.1 adds a formal intake layer for candidate tasks so future benchmark data
can be classified, validated, and traced without pretending internal tasks are
external.

## Risk Reduced

This phase reduces benchmark-origin risk:

- weak source traceability;
- accidental self-favoring tasks;
- task reuse across benchmark phases;
- unsupported externality claims;
- silent promotion from candidate pool to frozen dataset.

## What It Does Not Resolve

v0.3.1 does not:

- execute providers;
- measure performance;
- prove model or system advantage;
- promote candidates into the frozen dataset;
- provide verified third-party external tasks.

## Origin Types

| Origin | Meaning |
|---|---|
| `EXTERNAL_VERIFIED` | Verifiable external source with strong traceability. |
| `EXTERNAL_ADAPTED` | External source adapted to a local fixture with documented changes. |
| `MUTATED_FIXTURE` | Controlled mutation of a local fixture or mini-repo. |
| `SEMI_EXTERNAL_SYNTHETIC` | Internally authored issue-like task with anti-bias controls. |
| `REJECTED_INSUFFICIENT_ORIGIN` | Rejected due to weak origin, contamination, license, or traceability. |

## Candidate Pool

Created candidates:

```txt
candidate_count: 5
accepted_count: 5
warnings_count: 0
rejected_count: 0
```

Origin distribution:

```txt
MUTATED_FIXTURE: 2
SEMI_EXTERNAL_SYNTHETIC: 3
EXTERNAL_ADAPTED: 0
EXTERNAL_VERIFIED: 0
```

Mean externality score:

```txt
0.468
```

## Externality Score

Externality score is diagnostic only.

It does not authorize:

- performance claims;
- superiority claims;
- dataset promotion;
- provider claims;
- production-readiness claims.

## Candidate Pool Boundary

The candidate pool does not modify the frozen v0.3 seed dataset.

```txt
candidate_pool != frozen_benchmark_dataset
```

Promotion requires a future explicit phase, such as:

```txt
v0.3.2 DATASET_PROMOTION
```

## Artifacts

Generated without provider execution:

```txt
runs/finitexo_code_matrix_v0_3_1_intake/intake_summary.json
runs/finitexo_code_matrix_v0_3_1_intake/intake_report.md
```

## Tests

Executed:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\benchmarking\test_finitexo_code_matrix_v0_3_1_intake.py -q
```

Result:

```txt
14 passed
```

## Provider Execution

```txt
providers_executed: false
```

No `.env` file was read. No secrets were printed. No network calls were made.

## Final Decision

```txt
IMPLEMENTED_SEMI_EXTERNAL_INTAKE_ONLY
```

The repository now has a candidate intake layer with honest origin labels, but
it still does not contain verified third-party external benchmark tasks.

