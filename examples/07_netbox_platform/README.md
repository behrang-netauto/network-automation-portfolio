# 07 NetBox Platform

This folder contains design notes for a NetBox source-of-truth platform track.

It is documentation-oriented and does not contain executable automation code. The notes capture manual bring-up, planned bootstrap automation, minimum NetBox data modeling, inventory-provider contracts, and write-back behavior for later integration with the IOS upgrade workflow.

## Purpose

The purpose of this folder is to define the NetBox platform and data-model assumptions needed before using NetBox as an inventory and source-of-truth component in network automation workflows.

## What it contains

| Area | What it covers |
|---|---|
| `notes/netbox_phase1/` | Manual NetBox bring-up notes, health checks, service validation, UI validation, and operational facts from the first lab installation. |
| `notes/netbox_phase2/` | Deferred bootstrap automation plan for turning a clean Ubuntu snapshot into a working NetBox instance. |
| `notes/netbox_phase3/` | Minimum NetBox object model, field conventions, population checklist, and lab modeling rules. |
| `notes/netbox_phase4/` | NetBox inventory contract, source selection policy, fail-closed read behavior, and Stage 1 / Stage 2 write-back contract. |

## What it shows

- NetBox platform bring-up planning
- source-of-truth modeling decisions
- minimum lab data model definition
- custom field conventions for upgrade workflows
- inventory-provider contract design
- write-back contract design
- explicit separation between implemented work and deferred automation

## Current status

Phase 1, Phase 3, and Phase 4 notes describe the current design path. Phase 2 is explicitly marked as deferred and remains a future bootstrap automation track.

## Role in the repository

This folder supports the NetBox-driven inventory work in the IOS upgrade project. It should be read as design and planning material, not as a completed NetBox provisioning project.
