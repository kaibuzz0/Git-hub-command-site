from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_workbench_v4_is_wired_into_site():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "workbench_v4.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "workbench_v4.js").read_text(encoding="utf-8")
    assert "workbench_v4.css" in html
    assert "workbench_v4.js" in html
    assert "workspaceTabs" in html
    assert "wbInspector" in html
    assert "sidebar-splitter" in html
    assert "inspector-splitter" in html
    assert "whiteboardBtn" in html
    assert "--wb-sidebar-w" in css
    assert "--wb-inspector-w" in css
    assert "localStorage" in js
    assert "setInterval(()=>checkUpdates(false),60000)" in js
    assert "renderWhiteboard" in js
    assert "Export PNG" in js


def test_workbench_v4_keeps_static_security_boundary():
    js = (ROOT / "site" / "workbench_v4.js").read_text(encoding="utf-8")
    assert "raw.githubusercontent.com" not in js
    assert "Authorization" not in js
    assert "token" not in js.lower()
    assert "window.open" not in js or "noopener" in js
