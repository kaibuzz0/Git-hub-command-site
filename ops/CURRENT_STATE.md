# Current State

Last reconciled: 2026-08-17 01:02 UTC
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
- The central Command Center is live at `https://kaibuzz0.github.io/Git-hub-command-site/`.

## Fleet state

The owner account exposes 25 repositories to this integration: 19 public and 6 private.

- `cipher-solving-suite` retains its richer custom snapshot exporter and standalone project site while also participating in the central hub.
- The other connected repositories publish bounded snapshots through `.github/workflows/command-site-snapshot.yml` to `command-site-data`.
- Public snapshots are admitted through `data/repositories.json`; private repositories remain intentionally excluded from the public registry.
- Repository-tree metadata is content-free: tracked file paths, directory paths/counts, extensions, bounded totals, and source commit provenance. Empty directories cannot appear because Git does not track them.
- Large repositories are bounded to 5,000 individual file entries and 2,500 directory entries while retaining total counts.

## Generated repository websites

The canonical fleet website model no longer requires GitHub Pages to be enabled in each source repository.

The hub now generates one mini-site for every validated public repository and deploys it under:

`https://kaibuzz0.github.io/Git-hub-command-site/repos/<repo-id>/`

A repository detail view exposes a `Repo Website` action pointing to that mini-site. `/repos/` also contains an automatically generated index of the public repository workspaces.

The mini-sites are derived from exactly the same `repo-snapshot.json` used by the central hub and therefore update after normal source commits -> snapshot refresh -> hub sync/deploy. They include a VS Code-inspired Explorer, repository overview, exact source-commit provenance, public text-file preview, and GitHub/Actions/Issues links.

The production Pages run for PR #19 passed remote-registry validation, fetched snapshots, validated snapshots, built aggregate data, generated repository mini-sites, assembled the site, uploaded the Pages artifact, and deployed successfully.

## Pilot lesson

A dedicated per-repository Pages pilot was tested on `tradingviewsigdup`. The snapshot and mini-site build both succeeded, but `actions/configure-pages` failed because Pages had never been enabled for that repository. The pilot workflow was removed in `tradingviewsigdup` PR #2 after the central-hosted fleet design eliminated that requirement.

`connectors/command-site-pages.yml` remains available only as an optional dedicated-site template for repositories where an individual Pages URL is explicitly desired and does not conflict with an existing custom site.

## Execution and privacy boundary

GitHub Pages remains static/non-privileged. It does not store GitHub credentials, execute arbitrary local Python, expose private repository snapshots publicly, or perform repository writes.

Public file previews are fetched from the public source repository at the snapshot's exact `source_commit`. Unsupported/binary/oversized files fall back to GitHub. Private repository browser support requires an authenticated private transport and non-public presentation surface before those repositories can be admitted.

## Current priorities

1. Improve generated mini-site UI richness so tools, cases, opportunities, agent state, README/project summaries, and repo health can be shown contextually when present.
2. Add repository classification/language/health summaries and surface them in both the Command Center and individual mini-sites.
3. Build authenticated private-repository transport without leaking private paths/content into the public Pages artifact.
4. Continue developing the trusted-runner boundary for explicit execution/debug/write operations while keeping Pages non-privileged.
5. Keep connector/exporter upgrades pinned, bounded, and independently validated before fleet rotation.

## Next handoff

Treat centrally hosted `/repos/<repo-id>/` workspaces as the default public-repository website path. Do not install generic per-repository Pages workflows across the fleet unless an owner explicitly requests a dedicated URL and existing Pages usage has been checked first. The next UI pass should deepen each generated site using structured snapshot data rather than creating per-repo HTML forks.
