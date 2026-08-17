# Current State

Last reconciled: 2026-08-17 00:24 UTC
Default branch: `main`

## Verified foundation

- PRs #1–#7 established the multi-repository hub, remote snapshot transport, first production spoke, aggregate UI, onboarding kit, and freshness tracking.
- PR #9 merged Command Workbench v3: VS Code-inspired operator surfaces, Repository Manager, local scratch editor, workspace tools/settings, and the trusted-runner boundary.
- PR #10 merged the hardened fleet exporter and dedicated `command-site-data` publishing template.
- PR #11 registered the full 19-repository public fleet; production sync fetched and validated all 19 public snapshots successfully.
- PR #13 merged automatic repository Explorer support: bounded tracked-file/directory inventories, lazy per-repository snapshot loading, and touch/mobile scrolling fixes.
- The central GitHub Pages deployment is live at `https://kaibuzz0.github.io/Git-hub-command-site/`.
- Hub CI validates on Python 3.11, 3.12 and 3.13 with JavaScript syntax checks and diagnostic artifacts.

## Fleet connector rollout

The owner account currently exposes 25 repositories to this integration.

- `cipher-solving-suite` retains its richer repository-specific Pages snapshot exporter; PR #21 added the same bounded repository-tree metadata and its Pages deployment completed successfully.
- The other 24 repositories contain `.github/workflows/command-site-snapshot.yml` on their default branch.
- Fleet workflows now pin the Explorer-capable exporter from immutable hub commit `f01dbda76e0badfb162b0ecd14c30416ba6a8582`.
- Generated snapshots are published only to the dedicated `command-site-data` branch; source branches are not rewritten by recurring snapshot refreshes.
- Public snapshots use `raw.githubusercontent.com/<owner>/<repo>/command-site-data/repo-snapshot.json`.
- Private repositories use the same internal snapshot branch but remain intentionally excluded from the public hub registry until authenticated private-repository transport exists.
- The repository-tree contract is content-free metadata: tracked file paths, directory paths/counts, extensions, and bounded totals. Empty directories cannot appear because Git does not track them.
- Live proof on `tradingviewsigdup` shows the `BOT/` folder and its tracked Python files appearing automatically from the repository snapshot. Large repositories are bounded to 5,000 file entries and 2,500 directory entries while retaining total counts.

## Public registry

`data/repositories.json` contains all 19 public repositories, including the hub itself and the richer cipher spoke. Remote failures remain visible in sync health rather than silently replacing verified state.

Production proof before the Explorer rollout fetched and validated all 19 registered public repositories. A fresh post-rollout sync/deploy is triggered by this reconciliation merge to verify the Explorer-capable fleet together.

## User interface

- The workbench remains VS Code-inspired and repository-agnostic.
- Repository cards lazy-load `site-data/repo-<id>.json` only when opened, keeping the initial `hub.json` small.
- Repository Explorer renders folders/files from `repository_tree` and links files to the exact source commit on GitHub.
- Touch/mobile scrolling is explicitly enabled for the content pane, sidebar, repository Explorer, and bottom panel.
- Ordinary committed folder/file changes in a connected repository flow automatically through that repository's snapshot and become visible after the next hub refresh. No per-folder HTML edit is required.

## Execution and privacy boundary

The static Pages workbench remains non-privileged. It does not store GitHub credentials, execute arbitrary Python in the browser, expose private repository snapshots through public raw URLs, or copy connected repository source code into the hub.

The hub owns shared UI, validation, exporter logic, schemas, and orchestration. Connected repositories receive only the thin connector/publisher needed to expose bounded metadata. Repository writes/execution continue through GitHub Actions, an explicitly authorized AI, local CLI, or a future authenticated trusted runner. Connected repositories remain authoritative for their own state.

## Current priorities

1. Verify the post-rollout hub sync fetches all 19 public Explorer-capable snapshots and deploys successfully.
2. Improve file inspection from metadata-only links toward safe, lazy text preview without bloating snapshots.
3. Add repository-level classification/health summaries and richer project overview cards derived from snapshot metadata.
4. Add authenticated private-repository snapshot transport before registering the six private repositories.
5. Keep shared connector upgrades pinned to immutable hub commits and roll them out deliberately across the fleet.

## Next handoff

Verify the hub Pages run triggered by this state reconciliation. Confirm all 19 public snapshots fetch and validate, confirm `cipher-solving-suite` now includes `repository_tree`, and record any repository that exceeds practical snapshot/browser limits. Do not expose private snapshot URLs publicly and do not move source code into the central hub merely to make it browsable.
