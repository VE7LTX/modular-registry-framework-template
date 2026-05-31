from .api_clients import module as api_clients
from .artifact_library import module as artifact_library
from .audit_log import module as audit_log
from .dashboard import module as dashboard
from .diagnostics import module as diagnostics
from .env_secrets import module as env_secrets
from .example import module as example
from .exporters import module as exporters
from .flow_graph import module as flow_graph
from .graph_export import module as graph_export
from .health_checks import module as health_checks
from .help import module as help
from .importers import module as importers
from .jobs import module as jobs
from .module_packs import module as module_packs
from .module_test_harness import module as module_test_harness
from .records import module as records
from .reports import module as reports
from .runbook_generator import module as runbook_generator
from .runtime_trace import module as runtime_trace
from .secret_scanner import module as secret_scanner
from .settings_manager import module as settings_manager
from .storage import module as storage
from .template_generator import module as template_generator
from .workspace_scanner import module as workspace_scanner

MODULES = (
    audit_log,
    runtime_trace,
    diagnostics,
    health_checks,
    env_secrets,
    settings_manager,
    artifact_library,
    storage,
    records,
    jobs,
    importers,
    exporters,
    api_clients,
    reports,
    help,
    dashboard,
    flow_graph,
    graph_export,
    template_generator,
    module_packs,
    module_test_harness,
    runbook_generator,
    workspace_scanner,
    secret_scanner,
    example,
)

__all__ = ["MODULES"]
