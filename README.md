# GitHub Command Site

A central, static, multi-repository command center for GitHub projects.

## Architecture

Connected repositories export a small `repo-snapshot.json` document that conforms to `schemas/repo-snapshot.schema.json`. This hub stores accepted snapshots under `data/repos/`, validates and aggregates them with `scripts/build_hub.py`, and deploys the generated `site-data/` plus the reusable VS Code-style UI to GitHub Pages.

The UI is generic: new repositories, tools, toolsets, cases, opportunities, source-health records, agent activity, and repository metadata should appear from snapshot data without bespoke HTML edits.

## Add a repository

1. Copy `connectors/export_repo_snapshot.py` into the repository or adapt its JSON contract.
2. Produce `.command-site/repo-snapshot.json`.
3. Transfer the snapshot into this hub under `data/repos/<repo-id>.json` using an authorized automation/agent workflow.
4. Run `python scripts/build_hub.py --validate` and `python scripts/build_hub.py`.
5. Merge. Pages rebuilds automatically.

See `docs/CONNECTED_REPOSITORY_PROTOCOL.md` and `AGENTS.md` before editing.
