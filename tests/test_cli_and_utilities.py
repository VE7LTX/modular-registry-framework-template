from pathlib import Path

from modular_registry_framework.cli import main as cli_main
from modular_registry_framework.main import build_context


def test_workspace_scanner_detects_project_signals(tmp_path: Path):
    project = tmp_path / "ExampleProject"
    project.mkdir()
    (project / ".git").mkdir()
    (project / "README.md").write_text("# Example", encoding="utf-8")
    (project / "app.py").write_text("print('hi')", encoding="utf-8")
    (project / "tests").mkdir()
    (project / "tests" / "test_app.py").write_text("def test_app(): pass", encoding="utf-8")

    scanner = build_context(base_dir=tmp_path).registry.get_service("workspace_scanner")
    scans = scanner.scan_workspace(tmp_path)
    scan = next(item for item in scans if item.name == "ExampleProject")

    assert scan.has_git is True
    assert scan.has_readme is True
    assert scan.python_files == 2


def test_secret_scanner_redacts_findings(tmp_path: Path):
    source = tmp_path / "settings.py"
    source.write_text("API_KEY = 'abcdef123456'\n", encoding="utf-8")

    scanner = build_context(base_dir=tmp_path).registry.get_service("secret_scanner")
    findings = scanner.scan(tmp_path)

    assert findings[0].redacted == "abc****456"


def test_module_test_harness_writes_registration_test(tmp_path: Path):
    harness = build_context(base_dir=tmp_path).registry.get_service("module_test_harness")

    path = harness.write_registration_test("example", tmp_path / "tests")

    assert path.exists()
    assert "test_example_module_registers" in path.read_text(encoding="utf-8")


def test_runbook_generator_renders_operational_sections(tmp_path: Path):
    runbook = build_context(base_dir=tmp_path).registry.get_service("runbook_generator").render_markdown()

    assert "# Application Runbook" in runbook
    assert "## Health Checks" in runbook


def test_module_packs_include_data_ingestion(tmp_path: Path):
    packs = build_context(base_dir=tmp_path).registry.get_service("module_packs").list_packs()

    assert "data_ingestion" in packs
    assert "storage" in packs["data_ingestion"].modules


def test_cli_health_outputs_results(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli_main(["health"]) == 0

    output = capsys.readouterr().out
    assert "modules.dependencies" in output


def test_cli_module_test_outputs_pytest(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli_main(["module-test", "example"]) == 0

    output = capsys.readouterr().out
    assert "test_example_module_registers" in output


def test_view_models_command_palette_and_tui_render(tmp_path: Path):
    context = build_context(base_dir=tmp_path)

    modules_text = context.registry.get_service("view_models").modules_table().render_text()
    commands = context.registry.get_service("command_palette").search("health")
    tui = context.registry.get_service("tui_shell").render_dashboard()

    assert "Modules" in modules_text
    assert any(command.name == "view.health" for command in commands)
    assert "Modular Registry Framework TUI" in tui


def test_settings_editor_updates_values(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    editor = context.registry.get_service("settings_editor")

    value = editor.set_from_text("debug.enabled", "true")

    assert value is True
    assert context.settings.get("debug.enabled") is True


def test_log_viewer_tails_configured_log(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    log_path = tmp_path / "logs" / "app.log"
    log_path.parent.mkdir()
    log_path.write_text("2026 INFO app: hello\n2026 ERROR app: nope\n", encoding="utf-8")

    lines = context.registry.get_service("log_viewer").tail(level="ERROR")

    assert lines == ["2026 ERROR app: nope"]


def test_artifact_browser_lists_and_previews(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    artifact = context.registry.get_service("artifact_library").create_text_artifact("notes", "note.md", "# Note")
    browser = context.registry.get_service("artifact_browser")

    assert artifact.path in browser.list_files()
    assert browser.preview(artifact.path) == "# Note"


def test_project_repair_plans_and_applies_baseline(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    repair = context.registry.get_service("project_repair")
    target = tmp_path / "rough_project"

    plan = repair.plan(target)
    written = repair.apply_baseline(target)

    assert "create README.md" in plan
    assert target / "README.md" in written


def test_cli_tui_and_commands_output(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli_main(["tui"]) == 0
    assert "Modular Registry Framework TUI" in capsys.readouterr().out

    assert cli_main(["commands", "health"]) == 0
    assert "view.health" in capsys.readouterr().out


def test_cli_repair_apply_writes_baseline(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    target = tmp_path / "rough"

    assert cli_main(["repair", "apply", str(target)]) == 0

    assert (target / ".gitignore").exists()
    assert "Wrote" in capsys.readouterr().out


def test_cli_profiles_workflows_ui_trace_and_recipes(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli_main(["profiles", "tui_tool"]) == 0
    assert "TUI Tool" in capsys.readouterr().out

    assert cli_main(["workflows", "import_report_export", "--mermaid"]) == 0
    assert "flowchart LR" in capsys.readouterr().out

    assert cli_main(["ui"]) == 0
    assert "UI Adapter Coverage" in capsys.readouterr().out

    assert cli_main(["trace-graph"]) == 0
    assert "No traced runtime events" in capsys.readouterr().out

    assert cli_main(["recipes"]) == 0
    assert "csv_report" in capsys.readouterr().out


def test_cli_recipe_run_creates_artifact(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert cli_main(["recipes", "csv_report", "--run"]) == 0

    output = capsys.readouterr().out
    assert "csv_report" in output
    assert any((tmp_path / "artifacts" / "recipes").glob("csv_report-*.md"))
