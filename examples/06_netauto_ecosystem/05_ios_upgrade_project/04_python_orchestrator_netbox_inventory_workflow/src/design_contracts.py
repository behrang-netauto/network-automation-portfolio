SUPPORTED_RUNTIME_PAIRINGS = {
    ("netmiko", "scp"),
    ("scrapli", "copy_command"),
}

EXPECTED_INVENTORY_SOURCE = "netbox"
EXPECTED_INVENTORY_SITE = "lab-primary"

REQUIRED_STAGE1_HANDOFF_DEVICE_FIELDS = {
    "inventory_hostname",
    "host",
    "port",
    "os",
    "platform",
    "status",
}


def is_supported_runtime_pairing(cli_backend: str, transfer_method: str) -> bool:
    return (cli_backend, transfer_method) in SUPPORTED_RUNTIME_PAIRINGS


def is_expected_inventory_contract(source: str, site: str) -> bool:
    return source == EXPECTED_INVENTORY_SOURCE and site == EXPECTED_INVENTORY_SITE


def missing_stage1_handoff_device_fields(device_record: dict) -> list[str]:
    return sorted(REQUIRED_STAGE1_HANDOFF_DEVICE_FIELDS - set(device_record))


def has_minimal_stage1_handoff_device_contract(device_record: dict) -> bool:
    return not missing_stage1_handoff_device_fields(device_record)
