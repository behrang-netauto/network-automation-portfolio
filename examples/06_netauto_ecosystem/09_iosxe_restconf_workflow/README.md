# IOS XE RESTCONF Workflow

This project demonstrates a small IOS XE RESTCONF automation workflow with:

- RESTCONF health validation
- native interface read validation
- Loopback CRUD workflow
- per-device failure isolation
- request/response evidence
- offline quality checks
- offline CI

The first implementation is intentionally focused on IOS XE RESTCONF and Cisco IOS XE native YANG paths.

---

## Workflow overview

The main CRUD workflow is implemented as a safe per-device sequence. A failure on one device must not stop the whole run.

```text
health_check
  fail -> SKIPPED_RESTCONF_UNAVAILABLE -> next device

check_preexisting_loopback
  exists -> SKIPPED_PREEXISTING_RESOURCE -> next device

create_loopback
  fail -> FAILED_HTTP / FAILED_TIMEOUT -> next device

read_after_create
  fail -> cleanup attempt -> next device

update_description
  PATCH fail -> fallback full-resource PUT
  fallback PUT fail -> cleanup attempt -> next device

read_after_update
  fail -> cleanup attempt -> next device

delete_loopback
  fail -> final_status may be FAILED_HTTP

read_after_delete
  expected result: 404 / not found
```

---

## RESTCONF methods

| Operation | Method |
|---|---|
| Create | `PUT` |
| Read | `GET` |
| Update | `PATCH` |
| Update fallback | full-resource `PUT` |
| Delete | `DELETE` |

---

## Run

Run the CRUD workflow from the project root:

```bash
python scripts/run_loopback_crud.py
```

---

## Expected high-level results

| Device | Expected final status |
|---|---|
| `CSR1000v-1` | `OK` |
| `CSR1000v-2-restconf-down` | `SKIPPED_RESTCONF_UNAVAILABLE` |
| `CSR1000v-3-preexisting` | `SKIPPED_PREEXISTING_RESOURCE` |
| `CSR1000v-4` | `OK` |

---

## Evidence locations

The workflow writes evidence under `evidence_pack/`.

The main CRUD evidence files are:

- `evidence_pack/logs/<run_id>_crud_run.txt`
- `evidence_pack/requests/<run_id>/`
- `evidence_pack/responses/<run_id>/`

The script stores:

- actual create payload sent
- actual update payload sent
- fallback `PUT` payload, if used
- per-device CRUD step result
- full CRUD summary
- cleanup status

---

## Result schema

Each device result follows a stable schema:

```json
{
  "device": "CSR1000v-1",
  "host": "192.168.2.63",
  "workflow": "loopback_crud",
  "final_status": "OK",
  "steps": [
    {
      "name": "health_check",
      "method": "GET",
      "endpoint": "ietf-yang-library:modules-state/module-set-id",
      "status": "OK",
      "http_status": 200,
      "error": null
    }
  ],
  "created_by_script": true,
  "cleanup_attempted": true,
  "cleanup_status": "OK"
}
```

Final statuses used by the CRUD workflow:

- `OK`
- `NO_DATA`
- `FAILED_HTTP`
- `FAILED_TIMEOUT`
- `SKIPPED_RESTCONF_UNAVAILABLE`
- `SKIPPED_PREEXISTING_RESOURCE`

---

## Evidence model

Evidence root: `evidence_pack/`.

Subdirectories:

- `logs/`
- `requests/`
- `responses/`
- `cli_verification/`

Evidence captures:

- manual CLI verification
- manual RESTCONF discovery outputs
- health check summaries
- CRUD summaries
- per-device CRUD steps
- request payloads actually sent
- response evidence
- local offline quality-check logs

---

## Local offline quality checks

Run from the project root:

```bash
python -m compileall src scripts tests
ruff check .
yamllint .
pytest -q tests/offline
```

To save local quality-check evidence:

```bash
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p evidence_pack/logs/offline_ci

set -o pipefail

{
  set -e

  echo "Run ID: $RUN_ID"
  echo "Workflow: local offline quality checks"
  echo

  echo "== python compileall =="
  python -m compileall src scripts tests
  echo

  echo "== ruff check =="
  ruff check .
  echo

  echo "== yamllint =="
  yamllint .
  echo

  echo "== pytest offline =="
  pytest -q tests/offline
  echo

  echo "Result: PASS"
} 2>&1 | tee "evidence_pack/logs/offline_ci/${RUN_ID}_offline_quality_checks.log"
```

---

## Offline tests

Offline tests are stored under `tests/offline/`.

They validate:

- RESTCONF endpoint building
- response handling
- valid JSON payload files

These tests do not connect to real devices.

---

## GitHub Actions CI

Workflow file: `.github/workflows/restconf-workflow-ci.yml`.

The CI workflow is offline-only.

It does not:

- connect to real devices
- execute live RESTCONF calls
- run CRUD operations
- require device credentials

It runs:

```bash
python -m compileall src scripts tests
ruff check .
yamllint .
pytest -q tests/offline
```

---

## TLS note

The current lab uses `verify_ssl: false`.

This is equivalent to lab-mode `curl -k` behavior and is used because the IOS XE lab devices use self-signed HTTPS certificates.

Full TLS hardening is intentionally left out of the first implementation and may be added later as a follow-up update.

A future TLS hardening update may include:

- trusted CA bundle support
- `verify_ssl: true`
- documented certificate import/validation workflow
- additional evidence for verified TLS connectivity

---

## Scope boundary

### In scope

- IOS XE RESTCONF
- Cisco IOS XE native YANG paths
- YANG Library health check
- native interface read
- Loopback CRUD
- Python `requests`-based workflow
- per-device failure isolation
- request/response evidence
- offline tests
- offline CI

### Out of scope for the first implementation

- NETCONF
- Ansible bootstrap
- automatic RESTCONF enablement
- full TLS hardening
- Postman collection
- live RESTCONF tests in CI
- multi-vendor support
- production credential management
