# Reusable Modular App Framework Idea

This document describes a reusable architecture for building modular local applications. It is inspired by Drupal's module, hook, and service ideas, but it is not a copy or port of Drupal code.

The purpose is to create a clean Python base style for future apps where features can be added, removed, tested, and maintained without turning the project into one giant file.

## Plain-English Purpose

This architecture is for apps that start small but are expected to grow.

It gives every feature a predictable place to live:

- screens go in the feature module
- business logic goes in services
- settings are registered instead of hard-coded
- help text lives beside the feature it explains
- events/hooks let modules react to important actions
- the app shell builds navigation from registered modules

The goal is not to make a huge framework. The goal is to make repeatable app structure that stays understandable as the app grows.

## What Problem It Solves

Most internal tools begin as one script or one large app file. That works at first, but eventually causes problems:

- UI code, database code, file handling, reports, settings, and API calls all mix together
- changing one feature can break unrelated features
- fields and labels get duplicated in multiple places
- business logic is hard to test without opening the UI
- future projects copy messy patterns
- adding new screens requires editing the core app directly

This framework idea solves that by separating the app into a small core and feature modules.

## Architecture Name

Generic name:

```text
Modular Registry Framework
```

More descriptive name:

```text
Registry-Based Modular App Framework
```

Short description:

```text
A lightweight Python app architecture where modules register screens, services, settings, help text, file handlers, report sections, and event hooks with a small shared core.
```

## What It Is Similar To

This idea already exists in mature systems, but this version is smaller and focused on local Python apps.

Similar concepts:

- Drupal modules and hooks
- VS Code extension contribution points
- Eclipse RCP plugin architecture
- pytest/pluggy hook system
- Python package entry points
- service-oriented modular monoliths

This framework should borrow the ideas, not the source code.

## What It Is Not

This is not:

- a Drupal port
- a CMS
- a web framework by default
- a dynamic plugin marketplace
- a microservice system
- a reason to over-engineer tiny scripts

Start simple. Add dynamic loading or packaging only when there is a real need.

## Core Concept

The app is a host. Features are modules.

```text
Application Core
  |
  |-- starts the app
  |-- loads settings
  |-- opens the database
  |-- creates the registry
  |-- registers modules
  |-- builds the UI shell
  |-- emits events
  |
  +-- Feature Module A
  +-- Feature Module B
  +-- Feature Module C
```

The core does not know every detail of every feature. Modules register what they provide.

## Required Pieces

A minimum implementation needs these pieces.

The current template has grown past the minimum implementation. It now includes built-in modules for dashboarding, help, settings, diagnostics, audit logging, artifacts, jobs, importers, reports, and automatic flow graph tracing. See `docs/built-in-modules.md` for the current inventory.

### 1. App Core

The app core starts and coordinates the application.

Responsibilities:

- create the database connection
- load settings
- create the registry
- load/register modules
- create shared app context
- build the main app shell
- emit startup/shutdown events

The core should stay small.

### 2. Registry

The registry is where modules announce what they provide.

Minimum registry methods:

```python
registry.add_service(name, service)
registry.get_service(name)
registry.add_screen(area, title, factory, order=100)
registry.add_help_topic(key, content)
registry.on(event_name, handler)
registry.emit(event_name, payload)
```

Later registry methods:

```python
registry.add_setting(key, default, label, help_text)
registry.add_file_importer(extension, importer)
registry.add_report_section(name, renderer)
registry.add_comparison_metric(name, calculator)
registry.add_command(name, handler)
registry.add_data_input(module, name, kind, description)
registry.add_data_output(module, name, kind, description)
registry.add_flow(source, target, label, kind)
```

The registry is a directory of capabilities. It should not contain business logic.

### 3. App Context

The app context carries shared runtime objects.

Example:

```python
@dataclass
class AppContext:
    db: Database
    settings: Settings
    registry: Registry
    base_dir: Path
```

Pass context into modules, services, and screens instead of importing globals everywhere.

### 4. Modules

A module owns one feature area.

A module may provide:

- screens
- services
- settings
- help text
- field definitions
- file importers
- report sections
- event handlers

Each module exposes a `register` function.

```python
def register(registry, context):
    service = ExampleService(context.db)
    registry.add_service("example", service)
    registry.add_screen("Advanced", "Example", build_example_screen, order=50)
    registry.add_help_topic("example.overview", EXAMPLE_HELP)
```

### 5. Services

Services do real work. Screens call services.

Services should:

- validate inputs
- read/write data
- perform calculations
- import/export files
- generate reports
- emit meaningful events

Services should not:

- create UI widgets
- show message boxes
- depend on Tkinter
- directly manage navigation

Example:

```python
class RecordService:
    def list_active(self): ...
    def get(self, record_id): ...
    def create(self, values): ...
    def update(self, record_id, values): ...
    def archive(self, record_id): ...
```

### 6. Screens

Screens are UI modules.

Screens should:

- build widgets
- bind buttons and selection events
- call services
- show user-facing messages
- refresh displayed data

Screens should avoid direct SQL and heavy business logic.

Example:

