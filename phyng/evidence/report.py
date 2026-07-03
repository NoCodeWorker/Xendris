from pathlib import Path

from phyng.evidence.schemas import SourceRequirement
from phyng.rag.research_planner import list_research_tasks
from phyng.rag.source_registry import list_sources


def generate_source_requirements_report(
    requirements: list[SourceRequirement],
    root_dir: Path,
) -> Path:
    report_dir = root_dir / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "source_requirements.md"
    lines = [
        "# Source Requirements",
        "",
        "| Requirement | Topic | Trust | Status | Claims |",
        "|---|---|---|---|---|",
        *[
            (
                f"| {req.requirement_id} | {req.topic} | {req.required_trust_level} | "
                f"{req.status} | {', '.join(req.linked_claim_ids)} |"
            )
            for req in requirements
        ],
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def generate_evidence_reports(
    requirements: list[SourceRequirement],
    root_dir: Path,
) -> dict[str, Path]:
    report_dir = root_dir / "reports" / "rag"
    report_dir.mkdir(parents=True, exist_ok=True)
    sources = list_sources(root_dir)
    tasks = list_research_tasks(root_dir)
    paths: dict[str, Path] = {}
    paths["source_requirements"] = generate_source_requirements_report(requirements, root_dir)

    foundational = report_dir / "foundational_source_ingestion.md"
    foundational.write_text(
        "\n".join(
            [
                "# RAG-SRC-001 — Foundational Source Ingestion",
                "",
                f"- Source records currently ingested: {len(sources)}",
                f"- Source requirements tracked: {len(requirements)}",
                f"- Research tasks tracked: {len(tasks)}",
                "- Status: AWAITING_SOURCE_INGESTION",
                "- No invented citations are present in this report.",
            ]
        ),
        encoding="utf-8",
    )
    paths["foundational_source_ingestion"] = foundational

    matrix = report_dir / "source_claim_matrix.md"
    matrix.write_text(
        "\n".join(
            [
                "# Source Claim Matrix",
                "",
                "| Claim ID | Requirement | Status | Note |",
                "|---|---|---|---|",
                *[
                    f"| {claim_id} | {req.requirement_id} | REQUIRES_SOURCE | No direct source link audited. |"
                    for req in requirements
                    for claim_id in req.linked_claim_ids
                ],
            ]
        ),
        encoding="utf-8",
    )
    paths["source_claim_matrix"] = matrix

    awaiting = report_dir / "claims_awaiting_sources.md"
    awaiting.write_text(
        "\n".join(
            [
                "# Claims Awaiting Sources",
                "",
                *[
                    f"- {claim_id}: awaiting {req.requirement_id} ({req.topic})."
                    for req in requirements
                    for claim_id in req.linked_claim_ids
                ],
            ]
        ),
        encoding="utf-8",
    )
    paths["claims_awaiting_sources"] = awaiting

    unlocked = report_dir / "claims_unlocked_by_sources.md"
    unlocked.write_text(
        "\n".join(
            [
                "# Claims Unlocked By Sources",
                "",
                "- None.",
                "- No hard physical claim is unlocked without direct audited support.",
            ]
        ),
        encoding="utf-8",
    )
    paths["claims_unlocked_by_sources"] = unlocked
    return paths
