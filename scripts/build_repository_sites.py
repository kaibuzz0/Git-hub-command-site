#!/usr/bin/env python3
"""Generate standalone mini-sites for every synced public repository snapshot."""
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from connectors.build_repo_site import load_snapshot, write_site

ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="site-data")
    p.add_argument("--output", default="repo-sites")
    a = p.parse_args()
    source = Path(a.input)
    output = Path(a.output)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True, exist_ok=True)

    rows = []
    for path in sorted(source.glob("repo-*.json")):
        snapshot = load_snapshot(path)
        repo = snapshot.get("repo") or {}
        rid = str(repo.get("id") or "")
        if not ID_RE.fullmatch(rid):
            raise SystemExit(f"unsafe repository id in {path.name}: {rid!r}")
        target = output / rid
        write_site(snapshot, target)
        rows.append((rid, str(repo.get("full_name") or rid), snapshot.get("generated_at") or ""))

    links = "\n".join(
        f'<li><a href="{html.escape(rid)}/">{html.escape(full)}</a><span>{html.escape(str(stamp))}</span></li>'
        for rid, full, stamp in rows
    )
    (output / "index.html").write_text(
        "<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Repository Workspaces</title><style>body{margin:0;background:#181818;color:#ccc;font:14px Segoe UI,sans-serif}"
        "main{max-width:900px;margin:auto;padding:24px}h1{color:#fff}a{color:#9cdcfe;text-decoration:none}ul{list-style:none;padding:0}"
        "li{display:flex;justify-content:space-between;gap:16px;padding:10px 12px;border-bottom:1px solid #2b2b2b;background:#1f1f1f}"
        "span{color:#858585;font-size:12px}</style><main><h1>Repository Workspaces</h1>"
        f"<p>{len(rows)} generated public repository workspaces.</p><ul>{links}</ul></main>",
        encoding="utf-8",
    )
    print(json.dumps({"repositories": len(rows), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
