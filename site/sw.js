const CACHE='command-os-shell-v7';
const SHELL=[
  './','./index.html','./manifest.webmanifest','./icons/command-os.svg','./ui_blueprint.json',
  './app.css','./repository_explorer.css','./internal_editor.css','./workbench_v4.css','./workbench_v5.css','./command_os.css','./command_os_finalize.css','./ultimate_ui.css','./living_info.css','./pwa.css',
  './app.js','./internal_editor.js','./repository_explorer.js','./workbench_v4.js','./workbench_v5.js','./command_os.js','./command_os_search.js','./living_info.js','./ultimate_ui.js','./pwa.js','./vendor/monaco/vs/loader.js'
];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(SHELL))));
self.addEventListener('activate',event=>event.waitUntil(Promise.all([
  caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('command-os-')&&key!==CACHE).map(key=>caches.delete(key)))),
  self.clients.claim()
])));
self.addEventListener('message',event=>{if(event.data?.type==='SKIP_WAITING')self.skipWaiting()});
async function networkFirst(request,fallback){const cache=await caches.open(CACHE);try{const response=await fetch(request);if(response.ok)cache.put(request,response.clone()).catch(()=>{});return response}catch{const cached=await cache.match(request);if(cached)return cached;if(fallback){const shell=await cache.match(fallback);if(shell)return shell}throw new Error('offline')}}
async function shellFirst(request){const cache=await caches.open(CACHE),cached=await cache.match(request);const fresh=fetch(request).then(response=>{if(response.ok)cache.put(request,response.clone()).catch(()=>{});return response}).catch(()=>null);return cached||fresh||Response.error()}
self.addEventListener('fetch',event=>{
  const request=event.request;if(request.method!=='GET')return;
  const url=new URL(request.url);if(url.origin!==self.location.origin)return;
  if(request.mode==='navigate'){event.respondWith(networkFirst(request,'./index.html'));return}
  if(url.pathname.includes('/site-data/')||url.pathname.includes('/repos/')){event.respondWith(networkFirst(request));return}
  event.respondWith(shellFirst(request));
});
