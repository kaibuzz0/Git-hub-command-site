from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_command_center_uses_ultimate_theme_only():
    index = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "ultimate_ui.css").read_text(encoding="utf-8")
    assert 'ultimate_ui.css' in index
    assert 'vibrant_theme.css' not in index
    assert '--u-cyan:' in css
    assert '--u-purple:' in css
    assert '--u-black:#000' in css


def test_repo_builder_still_injects_vibrant_theme_and_triage():
    builder = (ROOT / "scripts" / "build_repository_sites.py").read_text(encoding="utf-8")
    assert 'repo_workspace_v6.css' in builder
    assert 'repo_workspace_v6.js' in builder
    assert 'vibrant_theme.css' in builder


def test_triage_queue_is_heuristic_and_handoff_only():
    js = (ROOT / "site" / "repo_workspace_v6.js").read_text(encoding="utf-8")
    assert 'Next Actions' in js
    assert 'Copy agent spec' in js
    assert 'Add task' in js
    assert "protocol:'command-site-agent/v1'" in js
    assert 'Verify every signal before changing code' in js
    assert 'Authorization' not in js
    assert 'github_pat_' not in js
