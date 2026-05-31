from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {".git", ".venv", "venv", "env", "__pycache__", "node_modules", ".pytest_cache"}


@dataclass(frozen=True, slots=True)
class ProjectScan:
    path: Path
    name: str
    has_git: bool
    has_readme: bool
    python_files: int
    markdown_files: int
    sqlite_files: int
    env_files: int
    test_files: int
    log_files: int

    @property
    def status_hint(self) -> str:
        if self.has_git and self.has_readme and self.test_files:
            return "active-candidate"
        if self.python_files or self.markdown_files:
            return "project-candidate"
        return "unknown"


class WorkspaceScannerService:
    def scan_workspace(self, root: Path, max_depth: int = 2) -> list[ProjectScan]:
        root = root.resolve()
        scans: list[ProjectScan] = []
        for child in sorted(path for path in root.iterdir() if path.is_dir() and path.name not in SKIP_DIRS):
            scans.append(self.scan_project(child, max_depth=max_depth))
        return scans

    def scan_project(self, path: Path, max_depth: int = 3) -> ProjectScan:
        files = list(_iter_files(path, max_depth=max_depth))
        return ProjectScan(
            path=path,
            name=path.name,
            has_git=(path / ".git").exists(),
            has_readme=any(file.name.lower() == "readme.md" for file in files),
            python_files=sum(1 for file in files if file.suffix == ".py"),
            markdown_files=sum(1 for file in files if file.suffix.lower() == ".md"),
            sqlite_files=sum(1 for file in files if file.suffix.lower() in {".db", ".sqlite", ".sqlite3"}),
            env_files=sum(1 for file in files if file.name == ".env" or file.name.startswith(".env.")),
            test_files=sum(1 for file in files if file.name.startswith("test_") or file.parent.name == "tests"),
            log_files=sum(1 for file in files if file.suffix.lower() == ".log"),
        )

    def render_markdown(self, scans: list[ProjectScan]) -> str:
        lines = ["# Workspace Scan", "", "| Project | Status | Git | README | Py | MD | DB | Env | Tests | Logs |", "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
        for scan in scans:
            lines.append(
                f"| {scan.name} | {scan.status_hint} | {scan.has_git} | {scan.has_readme} | "
                f"{scan.python_files} | {scan.markdown_files} | {scan.sqlite_files} | "
                f"{scan.env_files} | {scan.test_files} | {scan.log_files} |"
            )
        return "\n".join(lines) + "\n"


def _iter_files(root: Path, max_depth: int):
    root = root.resolve()
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if len(path.relative_to(root).parts) > max_depth + 1:
            continue
        if path.is_file():
            yield path

