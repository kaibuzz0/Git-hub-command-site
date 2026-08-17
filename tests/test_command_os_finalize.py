from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def test_final_command_os_assets_are_wired():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    assert 'command_os_finalize.css' in html
    assert 'command_os_search.js' in html
    assert html.index('command_os.js') < html.index('command_os_search.js')


def test_project_search_spans_blueprint_memory_and_snapshot_sources():
    js = (SITE / "command_os_search.js").read_text(encoding="utf-8")
    for section in ('CODE', 'DOCUMENTATION', 'TASKS', 'RESEARCH', 'COMMANDS', 'PROJECT METADATA', 'NOTES'):
        assert section in js
    assert 'CommandInternalEditor' in js
    assert 'state.query' in js
    assert 'CommandOS.snapshot' in js
    assert '/search?q=' in js


def test_project_search_keeps_browser_security_boundary():
    js = (SITE / "command_os_search.js").read_text(encoding="utf-8").lower()
    assert 'localstorage' in js
    assert 'github_token' not in js
    assert 'authorization:' not in js
    assert 'bearer ' not in js
    assert 'api.github.com' not in js


def test_active_context_has_dedicated_desktop_grid_row():
    css = (SITE / "command_os_finalize.css").read_text(encoding="utf-8")
    assert 'grid-template-rows:35px auto var(--wb-tab-h) minmax(0,1fr) auto 22px' in css
    assert '.universal-search-grid' in css
    assert '@media(max-width:760px)' in css
