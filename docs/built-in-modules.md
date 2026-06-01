# Built-In Modules

The template now ships with a universal module set. These modules are intentionally generic so they can support desktop workflow apps, ingestion tools, AI agent tools, benchmark systems, report generators, and integration control panels.

## System Modules

### view_models

Provides shared display tables for CLI, TUI, and Tkinter.

Registers:

- service: `view_models`
- commands: `view.modules`, `view.health`
- screen: `System / View Models`
- inputs: registry data
- outputs: table views

### command_palette

Searches and runs registered commands.

Registers:

- service: `command_palette`
- commands: `commands.search`, `commands.run`
- screen: `System / Command Palette`
- inputs: registered commands
- outputs: command execution events

### ui_adapters

Maps registered modules to the surfaces where users can reach them: CLI commands, Tkinter screens, report sections, dashboard visibility, and TUI-friendly view models.

Registers:

- service: `ui_adapters`
- command: `ui_adapters.render`
- screen: `System / UI Adapters`
- inputs: registry surfaces
- outputs: surface map

### tui_shell

Renders a dependency-free terminal dashboard.

Registers:

- service: `tui_shell`
- command: `tui.render`
- screen: `System / TUI Preview`
- inputs: view models
- outputs: terminal dashboard

### dashboard

Shows the live map of registered modules and capabilities.

Registers:

- service: `dashboard`
- command: `dashboard.render_text`
- screen: `System / Dashboard`
- inputs: registry snapshot
- outputs: dashboard text

### help

Collects module-owned help topics into a browsable help screen.

Registers:

- service: `help`
- command: `help.render_topic_index`
- screen: `System / Help`
- inputs: help topics
- outputs: topic index

### settings_manager

Shows registered settings and saves selected values.

Registers:

- service: `settings_manager`
- command: `settings.save`
- screen: `System / Settings`
- inputs: registered settings
- outputs: settings files

### settings_editor

Provides shared settings edit/save helpers.

Registers:

- service: `settings_editor`
- commands: `settings.edit`, `settings.editor_save`
- screen: `System / Settings Editor`
- inputs: setting text
- outputs: settings values

### diagnostics

Provides top-down debug mode, logging configuration, and runtime inspection.

Registers:

- service: `diagnostics`
- settings: `debug.enabled`, `logging.level`, `logging.console_enabled`, `logging.file_enabled`, `logging.file`
- screen: `System / Diagnostics`
- inputs: debug settings
- outputs: log files

### audit_log

Records recent registry events through a wildcard event handler.

Registers:

- service: `audit_log`
- wildcard handler: `*`
- screen: `System / Audit Log`
- inputs: registry events
- outputs: audit events

### flow_graph

Builds an automatic graph of modules, capabilities, events, inputs, outputs, and flows.

Registers:

- service: `flow_graph`
- commands: `flow_graph.render_mermaid`, `flow_graph.render_adjacency`
- report section: `system.flow_graph`
- screen: `System / Flow Graph`
- inputs: registry capabilities
- outputs: Mermaid graph

### graph_export

Persists flow graph snapshots as Mermaid and JSON artifacts.

Registers:

- service: `graph_export`
- commands: `graph_export.save_mermaid`, `graph_export.save_json`
- report section: `system.graph_export`
- screen: `System / Graph Export`
- inputs: flow graph
- outputs: graph artifacts

### health_checks

Runs readiness checks contributed by modules.

Registers:

- service: `health_checks`
- health checks: `modules.registered`, `modules.dependencies`, `trace.ports`
- screen: `System / Health`
- inputs: registered checks
- outputs: health results

### env_secrets

Loads `.env`, validates required variables, and redacts secret diagnostics.

Registers:

- service: `env_secrets`
- command: `env_secrets.generate_example`
- health check: `env_secrets.required`
- screen: `System / Secrets`
- inputs: `.env file`
- outputs: redacted secret status

### runtime_trace

Collects events that carry `trace_id`.

Registers:

- service: `runtime_trace`
- command: `runtime_trace.new_trace_id`
- report section: `runtime_trace.events`
- wildcard handler: `*`
- screen: `System / Runtime Trace`
- inputs: trace events
- outputs: trace report

Persistence:

- stores trace events in SQLite when `storage` is available

### trace_graph

Turns actual runtime trace events into a run-history graph.

Registers:

- service: `trace_graph`
- commands: `trace_graph.render`, `trace_graph.mermaid`
- report section: `trace_graph.runtime`
- screen: `System / Trace Graph`
- inputs: trace events
- outputs: run graph

### storage

Provides SQLite lifecycle, initialization, health check, and backup baseline.

Registers:

- service: `storage`
- commands: `storage.initialize`, `storage.backup`
- health check: `storage.sqlite`
- report section: `storage.sqlite`
- screen: `System / Storage`
- inputs: database path
- outputs: SQLite database

Persistence:

- `audit_log` stores audit events in `audit_events`
- `runtime_trace` stores trace events in `trace_events`

### log_viewer

Tails and filters the configured app log.

Registers:

- service: `log_viewer`
- command: `logs.tail`
- screen: `System / Logs`
- inputs: log file
- outputs: log lines

### artifact_browser

Lists and previews generated artifacts.

Registers:

