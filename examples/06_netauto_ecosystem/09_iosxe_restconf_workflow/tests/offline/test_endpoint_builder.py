from src.restconf_client import RestconfClient


def make_client() -> RestconfClient:
    return RestconfClient(
        device_name="CSR1000v-1",
        host="192.168.2.63",
        scheme="https",
        port=443,
        base_path="/restconf/data",
        username="test",
        password="test",
        verify_ssl=False,
        timeout_sec=15,
    )


def test_build_url_for_native_interface_endpoint():
    client = make_client()

    url = client.build_url("Cisco-IOS-XE-native:native/interface")

    assert url == (
        "https://192.168.2.63:443/restconf/data/"
        "Cisco-IOS-XE-native:native/interface"
    )


def test_build_url_normalizes_slashes():
    client = make_client()

    url = client.build_url("/Cisco-IOS-XE-native:native/interface/Loopback=123/")

    assert url == (
        "https://192.168.2.63:443/restconf/data/"
        "Cisco-IOS-XE-native:native/interface/Loopback=123"
    )
