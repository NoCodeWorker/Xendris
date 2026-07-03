"""
Integration tests for phyng.campaigns.baseline_source_pack_ingestion
(BASELINE-SRC-PACK-001 v1.0 full pipeline)
"""

import json
from pathlib import Path

import pytest

from phyng.baselines.limited_upgrade_execution import run_limited_upgrade_execution
from phyng.campaigns.baseline_source_pack_ingestion import main


class TestBaselineSourcePackIngestionV1:
    """Full-pipeline integration tests for BASELINE-SRC-PACK-001."""

    # ── Empty / no-source scenarios ─────────────────────────────────────

    def test_empty_baseline_does_not_upgrade(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert result.upgrade_success is False
        assert "REQUIRES_SOURCE" in result.baseline_after

    def test_url_only_source_does_not_upgrade(self, tmp_path: Path) -> None:
        baseline = tmp_path / "sources" / "baseline"
        baseline.mkdir(parents=True)
        manifest = [
            {
                "source_candidate_id": "CAND-URL",
                "requirement_id": "BSR-001",
                "title": "URL-Only Paper",
                "authors": ["Author X"],
                "year": "2024",
                "source_type": "PAPER",
                "local_path": None,
                "url": "https://example.com/paper.pdf",
                "trust_level": "HIGH",
                "notes": "URL only — no local file.",
            }
        ]
        (baseline / "source_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert result.upgrade_success is False
        assert result.audited_sources_count == 0

    # ── Report generation ───────────────────────────────────────────────

    def test_six_reports_always_generated(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        result = run_limited_upgrade_execution(project_root=tmp_path)
        assert len(result.report_paths) == 6

    def test_rag_reports_exist(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        run_limited_upgrade_execution(project_root=tmp_path)
        rag = tmp_path / "reports" / "rag"
        assert (rag / "baseline_source_pack_v1_0.md").exists()
        assert (rag / "baseline_support_matrix_v1_0.md").exists()
        assert (rag / "citation_audit_v1_0.md").exists()

    def test_campaign_reports_exist(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        run_limited_upgrade_execution(project_root=tmp_path)
        camp = tmp_path / "reports" / "campaigns"
        assert (camp / "BASELINE-SRC-PACK-001_ingestion_result.md").exists()
        assert (camp / "CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md").exists()

    def test_model_comparison_report_exists(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        run_limited_upgrade_execution(project_root=tmp_path)
        comp = tmp_path / "reports" / "model_comparison"
        assert (comp / "CAMPAIGN-002_source_backed_baseline_status_v1_0.md").exists()

    def test_ingestion_result_mentions_blocked_claims(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        run_limited_upgrade_execution(project_root=tmp_path)
        report = (
            tmp_path / "reports" / "campaigns" / "BASELINE-SRC-PACK-001_ingestion_result.md"
        ).read_text(encoding="utf-8")
        assert "Blocked Claims" in report

    # ── Physical prediction always blocked ──────────────────────────────

    def test_physical_prediction_blocked_in_result(self, tmp_path: Path) -> None:
        result = run_limited_upgrade_execution(project_root=tmp_path)
        blocked_text = " ".join(result.blocked_claims).lower()
        assert "predict" in blocked_text or "validated" in blocked_text

    def test_upgrade_attempt_report_says_blocked(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        run_limited_upgrade_execution(project_root=tmp_path)
        content = (
            tmp_path / "reports" / "campaigns" / "CAMPAIGN-002_baseline_upgrade_attempt_v1_0.md"
        ).read_text(encoding="utf-8")
        assert "can_claim_physical_prediction = False" in content

    # ── Campaign runner (CLI entrypoint) ────────────────────────────────

    def test_main_runs_without_exception(self, tmp_path: Path, capsys) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        main(project_root=tmp_path)
        captured = capsys.readouterr()
        assert "BASELINE-SRC-PACK-001" in captured.out

    def test_main_prints_blocked_claims(self, tmp_path: Path, capsys) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        main(project_root=tmp_path)
        captured = capsys.readouterr()
        assert "Blocked Claims" in captured.out

    # ── Idempotency ─────────────────────────────────────────────────────

    def test_run_twice_is_idempotent(self, tmp_path: Path) -> None:
        (tmp_path / "sources" / "baseline").mkdir(parents=True)
        r1 = run_limited_upgrade_execution(project_root=tmp_path)
        r2 = run_limited_upgrade_execution(project_root=tmp_path)
        assert r1.baseline_after == r2.baseline_after
        assert r1.upgrade_success == r2.upgrade_success
