from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_types import (
    AUDIT_COMPONENTS,
)
from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_scoring import (
    FAMILIES,
)

BENCHMARK_NAME = "Finitexo Code Matrix"
BENCHMARK_VERSION = "v0.10.0"
DATASET_NAME = "finitexo_code_matrix_hard_programming_n30"
DATASET_VERSION = "0.8.0"
DATASET_PATH = Path("benchmarks/finitexo_code_matrix_v0_8/datasets/hard_programming_n30")
EXPECTED_DATASET_HASH = "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841"
EXPECTED_MANIFEST_HASH = "3cfa4e904c0cf5918da4483c1e656fd8cf9b8e231bc5487b45e86eabb2ff1c54"
EXPECTED_TASK_COUNT = 30
EXPECTED_ATTEMPTS = 180
BUDGET_CAP_USD = 3.0

COST_FRONTIER_DECISIONS = {
    "BLOCKED": "COST_FRONTIER_PREFLIGHT_BLOCKED",
    "COMPLETED": "COST_FRONTIER_COMPLETED_DIAGNOSTIC_ONLY",
    "PARTIAL": "COST_FRONTIER_PARTIAL_DIAGNOSTIC_ONLY",
}


@dataclass
class CostFrontierVariantSpec:
    variant_name: str
    provider_name: str
    model_name: str
    api_key_env: str
    estimated_cost_per_task_usd: float
    execution_method: str  # BASE or CALIBRATED_RUNTIME
    use_runtime_loop: bool = False
    use_calibrated_runtime: bool = False
    use_xendris_wrapper: bool = False

    def __post_init__(self) -> None:
        if self.execution_method == "CALIBRATED_RUNTIME":
            self.use_calibrated_runtime = True
            self.use_runtime_loop = True
            self.use_xendris_wrapper = True

    def to_dict(self) -> dict:
        return {
            "variant_name": self.variant_name,
            "provider_name": self.provider_name,
            "model_name": self.model_name,
            "api_key_env": self.api_key_env,
            "estimated_cost_per_task_usd": self.estimated_cost_per_task_usd,
            "execution_method": self.execution_method,
        }


DEFAULT_VARIANTS = (
    CostFrontierVariantSpec("deepseek_v4_flash_base", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.00035, "BASE"),
    CostFrontierVariantSpec("deepseek_v4_flash_calibrated_runtime", "deepseek", "deepseek-v4-flash", "DEEPSEEK_API_KEY", 0.0009, "CALIBRATED_RUNTIME"),
    CostFrontierVariantSpec("deepseek_v4_pro_base", "deepseek", "deepseek-v4-pro", "DEEPSEEK_API_KEY", 0.0015, "BASE"),
    CostFrontierVariantSpec("gpt_4_1_nano_base", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00008, "BASE"),
    CostFrontierVariantSpec("gpt_4_1_nano_calibrated_runtime", "openai", "gpt-4.1-nano", "OPENAI_API_KEY", 0.00036, "CALIBRATED_RUNTIME"),
    CostFrontierVariantSpec("gpt_4_1_mini_base", "openai", "gpt-4.1-mini", "OPENAI_API_KEY", 0.0004, "BASE"),
)


@dataclass
class CostFrontierConfig:
    benchmark_name: str = BENCHMARK_NAME
    benchmark_version: str = BENCHMARK_VERSION
    dataset_name: str = DATASET_NAME
    dataset_version: str = DATASET_VERSION
    dataset_path: Path = DATASET_PATH
    expected_dataset_hash: str = EXPECTED_DATASET_HASH
    expected_manifest_hash: str = EXPECTED_MANIFEST_HASH
    expected_task_count: int = EXPECTED_TASK_COUNT
    expected_attempts: int = EXPECTED_ATTEMPTS
    variants: tuple[CostFrontierVariantSpec, ...] = DEFAULT_VARIANTS
    budget_cap_usd: float = BUDGET_CAP_USD
    allow_overwrite: bool = False
    provider_mode: str = "real"
    temperature: float = 0.0
    environ: dict[str, str] = field(default_factory=lambda: {
        "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM": "true",
        "DEEPSEEK_API_KEY": "present",
        "OPENAI_API_KEY": "present",
    })
    run_id: str = "finitexo_v0_10_0_cost_frontier_model_step_n30"
    output_dir: Path = Path("runs/finitexo_code_matrix_v0_10_0_cost_frontier_model_step_n30")

    def with_run_id_suffix(self, suffix: str) -> CostFrontierConfig:
        from benchmarks.finitexo_code_matrix_v0_9.runtime_paired_lift.runtime_lift_config import (
            validate_run_id_suffix,
        )
        validate_run_id_suffix(suffix)
        new = CostFrontierConfig(
            run_id=f"{self.run_id}_{suffix}",
            output_dir=Path(f"{self.output_dir}_{suffix}"),
        )
        return new

    def to_dict(self) -> dict:
        return {
            "benchmark_name": self.benchmark_name,
            "benchmark_version": self.benchmark_version,
            "run_id": self.run_id,
            "provider_mode": self.provider_mode,
            "budget_cap_usd": self.budget_cap_usd,
            "expected_task_count": self.expected_task_count,
            "expected_attempts": self.expected_attempts,
            "temperature": self.temperature,
            "variants": [v.to_dict() for v in self.variants],
        }
