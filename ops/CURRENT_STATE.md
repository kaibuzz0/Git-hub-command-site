# Current State

Last reconciled: 2026-08-17 01:23 UTC
Default branch: `main`

## Verified platform

- PRs #1–#7 established the multi-repository hub, remote snapshot transport, first production spoke, aggregate UI, onboarding kit, and freshness tracking.
- PR #9 established Command Workbench v3 with VS Code-inspired operator surfaces, Repository Manager, scratch editor, workspace tools/settings, and the trusted-runner boundary.
- PR #10 hardened the fleet exporter and dedicated `command-site-data` publishing model.
- PR #11 registered the full 19-repository public fleet; production sync has repeatedly fetched and validated all 19 public snapshots successfully.
- PR #13 added bounded repository Explorer data, lazy per-repo snapshot loading, and touch/mobile scrolling fixes.
- PR #16 completed the internal code-preview layer: Monaco on supported desktop browsers, mobile/touch fallback, exact-commit public file loading, and pinned Monaco packaging in Pages.
- PR #17 added the reusable standalone repository-site generator.
- PR #19 made generated repository websites a first-class output of the central Pages deployment.
- PR #22 restored the Cipher Suite VS Code layout as the reusable visual baseline for generated repository workspaces.
- PR #24 added the dockable Workbench v4 shell: resizable sidebar/inspector/output panes, workspace tabs, update checks, and a browser-local whiteboard. Its production Pages run completed successfully.
- The central Command Center is live at `https://kaibuzz0.github.io/Git-hub-command-site/`.

## Fleet state

The owner account exposes 25 repositories to this integration: 19 public and 6 private.

- `cipher-solving-suite` retains its richer custom snapshot exporter and standalone project site while also participating in the central hub.
- The other connected repositories publish bounded snapshots through `.github/workflows/command-site-snapshot.yml` to `command-site-data`.
- Public snapshots are admitted through `data/repositories.json`; private repositories remain intentionally excluded from the public registry and public Pages output.
- Repository-tree metadata is content-free: tracked file paths, directory paths/counts, extensions, bounded totals, and source commit provenance. Empty directories cannot appear because Git does not track them.
- Large repositories are bounded to 5,000 individual file entries and 2,500 directory entries while retaining total counts.

## Generated repository websites

The canonical fleet website model no longer requires GitHub Pages to be enabled in each source repository.

The hub generates one mini-site for every validated public repository and deploys it under:

`https://kaibuzz0.github.io/Git-hub-command-site/repos/<repo-id>/`

A repository detail view exposes a `Repo Website` action pointing to that mini-site. `/repos/` also contains an automatically generated index of the public repository workspaces.

The mini-sites are derived from exactly the same `repo-snapshot.json` used by the central hub and update after normal source commits -> snapshot refresh -> hub sync/deploy. They use the Cipher Suite-style VS Code layout, repository Explorer, exact source-commit provenance, public text-file preview, and contextual structured-data sections when available.

## Workbench composition

Workbench v4 is the current verified production shell. It keeps the Command Center on the far-left Activity Bar, repository/data navigation in the left sidebar, the central editor/workspace, an optional right Inspector, and the bottom output panel. Sidebar, Inspector, and output-panel dimensions persist browser-locally. Workspace tabs, update checks, and the whiteboard also remain browser-local and do not mutate repositories.

Workbench v5 is the active bounded implementation branch. It adds split editor groups (right/down), a second dockable resource surface, README preview at the exact snapshot commit, browser-local unified-diff review, repository-site embedding, built-in Coding/Research/Repo Review/Focus layouts, custom saved layouts, and tab drag/reorder behavior. v5 remains additive to v4 and does not alter the remote snapshot or privilege boundary.

## Execution and privacy boundary

GitHub Pages remains static/non-privileged. It does not store GitHub credentials, execute arbitrary local Python, expose private repository snapshots publicly, or perform repository writes.

Public file/README previews are fetched from the public source repository at the snapshot's exact `source_commit` with bounded size limits. Unsupported/binary/oversized resources fall back to GitHub. Private repository browser support requires an authenticated private transport and non-public presentation surface before those repositories can be admitted.

## Current priorities

1. Validate and merge Workbench v5 split editor groups, saved layouts, README/reference preview, and scratch diff review.
2. Add richer document composition: Markdown/source side-by-side, search-result tabs, commit/PR/check review surfaces, and recently opened resources.
3. Add repository classification/language/health summaries and surface them in both the Command Center and individual mini-sites.
4. Build authenticated private-repository transport without leaking private paths/content into the public Pages artifact.
5. Continue developing the trusted-runner boundary for explicit execution/debug/write operations while keeping Pages non-privileged.

## Next handoff

Treat the Command Center as a single-page multi-repository operating workspace, not a collection of fixed dashboards. Extend shared editor groups/panels/layouts rather than creating one-off full-page UIs. Keep public repo content exact-commit and bounded, keep private repositories outside the public build, and route execution/writes through the trusted runner or authorized-agent boundary.
