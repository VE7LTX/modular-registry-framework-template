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

## Core Rules

- `core/` should not import from feature modules.
- Feature screens can call feature services through `context.registry`.
- Services should avoid importing Tkinter or other UI packages.
- Events are for important cross-module actions, not every button click.
- Keep module loading explicit until dynamic loading solves a real problem.

## Verification

Run these before treating the template as healthy:

```powershell
python -m compileall modular_registry_framework tests
python -m pytest -q
```

