variable "site_name" {
  type        = string
  description = "Logical lab site name used in generated automation artifacts."

  validation {
    condition     = length(trimspace(var.site_name)) > 0
    error_message = "site_name must not be empty."
  }
}

variable "devices" {
  description = "Structured lab device model used to generate network automation artifacts."

  type = map(object({
    mgmt_ip           = string
    platform          = string
    device_model      = string
    role              = string
    execution_context = string

    restconf = object({
      supported = bool
      enabled   = bool
      port      = number
    })

    netconf = object({
      supported = bool
      enabled   = bool
      port      = number
    })
  }))

  validation {
    condition     = length(var.devices) > 0
    error_message = "devices must contain at least one device."
  }

  validation {
    condition = alltrue([
      for device_name, _ in var.devices :
      length(trimspace(device_name)) > 0
    ])
    error_message = "device names must not be empty."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      can(regex("^([0-9]{1,3}\\.){3}[0-9]{1,3}$", device.mgmt_ip))
      && can(cidrhost("${device.mgmt_ip}/32", 0))
    ])
    error_message = "each device mgmt_ip must be a valid IPv4 address."
  }

  validation {
    condition = length(distinct([
      for _, device in var.devices :
      device.mgmt_ip
    ])) == length(var.devices)
    error_message = "device mgmt_ip values must be unique."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      contains(["ios", "iosxe", "nxos"], device.platform)
    ])
    error_message = "each device platform must be one of: ios, iosxe, nxos."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      length(trimspace(device.device_model)) > 0
    ])
    error_message = "each device device_model must not be empty."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      contains(["router", "switch"], device.role)
    ])
    error_message = "each device role must be one of: router, switch."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      contains(["ios", "nxos", "iosxe_netconf"], device.execution_context)
    ])
    error_message = "each device execution_context must be one of: ios, nxos, iosxe_netconf."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      (
        device.execution_context == "ios"
        && contains(["ios", "iosxe"], device.platform)
        ) || (
        device.execution_context == "nxos"
        && device.platform == "nxos"
        ) || (
        device.execution_context == "iosxe_netconf"
        && device.platform == "iosxe"
        && device.netconf.supported
        && device.netconf.enabled
      )
    ])
    error_message = "execution_context must match platform and protocol capability."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      device.restconf.enabled ? device.restconf.supported : true
    ])
    error_message = "restconf.enabled cannot be true when restconf.supported is false."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      device.netconf.enabled ? device.netconf.supported : true
    ])
    error_message = "netconf.enabled cannot be true when netconf.supported is false."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      device.restconf.port >= 1 && device.restconf.port <= 65535
    ])
    error_message = "each device restconf.port must be between 1 and 65535."
  }

  validation {
    condition = alltrue([
      for _, device in var.devices :
      device.netconf.port >= 1 && device.netconf.port <= 65535
    ])
    error_message = "each device netconf.port must be between 1 and 65535."
  }
}
