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
    registry = json.loads((ROOT / "data/repositories.json").read_text())
    assert registry["repositories"][0]["id"] == "cipher-solving-suite"
    assert registry["repositories"][0]["stale_after_hours"] == 168


def test_hub_builder_validates_without_remote_cache():
    proc = run("scripts/build_hub.py", "--validate")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Valid snapshots:" in proc.stdout


def test_workbench_registry_and_settings_are_valid():
    tools = json.loads((ROOT / "data/workspace-tools.json").read_text())
    settings = json.loads((ROOT / "data/workspace-settings.json").read_text())
    ids = [item["id"] for item in tools["tools"]]
    assert tools["schema_version"] == 1
    assert len(ids) == len(set(ids))
    assert "repository-manager" in ids
    assert "python-debug-adapter" in ids
    assert settings["theme"] == "vscode-dark-plus"
    assert settings["runner"]["allow_browser_code_execution"] is False


def test_site_exposes_operator_workbench_surfaces():
    js = (ROOT / "site/app.js").read_text()
    html = (ROOT / "site/index.html").read_text()
    css = (ROOT / "site/app.css").read_text()
    builder = (ROOT / "scripts/build_hub.py").read_text()
    assert "site-data/hub.json" in js
    assert "workspace_tools" in builder and "workspace_settings" in builder
    for view in ("source-control", "run-debug", "editor", "workspace-tools", "settings"):
        assert view in html or view in js
    assert "Repository Manager" in js
    assert "Python Debug Adapter" in js
    assert "localStorage" in js
    assert "vscode.dev/github/" in js
    assert "--blue:#007acc" in css
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
    proc = run("scripts/onboard_repository.py", "--repo-id", "example-repo", "--full-name", "example/example-repo", "--snapshot-url", "https://example.github.io/example-repo/data/repo-snapshot.json", "--output", str(output))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (output / "export_repo_snapshot.py").exists()
    assert json.loads((output / "registry-entry.json").read_text())["id"] == "example-repo"


def test_onboarding_kit_rejects_unapproved_transport(tmp_path):
    proc = run("scripts/onboard_repository.py", "--repo-id", "bad-repo", "--full-name", "example/bad-repo", "--snapshot-url", "https://example.com/repo-snapshot.json", "--output", str(tmp_path / "bad"))
    assert proc.returncode == 1
    assert "not approved" in proc.stdout


def test_repository_connector_plans_without_mutating_registry():
    before = (ROOT / "data/repositories.json").read_text()
    proc = run("scripts/connect_repository.py", "--repo-id", "planned-repo", "--full-name", "example/planned-repo", "--snapshot-url", "https://example.github.io/planned-repo/data/repo-snapshot.json")
    after = (ROOT / "data/repositories.json").read_text()
    assert proc.returncode == 0, proc.stdout + proc.stderr
    data = json.loads(proc.stdout)
    assert data["applied"] is False
    assert data["registry_entry"]["id"] == "planned-repo"
    assert before == after


def test_repository_connector_rejects_duplicate_identity():
    proc = run("scripts/connect_repository.py", "--repo-id", "cipher-solving-suite", "--full-name", "kaibuzz0/cipher-solving-suite", "--snapshot-url", "https://kaibuzz0.github.io/cipher-solving-suite/data/repo-snapshot.json")
    assert proc.returncode == 1
    assert "already registered" in proc.stdout


def test_runner_protocol_keeps_browser_execution_outside_static_site():
    protocol = (ROOT / "docs/WORKSPACE_RUNNER_PROTOCOL.md").read_text()
    assert "No browser-side credential storage" in protocol
    assert "python-debug" in protocol
    assert "trusted runner" in protocol.lower()
