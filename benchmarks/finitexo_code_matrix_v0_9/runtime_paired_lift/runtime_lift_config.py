"""Configuration for v0.9.0 runtime paired lift n=30."""

from __future__ import annotations

import dataclasses
import os
import re
from dataclasses import dataclass, field
from pathlib import Path


SUFFIX_ALLOWED_RE = re.compile(r"^[a-zA-Z0-9_-]+$")


def validate_run_id_suffix(suffix: str) -> str:
    suffix = suffix.strip()
    if not suffix:
        raise ValueError("Run ID suffix must not be empty.")
    if not SUFFIX_ALLOWED_RE.match(suffix):
        raise ValueError(
            f"Run ID suffix {suffix!r} contains invalid characters. "
            "Only letters, numbers, underscore, and hyphen are allowed."
        )
    return suffix


@dataclass(frozen=True)
class RuntimeVariantSpec:
    variant_name: str
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float = 0.00035
    use_xendris_wrapper: bool = False
    use_runtime_loop: bool = False
    use_calibrated_runtime: bool = False
    endpoint_url: str = ""


@dataclass(frozen=True)
class RuntimeConfig:
    run_id: str = "finitexo_v0_9_0_runtime_paired_lift_n30"
    provider_mode: str = "real"
    variants: tuple[RuntimeVariantSpec, ...] = field(
        default_factory=lambda: (
            RuntimeVariantSpec(
                "deepseek_base", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00035, False, False, False,
                "https://api.deepseek.com/chat/completions",
            ),
            RuntimeVariantSpec(
                "deepseek_wrapper", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00035, True, False, False,
                "https://api.deepseek.com/chat/completions",
            ),
            RuntimeVariantSpec(
                "deepseek_runtime", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00070, True, True, False,
                "https://api.deepseek.com/chat/completions",
            ),
            RuntimeVariantSpec(
                "deepseek_calibrated_runtime", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00090, True, True, True,
                "https://api.deepseek.com/chat/completions",
            ),
            RuntimeVariantSpec(
                "openai_base", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00008, False, False, False,
                "https://api.openai.com/v1/chat/completions",
            ),
            RuntimeVariantSpec(
                "openai_wrapper", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00008, True, False, False,
                "https://api.openai.com/v1/chat/completions",
            ),
            RuntimeVariantSpec(
                "openai_runtime", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00016, True, True, False,
                "https://api.openai.com/v1/chat/completions",
            ),
            RuntimeVariantSpec(
                "openai_calibrated_runtime", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00036, True, True, True,
                "https://api.openai.com/v1/chat/completions",
            ),
        )
    )
    dataset_path: Path = Path(
        "benchmarks/finitexo_code_matrix_v0_8/datasets/hard_programming_n30"
    )
    output_dir: Path = Path(
        "runs/finitexo_code_matrix_v0_9_0_runtime_paired_lift_n30"
    )
    confirmation_env_var: str = "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"
    suffix_env_var: str = "FINITEXO_RUNTIME_LIFT_RUN_ID_SUFFIX"
    expected_task_count: int = 30
    expected_attempts: int = 240
    budget_cap_usd: float = 2.00
    soft_target_usd: float = 0.80
    max_attempts_per_task_pair: int = 1
    max_tokens: int = 1024
    temperature: float = 0.0
    request_timeout_seconds: float = 60.0
    allow_mock_fallback: bool = False
    allow_overwrite: bool = False
    expected_dataset_hash: str = (
        "5554e273ecc30b4fd222763e68466b37f784e2a419e842fbaea48249360e2841"
    )
    expected_manifest_hash: str = (
        "3cfa4e904c0cf5918da4483c1e656fd8cf9b8e231bc5487b45e86eabb2ff1c54"
    )
    environ: dict[str, str] = field(default_factory=lambda: dict(os.environ))

    def with_run_id_suffix(self, suffix: str) -> RuntimeConfig:
        valid = validate_run_id_suffix(suffix)
        new_run_id = f"{self.run_id}_{valid}"
        new_dir = self.output_dir.parent / f"{self.output_dir.name}_{valid}"
        return dataclasses.replace(self, run_id=new_run_id, output_dir=new_dir)
