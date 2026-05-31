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
