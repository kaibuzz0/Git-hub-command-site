# GitHub Command Site

A central, static, multi-repository command center for GitHub projects.

The hub repository owns the **website code, snapshot contract, aggregate data model, sync logic, validation, and GitHub Pages deployment**. Connected repositories remain independent sources of truth and publish small bounded metadata snapshots that the hub can ingest.

## Architecture

```text
Connected repo A ─┐
Connected repo B ─┼─> public repo snapshot ─> sync/validate ─> aggregate hub.json ─> static VS Code-style UI
Connected repo C ─┘
```

A connected repository can publish `.command-site/repo-snapshot.json`, a Pages-hosted `data/repo-snapshot.json`, or another approved GitHub-hosted snapshot endpoint. The hub registry lives at `data/repositories.json`.

The UI is generic. New repositories and normal additions to tools, toolsets, cases, opportunities, intelligence, sources, prompts, evidence, Agent Ops, and activity should appear from snapshot data without bespoke HTML edits.

## First connected repository

`kaibuzz0/cipher-solving-suite` is the first production spoke. Its normal Pages build generates a bounded snapshot from canonical repository state, and this hub is registered to ingest it from:

`https://kaibuzz0.github.io/cipher-solving-suite/data/repo-snapshot.json`

This proves the main design: the source repository can keep evolving independently while the command center visualizes the latest published state.

## Add another repository

1. Read `docs/CONNECTED_REPOSITORY_PROTOCOL.md` and `docs/ARCHITECTURE_BLUEPRINT.md`.
2. Add/adapt `connectors/export_repo_snapshot.py` in the connected repository.
3. Publish a schema-v1 snapshot from canonical repository data.
4. Add one entry to `data/repositories.json`.
5. Run `python scripts/sync_repositories.py --validate` and `python scripts/build_hub.py --validate`.
6. Merge normally. The hub refresh workflow fetches registered snapshots and regenerates the static site.

The hub also supports checked-in `data/repos/<repo-id>.json` last-known-good snapshots when a remote source is temporarily unavailable.

## Development

```bash
python -m pytest tests/ -vv --tb=short
python scripts/sync_repositories.py --validate
python scripts/build_hub.py --validate
python scripts/build_hub.py
```

See `AGENTS.md` before making structural changes.
