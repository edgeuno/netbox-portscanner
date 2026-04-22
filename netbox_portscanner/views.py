from django.shortcuts import render
from django.views import View

from netbox import configuration

from . import PortscannerConfig


class HomeView(View):
    """Homepage"""
    template_name = 'netbox_portscanner/home.html'

    # service incoming GET HTTP requests
    def get(self, request):
        """Get request."""

        plugin_configuration = configuration.PLUGINS_CONFIG.get("netbox_portscanner", {})
        default_config = PortscannerConfig.default_settings
        proxmox_settings = plugin_configuration.get("proxmox", {})
        netbox_settings = plugin_configuration.get("netbox", {})

        return render(
            request,
            self.template_name,
            {
                "default_proxmox_settings": default_config.get("proxmox", {}),
                "default_netbox_settings": default_config.get("netbox", {}),
                "proxmox_settings": proxmox_settings,
                "netbox_settings": netbox_settings,
                "has_proxmox_credentials": bool(
                    proxmox_settings.get("password")
                    or proxmox_settings.get("token_value")
                    or proxmox_settings.get("token", {}).get("value")
                ),
                "has_netbox_token": bool(netbox_settings.get("token")),
            }
        )
