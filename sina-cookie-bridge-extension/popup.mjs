import { BRIDGE_PORT } from './bridge_config.mjs';
const $ = (id) => document.getElementById(id);
const statusEl = $('status'), dot = $('dot'), countEl = $('count'), lastEl = $('last');
const pushesEl = $('pushes'), domainsEl = $('domains'), pushBtn = $('push'), autoEl = $('auto'), verEl = $('ver');

function render(s) {
  const ok = !!(s && s.connected);
  dot.className = 'dot ' + (ok ? 'ok' : 'bad');
  statusEl.textContent = ok ? 'Connected to SINA app' : 'Waiting for SINA app…';
  statusEl.className = 'status ' + (ok ? 'ok' : 'bad');
  countEl.textContent = (s && s.count) || 0;
  pushesEl.textContent = (s && s.pushes) || 0;
  lastEl.textContent = (s && s.lastPush) ? new Date(s.lastPush).toLocaleTimeString() : '—';
  verEl.textContent = (s && s.appVersion) ? 'SINA app v' + s.appVersion : 'Real-time local sync';
  domainsEl.replaceChildren(...((s && s.domains) || []).map((d) => {
    const el = document.createElement('div');
    el.className = 'domain';
    el.textContent = d.domain + ' · ' + d.count;
    return el;
  }));
  statusEl.title = (!ok && s && s.error) ? s.error : '';
}

async function refresh() {
  const stored = await chrome.storage.local.get(['sinaStatus', 'sinaSettings']);
  autoEl.checked = (stored.sinaSettings || { autoPush: true }).autoPush !== false;
  render(stored.sinaStatus || { connected: false, count: 0 });
}

pushBtn.addEventListener('click', async () => {
  pushBtn.disabled = true; pushBtn.textContent = 'Pushing…';
  const s = await chrome.runtime.sendMessage({ type: 'push' });
  render(s);
  pushBtn.disabled = false; pushBtn.textContent = 'Push cookies now';
});

$('export').addEventListener('click', async () => {
  await chrome.runtime.sendMessage({ type: 'export' });
});

autoEl.addEventListener('change', async () => {
  const stored = await chrome.storage.local.get('sinaSettings');
  await chrome.storage.local.set({ sinaSettings: { ...(stored.sinaSettings || {}), autoPush: autoEl.checked } });
});

$('options').addEventListener('click', (e) => { e.preventDefault(); chrome.runtime.openOptionsPage(); });

refresh();
setInterval(refresh, 2000);   // live updates while the popup is open
