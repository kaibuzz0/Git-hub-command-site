# Work Queue

## P1

- [x] Build and merge the multi-repo command-center foundation.
- [x] Add remote snapshot synchronization, sync health, command palette and PWA groundwork.
- [x] Merge the first production connected-repository exporter in `kaibuzz0/cipher-solving-suite` (PR #20).
- [x] Publish the cipher command-site snapshot through its successful GitHub Pages build.
- [x] Merge the main Command Center v2 data/UI architecture and first real repository registry entry (PR #4).
- [ ] Merge the remaining governance reconciliation in hub PR #5.
- [ ] Enable GitHub Pages once in this hub repository's settings using **Source: GitHub Actions**.
- [ ] Verify live end-to-end hub sync from the published `cipher-solving-suite` snapshot into aggregate `hub.json` and the rendered UI.

## P2

- [ ] Add repository-dispatch/GitHub App refresh so connected repo updates can trigger near-immediate hub rebuilds instead of waiting for schedule.
- [ ] Add richer cross-repository relationships and saved workspace views.
- [ ] Add optional GitHub PR/check/issue activity collectors without requiring browser-side API credentials.
- [ ] Add stale-snapshot age thresholds and stronger health warnings.
- [ ] Package the connected-repository exporter as a reusable toolset/template for fast onboarding of future repos.
- [ ] Add a repository onboarding wizard/checklist in the command site documentation.
- [ ] Add a last-known-good snapshot promotion workflow after a remote snapshot passes validation, without hiding later remote failures.
