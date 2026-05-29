# Terraform Network Artifact Generator

This lab uses Terraform as a small network automation artifact generator.

It does not provision network infrastructure and it does not connect to network devices. Instead, it takes a structured Terraform input model and generates automation-ready files for nearby workflows such as Ansible, RESTCONF, NetBox-oriented bootstrap data, and a human-readable device matrix.

The purpose is to demonstrate practical Terraform fundamentals in a network automation context:

- typed input variables
- validation
- local values
- `templatefile()`
- the `hashicorp/local` provider
- generated artifacts
- Terraform outputs
- local evidence logs
- GitHub Actions CI with an offline quality gate

## Quick start

From the project directory:

```bash
terraform fmt
terraform init
terraform apply -auto-approve -input=false -no-color
```

Review generated artifacts:

```bash
tree -a generated
or
find generated -type f | sort
```

## Scope

This project is intentionally small. It is an artifact generator, not a production IaC platform.

In scope:

- model lab inventory targets in `terraform.tfvars`
- validate the input model
- derive views with `locals.tf`
- render generated files with Terraform templates
- commit reviewed generated artifacts
- verify locally with Terraform commands
- verify in CI with `fmt`, `init`, `validate`, `plan`, and artifact sync checks

Out of scope:

- provisioning VMs, network devices, or cloud resources
- connecting to real routers or switches
- storing credentials in Terraform
- reading inventory directly from NetBox
- running Ansible, RESTCONF, or NETCONF workflows from Terraform

## Design summary

The data flow is:

```text
terraform.tfvars
  structured lab target model
        ↓
variables.tf
  type constraints + validation
        ↓
locals.tf
  derived views / filtered maps
        ↓
templatefile()
  render automation-ready artifacts
        ↓
local_file resources
  write files under generated/
```

Each device entry represents one logical inventory target with one execution context.

If a physical device needs more than one execution path, it should be represented as separate logical targets. For this lab, `csr1000v_5` represents the NETCONF execution context as its own target with its own management IP.

## Project layout

```text
10_terraform_network_artifact_generator/
├── README.md
├── versions.tf
├── variables.tf
├── locals.tf
├── main.tf
├── outputs.tf
├── terraform.tfvars
├── templates/
│   ├── ansible_inventory.yml.tftpl
│   ├── restconf_config.yml.tftpl
│   ├── netbox_seed.yml.tftpl
│   └── device_matrix.md.tftpl
├── generated/
│   ├── ansible/
│   │   └── inventory.generated.yml
│   ├── restconf/
│   │   └── config.generated.yml
│   ├── netbox/
│   │   └── netbox_seed.generated.yml
│   └── reports/
│       └── device_matrix.md
└── evidence_pack/
    └── logs/
        └── offline_ci/
```

## Terraform files

| File | Purpose |
|---|---|
| `versions.tf` | Pins Terraform version range and the `hashicorp/local` provider |
| `variables.tf` | Defines the external input contract and validation rules |
| `terraform.tfvars` | Holds the structured lab target data |
| `locals.tf` | Builds derived views such as RESTCONF-enabled and NETCONF-enabled targets |
| `main.tf` | Uses `local_file` and `templatefile()` to generate artifacts |
| `outputs.tf` | Prints generated file paths and a short artifact summary |

## Input model

The input model is defined in `terraform.tfvars`.

The current lab model includes:

- five CSR1000v targets
- one NX-OS target
- one IOS/IOL target

Each target has:

- management IP
- platform
- device model
- role
- execution context
- RESTCONF capability and enabled state
- NETCONF capability and enabled state

Example shape:

```hcl
csr1000v_1 = {
  mgmt_ip           = "192.168.2.63"
  platform          = "iosxe"
  device_model      = "csr1000v"
  role              = "router"
  execution_context = "ios"

  restconf = {
    supported = true
    enabled   = true
    port      = 443
  }

  netconf = {
    supported = true
    enabled   = false
    port      = 830
  }
}
```

## Execution contexts

The generated Ansible inventory is built from `execution_context`.

Current execution contexts:

| Context | Meaning |
|---|---|
| `ios` | CLI-based IOS / IOS XE execution with `ansible.netcommon.network_cli` |
| `nxos` | CLI-based NX-OS execution with `ansible.netcommon.network_cli` |
| `iosxe_netconf` | NETCONF execution with `ansible.netcommon.netconf` |

The contract is simple: one Terraform device entry has one execution context.

## Capability model

RESTCONF and NETCONF are modeled as capability blocks:

```hcl
restconf = {
  supported = true
  enabled   = true
  port      = 443
}

netconf = {
  supported = true
  enabled   = false
  port      = 830
}
```

The distinction matters:

- `supported` means the target or platform can support the protocol.
- `enabled` means it is enabled and usable in the current lab context.

Validation prevents impossible combinations such as `enabled = true` with `supported = false`.

