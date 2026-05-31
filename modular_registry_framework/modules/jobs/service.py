from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Callable

from modular_registry_framework.core.context import AppContext

from .models import JobRecord


class JobService:
    def __init__(self, context: AppContext) -> None:
        self.context = context
        self._next_id = 1
        self._jobs: list[JobRecord] = []

    def run_sync(self, name: str, handler: Callable[[], Any], trace_id: str | None = None) -> JobRecord:
        logger = logging.getLogger(__name__)
        if trace_id is None and "runtime_trace" in self.context.registry.list_services():
            trace_id = self.context.registry.get_service("runtime_trace").new_trace_id()
        job = JobRecord(id=self._next_id, name=name, status="running", trace_id=trace_id)
        self._next_id += 1
        self._jobs.append(job)
        logger.debug("Job started: id=%s name=%s", job.id, job.name)
        self.context.registry.emit("job.started", {"id": job.id, "name": job.name, "trace_id": trace_id})

        try:
            job.result = handler()
        except Exception as exc:
            job.status = "failed"
            job.error = str(exc)
            job.finished_at = datetime.now(timezone.utc)
            logger.exception("Job failed: id=%s name=%s", job.id, job.name)
            self.context.registry.emit(
                "job.failed",
                {"id": job.id, "name": job.name, "error": job.error, "trace_id": trace_id},
            )
            raise

        job.status = "completed"
        job.finished_at = datetime.now(timezone.utc)
        logger.debug("Job completed: id=%s name=%s result=%r", job.id, job.name, job.result)
        self.context.registry.emit("job.completed", {"id": job.id, "name": job.name, "trace_id": trace_id})
        return job

    def list_jobs(self) -> list[JobRecord]:
        return list(reversed(self._jobs))
