#!/usr/bin/env python3
"""Portable baseline exporter for connecting a repository to GitHub Command Site.

Exports bounded metadata only. Repositories should adapt mappings to their
existing canonical registries rather than creating duplicate source-of-truth
files merely for the command site.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git(*args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def doc(path: Path) -> dict:
    if not path.exists(): return {}
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError): return {}
    return data if isinstance(data,dict) else {}


def collection(path: Path, *keys: str) -> list:
    data=doc(path)
    for key in keys:
        value=data.get(key)
        if isinstance(value,list): return value
    return []


def recent_activity(full_name: str, limit: int=10) -> list[dict]:
    raw=git("log",f"-{limit}","--pretty=format:%H%x1f%aI%x1f%s")
    rows=[]
    for line in raw.splitlines() if raw else []:
        parts=line.split("\x1f",2)
        if len(parts)==3:
            sha,stamp,title=parts
            rows.append({"id":sha,"type":"commit","title":title,"timestamp":stamp,"url":f"https://github.com/{full_name}/commit/{sha}"})
    return rows


def build(repo_id: str, full_name: str) -> dict:
    root=Path.cwd(); commit=git("rev-parse","HEAD") or "unknown-commit"; branch=git("rev-parse","--abbrev-ref","HEAD") or "main"
    now=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    site=root/"site-data"; data=root/"data"
    return {
        "schema_version":1,"generated_at":now,"source_commit":commit,
        "repo":{"id":repo_id,"full_name":full_name,"url":f"https://github.com/{full_name}","default_branch":branch if branch!="HEAD" else "main"},
        "stats":doc(site/"status.json"),
        "tools":collection(data/"tools.json","items","tools"),
        "toolsets":collection(site/"toolsets.json","items","toolsets"),
        "cases":collection(site/"cases.json","items","cases"),
        "opportunities":collection(data/"opportunities.json","items","opportunities"),
        "intelligence":collection(data/"intelligence.json","items","intelligence"),
        "sources":collection(site/"sources.json","sources","items") or collection(data/"intelligence_sources.json","sources","items"),
        "prompts":collection(data/"prompts.json","prompts","items"),
        "evidence":collection(site/"artifacts.json","items","artifacts"),
        "agent_ops":doc(site/"agent-ops.json"),
        "activity":recent_activity(full_name),
        "links":[{"id":"github","name":"GitHub repository","url":f"https://github.com/{full_name}"}]
    }


def main() -> int:
    p=argparse.ArgumentParser();p.add_argument("--repo-id",required=True);p.add_argument("--full-name",required=True);p.add_argument("--output",default=".command-site/repo-snapshot.json");a=p.parse_args()
    output=Path(a.output);output.parent.mkdir(parents=True,exist_ok=True);snapshot=build(a.repo_id,a.full_name);output.write_text(json.dumps(snapshot,indent=2)+"\n",encoding="utf-8");print(output);return 0


if __name__=="__main__": raise SystemExit(main())
