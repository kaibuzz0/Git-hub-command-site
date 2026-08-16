# GitHub Command Workbench

A central, static, multi-repository command center and operator workspace for GitHub projects.

The hub owns the **VS Code-inspired workbench UI, snapshot contract, repository registry, sync logic, workspace tool registry, aggregation, validation, and GitHub Pages deployment**. Connected repositories remain independent sources of truth and publish bounded metadata snapshots that the hub can ingest.

**Live workbench:** https://kaibuzz0.github.io/Git-hub-command-site/

## Architecture

```text
Connected repositories
        │
        ├─ canonical project state
        ▼
Bounded repository snapshots
        │
        ▼
Registry + sync + validation
        │
        ▼
Aggregate hub model
        │
        ├─ repository collections
        ├─ health / freshness
        ├─ workspace tools
        └─ workspace settings
        ▼
VS Code-inspired Command Workbench
```

The browser remains a static security boundary. It can search, inspect, edit browser-local scratch/config text, prepare repository connection plans, create trusted-runner request payloads, and open authorized GitHub/VS Code for Web sessions. It does **not** silently execute local Python, store GitHub credentials, or mutate repositories from remote snapshot data.

## Command Workbench surfaces

The UI now follows the Microsoft VS Code workbench model with an Activity Bar and dedicated surfaces for:

- Command Center / workspace health;
- Explorer / connected repositories;
- Search;
- Source Control links and repository state;
- Run and Debug;
- browser-local Workbench Editor;
- Workspace Tools;
- Settings;
- Command Palette (`Ctrl+K`);
- bottom Output panel.

The canonical hub-owned tool registry lives at `data/workspace-tools.json`. Workspace settings live at `data/workspace-settings.json`.

## Repository Manager

Plan a connection without modifying anything:

```bash
python scripts/connect_repository.py \
  --repo-id my-repo \
  --full-name OWNER/REPOSITORY \
  --snapshot-url https://OWNER.github.io/REPOSITORY/data/repo-snapshot.json
```

Apply the hub-side integration explicitly:

```bash
python scripts/connect_repository.py \
  --repo-id my-repo \
  --full-name OWNER/REPOSITORY \
  --snapshot-url https://OWNER.github.io/REPOSITORY/data/repo-snapshot.json \
  --apply
```

`--apply` generates the portable connector kit and adds the validated hub registry entry. The target repository still must be modified through its own authorized workflow. The generated integration plan makes those remaining steps explicit.

For a new repository, add `--mode new`; for an existing repository, the default mode is `existing`.

## Trusted runner and Python debugging

GitHub Pages cannot safely run a local Python debugger. Instead the Run and Debug surface prepares bounded requests following `docs/WORKSPACE_RUNNER_PROTOCOL.md`. An authorized local runner, GitHub Actions workflow, or repository-authorized AI can execute operations such as:

- Python `pdb` debugging;
- pytest;
- compile checks;
- builds and validation;
- repository connection operations.

The runner returns a bounded structured result which the workbench can display as data.

## Connected repository contract

A connected repository can publish `.command-site/repo-snapshot.json`, a Pages-hosted `data/repo-snapshot.json`, or another approved GitHub-hosted snapshot endpoint. The hub registry lives at `data/repositories.json`.

Snapshots can contain tools, toolsets, cases, opportunities, intelligence, sources, prompts, evidence metadata, Agent Ops, activity, links, stats, and repository identity. They must not contain credentials, secrets, private keys, wallet seeds, private user data, unbounded file bodies, or uncontrolled scan output.

`kaibuzz0/cipher-solving-suite` remains the first production spoke and proves the end-to-end snapshot flow.

## Development

```bash
python -m pytest tests/ -vv --tb=short
python -m py_compile scripts/*.py connectors/*.py
node --check site/app.js
python scripts/sync_repositories.py --validate
python scripts/build_hub.py --validate
python scripts/build_hub.py
```

Read `AGENTS.md`, `docs/ARCHITECTURE_BLUEPRINT.md`, and `docs/WORKSPACE_RUNNER_PROTOCOL.md` before structural changes.
