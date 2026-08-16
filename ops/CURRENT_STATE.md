# Current State

Last reconciled: 2026-08-16 23:20 UTC
Default branch: `main`

## Verified architecture

- PR #1 merged the multi-repository command-center foundation.
- PR #3 merged remote snapshot synchronization, scheduled refresh support, command palette, sync health and PWA groundwork.
- Hub CI validates on Python 3.11, 3.12 and 3.13 with per-test diagnostics.
- The hub owns the UI, shared snapshot contract, registry, sync logic, aggregation and Pages workflow.
- Connected repositories remain authoritative and export bounded public metadata snapshots.

## First connected repository

- `kaibuzz0/cipher-solving-suite` is being onboarded as the first production spoke.
- Its integration branch/PR exports a Pages-hosted `data/repo-snapshot.json` from canonical tools, toolsets, cases, opportunities, intelligence, source health, prompts, evidence metadata, Agent Ops, stats, links and recent commit activity.
- This hub registers `cipher-solving-suite` through `data/repositories.json` and accepts approved public GitHub Pages (`*.github.io`) snapshot transport in addition to `raw.githubusercontent.com`.

## Command Center v2

The current feature branch expands the hub with:

- repository filtering and global workspace mode;
- global search across repository collections;
- repository health/attention aggregation;
- prompts and evidence collections;
- richer repository drill-down;
- Agent Ops priorities and handoffs in repository detail;
- recent activity and opportunity radar;
- relationship navigation for case/source/toolset-linked records;
- safer HTTPS link rendering;
- visible snapshot provenance and sync state.

## Known blocker

GitHub Pages is not yet enabled at the repository-account setting level. The Pages workflow successfully validates snapshots, builds aggregate data and assembles the static site, but `actions/configure-pages` cannot create the initial Pages site with the workflow token (`Resource not accessible by integration`).

One manual repository setting is still required: **Settings → Pages → Source: GitHub Actions**. After that, the existing deployment workflow can publish the site normally.

## Current priorities

1. Merge the `cipher-solving-suite` connected-repository exporter after its CI passes.
2. Merge the hub Command Center v2/first-repository integration after CI passes.
3. Enable GitHub Pages once through repository Settings → Pages → GitHub Actions.
4. Verify the hub fetches the live cipher snapshot and renders its collections.
5. Use the first integration as the reference connector for the next repositories.

## Next handoff

Verify both integration PRs independently. Once `cipher-solving-suite` publishes its snapshot and this hub branch is merged, run the hub remote sync and confirm `cipher-solving-suite` appears with real tools/toolsets/cases/opportunities/intelligence/sources/prompts/evidence/Agent Ops/activity rather than an empty placeholder.
