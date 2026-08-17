from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_workbench_v5_is_wired_into_site():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "workbench_v5.css").read_text(encoding="utf-8")
    js = (ROOT / "site" / "workbench_v5.js").read_text(encoding="utf-8")
    assert "workbench_v5.css" in html
    assert "workbench_v5.js" in html
    assert "wb-editor-area" in css
    assert "split-vertical" in css
    assert "split-horizontal" in css
    assert "Workspace Layouts" in js
    assert "Coding" in js
    assert "Research" in js
    assert "Repo Review" in js
    assert "Scratch Diff" in js
    assert "README" in js
    assert "Repo Site" in js


def test_workbench_v5_keeps_browser_local_security_boundary():
    js = (ROOT / "site" / "workbench_v5.js").read_text(encoding="utf-8")
    assert "localStorage" in js
    assert "Authorization" not in js
    assert "Bearer " not in js
    assert "github_pat_" not in js
    assert "ghp_" not in js
    assert "raw.githubusercontent.com" in js
    assert "source_commit" in js
    assert "noopener" in js


def test_v5_diff_and_readme_are_bounded_or_local():
    js = (ROOT / "site" / "workbench_v5.js").read_text(encoding="utf-8")
    assert "524288" in js
    assert "command-workbench-v5-diff" in js
    assert "Paste a unified diff" in js
    assert "README exceeds preview limit" in js
    assert "browser-local" in js
