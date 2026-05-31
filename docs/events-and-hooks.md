# Events And Hooks

Events let modules cooperate without direct imports.

## Event Names

Use dotted names:

```text
app.started
app.shutdown
file.imported
artifact.created
job.started
job.completed
job.failed
report.generated
setting.changed
diagnostics.debug_changed
```

Use past-tense names for completed facts. Use events for meaningful cross-module actions, not every button click.

## Payloads

Payloads should be small dictionaries with simple values:

```python
registry.emit("file.imported", {
    "path": str(path),
    "extension": ".csv",
    "label": "CSV",
})
```

Prefer strings, numbers, booleans, and IDs. Avoid sending UI widgets or open file handles.

## Handlers

Register handlers with:

```python
registry.on("file.imported", refresh_index)
```

The audit log uses the wildcard event:

```python
registry.on("*", audit_log.handle_registry_event)
```

Wildcard handlers receive:

```python
{
    "event_name": "file.imported",
    "payload": {...}
}
```

