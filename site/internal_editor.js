(() => {
  const TEXT_EXTENSIONS = new Set(['.py','.js','.mjs','.cjs','.ts','.tsx','.jsx','.json','.md','.txt','.text','.yml','.yaml','.toml','.ini','.cfg','.conf','.sh','.bash','.zsh','.fish','.ps1','.bat','.cmd','.html','.htm','.css','.scss','.less','.xml','.svg','.sql','.rs','.go','.java','.c','.h','.cpp','.hpp','.cc','.cs','.rb','.php','.lua','.pl','.r','.dart','.kt','.kts','.swift','.sol','.pine']);
  const MAX_FILE_BYTES = 512 * 1024;
  let monacoPromise = null;
  let editor = null;

  const mobileLike = () => matchMedia('(max-width: 760px), (pointer: coarse)').matches;
  const encodePath = path => String(path || '').split('/').map(encodeURIComponent).join('/');
  const rawUrl = (repo, path) => `https://raw.githubusercontent.com/${repo.full_name}/${encodeURIComponent(repo.source_commit || repo.default_branch)}/${encodePath(path)}`;
  const githubUrl = (repo, path) => `https://github.com/${repo.full_name}/blob/${encodeURIComponent(repo.source_commit || repo.default_branch)}/${encodePath(path)}`;
  const languageFor = path => ({py:'python',js:'javascript',mjs:'javascript',cjs:'javascript',ts:'typescript',tsx:'typescript',jsx:'javascript',json:'json',md:'markdown',yml:'yaml',yaml:'yaml',html:'html',htm:'html',css:'css',scss:'scss',less:'less',xml:'xml',sql:'sql',rs:'rust',go:'go',java:'java',c:'c',h:'c',cpp:'cpp',hpp:'cpp',cc:'cpp',cs:'csharp',rb:'ruby',php:'php',lua:'lua',r:'r',dart:'dart',kt:'kotlin',kts:'kotlin',swift:'swift',sol:'sol',sh:'shell',bash:'shell',zsh:'shell',ps1:'powershell'})[String(path).split('.').pop().toLowerCase()] || 'plaintext';

  function canPreview(file) {
    const name = String(file?.name || file?.path || '').toLowerCase();
    const ext = name.includes('.') ? `.${name.split('.').pop()}` : '';
    return TEXT_EXTENSIONS.has(ext) || ['readme','license','dockerfile','makefile'].some(x => name.endsWith(x));
  }

  function ensureMonaco() {
    if (window.monaco) return Promise.resolve(window.monaco);
    if (monacoPromise) return monacoPromise;
    monacoPromise = new Promise((resolve, reject) => {
      if (!window.require) return reject(new Error('Monaco loader unavailable'));
      window.require.config({paths:{vs:'vendor/monaco/vs'}});
      window.require(['vs/editor/editor.main'], () => resolve(window.monaco), reject);
    });
    return monacoPromise;
  }

  function renderShell(repo, file) {
    $('#crumb').textContent = `WORKBENCH / ${repo.full_name} / ${file.path}`;
    $('#content').innerHTML = `<div class="internal-editor-shell"><div class="internal-editor-tabs"><div class="internal-editor-tab active">${esc(file.name || file.path)}</div><div class="internal-editor-actions"><span class="muted small">${esc((repo.source_commit || '').slice(0,10))}</span><a class="secondary-btn" target="_blank" rel="noopener" href="${safeUrl(githubUrl(repo,file.path))}">GitHub</a><a class="secondary-btn" target="_blank" rel="noopener" href="${safeUrl('https://vscode.dev/github/'+repo.full_name)}">Full VS Code</a></div></div><div id="internalEditorHost" class="internal-editor-host"><div class="empty-state">Loading ${esc(file.path)}…</div></div><div class="internal-editor-status"><span>${esc(file.path)}</span><span>read-only • exact snapshot commit</span></div></div>`;
  }

  async function fetchText(repo, file) {
    const response = await fetch(rawUrl(repo,file.path), {cache:'no-store'});
    if (!response.ok) throw new Error(`file fetch ${response.status}`);
    const length = Number(response.headers.get('content-length') || 0);
    if (length && length > MAX_FILE_BYTES) throw new Error(`file exceeds ${Math.round(MAX_FILE_BYTES/1024)} KB preview limit`);
    const text = await response.text();
    if (new Blob([text]).size > MAX_FILE_BYTES) throw new Error(`file exceeds ${Math.round(MAX_FILE_BYTES/1024)} KB preview limit`);
    return text;
  }

  function fallback(host, text, file) {
    host.innerHTML = `<textarea class="mobile-code-viewer" readonly spellcheck="false" aria-label="${esc(file.path)}"></textarea>`;
    host.querySelector('textarea').value = text;
  }

  async function open(repoId, file) {
    const repo = state.hub.repositories.find(r => r.id === repoId);
    if (!repo || !file?.path) return;
    if (!canPreview(file)) {
      showOutput(`Inline preview is disabled for ${file.path}. Open it on GitHub instead.`);
      window.open(githubUrl(repo,file.path), '_blank', 'noopener');
      return;
    }
    renderShell(repo,file);
    const host = $('#internalEditorHost');
    try {
      const text = await fetchText(repo,file);
      if (mobileLike()) return fallback(host,text,file);
      try {
        const monaco = await ensureMonaco();
        host.innerHTML = '';
        if (editor) editor.dispose();
        editor = monaco.editor.create(host,{value:text,language:languageFor(file.path),theme:'vs-dark',readOnly:true,automaticLayout:true,minimap:{enabled:true},fontSize:13,scrollBeyondLastLine:false,wordWrap:'off'});
      } catch {
        fallback(host,text,file);
      }
    } catch (error) {
      host.innerHTML = `<div class="empty-state bad">Could not preview file: ${esc(error.message)}</div>`;
    }
  }

  window.CommandInternalEditor = {open, canPreview};
})();
