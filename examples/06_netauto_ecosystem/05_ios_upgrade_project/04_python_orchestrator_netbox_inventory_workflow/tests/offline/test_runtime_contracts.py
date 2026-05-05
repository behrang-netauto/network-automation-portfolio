from src.design_contracts import is_supported_runtime_pairing


def test_supported_runtime_pairings_are_accepted():
    assert is_supported_runtime_pairing("netmiko", "scp") is True
    assert is_supported_runtime_pairing("scrapli", "copy_command") is True


def test_unsupported_runtime_pairings_are_rejected():
    assert is_supported_runtime_pairing("netmiko", "copy_command") is False
    assert is_supported_runtime_pairing("scrapli", "scp") is False
