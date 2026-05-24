import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PAYLOAD_DIR = PROJECT_ROOT / "payloads"


def test_payload_directory_exists():
    assert PAYLOAD_DIR.exists()
    assert PAYLOAD_DIR.is_dir()


def test_payload_files_are_valid_json():
    payload_files = sorted(PAYLOAD_DIR.glob("*.json"))

    assert payload_files, "Expected at least one JSON payload file"

    for path in payload_files:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Invalid JSON payload: {path}") from exc
