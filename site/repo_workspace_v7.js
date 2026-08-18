(()=>{
'use strict';
function trigger(selector){document.querySelector(selector)?.click()}
function install(){if(document.getElementById('r7Topbar'))return;if(!document.getElementById('workspaceNav'))return setTimeout(install,60);const editor=document.querySelector('.editor'),toolbar=document.querySelector('.toolbar');if(!editor||!toolbar)return;
 const top=document.createElement('nav');top.id='r7Topbar';top.className='r7-topbar';top.setAttribute('aria-label','Repository workspace shortcuts');toolbar.insertAdjacentElement('afterend',top);
 const quick=document.createElement('nav');quick.className='r7-quick';quick.setAttribute('aria-label','Repository quick actions');quick.innerHTML='<button data-q="menu" title="Explorer">☰</button><button data-q="home" title="Overview">⌂</button><button data-q="files" title="Repository files">▱</button><button data-q="center" title="Command Center">◈</button>';document.body.append(quick);
 quick.querySelector('[data-q="menu"]').onclick=()=>document.getElementById('sidebar')?.classList.toggle('open');quick.querySelector('[data-q="home"]').onclick=()=>document.querySelector('#workspaceNav button')?.click();quick.querySelector('[data-q="files"]').onclick=()=>{const fileBtn=[...document.querySelectorAll('#workspaceNav button')].find(b=>/files|explorer|repository/i.test(b.textContent));if(fileBtn)fileBtn.click();else document.querySelector('#tree .tree-folder,#tree .tree-item')?.click()};quick.querySelector('[data-q="center"]').onclick=()=>location.href='https://kaibuzz0.github.io/Git-hub-command-site/';
 function rebuild(){const buttons=[...document.querySelectorAll('#workspaceNav button')].filter(b=>b.offsetParent!==null||b.textContent.trim());top.innerHTML='';buttons.slice(0,18).forEach((src,i)=>{const b=document.createElement('button');b.textContent=src.textContent.trim().replace(/\s+/g,' ');b.title=b.textContent;b.onclick=()=>src.click();top.append(b)});if(!buttons.length){const b=document.createElement('button');b.textContent='Overview';b.onclick=()=>document.querySelector('#activity .activity')?.click();top.append(b)}}
 rebuild();new MutationObserver(rebuild).observe(document.getElementById('workspaceNav'),{childList:true,subtree:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});else install();
})();
