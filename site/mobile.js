(() => {
  const mq=matchMedia('(max-width:760px)');
  const $=s=>document.querySelector(s);
  function mobile(){return mq.matches}
  function closeDrawer(){document.body.classList.remove('mobile-drawer-open')}
  function closeMore(){document.getElementById('mobileMore')?.classList.remove('open')}
  function title(){
    const r=state?.hub?.repositories?.find(x=>x.id===state.repoFilter);
    const strong=document.querySelector('#mobileTitle strong'),small=document.querySelector('#mobileTitle small');
    if(!strong)return;
    if(r){strong.textContent=r.full_name;small.textContent=`${r.default_branch||''} · ${(r.source_commit||'').slice(0,8)}`}
    else{strong.textContent=state?.view==='home'?'Command Center':String(state?.view||'Workbench').replaceAll('-',' ');small.textContent=`${state?.hub?.counts?.repositories||0} public repositories`}
  }
  function active(){
    const map={home:'home',repositories:'repos',search:'search',editor:'editor'};const key=map[state?.view]||'more';
    document.querySelectorAll('#mobileNav [data-mobile]').forEach(b=>b.classList.toggle('active',b.dataset.mobile===key));title();
  }
  function go(view){closeMore();closeDrawer();setView(view);active()}
  function openDrawer(){closeMore();document.body.classList.add('mobile-drawer-open');setTimeout(()=>document.querySelector('.sidebar #search')?.focus(),120)}
  function palette(){closeMore();document.getElementById('palette')?.classList.remove('hidden');setTimeout(()=>document.getElementById('paletteInput')?.focus(),30)}
  function more(){closeDrawer();document.getElementById('mobileMore')?.classList.toggle('open')}
  function install(){
    document.getElementById('wbMobileTop')?.remove();document.getElementById('wbMobileShade')?.remove();document.getElementById('wbMobileFab')?.remove();
    const top=document.createElement('div');top.className='mobile-top';top.innerHTML='<button id="mobileMenu" aria-label="Open repositories">☰</button><div id="mobileTitle" class="mobile-title"><strong>Command Center</strong><small>loading…</small></div><button id="mobileRefresh" aria-label="Refresh workspace">↻</button><button id="mobilePalette" aria-label="Command palette">⌕</button>';document.body.append(top);
    const shade=document.createElement('button');shade.className='mobile-shade';shade.setAttribute('aria-label','Close repositories');shade.onclick=closeDrawer;document.body.append(shade);
    const nav=document.createElement('nav');nav.id='mobileNav';nav.className='mobile-nav';nav.innerHTML='<button data-mobile="home"><b>⌂</b><span>Home</span></button><button data-mobile="repos"><b>▱</b><span>Repos</span></button><button data-mobile="search"><b>⌕</b><span>Search</span></button><button data-mobile="editor"><b>▤</b><span>Editor</span></button><button data-mobile="more"><b>•••</b><span>More</span></button>';document.body.append(nav);
    const sheet=document.createElement('section');sheet.id='mobileMore';sheet.className='mobile-more';sheet.innerHTML='<h3>Workspace tools</h3><div class="mobile-more-grid"><button data-view="source-control">⑂ Source control</button><button data-view="run-debug">▷ Run & debug</button><button data-view="workspace-tools">⬡ Tools</button><button data-special="whiteboard">✎ Whiteboard</button><button data-view="settings">⚙ Settings</button><button data-special="layouts">▦ Layouts</button></div>';document.body.append(sheet);
    $('#mobileMenu').onclick=openDrawer;$('#mobilePalette').onclick=palette;$('#mobileRefresh').onclick=()=>location.reload();
    nav.querySelector('[data-mobile="home"]').onclick=()=>go('home');nav.querySelector('[data-mobile="repos"]').onclick=()=>go('repositories');nav.querySelector('[data-mobile="search"]').onclick=()=>{go('search');setTimeout(()=>document.querySelector('.sidebar #search')?.focus(),50)};nav.querySelector('[data-mobile="editor"]').onclick=()=>go('editor');nav.querySelector('[data-mobile="more"]').onclick=more;
    sheet.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>go(b.dataset.view));sheet.querySelector('[data-special="whiteboard"]').onclick=()=>{closeMore();CommandWorkbenchV4?.renderWhiteboard?.();active()};sheet.querySelector('[data-special="layouts"]').onclick=()=>{closeMore();CommandWorkbenchV5?.renderLayouts?.();active()};
    document.querySelector('.sidebar')?.addEventListener('click',e=>{if(e.target.closest('.tree-item,.tree-title'))setTimeout(()=>{closeDrawer();title()},80)});
    const originalSetView=window.setView;if(typeof originalSetView==='function')window.setView=function(v){const x=originalSetView(v);setTimeout(active,0);return x};
    const originalRepo=window.repoView;if(typeof originalRepo==='function')window.repoView=async function(id){closeDrawer();closeMore();const x=await originalRepo(id);setTimeout(active,0);return x};
    document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDrawer();closeMore()}});
    mq.addEventListener?.('change',()=>{closeDrawer();closeMore()});
    active();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>setTimeout(install,80));else setTimeout(install,80);
})();
