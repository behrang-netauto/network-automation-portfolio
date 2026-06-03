# 03 Work by Config File

This folder introduces configuration-driven scripts, simple inventory handling, Netmiko examples, ping checks, logging, and parsing of generated output.

## Purpose

The purpose of this folder is to move from standalone Python exercises toward scripts that read input data, connect to devices, run commands, and write logs or summaries.

## What it shows

- helper functions for parsing device config text
- reading config files safely
- generating VLAN configuration snippets
- building and reading CSV inventory data
- using Netmiko for device access
- running ping checks from a network device
- writing raw and classified ping results to log files
- parsing a log summary after command execution
- early experimentation with running-config backup through SCP

## Type of exercises

The scripts are still learning-oriented, but they are closer to real network automation workflows than the earlier folders. Several examples combine input files, device connections, command execution, and output files.

## Role in the repository

This folder is a transition point. It bridges basic Python practice and the larger project-style work under `06_netauto_ecosystem`.
