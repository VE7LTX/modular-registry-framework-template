from pathlib import Path

from modular_registry_framework.scaffold import create_module, normalize_module_name


def test_normalize_module_name_creates_python_identifier():
    assert normalize_module_name("Report Builder") == "report_builder"
    assert normalize_module_name("123 Tools") == "module_123_tools"


def test_create_module_writes_standard_module_files(tmp_path: Path):
    modules_dir = tmp_path / "modules"

    target = create_module(modules_dir, "Report Builder", area="Reports", title="Report Builder")

    assert target == modules_dir / "report_builder"
    assert (target / "module.py").exists()
    assert (target / "service.py").exists()
    assert "registry.add_service" in (target / "module.py").read_text(encoding="utf-8")

