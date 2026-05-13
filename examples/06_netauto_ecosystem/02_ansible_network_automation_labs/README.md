# Ansible Network Automation Labs

This lab demonstrates a small, evidence-driven Ansible workflow for Cisco IOS / IOS XE and NX-OS devices.

The goal is not to build a production Ansible framework. The goal is to show practical network automation fundamentals with clear, readable playbooks and evidence for each workflow step.

## Scope

This lab covers:

- inventory-driven execution
- encrypted credentials with Ansible Vault
- Cisco IOS / IOS XE and NX-OS command execution
- IOS facts collection
- running-config backup
- SNMPv3 candidate configuration rendering
- idempotent IOS baseline configuration with `ios_config`
- conditional SNMPv3 configuration based on pre-checks
- post-change verification and evidence collection

## Lab devices

| Host | Platform | Management IP | Purpose |
|---|---|---:|---|
| `csr1000v` | IOS XE | `192.168.2.64` | IOS XE automation target |
| `iol_r1` | IOS / IOL | `192.168.2.65` | IOS automation target |
| `nxos1` | NX-OS | `192.168.2.66` | NX-OS connectivity and backup target |

## Project structure

```text
02_ansible_network_automation_labs/
├── README.md
├── ansible.cfg
├── requirements.yml
├── requirements.txt
├── pytest.ini
├── .yamllint.yml
├── .ansible-lint
├── inventory/
│   ├── inventory_lab.yml
│   └── group_vars/
│       ├── ios/
│       │   └── vars.yml
│       └── network_devices/
│           └── vault.yml
├── playbooks/
│   ├── 01_connectivity_check.yml
│   ├── 02_gather_ios_facts.yml
│   ├── 03_backup_running_config.yml
│   ├── 04_render_snmpv3_config.yml
│   ├── 05_apply_baseline_config.yml
│   ├── 06_apply_snmpv3_config.yml
│   └── 07_verify_and_collect_evidence.yml
├── templates/
│   └── snmpv3_config.j2
├── tests/
│   ├── fixtures/
│   │   └── snmpv3_template_vars.yml
│   ├── test_inventory_shape.py
│   └── test_snmpv3_template_render.py
├── artifacts/
│   └── .keep
└── evidence_pack/
    ├── command_outputs/
    ├── rendered_configs/
    └── logs/
```

## Playbooks

| Playbook | Purpose |
|---|---|
| `01_connectivity_check.yml` | Checks TCP/22 reachability and runs basic platform-specific show commands |
| `02_gather_ios_facts.yml` | Collects IOS / IOS XE facts and renders a small facts report |
| `03_backup_running_config.yml` | Backs up running-config from IOS / IOS XE and NX-OS devices |
| `04_render_snmpv3_config.yml` | Renders IOS SNMPv3 candidate configuration from a Jinja2 template |
| `05_apply_baseline_config.yml` | Applies a small IOS baseline using `cisco.ios.ios_config` |
| `06_apply_snmpv3_config.yml` | Applies SNMPv3 config only when the named objects are missing |
| `07_verify_and_collect_evidence.yml` | Verifies SNMPv3 state and collects final evidence |

## Variables and secrets

Non-secret IOS variables are stored in:

```text
inventory/group_vars/ios/vars.yml
```

Encrypted credentials and SNMPv3 secrets are stored in:

```text
inventory/group_vars/network_devices/vault.yml
```

The vault file is encrypted with Ansible Vault.

Example local usage:

```bash
ansible-vault view inventory/group_vars/network_devices/vault.yml
```

## Local setup

Python version used for this lab:

```text
Python 3.12.8
```

Create and activate the virtual environment:

```bash
python -m venv .venv-ansible
source .venv-ansible/bin/activate
pip install -r requirements.txt
ansible-galaxy collection install -r requirements.yml
```

## Running a playbook

Example:

```bash
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)

ansible-playbook \
  playbooks/01_connectivity_check.yml \
  -i inventory/inventory_lab.yml \
  --vault-password-file ~/.ansible/vault_pass.txt \
  -e run_id="$RUN_ID"
```

## Ad-hoc command examples

IOS / IOS XE:

```bash
ansible ios \
  -i inventory/inventory_lab.yml \
  -m cisco.ios.ios_command \
  -a "commands='show snmp user'" \
  --vault-password-file ~/.ansible/vault_pass.txt
```

NX-OS:

```bash
ansible nxos \
  -i inventory/inventory_lab.yml \
  -m cisco.nxos.nxos_command \
  -a "commands='show interface brief'" \
  --vault-password-file ~/.ansible/vault_pass.txt
```

## Evidence model

Execution evidence is written under:

```text
evidence_pack/
```

Examples:

```text
evidence_pack/command_outputs/<run_id>/
evidence_pack/rendered_configs/<run_id>/
```

Runtime-only generated files belong under:

```text
artifacts/
```

and are not committed except for `.keep`.

Raw configuration and command-output evidence may contain sensitive operational details. Review and redact evidence before committing.

Examples of values that should be redacted before Git commit:

```text
snmp-server user SNMPUser1 MONITOR-GRP v3 auth sha ******* priv aes 128 *******
User name: *******
```

## Quality checks

Local checks:

```bash
yamllint .
ansible-lint playbooks/
pytest -q tests/
```

Syntax check all playbooks:

```bash
for pb in playbooks/*.yml; do
  ansible-playbook \
    --syntax-check "$pb" \
    -i inventory/inventory_lab.yml \
    --vault-password-file ~/.ansible/vault_pass.txt
done
```

## Notes

This is a lab-oriented workflow. It intentionally keeps the playbooks simple and readable instead of using a larger role-based Ansible structure.

The main learning goals are:

- using inventory and group variables correctly
- separating secrets with Ansible Vault
- executing Cisco network modules
- applying IOS configuration with `ios_config`
- checking idempotent behavior
- using conditionals and filters
- collecting evidence for each automation step
