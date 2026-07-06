# Xendris Ablation Benchmark v0.1

Date: 2026-07-04

## Purpose

This benchmark defines a controlled ablation protocol for the Trust Traps
Dataset v0.1. Its purpose is to estimate which Xendris components contribute to
the observed improvement over DeepSeek Base, instead of attributing the full
delta to the complete system as a single opaque unit.

The benchmark is infrastructure for measurement. It does not prove universal
model superiority, general intelligence, production readiness, or domain-wide
correctness.

## Variants

The v0.1 ablation order is:

1. `deepseek_base`
   - Direct DeepSeek execution without Xendris layers.

2. `deepseek_response_contract`
   - DeepSeek with the minimal Xendris Response Contract layer.
   - No final Benchmark Gate exclusion.

3. `deepseek_trust_reasoning`
   - DeepSeek with trust/origin/support reasoning.
   - No final Benchmark Gate exclusion.

4. `deepseek_benchmark_gate`
   - DeepSeek with Benchmark Gate applied.
   - No additional layers beyond those required by the gate.

5. `xendris_full`
   - Current full Xendris + DeepSeek pipeline.

Each variant must produce:

- `system_name`
- `answer`
- `decision`
- `reason`
- `scoring_allowed`
- `latency_ms`
- `estimated_cost_usd`
- `fingerprint`

## Hypotheses

- `deepseek_base` should expose the raw base-model tendency to accept or answer
  trap prompts.
- `deepseek_response_contract` should improve handling of overclaims and
  unsupported premises when those signals are formal enough to be detected.
- `deepseek_trust_reasoning` should improve origin/support reasoning without
  relying on final exclusion behavior.
- `deepseek_benchmark_gate` should reveal how much of the score is explained by
  final admission control.
- `xendris_full` should show the combined effect of the current pipeline.

## Metrics

The summary produced by `summarize_ablation_results` includes:

- mean score per variant;
- win/tie/loss counts relative to `deepseek_base`;
- delta versus `deepseek_base`;
- incremental delta versus the previous variant;
- exclusion rate;
- human-review rate;
- estimated cost;
- average latency;
- cost per valid response;
- breakdown by category.

The implementation also separates rubric score from `valid_correct_count`.
An excluded response may receive rubric credit when the dataset expects
exclusion, but it is not counted as a valid correct answer.

## Correct Interpretation

This benchmark can support narrow statements such as:

> Under Trust Traps Dataset v0.1 and the configured rubric, variant X improved
> admission-control score by Y relative to `deepseek_base`.

It cannot support statements such as:

> Xendris is universally superior to DeepSeek.

or:

> The best ablation variant is generally more truthful across all tasks.

## Limitations

- Trust Traps v0.1 is a closed, purpose-built dataset.
- The dataset was designed around Xendris-style trust and benchmark-admission
  failure modes.
- The sample size is small for broad statistical generalization.
- Results depend on the runner callables, temperature, token limits, provider
  availability, and scoring rubric.
- Dry-run tests use fake callables and do not measure real model behavior.

## No Universal Superiority Warning

Any positive delta in this benchmark is bounded by:

- Trust Traps Dataset v0.1;
- the deterministic scoring rubric;
- the configured variant callables;
- the date and execution environment of the run.

The benchmark must not be cited as evidence of universal cognitive superiority,
general model quality, or broad production safety.

## Dry-Run Execution

Run the ablation infrastructure tests without real API calls:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_ablation_benchmark.py -q
```

Run the focused benchmark validation set:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_ablation_benchmark.py tests/benchmarking/test_trust_traps_dataset.py tests/benchmarking/test_ab_benchmark_runner.py tests/test_xendris_response_contract.py -q
```

## Real Run Execution

A real run should inject provider-backed callables for the five named variants:

```python
from xendris.benchmarking.ablation import run_ablation_benchmark, summarize_ablation_results
from xendris.benchmarking.datasets import load_trust_traps_v0_1

samples = load_trust_traps_v0_1()
variants = {
    "deepseek_base": deepseek_base_callable,
    "deepseek_response_contract": deepseek_response_contract_callable,
    "deepseek_trust_reasoning": deepseek_trust_reasoning_callable,
    "deepseek_benchmark_gate": deepseek_benchmark_gate_callable,
    "xendris_full": xendris_full_callable,
}

results = run_ablation_benchmark(samples, variants)
summary = summarize_ablation_results(results)
```

Real runs must record model, provider, temperature, max tokens, prompt contract,
date, and environment. They must also export raw JSONL/JSON outputs for audit.

## Output Files

The module provides:

- `write_ablation_results_jsonl`
- `write_ablation_results_json`

These helpers serialize raw ablation results only. They do not persist secrets,
API keys, or provider credentials.
