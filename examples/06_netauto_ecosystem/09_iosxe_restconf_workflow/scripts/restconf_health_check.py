from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.restconf_client import RestconfClient, STATUS_OK, STATUS_NO_DATA  # noqa: E402


STATUS_RESTCONF_AVAILABLE = "RESTCONF_AVAILABLE"


def load_config() -> dict[str, Any]:
    with (PROJECT_ROOT / "config.yml").open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_evidence_dirs(root: Path, run: str) -> dict[str, Path]:
    paths = {
        "logs": root / "logs",
        "responses": root / "responses" / run,
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def has_native_interface_structure(data: Any) -> bool:
    if not isinstance(data, dict):
        return False

    return (
        "Cisco-IOS-XE-native:interface" in data
        or "interface" in data
        or any("interface" in str(key) for key in data.keys())
    )


def check_device(config: dict[str, Any], device: dict[str, Any]) -> dict[str, Any]:
    restconf = config["restconf"]
    health_timeout = int(restconf["health_timeout_sec"])
    request_timeout = int(restconf["request_timeout_sec"])

    client = RestconfClient.from_config(config, device, timeout_sec=request_timeout)

    health = client.get(restconf["health_endpoint"], timeout_sec=health_timeout)

    result = {
        "device": device["name"],
        "host": device["host"],
        "workflow": "restconf_health_check",
        "final_status": health["status"],
        "steps": [
            {
                "name": "health_check",
                "method": "GET",
                "endpoint": restconf["health_endpoint"],
                "status": health["status"],
                "http_status": health["http_status"],
                "error": health["error"],
            }
        ],
    }

    if health["status"] != STATUS_OK:
        return result

    native = client.get(restconf["native_interface_endpoint"], timeout_sec=request_timeout)

    native_step_status = native["status"]
    if native["status"] == STATUS_OK and not has_native_interface_structure(native["data"]):
        native_step_status = STATUS_NO_DATA

    result["steps"].append(
        {
            "name": "native_interface_read",
            "method": "GET",
            "endpoint": restconf["native_interface_endpoint"],
            "status": native_step_status,
            "http_status": native["http_status"],
            "error": native["error"],
        }
    )

    if health["status"] == STATUS_OK and native_step_status == STATUS_OK:
        result["final_status"] = STATUS_RESTCONF_AVAILABLE
    else:
        result["final_status"] = native_step_status

    return result


def main() -> int:
    config = load_config()
    run = run_id()
    evidence_root = PROJECT_ROOT / config["evidence"]["root"]
    paths = ensure_evidence_dirs(evidence_root, run)

    devices = config["devices"]
    max_workers = int(config["execution"]["max_workers"])

    results: list[dict[str, Any]] = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(check_device, config, device) for device in devices]
        for future in as_completed(futures):
            results.append(future.result())

    results = sorted(results, key=lambda item: item["device"])

    summary = {
        "run_id": run,
        "workflow": "restconf_health_check",
        "results": results,
    }

    summary_file = paths["responses"] / "health_check_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    log_file = paths["logs"] / f"{run}_health_check.txt"
    with log_file.open("w", encoding="utf-8") as file:
        file.write(f"Run ID: {run}\n")
        file.write("Workflow: restconf_health_check\n\n")
        for result in results:
            file.write(f"{result['device']} ({result['host']}): {result['final_status']}\n")
            for step in result["steps"]:
                file.write(
                    f"  - {step['name']}: {step['status']} "
                    f"http={step['http_status']} error={step['error']}\n"
                )
            file.write("\n")

    print(f"Health check summary: {summary_file}")
    print(f"Health check log: {log_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
