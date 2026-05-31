from modular_registry_framework.core.registry import ModuleMetadata, Registry


def test_registry_orders_screens_by_area_order_and_title():
    registry = Registry()

    registry.add_screen("Reports", "Late", lambda parent, context: None, order=20)
    registry.add_screen("Reports", "Early", lambda parent, context: None, order=10)
    registry.add_screen("Admin", "Settings", lambda parent, context: None, order=50)

    screens = registry.list_screens()

    assert [screen.title for screen in screens] == ["Settings", "Early", "Late"]


def test_registry_emits_event_to_registered_handlers():
    registry = Registry()
    seen = []

    registry.on("record.created", lambda payload: seen.append(payload["id"]))

    registry.emit("record.created", {"id": 7})

    assert seen == [7]


def test_registry_tracks_module_metadata():
    registry = Registry()

    registry.add_module(
        ModuleMetadata(
            name="records",
            title="Records",
            description="Record management",
            dependencies=("audit_log",),
        )
    )

    assert registry.list_modules()["records"].dependencies == ("audit_log",)
    assert registry.list_module_order() == ["records"]


def test_registry_supports_wildcard_event_handlers():
    registry = Registry()
    seen = []

    registry.on("*", lambda payload: seen.append(payload))

    registry.emit("file.imported", {"path": "data.csv"})

    assert seen == [{"event_name": "file.imported", "payload": {"path": "data.csv"}}]


def test_registry_tracks_importers_and_report_sections():
    registry = Registry()

    registry.add_file_importer("csv", lambda path, context: [], label="CSV")
    registry.add_report_section("summary", "Summary", lambda context: "Done", order=20)

    assert ".csv" in registry.list_file_importers()
    assert registry.get_file_importer(".csv").label == "CSV"
    assert registry.list_report_sections()[0].name == "summary"


def test_registry_tracks_data_ports_and_flows():
    registry = Registry()

    registry.add_data_input("importers", "files", "file")
    registry.add_data_output("importers", "records", "records")
    registry.add_flow("port:importers:input:files", "port:importers:output:records", "parse")

    assert registry.list_data_ports()[0].direction == "input"
    assert registry.list_data_ports()[1].direction == "output"
    assert registry.list_flows()[0].label == "parse"


def test_registry_tracks_health_checks_exporters_and_api_clients():
    registry = Registry()

    registry.add_health_check("ready", "Ready", lambda context: {"status": "pass"})
    registry.add_exporter("json", ".json", lambda data: "{}", "JSON")
    registry.add_api_client("example", "Example", object())

    assert "ready" in registry.list_health_checks()
    assert registry.get_exporter("json").extension == ".json"
    assert registry.get_api_client("example").label == "Example"
