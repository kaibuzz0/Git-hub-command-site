from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repo_workspace_v2_assets_define_useful_repo_tools():
    js = (ROOT / "site" / "repo_workspace_v2.js").read_text(encoding="utf-8")
    css = (ROOT / "site" / "repo_workspace_v2.css").read_text(encoding="utf-8")
    assert "renderScripts" in js
    assert "runnerSpec" in js
    assert "python','-m','pdb" in js
    assert "pytest" in js
    assert "node','--inspect-brk" in js
    assert "bash','-x" in js
    assert "renderNotes" in js
    assert "localStorage" in js
    assert "renderRecent" in js
    assert ".repo-notebook" in css
    assert ".script-card" in css


def test_repo_workspace_v2_keeps_static_execution_boundary():
    js = (ROOT / "site" / "repo_workspace_v2.js").read_text(encoding="utf-8")
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "eval(" not in js
    assert "new Function" not in js
    assert "execute" not in js.lower() or "does not execute arbitrary code" in js.lower()


def test_fleet_builder_injects_repo_workspace_assets():
    builder = (ROOT / "scripts" / "build_repository_sites.py").read_text(encoding="utf-8")
    assert "repo_workspace_v2.css" in builder
    assert "repo_workspace_v2.js" in builder
    assert "install_workspace_tools" in builder
