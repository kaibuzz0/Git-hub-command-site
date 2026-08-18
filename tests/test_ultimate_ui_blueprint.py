import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def test_python_blueprint_and_browser_blueprint_define_one_ui_contract():
    py = (ROOT / "scripts" / "ui_blueprint.py").read_text(encoding="utf-8")
    data = json.loads((SITE / "ui_blueprint.json").read_text(encoding="utf-8"))
    assert data["name"] == "Command OS Ultimate UI"
    assert data["schema_version"] == 1
    assert len(data["project"]) == 12
    assert len(data["mobile"]) == 5
    assert "--check" in py
    for key in ("cyan", "blue", "purple", "pink", "green", "lime", "yellow", "orange", "red"):
        assert key in data["theme"]


def test_index_uses_one_canonical_presentation_layer():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    assert "ultimate_ui.css" in html and "ultimate_ui.js" in html
    for legacy in ("mobile.css", "mobile.js", "vibrant_theme.css", "cyber_theme.css", "edge_shell.css", "edge_shell.js"):
        assert legacy not in html
    assert html.index("command_os.js") < html.index("ultimate_ui.js")


def test_ultimate_ui_supports_four_edge_desktop_and_mobile_drawers():
    css = (SITE / "ultimate_ui.css").read_text(encoding="utf-8")
    js = (SITE / "ultimate_ui.js").read_text(encoding="utf-8")
    for selector in (".u-left", ".u-top", ".u-right", ".u-bottom", ".u-mobile-head", ".u-mobile-nav", ".u-drawer"):
        assert selector in css
    for phrase in ("ui_blueprint.json", "CommandUltimateUI", "openLeft", "openRight", "openMore", "activateRepo"):
        assert phrase in js
    lowered = js.lower()
    assert "authorization:" not in lowered
    assert "bearer " not in lowered
    assert "github_pat_" not in lowered
    assert "api.github.com" not in lowered


def test_all_major_workspace_boxes_receive_semantic_borders():
    css = (SITE / "ultimate_ui.css").read_text(encoding="utf-8").lower()
    for selector in (".card", ".metric", ".os-panel", ".task-card", ".agent-card", ".editor-shell", ".repo-card"):
        assert selector in css
    for color in ("#00e5ff55", "#2979ff55", "#b026ff55", "#ff2bd655", "#39ff8855", "#ffe60055", "#ff8a0055", "#ff315555"):
        assert color in css


def test_ultimate_ui_places_wrapped_workbench_in_real_workspace_row():
    css = (SITE / "workbench_v5.css").read_text(encoding="utf-8")
    assert "body.ultimate-ready .wb-session-banner{display:none!important}" in css
    assert "body.ultimate-ready #wbEditorArea{grid-row:4!important" in css
    assert "body.ultimate-ready #wbPrimaryBody>#content{height:auto!important" in css
    assert "@media(max-width:767px)" in css
    assert "body.ultimate-ready #wbEditorArea{grid-row:3!important" in css
    assert "body.ultimate-ready #wbEditorArea>.wb-editor-group.primary>.wb-group-head{display:none!important}" in css
    assert "body.ultimate-ready #wbEditorArea>.wb-editor-group.secondary{display:none!important}" in css
