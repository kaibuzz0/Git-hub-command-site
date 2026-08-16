const state={hub:null,view:'home',query:'',repoFilter:''};
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safeUrl=u=>{try{const x=new URL(String(u));return x.protocol==='https:'?x.href:'#'}catch{return'#'}};
const GROUPS=[
  ['Repositories','repositories'],['Tools','tools'],['Toolsets','toolsets'],['Cases','cases'],
  ['Opportunities','opportunities'],['Intelligence','intelligence'],['Sources','sources'],
  ['Prompts','prompts'],['Evidence','evidence'],['Activity','activity']
];
const COLLECTIONS=GROUPS.slice(1).map(x=>x[1]);

async function boot(){
  try{
    state.hub=await fetch('site-data/hub.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw Error(r.status);return r.json()});
    const sync=state.hub.sync?.results||[];
    const errors=sync.filter(x=>x.status==='error').length;
    $('#status').textContent=`${state.hub.counts.repositories} repos • ${new Date(state.hub.generated_at).toLocaleString()}`;
    $('#syncState').textContent=sync.length?`${sync.length} remote • ${errors} errors`:'snapshot registry';
    renderTree(); render(); palette('');
  }catch(e){
    $('#status').textContent='data unavailable';
    $('#content').innerHTML='<h1 class="title">GitHub Command Site</h1><p class="muted">Aggregate repository data has not been deployed yet.</p>';
  }
}

function itemKey(x){return String(x.id||x.full_name||x.url||x.path||x.name||x.title||JSON.stringify(x))}
function labelOf(x){return x.name||x.title||x.full_name||x.id||x.path||'item'}
function repoMatches(x){return !state.repoFilter||x.id===state.repoFilter||x.repo_id===state.repoFilter}
function textMatches(x){const q=state.query.trim().toLowerCase();return !q||JSON.stringify(x).toLowerCase().includes(q)}
function items(kind){return (state.hub?.[kind]||[]).filter(x=>repoMatches(x)&&textMatches(x))}
function filterLabel(){const r=state.hub?.repositories.find(x=>x.id===state.repoFilter);return r?` • ${r.full_name}`:''}

function renderTree(){
  const h=state.hub; if(!h)return;
  let html='<div class="tree-group"><div class="tree-title">Workspace</div>';
  html+=`<div class="tree-item ${!state.repoFilter?'selected':''}" data-repo-filter="">◫ All repositories</div>`;
  for(const r of h.repositories||[])html+=`<div class="tree-item ${state.repoFilter===r.id?'selected':''}" data-repo-filter="${esc(r.id)}">▣ ${esc(r.full_name)}</div>`;
  html+='</div>';
  for(const [label,key] of GROUPS.slice(1)){
    const rows=(h[key]||[]).filter(repoMatches);
    html+=`<div class="tree-group"><div class="tree-title" data-open-view="${key}">${label}<span class="badge">${rows.length}</span></div>`;
    for(const x of rows.slice(0,60))html+=`<div class="tree-item" data-kind="${key}" data-key="${esc(itemKey(x))}">${esc(labelOf(x))}</div>`;
    html+='</div>';
  }
  $('#tree').innerHTML=html;
  document.querySelectorAll('[data-repo-filter]').forEach(el=>el.onclick=()=>{state.repoFilter=el.dataset.repoFilter;renderTree();render()});
  document.querySelectorAll('[data-open-view]').forEach(el=>el.onclick=()=>{state.view=el.dataset.openView;render()});
  document.querySelectorAll('.tree-item[data-kind]').forEach(el=>el.onclick=()=>detail(el.dataset.kind,el.dataset.key));
}

function metricCard(label,value,tone=''){return `<div class="metric ${tone}"><div class="metric-label">${esc(label)}</div><div class="metric-value">${esc(value)}</div></div>`}
function healthCards(h){const x=h.health||{};return `<div class="metrics">${metricCard('Sources due',x.sources_due||0,(x.sources_due||0)?'warn-card':'')}${metricCard('Toolsets attention',x.toolsets_needing_attention||0,(x.toolsets_needing_attention||0)?'warn-card':'')}${metricCard('P1 queue',x.queue_p1||0,(x.queue_p1||0)?'warn-card':'')}${metricCard('Integration inbox',x.integration_items||0,(x.integration_items||0)?'warn-card':'')}${metricCard('Evidence review',x.artifacts_review_before_move||0,(x.artifacts_review_before_move||0)?'warn-card':'')}${metricCard('Known debt',x.known_debt||0,(x.known_debt||0)?'warn-card':'') }</div>`}
function syncPanel(){const rows=state.hub.sync?.results||[];if(!rows.length)return'';return `<section><div class="section-head"><h2>Repository sync</h2><span class="muted">remote snapshot transport</span></div>${rows.map(x=>`<div class="row"><span class="${x.status==='error'?'bad':x.status==='fetched'?'good':'muted'}">●</span> <b>${esc(x.id)}</b> <span class="pill">${esc(x.status)}</span>${x.source_commit?`<span class="muted">${esc(x.source_commit.slice(0,8))}</span>`:''}${x.error?`<div class="bad small">${esc(x.error)}</div>`:''}</div>`).join('')}</section>`}
function repoCard(r){const health=r.health||{};const warnings=Object.values(health).reduce((a,b)=>a+(Number(b)||0),0);return `<div class="card repo-card" data-repo="${esc(r.id)}"><div class="card-top"><b>${esc(r.full_name)}</b><span class="status-dot ${warnings?'warn-dot':'good-dot'}"></span></div><p class="muted">${esc(r.description||'Connected repository')}</p><div><span class="pill">${esc(r.default_branch)}</span><span class="pill">${esc(r.snapshot_origin||'remote')}</span><span class="pill">${esc((r.source_commit||'').slice(0,8))}</span></div><div class="mini-stats"><span>tools ${r.stats?.tools||0}</span><span>cases ${r.stats?.active_cases||0}</span><span>opp ${r.stats?.opportunities||0}</span></div></div>`}
function globalSearch(){const q=state.query.trim();if(!q)return'';const found=[];for(const [label,key] of GROUPS){for(const x of (state.hub[key]||[])){if(repoMatches(x)&&textMatches(x))found.push({label,key,x})}}return `<section><div class="section-head"><h2>Search results</h2><span class="muted">${found.length} matches</span></div>${found.slice(0,40).map(({label,key,x})=>`<div class="row clickable" data-search-kind="${key}" data-search-key="${esc(itemKey(x))}"><b>${esc(labelOf(x))}</b><span class="pill">${esc(label)}</span><div class="muted">${esc(x.repo_full_name||x.url||x.path||'')}</div></div>`).join('')||'<p class="muted">No matches.</p>'}</section>`}

function render(){
  if(!state.hub)return;
  if(state.view==='home')return renderHome();
  if(state.view==='repositories')return renderRepositories();
  return listView(state.view);
}
function renderHome(){
  const h=state.hub,c=h.counts;
  $('#crumb').textContent=`COMMAND / HOME${filterLabel()}`;
  const recent=items('activity').slice(0,8), opp=items('opportunities').slice(0,6);
  $('#content').innerHTML=`<div class="hero"><div><h1 class="title">Multi-Repo Command Center</h1><p class="muted">One static workspace over validated repository snapshots.</p></div><button class="action-btn" id="clearFilter">${state.repoFilter?'Clear repo filter':'All repositories'}</button></div>${globalSearch()}<section><div class="section-head"><h2>Workspace health</h2><span class="muted">aggregated attention signals</span></div>${healthCards(h)}</section><section><div class="section-head"><h2>Repositories</h2><span class="muted">${h.repositories.length} connected</span></div><div class="grid">${h.repositories.filter(repoMatches).map(repoCard).join('')||'<p class="muted">No repositories connected.</p>'}</div></section><div class="two-col"><section><div class="section-head"><h2>Recent activity</h2><span class="muted">latest exported commits/events</span></div>${recent.map(activityRow).join('')||'<p class="muted">No activity exported.</p>'}</section><section><div class="section-head"><h2>Opportunity radar</h2><span class="muted">catalog/discovery records</span></div>${opp.map(x=>itemRow('opportunities',x)).join('')||'<p class="muted">No opportunities exported.</p>'}</section></div>${syncPanel()}`;
  document.querySelectorAll('[data-repo]').forEach(e=>e.onclick=()=>repoView(e.dataset.repo));
  document.querySelectorAll('[data-search-kind]').forEach(e=>e.onclick=()=>detail(e.dataset.searchKind,e.dataset.searchKey));
  document.querySelectorAll('[data-row-kind]').forEach(e=>e.onclick=()=>detail(e.dataset.rowKind,e.dataset.rowKey));
  $('#clearFilter').onclick=()=>{state.repoFilter='';renderTree();render()};
}
function renderRepositories(){
  $('#crumb').textContent=`COMMAND / REPOSITORIES${filterLabel()}`;
  $('#content').innerHTML=`<h1 class="title">Repositories</h1><div class="grid">${state.hub.repositories.filter(repoMatches).map(repoCard).join('')}</div>`;
  document.querySelectorAll('[data-repo]').forEach(e=>e.onclick=()=>repoView(e.dataset.repo));
}
function activityRow(x){return `<div class="row clickable" data-row-kind="activity" data-row-key="${esc(itemKey(x))}"><div><b>${esc(x.title||x.name||x.id)}</b></div><div class="muted">${esc(x.repo_full_name||'')} ${x.timestamp?`• ${esc(new Date(x.timestamp).toLocaleString())}`:''}</div></div>`}
function itemRow(kind,x){return `<div class="row clickable" data-row-kind="${kind}" data-row-key="${esc(itemKey(x))}"><div class="row-main"><b>${esc(labelOf(x))}</b>${statusPills(x)}</div><div class="muted">${esc(x.repo_full_name||x.url||x.path||x.category||'')}</div></div>`}
function statusPills(x){const values=[x.status,x.state,x.maturity,x.health,x.confidence,x.freshness_state].filter(Boolean).slice(0,3);return values.map(v=>`<span class="pill">${esc(v)}</span>`).join('')}
function listView(kind){
  const rows=items(kind);
  $('#crumb').textContent=`COMMAND / ${String(kind).toUpperCase()}${filterLabel()}`;
  $('#content').innerHTML=`<div class="section-head"><h1 class="title">${esc(kind)}</h1><span class="muted">${rows.length} visible</span></div>${rows.map(x=>itemRow(kind,x)).join('')||'<p class="muted">Nothing here yet.</p>'}`;
  document.querySelectorAll('[data-row-kind]').forEach(e=>e.onclick=()=>detail(e.dataset.rowKind,e.dataset.rowKey));
}

function repoView(id){
  const r=state.hub.repositories.find(x=>x.id===id);if(!r)return;
  state.repoFilter=id;renderTree();
  $('#crumb').textContent=`COMMAND / REPOSITORIES / ${r.full_name}`;
  const counts=GROUPS.slice(1).map(([label,key])=>[label,(state.hub[key]||[]).filter(x=>x.repo_id===id).length]);
  const ops=r.agent_ops||{}, priorities=ops.current_state?.priorities||[], handoffs=ops.recent_handoffs||[];
  const links=(r.links||[]).map(x=>`<a class="link-card" href="${safeUrl(x.url)}" target="_blank" rel="noopener">${esc(x.name||x.id||'Open')}</a>`).join('');
  $('#content').innerHTML=`<div class="hero"><div><h1 class="title">${esc(r.full_name)}</h1><p class="muted">${esc(r.description||'')}</p></div><a class="action-btn" href="${safeUrl(r.url)}" target="_blank" rel="noopener">Open GitHub ↗</a></div><div class="link-strip">${links}</div><section><div class="section-head"><h2>Repository health</h2><span class="muted">snapshot ${esc((r.source_commit||'').slice(0,8))} • ${esc(r.snapshot_origin)}</span></div>${healthCards({health:r.health})}</section><section><div class="section-head"><h2>Capabilities</h2><span class="muted">click a collection to filter</span></div><div class="metrics">${counts.map(([label,n])=>`<button class="metric metric-btn" data-repo-section="${label.toLowerCase()}"><span class="metric-label">${esc(label)}</span><span class="metric-value">${n}</span></button>`).join('')}</div></section><div class="two-col"><section><div class="section-head"><h2>Current priorities</h2><span class="muted">Agent Ops</span></div>${priorities.map(p=>`<div class="row">${esc(p)}</div>`).join('')||'<p class="muted">No structured priorities exported.</p>'}</section><section><div class="section-head"><h2>Recent handoffs</h2><span class="muted">${handoffs.length}</span></div>${handoffs.slice(0,5).map(h=>`<div class="row"><b>${esc(h.agent||'agent')}</b> <span class="pill">${esc(h.task||'handoff')}</span><div class="muted">${esc(h.objective||h.next_action||'')}</div></div>`).join('')||'<p class="muted">No handoffs exported.</p>'}</section></div><section><div class="section-head"><h2>Snapshot provenance</h2><span class="muted">generated ${esc(r.generated_at)}</span></div><pre>${esc(JSON.stringify({source_commit:r.source_commit,origin:r.snapshot_origin,stats:r.stats},null,2))}</pre></section>`;
  document.querySelectorAll('[data-repo-section]').forEach(e=>e.onclick=()=>{state.view=e.dataset.repoSection;render()});
}

function relationRows(kind,x){
  const rel=[];
  const caseId=x.related_case||x.case_id||x.case;
  if(caseId){const c=(state.hub.cases||[]).find(v=>v.repo_id===x.repo_id&&(v.id===caseId||v.case_id===caseId));if(c)rel.push(['Case','cases',c])}
  if(x.source_id){const s=(state.hub.sources||[]).find(v=>v.repo_id===x.repo_id&&v.id===x.source_id);if(s)rel.push(['Source','sources',s])}
  if(x.toolset_id){const t=(state.hub.toolsets||[]).find(v=>v.repo_id===x.repo_id&&v.id===x.toolset_id);if(t)rel.push(['Toolset','toolsets',t])}
  return rel;
}
function detail(kind,key){
  const x=(state.hub[kind]||[]).find(v=>itemKey(v)===key&&repoMatches(v))||(state.hub[kind]||[]).find(v=>itemKey(v)===key);if(!x)return;
  $('#crumb').textContent=`COMMAND / ${kind.toUpperCase()} / DETAIL`;
  const links=[];for(const [k,v] of Object.entries(x)){if(typeof v==='string'&&/^https:\/\//.test(v))links.push([k,v])}
  const relations=relationRows(kind,x);
  $('#content').innerHTML=`<div class="hero"><div><h1 class="title">${esc(labelOf(x))}</h1><p class="muted">${esc(x.repo_full_name||'')}</p></div>${x.repo_id?`<button class="action-btn" id="openRepoFromDetail">Repository</button>`:''}</div>${links.length?`<div class="link-strip">${links.map(([k,v])=>`<a class="link-card" href="${safeUrl(v)}" target="_blank" rel="noopener">${esc(k)} ↗</a>`).join('')}</div>`:''}${relations.length?`<section><div class="section-head"><h2>Related</h2></div>${relations.map(([label,k,v])=>`<div class="row clickable" data-related-kind="${k}" data-related-key="${esc(itemKey(v))}"><b>${esc(label)}</b> ${esc(labelOf(v))}</div>`).join('')}</section>`:''}<section><div class="section-head"><h2>Record</h2><span class="muted">validated snapshot data</span></div><pre>${esc(JSON.stringify(x,null,2))}</pre></section>`;
  if($('#openRepoFromDetail'))$('#openRepoFromDetail').onclick=()=>repoView(x.repo_id);
  document.querySelectorAll('[data-related-kind]').forEach(e=>e.onclick=()=>detail(e.dataset.relatedKind,e.dataset.relatedKey));
}

function allCommands(){
  const base=[{label:'Home',run:()=>{state.view='home';render()}},{label:'Clear repository filter',run:()=>{state.repoFilter='';renderTree();render()}},...GROUPS.map(([label,key])=>({label:`Open ${label}`,run:()=>{state.view=key;render()}}))];
  for(const r of state.hub?.repositories||[])base.push({label:`Repository: ${r.full_name}`,run:()=>repoView(r.id)});
  for(const [,kind] of GROUPS.slice(1))for(const x of (state.hub?.[kind]||[]).slice(0,100))base.push({label:`${kind}: ${labelOf(x)}`,run:()=>detail(kind,itemKey(x))});
  return base;
}
function palette(q){if(!state.hub)return;const rows=allCommands().filter(x=>x.label.toLowerCase().includes(q.toLowerCase())).slice(0,30);$('#paletteResults').innerHTML=rows.map((x,i)=>`<div class="palette-result" data-i="${i}">${esc(x.label)}</div>`).join('');document.querySelectorAll('.palette-result').forEach(e=>e.onclick=()=>{rows[+e.dataset.i].run();closePalette()})}
function openPalette(){$('#palette').classList.remove('hidden');$('#paletteInput').value='';palette('');$('#paletteInput').focus()}
function closePalette(){$('#palette').classList.add('hidden')}

document.querySelectorAll('.activity button[data-view]').forEach(b=>b.onclick=()=>{document.querySelectorAll('.activity button').forEach(x=>x.classList.remove('active'));b.classList.add('active');state.view=b.dataset.view;render()});
$('#search').oninput=e=>{state.query=e.target.value;renderTree();render()};
$('#paletteBtn').onclick=openPalette;$('#paletteInput').oninput=e=>palette(e.target.value);$('#palette').onclick=e=>{if(e.target.id==='palette')closePalette()};
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();openPalette()}if(e.key==='Escape')closePalette()});
if('serviceWorker'in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
boot();
