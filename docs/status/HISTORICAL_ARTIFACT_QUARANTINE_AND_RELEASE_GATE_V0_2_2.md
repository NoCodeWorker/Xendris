# Historical Artifact Quarantine and Release Gate v0.2.2

Date: 2026-07-06

## Purpose

Implement the Xendris v0.2.2 historical artifact quarantine layer and clean
release gate. The goal is to preserve rejected benchmark artifacts for
traceability without allowing them to contaminate active evidence or block
release merely by existing.

## Files Created

- `docs/policies/HISTORICAL_ARTIFACT_QUARANTINE_POLICY.md`
- `docs/benchmarks/HISTORICAL_REJECTED_ARTIFACTS.md`
- `scripts/release_gate_v0_2_2.py`
- `tests/benchmarking/test_historical_artifact_quarantine.py`
- `docs/status/HISTORICAL_ARTIFACT_QUARANTINE_AND_RELEASE_GATE_V0_2_2.md`

## Files Modified

- `scripts/audit_benchmark_suite_excellence.py`
- `phyng/api.py`
- `runs/benchmark_suite_excellence_audit.json`
- `docs/benchmarks/BENCHMARK_SUITE_EXCELLENCE_AUDIT.md`
- `runs/benchmark_evidence_registry.json`
- `docs/benchmarks/BENCHMARK_EVIDENCE_REGISTRY.md`

The `phyng/api.py` change is whitespace-only: a trailing-whitespace line and a
final blank line at EOF were removed.

## Artifacts Quarantined

The following rejected summaries are listed in the quarantine manifest:

| Rejected summary | Reason | Canonical admitted replacement |
|---|---|---|
| `runs/deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_summary.json` | `dry_run_report_claims_real_provider_performance` | `runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_summary.json` |
| `runs/deepseek_vs_xendris_trust_traps_v0_1_2026_07_04_v2_summary.json` | `missing_dataset_hash` | `runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_summary.json` |
| `runs/deepseek_vs_xendris_trust_traps_v0_1_summary.json` | `dry_run_report_claims_real_provider_performance` | `runs/trust_excellence_check/deepseek_vs_xendris_trust_traps_v0_1_summary.json` |

Allowed reference status:

```txt
historical only
not admitted evidence
not valid for public claims
```

## Active Evidence Separation

`scripts/audit_benchmark_suite_excellence.py` now loads:

```txt
docs/benchmarks/HISTORICAL_REJECTED_ARTIFACTS.md
```

and marks matching blocked summaries as:

```txt
is_quarantined_historical: true
```

Quarantined historical rejected artifacts are still recorded, but no longer
count as active release blockers.

## Evidence Registry Behavior

The Benchmark Evidence Registry still reports:

```txt
BENCHMARK_EVIDENCE_REGISTRY total=5 admitted=2 rejected=3
```

Rejected historical artifacts do not disappear. They remain visible as rejected
records and must not be used as admitted evidence.

## Commands Run

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_historical_artifact_quarantine.py -q
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_benchmark_evidence_citation_checker.py -q
.\.venv\Scripts\python.exe scripts\check_benchmark_evidence_citations.py
.\.venv\Scripts\python.exe scripts\audit_benchmark_suite_excellence.py --fail-on-blockers
.\.venv\Scripts\python.exe scripts\build_benchmark_evidence_registry.py --require-admitted
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_2.py
.\.venv\Scripts\python.exe -m pytest -q
git diff --check
git status --short
```

## Observed Results

Historical quarantine tests:

```txt
6 passed
```

Evidence citation checker tests:

```txt
7 passed
```

Evidence citation checker:

```txt
BENCHMARK_EVIDENCE_CITATIONS rejected=3 violations=0
```

Benchmark Suite Excellence Audit:

```txt
BENCHMARK_SUITE_EXCELLENCE summaries=5 ready=2 blocked=0 quarantined=3
```

Benchmark Evidence Registry:

```txt
BENCHMARK_EVIDENCE_REGISTRY total=5 admitted=2 rejected=3
```

Release gate:

```txt
XENDRIS_RELEASE_GATE_V0_2_2
status=BLOCKED
historical_rejected_artifacts=3
```

Full Python suite:

```txt
1446 passed, 4 warnings
```

Diff check:

```txt
git diff --check: PASS
```

Only CRLF working-copy warnings were reported by Git. No whitespace errors
remain in `phyng/api.py`.

## Release Gate Interpretation

The release gate now separates:

- active blockers;
- quarantined historical rejected artifacts;
- admitted benchmark evidence;
- rejected non-evidence artifacts;
- dirty working tree status.

The 3 historical rejected summaries no longer block release merely by existing.

## Remaining Blockers

The current release gate remains blocked because the working tree is not clean.
This is intentional. A tag should not be created until the release-relevant
changes are staged/committed or unrelated changes are separated.

Current known release blocker:

```txt
working_tree_clean: BLOCKED
```

## Tag Readiness

```txt
tag_ready: false
reason: working_tree_not_clean
```

Historical rejected artifacts are quarantined and no longer active blockers.
The evidence registry still records them as rejected.

## Next Recommended Step

Review the working tree, separate unrelated frontend/runtime changes from the
release hygiene changes, commit the intended v0.2.2 release-hygiene set, and
rerun:

```powershell
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_2.py
```

Only after the gate reports `PASS` should a release tag be considered.

## Non-Claims

This work does not:

- change benchmark scores;
- create new benchmark results;
- run real providers;
- claim universal superiority;
- claim real-provider performance;
- promote experimental v0.3.x-v1.1 modules into stable API.
