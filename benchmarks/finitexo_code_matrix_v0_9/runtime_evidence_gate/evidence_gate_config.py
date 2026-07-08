from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


BENCHMARK_NAME = "Finitexo Code Matrix"
BENCHMARK_VERSION = "v0.9.1"
SOURCE_RUN_VERSION = "v0.9.0"
SOURCE_RUN_ID = "finitexo_v0_9_0_runtime_paired_lift_n30_live_20260708_02"
SOURCE_RUN_DIR = Path(
    "runs/finitexo_code_matrix_v0_9_0_runtime_paired_lift_n30_live_20260708_02"
)

EXPECTED_DATASET_HASH = "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841"
EXPECTED_MANIFEST_HASH = "3cfa4e904c0cf5918da4483c1e656fd8cf9b8e231bc5487b45e86eabb2ff1c54"

EXPECTED_TOTAL_ATTEMPTS = 240
EXPECTED_TOTAL_COMPLETED = 240
EXPECTED_TOTAL_FAILED = 0
EXPECTED_SCORES = 240
EXPECTED_RESPONSES = 240
EXPECTED_METADATA = 240
EXPECTED_RUNTIME_TRACES = 120
EXPECTED_CALIBRATION_TRACES = 60
EXPECTED_ERRORS = 0

EXPECTED_VARIANTS = [
    "deepseek_base",
    "deepseek_wrapper",
    "deepseek_runtime",
    "deepseek_calibrated_runtime",
    "openai_base",
    "openai_wrapper",
    "openai_runtime",
    "openai_calibrated_runtime",
]

EXPECTED_FAMILIES = [
    "algorithmic_reasoning",
    "api_design_consistency",
    "edge_case_handling",
    "performance_constraints",
    "stateful_refactor",
]

OUTPUT_DIR = Path(
    "runs/finitexo_code_matrix_v0_9_1_runtime_evidence_gate_live_20260708_02"
)

REQUIRED_ARTIFACTS = [
    "summary.json",
    "gate.json",
    "evidence_integrity.json",
    "costs.json",
    "paired_lift.json",
    "responses.jsonl",
    "scores.jsonl",
    "metadata.jsonl",
    "runtime_traces.jsonl",
    "audit_decisions.jsonl",
    "repair_attempts.jsonl",
    "calibration_traces.jsonl",
    "claim_status.jsonl",
    "confidence_bands.jsonl",
    "allowed_blocked_language.jsonl",
    "calibrated_final_responses.jsonl",
    "errors.jsonl",
]

COMPARISON_SPECS = [
    ("deepseek_wrapper", "deepseek_base"),
    ("deepseek_runtime", "deepseek_base"),
    ("deepseek_calibrated_runtime", "deepseek_base"),
    ("deepseek_runtime", "deepseek_wrapper"),
    ("deepseek_calibrated_runtime", "deepseek_wrapper"),
    ("deepseek_calibrated_runtime", "deepseek_runtime"),
    ("openai_wrapper", "openai_base"),
    ("openai_runtime", "openai_base"),
    ("openai_calibrated_runtime", "openai_base"),
    ("openai_runtime", "openai_wrapper"),
    ("openai_calibrated_runtime", "openai_wrapper"),
    ("openai_calibrated_runtime", "openai_runtime"),
]

SIGNAL_CLASSIFICATIONS = {
    "STRONG_DIAGNOSTIC_SIGNAL": "strong",
    "MODERATE_DIAGNOSTIC_SIGNAL": "moderate",
    "WEAK_OR_INCONCLUSIVE_SIGNAL": "weak_or_inconclusive",
    "NEGATIVE_SIGNAL": "negative",
}

EVIDENCE_GATE_DECISIONS = {
    "BLOCKED_INTEGRITY_FAIL": "RUNTIME_EVIDENCE_GATE_BLOCKED_INTEGRITY_FAIL",
    "WEAK_OR_INCONCLUSIVE": "RUNTIME_EVIDENCE_GATE_COMPLETED_WEAK_OR_INCONCLUSIVE_DIAGNOSTIC_ONLY",
    "DIAGNOSTIC_SIGNAL": "RUNTIME_EVIDENCE_GATE_COMPLETED_DIAGNOSTIC_SIGNAL_ONLY",
}


@dataclass
class RuntimeEvidenceGateConfig:
    benchmark_name: str = BENCHMARK_NAME
    benchmark_version: str = BENCHMARK_VERSION
    source_run_version: str = SOURCE_RUN_VERSION
    source_run_id: str = SOURCE_RUN_ID
    source_run_dir: Path = SOURCE_RUN_DIR
    expected_dataset_hash: str = EXPECTED_DATASET_HASH
    expected_manifest_hash: str = EXPECTED_MANIFEST_HASH
    expected_total_attempts: int = EXPECTED_TOTAL_ATTEMPTS
    expected_total_completed: int = EXPECTED_TOTAL_COMPLETED
    expected_total_failed: int = EXPECTED_TOTAL_FAILED
    expected_scores: int = EXPECTED_SCORES
    expected_responses: int = EXPECTED_RESPONSES
    expected_metadata: int = EXPECTED_METADATA
    expected_runtime_traces: int = EXPECTED_RUNTIME_TRACES
    expected_calibration_traces: int = EXPECTED_CALIBRATION_TRACES
    expected_errors: int = EXPECTED_ERRORS
    expected_variants: list[str] = field(default_factory=lambda: list(EXPECTED_VARIANTS))
    expected_families: list[str] = field(default_factory=lambda: list(EXPECTED_FAMILIES))
    output_dir: Path = OUTPUT_DIR
    allow_overwrite: bool = False
    bootstrap_iterations: int = 10_000
    random_seed: int = 20260708
