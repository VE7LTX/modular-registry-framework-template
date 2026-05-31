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

