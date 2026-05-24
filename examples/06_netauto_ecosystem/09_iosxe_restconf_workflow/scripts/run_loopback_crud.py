from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.restconf_client import (  # noqa: E402
    RestconfClient,
    STATUS_FAILED_HTTP,
    STATUS_FAILED_TIMEOUT,
    STATUS_NO_DATA,
    STATUS_OK,
    contains_text,
    is_not_found,
    is_success_no_body,
)


STATUS_SKIPPED_RESTCONF_UNAVAILABLE = "SKIPPED_RESTCONF_UNAVAILABLE"
STATUS_SKIPPED_PREEXISTING_RESOURCE = "SKIPPED_PREEXISTING_RESOURCE"


def load_config() -> dict[str, Any]:
    with (PROJECT_ROOT / "config.yml").open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_evidence_dirs(root: Path, run: str) -> dict[str, Path]:
    paths = {
        "logs": root / "logs",
        "requests": root / "requests" / run,
        "responses": root / "responses" / run,
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def safe_name(device_name: str) -> str:
    return device_name.lower().replace(" ", "_").replace("-", "_")


def loopback_resource(config: dict[str, Any]) -> str:
    restconf = config["restconf"]
    loopback_id = int(config["lab_object"]["loopback_id"])
    return f"{restconf['native_interface_endpoint'].strip('/')}/Loopback={loopback_id}"


def build_create_payload(config: dict[str, Any], description: str | None = None) -> dict[str, Any]:
    lab = config["lab_object"]
    loopback_id = int(lab["loopback_id"])

    return {
        "Cisco-IOS-XE-native:Loopback": {
            "name": loopback_id,
            "description": description or lab["description_create"],
            "ip": {
                "address": {
                    "primary": {
                        "address": lab["ipv4_address"],
                        "mask": lab["ipv4_mask"],
                    }
                }
            },
        }
    }


def build_update_payload(config: dict[str, Any]) -> dict[str, Any]:
    lab = config["lab_object"]
    loopback_id = int(lab["loopback_id"])

    return {
        "Cisco-IOS-XE-native:Loopback": {
            "name": loopback_id,
            "description": lab["description_update"],
        }
    }


def save_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def step_record(name: str, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "name": name,
        "method": result["method"],
        "endpoint": result["endpoint"],
        "status": result["status"],
        "http_status": result["http_status"],
        "error": result["error"],
    }


def cleanup(client: RestconfClient, resource: str) -> dict[str, Any]:
    result = client.delete(resource)

    if is_success_no_body(result) or is_not_found(result):
        cleanup_status = STATUS_OK
    elif result["status"] == STATUS_FAILED_TIMEOUT:
        cleanup_status = STATUS_FAILED_TIMEOUT
    else:
        cleanup_status = STATUS_FAILED_HTTP

    return {
        "attempted": True,
        "status": cleanup_status,
        "method": result["method"],
        "endpoint": result["endpoint"],
        "http_status": result["http_status"],
        "error": result["error"],
    }


def apply_cleanup(result: dict[str, Any], client: RestconfClient, resource: str) -> None:
    cleanup_result = cleanup(client, resource)

    result["cleanup_attempted"] = cleanup_result["attempted"]
    result["cleanup_status"] = cleanup_result["status"]

    result["steps"].append(
        {
            "name": "cleanup_delete_loopback",
            "method": cleanup_result["method"],
            "endpoint": cleanup_result["endpoint"],
            "status": cleanup_result["status"],
            "http_status": cleanup_result["http_status"],
            "error": cleanup_result["error"],
        }
    )


def run_device(config: dict[str, Any], device: dict[str, Any], paths: dict[str, Path]) -> dict[str, Any]:
    restconf = config["restconf"]
    request_timeout = int(restconf["request_timeout_sec"])
    health_timeout = int(restconf["health_timeout_sec"])

    client = RestconfClient.from_config(config, device, timeout_sec=request_timeout)
    resource = loopback_resource(config)
    dev_safe = safe_name(device["name"])

    result: dict[str, Any] = {
        "device": device["name"],
        "host": device["host"],
        "workflow": "loopback_crud",
        "final_status": None,
        "steps": [],
        "created_by_script": False,
        "cleanup_attempted": False,
        "cleanup_status": None,
    }

    health = client.get(restconf["health_endpoint"], timeout_sec=health_timeout)
    result["steps"].append(step_record("health_check", health))

    if health["status"] != STATUS_OK:
        result["final_status"] = STATUS_SKIPPED_RESTCONF_UNAVAILABLE
        return result

    preexisting = client.get(resource)
    result["steps"].append(step_record("check_preexisting_loopback", preexisting))

    if preexisting["status"] == STATUS_OK:
        result["final_status"] = STATUS_SKIPPED_PREEXISTING_RESOURCE
        return result

    if preexisting["status"] == STATUS_FAILED_TIMEOUT:
        result["final_status"] = STATUS_FAILED_TIMEOUT
        return result

    if not is_not_found(preexisting):
        result["final_status"] = STATUS_FAILED_HTTP
        return result

    create_payload = build_create_payload(config)
    create_payload_file = paths["requests"] / f"{dev_safe}_create_payload.json"
    save_json(create_payload_file, create_payload)

    create = client.put(resource, create_payload)
    result["steps"].append(step_record("create_loopback", create))

    if not is_success_no_body(create):
        result["final_status"] = create["status"]
        return result

    result["created_by_script"] = True

    read_create = client.get(resource)
    result["steps"].append(step_record("read_after_create", read_create))

    if read_create["status"] != STATUS_OK:
        apply_cleanup(result, client, resource)
        result["final_status"] = read_create["status"]
        return result

    update_payload = build_update_payload(config)
    update_payload_file = paths["requests"] / f"{dev_safe}_update_payload.json"
    save_json(update_payload_file, update_payload)

    update = client.patch(resource, update_payload)
    result["steps"].append(step_record("update_description_patch", update))

    if not is_success_no_body(update):
        fallback_payload = build_create_payload(config, description=config["lab_object"]["description_update"])
        fallback_payload_file = paths["requests"] / f"{dev_safe}_update_fallback_put_payload.json"
        save_json(fallback_payload_file, fallback_payload)

        fallback = client.put(resource, fallback_payload)
        result["steps"].append(step_record("update_description_fallback_put", fallback))

        if not is_success_no_body(fallback):
            apply_cleanup(result, client, resource)
            result["final_status"] = fallback["status"]
            return result

    read_update = client.get(resource)
    result["steps"].append(step_record("read_after_update", read_update))

    if read_update["status"] != STATUS_OK:
        apply_cleanup(result, client, resource)
        result["final_status"] = read_update["status"]
        return result

    expected_description = config["lab_object"]["description_update"]
    if not contains_text(read_update["data"], expected_description):
        apply_cleanup(result, client, resource)
        result["final_status"] = STATUS_NO_DATA
        return result

    delete = client.delete(resource)
    result["steps"].append(step_record("delete_loopback", delete))

    if not is_success_no_body(delete):
        result["cleanup_attempted"] = True
        result["cleanup_status"] = STATUS_FAILED_HTTP
        result["final_status"] = delete["status"]
        return result

    result["cleanup_attempted"] = True
    result["cleanup_status"] = STATUS_OK

    read_delete = client.get(resource)
    read_delete_step = step_record("read_after_delete", read_delete)

    if is_not_found(read_delete):
        read_delete_step["status"] = STATUS_OK
        read_delete_step["expected_not_found"] = True
        result["steps"].append(read_delete_step)
        result["final_status"] = STATUS_OK
        return result

    result["steps"].append(read_delete_step)

    if read_delete["status"] == STATUS_FAILED_TIMEOUT:
        result["final_status"] = STATUS_FAILED_TIMEOUT
    else:
        result["final_status"] = STATUS_FAILED_HTTP

    return result


def main() -> int:
    config = load_config()
    run = run_id()
    evidence_root = PROJECT_ROOT / config["evidence"]["root"]
    paths = ensure_evidence_dirs(evidence_root, run)

    results = []
    for device in config["devices"]:
        device_result = run_device(config, device, paths)
        results.append(device_result)

        per_device_file = paths["responses"] / f"{safe_name(device['name'])}_crud_steps.json"
        save_json(per_device_file, device_result)

    summary = {
        "run_id": run,
        "workflow": "loopback_crud",
        "results": results,
    }

    summary_file = paths["responses"] / "crud_summary.json"
    save_json(summary_file, summary)

    log_file = paths["logs"] / f"{run}_crud_run.txt"
    with log_file.open("w", encoding="utf-8") as file:
        file.write(f"Run ID: {run}\n")
        file.write("Workflow: loopback_crud\n\n")

        for item in results:
            file.write(f"{item['device']} ({item['host']}): {item['final_status']}\n")
            file.write(f"  created_by_script: {item['created_by_script']}\n")
            file.write(f"  cleanup_attempted: {item['cleanup_attempted']}\n")
            file.write(f"  cleanup_status: {item['cleanup_status']}\n")
            for step in item["steps"]:
                file.write(
                    f"  - {step['name']}: {step['status']} "
                    f"http={step['http_status']} error={step['error']}\n"
                )
            file.write("\n")

    print(f"CRUD summary: {summary_file}")
    print(f"CRUD log: {log_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
