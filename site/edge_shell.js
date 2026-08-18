(()=>{
'use strict';
const LABELS={home:'Command Center',repositories:'Repositories',search:'Search','source-control':'Source Control','run-debug':'Run / Debug',editor:'Editor','workspace-tools':'Tools',whiteboard:'Whiteboard',settings:'Settings'};
const TOP=[['project-overview','⌂','Overview','cyan'],['project-intelligence','◈','Intelligence','purple'],['project-files','▱','Files','blue'],['project-code','</>','Code','pink'],['project-tests','✓','Tests / CI','green'],['project-tasks','☑','Tasks','yellow'],['project-agents','🤖','Agents','purple'],['project-research','◇','Research','orange'],['project-notes','✎','Notes','cyan'],['project-history','◷','History','blue']];
const BOTTOM=[['search','⌕','Search','cyan'],['editor','▤','Editor','pink'],['run-debug','▷','Run / Debug','green'],['source-control','⑂','Git / PRs','blue'],['workspace-tools','⬡','Tools','purple'],['whiteboard','✎','Whiteboard','orange'],['panel','≡','Output','yellow'],['palette','›_','Palette','cyan']];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function repo(){return state?.hub?.repositories?.find(r=>r.id===state.repoFilter)||null}
function clickView(v){const b=document.querySelector(`.activity button[data-view="${v}"]`);b?.click()}
function clickProject(v){const b=document.querySelector(`[data-project-view="${v}"]`);if(b)b.click();else{state.view=v;renderTree();render()}}
function clickRepo(id){const b=[...document.querySelectorAll('[data-repo-filter]')].find(x=>x.dataset.repoFilter===id);if(b)b.click();else{state.repoFilter=id;state.view='project-overview';localStorage.setItem('command-os-active-repo',id);renderTree();render()}}
function labelActivity(){document.querySelectorAll('.activity button').forEach(b=>{if(b.querySelector('.edge-label'))return;const v=b.dataset.view;const title=LABELS[v]||b.title||'Command';const glyph=[...b.childNodes].find(n=>n.nodeType===Node.TEXT_NODE)?.textContent?.trim()||b.textContent.trim();b.textContent='';const icon=document.createElement('span');icon.textContent=glyph;icon.className='edge-icon';const label=document.createElement('span');label.className='edge-label';label.textContent=title;b.append(icon,label)})}
function installShell(){if(document.getElementById('edgeTop'))return;document.body.classList.add('edge-shell-ready');labelActivity();const app=document.getElementById('app');
 const top=document.createElement('nav');top.id='edgeTop';top.className='edge-top';top.setAttribute('aria-label','Project command bar');
 const right=document.createElement('aside');right.id='edgeRight';right.className='edge-right';right.innerHTML='<div class="edge-right-head">REPOSITORIES <span class="edge-spacer"></span><button class="edge-btn purple" id="edgeReposOpen">ALL</button></div><div class="edge-right-list" id="edgeRepoList"></div>';
 const bottom=document.createElement('nav');bottom.id='edgeBottom';bottom.className='edge-bottom';bottom.setAttribute('aria-label','Tool command bar');
 app.append(top,right,bottom);renderShell();
 right.querySelector('#edgeReposOpen').onclick=()=>clickView('repositories');
 BOTTOM.forEach(([v,i,l,c])=>{const b=document.createElement('button');b.className=`edge-btn ${c}`;b.dataset.edgeView=v;b.innerHTML=`<span>${i}</span>${l}`;b.onclick=()=>{if(v==='panel'){document.getElementById('bottomPanel')?.classList.toggle('hidden');return}if(v==='palette'){document.getElementById('paletteBtn')?.click();return}clickView(v)};bottom.append(b)});
 const mo=new MutationObserver(()=>renderShell());mo.observe(document.getElementById('tree'),{childList:true,subtree:true,attributes:true});mo.observe(document.getElementById('content'),{childList:true,subtree:false});
 window.addEventListener('storage',renderShell);document.addEventListener('click',e=>{if(e.target.closest('[data-repo-filter],[data-project-view],.activity button[data-view]'))setTimeout(renderShell,0)},true)
}
function renderShell(){const top=document.getElementById('edgeTop'),list=document.getElementById('edgeRepoList');if(!top||!list)return;const r=repo();top.innerHTML=`<button class="edge-btn cyan" data-edge-global>⌂ Fleet</button>${r?`<span class="edge-btn purple active">${esc(r.full_name)}</span>`:''}${r?TOP.map(([v,i,l,c])=>`<button class="edge-btn ${c} ${state.view===v?'active':''}" data-edge-project="${v}"><span>${i}</span>${l}</button>`).join(''):'<span class="edge-btn blue active">Select a repository to enter project mode</span>'}`;top.querySelector('[data-edge-global]').onclick=()=>{const home=document.querySelector('[data-global-home]');if(home)home.click();else clickView('home')};top.querySelectorAll('[data-edge-project]').forEach(b=>b.onclick=()=>clickProject(b.dataset.edgeProject));
 const repos=state?.hub?.repositories||[];list.innerHTML=repos.map(x=>`<button class="edge-repo ${x.id===state.repoFilter?'active':''}" data-edge-repo="${esc(x.id)}"><i></i><span>${esc(x.full_name)}</span></button>`).join('');list.querySelectorAll('[data-edge-repo]').forEach(b=>b.onclick=()=>clickRepo(b.dataset.edgeRepo));
 document.querySelectorAll('#edgeBottom [data-edge-view]').forEach(b=>b.classList.toggle('active',b.dataset.edgeView===state.view));labelActivity()
}
function boot(){if(typeof state==='undefined'||!document.getElementById('app'))return setTimeout(boot,60);installShell()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});else boot();
})();
