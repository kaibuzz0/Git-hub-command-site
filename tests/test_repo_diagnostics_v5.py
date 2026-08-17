from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_repo_diagnostics_assets_are_wired():
    builder = (ROOT / "scripts" / "build_repository_sites.py").read_text(encoding="utf-8")
    js = (ROOT / "site" / "repo_workspace_v5.js").read_text(encoding="utf-8")
    css = (ROOT / "site" / "repo_workspace_v5.css").read_text(encoding="utf-8")
    assert "repo_workspace_v5.js" in builder
    assert "repo_workspace_v5.css" in builder
    assert "Health & attention" in js
    assert "review signals, not proof of defects" in js
    assert "POSSIBLE TEST GAPS" in js
    assert ".diag-score" in css


def test_repo_diagnostics_do_not_add_credentials_or_execution():
    js = (ROOT / "site" / "repo_workspace_v5.js").read_text(encoding="utf-8")
    lowered = js.lower()
    assert "authorization" not in lowered
    assert "github_token" not in lowered
    assert "localstorage" not in lowered
    assert "eval(" not in lowered
    assert "child_process" not in lowered
