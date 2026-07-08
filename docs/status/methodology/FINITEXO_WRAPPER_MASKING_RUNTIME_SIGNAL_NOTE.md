# Finitexo Methodology Note — Wrapper Masking Runtime Signal

## Purpose

This note records a methodological risk discovered during the Finitexo Code Matrix progression:
a wrapper-only approximation of Xendris almost led to the false impression that Xendris did not help on hard programming tasks, when the foundational Runtime / Calibrated Runtime methodology had not yet been measured.

## Context

- v0.7.0 measured paired wrapper lift on n=30.
- v0.8.1 measured hard paired wrapper lift on the hard programming n=30 dataset.
- v0.8.1 showed weak or negative wrapper signal, especially for DeepSeek.
- v0.9.0 restored the foundational methodology by separating:
  - base
  - wrapper
  - runtime
  - calibrated_runtime

## Key distinction

Wrapper is not Runtime.
Runtime is not Calibrated Runtime.
Wrapper results must not be generalized to Runtime or Calibrated Runtime.
A wrapper-only benchmark can mask a runtime signal.

## Evidence from v0.8.1

DeepSeek hard wrapper result:
- deepseek_base mean_score: 0.8141033333333333
- deepseek_xendris mean_score: 0.8044933333333333
- deepseek_xendris_minus_base: -0.00961

OpenAI hard wrapper result:
- openai_base mean_score: 0.865373333333333
- openai_xendris mean_score: 0.869223333333333
- openai_xendris_minus_base: +0.00385

Interpretation:
v0.8.1 made the wrapper appear weak or negative, but it did not evaluate the foundational Xendris Runtime or Calibrated Runtime.

## Evidence from v0.9.0 partial run

v0.9.0 live_20260708_01 was partial:

- final_decision: RUNTIME_LIFT_PARTIAL_DIAGNOSTIC_ONLY
- total_expected: 240
- total_attempted: 240
- total_completed: 239
- total_failed: 1
- runtime_traces: 119 / 120
- calibration_traces: 60 / 60
- evidence_integrity_ready: false
- error: OpenAI runtime timeout on task finitexo_v0_8_0_ec_004

Therefore:
The v0.9.0 numbers are diagnostic partial signals only and must not be promoted to final validated claims.

## v0.9.0 partial score signal

DeepSeek:
- deepseek_base mean: 0.80449
- deepseek_wrapper mean: 0.807053
- deepseek_runtime mean: 0.843573
- deepseek_calibrated_runtime mean: 0.872433

OpenAI:
- openai_base mean: 0.86345
- openai_wrapper mean: 0.870503
- openai_runtime mean: 0.864097
- openai_calibrated_runtime mean: 0.90322

## v0.9.0 partial lift signal

DeepSeek:
- deepseek_wrapper_vs_base_mean_lift: +0.002563
- deepseek_runtime_vs_base_mean_lift: +0.039083
- deepseek_calibrated_runtime_vs_base_mean_lift: +0.067943
- deepseek_runtime_vs_wrapper_mean_lift: +0.03652
- deepseek_calibrated_runtime_vs_wrapper_mean_lift: +0.06538
- deepseek_calibrated_runtime_vs_runtime_mean_lift: +0.02886

OpenAI:
- openai_wrapper_vs_base_mean_lift: +0.007053
- openai_runtime_vs_base_mean_lift: +0.000647
- openai_calibrated_runtime_vs_base_mean_lift: +0.03977
- openai_runtime_vs_wrapper_mean_lift: -0.006407
- openai_calibrated_runtime_vs_wrapper_mean_lift: +0.032717
- openai_calibrated_runtime_vs_runtime_mean_lift: +0.039123

## Methodological interpretation

The partial v0.9.0 signal suggests:
- wrapper effects were marginal;
- Runtime produced a stronger signal for DeepSeek;
- Calibrated Runtime produced the strongest signal for both DeepSeek and OpenAI;
- the wrapper-only line could have hidden the actual Runtime / Calibrated Runtime signal.

But this is not yet final evidence because v0.9.0 live_20260708_01 was partial.

## Blocked claims

- "v0.8.1 proves Xendris does not help hard programming."
- "v0.8.1 refutes Xendris Runtime."
- "Wrapper results generalize to Runtime."
- "Wrapper results generalize to Calibrated Runtime."
- "v0.9.0 live_20260708_01 proves Runtime superiority."
- "v0.9.0 live_20260708_01 proves Calibrated Runtime superiority."
- "Xendris is universally superior."
- "Xendris has statistical superiority."
- "Xendris is production ready."

## Allowed claims

- "v0.8.1 measured hard wrapper behavior, not Runtime."
- "v0.9.0 introduced base, wrapper, runtime, and calibrated_runtime as distinct variants."
- "v0.9.0 live_20260708_01 produced a partial diagnostic signal in which Runtime and Calibrated Runtime outperformed wrapper for DeepSeek, and Calibrated Runtime outperformed wrapper for OpenAI."
- "The partial v0.9.0 run requires a complete rerun before final interpretation."

## Corrective action

Run v0.9.0 again with a fresh suffix, for example:

FINITEXO_RUNTIME_LIFT_RUN_ID_SUFFIX=live_20260708_02

Required completion criteria:

- total_expected: 240
- total_completed: 240
- total_failed: 0
- runtime_traces: 120
- calibration_traces: 60
- errors_count: 0
- evidence_integrity_ready: true
- final_decision: RUNTIME_LIFT_COMPLETED_DIAGNOSTIC_ONLY

## Permanent methodological rule

Any future benchmark or interpretation must preserve the distinction:

base != wrapper != runtime != calibrated_runtime

A benchmark that measures wrapper must not be interpreted as measuring Runtime.
A benchmark that measures Runtime must not be interpreted as measuring Calibrated Runtime.
A benchmark that lacks required runtime/calibration traces must be blocked from runtime/calibrated runtime claims.

## Final decision

WRAPPER_MASKING_RUNTIME_SIGNAL_RECORDED
