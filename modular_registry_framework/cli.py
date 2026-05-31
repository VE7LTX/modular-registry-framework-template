from __future__ import annotations

import argparse
from pathlib import Path

from modular_registry_framework.main import build_context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mrf", description="Modular Registry Framework CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("health", help="Run registered health checks.")

    graph_parser = subparsers.add_parser("graph", help="Render or export the flow graph.")
    graph_parser.add_argument("action", choices=("mermaid", "adjacency", "export"))

    template_parser = subparsers.add_parser("template", help="Create a starter app folder.")
    template_parser.add_argument("template_name")
    template_parser.add_argument("target_dir", type=Path)

    scan_parser = subparsers.add_parser("scan", help="Scan a workspace folder.")
    scan_parser.add_argument("path", type=Path)

    secrets_parser = subparsers.add_parser("secrets", help="Scan for likely secrets.")
    secrets_parser.add_argument("path", type=Path)

    module_test_parser = subparsers.add_parser("module-test", help="Generate a module registration test.")
    module_test_parser.add_argument("module_name")
    module_test_parser.add_argument("--tests-dir", type=Path)

    runbook_parser = subparsers.add_parser("runbook", help="Render or save a runbook.")
    runbook_parser.add_argument("--save", action="store_true")

    packs_parser = subparsers.add_parser("packs", help="Render module packs.")
    packs_parser.add_argument("--markdown", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    context = build_context()

    if args.command == "health":
        for result in context.registry.get_service("health_checks").run_all():
            print(f"{result.status.upper()} {result.name}: {result.message}")
        return 0

    if args.command == "graph":
        graph = context.registry.get_service("flow_graph")
        if args.action == "mermaid":
            print(graph.render_mermaid())
        elif args.action == "adjacency":
            print(graph.render_adjacency())
        else:
            exporter = context.registry.get_service("graph_export")
            mermaid = exporter.save_mermaid()
            graph_json = exporter.save_json()
            print(f"Saved {mermaid.path}")
            print(f"Saved {graph_json.path}")
        return 0

    if args.command == "template":
        target = context.registry.get_service("template_generator").create_app(args.template_name, args.target_dir)
        print(f"Created {target}")
        return 0

    if args.command == "scan":
        service = context.registry.get_service("workspace_scanner")
        print(service.render_markdown(service.scan_workspace(args.path)))
        return 0

    if args.command == "secrets":
        service = context.registry.get_service("secret_scanner")
        print(service.render_markdown(service.scan(args.path)))
        return 0

    if args.command == "module-test":
        service = context.registry.get_service("module_test_harness")
        if args.tests_dir:
            path = service.write_registration_test(args.module_name, args.tests_dir)
            print(f"Wrote {path}")
        else:
            print(service.render_registration_test(args.module_name))
        return 0

    if args.command == "runbook":
        service = context.registry.get_service("runbook_generator")
        if args.save:
            record = service.save()
            print(f"Saved {record.path}")
        else:
            print(service.render_markdown())
        return 0

    if args.command == "packs":
        print(context.registry.get_service("module_packs").render_markdown())
        return 0

    raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

