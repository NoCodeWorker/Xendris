# Finitexo Code Matrix v0.10.0 — Cost Frontier Model-Step

## Purpose

This benchmark answers whether a cheaper model plus Xendris Calibrated Runtime is more cost-effective than the immediately superior model without Xendris.

It uses the hard programming n=30 dataset from v0.8.0.

## Variants

Six variants across two providers:

### DeepSeek
- `deepseek_v4_flash_base` — cheapest DeepSeek model, no Xendris
- `deepseek_v4_flash_calibrated_runtime` — same cheap model + Xendris Calibrated Runtime
- `deepseek_v4_pro_base` — next DeepSeek model step, no Xendris

### OpenAI
- `gpt_4_1_nano_base` — cheapest OpenAI model, no Xendris
- `gpt_4_1_nano_calibrated_runtime` — same cheap model + Xendris Calibrated Runtime
- `gpt_4_1_mini_base` — next OpenAI model step, no Xendris

## Expected Attempts

30 tasks x 6 variants = 180

## Cost Frontier Comparisons

### DeepSeek
- A: `flash_calibrated` vs `flash_base` — calibrated gain on same model
- B: `pro_base` vs `flash_base` — next model step, no Xendris
- C: `flash_calibrated` vs `pro_base` — cheap calibrated vs next model

### OpenAI
- A: `nano_calibrated` vs `nano_base` — calibrated gain on same model
- B: `mini_base` vs `nano_base` — next model step, no Xendris
- C: `nano_calibrated` vs `mini_base` — cheap calibrated vs next model

## Efficient Frontier Decisions

For each comparison C (cheap calibrated vs next model):

- `CHEAP_CALIBRATED_DOMINATES_NEXT_MODEL` — calibrated scores higher AND costs less
- `CHEAP_CALIBRATED_HIGHER_QUALITY_HIGHER_COST` — calibrated scores higher but costs more
- `TRADEOFF_CHEAP_CALIBRATED_LOWER_COST_LOWER_SCORE` — calibrated costs less but scores lower
- `NEXT_MODEL_DOMINATES_CHEAP_CALIBRATED` — next model scores higher AND costs less
- `INCONCLUSIVE` — score delta < 0.005 absolute

## Constraints

- No superiority claim is authorized
- No live execution occurs during implementation
- Final interpretation requires a complete run with integrity
- Calibrated runtime variants use the same foundational methodology as v0.9.0 (initial generation → deterministic audit → optional repair/degrade/block → final audit → calibration pass → calibrated final response)
- Calibrated runtime is not a prompt wrapper
