from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_internal_editor_is_wired_into_site():
    index = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    assert "internal_editor.css" in index
    assert "vendor/monaco/vs/loader.js" in index
    assert "internal_editor.js" in index
    assert index.index("internal_editor.js") < index.index("repository_explorer.js")


def test_pages_vendors_pinned_monaco():
    workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    assert "monaco-editor@0.55.1" in workflow
    assert "node_modules/monaco-editor/min/vs" in workflow


def test_repository_explorer_routes_previewable_files_internally():
    explorer = (ROOT / "site" / "repository_explorer.js").read_text(encoding="utf-8")
    editor = (ROOT / "site" / "internal_editor.js").read_text(encoding="utf-8")
    assert "CommandInternalEditor.open" in explorer
    assert "raw.githubusercontent.com" in editor
    assert "MAX_FILE_BYTES" in editor
    assert "readOnly:true" in editor
