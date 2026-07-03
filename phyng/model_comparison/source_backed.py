from pathlib import Path

from pydantic import BaseModel, Field

from phyng.benchmarks import BenchmarkDataset, classify_benchmark_readiness


MODEL_SUPPORT_STATUSES = {
    "UNSUPPORTED",
    "TOY_INTERNAL",
    "BACKGROUND_SUPPORTED",
    "DIRECTLY_SUPPORTED",
    "CONTRADICTED",
    "REQUIRES_SOURCE",
    "HYPOTHETICAL_CANDIDATE",
}


class SourceBackedModelSpec(BaseModel):
    model_id: str
    name: str
    model_role: str
    formula: str
    parameters: dict[str, float] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(default_factory=list)
    support_status: str
    allowed_claims: list[str] = Field(default_factory=list)
    forbidden_claims: list[str] = Field(default_factory=list)

    def model_post_init(self, __context) -> None:
        if self.model_role not in {"BASELINE", "CANDIDATE"}:
            raise ValueError("model_role must be BASELINE or CANDIDATE")
        if self.support_status not in MODEL_SUPPORT_STATUSES:
            raise ValueError(f"Unsupported support_status: {self.support_status}")


class SourceBackedComparisonReadiness(BaseModel):
    comparison_id: str
    baseline_status: str
    candidate_status: str
    benchmark_status: str
    can_compute_gain: bool
    gain_label: str | None = None
    can_claim_physical_prediction: bool
    max_claim_level: int
    missing_requirements: list[str] = Field(default_factory=list)
    blocked_claims: list[str] = Field(default_factory=list)


def evaluate_source_backed_comparison_readiness(
    comparison_id: str,
    baseline: SourceBackedModelSpec,
    candidate: SourceBackedModelSpec,
    benchmark: BenchmarkDataset | None,
) -> SourceBackedComparisonReadiness:
    missing: list[str] = []
    blocked = [
        "Phygn predicts decoherence.",
        "Phygn validates Frontera C.",
        "SyntheticGain proves physical gain.",
    ]

    baseline_status = baseline.support_status
    candidate_status = candidate.support_status
    if baseline_status in {"UNSUPPORTED", "TOY_INTERNAL", "REQUIRES_SOURCE"}:
        missing.append("source-backed baseline model")
    if baseline_status == "BACKGROUND_SUPPORTED":
        missing.append("direct baseline support")
    if baseline_status == "CONTRADICTED":
        missing.append("non-contradicted baseline")

    if candidate_status in {"UNSUPPORTED", "REQUIRES_SOURCE"}:
        missing.append("candidate support or explicit hypothesis label")
    if candidate_status == "CONTRADICTED":
        missing.append("non-contradicted candidate")

    if benchmark is None:
        benchmark_status = "MISSING_BENCHMARK"
        can_compute_gain = False
        gain_label = None
        max_claim_level = 3
        missing.append("benchmark dataset")
    else:
        benchmark_readiness = classify_benchmark_readiness(benchmark)
        benchmark_status = benchmark_readiness.readiness_status
        can_compute_gain = benchmark_readiness.can_compute_gain
        gain_label = benchmark_readiness.gain_label
        max_claim_level = min(benchmark_readiness.allowed_claim_level, 4)
        if not benchmark_readiness.can_compute_gain:
            missing.extend(benchmark_readiness.required_actions)

    if baseline_status == "DIRECTLY_SUPPORTED":
        max_claim_level = max(max_claim_level, 5 if can_compute_gain else 4)
    else:
        max_claim_level = min(max_claim_level, 3)

    if candidate_status in {"HYPOTHETICAL_CANDIDATE", "TOY_INTERNAL", "BACKGROUND_SUPPORTED"}:
        max_claim_level = min(max_claim_level, 4)
        if candidate_status == "HYPOTHETICAL_CANDIDATE":
            missing.append("direct candidate support for physical prediction")

    can_claim_physical_prediction = (
        baseline_status == "DIRECTLY_SUPPORTED"
        and candidate_status == "DIRECTLY_SUPPORTED"
        and benchmark is not None
        and benchmark.provenance_type == "EXPERIMENTAL"
        and can_compute_gain
    )
    if can_claim_physical_prediction:
        max_claim_level = max(max_claim_level, 6)
    else:
        max_claim_level = min(max_claim_level, 5)

    return SourceBackedComparisonReadiness(
        comparison_id=comparison_id,
        baseline_status=baseline_status,
        candidate_status=candidate_status,
        benchmark_status=benchmark_status,
        can_compute_gain=can_compute_gain,
        gain_label=gain_label,
        can_claim_physical_prediction=can_claim_physical_prediction,
        max_claim_level=max_claim_level,
        missing_requirements=sorted(set(missing)),
        blocked_claims=blocked,
    )


def generate_source_backed_readiness_report(
    readiness: SourceBackedComparisonReadiness,
    root_dir: Path,
) -> Path:
    report_dir = root_dir / "reports" / "model_comparison"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "source_backed_readiness.md"
    lines = [
        "# Source-Backed Comparison Readiness",
        "",
        f"- Comparison: {readiness.comparison_id}",
        f"- Baseline status: {readiness.baseline_status}",
        f"- Candidate status: {readiness.candidate_status}",
        f"- Benchmark status: {readiness.benchmark_status}",
        f"- Can compute gain: {readiness.can_compute_gain}",
        f"- Gain label: {readiness.gain_label or 'none'}",
        f"- Can claim physical prediction: {readiness.can_claim_physical_prediction}",
        f"- Max claim level: {readiness.max_claim_level}",
        "",
        "## Missing Requirements",
        *[f"- {item}" for item in readiness.missing_requirements],
        "",
        "## Blocked Overclaims",
        *[f"- {claim}" for claim in readiness.blocked_claims],
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
