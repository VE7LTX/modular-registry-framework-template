from __future__ import annotations

from pathlib import Path


DEFAULT_GITIGNORE = """__pycache__/
*.py[cod]
.venv/
venv/
env/
.env
.env.*
!.env.example
.pytest_cache/
artifacts/
data/
logs/
*.db
*.sqlite3
"""


class ProjectRepairService:
    def plan(self, path: Path) -> list[str]:
        actions: list[str] = []
        if not (path / ".gitignore").exists():
            actions.append("create .gitignore")
        if not (path / "README.md").exists():
            actions.append("create README.md")
        if not (path / ".env.example").exists():
            actions.append("create .env.example")
        if not (path / "tests").exists():
            actions.append("create tests/")
        if not (path / "docs").exists():
            actions.append("create docs/")
        return actions

    def apply_baseline(self, path: Path) -> list[Path]:
        path.mkdir(parents=True, exist_ok=True)
        written: list[Path] = []
        files = {
            ".gitignore": DEFAULT_GITIGNORE,
            "README.md": f"# {path.name}\n\n## Purpose\n\nDescribe this project.\n",
            ".env.example": "# Add required environment variables here.\n",
            "docs/README.md": "# Docs\n",
            "tests/README.md": "# Tests\n",
        }
        for relative, content in files.items():
            target = path / relative
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                written.append(target)
        return written

