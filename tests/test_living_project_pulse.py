from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def test_living_project_pulse_is_wired_into_command_os():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    assert "living_info.css" in html
    assert "living_info.js" in html
    assert html.index("command_os.js") < html.index("living_info.js") < html.index("ultimate_ui.js")


def test_living_project_pulse_surfaces_real_snapshot_collections():
    js = (SITE / "living_info.js").read_text(encoding="utf-8")
    for token in (
        "PROJECT PULSE",
        "LIVE FLEET PULSE",
        "COLLECTIONS",
        "OPERATIONAL SIGNALS",
        "START HERE",
        "RECENT REPOSITORY ACTIVITY",
        "site-data/repo-",
        "opportunities",
        "intelligence",
        "evidence",
        "activity",
        "agent_ops",
    ):
        assert token in js
    lowered = js.lower()
    assert "authorization:" not in lowered
    assert "bearer " not in lowered
    assert "github_pat_" not in lowered
    assert "api.github.com" not in lowered


def test_living_pulse_is_mobile_responsive_and_pwa_cached():
    css = (SITE / "living_info.css").read_text(encoding="utf-8")
    sw = (SITE / "sw.js").read_text(encoding="utf-8")
    assert "@media(max-width:767px)" in css
    assert "living_info.css" in sw and "living_info.js" in sw
    assert "command-os-shell-v7" in sw
