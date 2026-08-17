(()=>{
'use strict';
const escQ=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const active=()=>state.hub?.repositories?.find(r=>r.id===state.repoFilter)||null;
const read=(kind,d=[])=>{try{return JSON.parse(localStorage.getItem(`command-os:${active()?.id}:${kind}`))??d}catch{return d}};
function hit(text,q){return !q||String(text||'').toLowerCase().includes(q)}
function group(title,tone,rows){return `<section class="os-panel ${tone}"><div class="os-panel-title">${title} <span class="search-count">${rows.length}</span></div>${rows.length?rows.slice(0,80).join(''):'<div class="os-empty">No matches.</div>'}</section>`}
async function projectSearch(){
 const r=active();if(!r)return;
 const q=String(state.query||'').trim().toLowerCase();
 document.getElementById('crumb').textContent=`⌂ COMMAND CENTER / ${r.full_name} / SEARCH`;
 document.getElementById('content').innerHTML=`<div class="os-page-head"><div><div class="os-kicker">ACTIVE PROJECT / UNIVERSAL SEARCH</div><h1>Search ${escQ(r.full_name)}</h1><p>Files, docs, project memory and exported repository metadata. Type in the Explorer search field.</p></div></div><div class="syntax-meta"><span class="syn-key">QUERY</span><span class="syn-string">${escQ(state.query||'(all)')}</span><span class="syn-key">COMMIT</span><span class="syn-number">${escQ((r.source_commit||'').slice(0,12))}</span></div><div id="projectSearchResults" class="os-loading">Loading repository snapshot…</div>`;
 try{
  const s=await window.CommandOS.snapshot(r.id),fs=Array.isArray(s?.repository_tree?.files)?s.repository_tree.files:[];
  const fileMatches=fs.filter(f=>hit(f.path,q));
  const docs=fileMatches.filter(f=>/(readme|docs?\/|architecture|agents|contributing|\.md$)/i.test(f.path));
  const code=fileMatches.filter(f=>/\.(py|js|mjs|cjs|ts|tsx|jsx|go|rs|java|c|cpp|h|hpp|cs|rb|php|sol|sh|bash)$/i.test(f.path));
  const tasks=read('tasks').filter(x=>hit(JSON.stringify(x),q));
  const research=read('research').filter(x=>hit(JSON.stringify(x),q));
  const commands=read('commands').filter(x=>hit(JSON.stringify(x),q));
  const notes=localStorage.getItem(`command-os:${r.id}:notes`)||'';
  const hubKinds=['tools','toolsets','cases','opportunities','intelligence','sources','prompts','evidence','activity'];
  const hub=[];for(const kind of hubKinds)for(const x of state.hub[kind]||[])if((x.repo_id===r.id||x.repo_full_name===r.full_name)&&hit(JSON.stringify(x),q))hub.push({kind,x});
  const fileRow=(f,tag)=>`<button class="os-file search-file" data-search-file="${escQ(f.path)}"><span class="file-tag">${tag}</span><b>${escQ(f.path)}</b></button>`;
  const textRow=(label,text)=>`<div class="search-memory-row"><span>${escQ(label)}</span><b>${escQ(text)}</b></div>`;
  document.getElementById('projectSearchResults').className='universal-search-grid';
  document.getElementById('projectSearchResults').innerHTML=
   group('CODE','cyan',code.map(f=>fileRow(f,'code')))+
   group('DOCUMENTATION','purple',docs.map(f=>fileRow(f,'doc')))+
   group('TASKS','yellow',tasks.map(x=>textRow(x.priority||x.status,x.text)))+
   group('RESEARCH','orange',research.map(x=>textRow(x.type,x.text)))+
   group('COMMANDS','pink',commands.map(x=>textRow('command',x.command||x.name)))+
   group('PROJECT METADATA','green',hub.map(v=>textRow(v.kind,v.x.title||v.x.name||v.x.path||v.x.id||JSON.stringify(v.x).slice(0,100))))+
   group('NOTES','blue',notes&&hit(notes,q)?[textRow('local note',q?notes.slice(Math.max(0,notes.toLowerCase().indexOf(q)-80),notes.toLowerCase().indexOf(q)+180):notes.slice(0,240))]:[])+
   `<section class="os-panel red"><div class="os-panel-title">LIVE GITHUB SEARCH</div><p class="ctx-muted">For live Issues, PRs and full code-content search, open GitHub in your existing authenticated browser session.</p><a class="secondary-btn" target="_blank" rel="noopener" href="${safeUrl(`${r.url}/search?q=${encodeURIComponent(state.query||'')}`)}">Search on GitHub ↗</a></section>`;
  const map=new Map(fs.map(f=>[f.path,f]));document.querySelectorAll('[data-search-file]').forEach(b=>b.onclick=()=>{const f=map.get(b.dataset.searchFile);if(f)window.CommandInternalEditor?.open(r.id,f)});
 }catch(e){document.getElementById('projectSearchResults').innerHTML=`<div class="os-empty bad">Search snapshot unavailable: ${escQ(e.message)}</div>`}
}
function install(){if(!window.CommandOS||!state?.hub)return setTimeout(install,80);const core=render;render=function(){if(active()&&state.view==='search'){projectSearch();return}core()};if(active()&&state.view==='search')render();window.CommandOS.search=projectSearch}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
