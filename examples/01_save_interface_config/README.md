# 01 Save Interface Config

This folder contains small exercises for parsing interface output, saving results to files, and generating simple interface configuration snippets.

## Purpose

The purpose of this folder is to move from basic parsing into simple generated configuration artifacts.

## What it shows

- parsing `show ip interface brief` style output
- using generator functions for interface filtering
- writing command results to text files
- using helper functions for reusable config generation
- creating timestamped output filenames
- reading generated files back for verification

## Type of exercises

The scripts build the same idea in several small steps: find interfaces in `up/up` state, save the filtered results, and then generate a simple access interface configuration using helper functions.

## Role in the repository

This folder is still part of the early learning path. It introduces file-output and generated-config thinking, which becomes more important in the larger automation projects under `06_netauto_ecosystem`.
