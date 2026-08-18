from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mobile_is_owned_by_canonical_ultimate_shell():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "ultimate_ui.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "ultimate_ui.js").read_text(encoding="utf-8")
    assert 'ultimate_ui.css' in html
    assert 'ultimate_ui.js' in html
    assert 'mobile.css' not in html
    assert 'mobile.js' not in html
    assert '.u-mobile-nav' in css
    assert '.u-mobile-head' in css
    assert '.u-drawer.left' in css
    assert 'repeat(5,1fr)' in css
    assert 'Home' in (ROOT / 'site' / 'ui_blueprint.json').read_text(encoding='utf-8')
    assert 'openRight' in js and 'openMore' in js


def test_ultimate_mobile_preserves_static_security_boundary():
    js = (ROOT / "site" / "ultimate_ui.js").read_text(encoding="utf-8")
    lowered = js.lower()
    assert 'authorization:' not in lowered
    assert 'bearer ' not in lowered
    assert 'github_pat_' not in lowered
    assert 'ghp_' not in lowered
    assert 'api.github.com' not in lowered


def test_ultimate_mobile_prioritizes_touch_readability():
    css = (ROOT / "site" / "ultimate_ui.css").read_text(encoding="utf-8")
    assert '--u-mobile-top:58px' in css
    assert '--u-mobile-bottom:66px' in css
    assert 'min-height:46px' in css
    assert 'font-size:15px' in css
    assert 'grid-template-columns:repeat(2,minmax(0,1fr))' in css
