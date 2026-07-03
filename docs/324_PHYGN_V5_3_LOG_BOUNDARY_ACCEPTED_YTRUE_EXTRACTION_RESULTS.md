# Phygn v5.3 - LOG_BOUNDARY Accepted y_true Extraction Results

Date: 2026-07-02

## Completion Status

Final campaign status:

```txt
LOG_BOUNDARY_YTRUE_THRESHOLD_REACHED
```

Interpretation:

```txt
Strict y_true extraction was executed for Hackermueller 2004 FIG. 2.
Four visibility values were accepted as dimensionless-fraction y_true records with PASS_WITH_LIMITATIONS QC.
Heating power P was used only as an experimental condition.
No PredictiveGain was computed.
No physical claim was upgraded.
Frontera C remains unvalidated.
```

## Metrics

| Metric | Value |
|---|---:|
| Observed measurement candidates loaded | 1 |
| y_true candidates evaluated | 4 |
| Accepted y_true records | 4 |
| Rejected y_true records | 0 |
| Threshold reached | true |
| PredictiveGain computed | 0 |
| Physical claims created | 0 |

## Accepted y_true Records

| y_true_id | heating_power_W | original V | visibility_fraction | unit | QC |
|---|---:|---:|---:|---|---|
| `YTRUE-v5_3-LOG_BOUNDARY-HACKERMUELLER-FIG2-01` | 0.0 W | 47% | 0.47 | dimensionless_fraction | `PASS_WITH_LIMITATIONS` |
| `YTRUE-v5_3-LOG_BOUNDARY-HACKERMUELLER-FIG2-02` | 3.0 W | 29% | 0.29 | dimensionless_fraction | `PASS_WITH_LIMITATIONS` |
| `YTRUE-v5_3-LOG_BOUNDARY-HACKERMUELLER-FIG2-03` | 6.0 W | 7% | 0.07 | dimensionless_fraction | `PASS_WITH_LIMITATIONS` |
| `YTRUE-v5_3-LOG_BOUNDARY-HACKERMUELLER-FIG2-04` | 10.5 W | 0% | 0.00 | dimensionless_fraction | `PASS_WITH_LIMITATIONS` |

## Provenance

```txt
source_id: SRC-HACKERMUELLER-2004-THERMAL-EMISSION-DECOHERENCE
title: Decoherence of matter waves by thermal emission of radiation
authority: Nature 427, 711-714 (2004); arXiv/local PDF first page
year: 2004
external_identity: quant-ph/0402146
local_pdf_path: data\real_sources\pdfs\Hackermueller_2004_Thermal_Emission_Decoherence.pdf
local_pdf_hash: f1f38ac71b1a03102e1b09937eab5f855e0cd5b6a02ace2f5bb83d2a8c217a24
page_number: 2
figure_id: FIG. 2
```

## Created Artifacts

```txt
data/frontera_c/ytrue/log_boundary_ytrue_candidates_v5_3.json
data/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.json
data/frontera_c/ytrue/log_boundary_rejected_ytrue_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_extraction_audit_trail_v5_3.json
data/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.json
data/frontera_c/ytrue/log_boundary_v5_3_next_gate_decision.json
reports/frontera_c/ytrue/log_boundary_ytrue_candidates_v5_3.md
reports/frontera_c/ytrue/log_boundary_accepted_ytrue_v5_3.md
reports/frontera_c/ytrue/log_boundary_rejected_ytrue_v5_3.md
reports/frontera_c/ytrue/log_boundary_ytrue_extraction_audit_trail_v5_3.md
reports/frontera_c/ytrue/log_boundary_ytrue_dataset_v5_3.md
reports/frontera_c/ytrue/log_boundary_v5_3_next_gate_decision.md
reports/campaigns/FRONTERA-C-LOG-BOUNDARY-YTRUE-EXTRACTION-v5_3.md
```

## Next Gate

```txt
v5.4 - Prediction Alignment & Minimal Benchmark
```

v5.4 permitted: `True`

## Blocked Claims

- LOG_BOUNDARY is validated.
- LOG_BOUNDARY has PredictiveGain.
- Frontera C is validated.
- The invariant is empirically confirmed.
- Accepted y_true alone validates anything.
- Observable location equals y_true.

## Allowed Claims

- Strict y_true extraction was attempted for Hackermueller 2004 FIG. 2.
- Four visibility values were accepted as y_true records under strict provenance and PASS_WITH_LIMITATIONS QC.
- Heating power was used as an experimental condition.
- v5.4 is permitted because accepted_ytrue_count >= 3.

Final discipline:

```txt
No PredictiveGain in v5.3.
Accepted y_true permits benchmarking; it does not validate Frontera C.
```
