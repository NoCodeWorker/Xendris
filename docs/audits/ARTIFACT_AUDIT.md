# Artifact Audit

Date: 2026-07-02

Protocol: `governance/focus/04_ARTIFACT_AUDIT_PROTOCOL.md`

## Audit Scope

The audit inspected `.md`, `.py`, and `.json` artifacts excluding `.venv`, `.git`, `.pytest_cache`, `__pycache__`, `phyng.egg-info`, `node_modules`, `.next`, `dist`, and `build`.

Total audited artifacts:

```txt
2082
```

## Audit Summary

```yaml
audit_summary:
  core_count: 96
  bridge_count: 173
  auxiliary_count: 1562
  off_track_count: 259
  drift_detected: true
  main_risk: thermal_visibility_heating_power_axis_work_promoted_to_primary_path
  immediate_recenter_action: freeze_auxiliary_as_primary_and_restore_causal_informational_membrane_core
```

## Required Warning

```txt
CONTRACT WARNING: AUXILIARY PROMOTED TO CORE WITHOUT BRIDGE
```

The recent `heating_power_W`, visibility, contrast, and PredictiveGain path was useful as an auxiliary study, but it was being treated as the main route toward Frontera C validation. That promotion is now revoked.

## Artifact Classification Table

| Artifact | Path | Classification | Reason | Keep/Move/Archive | Required Action |
|---|---|---|---|---|---|
| Focus governance pack | `governance/focus/` | CORE | Defines binding focus contract for Frontera C-Mayor. | Keep | Treat as active governance. |
| Core seed manifest and case notes | `docs/frontera_c/00_frontera_c_v0_3_manifesto_operacional.md`, `docs/frontera_c/01_principio_seleccion_escala_operacional_L.md`, `docs/frontera_c/02_caso_estudio_1_canal_cuantico_huella_epistemologica.md`, `docs/frontera_c/03_caso_estudio_2_interferometro_mesoscopico_negative_bound.md`, `docs/frontera_c/04_claim_gatekeeper_v0_3.md`, `docs/frontera_c/05_prompt_codex_frontera_c_v0_3_lab.md` | CORE | Directly concern Frontera C, scale, causal/epistemic boundaries, and claim control. | Keep | Reconcile with Frontera C-Mayor definition. |
| Frontera C-Mayor definition | `docs/frontera_c/FRONTERA_C_MAYOR.md` | CORE | Defines `c` as causal-informational membrane. | Keep | Use as current center. |
| Known physics alignment | `docs/frontera_c/KNOWN_PHYSICS_ALIGNMENT.md` | CORE | Separates established relativity, horizons, measurement, and decoherence from possible novelty. | Keep | Use before novelty claims. |
| Novelty claims | `docs/frontera_c/NOVELTY_CLAIMS.md` | CORE | Defines what would and would not be novel. | Keep | Use before any validation claim. |
| Falsifiability | `docs/frontera_c/FALSIFIABILITY.md` | CORE | Defines failure routes and falsifiable claim template. | Keep | Use before experiments or benchmarks. |
| Validation ladder | `docs/status/VALIDATION_LADDER.md` | CORE | Defines allowed validation sequence and blocks auxiliary substitution. | Keep | Use before any next gate. |
| Mathematical sketch | `docs/frontera_c/MATHEMATICAL_SKETCH.md` | CORE | Defines provisional variables and minimal membrane claim without validation. | Keep | Review for redundancy against known physics. |
| Redundancy risk review | `docs/audits/REDUNDANCY_RISK_REVIEW.md` | CORE | Tests `B_c(O)` against known physics and blocks novelty promotion pending theorem. | Keep | Requires human review. |
| Minimal theorem attempt | `docs/frontera_c/MINIMAL_THEOREM_ATTEMPT.md` | CORE / BRIDGE | Attempts CIS Proposition and blocks theorem promotion pending formal review. | Keep | Human review required. |
| Relation formalization | `docs/frontera_c/RELATION_FORMALIZATION.md` | CORE / BRIDGE | Formalizes `A_c`, `I_c`, `M`, `K`, and `R`; classifies `D_CI(O)` as meaningful bridge framework, not validated core theory. | Keep | Human review required. |
| Bridge framework decision | `docs/audits/BRIDGE_FRAMEWORK_DECISION.md` | CORE / BRIDGE | Records human acceptance of Cycle 5 as `BRIDGE_FORMAL_FRAMEWORK_CREATED` while preserving `NOT_VALIDATED`, `UNRESOLVED` novelty, and `MEDIUM_HIGH` redundancy risk. | Keep | Use as governing decision before any next formal-theory action. |
| State of the project | `docs/frontera_c/FRONTERA_C_STATE_OF_THE_PROJECT.md` | CORE / BRIDGE | Consolidates current accepted status, formal structure, allowed/forbidden claims, risks, frozen branches, and next safe research actions after bridge-framework acceptance. | Keep | Use as the current human-review orientation document. |
| Formal review checklist | `docs/audits/FORMAL_REVIEW_CHECKLIST.md` | CORE / BRIDGE | Prepares external scientific review questions, redundancy checks, theorem requirements, falsifiability requirements, reviewer decisions, and status-update rules. | Keep | Use before any external formal review or theorem-promotion decision. |
| External review brief | `docs/frontera_c/FRONTERA_C_REVIEW_BRIEF.md` | CORE / BRIDGE | Concise technical brief for external review of `D_CI(O) subset D_LC(O)` as bridge framework, including redundancy, rejection, and survival criteria. | Keep | Send only with no validation or new-physics claims. |
| External review questions | `docs/audits/EXTERNAL_REVIEW_QUESTIONS.md` | CORE / BRIDGE | Domain-specific review questions for relativity, quantum information, mathematical physics, and foundations reviewers. | Keep | Use to guide external review. |
| Outreach email draft | `docs/audits/OUTREACH_EMAIL_DRAFT.md` | CORE / BRIDGE | Short English and Spanish outreach drafts requesting technical sanity check without grand claims. | Keep | Use for reviewer outreach. |
| Review response classifier | `docs/audits/REVIEW_RESPONSE_CLASSIFIER.md` | CORE / BRIDGE | Maps reviewer feedback categories to conservative `docs/status/PROJECT_STATUS.md` updates while preserving no-validation boundaries. | Keep | Use after receiving feedback. |
| Internet redundancy check | `docs/audits/INTERNET_REDUNDANCY_CHECK.md` | CORE / BRIDGE | Records exact-phrase and near-match literature search; finds no exact phrase match but high same-family overlap with AQFT, relativistic measurement, causal diamonds, and recoverability. | Keep | Use before any novelty or theorem promotion. |
| AQFT / Haag-Kastler comparison | `docs/audits/AQFT_HAAG_KASTLER_COMPARISON.md` | CORE / BRIDGE | Compares Frontera C-Mayor against AQFT local algebras, microcausality, and observable-region structure; concludes survival only as bridge layer pending expert review. | Keep | Use before any theorem-promotion or novelty claim. |
| I/K/R operational residue review | `docs/audits/IKR_OPERATIONAL_RESIDUE_REVIEW.md` | CORE / BRIDGE | Tests the surviving I_c/K/R layer against quantum channel capacity, decoherence/coherence theory, Petz recovery, QEC, and entanglement wedge reconstruction; keeps Frontera C-Mayor as bridge framework only. | Keep | Use before any claim that I/K/R is non-redundant. |
| Core/bridge tooling roadmap | `docs/audits/TOOLING_ROADMAP.md` | CORE / BRIDGE | Defines allowed internal tooling phases and what each tool can and cannot prove under no-validation governance. | Keep | Use to sequence RAG, Lean, collapse, and toy-model work without benchmark drift. |
| I/K/R collapse matrix | `docs/audits/IKR_COLLAPSE_MATRIX.md` | CORE / BRIDGE | Compares Frontera C-Mayor objects against AQFT, measurement theory, channels, decoherence, Petz recovery, QEC, entanglement wedge reconstruction, and information causality. | Keep | Use as redundancy-control input before any theorem or novelty language. |
| RAG corpus plan | `docs/rag/RAG_CORPUS_PLAN.md` | CORE / BRIDGE | Defines source-indexed corpus folders, metadata, claim extraction, and redundancy questions for conservative literature review. | Keep | Build only as review infrastructure, not evidence inflation. |
| Formal Lean plan | `docs/lean/FORMAL_LEAN_PLAN.md` | CORE / BRIDGE | Specifies minimal definitions for `O`, `E`, `A_c`, `I_c`, `M`, `K`, `R`, `D_LC`, `D_CI`, and strict inclusion while stating Lean cannot prove physical truth. | Keep | Use for formal consistency only. |
| D_CI strict inclusion toy spec | `docs/models/TOY_MODEL_DCI_STRICT_INCLUSION_SPEC.md` | CORE / BRIDGE | Provides a non-empirical toy model where events are inside `D_LC(O)` but outside `D_CI(O)` for information, coherence, or recoverability failures. | Keep | Use only to test formal usability. |
| Minimal Lean basic definitions | `formal/FrC/Basic.lean` | CORE / BRIDGE | Defines abstract `Observer`, `Event`, `A_c`, `I_c`, `M`, `K`, `R`, `D_LC`, and `D_CI` with no physical semantics encoded. | Keep | Compile only after Lean toolchain setup. |
| Minimal Lean subdomain theorem | `formal/FrC/Subdomain.lean` | CORE / BRIDGE | Proves the definitional result `D_CI_subset_D_LC`. | Keep | Treat as formal consistency only, not validation. |
| Minimal Lean strict inclusion scaffold | `formal/FrC/StrictInclusion.lean` | CORE / BRIDGE | Defines strict-inclusion witness predicates and proves conditional proper-subdomain consequences. | Keep | Requires witness assumptions; not empirical evidence. |
| Lean formalization report | `docs/lean/LEAN_FORMALIZATION_REPORT.md` | CORE / BRIDGE | Records what was formalized, what was proven, what remains definitional, and that Lean/Lake compilation succeeded for the abstract formalization. | Keep | Use before formal-methods review. |
| Lean Lake wrapper | `lakefile.lean` | CORE / BRIDGE | Defines a minimal Lake package and `FrC` library rooted at `formal/`. | Keep | Use only for compiling abstract formalization. |
| Lean toolchain pin | `lean-toolchain` | CORE / BRIDGE | Pins a Lean 4 toolchain for future compile attempts without installing anything immediately. | Keep | Update only with explicit toolchain decision. |
| Lean root module | `formal/FrC.lean` | CORE / BRIDGE | Imports `FrC.Basic`, `FrC.Subdomain`, and `FrC.StrictInclusion` as the root module. | Keep | Use as Lake library root. |
| Lean compile status | `docs/lean/LEAN_COMPILE_STATUS.md` | CORE / BRIDGE | Records Lean/Lake availability, wrapper files, import structure, and latest `COMPILED` build check for the abstract formalization. | Keep | Use only as type-checking evidence, not validation. |
| Lake manifest | `lake-manifest.json` | CORE / BRIDGE | Generated by successful `lake build`; records the minimal Lake package manifest state. | Keep | Regenerate through Lake only. |
| Lean toy witness module | `formal/FrC/ToyModel.lean` | CORE / BRIDGE | Adds an axiom-based abstract witness with `A_c O0 e0` and `Not (I_c O0 e0)` proving `D_LC O0 e0` and `Not (D_CI O0 e0)`. | Keep | Use only as formal witness under assumptions, not evidence. |
| Toy strict-inclusion report | `docs/models/TOY_MODEL_DCI_STRICT_INCLUSION_REPORT.md` | CORE / BRIDGE | Documents the abstract witness, proven Lean statements, non-physical status, and no-validation boundary. | Keep | Use before formal-methods review. |
| Source-indexed RAG plan | `docs/rag/SOURCE_INDEXED_RAG_PLAN.md` | CORE / BRIDGE | Defines source-indexed corpus folders, workflow, trust levels, review statuses, and claim-control rules for I/K/R redundancy review. | Keep | Use only for source-indexed redundancy review. |
| Paper source schema | `docs/rag/PAPER_SOURCE_SCHEMA.md` | CORE / BRIDGE | Defines metadata, key-definition, theorem/result, and relation-mapping schemas for I/K/R source review. | Keep | Use before registering source records. |
| I/K/R review query set | `docs/audits/IKR_REVIEW_QUERY_SET.md` | CORE / BRIDGE | Provides review questions for `I_c`, `K`, `R`, `D_CI`, `B_c`, and expert review routing. | Keep | Use during source review. |
| I/K/R redundancy source table | `docs/audits/IKR_REDUNDANCY_SOURCE_TABLE.md` | CORE / BRIDGE | Initializes source-family table with AQFT, Halvorson AQFT, detector/QFT measurement, recoverability, Petz, information causality, decoherence, QEC, and entanglement-wedge threats. | Keep | Populate with primary-source review; do not treat as validation. |
| I/K/R source metadata table | `docs/audits/IKR_SOURCE_METADATA_TABLE.md` | CORE / BRIDGE | Populates concrete source-family metadata, domains, URLs/arXiv/DOI where known, relation mapping, redundancy threat level, and review status. | Keep | Use as source-indexed review input, not evidence. |
| I/K/R claim extraction table | `docs/audits/IKR_CLAIM_EXTRACTION_TABLE.md` | CORE / BRIDGE | Extracts conservative claim summaries and maps them to `I_c`, `K`, `R`, and `D_CI` redundancy implications. | Keep | Use for expert review preparation. |
| I/K/R redundancy findings | `docs/audits/IKR_REDUNDANCY_FINDINGS.md` | CORE / BRIDGE | Summarizes collapse risk: `I_c` partially collapses, `K` and `R` strongly collapse, and the joint layer survives only as bridge. | Keep | Do not use as validation or novelty claim. |
| Bridge-only framework decision | `docs/audits/BRIDGE_ONLY_FRAMEWORK_DECISION.md` | CORE / BRIDGE | Records the human decision accepting I/K/R redundancy findings and demoting Frontera C-Mayor to bridge-only framework while preserving `NOT_VALIDATED`, `UNRESOLVED`, and no partial support. | Keep | Use as governing decision before expert review or primary-source deep review. |
| Frontera C lessons learned | `docs/frontera_c/FRONTERA_C_LESSONS_LEARNED.md` | CORE / BRIDGE | Documents the conservative lessons after bridge-only demotion: AQFT absorption, I/K/R redundancy, Lean limits, forbidden claims, reopen conditions, and future speculative-physics discipline. | Keep | Use as post-demotion orientation before any future reopen request. |
| Project status | `docs/status/PROJECT_STATUS.md` | CORE | Separates core, bridge, auxiliary, and validation status. | Keep | Update after each audit trigger. |
| Artifact audit | `docs/audits/ARTIFACT_AUDIT.md` | CORE | Classifies existing artifacts and drift. | Keep | Update after major state changes. |
| Auxiliary map | `docs/audits/AUXILIARY_STUDIES_MAP.md` | CORE | Registers auxiliary studies and freeze rules. | Keep | Use before expanding substudies. |
| Drift log | `docs/audits/DRIFT_LOG.md` | CORE | Records drift and recentering decisions. | Keep | Append on future drift. |
| Canonical status/reporting core | `phyng/core/` | BRIDGE | Governance and permission grammar supports epistemic control, not direct theory. | Keep | Preserve as infrastructure. |
| Evidence/source identity/local source pipeline | `phyng/evidence/`, `phyng/local_source_text/`, `phyng/source_download/`, `phyng/source_identity_preflight/`, related `data/real_sources/` | BRIDGE | Supports provenance, evidence boundaries, and source discipline. | Keep | Use only for core/bridge claims with explicit mapping. |
| Decoherence/source pressure/extract review packages | `phyng/extract_candidate_review/`, `phyng/pdf_text_extraction/`, `phyng/source_pressure_decision/`, related reports | BRIDGE | Could support coherence/decoherence bridge; not core validation by itself. | Keep | Require bridge document before promotion. |
| Phi Gradient / LOG_BOUNDARY / PredictiveGain history | `docs/214*` onward, `data/real_sources/`, `reports/pdf_text_extraction/`, `reports/extract_candidate_review/` | AUXILIARY | Mostly source extraction, benchmark, y_true, and predictive-gain scaffolding detached from `c` membrane. | Keep as archive | Mark AUXILIARY unless explicit bridge is written. |
| Visibility/decoherence dataset expansion | `phyng/dataset_expansion/`, `phyng/targeted_ytrue/`, `data/frontera_c/dataset_expansion/`, `data/frontera_c/targeted_ytrue/` | AUXILIARY | Concerns visibility/contrast observed datasets and y_true expansion. | Keep frozen | Do not continue as primary. |
| Heating-power axis work | `phyng/candidates/heating_power_axis_expansion.py`, `data/frontera_c/candidates/*heating_power_axis*v5_9_3.json`, `docs/381_PHYGN_V5_9_3_TARGETED_HEATING_POWER_AXIS_EXPANSION_RESULTS.md` | AUXILIARY | `heating_power_W` axis is thermal-optical auxiliary. | Keep frozen | No v6.0 continuation without bridge and explicit approval. |
| Common-axis recovery | `phyng/candidates/common_axis_recovery.py`, `docs/380_PHYGN_V5_9_2_COMMON_CONDITION_AXIS_RECOVERY_RESULTS.md` | AUXILIARY | Common condition axis was built around visibility/thermal benchmark path. | Keep frozen | May inform methodology only. |
| Candidate family selection v5.9 | `phyng/candidates/`, `docs/374_PHYGN_V5_9_REALITY_CONTACT_CANDIDATE_FAMILY_RESULTS.md` | AUXILIARY | Current selection path is benchmark-centered, not core `c` membrane. | Keep | Reclassify as method archive. |
| Synthetic benchmarks | `phyng/synthetic_benchmark_design/`, `benchmarks/` | AUXILIARY | Benchmark infrastructure does not define or validate Frontera C-Mayor. | Keep frozen | Do not optimize before core restoration. |
| Observable dataset packages | `phyng/observable_dataset/`, `phyng/observable_location/`, `data/frontera_c/observable_location/` | AUXILIARY | Local observable extraction, visibility, contrast, and source-location work. | Keep | Use only under bridge discipline. |
| Copilot/UX/frontend/application work | `frontend/`, `phyng/ux/`, `tools/run_api.py`, business/channel docs | OFF_TRACK | Product/interface/commercial work does not currently clarify Frontera C-Mayor. | Archive mentally | Do not expand in this research phase. |
| Backlog and miscellaneous scaffolding | `backlog/`, `.vscode/`, miscellaneous unclassified docs | OFF_TRACK | Operational or unrelated scaffolding. | Keep if harmless | Ignore until core restored. |
| Tests for auxiliary pipelines | `tests/test_*v5_7*`, `tests/test_*v5_9*`, heating/visibility/ytrue tests | AUXILIARY | Validate auxiliary machinery only. | Keep frozen | Do not treat passing tests as core progress. |
| Tests for core governance/status | `tests/test_*status*`, `tests/test_*report_contract*`, selected core tests | BRIDGE | Enforce epistemic/reporting discipline. | Keep | Extend only as governance needs. |

## Group Counts

| Top-level path | CORE | BRIDGE | AUXILIARY | OFF_TRACK |
|---|---:|---:|---:|---:|
| root files | 7 | 30 | 0 | 1 |
| `formal/` | 0 | 5 | 0 | 0 |
| `governance/` | 12 | 0 | 0 | 0 |
| `docs/` | 15 | 19 | 332 | 22 |
| `phyng/` | 33 | 48 | 419 | 105 |
| `data/` | 0 | 6 | 208 | 14 |
| `reports/` | 6 | 16 | 342 | 31 |
| `tests/` | 15 | 33 | 250 | 75 |
| `rag/` | 1 | 15 | 10 | 0 |
| `benchmarks/` | 0 | 0 | 1 | 0 |
| `frontend/` | 0 | 0 | 0 | 8 |
| other | 0 | 0 | 0 | 3 |

Frontera C-Mayor validation status remains separate from all auxiliary progress.
