# Module Lifecycle

The framework starts with a small host and a list of modules.

## Startup Flow

```text
1. Load settings from settings.json
2. Configure logging from settings
3. Create the Registry
4. Create AppContext
5. Register each module in MODULES order
6. Modules add metadata, services, screens, settings, help, importers, report sections, commands, and event handlers
7. DesktopShell reads registered screens and builds tabs
8. Core emits app.started
9. Screens and services emit domain events as work happens
10. Core emits app.shutdown
```

## Why Registration Order Matters

Some modules are foundational:

- `audit_log` registers the wildcard event handler early
- `diagnostics` registers debug and logging settings
- `artifact_library` gives reports and exports a place to write files
- `jobs` gives imports, scans, reports, and syncs a common lifecycle
- `importers` registers file handlers
- `reports` registers report sections and report commands
- `help` collects module help topics
- `dashboard` displays the assembled system

Feature modules should come after those built-ins so they can use the shared services.

## What A Module Can Contribute

A module can register:

- metadata with `registry.add_module(...)`
- business services with `registry.add_service(...)`
- screens with `registry.add_screen(...)`
- settings with `registry.add_setting(...)`
- help topics with `registry.add_help_topic(...)`
- commands with `registry.add_command(...)`
- file importers with `registry.add_file_importer(...)`
- report sections with `registry.add_report_section(...)`
- event handlers with `registry.on(...)`

The core does not call feature code directly. It asks the registry what exists.

