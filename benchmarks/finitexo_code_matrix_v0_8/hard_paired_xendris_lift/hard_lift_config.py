"""Configuration for v0.8.1 hard paired Xendris lift n=30."""

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
class HardLiftVariantSpec:
    variant_name: str
    provider_name: str
    model_name: str
    required_env_var: str
    estimated_cost_per_task_usd: float = 0.00025
    use_xendris_wrapper: bool = False
    endpoint_url: str = ""


@dataclass(frozen=True)
class HardLiftConfig:
    run_id: str = "finitexo_v0_8_1_hard_paired_xendris_lift_n30"
    provider_mode: str = "real"
    variants: tuple[HardLiftVariantSpec, ...] = field(
        default_factory=lambda: (
            HardLiftVariantSpec(
                "deepseek_base", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00035, False,
                "https://api.deepseek.com/chat/completions",
            ),
            HardLiftVariantSpec(
                "deepseek_xendris", "deepseek", "deepseek-v4-flash",
                "DEEPSEEK_API_KEY", 0.00035, True,
                "https://api.deepseek.com/chat/completions",
            ),
            HardLiftVariantSpec(
                "openai_base", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00008, False,
                "https://api.openai.com/v1/chat/completions",
            ),
            HardLiftVariantSpec(
                "openai_xendris", "openai", "gpt-4.1-nano",
                "OPENAI_API_KEY", 0.00008, True,
                "https://api.openai.com/v1/chat/completions",
            ),
        )
    )
    dataset_path: Path = Path(
        "benchmarks/finitexo_code_matrix_v0_8/datasets/hard_programming_n30"
    )
    output_dir: Path = Path(
        "runs/finitexo_code_matrix_v0_8_1_hard_paired_xendris_lift_n30"
    )
    confirmation_env_var: str = "FINITEXO_REAL_PROVIDER_EXECUTION_CONFIRM"
    suffix_env_var: str = "FINITEXO_HARD_LIFT_RUN_ID_SUFFIX"
    expected_task_count: int = 30
    expected_attempts: int = 120
    budget_cap_usd: float = 1.00
    soft_target_usd: float = 0.40
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

    def with_run_id_suffix(self, suffix: str) -> HardLiftConfig:
        valid = validate_run_id_suffix(suffix)
        new_run_id = f"{self.run_id}_{valid}"
        new_dir = self.output_dir.parent / f"{self.output_dir.name}_{valid}"
        return dataclasses.replace(self, run_id=new_run_id, output_dir=new_dir)
