locals {
  device_names = sort(keys(var.devices))

  devices_by_name = {
    for name in local.device_names :
    name => var.devices[name]
  }

  inventory_devices = local.devices_by_name
  netbox_devices    = local.devices_by_name

  execution_contexts = sort(distinct([
    for _, device in local.devices_by_name :
    device.execution_context
  ]))

  restconf_supported_devices = {
    for name, device in local.devices_by_name :
    name => device
    if device.restconf.supported
  }

  restconf_devices = {
    for name, device in local.devices_by_name :
    name => device
    if device.restconf.enabled
  }

  netconf_supported_devices = {
    for name, device in local.devices_by_name :
    name => device
    if device.netconf.supported
  }

  netconf_devices = {
    for name, device in local.devices_by_name :
    name => device
    if device.netconf.enabled
  }

  artifact_paths = {
    ansible_inventory = "${path.module}/generated/ansible/inventory.generated.yml"
    restconf_config   = "${path.module}/generated/restconf/config.generated.yml"
    netbox_seed       = "${path.module}/generated/netbox/netbox_seed.generated.yml"
    device_matrix     = "${path.module}/generated/reports/device_matrix.md"
  }
}
