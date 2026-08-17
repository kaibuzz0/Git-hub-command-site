(()=>{
'use strict';
let installPrompt=null;
const standalone=()=>matchMedia('(display-mode: standalone)').matches||navigator.standalone===true;
function controls(){let box=document.getElementById('pwaControls');if(box)return box;box=document.createElement('div');box.id='pwaControls';box.className='pwa-controls';box.innerHTML='<button id="pwaInstall" class="pwa-btn" hidden>Install App</button><button id="pwaUpdate" class="pwa-btn update" hidden>Update App</button><span id="pwaStatus" class="pwa-status" hidden></span>';document.body.append(box);return box}
function status(text,kind=''){controls();const el=document.getElementById('pwaStatus');el.textContent=text;el.className='pwa-status '+kind;el.hidden=!text}
function onlineState(){status(navigator.onLine?(standalone()?'APP · ONLINE':'ONLINE'):'OFFLINE',navigator.onLine?'':'offline');setTimeout(()=>{const el=document.getElementById('pwaStatus');if(el&&navigator.onLine)el.hidden=true},1800)}
function showUpdate(reg){const b=document.getElementById('pwaUpdate');b.hidden=false;b.onclick=()=>{if(reg.waiting)reg.waiting.postMessage({type:'SKIP_WAITING'});b.disabled=true;b.textContent='Updating…'}}
async function register(){controls();if(!('serviceWorker' in navigator)){status('PWA unsupported','offline');return}try{const reg=await navigator.serviceWorker.register('./sw.js',{scope:'./'});if(reg.waiting)showUpdate(reg);reg.addEventListener('updatefound',()=>{const w=reg.installing;if(!w)return;w.addEventListener('statechange',()=>{if(w.state==='installed'&&navigator.serviceWorker.controller)showUpdate(reg)})});navigator.serviceWorker.addEventListener('controllerchange',()=>location.reload());setInterval(()=>reg.update().catch(()=>{}),15*60*1000)}catch(e){console.warn('PWA registration failed',e);status('PWA registration failed','offline')}}
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;controls();const b=document.getElementById('pwaInstall');b.hidden=false;b.onclick=async()=>{if(!installPrompt)return;installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;b.hidden=true}});
window.addEventListener('appinstalled',()=>{installPrompt=null;const b=document.getElementById('pwaInstall');if(b)b.hidden=true;status('APP INSTALLED')});
window.addEventListener('online',onlineState);window.addEventListener('offline',onlineState);
function boot(){controls();if(standalone())document.documentElement.classList.add('pwa-standalone');onlineState();register()}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
