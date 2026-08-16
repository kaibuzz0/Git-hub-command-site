# Current State

Last reconciled: 2026-08-16 23:27 UTC
Default branch: `main`

## Verified architecture

- PR #1 merged the multi-repository command-center foundation.
- PR #3 merged remote snapshot synchronization, scheduled refresh support, command palette, sync health and PWA groundwork.
- PR #4 merged the main Command Center v2 implementation: first repository registry entry, GitHub Pages snapshot transport, expanded prompts/evidence schema and aggregation, repository health, global filtering/search, richer drill-down, Agent Ops views, activity/opportunity surfaces, and relationship navigation.
- PR #5 merged the remaining hub governance layer.
- Hub CI validates on Python 3.11, 3.12 and 3.13 with per-test diagnostics.
- The hub owns the UI, shared snapshot contract, registry, sync logic, aggregation and Pages workflow.
- Connected repositories remain authoritative and export bounded public metadata snapshots.

## First connected repository

- `kaibuzz0/cipher-solving-suite` is integrated as the first production spoke through source PR #20.
- Its exporter derives the command-site snapshot from canonical tools, toolsets, cases, opportunities, intelligence, source health, prompts, evidence metadata, Agent Ops, stats, links and bounded recent commit activity.
- Its Pages workflow publishes the generated snapshot as `data/repo-snapshot.json`.
- Source PR #20 passed Core Validation and Daily Repository Maintenance before merge.
- The post-merge cipher Pages build successfully completed snapshot generation, static assembly, artifact upload and final deployment.
- This hub registers `cipher-solving-suite` through `data/repositories.json` and accepts approved public GitHub Pages (`*.github.io`) snapshot transport in addition to `raw.githubusercontent.com`.

## Command Center v2 capabilities

- repository filtering and global workspace mode;
- global search across repository collections;
- repository health/attention aggregation;
- prompts and evidence collections;
- richer repository drill-down;
- Agent Ops priorities and handoffs in repository detail;
- recent activity and opportunity radar;
- relationship navigation for case/source/toolset-linked records;
- safer HTTPS link rendering;
- visible snapshot provenance and sync state;
- PWA/command-palette groundwork;
- scheduled remote refresh with bounded host/size/identity validation and local last-known-good fallback support.

## Known blocker

GitHub Pages is not yet enabled at the **hub repository** account-setting level. The hub Pages workflow successfully validates snapshots, builds aggregate data and assembles the static site, but `actions/configure-pages` cannot create the initial Pages site with the workflow token (`Resource not accessible by integration`).

One manual hub setting is still required: **Settings → Pages → Source: GitHub Actions**. After that, the existing deployment workflow can publish the command center normally.

## Current priorities

1. Enable GitHub Pages once through hub Settings → Pages → GitHub Actions.
2. Execute/verify the hub remote sync against the published cipher snapshot and confirm aggregate `hub.json` contains real repository collections.
3. Verify the live hub UI renders the first spoke correctly.
4. Package this first-spoke integration as the reusable onboarding path for subsequent repositories.
5. Add near-immediate event-driven refresh later without weakening the snapshot validation boundary.

## Next handoff

After this reconciliation merges and hub Pages is enabled, run the hub sync/build path and verify `cipher-solving-suite` appears with real tools/toolsets/cases/opportunities/intelligence/sources/prompts/evidence/Agent Ops/activity. Any remote failure must remain visible in sync health and must not be disguised as successful current data.
