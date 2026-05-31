from pathlib import Path

import pytest

from modular_registry_framework.core.settings import Settings


def sample_values():
    return {
        "app.enabled": True,
        "app.name": "Template App",
        "app.retries": 3,
        "app.tags": ["local", "template"],
        "app.thresholds": {"warn": 10, "fail": 20},
    }


@pytest.mark.parametrize("extension", [".json", ".jsonl", ".xml", ".yaml", ".yml"])
def test_settings_round_trip_supported_formats(tmp_path: Path, extension: str):
    path = tmp_path / f"settings{extension}"
    settings = Settings(sample_values())

    settings.save(path)
    loaded = Settings.load(path)

    assert loaded.values == sample_values()


def test_jsonl_settings_load_single_key_records(tmp_path: Path):
    path = tmp_path / "settings.jsonl"
    path.write_text('{"app.name": "Template App"}\n{"app.retries": 3}\n', encoding="utf-8")

    settings = Settings.load(path)

    assert settings.values == {"app.name": "Template App", "app.retries": 3}


def test_yaml_settings_loads_simple_hand_written_values(tmp_path: Path):
    path = tmp_path / "settings.yaml"
    path.write_text(
        "\n".join(
            [
                "# local settings",
                "app.name: Template App",
                "app.enabled: true",
                "app.retries: 3",
            ]
        ),
        encoding="utf-8",
    )

    settings = Settings.load(path)

    assert settings.values == {
        "app.name": "Template App",
        "app.enabled": True,
        "app.retries": 3,
    }


def test_settings_reject_unknown_format(tmp_path: Path):
    path = tmp_path / "settings.toml"
    path.write_text("app.name = Template App", encoding="utf-8")

    with pytest.raises(ValueError, match="Unsupported settings format"):
        Settings.load(path)

