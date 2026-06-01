# App Template Types

This framework is meant to support the kinds of apps in this workspace.

## Desktop Workflow App

Fits: Moruca REW, ChronoBrief, Budget, bandplanx.

Use:

- screens
- services
- settings
- audit log
- artifact library
- jobs
- reports
- template generator starter: `desktop_workflow`

## Data Ingestion App

Fits: PPAS, Oanda SDK, XRP, Amazon, CBIG.

Use:

- importers
- API clients
- retries and jobs
- raw payload artifacts
- normalized records
- audit log
- generated reports
- template generator starter: `data_ingestion`

## Case Or Project Workspace

Fits: ChronoBrief, Moruca REW, legal/lab/reporting tools.

Use:

- artifact library
- records
- imports
- generated exports
- report sections
- help topics
- workspace-level settings
- template generator starter: `case_workspace`

## AI Agent Tool

Fits: Ziggy, Auto-Ziggy, Protocol Z, OPENCLAW, Discord.

Use:

- settings
- diagnostics
- jobs
- artifact library
- model/API client modules
- prompt packs
- audit log
- eval reports
- template generator starter: `ai_agent_tool`

## Benchmark And Evaluation App

Fits: Ollama benchmark and future model comparisons.

Use:

- jobs
- settings
- importers
- artifact library
- report sections
- diagnostics
- audit log
- template generator starter: `benchmark_evaluation`

## Integration Control Panel

Fits: Oanda, HubSpot, Kraken, REW API, Personal AI/OpenClaw integrations.

Use:

- API client modules
- command registry
- status dashboard
- diagnostics
- audit log
- jobs
- reports
- template generator starter: `integration_control_panel`

## CLI Tool

Fits: one-shot utilities, project cleanup tools, import/export helpers, and scripted workspace automation.

Use:

- command palette
- settings editor
- project repair
- workspace scanner
- secret scanner
- recipes
- template generator starter: `cli_tool`

## TUI Tool

Fits: terminal-first dashboards, SSH-friendly utilities, and repeatable operator workflows.

Use:

- TUI shell
- view models
- command palette
- health checks
- log viewer
- artifact browser
- workflows
- template generator starter: `tui_tool`

## Tkinter Tool

Fits: local desktop tools that need richer operator screens but should keep business logic reusable.

Use:

- dashboard
- UI adapters
- view models
- settings editor
- jobs
- reports
- artifact browser
- template generator starter: `tkinter_tool`
