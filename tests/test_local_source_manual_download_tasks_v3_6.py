from phyng.campaigns.phi_gradient_source_pack_population import run_phi_gradient_source_pack_population_campaign
from phyng.local_source_text.source_registry import build_local_source_text_registry


def test_missing_files_create_download_tasks(tmp_path):
    run_phi_gradient_source_pack_population_campaign(tmp_path)

    specs, _, _, _, _, tasks, _ = build_local_source_text_registry(tmp_path)

    assert len(tasks.tasks) == 5
    assert [task.priority for task in tasks.tasks] == [1, 2, 3, 4, 5]
    assert tasks.tasks[0].source_id == specs[0].source_id
    assert tasks.tasks[0].status == "DOWNLOAD_TASK_CREATED"
    assert tasks.tasks[0].target_path.endswith("Hornberger_2003_Collisional_Decoherence.pdf")
