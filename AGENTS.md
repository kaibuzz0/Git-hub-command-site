# Agent Operating Contract

This repository is the source-of-truth codebase for the GitHub Command Site.

Before editing, read `README.md`, `ops/CURRENT_STATE.md`, `docs/AGENT_HANDOFF.md`, `docs/WORK_QUEUE.md`, `docs/CONNECTED_REPOSITORY_PROTOCOL.md`, open PRs, recent commits, and relevant CI.

## Invariants

- The hub UI must remain repository-agnostic. Do not hardcode normal repositories into HTML/JS.
- Connected repository state enters through validated snapshots under `data/repos/`.
- Preserve stable repository IDs and snapshot provenance.
- Never copy secrets, private file contents, credentials, tokens, or unbounded repository data into snapshots.
- Treat contributed snapshots as untrusted input until validation succeeds.
- Keep changes bounded, reviewable, and reversible.
- Prefer extending schemas/builders/renderers over creating parallel data systems.
- Normal repo additions should not require editing `site/index.html`.
- Update handoff/current state when architecture or operating state materially changes.

## Connected repo workflow

export -> validate locally -> transfer snapshot -> hub validate -> aggregate -> CI -> Pages -> refresh browser.
