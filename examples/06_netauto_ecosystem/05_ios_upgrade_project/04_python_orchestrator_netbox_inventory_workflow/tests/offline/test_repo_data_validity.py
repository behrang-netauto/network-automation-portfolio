import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]

EXCLUDE_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    "artifacts",
}


def should_skip(path: Path) -> bool:
    return any(part in EXCLUDE_PARTS for part in path.parts)


def test_all_yaml_files_are_valid():
    yaml_files = [
        path
        for path in ROOT.rglob("*")
        if path.suffix in {".yml", ".yaml"} and not should_skip(path)
    ]

    assert yaml_files, "Expected at least one YAML file to validate"

    for path in yaml_files:
        try:
            with path.open("r", encoding="utf-8") as file:
                yaml.safe_load(file)
        except Exception as exc:
            raise AssertionError(f"Invalid YAML file: {path}") from exc


def test_all_json_files_are_valid():
    json_files = [
        path
        for path in ROOT.rglob("*.json")
        if not should_skip(path)
    ]

    assert json_files, "Expected at least one JSON file to validate"

    for path in json_files:
        try:
            with path.open("r", encoding="utf-8") as file:
                json.load(file)
        except Exception as exc:
            raise AssertionError(f"Invalid JSON file: {path}") from exc
