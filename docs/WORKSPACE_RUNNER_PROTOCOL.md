# Workspace Runner Protocol

## Purpose

GitHub Pages is a static, untrusted browser surface. It can edit local scratch text, generate plans, display commands, and visualize results, but it must not pretend to execute local Python, mutate GitHub repositories, or access credentials.

Commands that require execution use a trusted runner boundary: a local CLI, GitHub Actions workflow, or explicitly authorized AI/agent with repository permissions.

## Request envelope

A runner request is bounded JSON:

```json
{
  "schema_version": 1,
  "request_id": "run-unique-id",
  "repo_id": "example-repo",
  "operation": "python-debug",
  "working_directory": ".",
  "command": ["python", "-m", "pdb", "script.py"],
  "timeout_seconds": 120,
  "artifacts": []
}
```

Supported operation classes are intentionally explicit: `validate`, `test`, `build`, `python-run`, `python-debug`, and `repo-connect`.

## Result envelope

```json
{
  "schema_version": 1,
  "request_id": "run-unique-id",
  "status": "success",
  "exit_code": 0,
  "started_at": "2026-08-16T00:00:00Z",
  "finished_at": "2026-08-16T00:00:01Z",
  "stdout": "bounded text",
  "stderr": "",
  "artifacts": []
}
```

Results must remain bounded. Do not return secrets, environment dumps, credentials, tokens, private keys, wallet seeds, or uncontrolled repository/file contents.

## Python debugging

The workbench may prepare launch specifications for `pdb`, pytest, compile checks, or another explicitly configured Python debugger. Execution occurs only in a trusted runner with user/repository authorization. The browser UI labels this distinction clearly.

## Repository writes

A repository-connect request may generate a connector kit and hub registry change. Modifying the target repository still requires that target repository's own authorization and governance. A hub registry entry never grants authority over a connected repository.

## Security invariants

- No browser-side credential storage.
- No arbitrary shell execution from snapshot data.
- No command is executed merely because a remote snapshot contains it.
- Runner command allowlists and repository permissions are enforced outside the static site.
- Remote snapshot URLs remain bounded to approved transports.
- Results are treated as data and rendered escaped by the UI.
