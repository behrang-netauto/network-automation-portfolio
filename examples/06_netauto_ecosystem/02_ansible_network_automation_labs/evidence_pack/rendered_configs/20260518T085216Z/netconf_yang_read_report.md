# NETCONF/YANG Read Report

Run ID: `20260518T085216Z`

This playbook validates a read-only NETCONF path using `ansible.netcommon.netconf_get`.

Report file:
`evidence_pack/rendered_configs/20260518T085216Z/netconf_yang_read_report.md`

## Summary

| Host alias | Management IP | Connection | Port | Check name | Status | Output path | Error |
|---|---|---|---:|---|---|---|---|



| csr1000v_netconf | 192.168.2.64 | ansible.netcommon.netconf | 830 | hostname_native | ok | `evidence_pack/command_outputs/20260518T085216Z/csr1000v_netconf/netconf_hostname_get.xml` |  |


| csr1000v_netconf | 192.168.2.64 | ansible.netcommon.netconf | 830 | interfaces_state | ok | `evidence_pack/command_outputs/20260518T085216Z/csr1000v_netconf/netconf_interfaces_state.xml` |  |

## Checks



### hostname_native

Host alias: `csr1000v_netconf`

Description:

Read IOS XE hostname using Cisco-IOS-XE-native YANG model

Status: `ok`

Output file:

`evidence_pack/command_outputs/20260518T085216Z/csr1000v_netconf/netconf_hostname_get.xml`




### interfaces_state

Host alias: `csr1000v_netconf`

Description:

Read interface state using IETF interfaces YANG model

Status: `ok`

Output file:

`evidence_pack/command_outputs/20260518T085216Z/csr1000v_netconf/netconf_interfaces_state.xml`



## Notes

- Design: data-driven list of NETCONF checks from `netconf_checks`
- Mechanism: NETCONF connection with YANG-modeled read operations
- Operation: `ansible.netcommon.netconf_get`
- Scope: read-only validation, no NETCONF configuration push
