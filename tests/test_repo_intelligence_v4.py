from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repo_intelligence_assets_are_injected():
    builder = (ROOT / "scripts" / "build_repository_sites.py").read_text(encoding="utf-8")
    js = (ROOT / "site" / "repo_workspace_v4.js").read_text(encoding="utf-8")
    css = (ROOT / "site" / "repo_workspace_v4.css").read_text(encoding="utf-8")
    assert "repo_workspace_v4.js" in builder
    assert "repo_workspace_v4.css" in builder
    assert "Start Here" in js
    assert "Likely entry points" in js
    assert "TODO / FIXME Hotspots" in js
    assert "Structure" in js
    assert ".intel-grid" in css


def test_repo_intelligence_keeps_public_static_boundary():
    js = (ROOT / "site" / "repo_workspace_v4.js").read_text(encoding="utf-8")
    assert "raw.githubusercontent.com" in js
    assert "source_commit" in js
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "slice(0,45)" in js
    assert "slice(0,200000)" in js
