import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_generator_builds_standalone_workspace(tmp_path):
    snapshot = {
        "schema_version": 1,
        "generated_at": "2026-08-17T00:00:00Z",
        "source_commit": "a" * 40,
        "repo": {"id": "demo", "full_name": "kaibuzz0/demo", "url": "https://github.com/kaibuzz0/demo", "default_branch": "main"},
        "stats": {"tracked_files": 2, "workflow_files": 1},
        "repository_tree": {"total_files": 2, "total_directories": 1, "files": [{"path": "README.md", "name": "README.md", "extension": ".md"}, {"path": "src/main.py", "name": "main.py", "extension": ".py"}]},
        "tools": [{"id": "demo-tool", "name": "Demo Tool", "description": "Reusable demo tool", "status": "ready"}],
        "cases": [{"id": "case-1", "name": "Example Case", "status": "active"}],
        "activity": [{"id": "commit-1", "title": "Initial commit", "type": "commit"}],
    }
    source = tmp_path / "repo-snapshot.json"
    source.write_text(json.dumps(snapshot), encoding="utf-8")
    output = tmp_path / "site"
    subprocess.run([sys.executable, str(ROOT / "connectors" / "build_repo_site.py"), "--snapshot", str(source), "--output", str(output)], check=True)
    index = (output / "index.html").read_text(encoding="utf-8")
    assert "kaibuzz0/demo" in index
    assert "Repository Workspace" in index
    assert "raw.githubusercontent.com" in index
    assert "source_commit" in index
    assert "class=\"activitybar\"" in index
    assert "class=\"sidebar\"" in index
    assert "class=\"tabbar\"" in index
    assert "class=\"breadcrumbs\"" in index
    assert "class=\"statusbar\"" in index
    assert "REPOSITORY" in index
    assert "AVAILABLE WORKSPACE DATA" in index
    assert "collections=[['tools'" in index
    assert (output / "repo-snapshot.json").exists()
    assert (output / "manifest.webmanifest").exists()


def test_pages_template_is_pinned_placeholder_and_private_safe():
    workflow = (ROOT / "connectors" / "command-site-pages.yml").read_text(encoding="utf-8")
    assert "GENERATOR_SHA" in workflow
    assert "command-site-data" in workflow
    assert "actions/deploy-pages@v4" in workflow
    docs = (ROOT / "docs" / "GENERATED_REPOSITORY_SITES.md").read_text(encoding="utf-8")
    assert "Do not deploy public Pages workspaces for private repositories" in docs
