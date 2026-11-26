import { BRIDGE_PORT } from './bridge_config.mjs';
const $ = (id) => document.getElementById(id);
const autoEl = $('auto'), notifyEl = $('notify'), modeEl = $('domainMode'), conn = $('conn');

async function load() {
  const s = await chrome.storage.local.get('sinaSettings');
  const cfg = { autoPush: true, notify: false, domainMode: 'all', ...(s.sinaSettings || {}) };
  autoEl.checked = cfg.autoPush !== false;
  notifyEl.checked = !!cfg.notify;
  modeEl.value = cfg.domainMode === 'media' ? 'media' : 'all';
}
async function save() {
  const s = await chrome.storage.local.get('sinaSettings');
  await chrome.storage.local.set({ sinaSettings: { ...(s.sinaSettings || {}),
    autoPush: autoEl.checked, notify: notifyEl.checked, domainMode: modeEl.value } });
}
autoEl.addEventListener('change', save);
notifyEl.addEventListener('change', save);
modeEl.addEventListener('change', save);

async function test() {
  conn.textContent = 'Testing…'; conn.className = 'status';
  try {
    const r = await fetch('http://127.0.0.1:' + BRIDGE_PORT + '/ping', { signal: AbortSignal.timeout(3000) });
    const j = await r.json();
    if (j.ok) { conn.textContent = 'Connected: ' + j.app + ' v' + j.version; conn.className = 'status ok'; }
    else throw new Error('bad response');
  } catch (e) { conn.textContent = 'App not reachable. Open SINA Fusion Downloader.'; conn.className = 'status bad'; }
}
$('test').addEventListener('click', test);
$('push').addEventListener('click', async () => { await chrome.runtime.sendMessage({ type: 'push' }); test(); });
load(); test();
