# GitHub Command Site

A central, static, multi-repository command center for GitHub projects.

The hub repository owns the **website code, snapshot contract, aggregate data model, sync logic, validation, and GitHub Pages deployment**. Connected repositories remain independent sources of truth and publish small bounded metadata snapshots that the hub can ingest.

**Live command center:** https://kaibuzz0.github.io/Git-hub-command-site/

## Architecture

```text
Connected repo A ─┐
Connected repo B ─┼─> public repo snapshot ─> sync/validate ─> aggregate hub.json ─> static VS Code-style UI
Connected repo C ─┘
```

A connected repository can publish `.command-site/repo-snapshot.json`, a Pages-hosted `data/repo-snapshot.json`, or another approved GitHub-hosted snapshot endpoint. The hub registry lives at `data/repositories.json`.

The UI is generic. New repositories and normal additions to tools, toolsets, cases, opportunities, intelligence, sources, prompts, evidence, Agent Ops, and activity should appear from snapshot data without bespoke HTML edits.

## First connected repository

`kaibuzz0/cipher-solving-suite` is the first production spoke. Its normal Pages build generates a bounded snapshot from canonical repository state, and this hub successfully fetches it from:

`https://kaibuzz0.github.io/cipher-solving-suite/data/repo-snapshot.json`

The first verified aggregate contained 11 tools, 1 toolset, 1 case, 21 opportunities, 6 intelligence records, 16 sources, 5 prompts, and 40 evidence records.

## Add another repository

Generate a reusable onboarding kit:

```bash
python scripts/onboard_repository.py \
  --repo-id my-repo \
  --full-name OWNER/REPOSITORY \
  --snapshot-url https://OWNER.github.io/REPOSITORY/data/repo-snapshot.json
```

The generated kit contains the portable exporter, connector configuration, hub registry entry, and setup instructions. An authorized AI can adapt that exporter to the target repository's existing canonical data instead of inventing another database.

Then:

1. Read `docs/CONNECTED_REPOSITORY_PROTOCOL.md` and `docs/ARCHITECTURE_BLUEPRINT.md`.
2. Copy/adapt the generated exporter in the connected repository.
3. Publish a schema-v1 snapshot from canonical repository data.
4. Add the generated registry entry to `data/repositories.json`.
5. Run remote-registry and snapshot validation.
6. Merge normally. The hub refresh workflow fetches registered snapshots and regenerates the static site.

Each registry entry can set `stale_after_hours`; the default is seven days. Aggregate health tracks stale repository snapshots instead of silently treating old data as current.

The hub also supports checked-in `data/repos/<repo-id>.json` last-known-good snapshots when a remote source is temporarily unavailable.

## Development

```bash
python -m pytest tests/ -vv --tb=short
python scripts/sync_repositories.py --validate
python scripts/build_hub.py --validate
python scripts/build_hub.py
```

See `AGENTS.md` before making structural changes.
