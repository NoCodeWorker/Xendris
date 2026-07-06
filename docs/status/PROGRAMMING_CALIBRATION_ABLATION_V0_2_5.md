# Programming Calibration Ablation v0.2.5

## Objective

Create a dry-run experimental ablation that compares:

1. `deepseek_base`
2. `xendris_uncalibrated`
3. `xendris_calibrated`

on Programming Reliability v0.1 without calling real providers and without
rewriting historical benchmark artifacts.

## Motivation

Programming Reliability v0.1 showed that Xendris can help and harm depending on
category:

- `edge_cases`: Xendris helped.
- `api_contracts`: Xendris over-intervened.
- `unit_tests`: Xendris over-intervened.

The calibration ablation exists to measure whether experimental
benchmark-aware intervention policy reduces that overengineering harm while
preserving useful edge-case behavior.

## Benchmark Design

The ablation is dry-run only.

It runs deterministic local variants:

| Variant | Meaning |
|---|---|
| `deepseek_base` | Baseline mock behavior. |
| `xendris_uncalibrated` | Xendris-style behavior with known overengineering failure modes. |
| `xendris_calibrated` | Xendris behavior with `ProgrammingInterventionPolicy` enabled. |

## Output Paths

Default output directory:

```txt
runs/programming_calibration_ablation_v0_2_5/
```

Generated files:

```txt
summary.json
results.jsonl
report.md
```

These are separate from historical Programming Reliability artifacts.

## Command

```powershell
.\.venv\Scripts\python.exe scripts\run_programming_calibration_ablation.py
```

## Evidence Gate

The ablation uses a specific experimental interpretation gate:

```txt
assess_programming_calibration_ablation(...)
```

Possible status:

- `ADMITTED_EXPERIMENTAL_ANALYSIS`
- `BLOCKED_FOR_INTERPRETATION`

This status does not imply stable public superiority.

## Required Interpretation Questions

The report must answer from computed artifacts only:

- Did calibration improve `api_contracts` vs uncalibrated?
- Did calibration improve `unit_tests` vs uncalibrated?
- Did calibration preserve `edge_cases`?
- Did calibration reduce import-related failures?
- Did calibration reduce overengineering-style failures?

## Observed Results

Generated artifacts:

```txt
runs/programming_calibration_ablation_v0_2_5/summary.json
runs/programming_calibration_ablation_v0_2_5/results.jsonl
runs/programming_calibration_ablation_v0_2_5/report.md
```

Observed dry-run scores:

| Variant | Score |
|---|---:|
| `deepseek_base` | 0.900 |
| `xendris_uncalibrated` | 0.650 |
| `xendris_calibrated` | 1.000 |

Observed deltas:

| Delta | Value |
|---|---:|
| calibrated vs uncalibrated | +0.350 |
| calibrated vs base | +0.100 |
| uncalibrated vs base | -0.250 |

Category-level answers from the generated summary:

| Question | Computed answer |
|---|---|
| Did calibration improve `api_contracts` vs uncalibrated? | yes |
| Did calibration improve `unit_tests` vs uncalibrated? | yes |
| Did calibration preserve `edge_cases`? | yes |
| Did calibration reduce import-related failures? | yes |
| Did calibration reduce overengineering-style failures? | yes |

Calibration metrics for `xendris_calibrated`:

| Metric | Value |
|---|---:|
| calibrated samples | 100 |
| minimal intervention samples | 75 |
| moderate intervention samples | 25 |
| strong intervention samples | 0 |
| import-restricted samples | 100 |
| signature-preservation-required samples | 100 |
| test-framework-import-restricted samples | 100 |
| security false-positive warning samples | 10 |

Evidence status:

```txt
ADMITTED_EXPERIMENTAL_ANALYSIS
```

This is experimental dry-run analysis only.

## Limitations

- Dry-run only.
- Mock provider only.
- Closed Programming Reliability v0.1 dataset.
- No real-provider performance is measured.
- No universal superiority is implied.
- No global programming improvement is claimed.
- Calibration remains experimental and is not promoted to stable public API.

## Historical Artifact Policy

Historical benchmark summaries are not overwritten by this ablation.

The ablation writes to its own output directory and must not replace admitted
Programming Reliability summaries.

## Next Recommended Step

Run the dry-run ablation, inspect category-level deltas, and only then decide
whether a real-provider calibration experiment is worth the external API cost
and disclosure risk.
