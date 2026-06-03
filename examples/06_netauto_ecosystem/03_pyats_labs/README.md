# pyATS / Genie Labs

This folder contains pyATS and Genie learning labs for connecting to devices, parsing command output, running AEtest workflows, using job files, and experimenting with clean/reload definitions.

## Purpose

The purpose of this folder is to practice pyATS / Genie concepts in small, focused examples before using validation workflows in larger automation projects.
Conceptually, the folder has two tracks:

- parsing and AEtest validation workflows
- clean/reload and schema exploration experiments

## What it contains

| Area | What it contains |
|---|---|
| `testbed.yml` | Main pyATS testbed definition used by the scripts and jobs. |
| `scripts/` | pyATS / Genie scripts for parsing `show version`, extracting uptime, writing JSON/CSV/TXT output, and running AEtest workflows. |
| `jobs/` | pyATS job files used to launch the AEtest scripts. |
| `clean_*.yml` | Clean/reload YAML experiments for device-level and grouped clean scenarios. |
| `dump_*schema*.py` | Helper scripts used to inspect or dump Genie clean schema information. |
| `output/`, `outputs/`, `snapshots/` | Local run outputs and evidence from parsing, uptime, clean/reload, and snapshot experiments. |

## Main workflow themes

### 1. Genie parsing and output generation

The folder includes scripts that connect to lab devices, parse command output such as `show version`, and write results as JSON, text, or CSV artifacts.

### 2. AEtest uptime validation

Several scripts use AEtest structure to connect to devices, extract uptime information, and store results either as one combined JSON output or as per-device JSON files.

### 3. pyATS job execution

The `jobs/` folder contains job files that launch the AEtest scripts in serial or parallel-style workflows.

### 4. Clean/reload experiments

The clean YAML files and schema-dumping helpers capture experiments around pyATS / Genie clean and reload workflows.

## Important files

| File | Role |
|---|---|
| `scripts/pyats_get_show_version_json_txt_files.py` | Connects to devices, parses `show version`, and writes JSON/TXT outputs. |
| `scripts/genie_get_up_time_csv_txt_table.py` | Extracts uptime information and writes CSV/text table output. |
| `scripts/genie_uptime_serial_aetest.py` | Serial AEtest uptime workflow. |
| `scripts/genie_uptime_parallel_once_json_aetest.py` | AEtest workflow that writes one combined JSON result. |
| `scripts/genie_uptime_parallel_per_device_json_aetest.py` | AEtest workflow that writes one JSON result per device. |
| `jobs/uptime_serial_job.py` | Job file for the serial uptime AEtest workflow. |
| `jobs/uptime_job_parallel_once_json.py` | Job file for the combined JSON parallel-style workflow. |
| `jobs/uptime_job_parallel_per_device_json.py` | Job file for the per-device JSON workflow. |

## Notes

This folder is a practical pyATS learning area. Some outputs are local evidence from previous runs. For a clean portfolio view, the most important items are the testbed, scripts, jobs, selected output examples, and clean/reload notes.
