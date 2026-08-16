# Current State

Status: foundation build

## Architecture

- Hub repository owns UI, schemas, aggregate data, and Pages deployment.
- Connected repositories export bounded JSON snapshots.
- `scripts/build_hub.py` validates and aggregates snapshots into `site-data/`.
- The site dynamically renders repositories and their capabilities.

## Current priorities

1. Validate the foundation through CI.
2. Connect the first real repository using the snapshot protocol.
3. Expand generic relationship/detail views as real data requires them.

## Next handoff

Verify the foundation PR, then onboard `cipher-solving-suite` as the first real connected repository without hardcoding it into the site.
