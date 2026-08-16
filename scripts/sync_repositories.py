#!/usr/bin/env python3
"""Fetch public connected-repository snapshots into an ephemeral cache.

Remote failures are recorded, not silently promoted. Checked-in snapshots under
`data/repos/` remain the last-known-good fallback consumed by build_hub.py.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "repositories.json"
CACHE = ROOT / ".cache" / "repos"
STATUS = ROOT / ".cache" / "sync-status.json"
MAX_BYTES = 2_000_000
STATIC_HOSTS = {"raw.githubusercontent.com"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_registry() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("repositories"), list):
        raise ValueError("data/repositories.json must contain schema_version=1 and repositories[]")
    return data


def approved_host(hostname: str | None) -> bool:
    if not hostname:
        return False
    return hostname in STATIC_HOSTS or hostname.endswith(".github.io")


def validate_entry(entry: dict) -> list[str]:
    errors = []
    for field in ("id", "snapshot_url"):
        if not entry.get(field):
            errors.append(f"missing {field}")
    url = str(entry.get("snapshot_url", ""))
    parsed = urlparse(url)
    if parsed.scheme != "https":
        errors.append("snapshot_url must use https")
    if not approved_host(parsed.hostname):
        errors.append("snapshot_url host must be raw.githubusercontent.com or a public *.github.io host")
    return errors


def fetch_json(url: str) -> dict:
    req = Request(url, headers={"User-Agent": "github-command-site/1"})
    with urlopen(req, timeout=20) as response:
        content_type = response.headers.get("Content-Type", "")
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("snapshot exceeds 2 MB limit")
    if content_type and "json" not in content_type and "text/plain" not in content_type and "octet-stream" not in content_type:
        raise ValueError(f"unexpected snapshot content type: {content_type}")
    return json.loads(raw.decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true", help="validate registry without network access")
    args = parser.parse_args()
    registry = load_registry()
    seen = set()
    problems = []
    for entry in registry["repositories"]:
        rid = entry.get("id")
        if rid in seen:
            problems.append(f"duplicate registry id: {rid}")
        seen.add(rid)
        problems.extend(f"{rid or '<unknown>'}: {error}" for error in validate_entry(entry))
    if problems:
        print("\n".join(problems))
        return 1
    if args.validate:
        print(f"Valid remote registry: {len(registry['repositories'])} repositories")
        return 0

    CACHE.mkdir(parents=True, exist_ok=True)
    results = []
    for entry in registry["repositories"]:
        rid = entry["id"]
        if not entry.get("enabled", True):
            results.append({"id": rid, "status": "disabled"})
            continue
        try:
            doc = fetch_json(entry["snapshot_url"])
            snapshot_id = doc.get("repo", {}).get("id")
            if snapshot_id != rid:
                raise ValueError(f"snapshot repo.id {snapshot_id!r} does not match registry id {rid!r}")
            (CACHE / f"{rid}.json").write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
            results.append({
                "id": rid,
                "status": "fetched",
                "snapshot_url": entry["snapshot_url"],
                "source_commit": doc.get("source_commit", ""),
                "generated_at": doc.get("generated_at", ""),
            })
        except Exception as exc:  # collection failures are surfaced as status, not hidden
            results.append({"id": rid, "status": "error", "error": str(exc), "snapshot_url": entry["snapshot_url"]})
    report = {"generated_at": now_iso(), "results": results}
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
