#!/usr/bin/env python3
"""Build a standalone VS Code-inspired repository workspace from repo-snapshot.json."""
from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path

MAX_SNAPSHOT_BYTES = 8_000_000


def load_snapshot(path: Path) -> dict:
    if not path.exists() or path.stat().st_size > MAX_SNAPSHOT_BYTES:
        raise SystemExit("snapshot missing or too large")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or not isinstance(value.get("repo"), dict):
        raise SystemExit("invalid snapshot")
    return value


def write_site(snapshot: dict, output: Path) -> None:
    repo = snapshot["repo"]
    rid = str(repo.get("id", "repository"))
    full = str(repo.get("full_name", rid))
    commit = str(snapshot.get("source_commit", ""))
    tree = snapshot.get("repository_tree") if isinstance(snapshot.get("repository_tree"), dict) else {}
    payload = json.dumps(snapshot, separators=(",", ":")).replace("</", "<\\/")
    output.mkdir(parents=True, exist_ok=True)
    (output / ".nojekyll").write_text("", encoding="utf-8")
    (output / "repo-snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    (output / "manifest.webmanifest").write_text(json.dumps({
        "name": f"{full} Workspace", "short_name": rid[:30], "start_url": "./", "scope": "./",
        "display": "standalone", "background_color": "#181818", "theme_color": "#181818"
    }, indent=2) + "\n", encoding="utf-8")
    (output / "index.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#181818"><link rel="manifest" href="manifest.webmanifest"><title>{html.escape(full)} · Workspace</title>
<style>
:root{{--bg:#181818;--side:#181818;--panel:#1f1f1f;--line:#2b2b2b;--text:#cccccc;--muted:#858585;--blue:#007acc;--tab:#1e1e1e}}
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:var(--bg);color:var(--text);font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
body{{min-height:100vh;overflow:auto}}.title{{height:36px;position:sticky;top:0;z-index:4;background:#181818;border-bottom:1px solid var(--line);display:flex;align-items:center;padding:0 12px;gap:12px}}.title b{{color:#fff}}.title a{{margin-left:auto;color:#9cdcfe;text-decoration:none}}
.layout{{display:grid;grid-template-columns:minmax(220px,300px) 1fr;min-height:calc(100vh - 36px)}}aside{{border-right:1px solid var(--line);background:var(--side);overflow:auto;padding-bottom:40px}}main{{min-width:0;overflow:auto;padding:18px}}.section{{padding:10px 12px;border-bottom:1px solid var(--line)}}.section h3{{margin:0 0 8px;font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#bbb}}button.file,button.folder{{width:100%;border:0;background:none;color:var(--text);text-align:left;padding:4px 6px;cursor:pointer;border-radius:3px}}button:hover{{background:#2a2d2e}}.tree{{font-family:Consolas,"Courier New",monospace}}.children{{padding-left:14px}}.hidden{{display:none}}.crumb{{color:#9cdcfe;font-family:Consolas,monospace;margin-bottom:10px}}pre{{margin:0;white-space:pre;overflow:auto;background:#1e1e1e;border:1px solid var(--line);padding:14px;min-height:60vh;font:13px/1.5 Consolas,"Courier New",monospace}}.welcome{{max-width:900px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin:16px 0}}.card{{background:var(--panel);border:1px solid var(--line);padding:12px}}.card strong{{display:block;color:#fff;font-size:20px}}.muted{{color:var(--muted)}}.actions a{{display:inline-block;margin:6px 8px 6px 0;padding:6px 9px;border:1px solid #3c3c3c;color:#9cdcfe;text-decoration:none}}
@media(max-width:760px){{.layout{{grid-template-columns:1fr}}aside{{max-height:42vh;border-right:0;border-bottom:1px solid var(--line)}}main{{padding:12px}}pre{{min-height:45vh;font-size:12px}}}}
</style></head><body>
<div class="title"><span>☰</span><b>{html.escape(full)}</b><span class="muted">{html.escape(commit[:12])}</span><a href="https://kaibuzz0.github.io/Git-hub-command-site/">Command Center</a></div>
<div class="layout"><aside><div class="section"><h3>Explorer</h3><div id="tree" class="tree"></div></div><div class="section"><h3>Workspace</h3><button class="file" id="overview">⌂ Overview</button></div></aside><main id="main"></main></div>
<script id="snapshot" type="application/json">{payload}</script>
<script>
const S=JSON.parse(document.getElementById('snapshot').textContent), R=S.repo||{{}}, T=S.repository_tree||{{}};
const main=document.getElementById('main'), tree=document.getElementById('tree');
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c]));
function overview(){{let stats=S.stats||{{}};main.innerHTML=`<div class="welcome"><h1>${{esc(R.full_name||R.id)}}</h1><p class="muted">Generated ${{esc(S.generated_at)}} · source commit ${{esc((S.source_commit||'').slice(0,12))}}</p><div class="cards"><div class="card"><strong>${{T.total_files||0}}</strong>files</div><div class="card"><strong>${{T.total_directories||0}}</strong>folders</div><div class="card"><strong>${{(S.tools||[]).length}}</strong>tools</div><div class="card"><strong>${{(S.activity||[]).length}}</strong>recent activity</div></div><div class="actions"><a href="${{esc(R.url)}}">GitHub</a><a href="${{esc(R.url)}}/actions">Actions</a><a href="${{esc(R.url)}}/issues">Issues</a></div><h2>Repository workspace</h2><p>Use Explorer to browse committed folders and files. Text files open inside this site at the exact snapshot commit. Empty folders cannot appear because Git does not track them.</p></div>`}}
function raw(path){{let [owner,repo]=(R.full_name||'').split('/');return `https://raw.githubusercontent.com/${{owner}}/${{repo}}/${{S.source_commit}}/${{path.split('/').map(encodeURIComponent).join('/')}}`}}
function github(path){{return `${{R.url}}/blob/${{S.source_commit}}/${{path.split('/').map(encodeURIComponent).join('/')}}`}}
const textExt=new Set(['.py','.js','.ts','.tsx','.jsx','.json','.md','.txt','.yml','.yaml','.html','.css','.scss','.sh','.bash','.zsh','.toml','.ini','.cfg','.xml','.csv','.sql','.sol','.rs','.go','.java','.c','.h','.cpp','.hpp','.cs','.rb','.php','.pl','.lua','.r','.dockerfile']);
async function openFile(path){{main.innerHTML=`<div class="crumb">${{esc(path)}}</div><p class="muted">Loading exact snapshot file…</p>`;let ext='.'+(path.split('.').pop()||'').toLowerCase();if(!textExt.has(ext)&&!['readme','license','dockerfile','makefile'].includes(path.split('/').pop().toLowerCase())){{main.innerHTML=`<div class="crumb">${{esc(path)}}</div><p>This file is not previewed inline.</p><div class="actions"><a href="${{github(path)}}">Open on GitHub</a></div>`;return}}try{{let r=await fetch(raw(path));if(!r.ok)throw Error(r.status);let text=await r.text();if(text.length>524288)throw Error('file exceeds 512 KB preview limit');main.innerHTML=`<div class="crumb">${{esc(path)}}</div><div class="actions"><a href="${{github(path)}}">GitHub</a><a href="https://vscode.dev/github/${{esc(R.full_name)}}/blob/${{esc(S.source_commit)}}/${{path.split('/').map(encodeURIComponent).join('/')}}">VS Code</a></div><pre>${{esc(text)}}</pre>`}}catch(e){{main.innerHTML=`<div class="crumb">${{esc(path)}}</div><p>Preview unavailable: ${{esc(e.message)}}</p><div class="actions"><a href="${{github(path)}}">Open on GitHub</a></div>`}}}}
function buildTree(){{let root={{d:{{}},f:[]}};(T.files||[]).forEach(x=>{{let p=x.path.split('/'),n=root;for(let i=0;i<p.length-1;i++)n=n.d[p[i]]||(n.d[p[i]]={{d:{{}},f:[]}});n.f.push({{name:p.at(-1),path:x.path}})}});function render(n,el){{Object.keys(n.d).sort().forEach(name=>{{let wrap=document.createElement('div'),b=document.createElement('button'),c=document.createElement('div');b.className='folder';b.textContent='▸ '+name;c.className='children hidden';b.onclick=()=>{{c.classList.toggle('hidden');b.textContent=(c.classList.contains('hidden')?'▸ ':'▾ ')+name}};wrap.append(b,c);el.append(wrap);render(n.d[name],c)}});n.f.sort((a,b)=>a.name.localeCompare(b.name)).forEach(f=>{{let b=document.createElement('button');b.className='file';b.textContent='  '+f.name;b.onclick=()=>openFile(f.path);el.append(b)}})}}render(root,tree)}}
document.getElementById('overview').onclick=overview;buildTree();overview();
</script></body></html>''', encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", default="repo-snapshot.json")
    p.add_argument("--output", default="repo-site")
    a = p.parse_args()
    out = Path(a.output)
    if out.exists():
        shutil.rmtree(out)
    write_site(load_snapshot(Path(a.snapshot)), out)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
