from pathlib import Path

from modular_registry_framework.main import build_context


def test_context_registers_universal_modules(tmp_path: Path):
    context = build_context(base_dir=tmp_path)

    modules = context.registry.list_modules()

    assert "dashboard" in modules
    assert "audit_log" in modules
    assert "settings_manager" in modules
    assert "diagnostics" in modules
    assert "artifact_library" in modules
    assert "jobs" in modules
    assert "importers" in modules
    assert "reports" in modules
    assert "help" in modules


def test_audit_log_records_registry_events(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    audit_log = context.registry.get_service("audit_log")

    context.registry.emit("test.event", {"value": 42})

    assert audit_log.list_events(limit=1)[0].event_name == "test.event"


def test_artifact_library_creates_text_artifacts(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    artifacts = context.registry.get_service("artifact_library")

    record = artifacts.create_text_artifact("reports", "summary.md", "# Summary")

    assert record.path.exists()
    assert record.path.read_text(encoding="utf-8") == "# Summary"


def test_jobs_run_sync_records_completed_job(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    jobs = context.registry.get_service("jobs")

    job = jobs.run_sync("example", lambda: "done")

    assert job.status == "completed"
    assert job.result == "done"


def test_importers_load_registered_file_formats(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    importers = context.registry.get_service("importers")
    csv_path = tmp_path / "items.csv"
    jsonl_path = tmp_path / "items.jsonl"
    yaml_path = tmp_path / "settings.yaml"
    xml_path = tmp_path / "root.xml"
    csv_path.write_text("name,status\nAlpha,New\n", encoding="utf-8")
    jsonl_path.write_text('{"name": "Alpha"}\n', encoding="utf-8")
    yaml_path.write_text("app.name: Template\napp.enabled: true\n", encoding="utf-8")
    xml_path.write_text("<root><child /></root>", encoding="utf-8")

    assert importers.import_file(csv_path).data == [{"name": "Alpha", "status": "New"}]
    assert importers.import_file(jsonl_path).data == [{"name": "Alpha"}]
    assert importers.import_file(yaml_path).data == {"app.name": "Template", "app.enabled": True}
    assert importers.import_file(xml_path).data["children"] == ["child"]


def test_reports_render_registered_sections(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    reports = context.registry.get_service("reports")

    markdown = reports.render_markdown("System Report")

    assert "# System Report" in markdown
    assert "## Module Inventory" in markdown
    assert "## Registered Capabilities" in markdown


def test_diagnostics_toggle_debug_mode(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    diagnostics = context.registry.get_service("diagnostics")

    diagnostics.set_debug_enabled(True)

    assert context.settings.get("debug.enabled") is True
    assert context.settings.get("logging.level") == "DEBUG"
    assert context.settings.get("logging.file_enabled") is True


def test_debug_mode_writes_core_logs_to_file(tmp_path: Path):
    (tmp_path / "settings.json").write_text(
        """
{
  "debug.enabled": true,
  "logging.level": "DEBUG",
  "logging.console_enabled": false,
  "logging.file_enabled": true,
  "logging.file": "logs/app.log"
}
""".strip(),
        encoding="utf-8",
    )

    context = build_context(base_dir=tmp_path)
    context.registry.emit("test.logging", {"ok": True})

    log_text = (tmp_path / "logs" / "app.log").read_text(encoding="utf-8")
    assert "Building app context" in log_text
    assert "Registered module" in log_text
    assert "Emitting event test.logging" in log_text


def test_settings_manager_saves_current_settings(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    settings_manager = context.registry.get_service("settings_manager")
    output_path = tmp_path / "saved-settings.yaml"

    settings_manager.set_value("debug.enabled", True)
    settings_manager.save(output_path)

    assert output_path.exists()
    assert "debug.enabled: true" in output_path.read_text(encoding="utf-8")
