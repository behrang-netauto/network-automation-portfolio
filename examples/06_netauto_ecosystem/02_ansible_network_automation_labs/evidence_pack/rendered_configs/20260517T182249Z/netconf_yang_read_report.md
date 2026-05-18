# NETCONF/YANG Read Report

Run ID: `20260517T182249Z`

This playbook validates a read-only NETCONF path using `ansible.netcommon.netconf_get`.

Report file:
`evidence_pack/rendered_configs/20260517T182249Z/netconf_yang_read_report.md`

## Summary

| Host alias | Management IP | Connection | Port | Check name | Status | Output path | Error |
|---|---|---|---:|---|---|---|---|


## Checks


## Notes

- Design: data-driven list of NETCONF checks from `netconf_checks`
- Mechanism: NETCONF connection with YANG-modeled read operations
- Operation: `ansible.netcommon.netconf_get`
- Scope: read-only validation, no NETCONF configuration push
