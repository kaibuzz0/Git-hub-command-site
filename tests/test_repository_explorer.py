import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORTER = ROOT / "connectors" / "export_repo_snapshot.py"


def load_exporter():
    spec = importlib.util.spec_from_file_location("command_site_exporter", EXPORTER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_repository_inventory_discovers_nested_directories():
    exporter = load_exporter()
    inventory = exporter.repository_inventory([
        "README.md",
        "src/app.py",
        "src/lib/helpers.py",
        "docs/guide.md",
    ])
    paths = {item["path"] for item in inventory["directories"]}
    assert inventory["total_files"] == 4
    assert {"src", "src/lib", "docs"}.issubset(paths)
    assert "src" in inventory["top_level"]
    assert any(item["path"] == "src/app.py" for item in inventory["files"])


def test_repository_inventory_is_bounded():
    exporter = load_exporter()
    files = [f"generated/{i:05d}.txt" for i in range(exporter.MAX_REPOSITORY_FILES + 5)]
    inventory = exporter.repository_inventory(files)
    assert len(inventory["files"]) == exporter.MAX_REPOSITORY_FILES
    assert inventory["files_truncated"] is True
    assert inventory["total_files"] == len(files)


def test_schema_accepts_repository_tree_shape():
    schema = json.loads((ROOT / "schemas/repo-snapshot.schema.json").read_text())
    tree = schema["properties"]["repository_tree"]
    assert tree["type"] == "object"
    assert tree["properties"]["directories"]["type"] == "array"
    assert tree["properties"]["files"]["type"] == "array"


def test_site_loads_repository_explorer_and_scroll_layer():
    html = (ROOT / "site/index.html").read_text()
    js = (ROOT / "site/repository_explorer.js").read_text()
    css = (ROOT / "site/repository_explorer.css").read_text()
    assert 'repository_explorer.css' in html
    assert 'repository_explorer.js' in html
    assert 'site-data/repo-' in js
    assert 'repository_tree' in js
    assert 'repoView = enhancedRepoView' in js
    assert '-webkit-overflow-scrolling:touch' in css
    assert '#content' in css and 'overflow-y:auto' in css


def test_repository_explorer_javascript_parses_when_node_available():
    proc = subprocess.run(
        ["node", "--check", "site/repository_explorer.js"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
