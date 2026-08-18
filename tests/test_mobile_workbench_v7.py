from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_legacy_mobile_runtimes_are_not_wired_after_ultimate_ui():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    assert "mobile_v6.css" not in html
    assert "mobile_v7.js" not in html
    assert "mobile.css" not in html
    assert "mobile.js" not in html
    assert "ultimate_ui.css" in html
    assert "ultimate_ui.js" in html


def test_legacy_mobile_files_remain_non_privileged_if_retained():
    js = (ROOT / "site" / "mobile_v7.js").read_text(encoding="utf-8")
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "fetch(" not in js


def test_ultimate_ui_owns_thumb_navigation_and_drawer_behavior():
    css = (ROOT / "site" / "ultimate_ui.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "ultimate_ui.js").read_text(encoding="utf-8")
    assert ".u-mobile-nav" in css
    assert "translateX(-104%)" in css
    assert ".u-drawer.open" in css
    assert "Open repositories" in js
    assert "MORE TOOLS" in js
