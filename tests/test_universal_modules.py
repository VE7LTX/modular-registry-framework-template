from pathlib import Path
import sqlite3

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
    assert "flow_graph" in modules
    assert "health_checks" in modules
    assert "env_secrets" in modules
    assert "storage" in modules
    assert "records" in modules
    assert "api_clients" in modules
    assert "runtime_trace" in modules
    assert "trace_graph" in modules
    assert "exporters" in modules
    assert "graph_export" in modules
    assert "workflows" in modules
    assert "recipes" in modules
    assert "ui_adapters" in modules
    assert "app_profiles" in modules


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
    assert "## System Flow Graph" in markdown


def test_flow_graph_renders_declared_inputs_outputs_and_edges(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    flow_graph = context.registry.get_service("flow_graph")

    mermaid = flow_graph.render_mermaid()
    adjacency = flow_graph.render_adjacency()

    assert "flowchart LR" in mermaid
    assert "input: files" in mermaid
    assert "output: import results" in mermaid
    assert "parse files" in adjacency
    assert "emit report event" in adjacency


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


def test_health_checks_run_registered_checks(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    health_checks = context.registry.get_service("health_checks")

    summary = health_checks.summary()

    assert summary["pass"] >= 1


def test_env_secrets_validate_and_redact(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    env_secrets = context.registry.get_service("env_secrets")
    env_secrets.require("MRF_TEST_SECRET", "Test Secret")
    (tmp_path / ".env").write_text("MRF_TEST_SECRET=abcdef\n", encoding="utf-8")

    rows = env_secrets.validate()

    assert rows[0]["present"] is True
    assert rows[0]["redacted"] == "ab****ef"


def test_storage_initializes_and_backs_up_sqlite(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    storage = context.registry.get_service("storage")

    storage.initialize()
    backup = storage.backup()

    assert storage.path.exists()
    assert backup.exists()


def test_records_create_and_archive_records(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    records = context.registry.get_service("records")

    record = records.create("case", {"name": "Alpha"})
    archived = records.archive(record.id)

    assert archived.archived is True
    assert records.list_records("case", include_archived=True)[0].values["name"] == "Alpha"


def test_api_clients_report_example_status(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    api_clients = context.registry.get_service("api_clients")

    statuses = api_clients.status_all()

    assert statuses[0].available is True


def test_runtime_trace_collects_events_with_trace_id(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    runtime_trace = context.registry.get_service("runtime_trace")
    trace_id = runtime_trace.new_trace_id()

    context.registry.emit("example.traced", {"trace_id": trace_id, "value": 1})

    assert runtime_trace.list_events(trace_id)[0].event_name == "example.traced"


def test_exporters_serialize_formats(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    exporters = context.registry.get_service("exporters")

    assert '"name": "Alpha"' in exporters.export("json", {"name": "Alpha"})
    assert "name" in exporters.export("csv", [{"name": "Alpha"}])
    assert "name:" in exporters.export("yaml", {"name": "Alpha"})


def test_graph_export_saves_mermaid_and_json(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    graph_export = context.registry.get_service("graph_export")

    mermaid = graph_export.save_mermaid()
    graph_json = graph_export.save_json()

    assert mermaid.path.exists()
    assert graph_json.path.exists()


def test_dependency_and_graph_quality_health_checks_pass(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    health_checks = context.registry.get_service("health_checks")

    results = {result.name: result for result in health_checks.run_all()}

    assert results["modules.dependencies"].status == "pass"
    assert results["flow_graph.quality"].status == "pass"


def test_trace_id_propagates_through_job_import_artifact_report_and_export(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    trace_id = context.registry.get_service("runtime_trace").new_trace_id()
    jobs = context.registry.get_service("jobs")
    importers = context.registry.get_service("importers")
    reports = context.registry.get_service("reports")
    exporters = context.registry.get_service("exporters")
    artifacts = context.registry.get_service("artifact_library")
    csv_path = tmp_path / "items.csv"
    csv_path.write_text("name\nAlpha\n", encoding="utf-8")

    jobs.run_sync("traceable job", lambda: "done", trace_id=trace_id)
    importers.import_file(csv_path, trace_id=trace_id)
    artifacts.create_text_artifact("notes", "note.txt", "hello", trace_id=trace_id)
    reports.save_markdown("trace-report.md", "Trace Report", trace_id=trace_id)
    exporters.export_artifact("json", {"ok": True}, "trace-export.json", trace_id=trace_id)

    event_names = [event.event_name for event in context.registry.get_service("runtime_trace").list_events(trace_id)]

    assert "job.started" in event_names
    assert "file.imported" in event_names
    assert "artifact.created" in event_names
    assert "report.generated" in event_names
    assert "data.exported" in event_names


def test_audit_and_trace_events_persist_to_sqlite(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    storage = context.registry.get_service("storage")
    trace_id = context.registry.get_service("runtime_trace").new_trace_id()

    context.registry.emit("test.persisted", {"trace_id": trace_id})

    with sqlite3.connect(storage.path) as connection:
        audit_count = connection.execute("SELECT COUNT(*) FROM audit_events").fetchone()[0]
        trace_count = connection.execute("SELECT COUNT(*) FROM trace_events WHERE trace_id = ?", (trace_id,)).fetchone()[0]

    assert audit_count >= 1
    assert trace_count == 1


def test_template_generator_creates_starter_files(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    generator = context.registry.get_service("template_generator")
    target = tmp_path / "starter"

    generator.create_app("data_ingestion", target)

    assert (target / "README.md").exists()
    assert (target / "settings.json").exists()
    assert (target / "modules.txt").read_text(encoding="utf-8").splitlines()[0] == "storage"


def test_profiles_workflows_recipes_and_trace_graph(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    profiles = context.registry.get_service("app_profiles")
    workflows = context.registry.get_service("workflows")
    recipes = context.registry.get_service("recipes")
    trace_graph = context.registry.get_service("trace_graph")
    ui_adapters = context.registry.get_service("ui_adapters")

    assert "tui_shell" in profiles.modules_for("tui_tool")
    assert "`importers` import" in workflows.render("import_report_export")
    assert "flowchart LR" in workflows.render_mermaid("import_report_export")

    trace_id = workflows.run_demo("import_report_export")
    assert trace_id in trace_graph.render_text(trace_id)
    assert "workflow.completed" in trace_graph.render_mermaid(trace_id)

    artifact_path = recipes.run("csv_report")
    assert Path(artifact_path).exists()
    assert ui_adapters.coverage_summary()["modules"] >= 1


def test_template_generator_creates_cli_tui_and_tkinter_starters(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    generator = context.registry.get_service("template_generator")

    cli_target = generator.create_app("cli_tool", tmp_path / "cli")
    tui_target = generator.create_app("tui_tool", tmp_path / "tui")
    tk_target = generator.create_app("tkinter_tool", tmp_path / "tk")

    assert "command_palette" in (cli_target / "modules.txt").read_text(encoding="utf-8")
    assert "tui_shell" in (tui_target / "modules.txt").read_text(encoding="utf-8")
    assert "ui_adapters" in (tk_target / "modules.txt").read_text(encoding="utf-8")
