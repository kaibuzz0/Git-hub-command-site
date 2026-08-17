(() => {
  const repoCache = new Map();

  function encodePath(path) {
    return String(path || '').split('/').map(encodeURIComponent).join('/');
  }

  function makeNode() {
    return {dirs: new Map(), files: []};
  }

  function ensureDirectory(root, path) {
    let node = root;
    for (const part of String(path || '').split('/').filter(Boolean)) {
      if (!node.dirs.has(part)) node.dirs.set(part, makeNode());
      node = node.dirs.get(part);
    }
    return node;
  }

  function buildTree(inventory) {
    const root = makeNode();
    for (const item of inventory?.directories || []) ensureDirectory(root, item.path);
    for (const file of inventory?.files || []) {
      const parts = String(file.path || '').split('/').filter(Boolean);
      const name = parts.pop();
      const parent = ensureDirectory(root, parts.join('/'));
      parent.files.push({...file, name: file.name || name});
    }
    return root;
  }

  function fileUrl(repo, path) {
    const ref = repo.source_commit || repo.default_branch;
    return `https://github.com/${repo.full_name}/blob/${encodeURIComponent(ref)}/${encodePath(path)}`;
  }

  function renderNode(node, repo, depth = 0, prefix = '') {
    const dirs = [...node.dirs.entries()].sort((a,b) => a[0].localeCompare(b[0]));
    const files = [...node.files].sort((a,b) => String(a.name).localeCompare(String(b.name)));
    let html = '';
    for (const [name, child] of dirs) {
      const path = prefix ? `${prefix}/${name}` : name;
      html += `<details class="repo-folder" ${depth === 0 ? 'open' : ''}><summary><span class="folder-icon">▾</span> ${esc(name)}</summary><div class="repo-folder-children">${renderNode(child, repo, depth + 1, path)}</div></details>`;
    }
    for (const file of files) {
      html += `<a class="repo-file" target="_blank" rel="noopener" href="${safeUrl(fileUrl(repo, file.path))}" title="${esc(file.path)}"><span class="file-icon">${esc(file.extension || '·')}</span><span>${esc(file.name)}</span></a>`;
    }
    return html;
  }

  async function loadSnapshot(id) {
    if (repoCache.has(id)) return repoCache.get(id);
    const request = fetch(`site-data/repo-${encodeURIComponent(id)}.json`, {cache:'no-store'})
      .then(r => { if (!r.ok) throw new Error(`snapshot ${r.status}`); return r.json(); });
    repoCache.set(id, request);
    return request;
  }

  async function enhancedRepoView(id) {
    const repo = state.hub.repositories.find(x => x.id === id);
    if (!repo) return;
    state.repoFilter = id;
    renderTree();
    $('#crumb').textContent = `WORKBENCH / REPOSITORIES / ${repo.full_name}`;
    $('#content').innerHTML = `<div class="hero"><div><h1 class="title">${esc(repo.full_name)}</h1><p class="muted">${esc(repo.description || 'Connected repository')}</p></div><div class="button-row"><a class="action-btn" target="_blank" rel="noopener" href="${safeUrl(repo.url)}">GitHub</a><a class="secondary-btn" target="_blank" rel="noopener" href="${safeUrl('https://vscode.dev/github/'+repo.full_name)}">VS Code for Web</a></div></div>${healthCards({health:repo.health})}<div class="section-head"><h2>Repository Explorer</h2><span class="muted">loading snapshot…</span></div><div id="repoExplorer" class="repo-explorer"><div class="empty-state">Loading repository tree…</div></div><div class="section-head"><h2>Snapshot</h2></div><pre>${esc(JSON.stringify({generated_at:repo.generated_at,source_commit:repo.source_commit,origin:repo.snapshot_origin,health:repo.health},null,2))}</pre>`;

    try {
      const snapshot = await loadSnapshot(id);
      const inventory = snapshot.repository_tree;
      const host = $('#repoExplorer');
      if (!host) return;
      if (!inventory) {
        host.innerHTML = '<div class="empty-state">This repository is connected with an older snapshot that does not include file-tree data yet.</div>';
        return;
      }
      const tree = buildTree(inventory);
      const truncation = inventory.files_truncated || inventory.directories_truncated;
      const summary = `${inventory.total_files ?? 0} files • ${inventory.total_directories ?? 0} folders${truncation ? ' • bounded snapshot' : ''}`;
      const heading = host.previousElementSibling?.querySelector('.muted');
      if (heading) heading.textContent = summary;
      host.innerHTML = `${truncation ? '<div class="repo-tree-notice">Large repository: the complete folder summary is retained where possible, while individual file entries are bounded to keep snapshots safe and fast.</div>' : ''}${renderNode(tree, repo) || '<div class="empty-state">No tracked files in this snapshot.</div>'}`;
    } catch (error) {
      const host = $('#repoExplorer');
      if (host) host.innerHTML = `<div class="empty-state bad">Could not load repository snapshot: ${esc(error.message)}</div>`;
    }
  }

  // Replace the base repository detail view while leaving every other workbench
  // surface untouched. Repo cards and palette commands already call repoView().
  repoView = enhancedRepoView;
})();
