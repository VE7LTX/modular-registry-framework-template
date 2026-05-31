from __future__ import annotations

from pathlib import Path


class ModuleTestHarnessService:
    def render_registration_test(self, module_name: str) -> str:
        safe_name = module_name.strip().lower()
        return f'''from pathlib import Path

from modular_registry_framework.main import build_context


def test_{safe_name}_module_registers(tmp_path: Path):
    context = build_context(base_dir=tmp_path)

    assert "{safe_name}" in context.registry.list_modules()
    assert "{safe_name}" in context.registry.list_services()
    assert any(port.module == "{safe_name}" for port in context.registry.list_data_ports())
'''

    def write_registration_test(self, module_name: str, tests_dir: Path) -> Path:
        tests_dir.mkdir(parents=True, exist_ok=True)
        path = tests_dir / f"test_{module_name.strip().lower()}_module.py"
        path.write_text(self.render_registration_test(module_name), encoding="utf-8")
        return path

