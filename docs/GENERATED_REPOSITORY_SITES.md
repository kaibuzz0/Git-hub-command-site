# Generated Repository Workspaces

The Command Site supports two complementary surfaces:

1. the central multi-repository Command Center; and
2. an optional standalone GitHub Pages workspace for each public connected repository.

A repository workspace is generated from the same bounded `repo-snapshot.json` already used by the hub. It is not a second manually maintained website database.

## Flow

`repo commit -> snapshot workflow -> command-site-data/repo-snapshot.json -> repository Pages builder -> standalone workspace`

At the same time the hub continues to consume the same snapshot:

`command-site-data/repo-snapshot.json -> hub sync -> validate -> aggregate -> central Command Center`

## Ownership

The hub owns the reusable site generator in `connectors/build_repo_site.py`. Connected repositories should contain only a thin pinned Pages workflow. Normal UI upgrades happen in the hub and are rolled out by deliberately rotating the immutable generator SHA in connected workflows.

## Workspace behavior

The generated site is VS Code-inspired and repository-specific. It exposes the committed repository tree, overview statistics, exact snapshot commit, activity counts, GitHub/Actions/Issues links, and safe lazy text-file preview. It does not copy repository source into the hub and does not embed secrets or credentials.

Text previews are fetched from the public repository at the exact `source_commit`. Unsupported/binary files fall back to GitHub. Empty directories cannot appear because Git does not track them.

## Privacy boundary

Do not deploy public Pages workspaces for private repositories. Private repositories remain connector-capable but require authenticated private transport before any browser workspace is exposed.

## Pages setting

A repository must have GitHub Pages configured for GitHub Actions. The workflow cannot always bootstrap that repository setting with its own workflow token. If Pages has never been enabled, enable `Settings -> Pages -> Source: GitHub Actions` once.

## Fleet rollout

Rollout is intentionally two-phase:

1. merge and validate the generator in the hub to obtain an immutable commit SHA;
2. install/rotate the thin Pages workflow in selected public repositories using that pinned SHA.

Do not point fleet workflows at mutable `main` for executable generator code.
