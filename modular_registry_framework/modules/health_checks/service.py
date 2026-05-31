from __future__ import annotations

import logging

from modular_registry_framework.core.context import AppContext

from .models import HealthResult


class HealthCheckService:
    def __init__(self, context: AppContext) -> None:
        self.context = context

    def run_all(self) -> list[HealthResult]:
        results: list[HealthResult] = []
        for name, check in self.context.registry.list_health_checks().items():
            logging.getLogger(__name__).debug("Running health check: %s", name)
            try:
                result = check.handler(self.context)
            except Exception as exc:
                result = HealthResult(name, "fail", str(exc), check.module)
            if isinstance(result, HealthResult):
                results.append(result)
            elif isinstance(result, dict):
                results.append(
                    HealthResult(
                        name=result.get("name", name),
                        status=result.get("status", "unknown"),
                        message=result.get("message", ""),
                        module=result.get("module", check.module),
                    )
                )
            else:
                results.append(HealthResult(name, "pass", str(result), check.module))
        self.context.registry.emit("health.checked", {"count": len(results), "failed": self.failed_count(results)})
        return results

    def summary(self) -> dict[str, int]:
        results = self.run_all()
        return {
            "pass": sum(1 for result in results if result.status == "pass"),
            "warn": sum(1 for result in results if result.status == "warn"),
            "fail": sum(1 for result in results if result.status == "fail"),
        }

    @staticmethod
    def failed_count(results: list[HealthResult]) -> int:
        return sum(1 for result in results if result.status == "fail")


def modules_registered_check(context: AppContext) -> HealthResult:
    count = len(context.registry.list_modules())
    status = "pass" if count else "fail"
    return HealthResult("modules.registered", status, f"{count} modules registered.", "health_checks")


def trace_ports_check(context: AppContext) -> HealthResult:
    ports = context.registry.list_data_ports()
    status = "pass" if ports else "warn"
    return HealthResult("trace.ports", status, f"{len(ports)} trace ports declared.", "health_checks")

