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

