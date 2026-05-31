# Module Roadmap

This is the next build queue for turning the template into a broad reusable app source.

## Highest Priority

The first baseline for these modules now exists in the template. The next work is to deepen them from generic skeletons into production-ready foundations.

## Recently Deepened

- `health_checks` now validates module dependencies and startup ordering.
- `flow_graph` now contributes graph quality checks.
- `jobs`, `importers`, `artifact_library`, `reports`, and `exporters` can carry `trace_id`.
- `audit_log` and `runtime_trace` persist to SQLite when storage is available.
- `template_generator` creates starter folders for six app families.

### api_clients

Shared pattern for external APIs.

Baseline shipped:

- client registration
- example local client
- status checks
- health check contribution
- graph trace ports

Next depth:

- auth status checks
- retry and backoff policy
- rate-limit tracking
- raw payload artifact capture
- redacted request/response logging
- events such as `api.requested`, `api.succeeded`, `api.failed`, `api.rate_limited`
- request/response artifact capture through `artifact_library`
- trace ID propagation through API calls

Useful for Oanda, Kraken, HubSpot, Amazon PAAPI, Personal AI, OpenClaw, REW API, and future integrations.

### records

Generic list/detail/edit workflow foundation.

Baseline shipped:

- generic in-memory record model
- create/list/archive service
- record events
- graph trace ports

Next depth:

- record model pattern
- list/filter/sort service helpers
- detail view pattern
- validation hooks
- events such as `record.created`, `record.updated`, `record.archived`

Useful for inventory, case records, DUT records, benchmark runs, customers, transcripts, and business graph entities.

### storage

SQLite and local persistence helpers.

Baseline shipped:

- SQLite connection lifecycle
- initialization
- backup
- health check
- storage report section
- persistent audit and trace tables

Next depth:

- database connection lifecycle
- repository base classes
- migrations folder pattern
- backup/export helpers
- schema report section
- events such as `storage.opened`, `storage.migrated`, `storage.backed_up`

Useful for ChronoBrief, Moruca REW, Budget, Oanda, PPAS, bandplanx, and CBIG.

### env_secrets

Environment and secret validation without leaking values.

Baseline shipped:

- `.env` loading
- required variable declarations
- redacted diagnostics
- health check
- `.env.example` content generation

Next depth:

- `.env` loading pattern
- required variable declarations
- redacted diagnostics
- missing-secret warnings
- `.env.example` generation

Useful for API-heavy tools and anything with model/API credentials.

## Next Layer

### validators

Reusable field/data validation.

Should provide:

- required field checks
- type checks
- choices
- range checks
- validation result objects
- UI-friendly error messages

### exporters

Registry for output formats.

Baseline shipped:

- exporter registry contribution point
- JSON, JSONL, text, Markdown, CSV, XML, YAML, and YML serializers
- export events
- artifact saves through `export_artifact`

Next depth:

- Markdown
- HTML
- CSV
- JSON
- JSONL
- XML
- YAML
- plain text

### graph_export

Persist graph outputs.

Baseline shipped:

- Mermaid artifact output
- JSON graph output
- graph export report section

Next depth:

- Mermaid artifact output
- JSON graph output
- Graphviz/DOT output
- timestamped graph snapshots
- graph report links

### runtime_trace

Trace IDs across jobs, imports, artifacts, reports, logs, and events.

Baseline shipped:

- generated trace IDs
- wildcard event capture when payload has `trace_id`
- trace report section

Next depth:

- generated trace IDs
- parent/child trace relationships
- trace-aware audit log entries
- trace report section

### health_checks

Readiness and configuration warnings.

Baseline shipped:

- health check registry contribution point
- pass/warn/fail result model
- readiness screen
- health event

Next depth:

- module readiness checks
- file path checks
- API connectivity checks
- missing-secret checks
- dependency checks
- dashboard status summaries

## Template Families

Starter folder generation now exists for:

- `desktop_workflow`
- `data_ingestion`
- `case_workspace`
- `ai_agent_tool`
- `benchmark_evaluation`
- `integration_control_panel`

Each starter should declare:

- included modules
- expected folders
- default settings
- example flow graph
- run/test commands
- app-specific README section

Next depth:

- generate importable Python packages, not only starter folders
- generate tests per template family
- generate `.env.example`
- generate app-specific enabled module lists
- optionally copy runnable shell entry points
