Port Scanner
============

This repository contains a NetBox plugin focused on one supported workflow: scan NetBox virtual machines for open ports and sync detected services back into NetBox.

## Supported Runtime

The active execution path is:

```text
portscanner_runner.sh
  -> /opt/netbox/venv/bin/python <manage.py> portscanner <tenant>
  -> netbox_portscanner.management.commands.portscanner
  -> netbox_portscanner.scanner.vm_port_scanner_queue.VMPortScannerQueue
```

Legacy Proxbox synchronization code and plugin models have been removed from the runtime. If you are upgrading an older deployment, handle database retirement and migration work separately.

## Execution Paths

These are the supported ways to execute the plugin today:

1. Local wrapper script

```bash
./portscanner_runner.sh EdgeUno
./portscanner_runner.sh EdgeUno TenantA TenantB
```

2. Direct Django management command inside a prepared NetBox runtime

```bash
/opt/netbox/venv/bin/python <manage.py> portscanner EdgeUno
```

3. Scheduler-driven Docker runner

```bash
docker compose -f docker-compose.yaml up --build
```

This path keeps the container alive and executes according to `runtime/scanner.env`.

4. One-shot Docker execution

```bash
docker compose -f docker-compose-single-exec.yml run --rm scanner-single-exec
```

This path is for manual runs and diagnostics.

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

## Docker Files

- `.env`: build/runtime selection, mainly `NETBOX_VERSION` and `TZ`
- `runtime/configuration.py`: the real NetBox configuration file used by Django
- `runtime/scanner.env`: scheduler-only inputs such as mode, tenants, interval, and cron expression
- [docker-compose.yaml](/Users/javier/projects/netbox-portscanner/docker-compose.yaml): scheduler-driven runner
- [docker-compose-single-exec.yml](/Users/javier/projects/netbox-portscanner/docker-compose-single-exec.yml): one-off/manual execution path

`NETBOX_VERSION` in `.env` must be an exact `X.Y.Z` value, because the Dockerfile downloads `vX.Y.Z` from the NetBox GitHub release archive.

## Configuration

The Docker runtime mounts the NetBox configuration file at:

```text
/opt/netbox/netbox/netbox/netbox/configuration.py
```

Use [runtime/configuration.py.example](/Users/javier/projects/netbox-portscanner/runtime/configuration.py.example) as the starting point for the mounted file. That file must contain the NetBox database settings, Redis settings, `SECRET_KEY`, and:

```python
PLUGINS = ["netbox_portscanner"]
```

Scheduler inputs remain separate in `runtime/scanner.env`:

```bash
SCANNER_MODE=off|continuous|interval|cron
SCANNER_TENANTS=EdgeUno
SCANNER_INTERVAL_SECONDS=900
SCANNER_CRON_EXPRESSION=*/15 * * * *
SCANNER_RESTART_DELAY_SECONDS=0
```

The scheduler reads database and Redis connection settings from `runtime/configuration.py`, not from Compose environment variables.

## Run

Run the scanner for one or more tenants:

```bash
./portscanner_runner.sh EdgeUno
```

`portscanner_runner.sh` is the preferred entrypoint because it resolves the correct `manage.py` path for the current NetBox layout.

Example with multiple tenants:

```bash
./portscanner_runner.sh EdgeUno TenantA TenantB
```

If you are already inside a prepared NetBox environment, you can also call the management command directly:

```bash
/opt/netbox/venv/bin/python <manage.py> portscanner EdgeUno
```

## Docker Scheduled Runner

Use the scheduler-driven stack when you want the container to keep running:

```bash
docker compose -f docker-compose.yaml up --build
```

Behavior is controlled by `runtime/scanner.env`:

- `off`: start the scheduler and stay idle
- `continuous`: rerun immediately after the previous execution finishes, with optional delay
- `interval`: sleep `SCANNER_INTERVAL_SECONDS` between runs
- `cron`: use `SCANNER_CRON_EXPRESSION`

## Docker Setup

Typical first-time setup:

```bash
cp .env.example .env
cp runtime/configuration.py.example runtime/configuration.py
cp runtime/scanner.env.example runtime/scanner.env
```

Then edit:

1. `.env` for `NETBOX_VERSION` and timezone
2. `runtime/configuration.py` for database, Redis, `SECRET_KEY`, and `PLUGINS`
3. `runtime/scanner.env` for scheduler mode and tenants

## Docker Single Execution

For a one-shot container execution without the scheduler loop, use [docker-compose-single-exec.yml](/Users/javier/projects/netbox-portscanner/docker-compose-single-exec.yml):

```bash
docker compose -f docker-compose-single-exec.yml run --rm scanner-single-exec
```

This service mounts `runtime/configuration.py`, uses the same image build, and is intended for one-off command execution.

When you need multiple commands in this file, use shell form through `/bin/sh -lc '...'` so operators like `&&` work correctly. The current file is an example of that pattern and can be edited for diagnostics or a direct `manage.py portscanner` invocation.

## Validation

Before shipping changes, at minimum run:

```bash
python -m compileall netbox_portscanner
```

For Docker file validation, these are the quick checks:

```bash
docker compose -f docker-compose.yaml config
docker compose -f docker-compose-single-exec.yml config
```

## Contributing

Keep contributions scoped to the scanner-first plugin behavior. Before submitting changes, document the runtime impact, validation steps, and any operational follow-up required for NetBox administrators.
