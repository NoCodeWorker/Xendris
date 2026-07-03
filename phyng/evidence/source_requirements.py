from pathlib import Path

from phyng.evidence.schemas import SourceRequirement
from phyng.rag.research_planner import list_research_tasks, save_research_task
from phyng.rag.schemas import ResearchTask


DEFAULT_SOURCE_REQUIREMENTS = [
    SourceRequirement(
        requirement_id="REQ-SRC-001",
        topic="Reduced Compton wavelength",
        reason="Ground lambda_C definition and quantum localization boundary language.",
        linked_claim_ids=[
            "CLAIM-QB-001",
            "CLAIM-QB-002",
            "CLAIM-ATLAS-QUANTUM-BOUNDARY",
        ],
        linked_campaign_ids=["CAMPAIGN-001"],
        required_trust_level="HIGH",
        required_source_types=["BOOK", "PAPER", "LECTURE_NOTES"],
        suggested_queries=["reduced Compton wavelength definition quantum mechanics"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-002",
        topic="Gravitational radius / Schwarzschild radius",
        reason="Ground rg and RS definitions and horizon boundary interpretation.",
        linked_claim_ids=["CLAIM-GRAV-001", "CLAIM-ATLAS-GRAV-BOUNDARY"],
        linked_campaign_ids=["CAMPAIGN-001"],
        required_trust_level="HIGH",
        required_source_types=["BOOK", "PAPER", "LECTURE_NOTES"],
        suggested_queries=["Schwarzschild radius gravitational radius definition"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-003",
        topic="Planck scale",
        reason="Ground Planck length, Planck mass and Planck crossing language.",
        linked_claim_ids=["CLAIM-PLANCK-001", "CLAIM-ATLAS-PLANCK-CROSSING"],
        linked_campaign_ids=["CAMPAIGN-001"],
        required_trust_level="HIGH",
        required_source_types=["BOOK", "PAPER", "LECTURE_NOTES"],
        suggested_queries=["Planck length Planck mass definition"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-004",
        topic="Compton-Schwarzschild related work",
        reason="Support novelty discipline and avoid overclaiming related work.",
        linked_claim_ids=["CLAIM-QB-RELATED-WORK", "CLAIM-NOVELTY-LIMITATION"],
        linked_campaign_ids=["CAMPAIGN-001"],
        required_trust_level="MEDIUM",
        required_source_types=["PAPER", "BOOK"],
        suggested_queries=["Compton Schwarzschild diagram related work"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-005",
        topic="Mesoscopic matter-wave interferometry",
        reason="Ground mass ranges, length scales and visibility context.",
        linked_claim_ids=["CLAIM-MESO-001", "CLAIM-MESO-MAQRO-LIKE"],
        linked_campaign_ids=["CAMPAIGN-001", "CAMPAIGN-002"],
        required_trust_level="HIGH",
        required_source_types=["PAPER"],
        suggested_queries=["mesoscopic matter wave interferometry nanoparticle visibility"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-006",
        topic="Environmental decoherence models",
        reason="Ground baseline visibility decay and standard decoherence comparison.",
        linked_claim_ids=[
            "CLAIM-DECOH-BASELINE-001",
            "CLAIM-CAMPAIGN-002-MODEL-BASE",
        ],
        linked_campaign_ids=["CAMPAIGN-002"],
        required_trust_level="HIGH",
        required_source_types=["PAPER", "BOOK"],
        suggested_queries=["environmental decoherence visibility decay matter wave interferometry"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-007",
        topic="Experimental visibility thresholds",
        reason="Ground epsilon_exp and detectability threshold interpretation.",
        linked_claim_ids=["CLAIM-DETECTABILITY-001", "CLAIM-CAMPAIGN-002-EPSILON"],
        linked_campaign_ids=["CAMPAIGN-002"],
        required_trust_level="HIGH",
        required_source_types=["PAPER"],
        suggested_queries=["experimental visibility threshold matter wave interferometry"],
    ),
    SourceRequirement(
        requirement_id="REQ-SRC-008",
        topic="Benchmark or data source",
        reason="Ground y_true, benchmark curve and error metric comparison.",
        linked_claim_ids=["CLAIM-GAIN-001", "CLAIM-CAMPAIGN-002-PREDICTIVE-GAIN"],
        linked_campaign_ids=["CAMPAIGN-002"],
        required_trust_level="HIGH",
        required_source_types=["PAPER", "DATASET"],
        suggested_queries=["matter wave interferometry visibility benchmark data"],
    ),
]


def default_source_requirements() -> list[SourceRequirement]:
    return [SourceRequirement.model_validate(req.model_dump()) for req in DEFAULT_SOURCE_REQUIREMENTS]


def create_research_tasks_for_requirements(
    requirements: list[SourceRequirement],
    root_dir: Path,
) -> list[str]:
    existing_ids = {task.task_id for task in list_research_tasks(root_dir)}
    created_or_existing: list[str] = []

    for requirement in requirements:
        task_id = f"RT-{requirement.requirement_id}"
        if task_id not in existing_ids:
            save_research_task(
                ResearchTask(
                    task_id=task_id,
                    question=f"What source satisfies {requirement.topic} for Phygn claims?",
                    reason=requirement.reason,
                    linked_gap_id=requirement.requirement_id,
                    required_source_types=requirement.required_source_types,
                    priority="P1",
                    expected_output="SOURCE_RECORDS",
                    status="AWAITING_SOURCE_INGESTION",
                ),
                root_dir,
            )
        created_or_existing.append(task_id)

    return created_or_existing
