from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_command_center_wires_one_canonical_four_edge_shell():
    index = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "ultimate_ui.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "ultimate_ui.js").read_text(encoding="utf-8")
    assert 'href="ultimate_ui.css"' in index
    assert 'src="ultimate_ui.js"' in index
    assert 'edge_shell.css' not in index
    assert 'edge_shell.js' not in index
    assert ".u-top" in css
    assert ".u-right" in css
    assert ".u-bottom" in css
    assert "--u-left" in css
    assert "REPOSITORIES" in js
    assert "CommandUltimateUI" in js
    assert "authorization:" not in js.lower()
    assert "bearer " not in js.lower()


def test_neon_semantic_border_palette_is_present():
    css = (ROOT / "site" / "ultimate_ui.css").read_text(encoding="utf-8").lower()
    for color in ("#00e5ff", "#2979ff", "#b026ff", "#ff2bd6", "#39ff88", "#ffe600", "#ff8a00", "#ff3155"):
        assert color in css
    assert "border-color:#00e5ff55" in css
    assert "border-color:#b026ff55" in css
    assert "border-color:#39ff8855" in css


def test_generated_repo_sites_keep_v7_navigation_layer():
    builder = (ROOT / "scripts" / "build_repository_sites.py").read_text(encoding="utf-8")
    css = (ROOT / "site" / "repo_workspace_v7.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "repo_workspace_v7.js").read_text(encoding="utf-8")
    assert '"repo_workspace_v7.css"' in builder
    assert '"repo_workspace_v7.js"' in builder
    assert ".r7-topbar" in css
    assert ".r7-quick" in css
    assert "Repository quick actions" in js
    assert "Command Center" in js
