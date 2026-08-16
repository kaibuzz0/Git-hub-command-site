#!/usr/bin/env python3
"""Plan or apply the hub side of connecting a repository to Command Workbench."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "repositories.json"
ONBOARD = ROOT / "scripts" / "onboard_repository.py"
DEFAULT_STALE_HOURS = 168


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("repositories"), list):
        raise ValueError("invalid data/repositories.json")
    return data


def entry_for(repo_id: str, full_name: str, snapshot_url: str, stale_after_hours: int) -> dict:
    owner, repository = full_name.split("/", 1)
    return {
        "id": repo_id,
        "snapshot_url": snapshot_url,
        "enabled": True,
        "owner": owner,
        "repository": repository,
        "stale_after_hours": stale_after_hours,
        "notes": "Managed through Command Workbench repository connector."
    }


def conflicts(registry: dict, candidate: dict) -> list[str]:
    errors = []
    for current in registry.get("repositories", []):
        if current.get("id") == candidate["id"]:
            errors.append(f"repository id already registered: {candidate['id']}")
        if current.get("snapshot_url") == candidate["snapshot_url"]:
            errors.append(f"snapshot URL already registered: {candidate['snapshot_url']}")
        if current.get("owner") == candidate["owner"] and current.get("repository") == candidate["repository"]:
            errors.append(f"repository already registered: {candidate['owner']}/{candidate['repository']}")
    return sorted(set(errors))


def plan(repo_id: str, full_name: str, snapshot_url: str, stale_after_hours: int, mode: str) -> dict:
    registry = load_registry()
    candidate = entry_for(repo_id, full_name, snapshot_url, stale_after_hours)
    errors = conflicts(registry, candidate)
    return {
        "schema_version": 1,
        "mode": mode,
        "repo": {"id": repo_id, "full_name": full_name, "snapshot_url": snapshot_url},
        "registry_entry": candidate,
        "conflicts": errors,
        "operations": [
            {"scope": "hub", "action": "generate-connector-kit", "status": "planned"},
            {"scope": "target", "action": "adapt-exporter-to-canonical-state", "status": "requires-target-authorization"},
            {"scope": "target", "action": "publish-bounded-snapshot", "status": "requires-target-authorization"},
            {"scope": "hub", "action": "register-snapshot-endpoint", "status": "planned"},
            {"scope": "hub", "action": "sync-validate-aggregate", "status": "planned"}
        ],
        "validation": [
            "python scripts/sync_repositories.py --validate",
            "python scripts/build_hub.py --validate",
            "python scripts/build_hub.py"
        ]
    }


def apply_connection(doc: dict, output_dir: Path) -> None:
    if doc["conflicts"]:
        raise ValueError("; ".join(doc["conflicts"]))
    repo = doc["repo"]
    subprocess.check_call([
        sys.executable, str(ONBOARD),
        "--repo-id", repo["id"],
        "--full-name", repo["full_name"],
        "--snapshot-url", repo["snapshot_url"],
        "--output", str(output_dir)
    ], cwd=ROOT)
    registry = load_registry()
    registry["repositories"].append(doc["registry_entry"])
    registry["repositories"].sort(key=lambda item: str(item.get("id", "")))
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    (output_dir / "integration-plan.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description="Connect a repository to GitHub Command Workbench")
    p.add_argument("--repo-id", required=True)
    p.add_argument("--full-name", required=True)
    p.add_argument("--snapshot-url", required=True)
    p.add_argument("--mode", choices=["existing", "new"], default="existing")
    p.add_argument("--stale-after-hours", type=int, default=DEFAULT_STALE_HOURS)
    p.add_argument("--output")
    p.add_argument("--apply", action="store_true", help="write connector kit and hub registry entry")
    a = p.parse_args()
    if a.stale_after_hours < 1:
        print("stale-after-hours must be positive")
        return 1
    if a.full_name.count("/") != 1:
        print("full-name must be OWNER/REPOSITORY")
        return 1
    doc = plan(a.repo_id, a.full_name, a.snapshot_url, a.stale_after_hours, a.mode)
    if a.apply:
        out = Path(a.output) if a.output else ROOT / "onboarding" / a.repo_id
        try:
            apply_connection(doc, out)
        except (ValueError, subprocess.CalledProcessError) as exc:
            print(str(exc))
            return 1
        doc["applied"] = True
        doc["output"] = str(out)
    else:
        doc["applied"] = False
    print(json.dumps(doc, indent=2))
    return 1 if doc["conflicts"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
