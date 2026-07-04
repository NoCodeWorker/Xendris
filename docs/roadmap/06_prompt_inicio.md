# 06 — Prompt de inicio

Usar este prompt en el IDE/agente para iniciar la implementación.

```text
Implement Xendris v0.4 Local Claim Algebras as a deterministic extension of the existing Trust Kernel.

Project context:
Xendris is evolving into an Algebraic Trust Architecture for governing generative models. The goal is not to claim physical validation from Algebraic Quantum Field Theory, but to use AQFT-inspired structures — local observable algebras, sectors, representations, and non-contamination boundaries — as formal software architecture patterns.

Do not modify frontend/, providers/, benchmark datasets, or existing public APIs unless strictly necessary.
Do not make provider calls.
Do not change model behavior.
Do not update documentation with invented test counts.
Do not introduce universal superiority claims.

Create deterministic packages:

xendris/core/algebra/
xendris/core/local/
xendris/core/boundary/

Requirements:

1. Define ClaimObject as an immutable structured object wrapping or extending existing Claim semantics where possible.

2. Define LocalContext enum with at least:
   USER, BENCHMARK, CODE, RUNTIME, RAG, POLICY, COST, LATENCY, PRODUCTION, DOCUMENTATION.

3. Define LocalClaimAlgebra with:
   - context
   - allowed claim types
   - allowed outgoing transitions
   - blocked outgoing transitions
   - default risk level

4. Define EvidenceBridge with:
   - bridge_type
   - source_context
   - target_context
   - evidence_ref
   - confidence
   - metadata

5. Define BoundaryDecision enum:
   ALLOW, ALLOW_WITH_LIMITATIONS, BLOCK, HUMAN_REVIEW.
   (And ALLOW_AS_HYPOTHESIS or equivalent compatibility mode, such as ALLOW_WITH_LIMITATIONS with limitation = "hypothesis_only").

6. Define ContaminationGuard:
   - accepts source claim, target context, requested target claim type, optional evidence bridge
   - returns deterministic decision object containing decision, reason, risk level, and limitations

6b. Define UsefulnessPreservationPolicy:
   - inspects an initial guard decision,
   - detects whether the claim is low-risk, exploratory, creative, explanatory, or operational,
   - attempts safe downgrade before block,
   - outputs ALLOW_WITH_LIMITATIONS or ALLOW_AS_HYPOTHESIS where appropriate,
   - preserves BLOCK for hard forbidden transitions (such as BENCHMARK -> UNIVERSAL_SUPERIORITY or DRY_RUN_LATENCY -> PRODUCTION_LATENCY without real measurement),
   - preserves HUMAN_REVIEW for unresolved high-risk conflicts.
   - Invariant: UsefulnessPreservationPolicy must never override ContaminationGuard for hard forbidden transitions.

7. Add explicit blocked transitions:
   - BENCHMARK -> UNIVERSAL_SUPERIORITY
   - LATENCY -> ACCURACY
   - USER_PROVIDED -> VERIFIED without evidence
   - CODE_STATE -> PRODUCTION_READY without tests/build/deployment evidence
   - DRY_RUN_LATENCY -> PRODUCTION_LATENCY without real measurement
   - BENCHMARK_SCORE -> GENERAL_MODEL_QUALITY without external validation
   - NORMAL_CONTROL -> UNIVERSAL_SAFETY

8. Add limited allowed transitions:
   - BENCHMARK_SCORE + BENCHMARK_ARTIFACT -> LIMITED_BENCHMARK_CLAIM
   - CODE_STATE + TEST_RESULT or BUILD_LOG -> VERIFIED_CODE_STATE
   - RUNTIME_ERROR + RUNTIME_TRACE -> EXCLUDED_FROM_SCORING
   - USER_PROVIDED -> USER_ASSERTION
   - DRY_RUN_LATENCY -> LATENCY_LIMITED_CLAIM

9. Add unit tests proving:
   - benchmark scores cannot become universal superiority claims.
   - benchmark scores can become limited benchmark claims when scoped correctly.
   - dry-run latency cannot become production latency.
   - dry-run latency can become a limited dry-run latency claim.
   - user-provided claims cannot become factual/verified claims without evidence.
   - user-provided claims can be promoted with a valid evidence bridge.
   - code state claims cannot become production-ready claims without verification.
   - code state claims can become verified code state with tests/build evidence.
   - latency cannot become accuracy.
   - normal control success cannot become universal safety.
   - invalid or mismatched evidence bridges do not allow unsafe promotion.
   - human review bridges can produce HUMAN_REVIEW or ALLOW_WITH_LIMITATIONS where appropriate.
   - test_normal_control_claim_passes_without_overblocking
   - test_low_risk_unsupported_claim_is_downgraded_not_blocked
   - test_exploratory_claim_allowed_as_hypothesis
   - test_creative_non_factual_output_passes_without_gate_interference
   - test_overbroad_claim_is_scoped_before_blocking_when_safe
   - test_high_risk_unsupported_claim_requires_human_review_or_block
   - test_usefulness_preservation_does_not_override_forbidden_transition
   - test_usefulness_preservation_does_not_promote_user_claim_without_evidence
   - test_usefulness_preservation_does_not_convert_benchmark_win_to_universal_superiority
   - test_usefulness_preservation_does_not_convert_dry_run_latency_to_production_latency
   - test_allow_with_limitations_contains_explicit_scope
   - test_allow_as_hypothesis_contains_non_factual_marker

10. Add docs/status/XENDRIS_ALGEBRAIC_TRUST_V0_4.md explaining:
   - purpose
   - architecture
   - AQFT inspiration without physical validation claims
   - limitations
   - modules created
   - UsefulnessPreservationPolicy implementation details
   - tests actually run and observed results

Roadmap file references for planning:
- docs/roadmap/README.md
- docs/roadmap/00_vision.md
- docs/roadmap/01_aqft_mapping.md
- docs/roadmap/02_architecture.md
- docs/roadmap/03_roadmap_versions.md
- docs/roadmap/04_v0_4_local_claim_algebras.md
- docs/roadmap/05_tests_acceptance.md
- docs/roadmap/08_glossary.md

Run the relevant test suite.
Return:
- files created
- files modified
- tests run
- observed result
- remaining risks
- suggested commit message
```
