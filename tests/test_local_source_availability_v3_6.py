from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.local_source_text.source_registry import build_local_source_text_registry


def test_all_missing_status(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)

    _, registry, _, _, availability, tasks, blocked = build_local_source_text_registry(tmp_path)

    assert blocked is None
    assert registry.registry_status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_MISSING"
    assert registry.missing_count == 5
    assert len(tasks.tasks) == 5
    assert all(item.availability_status == "SOURCE_FILE_REQUIRES_MANUAL_DOWNLOAD" for item in availability.availability)


def test_partial_available_status(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)
    _, registry_seed, _, _, _, _, _ = build_local_source_text_registry(tmp_path)
    first = registry_seed.source_records[0]
    target = tmp_path / first.local_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(b"%PDF-1.4\npartial source\n")

    _, registry, _, hashes, _, tasks, _ = build_local_source_text_registry(tmp_path)

    assert population.status == "PHI_GRADIENT_SOURCE_PACK_POPULATED"
    assert registry.registry_status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_PARTIAL"
    assert registry.available_count == 1
    assert len(hashes.hashes) == 1
    assert len(tasks.tasks) == 4


def test_all_ready_status(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)
    specs, _, _, _, _, _, _ = build_local_source_text_registry(tmp_path)
    for spec in specs:
        target = tmp_path / spec.target_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(f"%PDF-1.4\n{spec.source_id}\n".encode("utf-8"))

    _, registry, _, hashes, _, tasks, _ = build_local_source_text_registry(tmp_path)

    assert registry.registry_status == "PHI_GRADIENT_LOCAL_SOURCE_FILES_READY"
    assert registry.available_count == 5
    assert len(hashes.hashes) == 5
    assert len(tasks.tasks) == 0
