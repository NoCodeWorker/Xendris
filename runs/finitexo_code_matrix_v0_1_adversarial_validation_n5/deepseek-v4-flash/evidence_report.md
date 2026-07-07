# Agentic Programming Benchmark Evidence Report

## Evidence Decision

Decision: INTERPRETABLE

## Execution Identity

- Providers: ['deepseek']
- Transport: direct
- Transports: ['direct']
- Provider source: variant_name_prefix
- Transport source: explicit_provider_default

## Model Identity

- Resolved: True
- Provider: deepseek
- Model alias: deepseek-v4-flash
- Model ID: deepseek-v4-flash
- API surface: chat_completions
- Supports reasoning: False
- Supports structured output: True

## Interpretation Admissibility

- Provider metadata sufficient: True
- Transport metadata sufficient: True
- Model metadata sufficient: True
- Admissible: True
- Limitations: (none)

## Evidence Contract

- Contract version: 0.1
- Identity resolved: True
- Provenance recorded: True
- Model identity resolved: True
- Interpretation admissible: True
- Scoring complete: True
- Decision: INTERPRETABLE
- Limitations: (none)

## Score Summary

- Benchmark name: Agentic Programming Reliability
- Dataset: Xendris Agentic Programming v0.1
- Dataset size: 5
- Execution mode: live
- Provider mode: real
- Variants: ['deepseek_base_agent', 'deepseek_xendris_agent', 'deepseek_xendris_calibrated_agent']

### Scores by Variant

- **deepseek_base_agent**: total_score=0.74, pass_rate=0.4
- **deepseek_xendris_agent**: total_score=0.93, pass_rate=0.8
- **deepseek_xendris_calibrated_agent**: total_score=0.85, pass_rate=0.6

## Final Interpretation

This benchmark run is interpretable as evidence because execution identity, provenance, model identity, interpretation admissibility, and scoring completeness are all satisfied.
