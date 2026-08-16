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
    entry = registry["repositories"][0]
    assert entry["id"] == "cipher-solving-suite"
    assert entry["snapshot_url"].startswith("https://kaibuzz0.github.io/")
    assert entry["stale_after_hours"] == 168


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


def test_hub_tracks_snapshot_staleness():
    builder = (ROOT / "scripts/build_hub.py").read_text()
    assert "DEFAULT_STALE_HOURS = 168" in builder
    assert '"snapshot_age_hours"' in builder
    assert '"snapshot_stale"' in builder
    assert '"stale_repositories"' in builder


def test_onboarding_kit_generator(tmp_path):
    output = tmp_path / "kit"
    proc = run(
        "scripts/onboard_repository.py",
        "--repo-id", "example-repo",
        "--full-name", "example/example-repo",
        "--snapshot-url", "https://example.github.io/example-repo/data/repo-snapshot.json",
        "--output", str(output),
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (output / "export_repo_snapshot.py").exists()
    config = json.loads((output / "command-site.config.json").read_text())
    entry = json.loads((output / "registry-entry.json").read_text())
    assert config["repo_id"] == "example-repo"
    assert entry["snapshot_url"].startswith("https://example.github.io/")


def test_onboarding_kit_rejects_unapproved_transport(tmp_path):
    proc = run(
        "scripts/onboard_repository.py",
        "--repo-id", "bad-repo",
        "--full-name", "example/bad-repo",
        "--snapshot-url", "https://example.com/repo-snapshot.json",
        "--output", str(tmp_path / "bad"),
    )
    assert proc.returncode == 1
    assert "not approved" in proc.stdout
