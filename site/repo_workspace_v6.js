(() => {
  const S=()=>window.repoSnapshot||{}, R=()=>S().repo||{}, T=()=>S().repository_tree||{}, F=()=>Array.isArray(T().files)?T().files:[];
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const key=s=>`gh-command:${R().id||'repo'}:${s}`;
  const load=(k,d)=>{try{return JSON.parse(localStorage.getItem(key(k)))??d}catch{return d}};
  const save=(k,v)=>{try{localStorage.setItem(key(k),JSON.stringify(v))}catch{}};
  const copy=t=>navigator.clipboard?.writeText(t).catch(()=>{});
  const codeExt=new Set(['.py','.js','.mjs','.cjs','.ts','.tsx','.jsx','.go','.rs','.java','.c','.cc','.cpp','.h','.hpp','.cs','.rb','.php','.sol','.sh','.bash']);
  const base=p=>String(p||'').split('/').pop(), ext=p=>{const n=base(p);return n.includes('.')?n.slice(n.lastIndexOf('.')).toLowerCase():''};
  function analyze(){
    const files=F(), tests=files.filter(f=>/(^|\/)(tests?|specs?)\/|(^|\/)(test_|.*_test\.)/i.test(f.path)), workflows=files.filter(f=>/^\.github\/workflows\/.*\.ya?ml$/i.test(f.path));
    const sources=files.filter(f=>codeExt.has(ext(f.path))&&!/(^|\/)(tests?|specs?)\//i.test(f.path));
    const names=new Map();files.forEach(f=>names.set(base(f.path).toLowerCase(),(names.get(base(f.path).toLowerCase())||0)+1));
    const repeats=[...names.entries()].filter(([,n])=>n>1).sort((a,b)=>b[1]-a[1]);
    const gaps=sources.filter(f=>{const n=base(f.path).replace(/\.[^.]+$/,'').toLowerCase();return !tests.some(t=>base(t.path).toLowerCase().includes(n))}).slice(0,20);
    const actions=[];
    if(!workflows.length)actions.push({p:1,title:'Add or review CI automation',reason:'No GitHub Actions workflow was detected.',kind:'ci',target:`${R().url}/actions`});
    if(sources.length>10&&!tests.length)actions.push({p:1,title:'Establish a test baseline',reason:`${sources.length} code files detected with no identified tests.`,kind:'tests',target:`${R().url}`});
    if(gaps.length>8)actions.push({p:2,title:'Review likely test gaps',reason:`${gaps.length} sampled source files have no obvious similarly named test.`,kind:'tests',paths:gaps.slice(0,8).map(x=>x.path)});
    if(repeats.length>8)actions.push({p:2,title:'Review repeated basenames',reason:`${repeats.length} repeated filenames may hide duplicated or parallel implementations.`,kind:'duplication',paths:repeats.slice(0,8).map(x=>`${x[0]} ×${x[1]}`)});
    if(T().files_truncated||T().directories_truncated)actions.push({p:2,title:'Run a deeper inventory pass',reason:'The public snapshot is truncated, so diagnostics are partial.',kind:'inventory'});
    const latest=S().activity?.[0]?.timestamp?Date.parse(S().activity[0].timestamp):NaN;if(Number.isFinite(latest)){const days=(Date.now()-latest)/86400000;if(days>120)actions.push({p:2,title:'Review stale project areas',reason:`Latest exported activity is about ${Math.round(days)} days old.`,kind:'stale'});}
    const todos=files.filter(f=>/TODO|FIXME/i.test(f.path)).slice(0,6);if(todos.length)actions.push({p:3,title:'Inspect TODO/FIXME-related files',reason:`${todos.length} filenames suggest unfinished work.`,kind:'todo',paths:todos.map(x=>x.path)});
    if(!actions.length)actions.push({p:3,title:'Perform a targeted maintenance pass',reason:'No strong snapshot warnings detected; review Start Here, Hotspots and CI for the next meaningful improvement.',kind:'review'});
    return actions.sort((a,b)=>a.p-b.p);
  }
  function addTask(a){const tasks=load('tasks',[]);const text=`[${a.kind}] ${a.title} — ${a.reason}`;if(!tasks.some(x=>x.text===text)){tasks.push({text,done:false,created_at:new Date().toISOString(),source:'next-actions'});save('tasks',tasks)}}
  function agentSpec(a){return {protocol:'command-site-agent/v1',kind:'repo-triage',repository:R().full_name,repository_id:R().id,source_commit:S().source_commit,priority:a.p,title:a.title,reason:a.reason,paths:a.paths||[],created_at:new Date().toISOString(),instruction:'Inspect this signal, verify it against the repository, make only the smallest justified change, run relevant tests, and report evidence.'}}
  function render(){const rows=analyze();window.repoWorkspaceRender('next-actions.json','⚡','next-actions',`<div class="repo-console-head"><div><div class="kicker">ACTIONABLE TRIAGE</div><h1>Next Actions</h1><p class="muted">Ranked review queue derived from transparent snapshot heuristics. Verify every signal before changing code.</p></div><span class="repo-count">${rows.length} actions</span></div><div class="triage-list">${rows.map((a,i)=>`<article class="triage-card p${a.p}"><div class="triage-rank">P${a.p}</div><div class="triage-body"><h3>${esc(a.title)}</h3><p>${esc(a.reason)}</p>${a.paths?.length?`<div class="triage-paths">${a.paths.map(p=>`<code>${esc(p)}</code>`).join('')}</div>`:''}</div><div class="triage-actions"><button data-task="${i}">Add task</button><button data-agent="${i}">Copy agent spec</button>${a.target?`<a target="_blank" href="${esc(a.target)}">Open</a>`:''}</div></article>`).join('')}</div>`);document.querySelectorAll('[data-task]').forEach(b=>b.onclick=()=>{addTask(rows[+b.dataset.task]);const old=b.textContent;b.textContent='Added';setTimeout(()=>b.textContent=old,900)});document.querySelectorAll('[data-agent]').forEach(b=>b.onclick=()=>{copy(JSON.stringify(agentSpec(rows[+b.dataset.agent]),null,2));const old=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=old,900)})}
  function install(){if(!window.repoWorkspaceRender||!window.repoSnapshot)return setTimeout(install,60);const nav=document.getElementById('workspaceNav');if(!nav||document.getElementById('repoTriageNav'))return;const box=document.createElement('div');box.id='repoTriageNav';box.className='tree-section';box.innerHTML='<div class="tree-caption">ACTION QUEUE</div><button class="tree-item" data-triage="next">⚡ <span>Next Actions</span></button>';nav.append(box);box.querySelector('[data-triage="next"]').onclick=render}
  install();
})();
