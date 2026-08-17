from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mobile_v8_is_single_coherent_shell():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "mobile.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "mobile.js").read_text(encoding="utf-8")
    assert 'mobile.css' in html
    assert 'mobile.js' in html
    assert 'mobile_v6.css' not in html
    assert 'mobile_v7.js' not in html
    assert '.mobile-nav' in css
    assert '.mobile-top' in css
    assert '.mobile-drawer-open .sidebar' in css
    assert '.wb-editor-area>.wb-editor-group.secondary{display:none!important}' in css
    assert 'repeat(5,1fr)' in css
    assert 'Workspace tools' in js
    assert 'Home' in js and 'Repos' in js and 'Search' in js and 'Editor' in js and 'More' in js


def test_mobile_v8_preserves_static_security_boundary():
    js = (ROOT / "site" / "mobile.js").read_text(encoding="utf-8")
    assert 'Authorization' not in js
    assert 'Bearer ' not in js
    assert 'github_pat_' not in js
    assert 'ghp_' not in js
    assert 'fetch(' not in js
    assert 'localStorage' not in js


def test_mobile_v8_prioritizes_touch_readability():
    css = (ROOT / "site" / "mobile.css").read_text(encoding="utf-8")
    assert '--m-top:54px' in css
    assert '--m-nav:62px' in css
    assert 'min-height:44px' in css
    assert 'font-size:15px' in css
    assert 'grid-template-columns:repeat(2,minmax(0,1fr))' in css
