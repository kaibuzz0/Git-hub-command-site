(() => {
  const FILES = Array.isArray(T?.files) ? T.files : [];
  const SCRIPT_RE = /(?:^|\/)(?:test_.*\.py|.*_test\.py|.*\.(?:py|sh|bash|js|mjs|cjs))$/i;
  const scripts = FILES.filter(f => SCRIPT_RE.test(String(f.path || ''))).slice(0, 250);
  const repoId = String(R.id || R.full_name || 'repository');
  const noteKey = `command-site:repo-notes:${repoId}`;
  const recentKey = `command-site:recent-files:${repoId}`;
  const outputKey = `command-site:last-runner-spec:${repoId}`;
  const e = s => esc(s);
  window.repoSnapshot = S;
  window.repoWorkspaceScripts = scripts;
  window.repoWorkspaceRender = (name, icon, path, body) => { setHead(name, icon, path); main.innerHTML = body; };

  function storeGet(key, fallback) { try { const v = localStorage.getItem(key); return v == null ? fallback : JSON.parse(v); } catch { return fallback; } }
  function storeSet(key, value) { try { localStorage.setItem(key, JSON.stringify(value)); } catch {} }
  function copyText(text, button) { navigator.clipboard?.writeText(text).then(() => { if (button) { const old = button.textContent; button.textContent = 'Copied'; setTimeout(() => button.textContent = old, 900); } }).catch(() => {}); }
  function download(name, text, type='application/json') { const a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([text],{type})); a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(a.href),500); }

  function scriptKind(path) {
    const p=path.toLowerCase();
    if (p.endsWith('.py')) return 'python';
    if (/\.(sh|bash)$/.test(p)) return 'shell';
    return 'node';
  }
  function commands(path, mode) {
    const kind=scriptKind(path), test=/\/(?:tests?|spec)\/|(?:^|\/)(?:test_|.*_test\.)/i.test(path);
    if (kind==='python') {
      if (mode==='debug') return ['python','-m','pdb',path];
      if (mode==='test') return test ? ['python','-m','pytest',path,'-vv','--tb=short'] : ['python','-m','py_compile',path];
      return ['python',path];
    }
    if (kind==='shell') {
      if (mode==='debug') return ['bash','-x',path];
      if (mode==='test') return ['bash','-n',path];
      return ['bash',path];
    }
    if (mode==='debug') return ['node','--inspect-brk',path];
    if (mode==='test') return ['node','--check',path];
    return ['node',path];
  }
  function runnerSpec(path, mode) {
    return {
      schema_version: 1,
      request_id: `repo-${repoId}-${mode}-${Date.now()}`,
      repo_id: repoId,
      repository: R.full_name || repoId,
      source_commit: S.source_commit || '',
      operation: mode,
      working_directory: '.',
      command: commands(path, mode),
      timeout_seconds: mode==='test' ? 300 : 120,
      artifacts: [],
      note: 'Prepared by static repository workspace. Execute only in an authorized trusted runner.'
    };
  }
  function prepare(path, mode, button) {
    const spec=runnerSpec(path,mode), text=JSON.stringify(spec,null,2);
    storeSet(outputKey,spec); copyText(text,button);
    const box=document.getElementById('runnerOutput'); if(box) box.textContent=text;
  }
  function githubFile(path) { return `${R.url}/blob/${S.source_commit}/${path.split('/').map(encodeURIComponent).join('/')}`; }

  function renderScripts() {
    setHead('scripts.run.json','▷','scripts');
    const rows=scripts.map(f=>{const p=String(f.path||''); return `<div class="script-card"><div class="script-main"><strong>${e(p)}</strong><span>${e(scriptKind(p))}</span></div><div class="script-actions"><button data-run="run" data-path="${e(p)}">Run</button><button data-run="test" data-path="${e(p)}">Test</button><button data-run="debug" data-path="${e(p)}">Debug</button><a href="${e(githubFile(p))}" target="_blank">GitHub</a></div></div>`}).join('');
    const last=storeGet(outputKey,null);
    main.innerHTML=`<div class="repo-tool-head"><div><div class="kicker">TRUSTED RUNNER ADAPTER</div><h1>Scripts</h1><p class="muted">Detected from committed repository files. Buttons prepare and copy exact runner requests; this static site does not execute arbitrary code.</p></div><span class="repo-count">${scripts.length} detected</span></div><div class="script-list">${rows||'<div class="empty">No supported scripts detected.</div>'}</div><div class="section-caption">RUNNER REQUEST</div><pre id="runnerOutput" class="runner-output">${e(last?JSON.stringify(last,null,2):'Choose Run, Test, or Debug to prepare a trusted-runner request.')}</pre>`;
    main.querySelectorAll('[data-run]').forEach(b=>b.onclick=()=>prepare(b.dataset.path,b.dataset.run,b));
  }

  function renderNotes() {
    setHead('notes.md','✎','notes');
    const value=String(storeGet(noteKey,''));
    main.innerHTML=`<div class="repo-tool-head"><div><div class="kicker">BROWSER-LOCAL PROJECT MEMORY</div><h1>Repository Notes</h1><p class="muted">Autosaved only in this browser for ${e(R.full_name||repoId)}. Nothing is committed or uploaded automatically.</p></div></div><textarea id="repoNotebook" class="repo-notebook" spellcheck="true" placeholder="Ideas, TODOs, commands, handoff notes…">${e(value)}</textarea><div class="note-actions"><span id="noteState">Saved locally</span><button id="exportNotes">Export .md</button><button id="copyNotes">Copy</button><button id="clearNotes">Clear</button></div>`;
    const ta=document.getElementById('repoNotebook'), state=document.getElementById('noteState'); let timer;
    ta.oninput=()=>{state.textContent='Saving…';clearTimeout(timer);timer=setTimeout(()=>{storeSet(noteKey,ta.value);state.textContent='Saved locally'},180)};
    document.getElementById('exportNotes').onclick=()=>download(`${repoId}-notes.md`,ta.value,'text/markdown');
    document.getElementById('copyNotes').onclick=e=>copyText(ta.value,e.currentTarget);
    document.getElementById('clearNotes').onclick=()=>{if(confirm('Clear local notes for this repository?')){ta.value='';storeSet(noteKey,'');state.textContent='Cleared'}};
  }

  function recentFiles() { return storeGet(recentKey,[]).filter(x=>typeof x==='string').slice(0,12); }
  function remember(path) { const next=[path,...recentFiles().filter(x=>x!==path)].slice(0,12);storeSet(recentKey,next); }
  window.repoWorkspaceRemember = remember;
  function renderRecent() {
    setHead('recent.json','◷','recent files'); const rows=recentFiles();
    main.innerHTML=`<div class="repo-tool-head"><div><div class="kicker">LOCAL WORKSPACE HISTORY</div><h1>Recent Files</h1><p class="muted">Recently opened files on this device.</p></div></div><div class="recent-list">${rows.length?rows.map(p=>`<button data-recent="${e(p)}"><span>▤</span><strong>${e(p)}</strong></button>`).join(''):'<div class="empty">Open repository files and they will appear here.</div>'}</div>`;
    main.querySelectorAll('[data-recent]').forEach(b=>b.onclick=()=>openFile(b.dataset.recent));
  }

  if (typeof openFile === 'function') {
    const original=openFile;
    window.openFile = async path => { remember(path); return original(path); };
    document.addEventListener('click',ev=>{const b=ev.target.closest('.repo-tree .tree-item,#tree .tree-item'); if(b?.dataset?.path) remember(b.dataset.path)},true);
  }

  function addNavigation() {
    const activity=document.getElementById('activity'), nav=document.getElementById('workspaceNav');
    if (!activity || !nav) return;
    const entries=[['scripts','▷','Scripts',renderScripts,scripts.length],['notes','✎','Notes',renderNotes,1],['recent','◷','Recent',renderRecent,recentFiles().length]];
    entries.forEach(([id,icon,label,fn,count])=>{
      const a=document.createElement('button');a.className='activity';a.title=label;a.textContent=icon;a.dataset.repoTool=id;a.onclick=()=>{document.querySelectorAll('.activity').forEach(x=>x.classList.remove('active'));a.classList.add('active');fn();if(innerWidth<=850) side?.classList.remove('open')};activity.insertBefore(a,activity.querySelector('.activity-spacer'));
      const b=document.createElement('button');b.className='tree-item repo-tool-nav';b.innerHTML=`<span>${icon}</span><span>${label}</span><small>${count||''}</small>`;b.onclick=()=>a.click();nav.appendChild(b);
    });
  }

  addNavigation();
})();
