# Debugging And Logging

The framework includes switchable debugging and standard Python logging.

## Settings

```json
{
  "debug.enabled": true,
  "logging.level": "DEBUG",
  "logging.console_enabled": true,
  "logging.file_enabled": true,
  "logging.file": "logs/app.log"
}
```

JSON is the default settings file format, but settings can also be saved as JSONL, XML, YAML, or YML through the settings system.

## Diagnostics Module

The Diagnostics screen shows:

- debug mode state
- active logging level
- active logging handlers
- event handler counts

It can turn debug mode on and off while the app is running.

## What Debug Mode Does

When debug mode is enabled:

- logging level becomes `DEBUG`
- file logging is enabled
- registry event emissions are logged
- module registration is logged
- service, screen, setting, command, importer, report section, and event handler registration is logged
- imports, jobs, reports, artifacts, and settings saves are logged by their services
- diagnostics events are emitted when debug settings change

The logging configuration is applied at the Python root logger. That means module loggers inherit the core level unless a module deliberately overrides its own logger. For normal framework modules, this is top-down and app-wide.

## Exhaustive Trace Points

The core logs:

- settings load/save
- logging configuration
- context build start/end
- module entry point registration
- module metadata registration
- service registration
- screen registration
- setting registration
- command registration
- file importer registration
- report section registration
- event handler registration
- event emission

The built-in modules log:

- artifact folder creation
- artifact creation and registration
- job start/completion/failure
- file import start/completion
- report render/save and section rendering
- settings changes and saves
- diagnostics changes

## Recommended Use

Use debug mode when:

- building a new module
- tracing an importer
- testing a report section
- validating event hooks
- diagnosing API behavior
- understanding why a job failed

Leave debug mode off for normal operation unless the app is being actively diagnosed.
