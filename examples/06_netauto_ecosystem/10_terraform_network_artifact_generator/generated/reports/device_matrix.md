# Terraform Generated Device Matrix

Site: `lab-primary`

| Device | Platform | Model | Role | Mgmt IP | Execution context | RESTCONF supported | RESTCONF enabled | NETCONF supported | NETCONF enabled |
|---|---|---|---|---|---|---:|---:|---:|---:|
| `csr1000v_1` | `iosxe` | `csr1000v` | `router` | `192.168.2.63` | `ios` | `true` | `true` | `true` | `false` |
| `csr1000v_2` | `iosxe` | `csr1000v` | `router` | `192.168.2.64` | `ios` | `true` | `false` | `true` | `false` |
| `csr1000v_3` | `iosxe` | `csr1000v` | `router` | `192.168.2.65` | `ios` | `true` | `true` | `true` | `false` |
| `csr1000v_4` | `iosxe` | `csr1000v` | `router` | `192.168.2.66` | `ios` | `true` | `true` | `true` | `false` |
| `csr1000v_5` | `iosxe` | `csr1000v` | `router` | `192.168.2.67` | `iosxe_netconf` | `true` | `false` | `true` | `true` |
| `iol_r1` | `ios` | `iol` | `router` | `192.168.2.69` | `ios` | `false` | `false` | `false` | `false` |
| `nxos1` | `nxos` | `nxosv` | `switch` | `192.168.2.68` | `nxos` | `true` | `false` | `false` | `false` |

## Summary

- Total inventory targets: `7`
- Execution contexts: `ios, iosxe_netconf, nxos`
- RESTCONF-supported targets: `6`
- RESTCONF-enabled targets: `3`
- NETCONF-supported targets: `5`
- NETCONF-enabled targets: `1`

## Notes

This report is generated from the Terraform input data model.

Each device entry represents one logical inventory target with one execution context.

RESTCONF and NETCONF artifacts are generated only from targets where the corresponding protocol is enabled.
