from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mobile_v7_legacy_runtime_is_not_wired_after_v8():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    assert "mobile_v6.css" not in html
    assert "mobile_v7.js" not in html
    assert "mobile.css" in html
    assert "mobile.js" in html


def test_legacy_mobile_files_remain_non_privileged_if_retained():
    js = (ROOT / "site" / "mobile_v7.js").read_text(encoding="utf-8")
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "fetch(" not in js


def test_v8_owns_thumb_navigation_and_drawer_behavior():
    css = (ROOT / "site" / "mobile.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "mobile.js").read_text(encoding="utf-8")
    assert "bottom:0" in css
    assert "translateX(-104%)" in css
    assert "mobile-drawer-open" in css
    assert "Open repositories" in js
    assert "Workspace tools" in js
