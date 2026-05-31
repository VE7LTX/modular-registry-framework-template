# Modular Registry Framework

A lightweight Python app template for building local tools from a small core and feature modules.

This project is inspired by Drupal's module, hook, and service ideas, but it is not Drupal and does not copy Drupal code. The useful idea is the architecture: the app provides a host, and each feature module registers what it contributes.

The goal is to keep future apps from turning into one giant file.

## Why This Exists

Small internal tools often start clean:

- one script
- one window
- one database table
- one import flow
- one report

That works until the tool becomes useful. Then more screens, settings, reports, file handlers, API calls, and special cases get added. Without structure, everything starts to mix together:

- UI code talks directly to database code
- labels, fields, and validation rules get copied in multiple places
- changing one feature breaks another feature
- business logic cannot be tested without opening the app
- new screens require editing the central app shell
- old features become hard to remove
- future projects inherit the same messy patterns

This template gives growing apps a boring, repeatable structure before that happens.

## The Core Idea

The app is a host. Features are modules.

The core starts the app, creates shared runtime objects, loads modules, and builds the shell. Modules own their feature area and register the capabilities they provide.

```text
Application Core
  |
  |-- creates settings/database/context
  |-- creates the registry
  |-- loads modules
  |-- builds navigation from registered screens
  |-- emits important app events
  |
  +-- records module
  +-- reports module
  +-- imports module
  +-- settings module
```

The core does not need to know every detail of every feature. It only needs to know what modules registered.

## Drupal-Inspired, Python-Sized

Drupal proved that large systems can stay extensible when features contribute through clear module boundaries. This project borrows that style in a much smaller form:

- modules register screens, services, settings, help, commands, and event handlers
- services hold business logic
- screens build the UI and call services
- hooks/events let modules react to important actions
- the app shell builds itself from registered screens

This is not a CMS, plugin marketplace, web framework, or Drupal port. It is a practical pattern for local Python apps that are expected to grow.

## What This Helps With

This template is useful when you need to build:

- local engineering tools
- lab workflow apps
- inventory and asset tools
- QC/QA tracking apps
- report generators
- API control panels
- desktop apps with several screens
- business workflow tools that will keep evolving

It is probably too much for a one-off script, a tiny converter, or a throwaway prototype.

## How The Pieces Fit

### Registry

`modular_registry_framework/core/registry.py`

The registry is the directory of things modules provide. It can hold:

- services
- screens
- help topics
- settings
- commands
- event handlers

Modules register capabilities with the registry. The registry stores them. It should not contain business logic.

### App Context

`modular_registry_framework/core/context.py`

The context carries shared runtime objects such as:

- database connection
- settings
- registry
- base directory

Passing context into modules avoids global imports scattered across the app.

### Modules

`modular_registry_framework/modules/example/`

A module owns one feature area. A normal module has:

```text
module.py      registration entry point
service.py     business logic
screens.py     UI screen builders
fields.py      field definitions and validation metadata
help.py        help text and explanations
models.py      dataclasses or typed objects
```

The important file is `module.py`. It exposes a `register()` function:

```python
def register(registry, context):
    registry.add_service("records", RecordService(context.db))
    registry.add_screen("Records", "Record Library", build_record_screen, order=10)
    registry.add_help_topic("records.overview", RECORDS_HELP)
```

### Services

Services do the actual work:

- validate input
- read and write data
- import and export files
- calculate reports
- emit meaningful events

Services should not create UI widgets or show message boxes. That keeps business logic testable.

### Screens

Screens build the user interface:

- create widgets
- bind buttons and selections
- call services
- display user-facing messages
- refresh visible data

Screens should avoid direct SQL and heavy business rules.

### Events And Hooks

Events let modules react to important app actions without hard-coded imports.

Example events:

```text
app.started
app.shutdown
record.created
record.updated
file.imported
report.generated
api.unavailable
```

Use events for meaningful cross-module actions, not every small UI click.

## What Is In This Template

- `modular_registry_framework/core/registry.py` - capability registry
- `modular_registry_framework/core/context.py` - shared runtime context
- `modular_registry_framework/core/settings.py` - settings object with JSON, JSONL, XML, YAML, and YML load/save support
- `modular_registry_framework/modules/example/` - minimal feature module
- `modular_registry_framework/desktop/shell.py` - small Tkinter shell that builds navigation from registered screens
- `modular_registry_framework/scaffold.py` - CLI for creating a new module folder
- `docs/architecture.md` - full architecture note
- `docs/development-workflow.md` - practical workflow notes
- `tests/` - tests for registry, example module, and scaffolding

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

Then enable it in `modular_registry_framework/modules/__init__.py`:

```python
from .example import module as example
from .inventory import module as inventory

MODULES = (example, inventory)
```

## Settings Formats

Settings load and save based on the file extension:

- `.json` - normal JSON object
- `.jsonl` - one setting per line as `{"key": "app.name", "value": "Template App"}`
- `.xml` - `<settings>` root with `<setting key="...">...</setting>` entries
- `.yaml` / `.yml` - flat key/value mapping with JSON-compatible values

JSON remains the default format used by the example app.

## Development Rules

- Core coordinates; modules own features.
- Screens handle UI; services handle work.
- Modules register capabilities; the shell displays them.
- Events connect modules without tight coupling.
- Keep module loading explicit until dynamic loading solves a real problem.
- Add new registry contribution points only when multiple modules need them.
- Prefer simple Python code over clever plugin machinery.

## Verify

```powershell
python -m compileall modular_registry_framework tests
python -m pytest -q
```

## Success Criteria

The architecture is working when:

- adding a feature mostly means adding a module folder
- the app shell rarely changes
- business logic can be tested without opening the UI
- help, settings, screens, and field definitions live beside the feature they explain
- modules can react to important events without direct imports
- future projects can reuse the same skeleton

If the framework makes small apps harder, it is too heavy. Keep it practical.
