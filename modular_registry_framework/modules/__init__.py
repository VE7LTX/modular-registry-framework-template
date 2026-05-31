from .artifact_library import module as artifact_library
from .audit_log import module as audit_log
from .dashboard import module as dashboard
from .diagnostics import module as diagnostics
from .example import module as example
from .flow_graph import module as flow_graph
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
    flow_graph,
    example,
)

__all__ = ["MODULES"]
