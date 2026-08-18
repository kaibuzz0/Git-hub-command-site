#!/usr/bin/env python3
"""Canonical UI blueprint for the Command OS presentation layer.

The Python blueprint is the source of truth.  The browser consumes the checked-in
site/ui_blueprint.json generated from this file; CI --check prevents drift.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "site" / "ui_blueprint.json"

BLUEPRINT = {
    "schema_version": 1,
    "name": "Command OS Ultimate UI",
    "breakpoints": {"mobile_max": 767, "compact_max": 1023},
    "theme": {
        "black": "#000000", "editor": "#030303", "surface": "#050505", "card": "#080808",
        "raised": "#0d0d0d", "white": "#f4f7ff", "muted": "#7d8799",
        "cyan": "#00e5ff", "blue": "#2979ff", "purple": "#b026ff", "pink": "#ff2bd6",
        "green": "#39ff88", "lime": "#b6ff3b", "yellow": "#ffe600", "orange": "#ff8a00", "red": "#ff3155",
    },
    "left": [
        ["home", "⌂", "Command Center", "cyan"], ["repositories", "▱", "Repositories", "blue"],
        ["search", "⌕", "Search", "cyan"], ["source-control", "⑂", "Source Control", "blue"],
        ["run-debug", "▷", "Run / Debug", "green"], ["editor", "▤", "Editor", "pink"],
        ["workspace-tools", "⬡", "Tools", "purple"], ["whiteboard", "✎", "Whiteboard", "orange"],
        ["settings", "⚙", "Settings", "yellow"], ["palette", "›_", "Command Palette", "cyan"],
    ],
    "project": [
        ["project-overview", "⌂", "Overview", "cyan"], ["project-intelligence", "◈", "Intelligence", "purple"],
        ["project-files", "▱", "Files", "blue"], ["project-code", "</>", "Code", "pink"],
        ["project-github", "⑂", "GitHub", "blue"], ["project-tests", "✓", "Tests / CI", "green"],
        ["project-tasks", "☑", "Tasks", "yellow"], ["project-agents", "🤖", "Agents", "purple"],
        ["project-research", "◇", "Research", "orange"], ["project-notes", "✎", "Notes", "cyan"],
        ["project-commands", "›_", "Commands", "pink"], ["project-history", "◷", "History", "blue"],
    ],
    "bottom": [
        ["search", "⌕", "Search", "cyan"], ["editor", "▤", "Editor", "pink"],
        ["run-debug", "▷", "Run / Debug", "green"], ["source-control", "⑂", "Git / PRs", "blue"],
        ["workspace-tools", "⬡", "Tools", "purple"], ["project-notes", "✎", "Notes", "cyan"],
        ["output", "≡", "Output", "yellow"], ["palette", "›_", "Palette", "orange"],
    ],
    "mobile": [
        ["home", "⌂", "Home", "cyan"], ["repositories", "▱", "Repos", "blue"],
        ["search", "⌕", "Search", "cyan"], ["editor", "▤", "Editor", "pink"],
        ["more", "•••", "More", "purple"],
    ],
}


def encoded() -> str:
    return json.dumps(BLUEPRINT, indent=2, ensure_ascii=False) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    text = encoded()
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            raise SystemExit("site/ui_blueprint.json is out of sync; run python scripts/ui_blueprint.py")
        print("UI blueprint is synchronized")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
