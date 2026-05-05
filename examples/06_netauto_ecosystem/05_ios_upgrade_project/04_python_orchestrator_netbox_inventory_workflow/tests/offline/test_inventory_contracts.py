from src.design_contracts import is_expected_inventory_contract


def test_expected_netbox_inventory_contract_is_accepted():
    assert is_expected_inventory_contract("netbox", "lab-primary") is True


def test_unexpected_inventory_contracts_are_rejected():
    assert is_expected_inventory_contract("yaml", "lab-primary") is False
    assert is_expected_inventory_contract("netbox", "other-site") is False
