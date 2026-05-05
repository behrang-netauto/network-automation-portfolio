import json
from pathlib import Path

from src.design_contracts import (
    REQUIRED_STAGE1_HANDOFF_DEVICE_FIELDS,
    has_minimal_stage1_handoff_device_contract,
    missing_stage1_handoff_device_fields,
)


FIXTURE = Path(__file__).resolve().parent / "fixtures" / "sample_stage1_handoff.json"


def test_sample_stage1_handoff_fixture_has_devices():
    handoff = json.loads(FIXTURE.read_text(encoding="utf-8"))

    assert "devices" in handoff
    assert isinstance(handoff["devices"], list)
    assert handoff["devices"], "sample handoff must contain at least one device"


def test_sample_stage1_handoff_device_has_required_fields():
    handoff = json.loads(FIXTURE.read_text(encoding="utf-8"))
    device = handoff["devices"][0]

    assert has_minimal_stage1_handoff_device_contract(device) is True
    assert missing_stage1_handoff_device_fields(device) == []


def test_missing_handoff_fields_are_reported():
    incomplete_device = {
        "inventory_hostname": "R1",
        "host": "192.0.2.10",
    }

    missing = missing_stage1_handoff_device_fields(incomplete_device)

    assert set(missing) == REQUIRED_STAGE1_HANDOFF_DEVICE_FIELDS - set(incomplete_device)
    assert has_minimal_stage1_handoff_device_contract(incomplete_device) is False
