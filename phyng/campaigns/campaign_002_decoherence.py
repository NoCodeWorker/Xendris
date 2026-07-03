from pathlib import Path

from pydantic import BaseModel, Field

from phyng.model_comparison import (
    ModelComparisonResult,
    ModelComparisonSpec,
    default_boundary_coupling_spec,
    generate_model_comparison_report,
    run_model_comparison,
)
from phyng.rag.research_planner import list_research_tasks, save_research_task
from phyng.rag.schemas import ResearchTask
from phyng.rag.source_registry import list_sources


class Campaign002Input(BaseModel):
    campaign_id: str = "CAMPAIGN-002"
    comparison_id: str = "CAMPAIGN-002_default_toy_comparison"
    system_id: str = "SYS-MESO-NANOPARTICLE"
    observable: str = "visibility_loss"
    t: list[float] = Field(default_factory=lambda: [float(i) for i in range(11)])
    gamma_base: float = 0.05
    alpha: float = 1.0
    B: float = 7.426160269118667e-38
    QB: float = 2.612280302374279e-56
    epsilon_exp: float | None = 1e-6
    y_true: list[float] | None = None
    error_metric: str = "MSE"


class Campaign002Result(BaseModel):
    campaign_id: str
    comparison: ModelComparisonResult
    mode: str
    inherited_bound: str
    report_path: str
    model_report_path: str
    rag_report_path: str
    next_research_tasks: list[str] = Field(default_factory=list)


RAG_TASKS_V06 = [
    (
        "RT-CAMPAIGN-002-SRC-DECOH-001",
        "What source grounds standard decoherence visibility decay for matter-wave systems?",
        "CAMPAIGN-002 requires a source-backed baseline before physical interpretation.",
    ),
    (
        "RT-CAMPAIGN-002-SRC-DECOH-002",
        "What source grounds environmental decoherence in matter-wave interferometry?",
        "CAMPAIGN-002 cannot treat the toy baseline as physical without source support.",
    ),
    (
        "RT-CAMPAIGN-002-SRC-DECOH-003",
        "What source defines experimental visibility thresholds for mesoscopic interferometry?",
        "Detectability needs a source-backed epsilon_exp before any physical claim.",
    ),
    (
        "RT-CAMPAIGN-002-SRC-DECOH-004",
        "What benchmark data can provide y_true for a toy or source-backed comparison?",
        "Predictive Gain is undefined without y_true or benchmark target data.",
    ),
]


def create_campaign_002_research_tasks(root_dir: Path) -> list[str]:
    existing_ids = {task.task_id for task in list_research_tasks(root_dir)}
    created_or_existing: list[str] = []

    for task_id, question, reason in RAG_TASKS_V06:
        if task_id not in existing_ids:
            save_research_task(
                ResearchTask(
                    task_id=task_id,
                    question=question,
                    reason=reason,
                    linked_gap_id=f"GAP_{task_id}",
                    required_source_types=["PAPER", "BOOK"],
                    priority="P1",
                    expected_output="SOURCE_RECORDS",
                    status="AWAITING_SOURCE_INGESTION",
                ),
                root_dir,
            )
        created_or_existing.append(task_id)

    return created_or_existing


def build_campaign_002_spec(campaign_input: Campaign002Input) -> ModelComparisonSpec:
    coupling = default_boundary_coupling_spec("B")
    return ModelComparisonSpec(
        comparison_id=campaign_input.comparison_id,
        campaign_id=campaign_input.campaign_id,
        system_id=campaign_input.system_id,
        observable=campaign_input.observable,
        t=campaign_input.t,
        parameters={
            "gamma_base": campaign_input.gamma_base,
            "alpha": campaign_input.alpha,
            "B": campaign_input.B,
            "QB": campaign_input.QB,
        },
        model_base_name="TOY_BASE_EXPONENTIAL_VISIBILITY",
        model_candidate_name="TOY_BOUNDARY_AWARE_VISIBILITY",
        model_base_description="V_base(t)=exp(-gamma_base*t). Toy baseline only.",
        model_candidate_description="V_C(t)=exp(-(gamma_base + alpha*B)*t). Toy candidate only.",
        error_metric=campaign_input.error_metric,
        epsilon_exp=campaign_input.epsilon_exp,
        y_true=campaign_input.y_true,
        source_ids=[],
        benchmark_ids=[],
        claim_ids=["CLAIM-DECOH-001"],
        status="TOY_MODEL_COMPARISON",
        boundary_coupling=coupling,
    )


