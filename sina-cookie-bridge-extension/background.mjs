import { toNetscape } from './modules/cookie_format.mjs';
import { getAllCookies } from './modules/get_all_cookies.mjs';
import { BRIDGE_PORT, BRIDGE_TOKEN } from './bridge_config.mjs';

const BRIDGE = 'http://127.0.0.1:' + BRIDGE_PORT;
const TICK = 'sina-tick';            // adaptive heartbeat / fast-connect loop
const DEBOUNCE = 'sina-debounce';    // near-real-time push on cookie change
const ONLINE_MS = 30000;             // heartbeat while the app is online
const OFFLINE_MS = 10000;            // fast watch while offline -> catches app launch
const DEBOUNCE_MS = 1500;            // cookie change -> push within ~1.5s

let last = { connected: false, count: 0, lastPush: 0, error: '', domains: [], appVersion: '', pushes: 0 };
let lastText = '';

async function settings() {
  try {
    const s = await chrome.storage.local.get('sinaSettings');
    return { autoPush: true, notify: false, domainMode: 'all', ...(s.sinaSettings || {}) };
  } catch (e) { return { autoPush: true, notify: false, domainMode: 'all' }; }
}

const MEDIA_DOMAINS = ['youtube.com', 'youtu.be', 'google.com', 'instagram.com', 'cdninstagram.com',
  'twitter.com', 'x.com', 'facebook.com', 'fbcdn.net', 'tiktok.com', 'vimeo.com', 'dailymotion.com',
  'twitch.tv', 'reddit.com', 'soundcloud.com', 'bilibili.com', 'nicovideo.jp'];
function filterMedia(cookies) {
  return cookies.filter((c) => {
    const d = (c.domain || '').replace(/^\./, '').toLowerCase();
    return MEDIA_DOMAINS.some((m) => d === m || d.endsWith('.' + m));
  });
}

function topDomains(cookies) {
  const m = {};
  for (const c of cookies) { const d = (c.domain || '').replace(/^\./, ''); m[d] = (m[d] || 0) + 1; }
  return Object.entries(m).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([domain, count]) => ({ domain, count }));
}

function badge(text, color) {
  chrome.action.setBadgeText({ text });
  chrome.action.setBadgeBackgroundColor({ color });
}
async function save() { try { await chrome.storage.local.set({ sinaStatus: last }); } catch (e) {} }
function notify(title, message) {
  try { chrome.notifications.create({ type: 'basic', iconUrl: 'images/icon128.png', title, message }); } catch (e) {}
}
function scheduleTick() {
  chrome.alarms.create(TICK, { when: Date.now() + (last.connected ? ONLINE_MS : OFFLINE_MS) });
}

async function ping() {
  try {
    const r = await fetch(BRIDGE + '/ping', { signal: AbortSignal.timeout(3000) });
    if (!r.ok) return null;
    return await r.json();
  } catch (e) { return null; }
}

async function push(force) {
  const cfg = await settings();
  if (!force && !cfg.autoPush) { scheduleTick(); return last; }
  try {
    let cookies = await getAllCookies();
    if (cfg.domainMode === 'media') cookies = filterMedia(cookies);
    if (!cookies.length) {
      // NEVER push an empty jar - it would wipe the app's good cookies.
      last = { ...last, count: 0, error: 'No cookies available' };
      badge('0', '#64748b'); await save(); scheduleTick(); return last;
    }
    const text = toNetscape(cookies);
    if (!force && text === lastText && last.connected) { scheduleTick(); return last; } // unchanged
    const r = await fetch(BRIDGE + '/cookies', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Bridge-Token': BRIDGE_TOKEN },
      body: JSON.stringify({ netscape: text, count: cookies.length, ts: Date.now() }),
      signal: AbortSignal.timeout(6000),
    });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const wasOffline = !last.connected;
    lastText = text;
    last = { connected: true, count: cookies.length, lastPush: Date.now(), error: '',
             domains: topDomains(cookies), appVersion: last.appVersion, pushes: (last.pushes || 0) + 1 };
    badge(String(cookies.length), '#16a34a');
    if (wasOffline && cfg.notify) notify('Connected to SINA', cookies.length + ' cookies synced.');
  } catch (e) {
    const wasOnline = last.connected;
    last = { ...last, connected: false, error: String((e && e.message) || e) };
    badge('!', '#dc2626');
    if (wasOnline && cfg.notify) notify('SINA app disconnected', 'Reconnecting automatically…');
  }
  await save();
  scheduleTick();
  return last;
}

// Adaptive loop: ping the app; when it appears (e.g. user just launched it) push
// immediately. Alarms are durable across service-worker eviction.
async function tick() {
  const info = await ping();
  if (info && info.ok) {
    last.appVersion = info.version || '';
    await push(false);
  } else {
    if (last.connected) {
      last = { ...last, connected: false, error: 'SINA app is not running' };
      badge('!', '#dc2626'); await save();
    }
    scheduleTick();
  }
}

function ensureContextMenu() {
  chrome.contextMenus.removeAll(() => {
    chrome.contextMenus.create({ id: 'sina-push', title: 'Send cookies to SINA', contexts: ['action'] });
  });
}

async function exportFile() {
  const cookies = await getAllCookies();
  const text = toNetscape(cookies);
  const url = URL.createObjectURL(new Blob([text], { type: 'text/plain' }));
  try { await chrome.downloads.download({ url, filename: 'sina_cookies.txt', saveAs: true }); } catch (e) {}
  return { ok: true, count: cookies.length };
}

chrome.runtime.onInstalled.addListener(() => { ensureContextMenu(); push(true); });
chrome.runtime.onStartup.addListener(() => { ensureContextMenu(); push(true); });
chrome.alarms.onAlarm.addListener((a) => {
  if (a.name === TICK) tick();
  else if (a.name === DEBOUNCE) push(false);
});
chrome.cookies.onChanged.addListener(() => {
  chrome.alarms.create(DEBOUNCE, { when: Date.now() + DEBOUNCE_MS });
});
chrome.contextMenus.onClicked.addListener((i) => { if (i.menuItemId === 'sina-push') push(true); });
chrome.commands.onCommand.addListener((c) => { if (c === 'push-cookies') push(true); });

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === 'push') { push(true).then(sendResponse); return true; }
  if (msg && msg.type === 'status') { sendResponse(last); return true; }
  if (msg && msg.type === 'export') { exportFile().then(sendResponse); return true; }
  return false;
});
