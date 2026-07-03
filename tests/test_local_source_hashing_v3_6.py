import hashlib

from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.local_source_text.file_discovery import discover_local_source_files
from phyng.local_source_text.hashing import sha256_file
from phyng.local_source_text.source_registry import build_priority_local_source_specs


def test_existing_file_gets_sha256(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)
    specs = build_priority_local_source_specs(population.population_result.manifest)
    payload = b"local source text placeholder for hash only"
    target = tmp_path / specs[0].target_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)

    records = discover_local_source_files(specs, tmp_path)

    assert records[0].sha256 == hashlib.sha256(payload).hexdigest()
    assert sha256_file(target) == records[0].sha256
