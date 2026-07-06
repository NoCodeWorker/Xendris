# Generated Output Policy

## Purpose

This policy defines how Xendris handles generated artifacts, runtime outputs,
and benchmark evidence files. It exists to keep source control clean while still
allowing curated benchmark artifacts to be reviewed, audited, and admitted as
evidence.

## Commit-Eligible Generated Artifacts

Generated artifacts may be committed only when they are intentionally curated
and useful for reproducibility or release review.

Commit-eligible artifacts include:

- benchmark summary JSON files that include required metadata;
- benchmark JSONL result files for closed datasets when size is reasonable;
- benchmark reports that include limitations and no-universal-superiority
  warnings;
- Benchmark Excellence outputs;
- Benchmark Evidence Registry outputs;
- release-gate reports;
- small deterministic fixtures required by tests.

Commit-eligible generated artifacts must be stable enough to review in Git and
must not contain secrets, API keys, personal data, provider raw payloads, or
large transient logs.

## Runtime Outputs That Must Stay Local

The following must not be committed:

- ad hoc provider logs;
- raw debugging dumps;
- scratch run folders;
- temporary benchmark outputs;
- local provider transcripts that have not passed the evidence gate;
- generated files containing secrets or environment details;
- caches, builds, virtual environments, frontend build outputs, and test caches.

The `.gitignore` keeps common scratch paths out of Git:

```txt
benchmark_output/
runs/local/
runs/tmp/
runs/**/scratch/
runs/**/*.tmp
runs/**/*.log
```

The `runs/` directory itself is not globally ignored because curated benchmark
summaries, JSONL files, suite audits, and registry files may be committed after
review.

## Canonical Runs Directory Rules

Canonical benchmark artifacts should live under `runs/` using stable names:

```txt
runs/<benchmark_name>_<dataset_version>_<date>.jsonl
runs/<benchmark_name>_<dataset_version>_<date>_summary.json
runs/<benchmark_name>_<dataset_version>_<date>_excellence.json
```

Specialized regenerated artifacts may use a clear subdirectory such as:

```txt
runs/trust_excellence_check/
```

Scratch or exploratory runs must use:

```txt
runs/local/
runs/tmp/
runs/<name>/scratch/
```

and remain ignored.

## Benchmark Report Naming

Benchmark reports should live under `docs/benchmarks/` and use uppercase
descriptive names:

```txt
docs/benchmarks/RUN_<SYSTEM>_<DATASET>_<VERSION>_<DATE>.md
docs/benchmarks/<BENCHMARK_NAME>_V<MAJOR>_<MINOR>.md
```

Reports that describe templates must use `.template` in the filename and must
not be cited as measured evidence.

## Evidence Admission Rule

A generated benchmark artifact can be used as benchmark evidence only if it is
admitted by:

```txt
runs/benchmark_evidence_registry.json
```

The registry is built from the Benchmark Excellence Gate. Admission means the
artifact is structurally ready for careful interpretation. It does not validate
universal superiority, production readiness, scientific truth, or general model
quality.

## Rejected Artifact Rule

Rejected artifacts may remain in the repository as historical records, but they
must not be used as evidence in roadmap decisions, public comparisons, or model
quality claims.

Rejected artifacts may be referenced only when the surrounding text clearly
marks them as rejected, blocked, historical, not admitted, or superseded. Public
documents must not cite rejected artifact paths as if they were current evidence.

Use:

```powershell
.\.venv\Scripts\python.exe scripts\check_benchmark_evidence_citations.py
```

to detect citations to rejected artifacts outside allowed contexts.

## Real Provider Outputs

Real-provider benchmark artifacts may be committed only when all of these are
true:

- no secrets are present;
- provider name and model name are disclosed;
- execution mode is explicit;
- external data disclosure is included;
- pricing assumptions are included;
- limitations are included;
- the artifact passes Benchmark Excellence;
- the artifact is admitted by the Evidence Registry.

Dry-run artifacts must never be described as real provider performance.

## Enforcement

The intended local release flow is:

```powershell
.\.venv\Scripts\python.exe scripts\audit_benchmark_suite_excellence.py --fail-on-blockers
.\.venv\Scripts\python.exe scripts\build_benchmark_evidence_registry.py --require-admitted
.\.venv\Scripts\python.exe scripts\check_benchmark_evidence_citations.py
.\.venv\Scripts\python.exe scripts\release_gate_v0_2_1.py
```

If any step blocks, the release remains blocked until the artifact, report, or
policy violation is fixed.
