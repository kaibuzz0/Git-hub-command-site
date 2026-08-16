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
    assert "1 repositories" in proc.stdout
    registry = json.loads((ROOT / "data/repositories.json").read_text())
    assert registry["repositories"][0]["id"] == "cipher-solving-suite"
    assert registry["repositories"][0]["snapshot_url"].startswith("https://kaibuzz0.github.io/")


def test_hub_builder_validates_without_remote_cache():
    proc = run("scripts/build_hub.py", "--validate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Valid snapshots:" in proc.stdout


def test_site_is_data_driven_installable_and_supports_expanded_collections():
    js = (ROOT / "site/app.js").read_text()
    html = (ROOT / "site/index.html").read_text()
    builder = (ROOT / "scripts/build_hub.py").read_text()
    assert "site-data/hub.json" in js
    assert "repositories" in js
    assert "prompts" in js and "evidence" in js
    assert "prompts" in builder and "evidence" in builder
    assert "Workspace health" in js
    assert "Ctrl+K" in html
    assert "manifest.webmanifest" in html
    assert "serviceWorker" in js


def test_remote_transport_is_bounded_to_github_hosts():
    script = (ROOT / "scripts/sync_repositories.py").read_text()
    assert '"raw.githubusercontent.com"' in script
    assert 'hostname.endswith(".github.io")' in script
    assert 'parsed.scheme != "https"' in script
    assert "MAX_BYTES = 2_000_000" in script


def test_snapshot_schema_declares_prompts_and_evidence():
    schema = json.loads((ROOT / "schemas/repo-snapshot.schema.json").read_text())
    assert schema["properties"]["prompts"]["type"] == "array"
    assert schema["properties"]["evidence"]["type"] == "array"
