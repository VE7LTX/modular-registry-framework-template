# Service Patterns

Services are where the app does real work. Screens stay thin by calling services.

## Good Service Responsibilities

- validate inputs
- normalize data
- read and write files
- call APIs
- run imports
- create artifacts
- emit events
- return typed results

## Avoid In Services

- building Tkinter widgets
- showing message boxes
- directly controlling navigation
- depending on a specific screen

## Common Service Shapes

### Record Service

```python
class RecordService:
    def list_records(self): ...
    def get_record(self, record_id): ...
    def create_record(self, values): ...
    def update_record(self, record_id, values): ...
```

### Import Service

```python
class ImportService:
    def import_file(self, path):
        importer = registry.get_file_importer(path.suffix)
        result = importer.handler(path, context)
        registry.emit("file.imported", {...})
        return result
```

### Report Service

```python
class ReportService:
    def render_markdown(self):
        for section in registry.list_report_sections():
            section.renderer(context)
```

The pattern is the same: services own work, registry connects capabilities, events announce important outcomes.

