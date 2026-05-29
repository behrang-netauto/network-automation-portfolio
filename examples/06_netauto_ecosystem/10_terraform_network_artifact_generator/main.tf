resource "local_file" "ansible_inventory" {
  filename = local.artifact_paths.ansible_inventory

  content = templatefile("${path.module}/templates/ansible_inventory.yml.tftpl", {
    inventory_devices  = local.inventory_devices
    execution_contexts = local.execution_contexts
  })
}

resource "local_file" "restconf_config" {
  filename = local.artifact_paths.restconf_config

  content = templatefile("${path.module}/templates/restconf_config.yml.tftpl", {
    site_name        = var.site_name
    restconf_devices = local.restconf_devices
  })
}

resource "local_file" "netbox_seed" {
  filename = local.artifact_paths.netbox_seed

  content = templatefile("${path.module}/templates/netbox_seed.yml.tftpl", {
    site_name      = var.site_name
    netbox_devices = local.netbox_devices
  })
}

resource "local_file" "device_matrix" {
  filename = local.artifact_paths.device_matrix

  content = templatefile("${path.module}/templates/device_matrix.md.tftpl", {
    site_name                  = var.site_name
    inventory_devices          = local.inventory_devices
    execution_contexts         = local.execution_contexts
    restconf_supported_devices = local.restconf_supported_devices
    restconf_devices           = local.restconf_devices
    netconf_supported_devices  = local.netconf_supported_devices
    netconf_devices            = local.netconf_devices
  })
}
