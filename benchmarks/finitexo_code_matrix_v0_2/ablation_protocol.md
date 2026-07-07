# Finitexo Code Matrix v0.2 - Ablation Protocol

## Objective

Measure whether any observed improvement is attributable to the full Xendris
architecture or to a single superficial intervention such as prompt wording.

## Variants

| Variant | Measures |
|---|---|
| base_agent | Bare model behavior |
| base_agent_with_contract_prompt | Effect of adding the response contract to the prompt |
| base_agent_with_scoring_awareness | Effect of showing scoring criteria |
| xendris_without_calibration | Effect of removing calibration |
| xendris_without_evidence_gate | Effect of removing evidence gate |
| xendris_without_claim_gate | Effect of removing claim gate |
| xendris_agent | Normal Xendris path |
| xendris_calibrated_agent | Calibrated Xendris path |

Unavailable variants must be reported as `SKIPPED_VARIANT_NOT_AVAILABLE`, not
hidden.

## Required Questions

- Does the signal remain when pieces are removed?
- Which piece appears to contribute most?
- Is there evidence that the result is only prompt engineering?
- Is there evidence of scoring overfit?
