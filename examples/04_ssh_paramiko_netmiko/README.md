# 04 SSH Paramiko Netmiko

This folder contains SSH and Telnet-oriented network automation exercises using Paramiko and Netmiko.

## Purpose

The purpose of this folder is to practice direct device access, basic reachability checks, SSH onboarding, and running-config comparison.

## What it shows

- connecting to devices with Paramiko
- connecting to devices with Netmiko
- running basic show commands
- checking ICMP reachability
- checking TCP ports `22` and `23`
- classifying SSH/Telnet reachability states
- enabling SSH-related configuration on devices
- disabling Telnet access by enforcing SSH transport
- collecting running-config output
- generating an HTML diff between device configs

## Type of exercises

The scripts include both read-only examples and operational scripts that can change device configuration. The SSH/Telnet onboarding scripts should be treated carefully in a real lab because they modify device access settings.

## Role in the repository

This folder builds practical device-access skills that support the later Ansible, Nornir, IOS upgrade, RESTCONF, and monitoring projects.
