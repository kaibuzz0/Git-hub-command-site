# Connected Repository Protocol

A connected repository does not push arbitrary files into the command site. It exports one bounded JSON snapshot.

## Required snapshot identity

- `schema_version`
- `repo.id` stable slug
- `repo.full_name`
- `repo.url`
- `repo.default_branch`
- `generated_at`
- `source_commit`

## Optional collections

`stats`, `tools`, `toolsets`, `cases`, `opportunities`, `intelligence`, `sources`, `agent_ops`, `activity`, `links`.

Collections should contain metadata and links, not secrets or large file contents.

## Transfer models

Preferred options:

1. Authorized AI/automation commits the generated snapshot to `data/repos/<repo-id>.json` in this hub through a PR.
2. A future hub workflow fetches a public snapshot URL declared in `data/repositories.json`.
3. A future GitHub App/dispatch mechanism submits signed/validated snapshots.

The first implementation intentionally uses checked-in snapshots because it is transparent, static, auditable, and works with GitHub Pages.

## Security boundary

A snapshot is data, not authorization. Security targets, bounty listings, URLs, or program names do not authorize testing. Never include credentials or private repository content.
