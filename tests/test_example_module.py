from pathlib import Path

from modular_registry_framework.main import build_context


def test_build_context_registers_example_module(tmp_path: Path):
    context = build_context(base_dir=tmp_path)

    assert "example" in context.registry.list_services()
    assert "example.overview" in context.registry.list_help_topics()
    assert context.registry.list_screens()[0].title == "Example Module"


def test_example_service_creates_items_and_emits_event(tmp_path: Path):
    context = build_context(base_dir=tmp_path)
    service = context.registry.get_service("example")
    seen = []
    context.registry.on("example.item_created", lambda payload: seen.append(payload["item"]))

    item = service.create_item("New thing")

    assert item.name == "New thing"
    assert seen == [item]

