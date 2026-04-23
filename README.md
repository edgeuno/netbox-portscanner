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

Install the plugin in development mode inside the NetBox virtual environment:

```bash
cd /opt/netbox/plugins
git clone <your-repo-url> netbox-portscanner
cd netbox-portscanner
/opt/netbox/venv/bin/python setup.py develop
```

Then enable the plugin in the NetBox configuration:

```python
PLUGINS = ["netbox_portscanner"]
```

Development install summary:

1. Clone this repository under `/opt/netbox/plugins/netbox-portscanner`
2. Run `/opt/netbox/venv/bin/python setup.py develop`
3. Add `netbox_portscanner` to `PLUGINS`
4. Restart the NetBox services so the plugin is loaded

For Docker-based execution, the container follows the same plugin installation model internally: the image installs this repository into the NetBox virtual environment with `python setup.py develop`.

The current Docker build no longer depends on the `netboxcommunity/netbox` image. It starts from a Python base image, downloads the tagged NetBox source archive for `NETBOX_VERSION`, installs NetBox requirements into `/opt/netbox/venv`, and then installs this plugin in editable mode.

## Configuration

The Docker runtime expects a mounted NetBox configuration file at:

```text
/opt/netbox/netbox/netbox/configuration.py
```

Use [runtime/configuration.py.example](/Users/javier/projects/netbox-portscanner/runtime/configuration.py.example) as the starting point for the mounted file. That file must contain the NetBox database settings, Redis settings, `SECRET_KEY`, and:

```python
PLUGINS = ["netbox_portscanner"]
```

Scheduler inputs remain separate in `runtime/scanner.env`.

`NETBOX_VERSION` in `.env` must be an exact `X.Y.Z` value, because the Dockerfile downloads `vX.Y.Z` from the NetBox GitHub release archive.

## Run

Run the scanner for one or more tenants:

```bash
/opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py portscanner EdgeUno
./portscanner_runner.sh EdgeUno
```

`portscanner_runner.sh` is the repository wrapper for the same command and is the preferred cron entrypoint.

Example with multiple tenants:

```bash
./portscanner_runner.sh EdgeUno TenantA TenantB
```

## Docker Single Execution

For a one-shot container execution without the scheduler loop, use [docker-compose-single-exec.yml](/Users/javier/projects/netbox-portscanner/docker-compose-single-exec.yml):

```bash
docker compose -f docker-compose-single-exec.yml run --rm scanner-single-exec
```

This service mounts `runtime/configuration.py`, uses the same image build, and is intended for one-off command execution.

When you need multiple commands in this file, use shell form through `/bin/sh -lc '...'` so operators like `&&` work correctly. The current file demonstrates that pattern before running `manage.py portscanner EdgeUno`.

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