def run_campaign_002_decoherence_model_comparison(
    root_dir: Path,
    campaign_input: Campaign002Input | None = None,
) -> Campaign002Result:
    campaign_input = campaign_input or Campaign002Input()
    spec = build_campaign_002_spec(campaign_input)
    comparison = run_model_comparison(spec)
    task_ids = create_campaign_002_research_tasks(root_dir)

    model_report_path = generate_model_comparison_report(spec, comparison, root_dir)
    report_path = generate_campaign_002_report(spec, comparison, task_ids, root_dir)
    rag_report_path = generate_foundational_source_ingestion_reports(root_dir, task_ids)

    return Campaign002Result(
        campaign_id=campaign_input.campaign_id,
        comparison=comparison,
        mode=spec.status,
        inherited_bound=f"CAMPAIGN-001 B = {campaign_input.B:.6e}; region = NEGATIVE_GRAVITY_BOUND",
        report_path=str(report_path),
        model_report_path=str(model_report_path),
        rag_report_path=str(rag_report_path),
        next_research_tasks=task_ids,
    )


def generate_campaign_002_report(
    spec: ModelComparisonSpec,
    result: ModelComparisonResult,
    task_ids: list[str],
    root_dir: Path,
) -> Path:
    report_dir = root_dir / "reports" / "campaigns"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "CAMPAIGN-002_decoherence_model_comparison.md"

    lines = [
        "# CAMPAIGN-002 — Decoherence Model Comparison",
        "",
        "## Scientific Question",
        "Can a boundary-aware toy candidate produce a quantified difference against a baseline decoherence toy model without violating CAMPAIGN-001 negative bounds?",
        "",
        "## CAMPAIGN-001 inherited bound",
        f"- B = {spec.parameters['B']:.6e}",
        "- Region = NEGATIVE_GRAVITY_BOUND",
        "- Direct gravitational decoherence overclaims remain blocked.",
        "",
        "## Model Base",
        f"- {spec.model_base_name}: {spec.model_base_description}",
        "",
        "## Model Candidate",
        f"- {spec.model_candidate_name}: {spec.model_candidate_description}",
        "",
        "## Observable",
        f"- {spec.observable}",
        "",
        "## Parameters",
        *[f"- {key}: {value}" for key, value in spec.parameters.items()],
        "",
        "## Source Status",
        "- AWAITING_SOURCE_INGESTION",
        "- No source-backed physical interpretation is allowed.",
        "",
        "## Benchmark Data",
        f"- y_true: {'provided' if spec.y_true is not None else 'not provided'}",
        "",
        "## Error Metric",
        f"- {spec.error_metric}",
        f"- error_base: {result.error_base if result.error_base is not None else 'undefined without y_true'}",
        f"- error_candidate: {result.error_candidate if result.error_candidate is not None else 'undefined without y_true'}",
        "",
        "## Gain_C",
        f"- {result.gain_c if result.gain_c is not None else 'undefined without y_true'}",
        f"- predictive_status: {result.predictive_status}",
        "",
        "## Detectability",
        f"- max_abs_delta: {result.max_abs_delta:.6e}",
        f"- detectability_status: {result.detectability_status}",
        "",
        "## Evidence Level",
        f"- Evidence Level: {result.evidence_level}",
        f"- Maximum Allowed Claim Level: {result.maximum_allowed_claim_level}",
        "",
        "## Allowed Claims",
        *[f"- {claim}" for claim in result.allowed_claims],
        "",
        "## Blocked Claims",
        *[f"- {claim}" for claim in result.blocked_claims],
        "",
        "## Safe Rewrite",
        "- Phygn computes a toy model delta under explicit assumptions. No physical decoherence prediction is claimed.",
        "",
        "## Next Required Research",
        *[f"- {task_id}" for task_id in task_ids],
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def generate_foundational_source_ingestion_reports(root_dir: Path, task_ids: list[str]) -> Path:
    report_dir = root_dir / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    sources = list_sources(root_dir)

    ingestion_path = report_dir / "foundational_source_ingestion.md"
    ingestion_lines = [
        "# RAG-SRC-001 — Foundational Source Ingestion",
        "",
        f"- Source records currently ingested: {len(sources)}",
        "- Status: AWAITING_SOURCE_INGESTION",
        "- No invented citations are present in this report.",
        "",
        "## Open Research Tasks",
        *[f"- {task_id}" for task_id in task_ids],
    ]
    ingestion_path.write_text("\n".join(ingestion_lines), encoding="utf-8")

    matrix_path = report_dir / "source_claim_matrix.md"
    matrix_lines = [
        "# Source Claim Matrix",
        "",
        "| Claim ID | Source IDs | Status | Note |",
        "|---|---|---|---|",
        "| CLAIM-DECOH-001 | none | BLOCKED | Requires dynamic model, sources, benchmark, Predictive Gain and detectability threshold. |",
    ]
    matrix_path.write_text("\n".join(matrix_lines), encoding="utf-8")

    awaiting_path = report_dir / "claims_awaiting_sources.md"
    awaiting_lines = [
        "# Claims Awaiting Sources",
        "",
        "- CLAIM-DECOH-001: remains blocked.",
        "- CAMPAIGN-002 toy comparison claims: require source ingestion for physical interpretation.",
    ]
    awaiting_path.write_text("\n".join(awaiting_lines), encoding="utf-8")

    return ingestion_path
