# Netbox plugin related import
try:
    from extras.plugins import PluginConfig
except Exception:
    from netbox.plugins import PluginConfig


class PortscannerConfig(PluginConfig):
    name = "netbox_portscanner"
    verbose_name = "Port Scanner"
    description = "Scans NetBox virtual machines and syncs detected services"
    version = "0.0.5"
    author = "Emerson Felipe (@emersonfelipesp)"
    author_email = "emerson.felipe@nmultifibra.com.br"
    base_url = "portscanner"
    required_settings = []
    default_settings = {
        'proxmox': {
            'filePath': '/opt/netbox/plugins/netbox-portscanner/configuration_options.json',
            'domain': 'proxmox.example.com',
            'http_port': 8006,
            'user': 'root@pam',
            'password': 'PROXMOX_PASSWORD',
            'token': {
                'name': 'TOKEN_NAME',
                'value': 'TOKEN_VALUE',
            },
            'token_name': 'TOKEN_NAME',
            'token_value': 'TOKEN_VALUE',
            'ssl': False
        },
        'netbox': {
            'domain': 'netbox.example.com',
            'http_port': 80,
            'token': 'NETBOX_API_TOKEN',
            'ssl': False,
            'settings': {
                'virtualmachine_role_id': 0,
                'node_role_id': 0,
                'site_id': 0
            },
            'manufacturer': 'Dell',
            'virtualmachine_role_id': 0,
            'virtualmachine_role_name': 'Port Scanner VM Role',
            'node_role_id': 0,
            'site_id': 0,
            'tenant_name': 'ExampleTenant',
            'tenant_regex_validator': '^tenant-',
            'tenant_description': 'Default tenant used by the scanner'
        }
    }


config = PortscannerConfig
