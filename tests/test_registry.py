from modular_registry_framework.core.registry import Registry


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

