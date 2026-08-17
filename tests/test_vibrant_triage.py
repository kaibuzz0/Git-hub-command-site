from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_command_center_loads_vibrant_theme():
    index = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    css = (ROOT / "site" / "vibrant_theme.css").read_text(encoding="utf-8")
    assert 'vibrant_theme.css' in index
    assert '--v-cyan:' in css
    assert '--v-purple:' in css
    assert 'linear-gradient' in css


def test_repo_builder_injects_vibrant_theme_and_triage():
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
