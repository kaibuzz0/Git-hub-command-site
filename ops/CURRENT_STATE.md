# Current State

Last reconciled: 2026-08-16 23:59 UTC
Default branch: `main`

## Verified foundation

- PRs #1–#7 established the multi-repository hub, remote snapshot transport, first production spoke, aggregate UI, onboarding kit, and freshness tracking.
- PR #9 merged Command Workbench v3: VS Code-inspired operator surfaces, Repository Manager, local scratch editor, workspace tools/settings, and the trusted-runner boundary.
- PR #10 merged the hardened fleet exporter and dedicated `command-site-data` publishing template.
- The central GitHub Pages deployment is live at `https://kaibuzz0.github.io/Git-hub-command-site/`.
- Hub CI validates on Python 3.11, 3.12 and 3.13 with JavaScript syntax checks and diagnostic artifacts.

## Fleet connector rollout

The owner account currently exposes 25 repositories to this integration.

- `cipher-solving-suite` retains its richer repository-specific Pages snapshot exporter.
- The other 24 repositories now contain `.github/workflows/command-site-snapshot.yml` on their default branch.
- Fleet workflows fetch the exporter from immutable hub commit `131fb04af009bddaaf173711b6e31c3f651210b4` and run it inside the source repository.
- Generated snapshots are published only to the dedicated `command-site-data` branch; source branches are not rewritten by recurring snapshot refreshes.
- Public snapshots use `raw.githubusercontent.com/<owner>/<repo>/command-site-data/repo-snapshot.json`.
- Private repositories use the same internal snapshot branch but are intentionally excluded from the public hub registry until authenticated private-repository transport exists.
- Live proof succeeded for `tradingviewsigdup` and `vscode`, including the large VS Code repository, demonstrating bounded generic metadata export and dedicated-branch publication.

## Public registry

`data/repositories.json` on the fleet-registration branch contains all 19 public repositories, including the hub itself and the existing cipher spoke. Remote failures remain visible in sync health rather than failing closed into stale/invalid data.

## Execution and privacy boundary

The static Pages workbench remains non-privileged. It does not store GitHub credentials, execute arbitrary Python in the browser, or expose private repository snapshots through public raw URLs.

Repository writes/execution continue through GitHub Actions, an explicitly authorized AI, local CLI, or a future authenticated trusted runner. Connected repositories remain authoritative for their own state.

## Current priorities

1. Validate and merge the 19-repository public registry update.
2. Let the hub sync all public `command-site-data` snapshots and surface any failed publishers as sync errors.
3. Verify the Pages deployment renders the expanded fleet.
4. Add authenticated private-repository snapshot transport before registering the six private repositories.
5. Build richer per-repository adapters only where generic metadata is insufficient; do not fork the frontend per repo.

## Next handoff

Run the hub sync after the public registry merges, record which public repos fetched successfully, keep failed publishers visible, and do not add private snapshot URLs to the public registry. The fleet workflow should remain pinned to an immutable exporter commit until a deliberate connector upgrade is rolled out.
