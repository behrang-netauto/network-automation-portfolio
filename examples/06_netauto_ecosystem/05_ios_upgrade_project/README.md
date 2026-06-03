# IOS Upgrade Project

This folder groups several staged IOS upgrade workflow designs.

It is the main IOS upgrade project area in the repository and shows a progression from Ansible/pyATS workflows toward Python orchestration with pluggable runtime drivers, transfer strategies, NetBox inventory integration, and write-back planning.

## Purpose

The purpose of this folder is to explore how an IOS upgrade workflow can be split into controlled stages, validated with pre/post checks, and connected to inventory and evidence models.

## Project index

| Folder | What it contains |
|---|---|
| `01_ansible_pyats_hybrid_workflow` | Hybrid workflow where Ansible handles Stage 1 preparation and pyATS handles Stage 2 reload and verification. |
| `02_ansible_role_workflow` | Ansible role-oriented version of the staged upgrade idea, with separate Stage 1 and Stage 2 playbooks. |
| `03_python_orchestrator_pluggable_cli_transfer_workflow` | Python orchestrator with pluggable CLI drivers, transfer strategies, handoff files, staged execution, and per-device worker logic. |
| `04_python_orchestrator_netbox_inventory_workflow` | More advanced Python orchestrator that adds inventory-provider abstraction, NetBox as a source-of-truth option, offline contract tests, and best-effort write-back logic. |

## High-level progression

1. Use Ansible for preparation and pyATS for reload/post-check validation.
2. Express the same idea with Ansible roles and clearer stage separation.
3. Move the workflow into Python to control orchestration, runtime selection, transfer strategy, handoff files, and per-device result handling.
4. Add NetBox as an inventory provider and introduce source-of-truth read behavior and write-back contracts.

## What it demonstrates

- staged IOS upgrade workflow design
- Stage 1 / Stage 2 separation
- pre-check, backup, transfer, reload, and post-check thinking
- pyATS validation workflows
- Ansible role/playbook structure
- Python orchestration with per-device workers
- pluggable CLI drivers such as Netmiko and Scrapli
- pluggable image transfer strategies
- handoff files between stages
- NetBox-driven inventory resolution
- best-effort write-back design
- offline contract tests around inventory, runtime, and handoff behavior

## Notes

Each subfolder has its own README and should be read as a separate design iteration. The later Python/NetBox workflow is the most complete version, while the earlier folders show the progression and design decisions that led to it.

This folder is not presented as a production upgrade framework. It is a lab and portfolio project that documents staged automation design, validation, and source-of-truth integration patterns.
