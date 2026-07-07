# Finitexo Code Matrix v0.2 Plan

## Objective

Finitexo Code Matrix v0.2 introduces an anti-ad-hoc validation layer for the
agentic programming benchmark work. Its purpose is to try to refute or weaken
the repeated v0.1 signal before any stronger interpretation is allowed.

## Problem Addressed

The v0.1 budget and adversarial runs produced a repeated signal under small
controlled samples, but that signal may still be explained by:

- dataset alignment with the Xendris control path;
- scoring that rewards contract obedience more than programming ability;
- small tasks;
- prompt-specific effects;
- a weak baseline;
- insufficiently blind evaluation.

v0.2 therefore starts by adding dataset freezing, task hashes, scoring contract
hashes, explicit anti-ad-hoc checks, and ablation reporting.

## Why It Does Not Authorize Superiority Claims

The v0.2 infrastructure does not prove broad programming quality. Small runs
remain budget validation or signal replication only. Public or comparative
claims require larger samples, valid hashes, complete evidence, and passing
interpretation gates.

Forbidden claims include:

- Xendris is superior.
- Xendris programs better in general.
- Xendris is production-ready.
- Results generalize to unmeasured tasks, models, or providers.

## Artifacts Created

- `benchmarks/finitexo_code_matrix_v0_2/README.md`
- `benchmarks/finitexo_code_matrix_v0_2/dataset_manifest.json`
- `benchmarks/finitexo_code_matrix_v0_2/scoring_contract.md`
- `benchmarks/finitexo_code_matrix_v0_2/anti_ad_hoc_protocol.md`
- `benchmarks/finitexo_code_matrix_v0_2/ablation_protocol.md`
- `benchmarks/finitexo_code_matrix_v0_2/interpretation_policy.md`
- `benchmarks/finitexo_code_matrix_v0_2/tasks/`
- `benchmarks/finitexo_code_matrix_v0_2/runners/`
- `benchmarks/finitexo_code_matrix_v0_2/evaluators/`
- `benchmarks/finitexo_code_matrix_v0_2/reports/REPORT_TEMPLATE.md`

## Small Dry Run

```powershell
.\.venv\Scripts\python.exe benchmarks\finitexo_code_matrix_v0_2\runners\run_matrix_v0_2.py --dry-run --samples 5 --output-dir runs\finitexo_code_matrix_v0_2_dry_run
```

## Ablation Dry Run

```powershell
.\.venv\Scripts\python.exe benchmarks\finitexo_code_matrix_v0_2\runners\run_ablation_v0_2.py --dry-run --samples 5 --output-dir runs\finitexo_code_matrix_v0_2_ablation_dry_run
```

## Scaling Path

| Stage | Sample count | Interpretation |
|---|---:|---|
| n=5 | 5 | Budget validation only |
| n=10 | 10 | Budget validation only |
| n=20 | 20 | Internal strong-signal discussion if gates pass |
| n=50 | 50 | Preliminary comparative discussion if gates pass |
| n=100 | 100 | Public claims may be considered only with all gates passing |

## Conditions for Future Claims

Future claims require:

- valid dataset hash;
- valid task hashes;
- valid scoring contract hash;
- anti-ad-hoc decision not blocked;
- evidence contract interpretable;
- no forbidden overclaim wording;
- sufficient sample threshold;
- provider/model/transport disclosure;
- cost and latency disclosure;
- ablation results reported, including skipped variants.

## Current Decision

`IMPLEMENTED_INFRASTRUCTURE`

The v0.2 anti-ad-hoc infrastructure is prepared for dry-run validation. Live
provider execution is intentionally not wired in this first pass.
