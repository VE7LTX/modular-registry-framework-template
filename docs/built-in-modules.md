# Built-In Modules

The template now ships with a universal module set. These modules are intentionally generic so they can support desktop workflow apps, ingestion tools, AI agent tools, benchmark systems, report generators, and integration control panels.

## System Modules

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
- health checks: `modules.registered`, `trace.ports`
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