```python
def build_record_screen(parent, context):
    service = context.registry.get_service("records")
    return RecordScreen(parent, service, context).frame
```

### 7. Events / Hooks

Events let modules respond to actions without hard-coding dependencies.

Example events:

```text
app.started
app.shutdown
record.created
record.updated
record.archived
file.imported
report.generated
api.connected
api.unavailable
```

Example handler:

```python
def register(registry, context):
    registry.on("file.imported", refresh_file_status)
```

Use events for important cross-module actions, not every small UI action.

## Standard Folder Layout

Recommended layout for a local desktop app:

```text
project_name/
  app/
    __init__.py
    main.py
    db.py
    core/
      __init__.py
      context.py
      events.py
      registry.py
      settings.py
    modules/
      __init__.py
      records/
        __init__.py
        module.py
        service.py
        screens.py
        fields.py
        help.py
        models.py
      reports/
        __init__.py
        module.py
        service.py
        screens.py
    desktop/
      __init__.py
      shell.py
      dialogs.py
      widgets.py
  docs/
    architecture.md
    development-workflow.md
  tests/
    test_records.py
  README.md
```

For a web app, add or replace the desktop folder:

```text
  app/
    web/
      routes.py
      templates/
      static/
```

## Module File Purposes

Inside each module:

```text
module.py      registration entry point
service.py     business logic and database operations
screens.py     UI screens or view builders
fields.py      field definitions and validation metadata
help.py        inline help, tooltips, and explainer text
models.py      dataclasses or typed objects
migrations.py  optional future database migrations
```

## Minimum First Version

Do not build everything at once.

A useful first version only needs:

```text
core/registry.py
core/context.py
modules/example/module.py
modules/example/service.py
modules/example/screens.py
desktop/shell.py
```

Minimum behavior:

1. create registry
2. create context
3. call each module's `register()` function
4. build top-level navigation from registered screens
5. let screens call registered services

## Example Startup Flow

```text
1. Start app
2. Load settings
3. Open database
4. Create Registry
5. Create AppContext
6. Import module list
7. Each module registers services/screens/hooks
8. Shell builds navigation from registry screens
9. Emit app.started
10. Enter UI loop
```

Example code shape:

```python
def main():
    db = Database("data/app.sqlite3")
    settings = Settings.load()
    registry = Registry()
    context = AppContext(db=db, settings=settings, registry=registry, base_dir=Path.cwd())

    for module in MODULES:
        module.register(registry, context)

    app = DesktopShell(context)
    registry.emit("app.started", {"context": context})
    app.run()
```

## Example Module

```python
# app/modules/records/module.py

from .service import RecordService
from .screens import build_record_screen
from .help import HELP_TOPICS


def register(registry, context):
    registry.add_service("records", RecordService(context.db))
    registry.add_screen("Records", "Record Library", build_record_screen, order=10)

    for key, content in HELP_TOPICS.items():
        registry.add_help_topic(key, content)
```

## What To Build First

Build in this order:

1. `Registry`
2. `AppContext`
3. one example module
4. app shell that reads screens from the registry
5. one real service
6. one real screen
7. event hooks
8. settings registry
9. file importers/report extensions only when needed

This keeps the framework usable early.

## When To Use This Pattern

Use it for:

- local engineering tools
- lab workflow apps
- inventory apps
- QC/QA tools
- report generators
- API control panels
- small desktop apps expected to grow
- business workflow tools with many screens

Avoid it for:

- one-off scripts
- tiny converters
- simple command-line tools
- prototypes that will be thrown away

## Design Rules

- Core coordinates; modules own features.
- Screens handle UI; services handle work.
- Modules register capabilities; the shell displays them.
- Events connect modules without tight coupling.
- Keep module loading explicit at first.
- Keep database changes deliberate and documented.
- Prefer boring code over clever plugin magic.
- Every module should be understandable by opening its folder.

## License And Code Reuse Note

Do not copy Drupal source code directly. Drupal is GPL-licensed, and a direct port or derivative copy could carry GPL obligations.

It is fine to use the architectural idea:

- modules
- hooks
- service registration
- settings registration
- contribution points

Implement the Python version from scratch.

## Future Expansion Ideas

Once the base pattern is working, future additions could include:

- module metadata files
- enabled/disabled modules
- module dependency declarations
- database migrations per module
- command registry
- permission/role registry
- dynamic plugin discovery through Python entry points
- `pluggy` integration for a more formal hook system
- module templates/scaffolding command
- API client module with auth/retry/redaction support
- records module for list/detail/edit workflows
- SQLite storage and migration helpers
- runtime trace IDs across jobs/imports/artifacts/reports/events
- graph exports to Mermaid, JSON, and Graphviz

Add these only when real projects need them.

See `docs/module-roadmap.md` for the current build queue.

## Success Criteria

The architecture is working if:

- adding a feature mostly means adding a module folder
- the app shell rarely changes
- business logic can be tested without the UI
- help/settings/screens live beside the feature they explain
- modules can react to important events without direct imports
- future projects can reuse the same skeleton

If the framework makes small apps harder, it is too heavy. Keep it practical.
