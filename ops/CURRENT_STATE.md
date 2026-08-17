# Current State

Last reconciled: 2026-08-17 09:30 UTC
Default branch: `main`

## Verified platform

The repository is the source of truth for a static multi-repository GitHub Command Workbench. The public fleet remains 19 connected public repositories; six private repositories remain intentionally excluded from public Pages.

Major verified foundations include remote snapshot sync/validation, central aggregate data, generated per-repo sites, fleet connector publishing, Explorer/file inventories, Monaco/mobile exact-commit preview, dockable/split workbench composition, saved layouts, whiteboard, repo intelligence/diagnostics/triage, and generated repo project-console tooling.

## Command OS blueprint

PR #44 replaced the earlier active-context shim with the canonical `site/command_os.js` + `site/command_os.css` runtime. Post-merge test reconciliation landed through PR #45; the corrected `main` validation completed successfully.

The workbench now has two canonical modes:

### Global fleet mode

With no active repository, Home is a fleet operating view with connected repositories, truthful attention/staleness signals, browser-local open task counts, browser-local active agent slots, P1 queue, tools, recent aggregate activity, and direct project activation.

### Active Repository Context

Selecting a repository from Explorer or a repository card establishes the active project context and persists it browser-locally. The workbench then exposes:

- Overview / Mission Control
- Repository Intelligence
- Files
- Code
- GitHub links (Issues / PRs / Commits / Actions / Branches / Releases)
- Tests / CI
- Tasks
- Agents
- Research
- Notes
- Commands
- History

Repository file/code/test/script views lazy-load the bounded `site-data/repo-<id>.json` snapshot and use the exact exported source commit. Local project memory is namespaced per repo in browser localStorage.

## Visual system

The production architecture now treats the workbench as a jet-black developer/cyber workstation rather than generic VS Code charcoal. `site/command_os.css` establishes black/near-black surfaces with semantic cyan, blue, purple, pink, green, lime, yellow, orange, red and white tokens. Color conveys information; panel borders use thin restrained luminous accents and metadata uses syntax-like typography.

## Generated repository websites

Every validated public repository continues to receive a centrally generated mini-site under:

`https://kaibuzz0.github.io/Git-hub-command-site/repos/<repo-id>/`

Those workspaces share the same snapshot contract and remain public-only. Private repositories are not admitted to the public registry or Pages artifact.

## Execution and privacy boundary

GitHub Pages remains static/non-privileged. It does not store GitHub credentials, send browser Authorization/Bearer headers, execute arbitrary local Python, expose private repository snapshots publicly, or perform repository writes from remote snapshot data.

Tests, commands, task/agent assignments and debug operations prepare bounded handoff/runner specs. Actual execution/writes require a trusted runner, GitHub Actions, or an explicitly authorized agent.

## Validation state

The Command OS runtime is covered by `node --check`, blueprint/context security tests, and the existing Python 3.11/3.12/3.13 CI matrix. The corrected post-merge `main` run after PR #45 completed successfully, including tests, registry validation, snapshot validation, aggregate generation and repository mini-site generation.

## Current priorities

The blueprint itself is implemented. Future work should deepen the existing Command OS instead of creating a parallel dashboard system:

1. authenticated trusted-runner transport and result ingestion;
2. richer public PR/check/issue collectors without browser credentials;
3. stronger language/static-analysis intelligence and dependency graphs;
4. authenticated private-repository transport/presentation;
5. near-immediate repository refresh via GitHub App/repository dispatch;
6. promote/export browser-local project memory into explicit repository-backed records when authorized.

## Next handoff

Treat `command_os.js` as the canonical active-context/project-operating layer. New project capabilities should subscribe to the active repository and extend the existing surfaces/panel model. Preserve exact-commit bounded public content, static browser privilege boundaries, and public/private separation.
