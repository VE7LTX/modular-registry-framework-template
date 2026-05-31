from .artifact_library import module as artifact_library
from .audit_log import module as audit_log
from .dashboard import module as dashboard
from .diagnostics import module as diagnostics
from .example import module as example
from .help import module as help
from .importers import module as importers
from .jobs import module as jobs
from .reports import module as reports
from .settings_manager import module as settings_manager

MODULES = (
    audit_log,
    diagnostics,
    settings_manager,
    artifact_library,
    jobs,
    importers,
    reports,
    help,
    dashboard,
    example,
)

__all__ = ["MODULES"]
