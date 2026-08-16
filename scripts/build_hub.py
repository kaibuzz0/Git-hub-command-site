#!/usr/bin/env python3
"""Validate connected repository snapshots and build static aggregate site data."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LOCAL_REPOS = ROOT / "data" / "repos"
REMOTE_CACHE = ROOT / ".cache" / "repos"
SYNC_STATUS = ROOT / ".cache" / "sync-status.json"
OUT = ROOT / "site-data"
COLLECTIONS = (
    "tools",
    "toolsets",
    "cases",
    "opportunities",
    "intelligence",
    "sources",
    "prompts",
    "evidence",
    "activity",
)


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
    for name in COLLECTIONS + ("links",):
        if name in snapshot and not isinstance(snapshot[name], list):
            errors.append(f"{path}: {name} must be an array")
    if "agent_ops" in snapshot and not isinstance(snapshot["agent_ops"], dict):
        errors.append(f"{path}: agent_ops must be an object")
    if "stats" in snapshot and not isinstance(snapshot["stats"], dict):
        errors.append(f"{path}: stats must be an object")
    return errors


def snapshot_files() -> list[tuple[Path, str]]:
    files = [(p, "local") for p in sorted(LOCAL_REPOS.glob("*.json"))]
    files += [(p, "remote") for p in sorted(REMOTE_CACHE.glob("*.json"))] if REMOTE_CACHE.exists() else []
    return files


def snapshots() -> tuple[list[dict], list[str]]:
    errors, chosen = [], {}
    # Local is last-known-good fallback; a valid remote snapshot with the same id
    # replaces it for this build.
    for path, origin in snapshot_files():
        try:
            doc = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: {exc}")
            continue
        item_errors = validate(doc, path)
        errors.extend(item_errors)
        if item_errors:
            continue
        rid = doc["repo"]["id"]
        if rid in chosen and origin == "local":
            errors.append(f"duplicate local repo id: {rid}")
            continue
        if rid not in chosen or origin == "remote":
            chosen[rid] = {**doc, "_snapshot_origin": origin}
    return list(chosen.values()), errors


def repo_health(doc: dict) -> dict:
    stats = doc.get("stats", {}) if isinstance(doc.get("stats"), dict) else {}
    agent_summary = doc.get("agent_ops", {}).get("summary", {}) if isinstance(doc.get("agent_ops"), dict) else {}
    return {
        "sources_due": int(stats.get("sources_due", 0) or 0),
        "toolsets_needing_attention": int(stats.get("toolsets_needing_attention", 0) or 0),
        "artifacts_review_before_move": int(stats.get("artifacts_review_before_move", 0) or 0),
        "queue_p1": int(agent_summary.get("queue_p1", 0) or 0),
        "integration_items": int(agent_summary.get("integration_items", 0) or 0),
        "known_debt": int(agent_summary.get("known_debt", 0) or 0),
    }


def aggregate(docs: list[dict]) -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = {
        "schema_version": 1,
        "generated_at": now,
        "repositories": [],
        "counts": {"repositories": len(docs)},
        "sync": {},
        "health": {
            "sources_due": 0,
            "toolsets_needing_attention": 0,
            "artifacts_review_before_move": 0,
            "queue_p1": 0,
            "integration_items": 0,
            "known_debt": 0,
        },
    }
    if SYNC_STATUS.exists():
        try:
            result["sync"] = load(SYNC_STATUS)
        except (OSError, json.JSONDecodeError):
            result["sync"] = {"status": "invalid-sync-report"}
    for name in COLLECTIONS:
        result[name] = []
        result["counts"][name] = 0
    for doc in sorted(docs, key=lambda d: d["repo"]["full_name"].lower()):
        repo = doc["repo"]
        health = repo_health(doc)
        for key, value in health.items():
            result["health"][key] += value
        result["repositories"].append(
            {
                **repo,
                "generated_at": doc["generated_at"],
                "source_commit": doc["source_commit"],
                "snapshot_origin": doc.get("_snapshot_origin", "local"),
                "stats": doc.get("stats", {}),
                "agent_ops": doc.get("agent_ops", {}),
                "health": health,
                "links": doc.get("links", []),
            }
        )
        for name in COLLECTIONS:
            for item in doc.get(name, []):
                result[name].append({"repo_id": repo["id"], "repo_full_name": repo["full_name"], **item})
            result["counts"][name] += len(doc.get(name, []))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
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
        clean = {k: v for k, v in doc.items() if not k.startswith("_")}
        (OUT / f"repo-{doc['repo']['id']}.json").write_text(json.dumps(clean, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"counts": hub["counts"], "health": hub["health"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
