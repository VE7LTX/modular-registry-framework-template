# Modular Registry Framework

A lightweight Python template for building local apps from a small core and feature modules.

This project was split out from the original architecture note in `docs/architecture.md` so the pattern can be developed as its own reusable template system.

## What Is Here

- `modular_registry_framework/core/registry.py` - capability registry for services, screens, settings, help topics, commands, and events
- `modular_registry_framework/core/context.py` - shared runtime context passed into modules and screens
- `modular_registry_framework/modules/example/` - minimal example feature module
- `modular_registry_framework/desktop/shell.py` - small Tkinter shell that builds navigation from registered screens
- `modular_registry_framework/scaffold.py` - CLI for creating a new module folder from the standard file pattern
- `docs/architecture.md` - original architecture document

## Run The Example App

```powershell
cd modular-registry-framework
python -m modular_registry_framework.main
```

## Scaffold A Module

```powershell
cd modular-registry-framework
python -m modular_registry_framework.scaffold inventory --area Inventory --title "Inventory"
```

This creates:

```text
modular_registry_framework/modules/inventory/
  __init__.py
  module.py
  service.py
  screens.py
  fields.py
  help.py
  models.py
```

Then add the generated module to `modular_registry_framework/modules/__init__.py`.

## Verify

```powershell
python -m compileall modular_registry_framework tests
python -m pytest -q
```

