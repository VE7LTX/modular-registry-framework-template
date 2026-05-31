from __future__ import annotations

import os
from pathlib import Path

from modular_registry_framework.core.context import AppContext
from modular_registry_framework.modules.health_checks.models import HealthResult

from .models import SecretRequirement


class EnvSecretsService:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self._requirements: dict[str, SecretRequirement] = {}

    def require(self, key: str, label: str, required: bool = True) -> None:
        self._requirements[key] = SecretRequirement(key, label, required)
        self.context.registry.emit("secret.required", {"key": key, "required": required})

    def load_env_file(self, path: Path | None = None) -> dict[str, str]:
        env_path = path or self.context.base_dir / ".env"
        values: dict[str, str] = {}
        if not env_path.exists():
            return values
        for line in env_path.read_text(encoding="utf-8").splitlines():
            clean_line = line.strip()
            if not clean_line or clean_line.startswith("#") or "=" not in clean_line:
                continue
            key, value = clean_line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
            os.environ.setdefault(key.strip(), values[key.strip()])
        return values

    def validate(self) -> list[dict]:
        self.load_env_file()
        rows = []
        for requirement in sorted(self._requirements.values(), key=lambda item: item.key):
            raw_value = os.environ.get(requirement.key, "")
            present = bool(raw_value)
            rows.append(
                {
                    "key": requirement.key,
                    "label": requirement.label,
                    "required": requirement.required,
                    "present": present,
                    "redacted": redact(raw_value),
                }
            )
        return rows

    def health_check(self, context: AppContext) -> HealthResult:
        missing = [row["key"] for row in self.validate() if row["required"] and not row["present"]]
        status = "pass" if not missing else "fail"
        message = "All required secrets are present." if not missing else f"Missing secrets: {', '.join(missing)}"
        return HealthResult("env_secrets.required", status, message, "env_secrets")

    def generate_example(self) -> str:
        lines = []
        for requirement in sorted(self._requirements.values(), key=lambda item: item.key):
            marker = "required" if requirement.required else "optional"
            lines.append(f"# {requirement.label} ({marker})")
            lines.append(f"{requirement.key}=")
        return "\n".join(lines) + ("\n" if lines else "")


def redact(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 4:
        return "****"
    return f"{value[:2]}****{value[-2:]}"

