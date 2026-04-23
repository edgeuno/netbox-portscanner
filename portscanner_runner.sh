#!/bin/bash

# Example:
#   ./portscanner_runner.sh EdgeUno
#   ./portscanner_runner.sh TenantA TenantB

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <tenant> [<tenant> ...]" >&2
    exit 1
fi

exec /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py portscanner "$@"
