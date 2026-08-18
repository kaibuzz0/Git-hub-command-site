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
EXTRA_CSS = [ROOT / "site" / name for name in (
    "repo_workspace_v2.css", "repo_workspace_v3.css", "repo_workspace_v4.css",
    "repo_workspace_v5.css", "repo_workspace_v6.css", "repo_workspace_v7.css", "vibrant_theme.css"
)]
EXTRA_JS = [ROOT / "site" / name for name in (
    "repo_workspace_v2.js", "repo_workspace_v3.js", "repo_workspace_v4.js",
    "repo_workspace_v5.js", "repo_workspace_v6.js", "repo_workspace_v7.js"
)]


def install_workspace_tools(target: Path) -> None:
    """Layer hub-owned interactive tooling onto one generated public mini-site."""
    assets = [*EXTRA_CSS, *EXTRA_JS]
    if any(not asset.exists() for asset in assets):
        raise SystemExit("repository workspace enhancement assets are missing")
    for asset in assets:
        shutil.copy2(asset, target / asset.name)
    index = target / "index.html"
    text = index.read_text(encoding="utf-8")
    for asset in EXTRA_CSS:
        tag = f'<link rel="stylesheet" href="{asset.name}">'
        if tag not in text:
            text = text.replace("</head>", tag + "</head>")
    for asset in EXTRA_JS:
        tag = f'<script src="{asset.name}"></script>'
        if tag not in text:
            text = text.replace("</body>", tag + "</body>")
    index.write_text(text, encoding="utf-8")


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
        install_workspace_tools(target)
        rows.append((rid, str(repo.get("full_name") or rid), snapshot.get("generated_at") or ""))

    tones = ["#00e5ff55", "#2979ff55", "#b026ff55", "#ff2bd655", "#39ff8855", "#ffe60055", "#ff8a0055", "#ff315555"]
    links = "\n".join(
        f'<li style="border-color:{tones[i % len(tones)]}"><a href="{html.escape(rid)}/">{html.escape(full)}</a><span>{html.escape(str(stamp))}</span></li>'
        for i, (rid, full, stamp) in enumerate(rows)
    )
    (output / "index.html").write_text(
        "<!doctype html><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>Repository Workspaces</title><style>body{margin:0;background:#000;color:#f4f7ff;font:14px Segoe UI,sans-serif}"
        "main{max-width:1000px;margin:auto;padding:24px}h1{color:#00e5ff;font-family:Consolas,monospace}a{color:#f4f7ff;text-decoration:none}ul{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:8px;list-style:none;padding:0}"
        "li{display:grid;gap:7px;padding:12px;border:1px solid;background:#050505}li:hover{background:#090909;box-shadow:0 0 12px #00e5ff10}"
        "span{color:#7d8799;font:11px Consolas,monospace}</style><main><h1>Repository Workspaces</h1>"
        f"<p>{len(rows)} generated public repository workspaces.</p><ul>{links}</ul></main>",
        encoding="utf-8",
    )
    print(json.dumps({"repositories": len(rows), "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
