from pathlib import Path

from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.local_source_text.file_discovery import discover_local_source_files
from phyng.local_source_text.source_registry import build_priority_local_source_specs


def test_existing_file_records_size_and_type(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)
    specs = build_priority_local_source_specs(population.population_result.manifest)
    target = tmp_path / specs[0].target_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"%PDF-1.4\nlocal test file\n")

    records = discover_local_source_files(specs, tmp_path)
    first = records[0]

    assert first.exists
    assert first.file_type == ".pdf"
    assert first.size_bytes == len(b"%PDF-1.4\nlocal test file\n")


def test_url_or_arxiv_does_not_count_as_local_file(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)
    specs = build_priority_local_source_specs(population.population_result.manifest)

    records = discover_local_source_files(specs, tmp_path)

    assert all(not record.exists for record in records)
    assert all(record.sha256 is None for record in records)
    assert all(record.registry_status == "LOCAL_SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD" for record in records)
