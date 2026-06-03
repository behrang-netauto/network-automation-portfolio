# 05 SNMP Paramiko Netmiko

This folder explores SNMPv3 polling, structured result handling, CSV/JSON evidence output, SNMP walks, CPU monitoring, and SSH-triggered debugging.

## Purpose

The purpose of this folder is to practice monitoring-oriented automation with SNMP while still using SSH/Netmiko where device configuration or deeper debug collection is needed.

## What it shows

- SNMPv3 GET operations
- batch OID polling
- structured result dictionaries
- multi-device SNMP polling
- asynchronous and concurrent SNMP execution
- pushing SNMPv3 configuration with Netmiko
- writing CSV and JSON output artifacts
- walking interface-related OIDs
- polling CPU utilization
- triggering SSH debug collection when an SNMP threshold is crossed

## Type of exercises

The folder starts with small SNMP examples and gradually moves toward monitoring-style workflows. Some scripts are simple polling experiments, while others produce evidence artifacts or combine SNMP detection with SSH follow-up actions.

## Role in the repository

This is the most advanced of the early Python folders. It prepares the ground for the Docker-based monitoring, SNMP CPU pipeline, and telemetry projects under `06_netauto_ecosystem`.
