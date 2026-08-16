import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_example_snapshot_has_required_identity():
    data = json.loads((ROOT / "examples/repo-snapshot.example.json").read_text())
    assert data["schema_version"] == 1
    assert data["repo"]["url"].startswith("https://")
    assert data["source_commit"]


def test_hub_builder_validates_empty_registry():
    proc = subprocess.run([sys.executable, "scripts/build_hub.py", "--validate"], cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Valid snapshots: 0" in proc.stdout


def test_site_is_data_driven():
    js = (ROOT / "site/app.js").read_text()
    assert "site-data/hub.json" in js
    assert "repositories" in js
