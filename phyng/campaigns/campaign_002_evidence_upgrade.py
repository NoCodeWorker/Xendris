from pathlib import Path

from pydantic import BaseModel

from phyng.benchmarks import (
    BenchmarkDataset,
    add_benchmark_dataset,
    classify_benchmark_readiness,
    generate_benchmark_registry_report,
)
from phyng.evidence import (
    create_research_tasks_for_requirements,
    default_source_requirements,
    generate_evidence_reports,
)
from phyng.model_comparison import (
    SourceBackedModelSpec,
    evaluate_source_backed_comparison_readiness,
    generate_source_backed_readiness_report,
)


class Campaign002EvidenceUpgradeResult(BaseModel):
    campaign_id: str = "CAMPAIGN-002"
    benchmark_id: str
    benchmark_status: str
    gain_label: str | None
    readiness_report_path: str
    benchmark_report_path: str
    source_requirements_report_path: str
    can_claim_physical_prediction: bool
    max_claim_level: int


def default_synthetic_visibility_benchmark() -> BenchmarkDataset:
    t = [float(i) for i in range(11)]
    y_true = [1.0 - 0.035 * value for value in t]
    return BenchmarkDataset(
        dataset_id="BENCH-CAMPAIGN-002-SYNTH-VISIBILITY-001",
        name="Synthetic CAMPAIGN-002 visibility benchmark",
        observable="visibility_loss",
        t=t,
        y_true=y_true,
        provenance_type="SYNTHETIC",
        source_ids=[],
        generation_method="deterministic linear synthetic visibility curve for engine validation",
        parameters={"slope": 0.035},
        uncertainty=None,
        epsilon_exp=1e-6,
        allowed_uses=["engine validation", "SyntheticGain calculation"],
        forbidden_uses=[
            "physical PredictiveGain",
            "experimental evidence",
            "Frontera C validation",
        ],
    )


def run_campaign_002_evidence_upgrade(root_dir: Path) -> Campaign002EvidenceUpgradeResult:
    requirements = default_source_requirements()
    create_research_tasks_for_requirements(requirements, root_dir)
    evidence_reports = generate_evidence_reports(requirements, root_dir)

    benchmark = default_synthetic_visibility_benchmark()
    add_benchmark_dataset(benchmark, root_dir)
    benchmark_readiness = classify_benchmark_readiness(benchmark)
    benchmark_report_path = generate_benchmark_registry_report([benchmark], root_dir)

    baseline = SourceBackedModelSpec(
        model_id="MODEL-CAMPAIGN-002-BASELINE",
        name="Toy exponential visibility baseline",
        model_role="BASELINE",
        formula="V_base(t)=exp(-gamma_base*t)",
        parameters={"gamma_base": 0.05},
        assumptions=["Toy baseline until REQ-SRC-006 is satisfied."],
        source_ids=[],
        support_status="TOY_INTERNAL",
        allowed_claims=["The baseline is an internal toy model."],
        forbidden_claims=["The baseline is a source-backed physical decoherence model."],
    )
    candidate = SourceBackedModelSpec(
        model_id="MODEL-CAMPAIGN-002-CANDIDATE",
        name="Boundary-aware toy candidate",
        model_role="CANDIDATE",
        formula="V_C(t)=exp(-(gamma_base + alpha*B)*t)",
        parameters={"gamma_base": 0.05, "alpha": 1.0},
        assumptions=["Hypothesis plumbing only."],
        source_ids=[],
        support_status="HYPOTHETICAL_CANDIDATE",
        allowed_claims=["The candidate is a testable hypothesis under explicit assumptions."],
        forbidden_claims=["The candidate is physically validated."],
    )
    readiness = evaluate_source_backed_comparison_readiness(
        "CAMPAIGN-002-source-backed-readiness",
        baseline,
        candidate,
        benchmark,
    )
    readiness_report_path = generate_source_backed_readiness_report(readiness, root_dir)

    return Campaign002EvidenceUpgradeResult(
        benchmark_id=benchmark.dataset_id,
        benchmark_status=benchmark_readiness.readiness_status,
        gain_label=benchmark_readiness.gain_label,
        readiness_report_path=str(readiness_report_path),
        benchmark_report_path=str(benchmark_report_path),
        source_requirements_report_path=str(evidence_reports["source_requirements"]),
        can_claim_physical_prediction=readiness.can_claim_physical_prediction,
        max_claim_level=readiness.max_claim_level,
    )
