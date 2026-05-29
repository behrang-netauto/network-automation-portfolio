site_name = "lab-primary"

devices = {
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

  csr1000v_2 = {
    mgmt_ip           = "192.168.2.64"
    platform          = "iosxe"
    device_model      = "csr1000v"
    role              = "router"
    execution_context = "ios"

    restconf = {
      supported = true
      enabled   = false
      port      = 443
    }

    netconf = {
      supported = true
      enabled   = false
      port      = 830
    }
  }

  csr1000v_3 = {
    mgmt_ip           = "192.168.2.65"
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

  csr1000v_4 = {
    mgmt_ip           = "192.168.2.66"
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

  csr1000v_5 = {
    mgmt_ip           = "192.168.2.67"
    platform          = "iosxe"
    device_model      = "csr1000v"
    role              = "router"
    execution_context = "iosxe_netconf"

    restconf = {
      supported = true
      enabled   = false
      port      = 443
    }

    netconf = {
      supported = true
      enabled   = true
      port      = 830
    }
  }

  nxos1 = {
    mgmt_ip           = "192.168.2.68"
    platform          = "nxos"
    device_model      = "nxosv"
    role              = "switch"
    execution_context = "nxos"

    restconf = {
      supported = true
      enabled   = false
      port      = 443
    }

    netconf = {
      supported = false
      enabled   = false
      port      = 830
    }
  }

  iol_r1 = {
    mgmt_ip           = "192.168.2.69"
    platform          = "ios"
    device_model      = "iol"
    role              = "router"
    execution_context = "ios"

    restconf = {
      supported = false
      enabled   = false
      port      = 443
    }

    netconf = {
      supported = false
      enabled   = false
      port      = 830
    }
  }
}
