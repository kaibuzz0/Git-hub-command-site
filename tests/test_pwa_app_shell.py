import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def test_manifest_is_installable_command_os():
    manifest = json.loads((SITE / "manifest.webmanifest").read_text(encoding="utf-8"))
    assert manifest["id"] == "./"
    assert manifest["start_url"] == "./"
    assert manifest["scope"] == "./"
    assert manifest["display"] == "standalone"
    assert manifest["background_color"] == "#000000"
    assert manifest["theme_color"] == "#000000"
    assert manifest["icons"]
    assert any(icon["src"] == "icons/command-os.svg" for icon in manifest["icons"])


def test_page_wires_pwa_controller_and_mobile_metadata():
    html = (SITE / "index.html").read_text(encoding="utf-8")
    assert 'rel="manifest" href="manifest.webmanifest"' in html
    assert 'apple-mobile-web-app-capable' in html
    assert 'icons/command-os.svg' in html
    assert 'pwa.css' in html
    assert 'pwa.js' in html


def test_service_worker_caches_current_shell_and_has_update_path():
    sw = (SITE / "sw.js").read_text(encoding="utf-8")
    for asset in (
        "command_os.js", "command_os_search.js", "command_os_finalize.css",
        "mobile.js", "pwa.js", "pwa.css", "manifest.webmanifest", "icons/command-os.svg",
    ):
        assert asset in sw
    assert "SKIP_WAITING" in sw
    assert "request.mode==='navigate'" in sw
    assert "site-data" in sw
    assert "url.origin!==self.location.origin" in sw


def test_pwa_controller_is_install_update_aware_and_credential_free():
    js = (SITE / "pwa.js").read_text(encoding="utf-8").lower()
    assert "beforeinstallprompt" in js
    assert "serviceworker.register" in js
    assert "controllerchange" in js
    assert "skip_waiting" in js
    assert "github_token" not in js
    assert "authorization:" not in js
    assert "bearer " not in js
    assert "api.github.com" not in js
