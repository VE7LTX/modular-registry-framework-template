# Development Workflow

Use this project as a living template. Keep the core small, put real feature code inside modules, and only add new registry contribution points when more than one module needs them.

## Add A Feature Module

1. Generate a module folder.

   ```powershell
   python -m modular_registry_framework.scaffold inventory --area Inventory --title "Inventory"
   ```

2. Add the module to `modular_registry_framework/modules/__init__.py`.

   ```python
   from .inventory import module as inventory

   MODULES = (example, inventory)
   ```

3. Put business logic in `service.py`.
4. Put UI assembly in `screens.py`.
5. Put user-facing help in `help.py`.
6. Register only stable contribution points in `module.py`.
7. Declare traceability with `add_data_input()`, `add_data_output()`, and `add_flow()`.
8. Add focused service tests before broad UI work.

## Core Rules

- `core/` should not import from feature modules.
- Feature screens can call feature services through `context.registry`.
- Services should avoid importing Tkinter or other UI packages.
- Events are for important cross-module actions, not every button click.
- Keep module loading explicit until dynamic loading solves a real problem.
- Debug/logging is core-level and inherited by modules through the root logger.
- New modules should declare inputs, outputs, and flow edges so the graph stays useful.

## Module Checklist

Before a module is considered complete:

- `module.py` registers `ModuleMetadata`.
- service logic lives in `service.py`.
- screens are thin and call services.
- help topics explain what the module does.
- settings include labels and help text.
- meaningful events are emitted after important outcomes.
- inputs, outputs, and flows are declared for traceability.
- debug logs exist around important operations.
- trace-aware operations accept or create `trace_id`.
- tests cover service behavior and registry contributions.
- docs mention new public contribution points.

## Verification

Run these before treating the template as healthy:

```powershell
python -m compileall modular_registry_framework tests
python -m pytest -q
```