- service: `artifact_browser`
- commands: `artifacts.list`, `artifacts.preview`
- screen: `System / Artifact Browser`
- inputs: artifact files
- outputs: artifact previews

## Work Modules

### artifact_library

Creates and tracks generated files in predictable artifact folders.

Registers:

- service: `artifact_library`
- screen: `System / Artifacts`
- inputs: artifact content
- outputs: artifact records
- events: `artifact.created`, `artifact.registered`

### jobs

Provides a shared lifecycle for important or long-running work.

Registers:

- service: `jobs`
- screen: `System / Jobs`
- inputs: callable work
- outputs: job records
- events: `job.started`, `job.completed`, `job.failed`

### importers

Provides a shared file-import surface.

Registers:

- service: `importers`
- screen: `Tools / Importers`
- importers: `.csv`, `.json`, `.jsonl`, `.md`, `.txt`, `.xml`, `.yaml`, `.yml`
- inputs: files
- outputs: import results
- events: `file.imported`

### exporters

Provides reusable output serializers.

Registers:

- service: `exporters`
- screen: `Tools / Exporters`
- exporters: `json`, `jsonl`, `txt`, `md`, `csv`, `xml`, `yaml`, `yml`
- inputs: structured data
- outputs: export text
- events: `data.exported`

Commands:

- `exporters.export`
- `exporters.export_artifact`

### records

Provides a generic in-memory record pattern.

Registers:

- service: `records`
- screen: `Tools / Records`
- inputs: record values
- outputs: record events
- events: `record.created`, `record.archived`

### api_clients

Registers external API clients and exposes availability checks.

Registers:

- service: `api_clients`
- API client: `example`
- health check: `api_clients.available`
- screen: `Integrations / API Clients`
- inputs: requests
- outputs: responses

### template_generator

Creates starter app folders for common application families.

Registers:

- service: `template_generator`
- command: `template_generator.create_app`
- screen: `Tools / Template Generator`
- inputs: template selection
- outputs: app starter folder

Starter families:

- `desktop_workflow`
- `data_ingestion`
- `case_workspace`
- `ai_agent_tool`
- `benchmark_evaluation`
- `integration_control_panel`
- `cli_tool`
- `tui_tool`
- `tkinter_tool`

### module_packs

Describes reusable sets of modules for each app family.

Registers:

- service: `module_packs`
- command: `module_packs.render`
- screen: `Tools / Module Packs`
- inputs: template families
- outputs: module packs

### app_profiles

Defines opinionated app modes for the kinds of tools this workspace tends to build.

Registers:

- service: `app_profiles`
- command: `app_profiles.render`
- screen: `Tools / App Profiles`
- inputs: app mode
- outputs: module bundle

Profiles:

- `cli_tool`
- `tui_tool`
- `tkinter_tool`
- `agent_lab`
- `data_api_tool`

### workflows

Defines repeatable module pipelines.

Registers:

- service: `workflows`
- commands: `workflows.render`, `workflows.mermaid`, `workflows.demo`
- screen: `Tools / Workflows`
- inputs: workflow definition
- outputs: workflow run

Built-in workflows:

- `import_report_export`
- `api_sync_review`
- `agent_eval`

### recipes

Provides tiny runnable examples that prove modules work together.

Registers:

- service: `recipes`
- commands: `recipes.render`, `recipes.run`
- screen: `Examples / Recipes`
- inputs: recipe name
- outputs: recipe artifact

Built-in recipes:

- `csv_report`
- `api_sync`
- `agent_eval`

### module_test_harness

Generates baseline pytest files for module registration and traceability.

Registers:

- service: `module_test_harness`
- commands: `module_test.render`, `module_test.write`
- screen: `Tools / Module Test Harness`
- inputs: module name
- outputs: pytest file

### runbook_generator

Generates operational runbooks from registered modules, settings, health checks, and data locations.

Registers:

- service: `runbook_generator`
- commands: `runbook.render`, `runbook.save`
- screen: `Tools / Runbook`
- inputs: registry metadata
- outputs: runbook artifact

### workspace_scanner

Scans local workspace folders and summarizes project signals.

Registers:

- service: `workspace_scanner`
- command: `workspace.scan`
- screen: `Tools / Workspace Scanner`
- inputs: workspace folder
- outputs: project inventory

### secret_scanner

Scans project text files for likely hardcoded secrets and redacts values.

Registers:

- service: `secret_scanner`
- command: `secrets.scan`
- screen: `Tools / Secret Scanner`
- inputs: source files
- outputs: redacted findings

### project_repair

Plans and creates missing baseline project files.

Registers:

- service: `project_repair`
- commands: `project_repair.plan`, `project_repair.apply`
- screen: `Tools / Project Repair`
- inputs: project folder
- outputs: baseline files

### reports

Renders Markdown reports from registered report sections.

Registers:

- service: `reports`
- commands: `reports.render_markdown`, `reports.save_markdown`
- report sections: `modules.inventory`, `modules.capabilities`
- screen: `Tools / Reports`
- inputs: report sections
- outputs: Markdown report
- events: `report.generated`

### example

Demonstrates the standard module shape.

Registers:

- service: `example`
- screen: `Examples / Example Module`
- setting: `example.default_status`
- inputs: item name
- outputs: example items
- events: `example.item_created`
