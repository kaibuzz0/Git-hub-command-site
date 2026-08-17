from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def test_active_repository_context_is_wired():
    index = (SITE / "index.html").read_text(encoding="utf-8")
    js = (SITE / "command_os.js").read_text(encoding="utf-8")
    assert 'command_os.js' in index
    assert 'active_context.js' not in index
    assert 'command-os-active-repo' in js
    assert 'data-repo-filter' in js
    assert 'ACTIVE PROJECT' in js
    assert 'activeContextBar' in js
    assert 'repoView=function(id){activate(id)}' in js


def test_cyber_theme_is_jet_black_and_semantic():
    index = (SITE / "index.html").read_text(encoding="utf-8")
    css = (SITE / "cyber_theme.css").read_text(encoding="utf-8").lower()
    assert 'cyber_theme.css' in index
    assert '--bg:#000' in css
    for color in ('#00e5ff', '#2979ff', '#b026ff', '#ff2bd6', '#39ff88', '#ffe600', '#ff8a00', '#ff3155'):
        assert color in css
    assert '.neon-card.cyan' in css
    assert '.neon-card.purple' in css
    assert '.syn-key' in css


def test_context_layer_keeps_browser_credential_boundary():
    js = (SITE / "command_os.js").read_text(encoding="utf-8").lower()
    assert 'github_token' not in js
    assert 'authorization:' not in js
    assert 'bearer ' not in js
    assert 'api.github.com' not in js
