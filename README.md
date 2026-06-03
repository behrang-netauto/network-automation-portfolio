# Python Basics for Network Automation

This repository documents a practical transition from traditional network engineering toward network automation and NetDevOps-style workflows.

It started as a Python learning path for network automation and gradually evolved into a set of hands-on Cisco-oriented labs. The work begins with Python basics and moves toward practical projects involving Ansible, RESTCONF/YANG, NetBox, telemetry, CI/CD, Docker-based monitoring, and Terraform-based artifact generation.

The goal is not to present a production framework. The goal is to document a practical learning and lab-building path through readable code, structured workflows, validation steps, and evidence-backed project outputs.

---

## Learning path

Many labs in this repository were built, adapted, redesigned, or extended while studying network automation references and related material, including:

- *Introduction to Python Network Automation, Volume I*
- *Introduction to Python Network Automation, Volume II*
- *Network Programmability and Automation Fundamentals*
- Cisco DevNet and network programmability material
- Ansible and network automation references

The repository reflects hands-on work around Python scripting, network device access, automation workflows, source-of-truth concepts, model-driven APIs, telemetry, monitoring, CI, and infrastructure-as-code fundamentals.

---

## What this repository contains

| Folder | What it contains |
|---|---|
| `00_basic_warm_up` | Basic Python warm-up scripts for strings, files, regex, generators, and simple anonymization tasks. |
| `01_save_interface_config` | Interface parsing and file-output examples, including small scripts for saving command output and generating interface configuration snippets. |
| `02_lambda_anonymous_function` | Lambda and sorting exercises based on network-style records such as interfaces, VLANs, ACLs, IP addresses, routes, and BGP-like data. |
| `03_work_by_config_file` | Configuration-driven Python examples using device inventories, CSV/YAML-style inputs, Netmiko, ping checks, logging, and parsing. |
| `04_ssh_paramiko_netmiko` | SSH automation examples with Paramiko and Netmiko, including port checks, SSH enforcement, Telnet removal, config collection, and running-config comparison. |
| `05_snmp_paramiko_netmiko` | SNMP-focused monitoring examples with SNMPv3 polling, async/concurrent checks, SNMP walks, CPU monitoring, CSV/JSON evidence, and SSH-triggered debug workflows. |
| `06_netauto_ecosystem` | The main project area of the repository. It contains the larger portfolio-level labs around Ansible, pyATS, Docker/SNMP monitoring, IOS upgrade 
orchestration, NetBox-driven inventory, Nornir, IOS XE telemetry, RESTCONF/YANG automation and Terraform artifact generation. Most folders include their own README, execution notes, evidence, generated artifacts or CI checks. |
| `07_netbox_platform` | NetBox source-of-truth design notes, phased bring-up plans, object modeling, inventory-provider ideas, and write-back contract planning. |

The most important portfolio-level work is concentrated under `06_netauto_ecosystem`. Earlier folders show the learning path and smaller Python/network automation exercises, while `06_netauto_ecosystem` contains the larger end-to-end labs with design notes, evidence, generated artifacts, and CI checks.

---

## Featured project areas

Most portfolio-level projects are under `examples/06_netauto_ecosystem/`.

This is the **main project area** of the repository.

| Project area | Where to look | What you can see |
|---|---|---|
| Practical Ansible workflows for Cisco day-2 network automation | `examples/06_netauto_ecosystem/02_ansible_network_automation_labs` | Inventory-driven Ansible workflows, Ansible Vault, Jinja2 templates, IOS / IOS XE and NX-OS modules, data-driven configuration, NETCONF read-only checks, pytest tests, and CI validation. |
| pyATS / Genie validation labs for network state checks | `examples/06_netauto_ecosystem/03_pyats_labs` | Basic pyATS / Genie validation workflows, clean file usage, uptime and version checks, and test-oriented device-state validation. |
| Docker-based monitoring and operational automation experiments | `examples/06_netauto_ecosystem/04_docker_monitoring` | Dockerized network checks, port monitoring, alerting experiments, Mailpit-based email testing, systemd/timer-based monitoring, and early monitoring workflow experiments. |
| IOS upgrade workflow design with Ansible, pyATS, Python, and NetBox | `examples/06_netauto_ecosystem/05_ios_upgrade_project` | Several staged IOS upgrade designs using Ansible, pyATS, Python orchestration, pluggable CLI/transfer drivers, handoff files, NetBox inventory integration, and write-back logic. |
| Nornir-based mini workflow for inventory-driven automation | `examples/06_netauto_ecosystem/06_nornir_project` | A compact Nornir workflow focused on inventory handling, pre-checks, backups, reload logic, and report generation. |
| SNMPv3 CPU monitoring pipeline with Docker Compose and alerting | `examples/06_netauto_ecosystem/07_snmp_cpu_monitoring_pipeline` | SNMPv3 bootstrap, Docker Compose runtime services, CPU polling, alerting, Mailpit email validation, and curated execution evidence. |
| IOS XE model-driven telemetry pipeline with alerting and TLS validation | `examples/06_netauto_ecosystem/08_iosxe_telemetry_pipeline` | IOS XE model-driven telemetry with configured dial-out subscriptions, Telegraf, InfluxDB, Grafana, alerting, TLS validation, and a complementary dial-in / dynamic telemetry note. |
| IOS XE RESTCONF/YANG CRUD workflow with Python and evidence-backed execution | `examples/06_netauto_ecosystem/09_iosxe_restconf_workflow` | Python-based IOS XE RESTCONF/YANG workflow using Cisco native YANG paths, JSON payloads, Loopback CRUD, per-device failure isolation, cleanup behavior, request/response evidence, and offline CI checks. |
| Terraform-based network automation artifact generator | `examples/06_netauto_ecosystem/10_terraform_network_artifact_generator` | Terraform variables, validation, locals, `templatefile()`, the `hashicorp/local` provider, generated Ansible / RESTCONF / NetBox artifacts, device matrix reporting, and CI-based artifact consistency checks. |

---

## Validation and evidence model

Many project folders include their own:

- `README.md`
- local run instructions
- evidence directories
- generated artifacts
- validation commands
- offline tests
- GitHub Actions workflows

Live device-dependent checks are intentionally kept local to the lab environment. Hosted CI workflows are generally limited to offline-safe checks such as syntax validation, linting, template rendering, payload validation, import checks, and generated artifact consistency.

This separation keeps the repository reproducible without requiring public access to private lab devices.

---

## Current direction

This repository captures the first major build phase of the transition path from traditional network engineering toward network automation and NetDevOps-style workflows.

Future experiments, smaller refactors, and new platform-specific labs may continue in a separate repository so this repository can remain a stable portfolio snapshot while new work continues elsewhere.
