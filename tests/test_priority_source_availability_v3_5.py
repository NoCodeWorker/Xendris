from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.priority_exact_fill.source_availability import classify_priority_source_availability, select_priority_sources


def test_priority_sources_are_selected(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)

    selected = select_priority_sources(population.population_result.manifest)

    assert len(selected) == 5
    assert selected[0][0] == "SRC-HORNBERGER-2003-COLLISIONAL-DECOHERENCE"
    assert {entry.source_id for _, entry in selected if entry} == {
        "SRC-PHI-V32-001",
        "SRC-PHI-V32-002",
        "SRC-PHI-V32-005",
        "SRC-PHI-V32-009",
        "SRC-PHI-V32-010",
    }


def test_source_text_unavailable_does_not_fabricate_extract(tmp_path):
    population = run_phi_gradient_source_pack_population_campaign(tmp_path)

    records = classify_priority_source_availability(population.population_result.manifest, tmp_path)

    assert records
    assert all(record.source_text_status == "SOURCE_TEXT_REQUIRES_MANUAL_DOWNLOAD" for record in records)
    assert all("not exact source text" in " ".join(record.notes) for record in records)
