(() => {
  const snap=()=>window.repoSnapshot||{};
  const repo=()=>snap().repo||{};
  const tree=()=>snap().repository_tree||{};
  const files=()=>Array.isArray(tree().files)?tree().files:[];
  const stats=()=>snap().stats||{};
  const activity=()=>Array.isArray(snap().activity)?snap().activity:[];
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const basename=p=>String(p||'').split('/').pop();
  const ext=p=>{const n=basename(p);return n.includes('.')?n.slice(n.lastIndexOf('.')).toLowerCase():''};
  const codeExt=new Set(['.py','.js','.mjs','.cjs','.ts','.tsx','.jsx','.go','.rs','.java','.c','.cc','.cpp','.h','.hpp','.cs','.rb','.php','.sol','.sh','.bash']);
  function classify(){
    const list=files(), names=new Map(), dirs=new Map(), tests=list.filter(f=>/(^|\/)(tests?|specs?)\/|(^|\/)(test_|.*_test\.)/i.test(f.path));
    for(const f of list){const n=basename(f.path).toLowerCase();if(n)names.set(n,(names.get(n)||0)+1);const top=String(f.path).split('/')[0];dirs.set(top,(dirs.get(top)||0)+1)}
    const duplicateNames=[...names.entries()].filter(([,n])=>n>1).sort((a,b)=>b[1]-a[1]).slice(0,20);
    const source=list.filter(f=>codeExt.has(ext(f.path))&&!/(^|\/)(tests?|specs?)\//i.test(f.path));
    const sourceWithoutNearbyTests=source.filter(f=>{const base=basename(f.path).replace(/\.[^.]+$/,'').toLowerCase();return !tests.some(t=>basename(t.path).toLowerCase().includes(base))}).slice(0,40);
    const bigDirs=[...dirs.entries()].sort((a,b)=>b[1]-a[1]).slice(0,12);
    const workflowCount=Number(stats().workflow_files||0), testCount=Number(stats().test_files||tests.length||0), sourceCount=source.length;
    let score=100, notes=[];
    if(!workflowCount){score-=15;notes.push('No GitHub Actions workflow detected in snapshot.')}
    if(sourceCount>10&&!testCount){score-=20;notes.push('Code files detected but no test files were identified.')}
    if(sourceWithoutNearbyTests.length>20){score-=10;notes.push('Many source files have no obvious similarly named test file.')}
    if(duplicateNames.length>10){score-=8;notes.push('Many repeated basenames may deserve a duplication/reuse review.')}
    if(tree().files_truncated||tree().directories_truncated){score-=5;notes.push('Repository inventory is truncated; diagnostics are partial.')}
    const recent=activity()[0]?.timestamp?Date.parse(activity()[0].timestamp):NaN;
    if(Number.isFinite(recent)){const days=(Date.now()-recent)/86400000;if(days>180){score-=12;notes.push(`Latest exported activity is about ${Math.round(days)} days old.`)}else if(days>60){score-=6;notes.push(`Latest exported activity is about ${Math.round(days)} days old.`)}}
    score=Math.max(0,Math.min(100,score));
    return {score,notes,duplicateNames,sourceWithoutNearbyTests,bigDirs,workflowCount,testCount,sourceCount};
  }
  function healthView(){
    const d=classify(), tone=d.score>=85?'good':d.score>=65?'warn':'bad';
    const dup=d.duplicateNames.map(([name,count])=>`<div class="diag-row"><b>${esc(name)}</b><span>${count} files share this basename</span></div>`).join('');
    const gaps=d.sourceWithoutNearbyTests.slice(0,18).map(f=>`<div class="diag-row"><b>${esc(f.path)}</b><span>no obvious similarly named test in bounded snapshot</span></div>`).join('');
    const dirs=d.bigDirs.map(([name,count])=>`<div class="diag-row"><b>${esc(name)}</b><span>${count} tracked files</span></div>`).join('');
    window.repoWorkspaceRender('health.json','♥','health',`<div class="repo-console-head"><div><div class="kicker">REPOSITORY DIAGNOSTICS</div><h1>Health & attention</h1><p class="muted">Transparent heuristics from the bounded public snapshot. These are review signals, not proof of defects.</p></div><div class="diag-score ${tone}"><strong>${d.score}</strong><span>/100</span></div></div><div class="diag-metrics"><div><b>${d.sourceCount}</b><span>code files</span></div><div><b>${d.testCount}</b><span>test files</span></div><div><b>${d.workflowCount}</b><span>workflows</span></div><div><b>${d.duplicateNames.length}</b><span>repeated names</span></div></div><div class="section-caption">ATTENTION SUMMARY</div><div class="diag-notes">${d.notes.length?d.notes.map(n=>`<div>• ${esc(n)}</div>`).join(''):'<div>• No major heuristic warnings from the current bounded snapshot.</div>'}</div><div class="section-caption">LARGEST TOP-LEVEL AREAS</div><div class="diag-list">${dirs||'<div class="empty">No structure data.</div>'}</div><div class="section-caption">REPEATED BASENAMES</div><div class="diag-list">${dup||'<div class="empty">No repeated basenames detected.</div>'}</div><div class="section-caption">POSSIBLE TEST GAPS</div><div class="diag-list">${gaps||'<div class="empty">No obvious test gaps detected by filename heuristic.</div>'}</div>`);
  }
  function install(){if(!window.repoWorkspaceRender||!window.repoSnapshot)return setTimeout(install,60);const nav=document.getElementById('workspaceNav');if(!nav||document.getElementById('repoDiagnosticsNav'))return;const box=document.createElement('div');box.id='repoDiagnosticsNav';box.className='tree-section';box.innerHTML='<div class="tree-caption">DIAGNOSTICS</div><button class="tree-item" data-diagnostic="health">♥ <span>Health / attention</span></button>';nav.append(box);box.querySelector('[data-diagnostic="health"]').onclick=healthView}
  install();
})();
