from __future__ import annotations

from modular_registry_framework.core.registry import Registry

from .models import ExampleItem


class ExampleService:
    def __init__(self, registry: Registry) -> None:
        self.registry = registry
        self._next_id = 1
        self._items: list[ExampleItem] = [
            ExampleItem(id=0, name="Example item", status="New"),
        ]

    def list_items(self) -> list[ExampleItem]:
        return list(self._items)

    def create_item(self, name: str, status: str = "New") -> ExampleItem:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Item name is required.")

        item = ExampleItem(id=self._next_id, name=clean_name, status=status)
        self._next_id += 1
        self._items.append(item)
        self.registry.emit("example.item_created", {"item": item})
        return item

