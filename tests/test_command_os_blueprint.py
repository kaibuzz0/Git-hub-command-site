from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_command_os_is_wired_as_primary_context_runtime():
    html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    assert 'command_os.css' in html
    assert 'command_os.js' in html
    assert 'active_context.js' not in html


def test_command_os_contains_full_project_blueprint_surfaces():
    js = (ROOT / "site" / "command_os.js").read_text(encoding="utf-8")
    for label in (
        'Overview', 'Intelligence', 'Files', 'Code', 'GitHub', 'Tests / CI',
        'Tasks', 'Agents', 'Research', 'Notes', 'Commands', 'History'
    ):
        assert label in js
    for phrase in (
        'MISSION CONTROL', 'ACTIVE PROJECT', 'agent-task', 'runner-request',
        'SOURCE → FINDING → HYPOTHESIS → EXPERIMENT → CODE → TEST → RESULT',
    ):
        assert phrase in js


def test_command_os_uses_local_project_memory_not_browser_credentials():
    js = (ROOT / "site" / "command_os.js").read_text(encoding="utf-8").lower()
    assert 'localstorage' in js
    assert 'github_token' not in js
    assert 'authorization:' not in js
    assert 'bearer ' not in js
    assert 'api.github.com' not in js


def test_command_os_theme_is_jet_black_semantic_neon():
    css = (ROOT / "site" / "command_os.css").read_text(encoding="utf-8").lower()
    for token in ('--os-black:#000', '--os-cyan:#00e5ff', '--os-purple:#b026ff', '--os-green:#39ff88', '--os-red:#ff3155'):
        assert token in css
    assert 'background:#000' in css
    assert '.os-panel.cyan' in css
    assert '.os-panel.purple' in css
    assert '.os-panel.green' in css
    assert '.os-panel.red' in css
