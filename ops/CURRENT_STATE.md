# Current State

Last reconciled: 2026-08-16 23:50 UTC
Default branch: `main`

## Verified foundation

- PRs #1–#7 established the multi-repository hub, remote snapshot transport, first production spoke, richer aggregate UI, reusable onboarding kit, and snapshot freshness tracking.
- `kaibuzz0/cipher-solving-suite` is the first production connected repository and its published snapshot has been fetched, validated, aggregated, and rendered by the live hub.
- The central GitHub Pages deployment is live at `https://kaibuzz0.github.io/Git-hub-command-site/`.
- Hub CI validates on Python 3.11, 3.12 and 3.13.

## Command Workbench v3 branch

Branch: `feature/command-workbench-v3`

This branch advances the hub from a repository dashboard into a VS Code-inspired operator workbench.

Implemented on the branch:

- Microsoft VS Code Dark+-inspired color/layout system;
- Activity Bar surfaces for Command Center, Explorer, Search, Source Control, Run and Debug, Editor, Workspace Tools, and Settings;
- bottom Output panel and expanded command palette;
- canonical `data/workspace-tools.json` operator-tool registry;
- canonical `data/workspace-settings.json` workbench settings;
- `scripts/connect_repository.py` orchestration for plan/apply repository onboarding;
- Repository Manager UI that builds connection commands and integration plans;
- browser-local text/config editor with localStorage autosave and no implicit repository writes;
- VS Code for Web deep links for connected repositories;
- Python debug adapter launch-spec surface;
- trusted runner boundary documented in `docs/WORKSPACE_RUNNER_PROTOCOL.md`;
- aggregate `workspace_tools` and `workspace_settings` in `site-data/hub.json`;
- CI compile checks plus `node --check site/app.js`;
- regression coverage for workspace tools, settings, connection planning, duplicate detection, and runner safety boundary.

## Execution boundary

The static Pages workbench remains non-privileged. It does not store credentials, execute arbitrary Python, or mutate repositories based on remote snapshot content.

Operations requiring writes or execution flow through a trusted runner, GitHub Actions, local CLI, or explicitly authorized AI. Target repository changes remain governed by the target repository itself.

## Current priorities

1. Validate Command Workbench v3 across Python 3.11/3.12/3.13 and JavaScript syntax.
2. Merge the workbench branch only after CI is green.
3. Verify post-merge Pages deployment and live rendering.
4. Next: add authenticated runner transport / repository-dispatch integration without weakening the static-site security boundary.
5. Next: add richer file metadata browsing and editor handoff into an authorized write workflow.

## Next handoff

Open and validate the Command Workbench v3 PR. Confirm the workspace tool registry appears in aggregate data, the Repository Manager remains plan-first unless `--apply` is explicit, browser code execution stays disabled, and the live Pages site still fetches the production cipher snapshot after merge.
