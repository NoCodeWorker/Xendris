# Finitexo Code Matrix v0.1 — Budget Mini-Validation

## Overview

This is a budget mini-validation phase following the initial smoke (n=1). It tests whether the initial signal repeats on a slightly larger sample (n=3 per variant, 9 per provider).

- **Dataset**: Xendris Agentic Programming v0.1 (closed synthetic)
- **Execution mode**: live (direct provider API)
- **Max iterations**: 1 (no retries)
- **Budget cap**: $1.00 per provider (total cap: $2.00)

## Models and Variants

| Model | Variant | Score | Pass Rate | Est. Cost | Verified Successes | Cost/Verified | Evidence Decision | Benchmark Gate | Limitations |
|---|---|---|---|---|---|---|---|---|---|
| DeepSeek V4 Flash | deepseek_base_agent | 0.5167 | 0.0 | $0.000372 | 0 | N/A | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION | none |
| DeepSeek V4 Flash | deepseek_xendris_agent | 1.0000 | 1.0 | $0.000599 | 3 | $0.000200 | INTERPRETABLE | READY_FOR_INTERPRETATION | none |
| DeepSeek V4 Flash | deepseek_xendris_calibrated_agent | 1.0000 | 1.0 | $0.000728 | 3 | $0.000243 | INTERPRETABLE | READY_FOR_INTERPRETATION | none |
| **DeepSeek V4 Flash subtotal** | | | | **$0.001698** | **6** | **$0.000283** | | | |
| GPT-4.1 nano | openai_base_agent | 0.5167 | 0.0 | $0.000112 | 0 | N/A | INTERPRETABLE | BLOCKED_FOR_INTERPRETATION | none |
| GPT-4.1 nano | openai_xendris_agent | 1.0000 | 1.0 | $0.000160 | 3 | $0.000053 | INTERPRETABLE | READY_FOR_INTERPRETATION | none |
| GPT-4.1 nano | openai_xendris_calibrated_agent | 1.0000 | 1.0 | $0.000159 | 3 | $0.000053 | INTERPRETABLE | READY_FOR_INTERPRETATION | none |
| **GPT-4.1 nano subtotal** | | | | **$0.000431** | **6** | **$0.000072** | | | |
| DeepSeek Reasoner | — | — | — | — | — | — | — | — | SKIPPED_MODEL_NOT_AVAILABLE |
| GPT-5.5 | — | — | — | — | — | — | — | — | SKIPPED_BUDGET_CONSTRAINT |
| **Total** | | | | **$0.002129** | **12** | **$0.000177** | | | |

## Commercial Metrics (Provider Level)

| Metric | DeepSeek V4 Flash | GPT-4.1 nano |
|---|---|---|
| Task success rate | 0.6667 | 0.6667 |
| Verified successful count | 6 | 6 |
| Visible test pass rate | 0.7778 | 0.7778 |
| Hidden test pass rate | 0.6667 | 0.6667 |
| API preservation rate | 1.0 | 1.0 |
| Forbidden file touch rate | 0.0 | 0.0 |
| False success claim rate | 0.0 | 0.0 |
| Minimal patch rate | 1.0 | 1.0 |
| Security clean rate | 1.0 | 1.0 |
| Avg latency (ms) | 306.31 | 1362.88 |
| Total estimated cost | $0.001698 | $0.000431 |
| Cost / verified task | $0.000283 | $0.000072 |

## Evidence Layer Validation

All six evidence layers were generated correctly and identically for both providers:

- **execution_provenance**: resolved (provider_source: variant_name_prefix, transport_source: explicit_provider_default)
- **model_identity**: resolved (provider, model_alias, model_id, api_surface all present)
- **interpretation_admissibility**: admissible (all metadata sufficient, no limitations)
- **evidence_contract**: INTERPRETABLE (identity_resolved, provenance_recorded, model_identity_resolved, interpretation_admissible, scoring_complete all True)
- **evidence_report.md**: written to each model subdirectory

## Gate Analysis

### Evidence Contract vs. Benchmark Gate

The **evidence_contract** decision is `INTERPRETABLE` for both providers. This means the evidence layers (identity, provenance, model identity, interpretation, scoring) all passed validation — the methodology is sound and the results are admissible as evidence.

