#!/usr/bin/env python3
"""Validate connected repository snapshots and build static aggregate site data."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REPOS = ROOT / "data" / "repos"
OUT = ROOT / "site-data"
COLLECTIONS = ("tools", "toolsets", "cases", "opportunities", "intelligence", "sources", "activity")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(snapshot: dict, path: Path) -> list[str]:
    errors: list[str] = []
    if snapshot.get("schema_version") != 1:
        errors.append(f"{path}: schema_version must be 1")
    repo = snapshot.get("repo")
    if not isinstance(repo, dict):
        return errors + [f"{path}: missing repo object"]
    for field in ("id", "full_name", "url", "default_branch"):
        if not repo.get(field):
            errors.append(f"{path}: repo.{field} missing")
    if repo.get("url") and urlparse(str(repo["url"])).scheme != "https":
        errors.append(f"{path}: repo.url must use https")
    if not snapshot.get("generated_at"):
        errors.append(f"{path}: generated_at missing")
    if not snapshot.get("source_commit"):
        errors.append(f"{path}: source_commit missing")
    for name in COLLECTIONS:
        if name in snapshot and not isinstance(snapshot[name], list):
            errors.append(f"{path}: {name} must be an array")
    return errors


def snapshots() -> tuple[list[dict], list[str]]:
    docs, errors, seen = [], [], set()
    for path in sorted(REPOS.glob("*.json")):
        try:
            doc = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        errors.extend(validate(doc, path))
        rid = doc.get("repo", {}).get("id")
        if rid in seen:
            errors.append(f"duplicate repo id: {rid}")
        seen.add(rid)
        docs.append(doc)
    return docs, errors


def aggregate(docs: list[dict]) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = {"schema_version": 1, "generated_at": now, "repositories": [], "counts": {"repositories": len(docs)}}
    for name in COLLECTIONS:
        result[name] = []
        result["counts"][name] = 0
    for doc in docs:
        repo = doc["repo"]
        result["repositories"].append({**repo, "generated_at": doc["generated_at"], "source_commit": doc["source_commit"], "stats": doc.get("stats", {})})
        for name in COLLECTIONS:
            for item in doc.get(name, []):
                result[name].append({"repo_id": repo["id"], "repo_full_name": repo["full_name"], **item})
            result["counts"][name] += len(doc.get(name, []))
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--validate", action="store_true")
    args = p.parse_args()
    docs, errors = snapshots()
    if errors:
        print("\n".join(errors))
        return 1
    if args.validate:
        print(f"Valid snapshots: {len(docs)}")
        return 0
    OUT.mkdir(exist_ok=True)
    hub = aggregate(docs)
    (OUT / "hub.json").write_text(json.dumps(hub, indent=2) + "\n", encoding="utf-8")
    for doc in docs:
        (OUT / f"repo-{doc['repo']['id']}.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(hub["counts"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
