#!/usr/bin/env python3
"""Portable baseline exporter for connecting a repository to GitHub Command Site.

This intentionally exports bounded metadata only. Repositories can extend the
snapshot with their own canonical registries while preserving schema v1.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def load_json(path: Path, key: str) -> list:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    value = data.get(key, []) if isinstance(data, dict) else []
    return value if isinstance(value, list) else []


def build(repo_id: str, full_name: str) -> dict:
    root = Path.cwd()
    commit = git("rev-parse", "HEAD")
    branch = git("rev-parse", "--abbrev-ref", "HEAD")
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": 1,
        "generated_at": now,
        "source_commit": commit,
        "repo": {
            "id": repo_id,
            "full_name": full_name,
            "url": f"https://github.com/{full_name}",
            "default_branch": branch if branch != "HEAD" else "main",
        },
        "tools": load_json(root / "data" / "tools.json", "tools"),
        "opportunities": load_json(root / "data" / "opportunities.json", "items"),
        "intelligence": load_json(root / "data" / "intelligence.json", "items"),
        "sources": load_json(root / "data" / "intelligence_sources.json", "sources"),
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-id", required=True)
    p.add_argument("--full-name", required=True)
    p.add_argument("--output", default=".command-site/repo-snapshot.json")
    args = p.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build(args.repo_id, args.full_name), indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
