# GitHub Command Workbench Architecture Blueprint

## Purpose

Build one browser-based operating environment for many GitHub projects. GitHub repositories remain the engineering/source-of-truth layer; GitHub Pages is the user-facing workspace.

The Command Workbench is not merely a repository dashboard. Its job is to help the operator **understand, operate, create, review, and remember** work across repositories while keeping privileged execution and writes behind explicit trusted-runner or authorized-agent boundaries.

## Core data model

```text
SOURCE REPOSITORIES
    │ canonical project state
    ▼
BOUNDED PUBLIC SNAPSHOTS
    │ approved GitHub-hosted HTTPS transport
    ▼
REGISTRY + SYNC + VALIDATION
    ▼
AGGREGATE HUB DATA
    ▼
COMMAND OS / STATIC WORKBENCH
```

Invalid remote data is surfaced as a sync error and never silently promoted. Private repositories remain outside the public registry and Pages artifact until an authenticated private transport exists.

## Command OS interaction model

The workbench has two primary modes.

### Global fleet mode

With no active repository, Home is the bird's-eye Command Center. It surfaces truthful aggregate/local signals such as connected repositories, stale/attention state, local open tasks, local active agent slots, P1 queue, tools, recent activity, and quick project selection.

### Active Repository Context

Selecting a repository from Explorer or a repository card establishes it as the single active project context. That context is remembered browser-locally and drives every project-aware surface until explicitly cleared.

```text
ACTIVE CONTEXT
    ├─ repository identity
    ├─ branch
    ├─ source commit
    ├─ bounded snapshot
    ├─ files / code
    ├─ tests / CI
    ├─ tasks
    ├─ agent slots
    ├─ research
    ├─ notes
    ├─ commands
    └─ history
```

Selecting a repository must change the whole workbench context; it must not merely filter the global Home page.

## Active-project surfaces

The canonical project navigation is:

1. **Overview / Mission Control** — repository identity, mission, phase, milestone, progress, project memory, and operate shortcuts.
2. **Repository Intelligence** — likely entry points, important docs, dependency manifests, structure, and transparent attention signals.
3. **Files** — bounded committed file inventory at the exact snapshot commit.
4. **Code** — source/script-focused inventory with internal exact-commit preview through the existing Monaco/mobile viewer layer.
5. **GitHub** — safe external links for Issues, Pull Requests, Commits, Actions, Branches, and Releases using the browser's normal GitHub session.
6. **Tests / CI** — detected tests/workflows plus bounded test/runner request generation.
7. **Tasks** — browser-local Backlog → Ready → In Progress → Verify → Done board with agent handoff generation.
8. **Agents** — browser-local Research/Builder/Tester/Reviewer control slots and explicit handoff specs; not claims of autonomous execution.
9. **Research** — browser-local Sources, Findings, Hypotheses, Experiments, References, Questions, Evidence, Rejected Ideas, and Results, with promotion into tasks.
10. **Notes** — persistent per-repository browser-local notebook with copy/export.
11. **Commands** — saved command presets plus script-derived command hints and trusted-runner/agent request generation.
12. **History** — chronological project memory combining exported repository activity with browser-local operator events.

Existing global Search, Source Control, Run/Debug, Monaco/editor, Workspace Tools, Settings, split-pane composition, whiteboard, Inspector, output panel, command palette, PWA/mobile shell, and generated per-repository websites remain part of the broader workbench.

## Visual language

The canonical theme is a restrained cyber/developer workstation rather than generic charcoal UI.

```text
MAIN BACKGROUND   #000000
EDITOR            #030303
SIDEBAR           #050505
CARDS             #080808
RAISED PANEL      #0D0D0D

CYAN               #00E5FF  information / files
BLUE               #2979FF  navigation
PURPLE             #B026FF  intelligence / agents
PINK               #FF2BD6  commands / special actions
GREEN              #39FF88  success / tests
LIME                #B6FF3B  numbers / metrics
YELLOW              #FFE600  warnings
ORANGE              #FF8A00  activity / strings
RED                 #FF3155  errors / attention
WHITE               #F4F7FF  primary text
```

Color is semantic. Borders use thin 1px luminous accents and restrained glow rather than large decorative effects. Metadata uses syntax-like typography: keys, strings, numbers, success state, and errors receive different semantic colors.

## Local project memory

Mission data, tasks, agent slots, research records, notes, command presets, active repository selection, layout preferences, and local history use browser localStorage. These are convenience/workspace records, not canonical repository state. They can be copied/exported or handed to an authorized agent, but they do not silently mutate GitHub.

## Exact-commit public content

Public repository snapshots carry `source_commit`. File and code previews use that exact commit and remain bounded. Normal repository additions should flow through the snapshot and appear automatically without bespoke HTML edits.

## Privilege and privacy boundary

GitHub Pages remains static and non-privileged.

- no GitHub token storage in browser code;
- no browser Authorization/Bearer headers;
- no arbitrary local Python execution;
- no repository writes from remote snapshot data;
- no publication of private repository snapshots or paths;
- no live security testing implied by public bounty metadata.

Execution/test/debug/write operations must use the trusted-runner or explicitly authorized-agent boundary documented in `docs/WORKSPACE_RUNNER_PROTOCOL.md`.

## Generated repository workspaces

Every validated public repository also receives a centrally generated workspace under:

`https://kaibuzz0.github.io/Git-hub-command-site/repos/<repo-id>/`

These sites derive from the same validated snapshot, use the Cipher Suite/VS Code-style layout, expose bounded repo intelligence and project-console tools, and remain separate from private repositories.

## Scaling principle

Repository #2 and repository #200 should use the same connector and UI contract. Scaling should mean adding a validated snapshot/registry entry, not cloning frontend code or inventing new storage systems.

## Completion definition

The Command OS blueprint is considered implemented when:

- repository selection establishes persistent active context;
- global fleet Home remains useful without a selected repo;
- all canonical active-project surfaces above are wired and usable;
- files/code/tests derive from bounded exact-commit snapshots;
- project-memory surfaces persist locally per repo;
- handoff/run actions remain bounded and non-privileged;
- jet-black semantic theme is active on desktop/mobile;
- CI validates the runtime and public fleet generation;
- private repositories remain excluded from public Pages.

Future work should deepen these surfaces (authenticated runner, richer PR/check collectors, authenticated private transport, stronger language/static analysis) rather than create another parallel dashboard architecture.
