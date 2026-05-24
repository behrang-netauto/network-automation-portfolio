# Manual RESTCONF Discovery Commands

This document records the manual discovery commands used before running the Python RESTCONF workflows.

The purpose of this manual discovery step is to validate the RESTCONF behavior of the IOS XE lab image before automating the workflow in Python.

## Evidence directories

Command outputs and request payloads are stored under:

- `evidence_pack/cli_verification/manual_discovery/`
- `evidence_pack/requests/manual_discovery/`
- `evidence_pack/responses/manual_discovery/`

The discovery evidence captures:

- manual CLI verification
- RESTCONF health endpoint validation
- native interface endpoint validation
- Loopback create payload validation
- Loopback update payload validation
- delete and post-delete verification

## Discovery goals

This discovery step validates:

- RESTCONF enablement on IOS XE
- the health endpoint for the lab image
- the native interface endpoint for the lab image
- the Loopback payload shape accepted by the device
- the expected CRUD methods for the Python workflow

## Lab devices

```yaml
devices:
  - name: CSR1000v-1
    host: 192.168.2.63

  - name: CSR1000v-2-restconf-down
    host: 192.168.2.64

  - name: CSR1000v-3-preexisting
    host: 192.168.2.65

  - name: CSR1000v-4
    host: 192.168.2.66
```

## Environment variables

Set the RESTCONF credentials before running the curl commands:

```bash
export IOSXE_RESTCONF_USER='test'
export IOSXE_RESTCONF_PASSWORD='****'
```

## Manual CLI verification

Run the following commands on each IOS XE device and save the output under `evidence_pack/cli_verification/manual_discovery/`.

Commands:

```text
terminal length 0
show ip http server status
show running-config | include restconf|ip http|username
```

For the pre-existing-resource test device, also capture:

```text
show running-config interface Loopback123
```

## RESTCONF health endpoint discovery

Validated endpoint: `/restconf/data/ietf-yang-library:modules-state/module-set-id`.

The curl examples use `IOSXE_RESTCONF_USER` and `IOSXE_RESTCONF_PASSWORD` for manual testing convenience. The Python workflow reads the username from `config.yml` and the 
password from `IOSXE_RESTCONF_PASSWORD`.

Example command:

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/ietf-yang-library:modules-state/module-set-id" \
  | tee evidence_pack/responses/manual_discovery/csr1000v_1_health_yang_library.txt
```

Expected result: `HTTP_STATUS:200`.

## Native interface endpoint discovery

Validated endpoint: `/restconf/data/Cisco-IOS-XE-native:native/interface`.

Example command:

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface" \
  | tee evidence_pack/responses/manual_discovery/csr1000v_1_native_interface_get.txt
```

Expected result: `HTTP_STATUS:200`.

The response must be valid JSON and contain the native IOS XE interface structure.

## Loopback create payload discovery

Payload used during manual discovery:

```json
{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 123,
    "description": "RESTCONF managed test interface",
    "ip": {
      "address": {
        "primary": {
          "address": "10.123.123.1",
          "mask": "255.255.255.255"
        }
      }
    }
  }
}
```

Save the payload:

```bash
cat > evidence_pack/requests/manual_discovery/loopback_create_test_payload.json <<'JSON'
{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 123,
    "description": "RESTCONF managed test interface",
    "ip": {
      "address": {
        "primary": {
          "address": "10.123.123.1",
          "mask": "255.255.255.255"
        }
      }
    }
  }
}
JSON
```

PUT create test:

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X PUT \
  --data @evidence_pack/requests/manual_discovery/loopback_create_test_payload.json \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=123" \
  | tee evidence_pack/responses/manual_discovery/loopback_create_test_response.txt
```

Expected result: `HTTP_STATUS:200`, `HTTP_STATUS:201`, or `HTTP_STATUS:204`, depending on the IOS XE RESTCONF response behavior.

## Read after create

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=123" \
  | tee evidence_pack/responses/manual_discovery/loopback_read_after_create.txt
```

Expected result: `HTTP_STATUS:200`.

The response should contain the newly created `Loopback123` interface.

## Loopback update payload discovery

Payload:

```json
{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 123,
    "description": "RESTCONF updated description"
  }
}
```

Save the payload:

```bash
cat > evidence_pack/requests/manual_discovery/loopback_update_test_payload.json <<'JSON'
{
  "Cisco-IOS-XE-native:Loopback": {
    "name": 123,
    "description": "RESTCONF updated description"
  }
}
JSON
```

PATCH update test:

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -H "Content-Type: application/yang-data+json" \
  -X PATCH \
  --data @evidence_pack/requests/manual_discovery/loopback_update_test_payload.json \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=123" \
  | tee evidence_pack/responses/manual_discovery/loopback_patch_update_test_response.txt
```

Expected result: `HTTP_STATUS:200` or `HTTP_STATUS:204`, depending on the IOS XE RESTCONF response behavior.

## Read after update

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=123" \
  | tee evidence_pack/responses/manual_discovery/loopback_read_after_update.txt
```

Expected result: `HTTP_STATUS:200`.

The response should show the updated description: `RESTCONF updated description`.

## Delete cleanup

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -X DELETE \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=123" \
  | tee evidence_pack/responses/manual_discovery/loopback_delete_test_response.txt
```

Expected result: `HTTP_STATUS:200`.

or:

```text
HTTP_STATUS:204
```

depending on the IOS XE RESTCONF response behavior.

## Read after delete

```bash
curl -sk \
  --connect-timeout 5 \
  --max-time 15 \
  -u "${IOSXE_RESTCONF_USER}:${IOSXE_RESTCONF_PASSWORD}" \
  -H "Accept: application/yang-data+json" \
  -w "\nHTTP_STATUS:%{http_code}\n" \
  "https://192.168.2.63/restconf/data/Cisco-IOS-XE-native:native/interface/Loopback=123" \
  | tee evidence_pack/responses/manual_discovery/loopback_read_after_delete.txt
```

Expected result after delete: `HTTP_STATUS:404`.

## Discovery outcome

The following RESTCONF contract was validated or selected for this lab image and Python workflow.

| Item | Validated value |
|---|---|
| Health endpoint | `ietf-yang-library:modules-state/module-set-id` |
| Native interface endpoint | `Cisco-IOS-XE-native:native/interface` |
| Loopback CRUD endpoint | `Cisco-IOS-XE-native:native/interface/Loopback=123` |
| Create method | `PUT` |
| Read method | `GET` |
| Update method | `PATCH` |
| Update fallback | full-resource `PUT` |
| Delete method | `DELETE` |

## Notes

The current lab uses curl with `-k`, which disables TLS certificate verification.

This is acceptable for the current IOS XE lab because the devices use self-signed HTTPS certificates. Full TLS validation is intentionally left out of the first implementation and can be added later as a separate hardening step.
