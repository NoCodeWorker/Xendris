# Cheap-to-Frontier Gap Benchmark v0.1

Date: 2026-07-04

## Purpose

This benchmark defines a narrow, reproducible way to estimate whether a cheaper
API model combined with Xendris local control layers can close part of the
measured benchmark gap to a frontier model.

The benchmark is not a general model ranking system. It is a dataset-specific
cost, latency, and score comparison over a concrete evaluation such as Trust
Traps Dataset v0.1.

## Hypothesis

Under datasets designed to measure epistemic control, benchmark admission, and
overclaim resistance, a cheap base model with Xendris may close a substantial
portion of the measured gap to a frontier base model.

This hypothesis must be tested per dataset and provider configuration.

## Required Inputs

Each system is represented by `FrontierGapSystemResult`:

- `system_name`
- `model_name`
- `provider`
- `role`
- `average_score`
- `total_cost_usd`
- `average_latency_ms`
- `scoring_allowed_count`
- `exclusion_rate`
- `human_review_rate`
- `cost_per_valid_answer`

Supported roles are:

- `cheap_base`
- `cheap_xendris`
- `frontier_base`
- `frontier_xendris_optional`

## Gap Closed Formula

If the frontier baseline does not exceed the cheap baseline, the measured gap is
not applicable:

```txt
frontier_base.average_score <= cheap_base.average_score
```

Otherwise:

```txt
gap_closed_ratio =
  (cheap_xendris.average_score - cheap_base.average_score)
  /
  (frontier_base.average_score - cheap_base.average_score)

gap_closed_percent = gap_closed_ratio * 100
```

A value above 100% is permitted, but it must be interpreted only as:

```txt
frontier exceeded on this benchmark only
```

It must not be presented as universal superiority.

## Cost Per Gap Point Formula

For Xendris:

```txt
cost_per_gap_point_xendris =
  (cheap_xendris.total_cost_usd - cheap_base.total_cost_usd)
  /
  max(cheap_xendris.average_score - cheap_base.average_score, epsilon)
```

For the frontier model:

```txt
cost_per_gap_point_frontier =
  (frontier_base.total_cost_usd - cheap_base.total_cost_usd)
  /
  max(frontier_base.average_score - cheap_base.average_score, epsilon)
```

If there is no positive measurable improvement, the implementation reports the
cost-per-gap-point value as not applicable rather than dividing by zero.

## Conceptual Example

Using the currently documented Trust Traps v0.1 values:

```txt
cheap_base_score = 0.10
cheap_xendris_score = 0.865
frontier_base_score = 0.89
```

The measured gap closure is:

```txt
gap_closed =
  (0.865 - 0.10)
  /
  (0.89 - 0.10)
  =
  96.8%
```

Interpretation:

```txt
Under Trust Traps v0.1, Xendris would close 96.8% of the measured gap between
the cheap model and the frontier model, assuming the measured frontier score is
0.89. This does not imply universal superiority or generalization to tasks not
evaluated by the benchmark.
```

## Metrics

The comparison produced by `compute_frontier_gap` includes:

- absolute delta from cheap base to cheap Xendris;
- absolute gap from cheap base to frontier base;
- gap closed ratio;
- gap closed percent;
- cost multiplier for Xendris versus cheap base;
- cost multiplier for frontier versus cheap base;
- cost per gap point for Xendris;
- cost per gap point for frontier;
- latency overhead for Xendris;
- latency overhead for frontier;
- conservative interpretation string.

## No Universal Superiority Warning

This benchmark does not imply universal superiority.

The result is valid only under:

- the selected dataset;
- the selected scoring rubric;
- the selected provider and model settings;
- the measured cost and latency configuration;
- the exact run conditions.

It does not establish that Xendris is generally better than a frontier model, nor
that a cheap model plus Xendris is safer, more truthful, or more capable across
unmeasured domains.

## Methodological Warnings

- Trust Traps v0.1 is a closed benchmark focused on epistemic traps and
  benchmark-admission behavior.
- A frontier model may perform differently on mathematical reasoning,
  instruction following, coding, multimodal tasks, long-context recall, or
  creative generation.
- Cost comparisons depend on provider pricing, token usage, retries, and
  caching.
- Latency comparisons depend on network, provider load, local hardware, and
  orchestration overhead.
- A gap closed above 100% is allowed numerically but must be labelled as
  benchmark-local.

## How To Interpret Results

Acceptable:

```txt
Under Trust Traps v0.1, cheap_xendris closed X% of the measured gap between
cheap_base and frontier_base.
```

Not acceptable:

```txt
Xendris is universally better than frontier models.
```

or:

```txt
The cheap model is now a frontier model.
```

## Dry-Run Execution

Run the focused tests without real API calls:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_frontier_gap_benchmark.py -q
```

Run the requested focused validation set:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/benchmarking/test_frontier_gap_benchmark.py tests/benchmarking/test_ab_benchmark_runner.py tests/benchmarking/test_trust_traps_dataset.py tests/test_xendris_response_contract.py -q
```

## Real Run Workflow

1. Execute the cheap base model on the benchmark.
2. Execute cheap model + Xendris on the same samples.
3. Execute the frontier baseline on the same samples.
4. Optionally execute frontier model + Xendris.
5. Convert each aggregate result into `FrontierGapSystemResult`.
6. Call `compute_frontier_gap`.
7. Export the summary JSON for audit.

## Next Step

Run the same Trust Traps v0.1 benchmark against frontier baselines such as:

- GPT;
- Claude;
- GLM;
- Gemini.

Each provider run must record model version, date, temperature, token limits,
pricing assumptions, and raw outputs.
