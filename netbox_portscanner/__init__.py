# Netbox plugin related import
try:
    from extras.plugins import PluginConfig
except Exception:
    from netbox.plugins import PluginConfig


class PortscannerConfig(PluginConfig):
    name = "netbox_portscanner"
    verbose_name = "Port Scanner"
    description = "Scans NetBox virtual machines and syncs detected services"
    version = "0.1.0"
    author = "Javier Alejandro Ruiz G."
    author_email = "javier.ruiz@edgeuno.com"
    base_url = "portscanner"
    required_settings = []


config = PortscannerConfig
