from pathlib import Path

from phyng.benchmarks.readiness import classify_benchmark_readiness
from phyng.benchmarks.schemas import BenchmarkDataset


def generate_benchmark_dataset_report(dataset: BenchmarkDataset, root_dir: Path) -> Path:
    report_dir = root_dir / "reports" / "benchmarks"
    report_dir.mkdir(parents=True, exist_ok=True)
    readiness = classify_benchmark_readiness(dataset)
    path = report_dir / f"{dataset.dataset_id}.md"
    lines = [
        f"# Benchmark Dataset: {dataset.dataset_id}",
        "",
        "## Dataset",
        f"- Name: {dataset.name}",
        f"- Observable: {dataset.observable}",
        f"- Points: {len(dataset.y_true)}",
        f"- Units: {dataset.units or 'unspecified'}",
        "",
        "## Provenance",
        f"- Type: {dataset.provenance_type}",
        f"- Source IDs: {', '.join(dataset.source_ids) if dataset.source_ids else 'none'}",
        f"- Generation method: {dataset.generation_method or 'none'}",
        f"- Extraction notes: {dataset.extraction_notes or 'none'}",
        "",
        "## Readiness",
        f"- Status: {readiness.readiness_status}",
        f"- Can compute gain: {readiness.can_compute_gain}",
        f"- Gain label: {readiness.gain_label or 'none'}",
        f"- Allowed claim level: {readiness.allowed_claim_level}",
        f"- Blocked reason: {readiness.blocked_reason or 'none'}",
        "",
        "## Allowed Uses",
        *[f"- {use}" for use in dataset.allowed_uses],
        "",
        "## Forbidden Uses",
        *[f"- {use}" for use in dataset.forbidden_uses],
        "",
        "## Uncertainty",
        f"- Present: {dataset.uncertainty is not None}",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def generate_benchmark_registry_report(
    datasets: list[BenchmarkDataset],
    root_dir: Path,
) -> Path:
    report_dir = root_dir / "reports" / "benchmarks"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / "benchmark_registry.md"
    lines = [
        "# Benchmark Registry",
        "",
        "| Dataset | Provenance | Readiness | Gain Label | Can Compute Gain |",
        "|---|---|---|---|---|",
    ]
    for dataset in datasets:
        readiness = classify_benchmark_readiness(dataset)
        lines.append(
            f"| {dataset.dataset_id} | {dataset.provenance_type} | "
            f"{readiness.readiness_status} | {readiness.gain_label or 'none'} | "
            f"{readiness.can_compute_gain} |"
        )
        generate_benchmark_dataset_report(dataset, root_dir)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
