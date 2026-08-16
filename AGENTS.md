# Agent Operating Contract

This repository is the source-of-truth codebase for the GitHub Command Site.

Before editing, read `README.md`, `docs/ARCHITECTURE_BLUEPRINT.md`, `ops/CURRENT_STATE.md`, `docs/AGENT_HANDOFF.md`, `docs/WORK_QUEUE.md`, `docs/CONNECTED_REPOSITORY_PROTOCOL.md`, open PRs, recent commits, and relevant CI.

## Invariants

- The hub UI must remain repository-agnostic. Do not hardcode normal repositories into HTML/JS.
- Connected repository state enters through validated bounded snapshots and the canonical registry in `data/repositories.json`.
- Preserve stable repository IDs, source commits, generated timestamps, transport provenance, and snapshot origin.
- Never copy secrets, private file contents, credentials, tokens, private keys, wallet seeds, or unbounded repository data into snapshots.
- Treat contributed/remote snapshots as untrusted input until validation succeeds.
- Remote fetches must remain bounded by HTTPS, approved public GitHub-hosted transports, size limits, and identity checks.
- A remote failure must be visible in sync health; it must not silently promote invalid data.
- Keep changes bounded, reviewable, and reversible.
- Prefer extending schemas/builders/renderers over creating parallel data systems.
- Normal repo additions should not require editing `site/index.html` or bespoke per-repo frontend branches.
- Connected repositories remain authoritative for their own state; the hub is a viewer/aggregator, not a replacement source of truth.
- Update handoff/current state when architecture or operating state materially changes.
- Public security/bounty metadata in a snapshot is information, not authorization to test any target.

## Connected repo workflow

canonical repo state -> generated bounded snapshot -> publish -> hub registry -> sync -> validate -> aggregate -> CI -> Pages -> refresh browser.

If a source repo already has canonical registries/site-data builders, its command-site exporter should derive from those rather than create a second manual database.
