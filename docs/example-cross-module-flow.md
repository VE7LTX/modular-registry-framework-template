# Example Cross-Module Flow

This is the intended feel of the framework: modules run independently but cooperate through the registry and events.

## Import And Report Flow

```text
1. User imports a CSV file
2. importers looks up the .csv handler
3. importers parses the file
4. importers emits file.imported
5. audit_log records the event
6. jobs can wrap the import if it is long-running
7. artifact_library can register raw or generated files
8. reports renders a Markdown report from registered sections
9. artifact_library saves the report under artifacts/reports/
10. reports emits report.generated
11. dashboard shows the registered modules and capabilities
```

No module needs to import every other module. Shared work moves through services, registry contribution points, and events.

## Why This Matters

In a one-file app, import logic, UI refresh, report generation, and logging usually become tangled. Here:

- importers parse files
- audit_log records events
- artifact_library tracks outputs
- reports renders reports
- dashboard explains what exists
- diagnostics helps debug what happened

That is the Drupal-style module idea reduced to a practical local Python app pattern.

