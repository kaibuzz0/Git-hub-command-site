import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def snapshot(repo_id: str) -> dict:
    return {
        "schema_version": 1,
        "generated_at": "2026-08-17T00:00:00Z",
        "source_commit": "b" * 40,
        "repo": {"id": repo_id, "full_name": f"kaibuzz0/{repo_id}", "url": f"https://github.com/kaibuzz0/{repo_id}", "default_branch": "main"},
        "stats": {},
        "repository_tree": {"total_files": 1, "total_directories": 0, "files": [{"path": "README.md", "name": "README.md", "extension": ".md"}]},
        "tools": [], "activity": []
    }


def test_build_repository_sites_generates_each_repo_and_index(tmp_path):
    source = tmp_path / "site-data"
    source.mkdir()
    for repo_id in ("alpha", "beta"):
        (source / f"repo-{repo_id}.json").write_text(json.dumps(snapshot(repo_id)), encoding="utf-8")
    out = tmp_path / "repo-sites"
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_repository_sites.py"), "--input", str(source), "--output", str(out)], check=True)
    assert (out / "alpha" / "index.html").exists()
    assert (out / "beta" / "index.html").exists()
    index = (out / "index.html").read_text(encoding="utf-8")
    assert "kaibuzz0/alpha" in index
    assert "kaibuzz0/beta" in index


def test_pages_packages_repo_sites_and_workbench_links_them():
    pages = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
    explorer = (ROOT / "site" / "repository_explorer.js").read_text(encoding="utf-8")
    assert "build_repository_sites.py" in pages
    assert "cp -R repo-sites/. _site/repos/" in pages
    assert "Repo Website" in explorer
    assert "repos/${encodeURIComponent(repo.id)}/" in explorer
