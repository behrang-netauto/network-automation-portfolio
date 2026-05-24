from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests
import urllib3


STATUS_OK = "OK"
STATUS_NO_DATA = "NO_DATA"
STATUS_FAILED_HTTP = "FAILED_HTTP"
STATUS_FAILED_TIMEOUT = "FAILED_TIMEOUT"


@dataclass
class RestconfClient:
    device_name: str
    host: str
    scheme: str
    port: int
    base_path: str
    username: str
    password: str
    verify_ssl: bool
    timeout_sec: int

    def __post_init__(self) -> None:
        if not self.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    @classmethod
    def from_config(cls, config: dict[str, Any], device: dict[str, Any], timeout_sec: int | None = None) -> "RestconfClient":
        defaults = config["defaults"]
        restconf = config["restconf"]
        auth = config["auth"]

        password_env = auth["password_env"]
        password = os.environ.get(password_env)
        if not password:
            raise RuntimeError(f"Missing required environment variable: {password_env}")

        return cls(
            device_name=device["name"],
            host=device["host"],
            scheme=defaults.get("scheme", "https"),
            port=int(defaults.get("port", 443)),
            base_path=restconf.get("base_path", "/restconf/data"),
            username=auth["username"],
            password=password,
            verify_ssl=bool(defaults.get("verify_ssl", False)),
            timeout_sec=int(timeout_sec or restconf.get("request_timeout_sec", 15)),
        )

    def build_url(self, resource_path: str) -> str:
        base = self.base_path.strip("/")
        resource = resource_path.strip("/")
        return f"{self.scheme}://{self.host}:{self.port}/{base}/{resource}"

    def _headers(self, has_body: bool = False) -> dict[str, str]:
        headers = {
            "Accept": "application/yang-data+json",
        }
        if has_body:
            headers["Content-Type"] = "application/yang-data+json"
        return headers

    def request(
        self,
        method: str,
        resource_path: str,
        payload: dict[str, Any] | None = None,
        timeout_sec: int | None = None,
    ) -> dict[str, Any]:
        method = method.upper()
        url = self.build_url(resource_path)
        has_body = payload is not None

        try:
            response = requests.request(
                method=method,
                url=url,
                auth=(self.username, self.password),
                headers=self._headers(has_body=has_body),
                json=payload,
                verify=self.verify_ssl,
                timeout=timeout_sec or self.timeout_sec,
            )
        except requests.Timeout as exc:
            return {
                "status": STATUS_FAILED_TIMEOUT,
                "http_status": None,
                "method": method,
                "endpoint": resource_path,
                "url": url,
                "error": str(exc),
                "data": None,
                "text": None,
            }
        except requests.RequestException as exc:
            return {
                "status": STATUS_FAILED_HTTP,
                "http_status": None,
                "method": method,
                "endpoint": resource_path,
                "url": url,
                "error": str(exc),
                "data": None,
                "text": None,
            }

        return self.handle_response(method=method, resource_path=resource_path, url=url, response=response)

    @staticmethod
    def handle_response(method: str, resource_path: str, url: str, response: requests.Response) -> dict[str, Any]:
        result = {
            "status": None,
            "http_status": response.status_code,
            "method": method,
            "endpoint": resource_path,
            "url": url,
            "error": None,
            "data": None,
            "text": response.text,
        }

        if response.status_code < 200 or response.status_code >= 300:
            result["status"] = STATUS_FAILED_HTTP
            result["error"] = response.text
            return result

        if response.status_code == 204 or not response.text.strip():
            result["status"] = STATUS_NO_DATA
            return result

        try:
            result["data"] = response.json()
        except ValueError:
            result["status"] = STATUS_NO_DATA
            result["error"] = "Response body is not valid JSON"
            return result

        result["status"] = STATUS_OK
        return result

    def get(self, resource_path: str, timeout_sec: int | None = None) -> dict[str, Any]:
        return self.request("GET", resource_path, timeout_sec=timeout_sec)

    def put(self, resource_path: str, payload: dict[str, Any], timeout_sec: int | None = None) -> dict[str, Any]:
        return self.request("PUT", resource_path, payload=payload, timeout_sec=timeout_sec)

    def patch(self, resource_path: str, payload: dict[str, Any], timeout_sec: int | None = None) -> dict[str, Any]:
        return self.request("PATCH", resource_path, payload=payload, timeout_sec=timeout_sec)

    def delete(self, resource_path: str, timeout_sec: int | None = None) -> dict[str, Any]:
        return self.request("DELETE", resource_path, timeout_sec=timeout_sec)


def is_success_no_body(result: dict[str, Any]) -> bool:
    return result["status"] in {STATUS_OK, STATUS_NO_DATA} and result["http_status"] in {200, 201, 202, 204}


def is_not_found(result: dict[str, Any]) -> bool:
    return result["status"] == STATUS_FAILED_HTTP and result["http_status"] == 404


def contains_text(value: Any, expected: str) -> bool:
    if isinstance(value, dict):
        return any(contains_text(v, expected) for v in value.values())
    if isinstance(value, list):
        return any(contains_text(v, expected) for v in value)
    if isinstance(value, str):
        return expected in value
    return False