The **benchmark-level gate** is `BLOCKED_FOR_INTERPRETATION` for both providers. This is because at least one variant (`base_agent`) scored below the excellence gate threshold (pass_rate=0.0). The blocked variant is retained for comparison only and is not admitted as positive evidence.

This distinction is intentional: the evidence contract validates the *process* (methodology); the benchmark gate evaluates the *outcome* (performance). A valid methodology can produce performance that does not clear the gate.

### Variant-Level Gates

| Variant | Gate | Reason |
|---|---|---|
| deepseek_base_agent | BLOCKED_FOR_INTERPRETATION | score=0.5167, pass_rate=0.0 |
| deepseek_xendris_agent | READY_FOR_INTERPRETATION | score=1.0, pass_rate=1.0 |
| deepseek_xendris_calibrated_agent | READY_FOR_INTERPRETATION | score=1.0, pass_rate=1.0 |
| openai_base_agent | BLOCKED_FOR_INTERPRETATION | score=0.5167, pass_rate=0.0 |
| openai_xendris_agent | READY_FOR_INTERPRETATION | score=1.0, pass_rate=1.0 |
| openai_xendris_calibrated_agent | READY_FOR_INTERPRETATION | score=1.0, pass_rate=1.0 |

## Signal Analysis: Smoke vs. Mini (n=1 → n=3)

| Metric | Smoke (n=1) | Budget Mini (n=3) | Change |
|---|---|---|---|
| DeepSeek base_agent score | 0.65 | 0.5167 | ↓ |
| DeepSeek xendris_agent score | 1.0 | 1.0 | — |
| DeepSeek xendris_calibrated score | 1.0 | 1.0 | — |
| GPT base_agent score | 0.65 | 0.5167 | ↓ |
| GPT xendris_agent score | 1.0 | 1.0 | — |
| GPT xendris_calibrated score | 1.0 | 1.0 | — |
| Total cost | ~$0.001 | ~$0.002 | — |

**Signal repeated**: Yes. Both Xendris variants (xendris_agent, xendris_calibrated_agent) achieved perfect scores (1.0) on both providers at n=3, replicating the n=1 smoke result. The base_agent score dropped from 0.65 to 0.5167, reflecting the hidden test pass weight (0.35) distributed across more samples.

## Skipped Models

| Model | Reason |
|---|---|
| DeepSeek Reasoner | SKIPPED_MODEL_NOT_AVAILABLE — model ID not in codebase; CLI validation (`scripts/run_agentic_programming_benchmark.py:1133-1134`) restricts `deepseek` provider to `deepseek-v4-flash` only. |
| GPT-5.5 | SKIPPED_BUDGET_CONSTRAINT — reserved for a later single-task premium reference baseline. |

## Budget Compliance

| Provider | Budget Cap | Actual Spend | Headroom |
|---|---|---|---|
| DeepSeek V4 Flash | $1.00 | $0.001698 | $0.998302 |
| GPT-4.1 nano | $1.00 | $0.000431 | $0.999569 |
| **Total** | **$2.00** | **$0.002129** | **$1.997871** |

No budget risk exceeded at any point. Actual spend is 0.1% of the hard target.

## Limitations

- n=3 per variant is still not statistically strong. Results cannot be generalized.
- The dataset is closed synthetic (20 samples total). It does not represent real-world programming diversity.
- Results are specific to the Agentic Programming v0.1 benchmark and should not be generalized to other benchmarks or capabilities.
- No comparison against Claude, Codex, Kimi, GLM, or any non-measured model is included.
- Cost estimates are based on token counts from API responses using published per-token pricing. Actual costs may vary.
- Average latency differs significantly between providers (306ms vs 1363ms) but this is not controlled — it reflects API endpoint infrastructure, not model capability.

## Conclusion (Budget Mini-Validation Only)

1. The initial smoke signal **repeated** at n=3: both Xendris variants scored 1.0 on both DeepSeek V4 Flash and GPT-4.1 nano.
2. Base agent scores dropped from 0.65 (n=1) to 0.5167 (n=3), consistent with the scoring formula's 35% hidden-test weight across more samples.
3. All evidence layers validated cleanly on both providers. No layer is a stub.
4. Both benchmarks blocked at the benchmark level due to base_agent underperformance — this is expected and correct behavior.
5. Total cost of ~$0.002 is negligible relative to the $2.00 budget.
6. No superiority claim is made or implied. n=3 is insufficient for any generalizable conclusion.
