# Contributing

## Scope

This repository now supports a scanner-first NetBox plugin. Contributions should target the supported runtime path only:

- `portscanner_runner.sh`
- `manage.py portscanner <tenant>`
- `netbox_portscanner.scanner.vm_port_scanner_queue.VMPortScannerQueue`

Do not reintroduce legacy Proxbox sync code, retired plugin models, or compatibility shims unless there is an explicit maintenance decision to do so.

## Reporting Bugs

When reporting a bug, include:

- the NetBox version and Python version
- the exact command or workflow used
- expected behavior and observed behavior
- relevant traceback or log output
- whether the issue affects runtime scanning, UI rendering, or upgrade/cleanup work

## Feature Requests

Keep feature requests narrow and tied to the scanner-first architecture. If a proposal would require bringing back legacy Proxbox synchronization behavior, call that out explicitly as a scope change.

## Pull Requests

Before opening a pull request:

- make sure the change has a clear runtime or maintenance purpose
- run at least `python -m compileall netbox_portscanner`
- note any operational follow-up, especially if administrators must clean up old NetBox data manually

Pull requests should include:

- a concise summary of the change
- validation steps run
- screenshots for UI changes
- upgrade notes if commands, templates, or config expectations changed

## Review Expectations

Prefer small, isolated changes. Cleanup work should keep the tracker in `work_plan/PROXBOX_CLEANUP_TRACKER.md` current so the repository state and the work plan do not drift apart.