Derived views are built in `locals.tf`:

- `restconf_devices`: targets where `restconf.enabled` is `true`
- `netconf_devices`: targets where `netconf.enabled` is `true`

## Generated artifacts

Terraform generates four files:

- `generated/ansible/inventory.generated.yml`
- `generated/restconf/config.generated.yml`
- `generated/netbox/netbox_seed.generated.yml`
- `generated/reports/device_matrix.md`

### Ansible inventory

`generated/ansible/inventory.generated.yml` is generated from all logical inventory targets.

It groups targets by execution context: `ios`, `nxos`, and `iosxe_netconf`.

### RESTCONF config

`generated/restconf/config.generated.yml` is generated only from targets where `restconf.enabled` is `true`.

Credentials are not stored in Terraform. The generated config references the `IOSXE_RESTCONF_USER` and `IOSXE_RESTCONF_PASSWORD` environment variable names.

### NetBox seed data

`generated/netbox/netbox_seed.generated.yml` is a NetBox-oriented seed artifact.

It is not read from NetBox. It is generated from the Terraform input model and can be used as bootstrap/reference data for a NetBox-oriented workflow.

### Device matrix report

`generated/reports/device_matrix.md` is a human-readable summary of the input model and derived target views.

## Local setup

Install Terraform first.

On macOS with Homebrew:

```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
terraform version
```

This lab was validated with Terraform v1.15.4.

## Local run

From the project directory:

```bash
terraform fmt
terraform init
terraform validate
terraform plan -input=false -no-color
terraform apply -auto-approve -input=false -no-color
```

After apply, check the generated files:

```bash
tree -a generated
```

## Local evidence log

This block reruns the same Terraform checks from **Local run** and writes a timestamped log under `evidence_pack/logs/offline_ci/`.

Use this command block to save local validation evidence:

```bash
RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p evidence_pack/logs/offline_ci

set -o pipefail

{
  set -e
  set -o pipefail

  echo "Run ID: $RUN_ID"
  echo "Workflow: Terraform local artifact generator checks"
  echo

  echo "== terraform version =="
  terraform version
  echo

  echo "== terraform fmt -check =="
  terraform fmt -check
  echo

  echo "== terraform init =="
  terraform init -input=false
  echo

  echo "== terraform validate =="
  terraform validate
  echo

  echo "== terraform plan =="
  terraform plan -input=false -no-color
  echo

  echo "== terraform apply =="
  terraform apply -auto-approve -input=false -no-color
  echo

  echo "== terraform output =="
  terraform output
  echo

  echo "== generated artifacts =="
  find generated -type f | sort
  echo

  echo "== generated device matrix preview =="
  sed -n '1,120p' generated/reports/device_matrix.md
  echo

  echo "== generated sync check =="
  git diff --exit-code -- generated
  test -z "$(git status --short -- generated)"
  echo

  echo "Result: PASS"
} 2>&1 | tee "evidence_pack/logs/offline_ci/${RUN_ID}_terraform_local_checks.log"
```

## Git ignore notes

Terraform working data should not be committed: `.terraform/`, `terraform.tfstate`, and `terraform.tfstate.backup`.

The generated artifacts under `generated/` are intentionally committed after review.

The `evidence_pack/` directory is used for local and CI evidence logs and is committed.

The Terraform lock file `.terraform.lock.hcl` is normally safe and useful to commit because it records provider dependency selections.

## GitHub Actions CI

The workflow file is expected at `.github/workflows/terraform-artifact-generator-ci.yml`.

The CI workflow is offline. It does not connect to network devices.

It runs:

```text
terraform fmt -check
terraform init -input=false
terraform validate
terraform plan -input=false -no-color
terraform apply -auto-approve -input=false -no-color
generated artifact sync check
```

The CI applies Terraform only inside the temporary GitHub Actions workspace. It does not modify the repository on GitHub and it does not affect the local workstation.

After `terraform apply`, CI checks that regenerated artifacts match the committed `generated/` files:

```bash
git diff --exit-code -- generated
test -z "$(git status --short -- generated)"
```

This catches cases where templates or input data changed but the generated artifacts were not updated and committed.

## Useful Terraform commands

Format Terraform files:

```bash
terraform fmt
```

Check formatting without modifying files:

```bash
terraform fmt -check
```

Initialize the project and download providers:

```bash
terraform init
```

Validate Terraform configuration:

```bash
terraform validate
```

Preview planned local file changes:

```bash
terraform plan -input=false -no-color
```

Generate artifacts:

```bash
terraform apply -auto-approve -input=false -no-color
```

Show outputs:

```bash
terraform output
```

## Future refactor ideas

Possible follow-up work:

- move artifact rendering into a small local Terraform module
- add `envs/` if multiple lab environments become necessary
- add stronger template validation
- add a small README index linking generated artifacts to the related Ansible, RESTCONF, and NetBox workflows
