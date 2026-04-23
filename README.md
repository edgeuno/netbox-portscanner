Port Scanner
============

This repository contains a NetBox plugin focused on one supported workflow: scan NetBox virtual machines for open ports and sync detected services back into NetBox.

## Supported Runtime

The active execution path is:

```text
portscanner_runner.sh
  -> /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py portscanner <tenant>
  -> netbox_portscanner.management.commands.portscanner
  -> netbox_portscanner.scanner.vm_port_scanner_queue.VMPortScannerQueue
```

Legacy Proxbox synchronization code and plugin models have been removed from the runtime. If you are upgrading an older deployment, handle database retirement and migration work separately.

## Install

Clone the repository into your NetBox plugins directory and install it in the NetBox virtual environment:

```bash
cd /opt/netbox/plugins
git clone <your-repo-url> netbox-portscanner
cd netbox-portscanner
/opt/netbox/venv/bin/python setup.py develop
```

Enable the plugin in NetBox:

```python
PLUGINS = ["netbox_portscanner"]
```

## Configuration

No plugin-specific configuration file is required by the current scanner runtime.

## Run

Run the scanner for one or more tenants:

```bash
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py portscanner EdgeUno
```

`portscanner_runner.sh` is the repository wrapper for the same command and is the preferred cron entrypoint.

## Validation

Before shipping changes, at minimum run:

```bash
python -m compileall netbox_portscanner
```

## Upgrade Notes

This repository no longer ships the legacy Proxbox synchronization stack. The following entrypoints and surfaces were intentionally removed without compatibility shims:

- legacy command aliases such as `proxboxportscanner`
- legacy Proxbox sync code and model-backed registry pages
- legacy Proxmox VM CRUD/API routes and full-update UI flows
- unsupported alternate scanner backends

If any external automation still calls removed commands, URLs, or API routes, update it to use the supported path:

```bash
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py portscanner <tenant>
```

## Legacy Data Retirement

This cleanup is code-first. The repository does **not** automatically delete legacy NetBox data created by older Proxbox sync behavior.

If you are upgrading an older deployment, review and retire these artifacts manually as needed:

- custom fields such as `proxmox_id`, `proxmox_node`, `proxmox_type`, and `proxmox_keep_interface`
- tags or auxiliary objects created only for the old sync workflow
- `local_context_data["proxmox"]` payloads on virtual machines
- database tables for removed plugin models after you add the retirement migrations

Keep this manual cleanup separate from the scanner runtime rollout so you can verify impact before deleting historical data.

## Contributing

Keep contributions scoped to the scanner-first plugin behavior. Before submitting changes, document the runtime impact, validation steps, and any operational follow-up required for NetBox administrators.
