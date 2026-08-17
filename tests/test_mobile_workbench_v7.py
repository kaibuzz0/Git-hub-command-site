from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mobile_v7_is_wired_into_site():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "mobile_v6.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "mobile_v7.js").read_text(encoding="utf-8")
    assert "mobile_v6.css" in html
    assert "mobile_v7.js" in html
    assert "wb-mobile-top" in css
    assert "wb-mobile-drawer-open" in css
    assert "wb-mobile-fab" in css
    assert "wbMobileExplorer" in js
    assert "wbMobileCommand" in js
    assert "touchstart" in js
    assert "touchend" in js


def test_mobile_v7_keeps_static_security_boundary():
    js = (ROOT / "site" / "mobile_v7.js").read_text(encoding="utf-8")
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "fetch(" not in js


def test_mobile_v7_has_thumb_navigation_and_drawer_behavior():
    css = (ROOT / "site" / "mobile_v6.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "mobile_v7.js").read_text(encoding="utf-8")
    assert "bottom:0" in css
    assert "translateX(-102%)" in css
    assert "transform:translateX(0)" in css
    assert "Command palette" in js or "command palette" in js
