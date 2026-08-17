# Generated Repository Workspaces

The Command Site exposes two complementary user-facing surfaces from the same validated repository snapshot:

1. the central multi-repository Command Center; and
2. a generated repository-specific mini-site for every connected public repository.

The canonical fleet path is central hosting under:

`https://kaibuzz0.github.io/Git-hub-command-site/repos/<repo-id>/`

A repository mini-site is generated from the same bounded `repo-snapshot.json` already used by the hub. It is not a second manually maintained website database.

## Canonical flow

`repo commit -> snapshot workflow -> command-site-data/repo-snapshot.json`

Then the same snapshot feeds both outputs:

`repo-snapshot.json -> hub sync -> validate -> aggregate -> central Command Center`

`repo-snapshot.json -> fleet mini-site generator -> /repos/<repo-id>/`

Because all public mini-sites are packaged into the existing Command Site Pages artifact, ordinary repositories do not need GitHub Pages enabled individually.

## Ownership

The hub owns the reusable generator in `connectors/build_repo_site.py` and the fleet builder in `scripts/build_repository_sites.py`. Connected repositories remain responsible only for publishing their bounded snapshot. Normal mini-site UI improvements therefore happen centrally and become available to every public connected repository on the next successful hub deployment.

Do not copy the Command Center frontend into every repository merely to create a website.

## Workspace behavior

Generated mini-sites are VS Code-inspired and repository-specific. They expose the committed repository tree, overview statistics, exact snapshot commit, activity counts, GitHub/Actions/Issues links, and safe lazy text-file preview.

Text previews are fetched from the public source repository at the exact `source_commit`. Unsupported, binary, or oversized files fall back to GitHub. Empty directories cannot appear because Git does not track them.

The central Command Center links each repository detail view to its generated mini-site through the `Repo Website` action.

## Privacy boundary

Do not deploy public Pages workspaces for private repositories. Only snapshots already admitted to the public hub registry receive central public mini-sites. Private repositories remain connector-capable but require authenticated private transport and a non-public presentation surface before they can be browsed safely.

## Optional dedicated repository Pages

`connectors/command-site-pages.yml` remains an optional template for a repository that explicitly needs its own `https://<owner>.github.io/<repo>/` deployment.

That mode is not the fleet default because GitHub Pages must be enabled for each repository and a workflow token cannot reliably bootstrap that setting. Dedicated deployment must also be checked for collisions with an existing custom Pages site before use.

Never overwrite a repository's established user-facing Pages application (for example, a project-specific site) just to install the generic Command Site workspace.

## Fleet deployment

The central Pages workflow:

1. syncs and validates all registered public snapshots;
2. generates aggregate Command Center data;
3. runs `scripts/build_repository_sites.py` against the synced snapshots;
4. packages every generated workspace under `_site/repos/<repo-id>/`; and
5. deploys one Pages artifact.

A failure in an individual source snapshot should remain visible through sync health and must not silently publish unvalidated repository state.
