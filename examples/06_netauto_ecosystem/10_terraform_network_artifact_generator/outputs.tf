output "generated_files" {
  description = "Generated artifact file paths."
  value = {
    ansible_inventory = local_file.ansible_inventory.filename
    restconf_config   = local_file.restconf_config.filename
    netbox_seed       = local_file.netbox_seed.filename
    device_matrix     = local_file.device_matrix.filename
  }
}

output "artifact_summary" {
  description = "Short summary of generated artifact inputs."
  value = {
    site_name                = var.site_name
    inventory_target_count   = length(local.inventory_devices)
    execution_contexts       = local.execution_contexts
    restconf_enabled_targets = keys(local.restconf_devices)
    netconf_enabled_targets  = keys(local.netconf_devices)
  }
}
