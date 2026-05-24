import requests

from src.restconf_client import (
    RestconfClient,
    STATUS_FAILED_HTTP,
    STATUS_FAILED_TIMEOUT,
    STATUS_NO_DATA,
    STATUS_OK,
)


class FakeResponse:
    def __init__(self, status_code: int, text: str = "", json_data=None):
        self.status_code = status_code
        self.text = text
        self._json_data = json_data

    def json(self):
        if self._json_data is None:
            raise ValueError("no json")
        return self._json_data


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


def test_200_json_response_is_ok():
    response = FakeResponse(
        status_code=200,
        text='{"ok": true}',
        json_data={"ok": True},
    )

    result = RestconfClient.handle_response(
        method="GET",
        resource_path="ietf-yang-library:modules-state/module-set-id",
        url="https://example/restconf/data/test",
        response=response,
    )

    assert result["status"] == STATUS_OK
    assert result["http_status"] == 200
    assert result["data"] == {"ok": True}


def test_204_empty_response_is_no_data():
    response = FakeResponse(status_code=204, text="")

    result = RestconfClient.handle_response(
        method="DELETE",
        resource_path="Cisco-IOS-XE-native:native/interface/Loopback=123",
        url="https://example/restconf/data/test",
        response=response,
    )

    assert result["status"] == STATUS_NO_DATA
    assert result["http_status"] == 204
    assert result["data"] is None


def test_401_response_is_failed_http():
    response = FakeResponse(status_code=401, text="Unauthorized")

    result = RestconfClient.handle_response(
        method="GET",
        resource_path="Cisco-IOS-XE-native:native/interface",
        url="https://example/restconf/data/test",
        response=response,
    )

    assert result["status"] == STATUS_FAILED_HTTP
    assert result["http_status"] == 401
    assert result["error"] == "Unauthorized"


def test_timeout_is_failed_timeout(monkeypatch):
    client = make_client()

    def raise_timeout(*args, **kwargs):
        raise requests.Timeout("timed out")

    monkeypatch.setattr(requests, "request", raise_timeout)

    result = client.get("ietf-yang-library:modules-state/module-set-id", timeout_sec=1)

    assert result["status"] == STATUS_FAILED_TIMEOUT
    assert result["http_status"] is None
    assert "timed out" in result["error"]
