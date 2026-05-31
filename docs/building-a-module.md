# Building A Module

A module owns one feature area. Keep everything related to that feature together.

```text
modules/inventory/
  __init__.py
  module.py
  service.py
  screens.py
  fields.py
  help.py
  models.py
```

## module.py

`module.py` is the registration entry point.

```python
def register(registry, context):
    registry.add_module(...)
    registry.add_service("inventory", InventoryService(context))
    registry.add_screen("Inventory", "Inventory", build_inventory_screen)
    registry.add_help_topic("inventory.overview", "...")
```

This file should describe what the module contributes. It should not contain business logic.

## service.py

Services do work:

- validate input
- read and write data
- call APIs
- parse files
- generate artifacts
- emit important events

Screens call services. Tests should usually target services first.

## screens.py

Screens build UI and call services. A screen should avoid direct SQL, API calls, and large business rules.

## fields.py

Use this for field labels, choices, validation rules, table columns, or form metadata. Keeping field definitions beside the feature avoids duplicated labels and mismatched validation.

## help.py

Help topics live beside the feature they explain. The built-in help module collects them.

## models.py

Use dataclasses or typed objects for records passed between services, screens, importers, reports, and tests.

