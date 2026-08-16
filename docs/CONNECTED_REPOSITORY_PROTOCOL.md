# Connected Repository Protocol

A connected repository exports one bounded JSON snapshot. The hub never needs a copy of the repository codebase.

## Fast path for a public repository

1. Add or adapt `connectors/export_repo_snapshot.py` in the connected repository.
2. Generate and commit `.command-site/repo-snapshot.json` in that repository.
3. Add one hub registry entry to `data/repositories.json`:

```json
{
  "id": "my-repo",
  "snapshot_url": "https://raw.githubusercontent.com/OWNER/REPO/main/.command-site/repo-snapshot.json",
  "enabled": true
}
```

4. The hub's scheduled/build workflow fetches the snapshot, validates `repo.id`, combines it with other repos, and republishes the static site.

A checked-in `data/repos/<id>.json` can serve as a transparent last-known-good fallback. A valid freshly fetched remote snapshot takes precedence for that build.

## Snapshot identity

Required: `schema_version`, `repo.id`, `repo.full_name`, `repo.url`, `repo.default_branch`, `generated_at`, `source_commit`.

Optional collections: `stats`, `tools`, `toolsets`, `cases`, `opportunities`, `intelligence`, `sources`, `agent_ops`, `activity`, `links`.

Collections contain metadata and links, never credentials, secrets, private file bodies, or unbounded repository content.

## Refresh behavior

The hub can rebuild on its own commits and on a schedule. This means a connected public repository can update its own committed snapshot without writing directly into the hub. A future GitHub App or repository-dispatch connector can make refresh effectively immediate without weakening this data contract.

## Security boundary

A snapshot is data, not authorization. Security targets, bounty listings, URLs, or program names do not authorize testing.
