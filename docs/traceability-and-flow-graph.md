# Traceability And Flow Graph

The framework now has a built-in graph layer for understanding how modules connect.

## Why This Exists

As the template grows, the biggest risk is losing track of:

- what each module consumes
- what each module produces
- which module emits which events
- which service creates artifacts
- which importers feed reports or records
- where settings, logs, jobs, and outputs come from

The flow graph makes that visible.

## Automatic Graph Sources

The Flow Graph module reads the registry and automatically maps:

- module metadata
- module dependencies
- services
- screens
- settings
- importers
- report sections
- commands
- event handlers
- declared input ports
- declared output ports
- explicit flow edges

It can render:

- Mermaid flowchart text
- adjacency-list text
- a report section inside generated Markdown reports

## Declaring Inputs And Outputs

Use ports to describe module boundaries.

```python
registry.add_data_input(
    "importers",
    "files",
    "file",
    "CSV, JSON, XML, YAML, Markdown, and text files.",
)

registry.add_data_output(
    "importers",
    "import results",
    "records",
    "Parsed file data returned as Python objects.",
)
```

Good port kinds include:

- `file`
- `records`
- `metadata`
- `settings`
- `event`
- `artifact`
- `task`
- `view`
- `diagram`
- `user_input`

## Declaring Flow Edges

Use explicit flows when a module transforms one thing into another.

```python
registry.add_flow(
    "port:importers:input:files",
    "port:importers:output:import results",
    "parse files",
    "data",
)

registry.add_flow(
    "port:importers:output:import results",
    "event:file.imported",
    "emit import event",
    "event",
)
```

The endpoint strings are intentionally simple. Stable prefixes are:

- `module:name`
- `service:name`
- `screen:area:title`
- `setting:key`
- `importer:.ext`
- `report_section:name`
- `event:name`
- `port:module:input:name`
- `port:module:output:name`

## What To Add Next

The current graph is registry-based and now feeds health checks. Good next upgrades are:

- trace IDs on API client calls and record changes
- Graphviz export
- dependency validation before app startup
- dead-port detection for outputs nobody consumes
- graph filters by module, event, or artifact
- clickable graph nodes in the desktop UI
