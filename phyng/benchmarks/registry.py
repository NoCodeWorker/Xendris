import json
from pathlib import Path

from phyng.benchmarks.schemas import BenchmarkDataset


def add_benchmark_dataset(dataset: BenchmarkDataset, root_dir: Path) -> None:
    benchmarks_dir = root_dir / "benchmarks"
    benchmarks_dir.mkdir(parents=True, exist_ok=True)
    path = benchmarks_dir / f"{dataset.dataset_id}.json"
    path.write_text(dataset.model_dump_json(indent=2), encoding="utf-8")


def list_benchmark_datasets(root_dir: Path) -> list[BenchmarkDataset]:
    benchmarks_dir = root_dir / "benchmarks"
    if not benchmarks_dir.exists():
        return []

    datasets: list[BenchmarkDataset] = []
    for path in benchmarks_dir.glob("*.json"):
        try:
            datasets.append(BenchmarkDataset.model_validate(json.loads(path.read_text(encoding="utf-8"))))
        except Exception:
            continue
    return datasets


def get_benchmark_dataset(dataset_id: str, root_dir: Path) -> BenchmarkDataset | None:
    path = root_dir / "benchmarks" / f"{dataset_id}.json"
    if not path.exists():
        return None
    try:
        return BenchmarkDataset.model_validate(json.loads(path.read_text(encoding="utf-8")))
    except Exception:
        return None
