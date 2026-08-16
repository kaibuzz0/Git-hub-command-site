import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)


def test_example_snapshot_has_required_identity():
    data = json.loads((ROOT / "examples/repo-snapshot.example.json").read_text())
    assert data["schema_version"] == 1
    assert data["repo"]["url"].startswith("https://")
    assert data["source_commit"]


def test_remote_registry_is_valid_without_network():
    proc = run("scripts/sync_repositories.py", "--validate")
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_hub_builder_validates_empty_registry():
    proc = run("scripts/build_hub.py", "--validate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Valid snapshots: 0" in proc.stdout


def test_site_is_data_driven_and_installable():
    js = (ROOT / "site/app.js").read_text()
    html = (ROOT / "site/index.html").read_text()
    assert "site-data/hub.json" in js
    assert "repositories" in js
    assert "Ctrl+K" in html
    assert "manifest.webmanifest" in html
    assert "serviceWorker" in js


def test_remote_registry_rejects_non_https_or_unapproved_hosts(tmp_path):
    script = (ROOT / "scripts/sync_repositories.py").read_text()
    assert 'ALLOWED_HOSTS = {"raw.githubusercontent.com"}' in script
    assert 'parsed.scheme != "https"' in script
