from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.local_source_text.source_registry import build_priority_local_source_specs


def test_priority_source_records_created(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)

    specs = build_priority_local_source_specs(population.population_result.manifest)

    assert len(specs) == 5
    assert specs[0].source_id == "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE"
    assert specs[0].preferred_filename == "Hornberger_2003_Collisional_Decoherence.pdf"
    assert specs[0].target_path.endswith("data\\real_sources\\pdfs\\Hornberger_2003_Collisional_Decoherence.pdf") or specs[0].target_path.endswith("data/real_sources/pdfs/Hornberger_2003_Collisional_Decoherence.pdf")
    assert specs[0].known_identifiers["arxiv_id"] == "quant-ph/0303093"
