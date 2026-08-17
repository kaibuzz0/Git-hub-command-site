from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_project_console_assets_are_injected():
    builder = (ROOT / "scripts" / "build_repository_sites.py").read_text(encoding="utf-8")
    js = (ROOT / "site" / "repo_workspace_v3.js").read_text(encoding="utf-8")
    css = (ROOT / "site" / "repo_workspace_v3.css").read_text(encoding="utf-8")
    assert "repo_workspace_v3.js" in builder
    assert "repo_workspace_v3.css" in builder
    for marker in ["README & docs", "Tasks & checklist", "Saved commands", "Dependencies & packages", "CI & test history"]:
        assert marker in js
    assert "repo-doc-grid" in css


def test_project_console_keeps_browser_local_boundary():
    js = (ROOT / "site" / "repo_workspace_v3.js").read_text(encoding="utf-8")
    assert "localStorage" in js
    assert "command-site-runner/v1" in js
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "fetch(raw" in js


def test_repo_workspace_v2_exposes_shared_hooks():
    js = (ROOT / "site" / "repo_workspace_v2.js").read_text(encoding="utf-8")
    assert "window.repoSnapshot" in js
    assert "window.repoWorkspaceRender" in js
    assert "window.repoWorkspaceRemember" in js
