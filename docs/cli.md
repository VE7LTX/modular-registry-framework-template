# CLI

The `mrf` command exposes the framework without opening the desktop shell.

## Commands

```powershell
mrf health
mrf graph mermaid
mrf graph adjacency
mrf graph export
mrf template data_ingestion .\MyIngestionApp
mrf scan "C:\VS Code Workspaces"
mrf secrets .\MyProject
mrf module-test inventory --tests-dir .\tests
mrf runbook
mrf runbook --save
mrf packs
mrf tui
mrf commands health
mrf settings show
mrf settings set debug.enabled true
mrf logs --level ERROR
mrf artifacts list
mrf repair plan .\SomeProject
mrf repair apply .\SomeProject
```

## Purpose

Use the CLI for automation, repository cleanup, CI-style checks, and one-off project work.

- `health`: run readiness checks.
- `graph`: inspect or persist the architecture graph.
- `template`: create starter folders for app families.
- `scan`: inventory a workspace folder.
- `secrets`: scan for likely hardcoded secrets.
- `module-test`: generate a baseline pytest file for a module.
- `runbook`: render or save operational documentation.
- `packs`: list module packs for template families.
- `tui`: render the terminal dashboard once.
- `commands`: search registered commands.
- `settings`: show, edit, or save settings.
- `logs`: tail the configured app log.
- `artifacts`: list or preview generated artifacts.
- `repair`: plan or apply project baseline repairs.
