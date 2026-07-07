# Finitexo Code Matrix v0.3.1 - Source Policy

## External Origin

An external origin means the task is based on a source independent of this
benchmark and has enough traceability to audit where the task came from.

## Adapted External Origin

An adapted external origin means an external source was simplified or adapted
to a local fixture. The adaptation must document what changed and why.

## Semi-Synthetic Origin

A semi-synthetic origin means the task was created internally but shaped to
look like ordinary software maintenance work. It must not be presented as
external evidence.

## Mutated Fixture Origin

A mutated fixture origin means the task is generated from a known local fixture
or mini-repository by applying a controlled mutation. The base fixture and
mutation intent must be documented.

## Rejected Sources

A source must be rejected when origin, traceability, license, contamination,
task contract, or hidden-test intent is not sufficient for benchmark intake.

## Avoiding Contamination

Candidate tasks must not mention the evaluated system, internal decision
layers, benchmark-specific response formats, or preferred architectural
terminology.

## Licenses

Do not copy large fragments from third-party repositories. If license or usage
is unclear, classify conservatively or reject the candidate.

## Insufficient Traceability

When in doubt, downgrade the origin classification.

## Externality Score

Externality is not performance evidence.

The externality score is diagnostic. It documents source independence and
traceability only. It cannot authorize benchmark performance claims.

## Intake Limitation

Dataset intake does not execute providers, does not measure performance, and
does not promote candidates into the frozen benchmark dataset.

