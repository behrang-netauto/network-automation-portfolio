# 06 Network Automation Ecosystem

This is the main project area of the repository.

It contains the larger, portfolio-level network automation labs that build on the earlier Python practice folders. The work here moves from basic scripting into structured automation workflows with Ansible, pyATS, Docker, Nornir, SNMP, telemetry, RESTCONF/YANG, NetBox-oriented inventory integration, and Terraform-generated artifacts.

## Purpose

The purpose of this folder is to collect the stronger project work in one place and show a practical transition from traditional network engineering toward network automation and NetDevOps-style workflows.

## Project index

| Folder | What it contains |
|---|---|
| `02_ansible_labs` | Older Ansible lab output and saved evidence from early Ansible runs. This is more historical than polished project material. |
| `02_ansible_network_automation_labs` | Structured Ansible network automation labs with inventory, group variables, playbooks, templates, evidence, NETCONF read-only checks, pytest tests, and CI validation. |
| `03_pyats_labs` | pyATS / Genie parsing and validation examples, including testbed usage, AEtest scripts, job files, uptime parsing, output generation, and clean/reload YAML experiments. |
| `04_docker_monitoring` | Dockerized reachability and TCP port monitoring experiments, including JSON inventory, alerting logic, Docker Compose usage, and systemd timer examples. |
| `05_ios_upgrade_project` | Main IOS upgrade project area with Ansible, pyATS, Python orchestrators, pluggable CLI/transfer drivers, staged execution, handoff files, NetBox inventory integration, and write-back planning. |
| `06_nornir_project` | Compact Nornir workflow for inventory handling, pre-checks, backups, reload logic, and JSON report generation. |
| `07_snmp_cpu_monitoring_pipeline` | Dockerized SNMPv3 CPU monitoring pipeline with device bootstrap, polling, threshold evaluation, Mailpit-based email alerting, and curated evidence. |
| `08_iosxe_telemetry_pipeline` | IOS XE model-driven telemetry pipeline using Telegraf, InfluxDB, Grafana, TLS validation, alerting, and complementary dial-in / dynamic telemetry notes. |
| `09_iosxe_restconf_workflow` | Python-based IOS XE RESTCONF/YANG workflow with health checks, native interface read tests, Loopback CRUD, per-device failure isolation, cleanup behavior, request/response evidence, and offline tests. |
| `10_terraform_network_artifact_generator` | Terraform lab that uses typed variables, validation, locals, `templatefile()`, and the `hashicorp/local` provider to generate Ansible, RESTCONF, NetBox, and reporting artifacts. |

## What this folder demonstrates

- inventory-driven automation
- Ansible playbooks and templates
- pyATS / Genie validation workflows
- Dockerized monitoring services
- SNMPv3 polling and alerting
- IOS XE telemetry pipeline design
- RESTCONF/YANG API automation
- staged IOS upgrade workflow design
- NetBox source-of-truth integration patterns
- Terraform artifact generation for nearby automation workflows
- local evidence collection and offline CI checks

## Notes

Most subfolders have their own README, execution notes, generated artifacts, evidence directories, or validation commands.

Live device-dependent workflows are intended to be run in the local lab. Hosted CI workflows are generally kept offline-safe and focus on syntax checks, template rendering, payload validation, import checks, and generated artifact consistency.
