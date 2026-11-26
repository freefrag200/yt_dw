
# -*- coding: utf-8 -*-
"""
SINA Fusion Downloader v18.5.0 (Pro Edition, Pure tkinter)
==========================================================
Modernized & hardened release. Highlights over v17.5:

ARCHITECTURE CHANGES (requested)
  * CustomTkinter REMOVED entirely. The UI is now 100% standard-library
    tkinter + ttk with a hand-crafted flat dark/light theme. Only mandatory
    third-party deps: yt-dlp, Pillow, requests.
  * Automatic queue-state persistence REMOVED: the app no longer creates
    sina_enterprise_queue_v15.json (or any queue file). Manual Export/Import
    of the queue to a user-chosen file is still available.
  * Cookies are now obtained CORRECTLY:
      - New BrowserCookieExtractor reads Chromium (Chrome/Edge/Brave/Opera/
        Vivaldi) and Firefox cookie databases directly, decrypts Chrome
        v10/v11 values with DPAPI + AES-256-GCM, and writes a proper Netscape
        cookies.txt. Works even while the browser is running (safe SQLite
        copy), which fixes the classic "could not copy chrome cookie
        database" / DPAPI lock failures.
      - 'auto' cookie mode now really is automatic: user cookies.txt ->
        live browser extraction -> yt-dlp cookiesfrombrowser fallback.
      - On auth errors the engine refreshes cookies and retries automatically.

BUG FIXES
  * Session cookies from Playwright were written with expiry=-1 and silently
    discarded -> normalized to 0 (session cookie).
  * Unchecking every playlist item silently downloaded the WHOLE playlist
    as one task -> now blocked with a clear warning.
  * Watchdog only monitored DOWNLOADING tasks; stuck metadata extraction
    (STARTING) was never recovered -> now covered too.
  * Queue dispatcher silently dropped tasks whose status changed mid-dispatch.
  * Settings load/save had a fragile self-reference during initialization and
    normalized settings outside the lock -> restructured, thread-safe.
  * MM:SS / HH:MM:SS timestamps accepted seconds/minutes >= 60 -> validated.
  * Hardsub burning used fragile ffmpeg filter escaping -> safe temp copy.
  * view_count formatting crashed on non-integer metadata -> robust helper.
  * Duplicate-URL protection now also covers queued/active tasks.
  * URL repair mutated shared task state without the state lock.

MODERNIZATION / NEW FEATURES
  * One-click FFmpeg download/update (Settings > Network & Engines, or
    Diagnostics): compact static ffmpeg first (~30 MB), full BtbN build as
    fallback, PLUS ffprobe via HTTP-Range partial extraction (only the needed
    ~25 MB of a 119 MB archive). Live progress + speed + ETA + cancel,
    auto-configured path. mutagen added to the install/update lists so
    thumbnail embedding works even without ffprobe.
  * Cookie Helper dialog: Extract Now, Auto-Fix (gracefully closes the browser,
    extracts cookies, reopens it with --restore-last-session), cookies.txt
    import, in-app Playwright engine installer, retry cookie-failed tasks.
  * Rotating on-disk log file (logs/sina_fusion.log) + "Open Logs Folder".
  * Global crash handlers (sys.excepthook + Tk callback exceptions).
  * Single-instance guard on Windows (prevents concurrent-run conflicts).
  * Exit confirmation while downloads are active/queued.
  * New 1440p / 4K quick presets, live queue-count badge in the sidebar,
    "Open Downloads" sidebar button, Ctrl+L to focus the URL box.
  * Headless `--selftest` mode for deterministic logic verification.
  * Refreshed browser fingerprints (Chrome 142 era).

v18.5.0 CHANGES (this release)
  * Cookie Bridge extension v3: connects AUTOMATICALLY the moment the app opens
    (adaptive 10s watch while offline -> instant push on app launch) and pushes
    cookie changes in near-real-time (~1.5s debounce) plus a 30s heartbeat.
  * Extension upgrades: live popup (auto-refresh, app version, sync count, top
    domains), advanced options (auto-push, connect/disconnect notifications,
    all-sites vs media-only domain filter), one-click cookies.txt export,
    context menu + Ctrl+Shift+S, durable alarm-based loop. /ping now reports
    app-side cookie stats.

v18.4.1 CHANGES
  * 'browser' cookie source now uses live bridge cookies directly when available,
    instead of failing on the locked browser DB first and wasting a retry (removes
    the misleading 'Could not copy Chrome cookie database' ERROR on every download).

v18.4.0 CHANGES
  * Full-project audit & hardening. Cookie Bridge security: Host-header check
    (anti DNS-rebinding) + a per-install secret token (blocks local cookie
    injection) + socket timeout + rejects empty cookie jars. yt-dlp now gets a
    snapshot copy so it can't clobber the live bridge file. CDP harvest only
    trusts real Chromium browsers (not Node/Electron inspectors).
  * Extension v2.0: generated icons, token auth, skip-empty push, durable alarm
    debounce + fetch timeout + exponential backoff, rich popup (status/count/last
    push/top domains/auto-push toggle), options page, context menu + Ctrl+Shift+S.
  * Engine fixes: hash-verify no longer leaves tasks stuck in VERIFYING; hardsub
    ffmpeg stderr goes to a file (no pipe deadlock) and partial output is cleaned
    on failure; 416 partial cleanup runs outside the state lock and protects other
    tasks by unique video id; permanent errors (unavailable/DRM/geo) stop retrying.
  * GUI/utils fixes: thumbnail socket leak closed; DEBUG no longer floods the log
    buffer when disabled; faster incremental log scan; Windows reserved filenames
    (CON/NUL/...) sanitized; settings save uses a unique temp file; disk free-space
    cached (no per-heartbeat disk syscall); thumbnail negative-cache evicts oldest.

v18.3.1 CHANGES
  * Fixed the infinite HTTP 416 resume loop: stale .part cleanup now searches
    playlist SUBFOLDERS recursively (it previously scanned only the top level and
    missed the partial file, so the same video retried 416 forever).

v18.3.0 CHANGES
  * SINA Cookie Bridge: a custom browser extension (rebuilt from "Get cookies.txt
    LOCALLY") collects ALL decrypted cookies via chrome.cookies and AUTO-PUSHES
    them to a tiny localhost server in this app. Works while the browser is OPEN
    with no restart and no CDP debug port. Cookie Helper > "Install SINA Cookie
    Extension" writes the loadable folder and opens the browser extensions page.
    The app prefers these live bridge cookies over DB/CDP extraction.
  * Bridge server is localhost-only and requires application/json (blocks drive-by
    web pages); cookies never leave the computer.

v18.2.0 CHANGES
  * REAL cookies automatically: when the browser is open and locks its cookie DB,
    auto-refresh now harvests DECRYPTED logged-in cookies through an already-open
    CDP port (non-disruptive, browser stays open) instead of falling back to
    anonymous cookies that cannot bypass YouTube bot/login checks. The CDP auto-fix
    port is remembered so later refreshes rediscover it; harvested cookies are
    persisted to the auto engine's file.
  * Fixed the futile retry loop: anonymous cookies no longer overwrite real ones
    (separate file) and the engine stops retrying with a clear "use Cookie Helper >
    CDP" remediation instead of looping on 'sign in to confirm you're not a bot'.
  * Cookie file validation: a configured cookies.txt that is not valid Netscape
    format is detected and skipped (falls back to auto) instead of aborting every
    download with 'does not look like a Netscape format cookies file'.
  * New "Copy Logs" button in System Logs: copies the shown entries (honoring the
    level filter + search) to the clipboard for easy pasting into reports.

v18.1.1 CHANGES
  * FFmpeg is now installed to a STABLE shared folder (~/.sina_fusion/ffmpeg/bin)
    and discovered there from ANY copy of the script - moving/running the file
    from a different folder no longer causes "FFmpeg Missing".
  * Playwright cookie warm-up uses the FULL Chromium binary via channel="chromium"
    (new headless mode); it never requires the separate, geo-blocked
    "chrome-headless-shell" download. executable_path kept as a fallback.
  * Fixed the Playwright browser mirror: the registry.npmmirror.com host serves
    the real builds (the previous cdn.npmmirror.com path returned 404), so fresh
    installs work in regions where cdn.playwright.dev is blocked (403).

v18.1.0 CHANGES
  * COOKIES WHILE BROWSER IS OPEN (extension-style): modern Chromium locks its
    cookie file EXCLUSIVELY while running, so no file-copy works. New
    CdpCookieExtractor harvests DECRYPTED cookies through the browser's own
    DevTools Protocol (the same source cookie extensions use) - handles v20
    app-bound encryption too. Cookie Helper > "Extract from OPEN browser (CDP)"
    gracefully restarts the browser with a local cookie-access port, harvests,
    and LEAVES IT OPEN with the session restored. Direct DB extraction also
    gained a Win32 shared-read fallback + WAL/SHM recovery.
  * Browser auto-detection: 'auto' / uninstalled browsers (e.g. 'chromium')
    now resolve to an actually-installed browser instead of yielding 0 cookies.
  * Post-download hash verification is now OPT-IN (off by default); existing
    installs migrated once. Re-enable any time in Settings.
  * Playwright: installs are usable WITHOUT restarting (runtime reload), the
    installer streams full progress to the log and verifies the Chromium binary.
  * Logging: DEBUG is the default; far more verbose cookie / CDP / Playwright /
    download diagnostics, plus a full startup environment dump in the log.

Run `python youtube-downloader-pro.py --selftest` to verify core logic.
"""
from __future__ import annotations

import collections
import copy
import base64
import gzip
import hashlib
import hmac
import http.server
import ipaddress
import json
import logging
import logging.handlers
import os
import platform
import pprint
import queue
import random
import re
import secrets
import shutil
import socket
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
import webbrowser
import zipfile
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
from urllib.parse import parse_qsl, urlencode, urlparse, urlsplit, urlunsplit
import tkinter
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def _safe_relaunch(py_exe: str, extra_env: Optional[Dict[str, str]] = None):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    subprocess.Popen([py_exe, str(Path(__file__).resolve()), *sys.argv[1:]], env=env)
    sys.exit(0)


def _bootstrap_venv_if_needed():
    if getattr(sys, "frozen", False) or os.environ.get("SINA_VENV_BOOTSTRAPPED") == "1":
        return
    try:
        import yt_dlp, PIL, requests  # noqa: F401
        return
    except (ImportError, ModuleNotFoundError):
        pass
    sdir = Path(__file__).resolve().parent
    for vn in (".venv", "venv", "env"):
        py = sdir / vn / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        if py.exists() and Path(sys.executable).resolve() != py.resolve():
            try:
                _safe_relaunch(str(py), {"SINA_VENV_BOOTSTRAPPED": "1"})
            except Exception:
                pass


_bootstrap_venv_if_needed()

_missing: List[str] = []
_pip_map = {"Pillow": "Pillow", "requests": "requests", "yt-dlp": "yt-dlp"}
try:
    from PIL import Image, ImageDraw, ImageTk
except Exception:
    Image = ImageDraw = ImageTk = None; _missing.append("Pillow")
try:
    import requests
except Exception:
    requests = None; _missing.append("requests")
try:
    import yt_dlp
except Exception:
    yt_dlp = None; _missing.append("yt-dlp")

if _missing:
    hint = "Missing required packages:\n\n" + "\n".join(f"- {p}" for p in _missing) + f"\n\nActive Python:\n{sys.executable}\n"
    if not getattr(sys, "frozen", False):
        try:
            r = tkinter.Tk(); r.withdraw()
            ok = messagebox.askyesno("SINA Fusion Dependencies", hint + "\nAuto-install missing packages now?")
            r.destroy()
            if ok:
                pkgs = list(dict.fromkeys([_pip_map[p] for p in _missing] + ["humanize", "psutil", "pycryptodome", "mutagen"]))
                # No -U: only install what is missing; do not force-upgrade packages
                # that are already present (broader than the consent prompt implies).
                subprocess.run([sys.executable, "-m", "pip", "install", *pkgs], timeout=900, check=True)
                _safe_relaunch(sys.executable)
        except Exception as err:
            try:
                r = tkinter.Tk(); r.withdraw()
                messagebox.showerror("Install Failed", f"{err}\n\nRun:\n\"{sys.executable}\" -m pip install {' '.join(_pip_map[p] for p in _missing)}")
                r.destroy()
            except Exception:
                sys.stderr.write(f"Install error: {err}\n")
    else:
        try:
            r = tkinter.Tk(); r.withdraw(); messagebox.showerror("Dependencies", hint); r.destroy()
        except Exception:
            sys.stderr.write(hint + "\n")
    sys.exit(1)

try:
    import humanize
except Exception:
    humanize = None
try:
    from plyer import notification
except Exception:
    notification = None
try:
    from pystray import Icon, MenuItem as item
except Exception:
    Icon = item = None
try:
    import instaloader
except Exception:
    instaloader = None
try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None


def reload_playwright() -> bool:
    """(Re)import Playwright at runtime so a fresh install is usable WITHOUT an
    app restart (the top-level import is cached at startup)."""
    global sync_playwright
    try:
        import importlib
        mod = importlib.import_module("playwright.sync_api")
        sync_playwright = getattr(mod, "sync_playwright", None)
        ok = sync_playwright is not None
        LoggerSetup.log(f"Playwright engine reload: {'OK' if ok else 'symbol missing'}", "debug")
        return ok
    except Exception as e:
        sync_playwright = None
        LoggerSetup.log(f"Playwright reload failed: {e}", "debug")
        return False


def playwright_browser_ready() -> Tuple[bool, str]:
    """Check both the pip package AND the downloaded Chromium binary are present."""
    if not sync_playwright:
        return False, "Playwright package is not installed."
    try:
        p = sync_playwright().start()
        try:
            exe = Path(p.chromium.executable_path)
            if exe.exists():
                return True, str(exe)
            return False, f"Chromium binary missing at {exe} (run: python -m playwright install chromium)"
        finally:
            p.stop()
    except Exception as e:
        return False, str(e).splitlines()[0][:200]
try:
    from fake_useragent import UserAgent
except Exception:
    UserAgent = None
try:
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import unpad
    HAS_CRYPTO = True
except Exception:
    HAS_CRYPTO = False
try:
    import psutil
except Exception:
    psutil = None
try:
    import ctypes, ctypes.wintypes as wintypes, comtypes, comtypes.client as cc
    HAS_TASKBAR = sys.platform == "win32"
except Exception:
    HAS_TASKBAR = False
    ctypes = wintypes = comtypes = cc = None


def _resolve_runtime_dirs() -> Tuple[Path, Path]:
    bdir = Path(getattr(sys, "_MEIPASS", Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent))
    pdir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    probe = pdir / ".sina_write_probe"
    try:
        pdir.mkdir(parents=True, exist_ok=True)
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return bdir, pdir
    except Exception:
        ddir = Path.home() / ".sina_fusion"
        ddir.mkdir(parents=True, exist_ok=True)
        return bdir, ddir


APP_NAME, APP_VERSION = "SINA Fusion Downloader", "18.5.0"
APP_DIR, DATA_DIR = _resolve_runtime_dirs()
SETTINGS_FILE = str(DATA_DIR / "sina_enterprise_settings_v15.json")
KEY_FILE = str(DATA_DIR / "sina_security.key")
AUTO_COOKIE_FILE = str(DATA_DIR / "cookies_auto.txt")
# Anonymous warm-up cookies live in a SEPARATE file so they never overwrite real
# browser cookies. They cannot bypass YouTube bot/login checks (last resort only).
ANON_COOKIE_FILE = str(DATA_DIR / "cookies_anon.txt")
ARCHIVE_FILE = "sina_download_archive.txt"
# SINA Cookie Bridge: a custom browser extension pushes decrypted cookies to a
# tiny localhost server in this app. Works while the browser is OPEN (no restart,
# no CDP debug port). The extension folder is materialized to a stable shared dir.
COOKIE_BRIDGE_PORT = 17373
COOKIE_BRIDGE_DIR = Path.home() / ".sina_fusion" / "cookie-bridge-extension"
BRIDGE_COOKIE_FILE = str(DATA_DIR / "cookies_bridge.txt")
# Stable, user-level FFmpeg location shared by EVERY copy of the script, so
# moving/running the file from a different folder never causes "FFmpeg Missing".
FFMPEG_SHARED_DIR = Path.home() / ".sina_fusion" / "ffmpeg" / "bin"

SUBTITLE_LANGUAGES = {"en": "English", "fa": "Persian", "fr": "French", "de": "German", "es": "Spanish", "it": "Italian", "ru": "Russian", "zh-Hans": "Chinese (Simplified)", "zh-Hant": "Chinese (Traditional)", "ja": "Japanese", "ko": "Korean", "ar": "Arabic", "tr": "Turkish", "pt": "Portuguese", "hi": "Hindi"}
DOH_PROVIDERS = {"Cloudflare": "https://cloudflare-dns.com/dns-query", "Google": "https://dns.google/resolve", "Quad9": "https://dns.quad9.net:5053/dns-query", "AdGuard": "https://dns.adguard-dns.com/resolve"}
SPONSORBLOCK_CATEGORIES = {"sponsor": "Sponsor", "intro": "Intro", "outro": "Outro", "selfpromo": "Self-Promo", "interaction": "Subscribe/Like", "preview": "Preview", "music_offtopic": "Non-Music"}
QUICK_PRESETS: Dict[str, Dict[str, Any]] = {
    "Best Video (MP4)": {"type": "video", "format": "bestvideo+bestaudio/best", "ext": "mp4"},
    "Best Video (MKV)": {"type": "video", "format": "bestvideo+bestaudio/best", "ext": "mkv"},
    "2160p 4K UHD (MP4)": {"type": "video", "format": "bestvideo[height<=2160]+bestaudio/best[height<=2160]", "ext": "mp4"},
    "1440p QHD (MP4)": {"type": "video", "format": "bestvideo[height<=1440]+bestaudio/best[height<=1440]", "ext": "mp4"},
    "1080p Full HD (MP4)": {"type": "video", "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]", "ext": "mp4"},
    "720p HD (MP4)": {"type": "video", "format": "bestvideo[height<=720]+bestaudio/best[height<=720]", "ext": "mp4"},
    "480p SD (MP4)": {"type": "video", "format": "bestvideo[height<=480]+bestaudio/best[height<=480]", "ext": "mp4"},
    "Audio MP3 (320k)": {"type": "audio", "codec": "mp3", "quality": "320"},
    "Audio M4A (256k)": {"type": "audio", "codec": "m4a", "quality": "256"},
    "Audio FLAC (Lossless)": {"type": "audio", "codec": "flac", "quality": "0"},
}
SPEED_LIMIT_CHOICES = {"Unlimited": 0, "10 MB/s": 10240, "5 MB/s": 5120, "2 MB/s": 2048, "1 MB/s": 1024, "500 KB/s": 500, "250 KB/s": 250}


def detect_bundled_ffmpeg() -> Optional[str]:
    bases = [APP_DIR, DATA_DIR, Path.home() / ".sina_fusion"]
    seen: Set[Path] = set()
    for b in bases:
        if b in seen:
            continue
        seen.add(b)
        for rel in ("ffmpeg-master-latest-win64-gpl-shared/bin/ffmpeg.exe", "ffmpeg/bin/ffmpeg.exe", "ffmpeg.exe", "ffmpeg/bin/ffmpeg", "ffmpeg"):
            c = b / rel
            if c.exists() and c.is_file():
                return str(c)
    return shutil.which("ffmpeg") or None


def resolve_ffmpeg_location(value: Optional[str]) -> Optional[str]:
    raw = (value or "").strip().strip('"')
    if raw and raw.lower() not in {"ffmpeg", "ffmpeg.exe"}:
        if Path(raw).exists():
            return str(Path(raw))
        f = shutil.which(raw)
        if f:
            return f
    return detect_bundled_ffmpeg()


def resolve_ffprobe_location(ff_loc: Optional[str] = None) -> Optional[str]:
    ff = resolve_ffmpeg_location(ff_loc)
    if ff:
        p = Path(ff)
        cand = p.parent / ("ffprobe.exe" if p.suffix.lower() == ".exe" else "ffprobe")
        if cand.exists():
            return str(cand)
    return shutil.which("ffprobe")


def detect_aria2(value: Optional[str] = None) -> Optional[str]:
    raw = (value or "aria2c").strip().strip('"')
    if raw:
        if Path(raw).exists() and Path(raw).is_file():
            return raw
        f = shutil.which(raw)
        if f:
            return f
    for b in (APP_DIR, DATA_DIR):
        for c in (b / "aria2c.exe", b / "aria2c"):
            if c.exists() and c.is_file():
                return str(c)
    return shutil.which("aria2c")


def detect_js_runtimes() -> Dict[str, Dict[str, str]]:
    out: Dict[str, Dict[str, str]] = {}
    for name, paths in {
        "deno": ["deno", str(APP_DIR / "deno.exe"), str(APP_DIR / "deno"), str(Path.home() / ".deno/bin/deno.exe"), str(Path.home() / ".deno/bin/deno")],
        "node": ["node", r"C:\Program Files\nodejs\node.exe", r"C:\Program Files (x86)\nodejs\node.exe", "/usr/local/bin/node", "/usr/bin/node"],
        "bun": ["bun", str(Path.home() / ".bun/bin/bun.exe"), str(Path.home() / ".bun/bin/bun")],
    }.items():
        for p in paths:
            f = shutil.which(p) if not os.path.isabs(p) else p
            if f and os.path.exists(f):
                out[name] = {"path": f}; break
    return out


def safe_int(v: Any, d: int, mn: Optional[int] = None, mx: Optional[int] = None) -> int:
    try:
        n = int(float(v))
    except Exception:
        n = d
    if mn is not None: n = max(mn, n)
    if mx is not None: n = min(mx, n)
    return n


def safe_float(v: Any, d: float, mn: Optional[float] = None, mx: Optional[float] = None) -> float:
    try:
        n = float(v)
    except Exception:
        n = d
    if mn is not None: n = max(mn, n)
    if mx is not None: n = min(mx, n)
    return n


def sanitize_filename_part(v: Any, default: str = "media", limit: int = 150) -> str:
    t = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", str(v if v is not None else default))
    t = re.sub(r"\s+", " ", t).strip(" .")[:limit].strip(" .") or default
    # Windows reserved device names (CON, NUL, COM1...) cannot be created as files.
    if sys.platform == "win32" and re.match(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)", t, re.IGNORECASE):
        t = "_" + t
    return t


def escape_ytdlp_template_literal(text: str) -> str:
    return (text or "").replace("%", "%%")


def clean_ansi_codes(text: Any) -> str:
    return re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-9;?]*[ -/]*[@-~])", "", str(text if text is not None else ""))


def format_bytes(num_bytes: Optional[Union[int, float]], binary: bool = True) -> str:
    if num_bytes is None:
        return "N/A"
    try:
        val = float(num_bytes)
    except Exception:
        return "N/A"
    if val < 0:
        return "N/A"
    if humanize is not None:
        try:
            return humanize.naturalsize(val, binary=binary)
        except Exception:
            pass
    base = 1024.0 if binary else 1000.0
    units = ("B", "KiB", "MiB", "GiB", "TiB") if binary else ("B", "KB", "MB", "GB", "TB")
    for u in units[:-1]:
        if val < base:
            return f"{val:.1f} {u}" if u != "B" else f"{int(val)} B"
        val /= base
    return f"{val:.2f} {units[-1]}"


def format_duration(seconds: Optional[Union[int, float]]) -> str:
    if seconds is None:
        return "N/A"
    try:
        sec = max(0, int(round(float(seconds))))
    except Exception:
        return "N/A"
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"


def format_count(value: Any) -> str:
    """Robust thousands-separated formatting for view/like counts (may be str)."""
    try:
        return f"{int(float(value)):,}"
    except (TypeError, ValueError):
        return str(value) if value is not None else "0"


def parse_timestamp_to_seconds(value: str) -> Optional[float]:
    raw = (value or "").strip()
    if not raw:
        return None
    if re.fullmatch(r"\d+(?:\.\d+)?", raw):
        return float(raw)
    parts = raw.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"Invalid timestamp '{value}'. Use SS, MM:SS, or HH:MM:SS.")
    try:
        nums = [float(p) for p in parts]
    except ValueError:
        raise ValueError(f"Invalid timestamp '{value}'. Use SS, MM:SS, or HH:MM:SS.") from None
    if any(n < 0 for n in nums):
        raise ValueError("Timestamp cannot be negative.")
    if len(nums) == 2:
        if nums[1] >= 60:
            raise ValueError("Seconds must be below 60 in MM:SS timestamps.")
        return nums[0] * 60.0 + nums[1]
    if nums[1] >= 60 or nums[2] >= 60:
        raise ValueError("Minutes and seconds must be below 60 in HH:MM:SS timestamps.")
    return nums[0] * 3600.0 + nums[1] * 60.0 + nums[2]


def parse_index_selection(spec: str, max_idx: int) -> List[int]:
    sel: Set[int] = set()
    for part in re.split(r"[,\s]+", (spec or "").strip()):
        if not part:
            continue
        try:
            if "-" in part:
                a, b = part.split("-", 1)
                lo, hi = max(1, int(a)), min(max_idx, int(b))
                if lo <= hi:
                    sel.update(range(lo, hi + 1))
            else:
                idx = int(part)
                if 1 <= idx <= max_idx:
                    sel.add(idx)
        except ValueError:
            raise ValueError(f"Invalid selection '{part}'. Use numbers and ranges like 1-5, 8.") from None
    return sorted(sel)


def extract_urls_from_text(text: str) -> List[str]:
    seen, out = set(), []
    for u in re.findall(r"https?://[^\s<>\"'\]\)]+", text or ""):
        u = u.rstrip(".,;:!?")
        if u and u not in seen:
            seen.add(u); out.append(u)
    return out


def strip_playlist_query_params(url: str) -> str:
    parts = urlsplit(url)
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in {"list", "index", "start_radio"}]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept, doseq=True), parts.fragment))


def _url_host(url: str) -> str:
    """Exact parsed hostname (lowercase). Never substring-match the full URL:
    'x.com' in 'netflix.com' and 'youtube.com.evil.example' must NOT match."""
    try:
        return (urlsplit((url or "").strip()).hostname or "").lower()
    except ValueError:
        return ""


def _host_is(host: str, domain: str) -> bool:
    return host == domain or host.endswith("." + domain)


def _has_playlist_param(url: str) -> bool:
    try:
        return any(k.lower() == "list" and v for k, v in parse_qsl(urlsplit(url).query, keep_blank_values=True))
    except ValueError:
        return False


def detect_platform_label(url: str) -> str:
    low = (url or "").lower()
    host = _url_host(url)
    if _host_is(host, "youtube.com") or _host_is(host, "youtu.be"):
        if _has_playlist_param(url) and not any(k in low for k in ("watch?v=", "youtu.be/", "/shorts/", "/live/")):
            return "YouTube Playlist"
        if _has_playlist_param(url):
            return "YouTube Video + Playlist"
        if "/shorts/" in low:
            return "YouTube Shorts"
        return "YouTube Music" if _host_is(host, "music.youtube.com") else "YouTube"
    for d, l in (("instagram.com", "Instagram"), ("tiktok.com", "TikTok"), ("twitter.com", "X / Twitter"), ("x.com", "X / Twitter"), ("soundcloud.com", "SoundCloud"), ("twitch.tv", "Twitch"), ("vimeo.com", "Vimeo"), ("facebook.com", "Facebook"), ("fb.watch", "Facebook"), ("reddit.com", "Reddit"), ("v.redd.it", "Reddit")):
        if _host_is(host, d):
            return l
    return "Web Media" if low.startswith("http") else "Unknown"


def detect_service_type(url: str) -> "ServiceType":
    host = _url_host(url)
    return ServiceType.YOUTUBE if (_host_is(host, "youtube.com") or _host_is(host, "youtu.be")) else (ServiceType.INSTAGRAM if _host_is(host, "instagram.com") else ServiceType.GENERIC)


def is_likely_media_url(url: str) -> bool:
    if not re.match(r"^https?://", (url or "").strip(), re.I):
        return False
    host = _url_host(url)
    return any(_host_is(host, d) for d in ("youtube.com", "youtu.be", "instagram.com", "tiktok.com", "twitter.com", "x.com", "soundcloud.com", "vimeo.com", "twitch.tv", "facebook.com", "fb.watch", "reddit.com", "dailymotion.com", "bilibili.com", "aparat.com")) or bool(re.search(r"\.(mp4|mkv|webm|mp3|m4a|flac|wav|m3u8|mpd)(\?|$)", url.lower()))


def compute_file_hash(filepath: str, algo: str = "md5") -> str:
    h = hashlib.sha256() if str(algo).lower() == "sha256" else hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def open_file_location(filepath: Optional[str]):
    if not filepath:
        return
    path = Path(filepath)
    if not path.exists():
        path = path.parent if path.parent.exists() else None
        if not path:
            return
    try:
        if sys.platform == "win32":
            subprocess.Popen(["explorer", "/select,", os.path.normpath(str(path))] if path.is_file() else ["explorer", os.path.normpath(str(path))])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-R", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path.parent if path.is_file() else path)])
    except Exception as e:
        LoggerSetup.log(f"Error opening folder: {e}", "error")


class ColorPalette(Enum):
    STATUS_DOWNLOADING = "#0EA5E9"; STATUS_COMPLETED = "#22C55E"; STATUS_ERROR = "#E11D48"
    STATUS_PAUSED = "#F59E0B"; STATUS_CANCELLED = "#64748B"; STATUS_PROCESSING = "#A855F7"
    STATUS_VERIFYING = "#38BDF8"; STATUS_SKIPPED = "#94A3B8"; STATUS_QUEUED = "#94A3B8"
    ACCENT_COLOR = "#0EA5E9"; ACCENT_HOVER = "#0284C7"; TEXT_GRAY = "#CBD5E1"; TEXT_ERROR = "#FB7185"
    BUTTON_CANCEL_FG = "#E11D48"; BUTTON_CANCEL_HOVER = "#BE123C"
    BUTTON_ACTION_FG = "#22C55E"; BUTTON_ACTION_HOVER = "#16A34A"; GRAPH_LINE = "#38BDF8"


class _ThemeColors:
    """Mode-aware palette (pure tkinter). Access colors as ThemeColors.CARD etc."""
    DARK = {"SIDEBAR": "#0B1220", "CARD": "#1E293B", "CARD_ALT": "#0F172A", "BORDER": "#334155",
            "TEXT_PRIMARY": "#F8FAFC", "TEXT_MUTED": "#94A3B8", "BADGE_BG": "#0C4A6E", "BADGE_TEXT": "#7DD3FC",
            "NAV_ACTIVE": "#1E293B", "BG": "#0F172A", "INPUT": "#111C2E", "CANVAS": "#0B1220"}
    LIGHT = {"SIDEBAR": "#E2E8F0", "CARD": "#FFFFFF", "CARD_ALT": "#F1F5F9", "BORDER": "#CBD5E1",
             "TEXT_PRIMARY": "#0F172A", "TEXT_MUTED": "#475569", "BADGE_BG": "#E0F2FE", "BADGE_TEXT": "#0369A1",
             "NAV_ACTIVE": "#CBD5E1", "BG": "#F8FAFC", "INPUT": "#FFFFFF", "CANVAS": "#E2E8F0"}

    def __init__(self):
        self.mode = "dark"

    def set_mode(self, mode: str):
        m = (mode or "dark").lower()
        if m == "system":
            m = "dark"
            try:
                if sys.platform == "win32":
                    import winreg
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize") as k:
                        m = "light" if winreg.QueryValueEx(k, "AppsUseLightTheme")[0] == 1 else "dark"
            except Exception:
                pass
        self.mode = m if m in ("dark", "light") else "dark"

    def palette(self) -> Dict[str, str]:
        return self.DARK if self.mode == "dark" else self.LIGHT

    def __getattr__(self, key: str) -> str:
        try:
            return self.palette()[key]
        except KeyError:
            raise AttributeError(key) from None


ThemeColors = _ThemeColors()


class IconFactory:
    _cache: Dict[Tuple[str, int, str], Any] = {}

    @classmethod
    def get(cls, name: str, size: int = 18, color: str = "#FFFFFF"):
        key = (name, size, color)
        if key in cls._cache:
            return cls._cache[key]
        pad, w, mid = max(2, size // 8), max(2, size // 9), size // 2
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        ln = lambda pts, wd=w: d.line(pts, fill=color, width=wd, joint="curve")
        rc = lambda box, wd=w: d.rounded_rectangle(box, radius=max(2, size // 8), outline=color, width=wd)
        if name == "add": ln([(mid, pad + 2), (mid, size - pad - 2)]); ln([(pad + 2, mid), (size - pad - 2, mid)])
        elif name in {"download", "analyze"}: ln([(mid, pad + 1), (mid, size - pad - 5)]); ln([(mid, size - pad - 5), (pad + 4, mid)]); ln([(mid, size - pad - 5), (size - pad - 4, mid)]); ln([(pad + 3, size - pad - 1), (size - pad - 3, size - pad - 1)])
        elif name == "search": d.ellipse((pad, pad, size - pad - 6, size - pad - 6), outline=color, width=w); ln([(size - pad - 7, size - pad - 7), (size - pad - 2, size - pad - 2)])
        elif name == "paste": rc((pad + 3, pad + 5, size - pad - 3, size - pad - 1)); d.rounded_rectangle((pad + 5, pad, size - pad - 5, pad + 6), radius=2, outline=color, width=w)
        elif name == "queue":
            for y in (pad + 2, mid, size - pad - 3): ln([(pad + 5, y), (size - pad - 2, y)]); d.ellipse((pad, y - 2, pad + 3, y + 2), fill=color)
        elif name == "logs":
            rc((pad + 2, pad, size - pad - 2, size - pad))
            for y in (pad + 5, mid, size - pad - 5): ln([(pad + 6, y), (size - pad - 6, y)], max(1, w - 1))
        elif name == "settings":
            d.ellipse((pad + 4, pad + 4, size - pad - 4, size - pad - 4), outline=color, width=w); d.ellipse((mid - 2, mid - 2, mid + 2, mid + 2), fill=color)
            for pts in ([(mid, pad), (mid, pad + 4)], [(mid, size - pad - 4), (mid, size - pad)], [(pad, mid), (pad + 4, mid)], [(size - pad - 4, mid), (size - pad, mid)]): ln(pts, max(1, w - 1))
        elif name == "pause": d.rounded_rectangle((pad + 3, pad + 2, mid - 2, size - pad - 2), radius=2, fill=color); d.rounded_rectangle((mid + 2, pad + 2, size - pad - 3, size - pad - 2), radius=2, fill=color)
        elif name in {"play", "retry"}: d.polygon([(pad + 4, pad + 2), (pad + 4, size - pad - 2), (size - pad - 2, mid)], fill=color)
        elif name == "cancel": ln([(pad + 3, pad + 3), (size - pad - 3, size - pad - 3)]); ln([(size - pad - 3, pad + 3), (pad + 3, size - pad - 3)])
        elif name == "clear": ln([(pad + 4, pad + 5), (size - pad - 4, size - pad - 5)]); ln([(size - pad - 4, pad + 5), (pad + 4, size - pad - 5)]); ln([(pad + 2, pad + 2), (size - pad - 2, pad + 2)])
        elif name == "folder": d.rounded_rectangle((pad, pad + 5, size - pad, size - pad - 2), radius=3, outline=color, width=w); d.rounded_rectangle((pad + 2, pad + 2, mid, pad + 7), radius=2, outline=color, width=w)
        elif name == "open": rc((pad + 2, pad + 5, size - pad - 5, size - pad - 2)); ln([(mid, pad + 2), (size - pad - 2, pad + 2), (size - pad - 2, mid)]); ln([(size - pad - 2, pad + 2), (mid, mid)])
        elif name == "repair": d.arc((pad + 2, pad + 2, size - pad - 2, size - pad - 2), 35, 320, fill=color, width=w); d.polygon([(size - pad - 2, mid - 4), (size - pad, mid + 3), (size - pad - 8, mid + 1)], fill=color)
        elif name == "up": ln([(mid, size - pad - 2), (mid, pad + 3)]); ln([(pad + 4, mid), (mid, pad + 3), (size - pad - 4, mid)])
        elif name == "done": ln([(pad + 2, mid), (mid - 1, size - pad - 4), (size - pad - 2, pad + 4)])
        elif name == "info": d.ellipse((pad + 1, pad + 1, size - pad - 1, size - pad - 1), outline=color, width=w); d.ellipse((mid - 1, pad + 4, mid + 1, pad + 6), fill=color); ln([(mid, mid - 1), (mid, size - pad - 4)])
        elif name == "clock": d.ellipse((pad + 1, pad + 1, size - pad - 1, size - pad - 1), outline=color, width=w); ln([(mid, pad + 4), (mid, mid), (size - pad - 4, mid + 2)])
        elif name == "shield": d.polygon([(mid, pad + 1), (size - pad - 2, pad + 4), (size - pad - 3, mid + 2), (mid, size - pad - 1), (pad + 3, mid + 2), (pad + 2, pad + 4)], outline=color, width=w)
        elif name == "exit": rc((pad + 2, pad + 2, size - pad - 5, size - pad - 2)); ln([(mid, mid), (size - pad - 1, mid)]); ln([(size - pad - 5, mid - 4), (size - pad - 1, mid), (size - pad - 5, mid + 4)])
        else: d.ellipse((pad, pad, size - pad, size - pad), outline=color, width=w)
        cls._cache[key] = ImageTk.PhotoImage(img)
        return cls._cache[key]


class ToolTip:
    def __init__(self, widget, text: str, delay: int = 450):
        self.widget, self.text, self.delay, self._aid, self._win = widget, text, delay, None, None
        for ev, fn in (("<Enter>", self._sched), ("<Leave>", self._hide), ("<ButtonPress>", self._hide), ("<Destroy>", self._hide)):
            widget.bind(ev, fn, add="+")

    def set_text(self, text: str):
        self.text = text

    def _sched(self, _e=None):
        self._hide()
        try:
            if self.widget.winfo_exists():
                self._aid = self.widget.after(self.delay, self._show)
        except Exception:
            pass

    def _show(self):
        if self._win or not self.text:
            return
        try:
            if not self.widget.winfo_exists():
                return
            self._win = tkinter.Toplevel(self.widget)
            self._win.wm_overrideredirect(True)
            self._win.wm_geometry(f"+{self.widget.winfo_rootx() + 10}+{self.widget.winfo_rooty() + self.widget.winfo_height() + 6}")
            tkinter.Label(self._win, text=self.text, bg="#0F172A", fg="#F8FAFC", padx=8, pady=4, relief="solid", borderwidth=1, font=("Arial", 9)).pack()
        except Exception:
            self._win = None

    def _hide(self, _e=None):
        if self._aid:
            try:
                self.widget.after_cancel(self._aid)
            except Exception:
                pass
            self._aid = None
        if self._win:
            try:
                self._win.destroy()
            except Exception:
                pass
            self._win = None


class LoggerSetup:
    _logger: Optional[logging.Logger] = None
    _file_handler: Optional[logging.Handler] = None
    _gui_notify: Optional[Callable[[], None]] = None
    _lock = threading.RLock()
    _records: collections.deque = collections.deque(maxlen=12000)
    # Verbose diagnostics ON by default so the full cookie / Playwright / download
    # pipeline is visible in the log file and the System Logs window without any
    # extra switch. Users can still turn it off in Settings.
    _seq, _debug_enabled = 0, True

    @staticmethod
    def log_dir() -> Path:
        d = DATA_DIR / "logs"
        try:
            d.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        return d

    @classmethod
    def set_debug_enabled(cls, en: bool):
        with cls._lock:
            cls._debug_enabled = bool(en)
            if cls._file_handler is not None:
                cls._file_handler.setLevel(logging.DEBUG if en else logging.INFO)

    @classmethod
    def set_gui_callback(cls, cb: Optional[Callable[[], None]]):
        with cls._lock:
            cls._gui_notify = cb
        if cb:
            try: cb()
            except Exception: pass

    @classmethod
    def get_logger(cls) -> logging.Logger:
        with cls._lock:
            if cls._logger is None:
                cls._logger = logging.getLogger("SinaEnterpriseCore")
                cls._logger.setLevel(logging.DEBUG); cls._logger.propagate = False
                if not cls._logger.handlers:
                    h = logging.StreamHandler(sys.stdout); h.setFormatter(logging.Formatter("%(message)s")); cls._logger.addHandler(h)
                    try:
                        fh = logging.handlers.RotatingFileHandler(cls.log_dir() / "sina_fusion.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
                        fh.setFormatter(logging.Formatter("%(message)s"))
                        fh.setLevel(logging.DEBUG if cls._debug_enabled else logging.INFO)
                        cls._logger.addHandler(fh); cls._file_handler = fh
                    except Exception:
                        pass
            return cls._logger

    @staticmethod
    def _console_safe(text: str) -> str:
        try:
            enc = getattr(sys.stdout, "encoding", None) or "utf-8"
            return text.encode(enc, errors="replace").decode(enc, errors="replace")
        except Exception:
            return str(text).encode("ascii", errors="replace").decode("ascii", errors="replace")

    @classmethod
    def log(cls, msg: Any, level: str = "info", debug_data: Any = None, exc_info: bool = False):
        logger, lvl = cls.get_logger(), (level or "info").lower()
        ts, tn = datetime.now().strftime("%H:%M:%S.%f")[:-3], threading.current_thread().name
        try:
            cf = sys._getframe(1)
            ctx = f"{os.path.basename(cf.f_code.co_filename).replace('.py', '')}.{cf.f_code.co_name}"
        except Exception:
            ctx = "CORE"
        line = f"[{ts}] | {lvl.upper():<7} | {tn[:15]:<15} | {ctx[:25]:<25} | {clean_ansi_codes(msg)}"
        if debug_data is not None: line += f"\n   >>> DATA:\n{pprint.pformat(debug_data, indent=4)}"
        if exc_info: line += f"\n   !!! TRACE:\n{traceback.format_exc()}"
        with cls._lock:
            cb, dbg = cls._gui_notify, cls._debug_enabled
            # Don't flood the bounded record buffer with DEBUG spam when debug is off
            # (it would evict real INFO/ERROR history and show DEBUG in the Logs UI).
            if lvl != "debug" or dbg:
                cls._seq += 1; cls._records.append({"seq": cls._seq, "level": lvl.upper(), "formatted": line})
        if lvl != "debug" or dbg:
            getattr(logger, lvl if lvl in {"info", "warning", "error", "debug"} else "info")(cls._console_safe(line))
        if cb:
            try: cb()
            except Exception: pass

    @classmethod
    def get_records(cls, after_seq: int = 0, level_filter: str = "ALL", search: str = "") -> Tuple[List[Dict[str, Any]], int]:
        lvl, q = (level_filter or "ALL").upper(), (search or "").strip().lower()
        with cls._lock:
            latest = cls._seq
            # Records are append-ordered: walk backwards and stop at after_seq so the
            # common incremental flush is O(new) instead of scanning all 12000.
            items = []
            for r in reversed(cls._records):
                if r["seq"] <= after_seq:
                    break
                items.append(r)
            items.reverse()
        if lvl != "ALL": items = [r for r in items if r["level"] == lvl]
        if q: items = [r for r in items if q in r["formatted"].lower()]
        return items, latest

    @classmethod
    def clear(cls):
        with cls._lock: cls._records.clear()


class YtdlLoggerAdapter:
    def debug(self, msg: Any):
        t = clean_ansi_codes(msg)
        LoggerSetup.log(f"[YTDL-DBG] {t[8:]}" if t.startswith("[debug] ") else f"[YTDL-INT] {t}", "debug")
    def info(self, msg: Any): LoggerSetup.log(f"[YTDL-INF] {clean_ansi_codes(msg)}", "info")
    def warning(self, msg: Any): LoggerSetup.log(f"[YTDL-WRN] {clean_ansi_codes(msg)}", "warning")
    def error(self, msg: Any): LoggerSetup.log(f"[YTDL-ERR] {clean_ansi_codes(msg)}", "error")


class EnvironmentDiagnostics:
    @staticmethod
    def collect(sm: "SettingsManager") -> Dict[str, str]:
        ff = resolve_ffmpeg_location(sm.get("ffmpeg_path"))
        fp, a2, js = resolve_ffprobe_location(ff), detect_aria2(sm.get("aria2_path")), detect_js_runtimes()
        ok_sp, sp_msg = DiskAnalyzer.check_space(sm.get("download_path"), 500)
        ck = sm.get("cookies_file_path") or ""
        try:
            import importlib.util
            mutagen_ok = importlib.util.find_spec("mutagen") is not None
        except Exception:
            mutagen_ok = False
        return {
            "App Version": f"{APP_NAME} v{APP_VERSION}",
            "OS / Python": f"{platform.system()} {platform.release()} ({platform.machine()}) | Python {platform.python_version()}",
            "UI / yt-dlp": f"tkinter {tkinter.TkVersion} (stdlib) / {getattr(getattr(yt_dlp, 'version', None), '__version__', '?')}",
            "Data Directory": str(DATA_DIR),
            "FFmpeg / FFprobe": f"{ff or 'Missing'} | {fp or 'Missing'}",
            "JS Runtimes": ", ".join(f"{k}: {v['path']}" for k, v in js.items()) or "None Detected (Install Deno/Node for full YouTube support)",
            "Aria2c": a2 or "Not Detected",
            "Playwright / Instaloader": f"{('Yes' if sync_playwright else 'No')} (browser: {playwright_browser_ready()[1] if sync_playwright else 'n/a'}) / {'Yes' if instaloader else 'No'}",
            "Crypto / psutil / mutagen": f"{'GCM' if HAS_CRYPTO else 'No'} / {'Yes' if psutil else 'No'} / {'Yes' if mutagen_ok else 'No (pip install mutagen)'}",
            "Cookie File": f"Found ({ck})" if (ck and os.path.exists(ck)) else f"Missing ({ck})",
            "Download Folder": f"{sm.get('download_path')} [{sp_msg}{' - OK' if ok_sp else ' - LOW'}]",
            "Log File": str(LoggerSetup.log_dir() / "sina_fusion.log"),
        }


class SecurityManager:
    def __init__(self, key_file: str = KEY_FILE):
        self.key_file = key_file; self.key = self._get_or_create_key()

    def _get_or_create_key(self) -> bytes:
        if not HAS_CRYPTO: return b"0" * 32
        try:
            if os.path.exists(self.key_file):
                k = Path(self.key_file).read_bytes()
                if len(k) == 32: return k
            k = get_random_bytes(32); Path(self.key_file).parent.mkdir(parents=True, exist_ok=True); Path(self.key_file).write_bytes(k)
            if os.name != "nt":
                try: os.chmod(self.key_file, 0o600)
                except OSError: pass
            return k
        except Exception as e:
            LoggerSetup.log(f"Security key unavailable ({e}); credentials will NOT be encrypted at rest.", "warning")
            return b"0" * 32

    def encrypt(self, plaintext: str) -> str:
        if not plaintext or plaintext.startswith("enc:v2:"): return plaintext
        if not HAS_CRYPTO:
            # SECURITY: never silently store a credential in plaintext while the
            # UI claims AES-256-GCM. Warn loudly so the user can install the dep.
            LoggerSetup.log("pycryptodome is NOT installed - credentials would be stored in PLAINTEXT. Install it (Settings > Update Libraries) to enable AES-256-GCM encryption.", "warning")
            return plaintext
        try:
            c = AES.new(self.key, AES.MODE_GCM); ct, tag = c.encrypt_and_digest(plaintext.encode("utf-8"))
            return "enc:v2:" + ":".join(base64.b64encode(x).decode("ascii") for x in (c.nonce, tag, ct))
        except Exception:
            LoggerSetup.log("Credential encryption failed; value stored unencrypted. Check the security key file.", "warning")
            return plaintext

    def decrypt(self, ciphertext: str) -> str:
        if not HAS_CRYPTO or not ciphertext: return ciphertext
        if ciphertext.startswith("enc:v2:"):
            try:
                _, _, nb, tb, cb = ciphertext.split(":", 4)
                return AES.new(self.key, AES.MODE_GCM, nonce=base64.b64decode(nb)).decrypt_and_verify(base64.b64decode(cb), base64.b64decode(tb)).decode("utf-8")
            except Exception: return ""
        if ":" in ciphertext:
            try:
                iv_s, ct_s = ciphertext.split(":", 1); iv, ct = base64.b64decode(iv_s), base64.b64decode(ct_s)
                if len(iv) == 16 and len(ct) >= 16 and len(ct) % 16 == 0:
                    return unpad(AES.new(self.key, AES.MODE_CBC, iv).decrypt(ct), AES.block_size).decode("utf-8")
            except Exception: return ciphertext
        return ciphertext


class DiskAnalyzer:
    @staticmethod
    def check_space(path: str, required_mb: int = 100) -> Tuple[bool, str]:
        try:
            p = path or str(Path.home())
            while p and not os.path.exists(p):
                parent = os.path.dirname(p)
                if parent == p: break
                p = parent
            if not os.path.exists(p): return True, "N/A"
            free = psutil.disk_usage(p).free if psutil is not None else shutil.disk_usage(p).free
            fs, ok = format_bytes(free, True), (free / (1024 * 1024)) >= required_mb
            return ok, f"{fs} free" if ok else f"Low Space ({fs} free)"
        except Exception as e: return True, str(e)


class TaskbarManager:
    def __init__(self):
        self.taskbar, self.hwnd = None, None
        if not HAS_TASKBAR: return
        try: comtypes.CoInitialize()
        except Exception: pass
        try:
            class ITaskbarList(comtypes.IUnknown):
                _iid_ = comtypes.GUID("{56FDF342-FD6D-11D0-958A-006097C9A090}")
                _methods_ = [
                    comtypes.COMMETHOD([], ctypes.HRESULT, "HrInit"),
                    comtypes.COMMETHOD([], ctypes.HRESULT, "AddTab", (["in"], wintypes.HWND, "hwnd")),
                    comtypes.COMMETHOD([], ctypes.HRESULT, "DeleteTab", (["in"], wintypes.HWND, "hwnd")),
                    comtypes.COMMETHOD([], ctypes.HRESULT, "ActivateTab", (["in"], wintypes.HWND, "hwnd")),
                    comtypes.COMMETHOD([], ctypes.HRESULT, "SetActiveAlt", (["in"], wintypes.HWND, "hwnd")),
                ]
            class ITaskbarList2(ITaskbarList):
                _iid_ = comtypes.GUID("{602D4995-B13A-429B-A66E-1935E44F4317}")
                _methods_ = [comtypes.COMMETHOD([], ctypes.HRESULT, "MarkFullscreenWindow", (["in"], wintypes.HWND, "hwnd"), (["in"], wintypes.BOOL, "f"))]
            class ITaskbarList3(ITaskbarList2):
                _iid_ = comtypes.GUID("{EA1AFB91-9E28-4B86-90E9-9E9F8A5EEFAF}")
                _methods_ = [
                    comtypes.COMMETHOD([], ctypes.HRESULT, "SetProgressValue", (["in"], wintypes.HWND, "hwnd"), (["in"], ctypes.c_uint64, "c"), (["in"], ctypes.c_uint64, "t")),
                    comtypes.COMMETHOD([], ctypes.HRESULT, "SetProgressState", (["in"], wintypes.HWND, "hwnd"), (["in"], ctypes.c_int, "flags")),
                ]
            tb = cc.CreateObject("{56FDF344-FD6D-11d0-958A-006097C9A090}", interface=ITaskbarList3); tb.HrInit(); self.taskbar = tb
        except Exception: self.taskbar = None

    def attach_window(self, root_widget):
        if not HAS_TASKBAR or not self.taskbar: return
        try:
            fh = root_widget.wm_frame()
            if fh and fh != "0x0": self.hwnd = int(fh, 16); return
        except Exception: pass
        try:
            wid = root_widget.winfo_id()
            self.hwnd = int(ctypes.windll.user32.GetAncestor(wid, 2) or ctypes.windll.user32.GetParent(wid) or wid)
        except Exception: self.hwnd = None

    def set_progress(self, current: int, total: int = 100, state: str = "normal"):
        if not self.taskbar or not self.hwnd: return
        try:
            self.taskbar.SetProgressState(self.hwnd, {"none": 0, "indeterminate": 1, "normal": 2, "error": 4, "paused": 8}.get(state, 2))
            if state in {"normal", "paused", "error"}: self.taskbar.SetProgressValue(self.hwnd, max(0, int(current)), max(1, int(total)))
        except Exception: pass


class DoHResolver:
    _orig_getaddrinfo, _lock, _tls = socket.getaddrinfo, threading.RLock(), threading.local()
    _cache: Dict[Tuple[str, int], Tuple[float, List[str]]] = {}
    _enabled, _doh_url, _doh_host = False, DOH_PROVIDERS["Cloudflare"], "cloudflare-dns.com"

    @classmethod
    def configure(cls, enabled: bool, doh_url: str):
        with cls._lock:
            url = (doh_url or "").strip() or DOH_PROVIDERS["Cloudflare"]
            cls._doh_url, cls._doh_host = url, (urlparse(url).hostname or "").lower()
            cls._cache.clear()
            if enabled and not cls._enabled:
                cls._enabled, socket.getaddrinfo = True, cls._patched_getaddrinfo
                LoggerSetup.log(f"DoH Resolver enabled ({url}).", "info")
            elif not enabled and cls._enabled:
                cls._enabled, socket.getaddrinfo = False, cls._orig_getaddrinfo
                LoggerSetup.log("DoH Resolver disabled.", "info")

    @classmethod
    def _sess(cls) -> requests.Session:
        s = getattr(cls._tls, "session", None)
        if s is None:
            s = requests.Session(); s.trust_env = False; cls._tls.session = s
        return s

    @classmethod
    def _query(cls, host: str, rr: str) -> List[str]:
        now, rnum = time.time(), (28 if rr == "AAAA" else 1)
        key = (host.lower(), rnum)
        with cls._lock:
            c = cls._cache.get(key)
            if c and c[0] > now: return list(c[1])
        ips, ttl = [], 120
        try:
            cls._tls.active = True
            resp = cls._sess().get(cls._doh_url, params={"name": host, "type": rr}, headers={"Accept": "application/dns-json"}, timeout=3.0)
            resp.raise_for_status()
            for ans in resp.json().get("Answer") or []:
                if ans.get("type") == rnum and ans.get("data"):
                    try:
                        ips.append(str(ipaddress.ip_address(str(ans["data"]).strip())))
                        ttl = min(ttl, safe_int(ans.get("TTL"), 120, 30, 600))
                    except ValueError: pass
        except Exception: ips = []
        finally: cls._tls.active = False
        with cls._lock: cls._cache[key] = (now + (ttl if ips else 15.0), list(ips))
        return ips

    @classmethod
    def _patched_getaddrinfo(cls, host, port, family=0, type=0, proto=0, flags=0):
        if not cls._enabled or getattr(cls._tls, "active", False) or host is None:
            return cls._orig_getaddrinfo(host, port, family, type, proto, flags)
        if flags & (getattr(socket, "AI_PASSIVE", 0) | getattr(socket, "AI_NUMERICHOST", 0)):
            return cls._orig_getaddrinfo(host, port, family, type, proto, flags)
        h = (host.decode("utf-8", errors="ignore") if isinstance(host, bytes) else str(host)).strip().lower()
        if not h or "." not in h or h in {"localhost", "localhost.localdomain"} or h.endswith(".local") or h == cls._doh_host:
            return cls._orig_getaddrinfo(host, port, family, type, proto, flags)
        try:
            ipaddress.ip_address(h); return cls._orig_getaddrinfo(host, port, family, type, proto, flags)
        except ValueError: pass
        if isinstance(port, int): p_int = port
        elif isinstance(port, str) and (port.isdigit() or port in {"http", "https"}): p_int = int(port) if port.isdigit() else (443 if port == "https" else 80)
        elif port is None: p_int = 0
        else: return cls._orig_getaddrinfo(host, port, family, type, proto, flags)
        st = type or socket.SOCK_STREAM
        sp = proto or (socket.IPPROTO_UDP if st == socket.SOCK_DGRAM else socket.IPPROTO_TCP)
        res = []
        if family in (0, socket.AF_INET): res.extend((socket.AF_INET, st, sp, "", (ip, p_int)) for ip in cls._query(h, "A"))
        if family == socket.AF_INET6 or (family == 0 and not res): res.extend((socket.AF_INET6, st, sp, "", (ip, p_int, 0, 0)) for ip in cls._query(h, "AAAA"))
        return res or cls._orig_getaddrinfo(host, port, family, type, proto, flags)

    @classmethod
    def test_connection(cls, doh_url: str, proxy_url: Optional[str] = None) -> Tuple[bool, str]:
        try:
            url = (doh_url or "").strip() or DOH_PROVIDERS["Cloudflare"]
            t0 = time.perf_counter()
            r = requests.get(url, params={"name": "www.youtube.com", "type": "A"}, headers={"Accept": "application/dns-json"}, timeout=6, proxies={"http": proxy_url, "https": proxy_url} if proxy_url else None)
            r.raise_for_status()
            ans = [str(a.get("data")) for a in (r.json().get("Answer") or []) if a.get("data")]
            ms = int((time.perf_counter() - t0) * 1000)
            return (True, f"DoH OK ({ms} ms) -> {', '.join(ans[:3])}") if ans else (False, f"DoH OK ({ms} ms) with no DNS answers.")
        except Exception as e: return False, f"DoH test failed: {e}"


class DigitalFingerprint:
    _UA_WIN = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    _UA_MAC = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"

    def __init__(self):
        self.ua = None
        if UserAgent is not None:
            try: self.ua = UserAgent(fallback=self._UA_WIN)
            except Exception: pass
        self._agents = [self._UA_WIN, self._UA_MAC]

    def get_random_headers(self) -> Dict[str, str]:
        try: agent = self.ua.random if self.ua else random.choice(self._agents)
        except Exception: agent = random.choice(self._agents)
        return {"User-Agent": agent, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9"}

    def get_yt_dlp_options(self, url: str = "") -> Dict[str, Any]:
        # SECURITY: TLS certificate verification stays ENABLED by default.
        # (v18 hardcoded nocheckcertificate=True, silently disabling it for all
        # traffic incl. cookie-authenticated requests.) Opt-in only via the
        # explicit 'allow_insecure_tls' setting, which logs a warning.
        opts: Dict[str, Any] = {"color": "no_color"}
        host = _url_host(url)
        if not (_host_is(host, "youtube.com") or _host_is(host, "youtu.be")):
            h = self.get_random_headers(); opts["user_agent"] = h["User-Agent"]; opts["http_headers"] = h
        return opts


def looks_like_netscape_cookie_text(text: str) -> bool:
    """True if the text looks like Netscape cookies.txt content (header or >=1
    valid 7-field tab-separated row)."""
    try:
        for i, line in enumerate((text or "").splitlines()):
            if i > 500:
                break
            s = line.strip()
            if not s:
                continue
            if s.startswith("#"):
                if "netscape" in s.lower() and "cookie" in s.lower():
                    return True
                continue
            parts = s.split("\t")
            if len(parts) >= 7 and parts[0]:
                return True
        return False
    except Exception:
        return False


def looks_like_netscape_cookie_file(path: Any) -> bool:
    """True if the file looks like a Netscape cookies.txt (header or >=1 valid
    7-field tab-separated row). Guards against handing a non-cookie .txt to
    yt-dlp, which otherwise aborts with 'does not look like a Netscape format
    cookies file' and triggers a pointless retry loop."""
    try:
        p = Path(str(path))
        if not p.is_file() or p.stat().st_size == 0:
            return False
        return looks_like_netscape_cookie_text(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return False


# --- SINA Cookie Bridge extension (customized from "Get cookies.txt LOCALLY") ---
# Rebuilt for this app: instead of manually exporting the active tab's cookies,
# it collects ALL cookies (chrome.cookies.getAll -> already decrypted, even with
# v20 app-bound encryption) and AUTO-PUSHES them to the app's localhost server.
# No browser restart, no CDP debug port, no data ever leaves the computer.
COOKIE_BRIDGE_EXTENSION_FILES: Dict[str, str] = {
    "manifest.json": """{
  "manifest_version": 3,
  "name": "SINA Cookie Bridge",
  "version": "3.0.0",
  "description": "Auto-syncs decrypted browser cookies to the local SINA Fusion Downloader app in real time. No data leaves your computer.",
  "minimum_chrome_version": "116",
  "permissions": ["cookies", "alarms", "storage", "contextMenus", "notifications", "downloads"],
  "host_permissions": ["<all_urls>", "http://127.0.0.1/*", "http://localhost/*"],
  "background": { "service_worker": "background.mjs", "type": "module" },
  "action": { "default_popup": "popup.html", "default_title": "SINA Cookie Bridge", "default_icon": { "16": "images/icon16.png", "48": "images/icon48.png", "128": "images/icon128.png" } },
  "icons": { "16": "images/icon16.png", "48": "images/icon48.png", "128": "images/icon128.png" },
  "options_ui": { "page": "options.html", "open_in_tab": false },
  "commands": { "push-cookies": { "suggested_key": { "default": "Ctrl+Shift+S" }, "description": "Send cookies to SINA now" } }
}
""",
    "modules/get_all_cookies.mjs": """// All cookies across ALL domains (the app needs YouTube/Google cookies
// regardless of which tab is active). chrome.cookies returns decrypted values.
export async function getAllCookies() {
  try {
    return await chrome.cookies.getAll({});
  } catch (e) {
    return [];
  }
}
""",
    "modules/cookie_format.mjs": """// Serialize cookies to Netscape cookies.txt (the format yt-dlp expects).
export function toNetscape(cookies) {
  const rows = cookies.map(({ domain, expirationDate, path, secure, name, value }) => {
    const includeSubDomain = !!domain && domain.startsWith('.');
    const expiry = expirationDate ? Math.floor(expirationDate) : 0;
    return [
      domain,
      includeSubDomain ? 'TRUE' : 'FALSE',
      path || '/',
      secure ? 'TRUE' : 'FALSE',
      String(expiry),
      name,
      value,
    ].join('\\t');
  });
  return [
    '# Netscape HTTP Cookie File',
    '# https://curl.haxx.se/rfc/cookie_spec.html',
    '# Generated by SINA Cookie Bridge',
    '',
    ...rows,
    '',
  ].join('\\n');
}
""",
    "background.mjs": """import { toNetscape } from './modules/cookie_format.mjs';
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
    const d = (c.domain || '').replace(/^\\./, '').toLowerCase();
    return MEDIA_DOMAINS.some((m) => d === m || d.endsWith('.' + m));
  });
}

function topDomains(cookies) {
  const m = {};
  for (const c of cookies) { const d = (c.domain || '').replace(/^\\./, ''); m[d] = (m[d] || 0) + 1; }
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
""",
    "popup.html": """<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <link rel="stylesheet" href="popup.css" />
</head>
<body>
  <header>
    <img src="images/icon48.png" width="28" height="28" alt="" />
    <div><h1>SINA Cookie Bridge</h1><div class="sub" id="ver">Real-time local sync</div></div>
    <span id="dot" class="dot"></span>
  </header>
  <div id="status" class="status">Checking…</div>
  <div class="stats">
    <div class="stat"><span id="count">0</span><label>cookies</label></div>
    <div class="stat"><span id="last">—</span><label>last push</label></div>
    <div class="stat"><span id="pushes">0</span><label>syncs</label></div>
  </div>
  <div id="domains" class="domains"></div>
  <label class="toggle"><input type="checkbox" id="auto" checked /> Auto-push (real time)</label>
  <button id="push">Push cookies now</button>
  <button id="export" class="secondary">Export cookies.txt…</button>
  <div class="row"><a href="#" id="options">Options</a><span class="hint">Ctrl+Shift+S</span></div>
  <p class="hint">Syncs automatically when the SINA app opens. Sent only to 127.0.0.1 — never leaves your computer.</p>
  <script src="popup.mjs" type="module"></script>
</body>
</html>
""",
    "popup.mjs": """import { BRIDGE_PORT } from './bridge_config.mjs';
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
""",
    "popup.css": """body { width: 300px; margin: 0; padding: 14px; font-family: Segoe UI, Arial, sans-serif; background: #0f172a; color: #e2e8f0; }
header { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
header img { border-radius: 8px; }
h1 { font-size: 15px; margin: 0; }
.sub { font-size: 11px; color: #64748b; }
.dot { width: 10px; height: 10px; border-radius: 50%; margin-left: auto; background: #64748b; }
.dot.ok { background: #4ade80; } .dot.bad { background: #f87171; }
.status { font-size: 13px; font-weight: 600; padding: 8px 10px; border-radius: 6px; background: #1e293b; }
.status.ok { color: #4ade80; } .status.bad { color: #f87171; }
.stats { display: flex; gap: 8px; margin: 12px 0; }
.stat { flex: 1; background: #1e293b; border-radius: 6px; padding: 8px 4px; text-align: center; }
.stat span { display: block; font-size: 15px; font-weight: 700; }
.stat label { font-size: 10px; color: #64748b; }
.domains { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 10px; }
.domain { font-size: 10px; background: #1e293b; color: #94a3b8; padding: 2px 6px; border-radius: 4px; }
.toggle { display: flex; align-items: center; gap: 6px; font-size: 12px; margin-bottom: 10px; cursor: pointer; }
button { width: 100%; padding: 9px; border: 0; border-radius: 6px; background: #2563eb; color: #fff; font-size: 13px; cursor: pointer; }
button.secondary { background: #334155; margin-top: 6px; }
button:disabled { opacity: .6; }
select { width: 100%; padding: 7px; border-radius: 6px; background: #1e293b; color: #e2e8f0; border: 1px solid #334155; font-size: 12px; }
.row { display: flex; justify-content: space-between; align-items: center; margin-top: 10px; }
.row a { color: #60a5fa; font-size: 12px; text-decoration: none; }
.hint { font-size: 11px; color: #64748b; margin: 10px 0 0; }
.field { margin-bottom: 10px; }
.field label { display: block; font-size: 12px; margin-bottom: 4px; color: #94a3b8; }
""",
    "options.html": """<!doctype html>
<html>
<head><meta charset="utf-8" /><link rel="stylesheet" href="popup.css" /></head>
<body style="width:320px">
  <header><img src="images/icon48.png" width="28" height="28" alt="" /><div><h1>Bridge Options</h1><div class="sub">SINA Cookie Bridge v3</div></div></header>
  <label class="toggle"><input type="checkbox" id="auto" checked /> Auto-push cookies (real time)</label>
  <label class="toggle"><input type="checkbox" id="notify" /> Notify on connect / disconnect</label>
  <div class="field">
    <label for="domainMode">Cookies to sync</label>
    <select id="domainMode">
      <option value="all">All sites (maximum compatibility)</option>
      <option value="media">Media sites only (YouTube, Google, Instagram…)</option>
    </select>
  </div>
  <div class="status" id="conn">Testing connection…</div>
  <button id="test">Test connection</button>
  <button id="push" class="secondary" style="margin-top:8px;background:#16a34a">Push cookies now</button>
  <p class="hint">The extension connects automatically when the SINA app opens and pushes cookie changes within ~1.5s. The app listens on 127.0.0.1 only with a private token; cookies never leave your computer.</p>
  <script src="options.mjs" type="module"></script>
</body>
</html>
""",
    "options.mjs": """import { BRIDGE_PORT } from './bridge_config.mjs';
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
""",
}


BRIDGE_TOKEN_FILE = COOKIE_BRIDGE_DIR / "bridge_token.txt"


def get_bridge_token() -> str:
    """Stable per-install secret shared by the extension and the bridge server.
    Blocks cookie injection by other local processes / a squatter on the port."""
    try:
        if BRIDGE_TOKEN_FILE.exists():
            t = BRIDGE_TOKEN_FILE.read_text(encoding="utf-8").strip()
            if t:
                return t
    except OSError:
        pass
    t = secrets.token_hex(16)
    try:
        COOKIE_BRIDGE_DIR.mkdir(parents=True, exist_ok=True)
        BRIDGE_TOKEN_FILE.write_text(t, encoding="utf-8")
        try: os.chmod(BRIDGE_TOKEN_FILE, 0o600)
        except OSError: pass
    except OSError:
        pass
    return t


def _generate_bridge_icons(d: Path):
    try:
        from PIL import Image, ImageDraw
        img = Image.new("RGBA", (128, 128), (37, 99, 235, 255))
        dr = ImageDraw.Draw(img)
        dr.ellipse((24, 24, 104, 104), fill=(245, 222, 179, 255))  # cookie
        for (x, y, r) in ((48, 50, 6), (78, 44, 5), (66, 70, 7), (44, 80, 5), (86, 78, 6)):
            dr.ellipse((x - r, y - r, x + r, y + r), fill=(92, 64, 51, 255))  # chips
        (d / "images").mkdir(parents=True, exist_ok=True)
        img.save(d / "images" / "icon128.png")
        resample = getattr(Image, "Resampling", Image).LANCZOS
        for s in (48, 16):
            img.resize((s, s), resample).save(d / "images" / f"icon{s}.png")
    except Exception as e:
        LoggerSetup.log(f"Could not generate bridge icons: {e}", "debug")


def materialize_cookie_bridge_extension() -> Path:
    """Write the custom cookie-bridge extension to the stable shared folder so
    the user can load it (unpacked) into their browser. Idempotent. Injects the
    per-install secret token and generates icons."""
    d = COOKIE_BRIDGE_DIR
    d.mkdir(parents=True, exist_ok=True)
    token = get_bridge_token()
    for name, content in COOKIE_BRIDGE_EXTENSION_FILES.items():
        fp = d / name
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content, encoding="utf-8", newline="\n")
    (d / "bridge_config.mjs").write_text(
        f"export const BRIDGE_PORT = {COOKIE_BRIDGE_PORT};\nexport const BRIDGE_TOKEN = '{token}';\n",
        encoding="utf-8", newline="\n")
    _generate_bridge_icons(d)
    return d


class CookieBridgeServer:
    """Tiny localhost HTTP server that receives cookies from the SINA Cookie
    Bridge extension and writes them to BRIDGE_COOKIE_FILE.

    Security: bound to 127.0.0.1 only; POST requires Content-Type application/json,
    which forces a CORS preflight that we never approve - so drive-by web pages
    cannot push cookies, while the extension (host_permissions) can.
    """

    def __init__(self, port: int = COOKIE_BRIDGE_PORT):
        self.port = port
        self.httpd: Optional[http.server.ThreadingHTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        self.last_push = 0.0
        self.last_count = 0
        self.received = 0

    def start(self) -> bool:
        server = self
        self.token = get_bridge_token()

        class Handler(http.server.BaseHTTPRequestHandler):
            timeout = 10  # bound slow/stalled clients (anti thread-exhaustion)

            def log_message(self, *a):
                pass

            def _host_ok(self) -> bool:
                # Anti DNS-rebinding: even if attacker.com resolves to 127.0.0.1,
                # the Host header stays attacker.com -> reject.
                host = (self.headers.get("Host") or "").split(":")[0].strip().lower()
                return host in ("127.0.0.1", "localhost", "")

            def _send(self, code: int, obj: Dict[str, Any]):
                body = json.dumps(obj).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Connection", "close")
                self.end_headers()
                try:
                    self.wfile.write(body)
                except Exception:
                    pass

            def do_GET(self):
                if not self._host_ok():
                    self._send(403, {"ok": False})
                    return
                if self.path.split("?")[0] == "/ping":
                    st = server.status()
                    self._send(200, {"ok": True, "app": APP_NAME, "version": APP_VERSION,
                                     "received": st["received"], "cookies": st["last_count"]})
                else:
                    self._send(404, {"ok": False})

            def do_OPTIONS(self):
                # Deliberately NO Access-Control-Allow-* headers: a cross-origin
                # web page's preflight fails, blocking drive-by cookie injection.
                self.send_response(204)
                self.send_header("Connection", "close")
                self.end_headers()

            def do_POST(self):
                if not self._host_ok():
                    self._send(403, {"ok": False, "error": "bad host"})
                    return
                if self.path.split("?")[0] != "/cookies":
                    self._send(404, {"ok": False})
                    return
                # Per-install secret: stops other local processes / port squatters.
                tok = self.headers.get("X-Bridge-Token") or ""
                if not hmac.compare_digest(tok, server.token):
                    self._send(401, {"ok": False, "error": "bad token"})
                    return
                ctype = (self.headers.get("Content-Type") or "").lower()
                if "application/json" not in ctype:
                    self._send(415, {"ok": False, "error": "application/json required"})
                    return
                try:
                    n = int(self.headers.get("Content-Length") or 0)
                    if n <= 0 or n > 8_000_000:
                        self._send(400, {"ok": False, "error": "bad length"})
                        return
                    data = json.loads(self.rfile.read(n).decode("utf-8"))
                    text = data.get("netscape") or ""
                    # Require real cookie rows - an empty/header-only jar must never
                    # overwrite the app's good cookies.
                    rows = sum(1 for ln in text.splitlines()
                               if ln.strip() and not ln.startswith("#") and len(ln.split("\t")) >= 7)
                    if rows == 0 or not looks_like_netscape_cookie_text(text):
                        self._send(400, {"ok": False, "error": "no cookie rows"})
                        return
                    p = Path(BRIDGE_COOKIE_FILE)
                    p.parent.mkdir(parents=True, exist_ok=True)
                    tmp = p.with_suffix(f".{threading.get_ident()}.tmp")
                    tmp.write_text(text, encoding="utf-8", newline="\n")
                    os.replace(tmp, p)
                    try: os.chmod(p, 0o600)
                    except OSError: pass
                    with server._lock:
                        server.last_push = time.time()
                        server.last_count = int(data.get("count") or rows)
                        server.received += 1
                        cnt = server.last_count
                    LoggerSetup.log(f"Cookie Bridge: received {cnt} cookies from the browser extension.", "info")
                    self._send(200, {"ok": True, "received": cnt})
                except Exception as e:
                    LoggerSetup.log(f"Cookie Bridge POST error: {e}", "warning")
                    self._send(500, {"ok": False, "error": str(e)})

        try:
            self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", self.port), Handler)
        except OSError as e:
            LoggerSetup.log(f"Cookie Bridge server could not start on port {self.port}: {e}", "warning")
            return False
        self.thread = threading.Thread(target=self.httpd.serve_forever, name="CookieBridge", daemon=True)
        self.thread.start()
        LoggerSetup.log(f"Cookie Bridge server listening on http://127.0.0.1:{self.port} (extension auto-push).", "info")
        return True

    def stop(self):
        if self.httpd is not None:
            try:
                self.httpd.shutdown()
                self.httpd.server_close()
            except Exception:
                pass
            self.httpd = None

    def status(self) -> Dict[str, Any]:
        with self._lock:
            return {"running": self.httpd is not None, "last_push": self.last_push,
                    "last_count": self.last_count, "received": self.received}


class CookieGenerator:
    # Single-flight: two concurrent warm-ups (e.g. two workers hitting auth
    # errors at once) must not launch two headless browsers / interleave writes.
    _gen_lock = threading.Lock()

    def __init__(self, cookie_path: str):
        self.cookie_path = cookie_path

    def generate(self) -> Tuple[bool, str]:
        if not sync_playwright and not reload_playwright():
            return False, "Playwright not installed. Use Settings > Cookie Helper > 'Install Playwright Engine', or run in PowerShell: pip install playwright; playwright install chromium"
        if not self._gen_lock.acquire(blocking=False):
            return False, "Cookie warm-up already in progress - skipped duplicate run."
        try:
            return self._generate_locked()
        finally:
            self._gen_lock.release()

    def _generate_locked(self) -> Tuple[bool, str]:
        LoggerSetup.log("Starting anonymous cookie warm-up with Playwright...", "info")
        try:
            with sync_playwright() as p:
                # Preflight: the pip package can be present while its browser
                # binaries were never downloaded (playwright install chromium).
                # Fail fast with a clear, actionable message instead of a huge
                # launch traceback.
                exe = Path(p.chromium.executable_path)
                LoggerSetup.log(f"Playwright Chromium binary: {exe} (exists={exe.exists()})", "debug")
                if not exe.exists():
                    return False, ("Playwright browser binaries are missing. Open Settings > Cookie Helper > "
                                   "'Install Playwright Engine' (one click), or run in PowerShell: "
                                   "python -m playwright install chromium")
                # Playwright 1.49+ defaults headless launches to a SEPARATE
                # "chrome-headless-shell" binary that is often not installed (and
                # whose download from cdn.playwright.dev is geo-blocked in some
                # regions). channel="chromium" forces the FULL Chromium binary in
                # the new headless mode - it never needs the headless shell.
                # Fall back to an explicit executable_path if the channel is unavailable.
                try:
                    browser = p.chromium.launch(headless=True, channel="chromium")
                except Exception as launch_err:
                    LoggerSetup.log(f"Warm-up: channel launch failed ({str(launch_err).splitlines()[0][:120]}); retrying with executable_path.", "debug")
                    browser = p.chromium.launch(headless=True, executable_path=str(exe))
                try:
                    ctx = browser.new_context(user_agent=DigitalFingerprint().get_random_headers()["User-Agent"], viewport={"width": 1280, "height": 720}, locale="en-US")
                    page = ctx.new_page()
                    LoggerSetup.log("Warm-up: navigating to youtube.com ...", "debug")
                    page.goto("https://www.youtube.com", timeout=60000, wait_until="domcontentloaded"); time.sleep(2.5)
                    for sel in ("button[aria-label='Accept all']", "button:has-text('Accept all')", "button:has-text('I agree')"):
                        try: page.click(sel, timeout=1500); LoggerSetup.log(f"Warm-up: clicked consent '{sel}'", "debug"); break
                        except Exception: pass
                    page.mouse.wheel(0, 400); time.sleep(1.0); cookies = ctx.cookies()
                    LoggerSetup.log(f"Warm-up: collected {len(cookies)} anonymous cookies.", "debug")
                finally:
                    browser.close()
            p_out = Path(self.cookie_path); p_out.parent.mkdir(parents=True, exist_ok=True)
            tmp = p_out.with_suffix(p_out.suffix + f".{threading.get_ident()}.tmp")
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write("# Netscape HTTP Cookie File\n")
                for c in cookies:
                    dom = c.get("domain", "")
                    exp = int(c.get("expires") or 0)
                    if exp < 0: exp = 0  # Playwright session cookies (-1) -> Netscape session (0)
                    f.write(f"{dom}\t{'TRUE' if dom.startswith('.') else 'FALSE'}\t{c.get('path', '/')}\t{'TRUE' if c.get('secure') else 'FALSE'}\t{exp}\t{c.get('name', '')}\t{c.get('value', '')}\n")
            os.replace(tmp, p_out)
            try: os.chmod(p_out, 0o600)
            except OSError: pass
            return True, f"Generated {len(cookies)} cookies at {self.cookie_path}"
        except Exception as e:
            msg = str(e).splitlines()[0][:300]
            LoggerSetup.log(f"Cookie gen failed: {msg}", "error")
            return False, msg


class BrowserCookieExtractor:
    """Extract cookies straight from browser profile databases into Netscape format.

    Fixes the classic yt-dlp failures ("could not copy chrome cookie database",
    DPAPI/locked-DB errors) by:
      * copying the SQLite DB safely (backup API, then raw copy) so it works
        even while the browser is RUNNING,
      * decrypting Chromium v10/v11 cookie values with DPAPI + AES-256-GCM,
      * reading Firefox cookies.sqlite directly (values are plaintext).
    Supported: Windows Chromium family (chrome/edge/brave/opera/vivaldi/chromium)
    and Firefox on all platforms. Other cases fall back to yt-dlp's own engine.
    """

    _last_copy_error: str = ""

    @staticmethod
    def _chromium_dirs() -> Dict[str, List[Path]]:
        la = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
        ro = Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming")))
        return {
            "chrome": [la / "Google" / "Chrome" / "User Data"],
            "edge": [la / "Microsoft" / "Edge" / "User Data"],
            "brave": [la / "BraveSoftware" / "Brave-Browser" / "User Data"],
            "vivaldi": [la / "Vivaldi" / "User Data"],
            "chromium": [la / "Chromium" / "User Data"],
            "opera": [ro / "Opera Software" / "Opera Stable", ro / "Opera Software" / "Opera GX Stable"],
        }

    @staticmethod
    def _firefox_root() -> Path:
        if sys.platform == "win32":
            return Path(os.environ.get("APPDATA", "")) / "Mozilla" / "Firefox" / "Profiles"
        if sys.platform == "darwin":
            return Path.home() / "Library" / "Application Support" / "Firefox" / "Profiles"
        return Path.home() / ".mozilla" / "firefox"

    @classmethod
    def browser_installed(cls, browser: str) -> bool:
        """True if the browser's profile/cookie database actually exists on disk."""
        b = (browser or "").strip().lower()
        if b == "firefox":
            root = cls._firefox_root()
            return root.exists() and any((p / "cookies.sqlite").is_file() for p in root.iterdir() if p.is_dir())
        if sys.platform != "win32":
            return False
        for base in cls._chromium_dirs().get(b, []):
            if not base.exists():
                continue
            for prof in [base / "Default"] + sorted(base.glob("Profile *")) + [base]:
                if (prof / "Network" / "Cookies").is_file() or (prof / "Cookies").is_file():
                    return True
        return False

    @classmethod
    def detect_installed_browser(cls) -> Optional[str]:
        """Pick a browser that is actually installed (preference order)."""
        for b in ("brave", "chrome", "edge", "vivaldi", "opera", "chromium", "firefox"):
            if cls.browser_installed(b):
                LoggerSetup.log(f"Auto-detected installed cookie browser: {b}", "debug")
                return b
        return None

    @classmethod
    def resolve_browser(cls, browser: str) -> str:
        """Resolve 'auto' / missing / uninstalled browsers to a concrete installed one."""
        b = (browser or "auto").strip().lower()
        if b in ("", "auto", "default"):
            return cls.detect_installed_browser() or "chrome"
        if b == "firefox" or (sys.platform == "win32" and b in cls._chromium_dirs()):
            if cls.browser_installed(b):
                return b
            alt = cls.detect_installed_browser()
            if alt:
                LoggerSetup.log(f"Cookie browser '{b}' not installed; using detected '{alt}' instead.", "debug")
                return alt
        return b

    @staticmethod
    def _dpapi_decrypt(data: bytes) -> bytes:
        import ctypes
        import ctypes.wintypes as wt

        class DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

        blob_in = DATA_BLOB(len(data), ctypes.create_string_buffer(data, len(data)))
        blob_out = DATA_BLOB()
        ok = ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out))
        if not ok:
            raise OSError("CryptUnprotectData failed (DPAPI).")
        try:
            return ctypes.string_at(blob_out.pbData, blob_out.cbData)
        finally:
            ctypes.windll.kernel32.LocalFree(blob_out.pbData)

    @classmethod
    def _chromium_key(cls, base: Path) -> Optional[bytes]:
        try:
            ls = base / "Local State"
            if not ls.exists(): return None
            enc_key = json.loads(ls.read_text(encoding="utf-8")).get("os_crypt", {}).get("encrypted_key", "")
            raw = base64.b64decode(enc_key)
            if raw.startswith(b"DPAPI"):
                key = cls._dpapi_decrypt(raw[5:])
                return key if len(key) == 32 else None
        except Exception as e:
            LoggerSetup.log(f"Cookie key extraction failed: {e}", "debug")
        return None

    @staticmethod
    def _win_shared_copy(src: Path, dst: Path) -> bool:
        """Copy a file even while another process holds it, using Win32 CreateFileW
        with FILE_SHARE_READ|WRITE|DELETE (the technique browser-cookie tools use).
        Also copies the SQLite -wal/-shm sidecars so the latest committed rows are
        recovered. Returns False if the owner holds an exclusive lock (modern
        Chromium does this while running -> use the CDP path instead)."""
        if sys.platform != "win32":
            return False
        import ctypes
        import ctypes.wintypes as wt
        k32 = ctypes.windll.kernel32
        k32.CreateFileW.restype = wt.HANDLE
        k32.CreateFileW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD, ctypes.c_void_p, wt.DWORD, wt.DWORD, wt.HANDLE]
        k32.ReadFile.argtypes = [wt.HANDLE, ctypes.c_void_p, wt.DWORD, ctypes.POINTER(wt.DWORD), ctypes.c_void_p]
        k32.GetFileSizeEx.argtypes = [wt.HANDLE, ctypes.POINTER(ctypes.c_longlong)]
        INVALID = ctypes.c_void_p(-1).value
        SHARE = 0x1 | 0x2 | 0x4  # READ | WRITE | DELETE

        def copy_one(s: Path, d: Path):
            h = k32.CreateFileW(str(s), 0x80000000, SHARE, None, 3, 0, None)
            if h == INVALID or h is None:
                raise OSError(f"CreateFileW sharing violation (err={ctypes.GetLastError()})")
            try:
                size = ctypes.c_longlong(0)
                k32.GetFileSizeEx(h, ctypes.byref(size))
                with open(d, "wb") as f:
                    remaining, buf = size.value, ctypes.create_string_buffer(1048576)
                    while remaining > 0:
                        got = wt.DWORD(0)
                        if not k32.ReadFile(h, buf, min(remaining, 1048576), ctypes.byref(got), None) or got.value == 0:
                            raise OSError(f"ReadFile err={ctypes.GetLastError()}")
                        f.write(buf.raw[:got.value])
                        remaining -= got.value
            finally:
                k32.CloseHandle(h)

        try:
            copy_one(src, dst)
            for suf in ("-wal", "-shm"):
                side = src.parent / (src.name + suf)
                if side.is_file():
                    try:
                        copy_one(side, Path(str(dst) + suf))
                    except OSError:
                        pass
            return True
        except Exception as e:
            BrowserCookieExtractor._last_copy_error = str(e)
            LoggerSetup.log(f"Shared-read copy failed for {src.name}: {e}", "debug")
            return False

    @staticmethod
    def _copy_db(src: Path, dst: Path) -> bool:
        BrowserCookieExtractor._last_copy_error = ""
        LoggerSetup.log(f"Copying cookie DB: {src}", "debug")
        try:
            con = sqlite3.connect(src.resolve().as_uri() + "?mode=ro", uri=True, timeout=3)
            try:
                out = sqlite3.connect(str(dst))
                try:
                    con.backup(out)
                    LoggerSetup.log("Cookie DB copied via SQLite backup API.", "debug")
                    return True
                finally:
                    out.close()
            finally:
                con.close()
        except Exception as e:
            BrowserCookieExtractor._last_copy_error = str(e)
            LoggerSetup.log(f"SQLite backup copy failed: {e}", "debug")
        try:
            shutil.copyfile(src, dst)
            LoggerSetup.log("Cookie DB copied via raw file copy.", "debug")
            return True
        except Exception as e:
            BrowserCookieExtractor._last_copy_error = str(e)
            LoggerSetup.log(f"Raw file copy failed: {e}", "debug")
        if BrowserCookieExtractor._win_shared_copy(src, dst):
            LoggerSetup.log("Cookie DB copied via Win32 shared-read (browser may be open).", "debug")
            return True
        return False

    @staticmethod
    def _decrypt_value(ev: bytes, key: Optional[bytes]) -> Optional[str]:
        if not ev: return ""
        if ev[:3] in (b"v10", b"v11"):
            if key and HAS_CRYPTO:
                try:
                    nonce, payload, tag = ev[3:15], ev[15:-16], ev[-16:]
                    return AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(payload, tag).decode("utf-8", errors="replace")
                except Exception:
                    return None
            return None
        if ev[:3] == b"v20":
            return None  # app-bound encryption (Chrome 127+): not decryptable outside the browser
        try:
            return ev.decode("utf-8")
        except Exception:
            return None

    @classmethod
    def _chromium_rows(cls, browser: str) -> List[Tuple]:
        rows: List[Tuple] = []
        for base in cls._chromium_dirs().get(browser, []):
            if not base.exists(): continue
            key = cls._chromium_key(base)
            profiles = [base / "Default"] + sorted(base.glob("Profile *")) + [base]
            for prof in profiles:
                db = prof / "Network" / "Cookies"  # Chromium 96+ location
                if not db.is_file(): db = prof / "Cookies"  # legacy location
                if not db.is_file(): continue
                tmp = DATA_DIR / f".cookie_copy_{os.getpid()}_{threading.get_ident()}.sqlite"
                try:
                    if not cls._copy_db(db, tmp): continue
                    con = sqlite3.connect(str(tmp))
                    try:
                        try:
                            raw = con.execute("SELECT host_key, name, encrypted_value, path, expires_utc, is_secure FROM cookies").fetchall()
                            dec = True
                        except sqlite3.OperationalError:
                            raw = con.execute("SELECT host_key, name, value, path, expires_utc, is_secure FROM cookies").fetchall()
                            dec = False
                        for host, name, val, path, exp_utc, secure in raw:
                            value = cls._decrypt_value(val, key) if dec else (val or "")
                            if value is None or not name: continue
                            expiry = int(exp_utc / 1_000_000 - 11644473600) if exp_utc else 0
                            if expiry < 0: expiry = 0
                            rows.append((host, "TRUE" if str(host).startswith(".") else "FALSE", path or "/", "TRUE" if secure else "FALSE", expiry, name, value))
                    finally:
                        con.close()
                except Exception as e:
                    LoggerSetup.log(f"Cookie DB read failed ({prof}): {e}", "debug")
                finally:
                    try: tmp.unlink(missing_ok=True)
                    except OSError: pass
                if rows: break  # first profile that yields cookies wins
            if rows: break
        return rows

    @classmethod
    def _firefox_rows(cls) -> List[Tuple]:
        if sys.platform == "win32":
            root = Path(os.environ.get("APPDATA", "")) / "Mozilla" / "Firefox" / "Profiles"
        elif sys.platform == "darwin":
            root = Path.home() / "Library" / "Application Support" / "Firefox" / "Profiles"
        else:
            root = Path.home() / ".mozilla" / "firefox"
        if not root.exists(): return []
        profiles = sorted(root.glob("*.default-release")) + sorted(root.glob("*.default*")) + sorted(root.iterdir())
        rows: List[Tuple] = []
        for prof in profiles:
            db = prof / "cookies.sqlite"
            if not db.is_file(): continue
            tmp = DATA_DIR / f".cookie_copy_{os.getpid()}_{threading.get_ident()}.sqlite"
            try:
                if not cls._copy_db(db, tmp): continue
                con = sqlite3.connect(str(tmp))
                try:
                    for host, name, value, path, expiry, secure in con.execute("SELECT host, name, value, path, expiry, isSecure FROM moz_cookies"):
                        if not name: continue
                        rows.append((host, "TRUE" if str(host).startswith(".") else "FALSE", path or "/", "TRUE" if secure else "FALSE", int(expiry or 0), name, value or ""))
                finally:
                    con.close()
            except Exception as e:
                LoggerSetup.log(f"Firefox cookie read failed ({prof}): {e}", "debug")
            finally:
                try: tmp.unlink(missing_ok=True)
                except OSError: pass
            if rows: break
        return rows

    @staticmethod
    def _write_netscape(rows: List[Tuple], dest: str) -> Tuple[bool, str]:
        """Atomically write cookie rows (host, include_subdomains, path, secure,
        expiry, name, value) to a Netscape cookies.txt with restrictive perms."""
        try:
            p = Path(dest); p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_suffix(p.suffix + f".{threading.get_ident()}.tmp")
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write("# Netscape HTTP Cookie File\n")
                for r in rows:
                    f.write("\t".join(str(x) for x in r) + "\n")
            os.replace(tmp, p)
            try: os.chmod(p, 0o600)  # best-effort: restrict cookie file permissions
            except OSError: pass
            yt_n = sum(1 for r in rows if "youtube" in str(r[0]) or "google" in str(r[0]))
            LoggerSetup.log(f"Wrote {len(rows)} cookies ({yt_n} YouTube/Google) -> {dest}", "debug")
            return True, f"Extracted {len(rows)} cookies ({yt_n} YouTube/Google) -> {dest}"
        except Exception as e:
            LoggerSetup.log(f"Failed writing cookie file: {e}", "error", exc_info=True)
            return False, f"Failed writing cookie file: {e}"

    @classmethod
    def extract(cls, browser: str, dest: str) -> Tuple[bool, str]:
        b = cls.resolve_browser(browser)
        cls._last_copy_error = ""
        LoggerSetup.log(f"Cookie extraction requested: browser='{browser}' -> resolved '{b}', dest={dest}", "debug")
        if b == "firefox":
            rows = cls._firefox_rows()
        elif sys.platform == "win32" and b in cls._chromium_dirs():
            rows = cls._chromium_rows(b)
        else:
            return False, f"Direct extraction for '{b}' needs Windows (Chromium) or Firefox. Use cookie source 'browser' instead."
        LoggerSetup.log(f"Direct DB extraction from '{b}' yielded {len(rows)} cookie rows.", "debug")
        if not rows:
            err = cls._last_copy_error.lower()
            locked = any(k in err for k in ("permission denied", "unable to open database", "locked", "busy", "sharing"))
            # Extension-style fallback: if the browser is running with a remote
            # debugging port open, harvest decrypted cookies via CDP (works even
            # for v20 app-bound encryption and exclusive file locks).
            if locked:
                port = CdpCookieExtractor.find_debug_port()
                if port:
                    LoggerSetup.log(f"DB locked; trying CDP harvest on running debug port {port}.", "debug")
                    ok, msg = CdpCookieExtractor.harvest(port, dest)
                    if ok:
                        return True, msg + " (via running-browser CDP)"
                return False, (f"'{b}' is RUNNING and has locked its cookie database (Windows limitation).\n\n"
                               f"Use Cookie Helper > 'Extract from OPEN browser (CDP)' - it works like a cookie\n"
                               f"extension and keeps your browser open. Or close {b} completely (incl. tray) and Extract Now.\n"
                               f"Tip: Firefox cookies can be read even while Firefox is open.")
            return False, f"No cookies could be extracted from '{b}'. Is the browser installed and used at least once?"
        ok, msg = cls._write_netscape(rows, dest)
        return ok, (msg.replace("Extracted", f"Extracted from {b}:", 1) if ok else msg)


class CdpCookieExtractor:
    """Extension-style cookie harvest via the Chrome DevTools Protocol (CDP).

    Cookie extensions (Get cookies.txt LOCALLY, Cookie-Editor, EditThisCookie...)
    read cookies through the browser's OWN chrome.cookies API. That returns
    already-DECRYPTED values - even for Chrome 127+ v20 app-bound encryption -
    and works while the browser holds an exclusive lock on its cookie file.
    CDP's cookie access is the same source, so we attach to a browser that has a
    remote-debugging port open and pull every cookie, then write a cookies.txt.
    This is the robust fix for "could not copy Chrome cookie database" while the
    browser is running.
    """

    DEBUG_PORTS = (9222, 9223, 9224, 9225, 9229, 9333, 9515)
    # Port used by the last successful CDP auto-fix. auto_fix_cdp picks a free
    # (often ephemeral) port, so remember it here - otherwise find_debug_port
    # could never rediscover the still-open browser for later automatic harvests.
    _last_port: Optional[int] = None

    @classmethod
    def find_debug_port(cls) -> Optional[int]:
        """Detect an already-running browser exposing a CDP endpoint."""
        ports = ([cls._last_port] if cls._last_port else []) + list(cls.DEBUG_PORTS)
        for port in ports:
            try:
                r = requests.get(f"http://127.0.0.1:{port}/json/version", timeout=1.5)
                if r.status_code != 200:
                    continue
                j = r.json()
                if "webSocketDebuggerUrl" not in j:
                    continue
                # Only trust a real Chromium browser - port 9229 is Node's inspector
                # and Electron apps (VS Code, Slack...) also expose CDP; harvesting
                # their cookies would write the WRONG application's data.
                browser_id = str(j.get("Browser") or "")
                if not any(k in browser_id for k in ("Chrome", "Chromium", "Edg", "Brave", "HeadlessChrome", "Opera", "Vivaldi")):
                    LoggerSetup.log(f"Ignoring non-browser CDP endpoint on port {port}: {browser_id}", "debug")
                    continue
                LoggerSetup.log(f"Found running browser CDP endpoint on port {port}: {browser_id}", "debug")
                return port
            except Exception:
                continue
        return None

    @staticmethod
    def free_port() -> int:
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        p = s.getsockname()[1]
        s.close()
        return p

    @staticmethod
    def wait_endpoint(port: int, timeout: float = 40.0) -> bool:
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if requests.get(f"http://127.0.0.1:{port}/json/version", timeout=2).status_code == 200:
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False

    @staticmethod
    def _cookies_to_rows(cookies: List[Dict[str, Any]]) -> List[Tuple]:
        rows: List[Tuple] = []
        for c in cookies:
            dom = c.get("domain", "")
            if not dom or not c.get("name"):
                continue
            exp = int(c.get("expires") or 0)
            if exp < 0:
                exp = 0  # session cookie
            rows.append((dom, "TRUE" if dom.startswith(".") else "FALSE", c.get("path", "/"),
                         "TRUE" if c.get("secure") else "FALSE", exp, c.get("name", ""), c.get("value", "")))
        return rows

    @classmethod
    def harvest(cls, port: int, dest: str) -> Tuple[bool, str]:
        """Attach to a running browser via CDP and write all decrypted cookies."""
        if not sync_playwright:
            return False, "Playwright is required for CDP harvest. Cookie Helper > 'Install Playwright Engine'."
        LoggerSetup.log(f"CDP harvest: connecting to http://127.0.0.1:{port}", "debug")
        try:
            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{port}", timeout=20000)
                try:
                    collected: List[Dict[str, Any]] = []
                    for ctx in browser.contexts:
                        try:
                            cs = ctx.cookies()
                            collected.extend(cs)
                            LoggerSetup.log(f"CDP context yielded {len(cs)} cookies.", "debug")
                        except Exception as e:
                            LoggerSetup.log(f"CDP context cookie read failed: {e}", "debug")
                    seen, uniq = set(), []
                    for c in collected:
                        k = (c.get("domain"), c.get("path"), c.get("name"))
                        if k in seen:
                            continue
                        seen.add(k)
                        uniq.append(c)
                    rows = cls._cookies_to_rows(uniq)
                    LoggerSetup.log(f"CDP harvest: {len(rows)} unique cookies collected.", "debug")
                    if not rows:
                        return False, "Connected to the browser but it returned no cookies."
                    return BrowserCookieExtractor._write_netscape(rows, dest)
                finally:
                    # Disconnects the CDP client only; the user's browser stays open.
                    try: browser.close()
                    except Exception: pass
        except Exception as e:
            msg = str(e).splitlines()[0][:300]
            LoggerSetup.log(f"CDP harvest failed: {msg}", "error", exc_info=True)
            return False, f"CDP harvest failed: {msg}"


class _HttpRangeFile:
    """Seekable read-only file-like over HTTP Range requests.

    Lets zipfile extract a SINGLE member (e.g. ffprobe.exe) from a large remote
    archive without downloading the whole thing - vital on slow connections.
    """

    def __init__(self, url: str, size: int, cancel: Optional[threading.Event] = None):
        self.url, self.size, self.pos = url, size, 0
        self.cancel = cancel
        self.fetched = 0
        self.on_fetch: Optional[Callable[[], None]] = None
        self._buf, self._buf_start = b"", 0
        self._chunk = 1048576

    def seekable(self): return True
    def readable(self): return True
    def tell(self): return self.pos

    def seek(self, off, whence=0):
        new = off if whence == 0 else (self.pos + off if whence == 1 else self.size + off)
        self.pos = max(0, min(new, self.size))
        return self.pos

    def read(self, n=-1):
        if self.cancel is not None and self.cancel.is_set():
            raise IOError("Cancelled")
        if n is None or n < 0: n = self.size - self.pos
        n = min(n, self.size - self.pos)
        if n <= 0: return b""
        out = b""
        while len(out) < n:
            need = n - len(out)
            p = self.pos + len(out)
            if self._buf and self._buf_start <= p < self._buf_start + len(self._buf):
                off = p - self._buf_start
                take = min(need, len(self._buf) - off)
                out += self._buf[off:off + take]
                continue
            end = min(p + max(self._chunk, need), self.size) - 1
            r = requests.get(self.url, headers={"Range": f"bytes={p}-{end}"}, timeout=(20, 120))
            if r.status_code == 206:
                data = r.content
            elif r.status_code == 200:
                data = r.content[p:end + 1]  # server ignored Range
            else:
                raise IOError(f"HTTP {r.status_code} during range read")
            if not data: raise IOError("Empty range response")
            self._buf, self._buf_start = data, p
            self.fetched += len(data)
            if self.on_fetch is not None:
                try: self.on_fetch()
                except Exception: pass
            out += data[:min(need, len(data))]
        self.pos += len(out)
        return out


class FFmpegInstaller:
    """One-click download/update of FFmpeg + ffprobe into the shared user-level
    folder (~/.sina_fusion/ffmpeg/bin) so every copy of the script finds it.

    Step 1: compact static ffmpeg (~30 MB, fastest on slow links), with the full
    BtbN build as fallback. Step 2: ffprobe via HTTP-Range partial extraction
    from the gyan.dev essentials zip (only the needed ~25 MB, not the full
    119 MB archive). Live progress, cancellation, binary verification.
    """

    SOURCES: List[Tuple[str, str]] = [
        ("https://github.com/eugeneware/ffmpeg-static/releases/latest/download/ffmpeg-win32-x64.gz", "gz"),
        ("https://github.com/BtbN/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip", "zip"),
    ]
    FFPROBE_PARTIAL_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    @classmethod
    def _ffprobe_from_zip(cls, url: str, dest: Path, progress: Callable[[float, str], None], cancel: threading.Event) -> bool:
        """Download ONLY ffprobe.exe from a remote zip using HTTP Range requests."""
        try:
            head = requests.head(url, timeout=25, allow_redirects=True)
            size = safe_int(head.headers.get("Content-Length"), 0, 0)
            if size <= 0: return False
            rf = _HttpRangeFile(url, size, cancel)
            with zipfile.ZipFile(rf) as zf:
                member = next((i for i in zf.infolist() if i.filename.lower().endswith("bin/ffprobe.exe")), None)
                if member is None: return False
                expected = max(1, member.compress_size)

                def report():
                    progress(min(0.99, rf.fetched / expected), f"Downloading ffprobe only: {format_bytes(rf.fetched, False)} / ~{format_bytes(expected, False)}")

                rf.on_fetch = report
                tmp = dest.with_suffix(".new")
                with zf.open(member) as fsrc, open(tmp, "wb") as fdst:
                    shutil.copyfileobj(fsrc, fdst, 1048576)
                os.replace(tmp, dest)
            return True
        except Exception as e:
            LoggerSetup.log(f"Partial ffprobe download failed: {e}", "warning")
            try: dest.with_suffix(".new").unlink(missing_ok=True)
            except OSError: pass
            return False

    @staticmethod
    def _download(url: str, dest: Path, progress: Callable[[float, str], None], cancel: threading.Event) -> bool:
        try:
            with requests.get(url, stream=True, timeout=(20, 90), allow_redirects=True) as r:
                r.raise_for_status()
                total = safe_int(r.headers.get("Content-Length"), 0, 0)
                done, t0, last_rep = 0, time.time(), 0.0
                with open(dest, "wb") as f:
                    for chunk in r.iter_content(262144):
                        if cancel.is_set():
                            progress(-1.0, "Cancelling..."); return False
                        if not chunk: continue
                        f.write(chunk); done += len(chunk)
                        now = time.time()
                        if now - last_rep >= 0.25:
                            last_rep = now
                            spd = done / max(0.001, now - t0)
                            if total > 0:
                                eta = (total - done) / max(1.0, spd)
                                progress(done / total, f"{format_bytes(done, False)} / {format_bytes(total, False)}  |  {format_bytes(spd, False)}/s  |  ETA {format_duration(eta)}")
                            else:
                                progress(-1.0, f"{format_bytes(done, False)} downloaded  |  {format_bytes(spd, False)}/s")
            return True
        except Exception as e:
            LoggerSetup.log(f"FFmpeg download failed ({url}): {e}", "warning")
            try: dest.unlink(missing_ok=True)
            except OSError: pass
            return False

    @classmethod
    def install(cls, progress: Callable[[float, str], None], cancel: threading.Event) -> Tuple[bool, str, Optional[str]]:
        if sys.platform != "win32":
            return False, "Auto-install currently supports Windows. Install FFmpeg via your package manager (apt/brew) and set its path.", None
        bin_dir = FFMPEG_SHARED_DIR
        try:
            bin_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return False, f"Cannot create install folder: {e}", None
        exe = bin_dir / "ffmpeg.exe"
        for url, kind in cls.SOURCES:
            if cancel.is_set(): return False, "Cancelled.", None
            progress(-1.0, f"Connecting to {urlparse(url).hostname}...")
            tmp = DATA_DIR / f"ffmpeg_download.{kind}"
            if not cls._download(url, tmp, progress, cancel):
                if cancel.is_set(): return False, "Cancelled.", None
                continue
            try:
                progress(-1.0, "Installing...")
                new_exe = exe.with_suffix(".new")
                if kind == "gz":
                    with gzip.open(tmp, "rb") as fsrc, open(new_exe, "wb") as fdst:
                        shutil.copyfileobj(fsrc, fdst, 1048576)
                else:
                    with zipfile.ZipFile(tmp) as zf:
                        member = next((n for n in zf.namelist() if n.lower().endswith("bin/ffmpeg.exe")), None)
                        if not member: raise RuntimeError("ffmpeg.exe not found in archive")
                        with zf.open(member) as fsrc, open(new_exe, "wb") as fdst:
                            shutil.copyfileobj(fsrc, fdst, 1048576)
                        probe_member = next((n for n in zf.namelist() if n.lower().endswith("bin/ffprobe.exe")), None)
                        if probe_member:
                            probe_new = (bin_dir / "ffprobe.exe").with_suffix(".new")
                            with zf.open(probe_member) as fsrc, open(probe_new, "wb") as fdst:
                                shutil.copyfileobj(fsrc, fdst, 1048576)
                            os.replace(probe_new, bin_dir / "ffprobe.exe")
                try: tmp.unlink(missing_ok=True)
                except OSError: pass
                # VERIFY BEFORE REPLACING: a corrupt/incomplete download must never
                # overwrite a working FFmpeg installation.
                progress(-1.0, "Verifying binary...")
                vr = subprocess.run([str(new_exe), "-version"], capture_output=True, text=True, timeout=30)
                if vr.returncode != 0: raise RuntimeError("ffmpeg -version failed (corrupt download?)")
                ver = (vr.stdout or "").splitlines()[0][:80]
                os.replace(new_exe, exe)
                probe = bin_dir / "ffprobe.exe"
                if not probe.exists() and not cancel.is_set():
                    progress(-1.0, "Fetching ffprobe (partial download, only the needed bytes)...")
                    if not cls._ffprobe_from_zip(cls.FFPROBE_PARTIAL_URL, probe, progress, cancel):
                        LoggerSetup.log("ffprobe unavailable (optional). Install 'mutagen' for thumbnail embedding without ffprobe.", "warning")
                probe_note = "ffprobe: installed." if probe.exists() else "ffprobe: not available (optional; mutagen covers most embedding)."
                return True, f"FFmpeg installed/updated successfully.\n{ver}\n{probe_note}\nLocation: {exe}", str(exe)
            except Exception as e:
                LoggerSetup.log(f"FFmpeg install step failed: {e}", "warning")
                try: tmp.unlink(missing_ok=True)
                except OSError: pass
                try: exe.with_suffix(".new").unlink(missing_ok=True)
                except OSError: pass
                continue
        return False, "FFmpeg could not be downloaded from any source. Check your internet connection and try again.", None


class BrowserCookieFixer:
    """Gracefully close a Chromium browser, extract its cookies, then reopen it.

    Chromium locks its cookie DB while running (Windows sharing violation).
    This helper closes the browser with WM_CLOSE (normal exit, session saved),
    waits for it to exit, extracts cookies, and relaunches it with
    --restore-last-session so the user's tabs come back.
    """

    # NOTE: 'chromium' is intentionally NOT aliased to chrome.exe - that would
    # kill Google Chrome when the user asked to fix Chromium. Auto-Fix reports
    # 'unsupported' for it instead; use Extract Now after closing it manually.
    PROC: Dict[str, str] = {"chrome": "chrome.exe", "edge": "msedge.exe", "brave": "brave.exe", "vivaldi": "vivaldi.exe", "opera": "opera.exe"}

    @staticmethod
    def _running(pname: str) -> bool:
        try:
            out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {pname}", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=15).stdout
            return pname.lower() in out.lower()
        except Exception:
            return False

    @staticmethod
    def _exe_path(pname: str) -> Optional[str]:
        if psutil is not None:
            try:
                for p in psutil.process_iter(["name", "exe"]):
                    if (p.info.get("name") or "").lower() == pname and p.info.get("exe"):
                        return p.info["exe"]
            except Exception:
                pass
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\{pname}") as k:
                v = str(winreg.QueryValueEx(k, "")[0]).strip('"')
                if v and os.path.exists(v): return v
        except Exception:
            pass
        return None

    @classmethod
    def auto_fix(cls, browser: str, dest: str, progress: Optional[Callable[[str], None]] = None) -> Tuple[bool, str]:
        if sys.platform != "win32":
            return False, "Auto-fix is supported on Windows only."
        b = (browser or "chrome").strip().lower()
        pname = cls.PROC.get(b)
        if not pname:
            return False, f"Auto-fix is not supported for '{b}'. Use 'Extract Now' after closing the browser, or import a cookies.txt."
        say_raw = progress or (lambda _t: None)

        def say(t: str):
            # Progress may target a dialog that the user closed mid-run. A raise
            # here must NOT abort auto-fix after taskkill (browser left killed).
            try: say_raw(t)
            except Exception: pass

        exe = cls._exe_path(pname)
        was_running = cls._running(pname)
        if was_running:
            say(f"Closing {b} gracefully (session is saved)...")
            try:
                subprocess.run(["taskkill", "/IM", pname, "/T"], capture_output=True, timeout=30)
            except Exception:
                pass
            for _ in range(40):
                if not cls._running(pname): break
                time.sleep(0.5)
            if cls._running(pname):
                return False, f"{b} did not close in time. Close it manually (check the tray) and press 'Extract Now'."
            say("Browser closed. Extracting cookies...")
        ok, msg = False, "Cookie extraction did not run."
        try:
            ok, msg = BrowserCookieExtractor.extract(b, dest)
        except Exception as e:
            ok, msg = False, f"Cookie extraction failed: {e}"
        finally:
            # Guarantee the browser is reopened even if extraction raises.
            if was_running and exe:
                try:
                    subprocess.Popen([exe, "--restore-last-session"], close_fds=True)
                    msg += "\nBrowser reopened with your previous session."
                except Exception as e:
                    msg += f"\nCould not reopen browser automatically: {e}"
        return ok, msg

    @classmethod
    def auto_fix_cdp(cls, browser: str, dest: str, progress: Optional[Callable[[str], None]] = None) -> Tuple[bool, str]:
        """Extension-style fix that works even while the browser is running.

        Gracefully close the browser, relaunch it with a local remote-debugging
        port + --restore-last-session, then harvest DECRYPTED cookies via CDP
        (the same source cookie extensions use). The browser STAYS OPEN afterwards
        with the user's tabs restored. Handles v20 app-bound encryption and the
        exclusive cookie-file lock that defeats direct DB copying.
        """
        if sys.platform != "win32":
            return False, "CDP auto-fix is supported on Windows only."
        b = BrowserCookieExtractor.resolve_browser(browser)
        pname = cls.PROC.get(b)
        if not pname:
            return False, f"CDP auto-fix is not supported for '{b}'. Use 'Extract Now' (browser closed) or import cookies.txt."
        say_raw = progress or (lambda _t: None)

        def say(t: str):
            try: say_raw(t)
            except Exception: pass

        exe = cls._exe_path(pname)
        if not exe:
            return False, f"Could not locate the {b} executable on this system."
        LoggerSetup.log(f"CDP auto-fix: browser={b} exe={exe}", "debug")
        port = CdpCookieExtractor.free_port()
        was_running = cls._running(pname)
        if was_running:
            say(f"Closing {b} gracefully (your session/tabs are saved)...")
            try:
                subprocess.run(["taskkill", "/IM", pname, "/T"], capture_output=True, timeout=30)
            except Exception:
                pass
            for _ in range(40):
                if not cls._running(pname): break
                time.sleep(0.5)
            if cls._running(pname):
                return False, f"{b} did not close in time. Close it manually (check the tray) and retry."
        say(f"Reopening {b} with cookie access (local CDP port {port})...")
        try:
            subprocess.Popen([exe, f"--remote-debugging-port={port}", "--restore-last-session"], close_fds=True)
        except Exception as e:
            return False, f"Could not relaunch {b}: {e}"
        if not CdpCookieExtractor.wait_endpoint(port, 40):
            return False, f"{b} reopened but its cookie (CDP) endpoint did not start. Try 'Extract Now' after closing it."
        say("Harvesting decrypted cookies from the open browser (like a cookie extension)...")
        ok, msg = CdpCookieExtractor.harvest(port, dest)
        if ok:
            CdpCookieExtractor._last_port = port  # browser stays open on this port -> auto-refresh can re-harvest
            msg += f"\n{b} stays open with your previous session restored."
        LoggerSetup.log(f"CDP auto-fix result: ok={ok} msg={msg}", "debug")
        return ok, msg


class DownloadStatus(Enum):
    QUEUED = "Queued"; STARTING = "Starting..."; DOWNLOADING = "Downloading"; PROCESSING = "Processing"
    PAUSED = "Paused"; COMPLETED = "Completed"; ERROR = "System Error"; CANCELLED = "Cancelled"
    INVALID = "Failed"; VERIFYING = "Verifying Hash"; SKIPPED = "Skipped"


class ErrorCategory(Enum):
    NONE = ""; NEEDS_COOKIES = "Needs Cookies / Auth"; COOKIE_DB_LOCKED = "Browser Cookie DB Locked"
    NETWORK_PROXY = "Network / Proxy"; RATE_LIMITED = "Rate Limited (429)"; FFMPEG = "FFmpeg / Post-Processing"
    FORMAT_UNAVAILABLE = "Format Unavailable"; OUTPUT_MISSING = "Output File Missing"; RESUME_MISMATCH = "Resume Mismatch (416)"
    GEO_BLOCKED = "Geo-Blocked"; DRM_PROTECTED = "DRM Protected"; DISK_FULL = "Disk Full / Permissions"
    UNAVAILABLE = "Media Unavailable"; CANCELLED = "Cancelled"; UNKNOWN = "Unknown Error"


class ErrorClassifier:
    @staticmethod
    def classify(message: Any) -> ErrorCategory:
        t = clean_ansi_codes(message or "").lower()
        if not t: return ErrorCategory.UNKNOWN
        if any(k in t for k in ("aborted by user", "cancelled", "canceled")): return ErrorCategory.CANCELLED
        if "requested range not satisfiable" in t or "http error 416" in t: return ErrorCategory.RESUME_MISMATCH
        if any(k in t for k in ("could not copy chrome cookie", "dpapi", "failed to decrypt cookie", "cookie database")): return ErrorCategory.COOKIE_DB_LOCKED
        if "drm" in t or "widevine" in t: return ErrorCategory.DRM_PROTECTED
        if any(k in t for k in ("no space left on device", "disk full", "not enough space", "permission denied")): return ErrorCategory.DISK_FULL
        if any(k in t for k in ("429", "too many requests", "rate limit")): return ErrorCategory.RATE_LIMITED
        if any(k in t for k in ("available in your country", "geo-restricted", "geo restricted")): return ErrorCategory.GEO_BLOCKED
        if any(k in t for k in ("sign in to confirm", "not a bot", "cookies", "cookie", "age restricted", "confirm your age", "private video", "members-only", "login required")): return ErrorCategory.NEEDS_COOKIES
        if any(k in t for k in ("video unavailable", "has been removed", "terminated", "copyright claim", "does not exist", "404")): return ErrorCategory.UNAVAILABLE
        if any(k in t for k in ("ssl:", "remote end closed", "connection reset", "timed out", "timeout", "proxy", "403", "forbidden", "getaddrinfo failed", "failed to resolve", "unable to download webpage")): return ErrorCategory.NETWORK_PROXY
        if any(k in t for k in ("ffmpeg", "ffprobe", "postprocessing", "merging formats", "unable to merge")): return ErrorCategory.FFMPEG
        if any(k in t for k in ("requested format is not available", "format is not available", "no video formats found", "no compatible formats", "only images are available")): return ErrorCategory.FORMAT_UNAVAILABLE
        if "no output media file" in t or "output file" in t: return ErrorCategory.OUTPUT_MISSING
        return ErrorCategory.UNKNOWN

    @staticmethod
    def remediation(cat: ErrorCategory) -> str:
        return {
            ErrorCategory.NEEDS_COOKIES: "Open Settings > Cookie Helper: extract from browser, Auto-Fix, or import cookies.txt.",
            ErrorCategory.COOKIE_DB_LOCKED: "Browser is open and locks its cookies. Use Settings > Cookie Helper > Auto-Fix (closes & reopens browser), or close the browser and retry.",
            ErrorCategory.NETWORK_PROXY: "Try Direct mode ('none'), DoH, or Force IPv4 in Settings.",
            ErrorCategory.RATE_LIMITED: "Increase Request Sleep Min/Max in Settings.",
            ErrorCategory.FFMPEG: "FFmpeg missing/outdated. Settings > Network & Engines > 'Download / Update FFmpeg' (one click).",
            ErrorCategory.FORMAT_UNAVAILABLE: "Install Deno JS runtime, enable Remote EJS, or try Best Quality.",
            ErrorCategory.OUTPUT_MISSING: "Output file not found. Try a simpler filename pattern.",
            ErrorCategory.RESUME_MISMATCH: "Partial file cleared after 416 mismatch; retry starts cleanly.",
            ErrorCategory.GEO_BLOCKED: "Region-locked content; use a VPN/proxy.",
            ErrorCategory.DRM_PROTECTED: "DRM-encrypted stream cannot be downloaded.",
            ErrorCategory.DISK_FULL: "Low disk space or folder write permission denied.",
            ErrorCategory.UNAVAILABLE: "Video removed, private, or URL invalid.",
            ErrorCategory.CANCELLED: "Cancelled by user.",
        }.get(cat, "Open Task Inspector or System Logs for details.")

    @staticmethod
    def recommended_action(cat: ErrorCategory) -> Optional[Tuple[str, str]]:
        return {
            ErrorCategory.NEEDS_COOKIES: ("browser_cookies", "Retry w/ Browser Cookies"),
            ErrorCategory.COOKIE_DB_LOCKED: ("file_cookies", "Retry w/ Cookie File"),
            ErrorCategory.NETWORK_PROXY: ("direct_no_proxy", "Retry Direct (No Proxy)"),
            ErrorCategory.RESUME_MISMATCH: ("clean_resume", "Clean Partial & Retry"),
            ErrorCategory.FORMAT_UNAVAILABLE: ("best_fallback", "Retry Best Quality"),
        }.get(cat)


class ServiceType(Enum):
    YOUTUBE = "youtube"; INSTAGRAM = "instagram"; GENERIC = "generic"


@dataclass
class DownloadTask:
    task_id: str; url: str; ydl_opts: Dict[str, Any]; download_type: str
    service_type: ServiceType = ServiceType.GENERIC
    title: str = "Fetching Title..."; is_placeholder_title: bool = False
    uploader: str = ""; duration_sec: Optional[float] = None; original_url: Optional[str] = None
    info_dict: Dict[str, Any] = field(default_factory=dict)
    status: DownloadStatus = DownloadStatus.QUEUED; stage_label: str = ""
    progress_str: str = "0%"; progress_float: float = 0.0
    downloaded_bytes: int = 0; total_bytes: int = 0
    speed_str: str = "N/A"; speed_float: float = 0.0; peak_speed: float = 0.0
    eta_str: str = "N/A"; total_bytes_str: str = "N/A"
    filepath: Optional[str] = None; error_message: Optional[str] = None
    error_category: str = ""; error_remediation: str = ""
    is_terminating: bool = False; quality_profile: str = "Custom"; thumbnail_url: Optional[str] = None
    speed_history: List[float] = field(default_factory=list); retry_count: int = 0
    file_hash: str = ""; hash_algo: str = "md5"; category: str = "Uncategorized"
    is_playlist_item: bool = False; playlist_title: str = ""
    created_at: float = field(default_factory=time.time); completed_at: Optional[float] = None
    last_activity_time: float = field(default_factory=time.time)

    @staticmethod
    def compact_info_dict(info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not isinstance(info, dict): return {}
        out: Dict[str, Any] = {}
        for k in ("id", "title", "uploader", "channel", "duration", "webpage_url", "thumbnail", "ext", "view_count", "upload_date", "playlist_title"):
            if info.get(k) is not None:
                try: json.dumps({k: info[k]}); out[k] = info[k]
                except Exception: pass
        return out

    def to_dict(self) -> Dict[str, Any]:
        oc = copy.deepcopy(self.ydl_opts) if isinstance(self.ydl_opts, dict) else {}
        for k in ("logger", "progress_hooks", "postprocessor_hooks", "cookiesfrombrowser", "download_ranges", "remote_components"):
            oc.pop(k, None)
        return {
            "task_id": self.task_id, "url": self.url, "original_url": self.original_url or self.url, "ydl_opts": oc,
            "download_type": self.download_type, "title": self.title or "Untitled Media", "is_placeholder_title": self.is_placeholder_title,
            "uploader": self.uploader, "duration_sec": self.duration_sec, "info_dict": self.compact_info_dict(self.info_dict),
            "status": self.status.value, "stage_label": self.stage_label, "service_type": self.service_type.value,
            "quality_profile": self.quality_profile, "thumbnail_url": self.thumbnail_url, "filepath": self.filepath,
            "category": self.category, "is_playlist_item": self.is_playlist_item, "playlist_title": self.playlist_title,
            "error_message": self.error_message, "error_category": self.error_category, "error_remediation": self.error_remediation,
            "progress_float": self.progress_float, "progress_str": self.progress_str, "downloaded_bytes": self.downloaded_bytes,
            "total_bytes": self.total_bytes, "total_bytes_str": self.total_bytes_str, "file_hash": self.file_hash,
            "hash_algo": self.hash_algo, "created_at": self.created_at, "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DownloadTask":
        if not isinstance(data, dict) or not data.get("url"): raise ValueError("Invalid queue entry.")
        try: st = ServiceType(data.get("service_type", "generic"))
        except Exception: st = detect_service_type(str(data["url"]))
        opts = copy.deepcopy(data.get("ydl_opts")) if isinstance(data.get("ydl_opts"), dict) else {}
        for k in ("logger", "progress_hooks", "postprocessor_hooks", "cookiesfrombrowser", "download_ranges", "remote_components"):
            opts.pop(k, None)
        inf = data.get("info_dict") if isinstance(data.get("info_dict"), dict) else {}
        t = cls(
            task_id=str(data.get("task_id") or f"task_{time.time_ns()}"), url=str(data["url"]), ydl_opts=opts,
            download_type=str(data.get("download_type") or "Video"), title=str(data.get("title") or inf.get("title") or "Restored Download"),
            is_placeholder_title=bool(data.get("is_placeholder_title", False)), uploader=str(data.get("uploader") or inf.get("uploader") or ""),
            duration_sec=data.get("duration_sec") or inf.get("duration"), original_url=data.get("original_url"), info_dict=inf,
            service_type=st, quality_profile=str(data.get("quality_profile") or "Custom"), thumbnail_url=data.get("thumbnail_url"),
            filepath=data.get("filepath"), category=str(data.get("category") or "Uncategorized"),
            is_playlist_item=bool(data.get("is_playlist_item") or data.get("category") == "Playlist"), playlist_title=str(data.get("playlist_title") or ""),
        )
        t.stage_label = str(data.get("stage_label") or ""); t.error_message = data.get("error_message")
        t.error_category = str(data.get("error_category") or ""); t.error_remediation = str(data.get("error_remediation") or "")
        t.progress_float = max(0.0, min(1.0, safe_float(data.get("progress_float"), 0.0))); t.progress_str = str(data.get("progress_str") or "0%")
        t.downloaded_bytes = safe_int(data.get("downloaded_bytes"), 0, 0); t.total_bytes = safe_int(data.get("total_bytes"), 0, 0)
        t.total_bytes_str = str(data.get("total_bytes_str") or "N/A"); t.file_hash = str(data.get("file_hash") or "")
        t.hash_algo = str(data.get("hash_algo") or "md5"); t.created_at = safe_float(data.get("created_at"), time.time()); t.completed_at = data.get("completed_at")
        smap = {x.value: x for x in (DownloadStatus.PAUSED, DownloadStatus.COMPLETED, DownloadStatus.SKIPPED, DownloadStatus.ERROR, DownloadStatus.CANCELLED, DownloadStatus.INVALID)}
        t.status = smap.get(data.get("status"), DownloadStatus.QUEUED)
        if t.status == DownloadStatus.COMPLETED: t.progress_float, t.progress_str = 1.0, "100%"
        elif t.status == DownloadStatus.SKIPPED: t.progress_float, t.progress_str = 1.0, "Skipped"
        elif t.status == DownloadStatus.QUEUED: t.progress_float, t.progress_str = 0.0, "0%"
        return t


class SettingsManager:
    DEFAULT_SETTINGS: Dict[str, Any] = {
        "download_path": str(Path.home() / "Downloads" / "SinaFusion"), "theme": "Dark", "max_concurrent_downloads": 2,
        "max_retries": 5, "retry_delay": 10, "default_download_type": "Video", "font_family": "Arial",
        "concurrent_fragments": 8, "audio_format": "mp3", "debug_mode": True, "ffmpeg_path": detect_bundled_ffmpeg() or "ffmpeg",
        "close_to_tray": False, "default_subtitle_langs": "en,fa", "embed_subtitles": True, "burn_subtitles": False,
        "embed_thumbnail": True, "embed_metadata": True, "sponsorblock_categories": [],
        "proxy_mode": "system", "proxy_type": "http", "proxy_address": "", "proxy_port": "", "force_ipv4": False,
        "doh_enabled": False, "doh_url": DOH_PROVIDERS["Cloudflare"], "auto_cookie_gen": True, "cookie_source": "auto",
        "cookies_file_path": str(Path.home() / ".sina_fusion" / "cookies.txt"), "cookie_browser": "auto",
        "youtube_client_profile": "auto", "ytdlp_remote_ejs": True, "request_sleep_min": 0.75, "request_sleep_max": 2.25,
        "po_token_mode": "off", "po_token": "", "instagram_user": "", "instagram_pass": "",
        "clipboard_monitor": False, "playlist_sync": True, "playlist_subfolder": True, "auto_cleanup": True,
        "watchdog_enabled": True, "auto_categorize": True, "filename_pattern": "%(title)s [%(id)s]",
        "verify_hash": False, "hash_algo": "md5", "use_aria2": False, "aria2_path": "aria2c",
        "global_speed_limit_kbps": 0, "search_results_count": 15, "on_queue_complete": "notify",
    }

    def __init__(self, settings_file: str):
        self.settings_file, self.security, self._lock = settings_file, SecurityManager(), threading.RLock()
        self.settings, changed = self._load()
        self._ensure_paths(); self.apply_runtime_globals()
        if changed: self.save()

    def _ensure_paths(self):
        try:
            Path(self.get("download_path")).mkdir(parents=True, exist_ok=True)
            cp = self.get("cookies_file_path")
            if cp: Path(cp).parent.mkdir(parents=True, exist_ok=True)
        except Exception as e: LoggerSetup.log(f"Path creation error: {e}", "error")

    def apply_runtime_globals(self):
        LoggerSetup.set_debug_enabled(bool(self.get("debug_mode")))
        DoHResolver.configure(bool(self.get("doh_enabled")), str(self.get("doh_url") or DOH_PROVIDERS["Cloudflare"]))

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock: val = self.settings.get(key, self.DEFAULT_SETTINGS.get(key, default))
        return self.security.decrypt(str(val)) if (key == "instagram_pass" and val) else val

    def set(self, key: str, value: Any):
        with self._lock:
            self.settings[key] = (self.security.encrypt(str(value or "")) if value else "") if key == "instagram_pass" else value

    def _normalize(self, s: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        changed = False
        for k, v in self.DEFAULT_SETTINGS.items():
            if k not in s: s[k], changed = copy.deepcopy(v), True
        bff = detect_bundled_ffmpeg()
        if bff and str(s.get("ffmpeg_path") or "").strip().lower() in {"", "ffmpeg", "ffmpeg.exe"}:
            s["ffmpeg_path"], changed = bff, True
        for k, (d, lo, hi) in {"max_concurrent_downloads": (2, 1, 8), "max_retries": (5, 0, 20), "retry_delay": (10, 1, 600), "concurrent_fragments": (8, 1, 32), "global_speed_limit_kbps": (0, 0, 1048576), "search_results_count": (15, 5, 30)}.items():
            nv = safe_int(s.get(k), d, lo, hi)
            if s.get(k) != nv: s[k], changed = nv, True
        for k, (d, lo, hi) in {"request_sleep_min": (0.75, 0.0, 30.0), "request_sleep_max": (2.25, 0.0, 60.0)}.items():
            nv = safe_float(s.get(k), d, lo, hi)
            if s.get(k) != nv: s[k], changed = nv, True
        if s["request_sleep_max"] < s["request_sleep_min"]: s["request_sleep_max"], changed = s["request_sleep_min"], True
        for k, (al, fb) in {
            "youtube_client_profile": ({"auto", "default_no_ios", "tv_embedded_combo", "web_safari", "web", "android", "ios", "mweb", "tv"}, "auto"),
            "po_token_mode": ({"off", "manual"}, "off"), "cookie_source": ({"auto", "file", "browser", "none"}, "auto"),
            "cookie_browser": ({"auto", "chrome", "edge", "brave", "vivaldi", "chromium", "opera", "firefox"}, "auto"),
            "proxy_mode": ({"system", "custom", "none"}, "system"), "hash_algo": ({"md5", "sha256"}, "md5"),
            "on_queue_complete": ({"none", "notify", "open_folder", "sleep", "shutdown"}, "notify"),
        }.items():
            if str(s.get(k) or "").lower() not in al: s[k], changed = fb, True
        # --- One-time migrations (v18.1) ---
        if not s.get("_migrated_v18_1"):
            s["_migrated_v18_1"], changed = True, True
            # Post-download hash verification is opt-in now; disable it once for
            # existing installs. Afterwards the user's own choice is preserved.
            if s.get("verify_hash"):
                s["verify_hash"] = False
                LoggerSetup.log("Migration: post-download hash verification disabled (now opt-in).", "info")
            # A configured browser that is not installed (e.g. 'chromium') silently
            # yielded zero cookies. Fall back to auto-detection of an installed one.
            cb = str(s.get("cookie_browser") or "auto").lower()
            if cb not in ("auto", "firefox") and not BrowserCookieExtractor.browser_installed(cb):
                s["cookie_browser"] = "auto"
                LoggerSetup.log(f"Migration: cookie browser '{cb}' is not installed -> 'auto'.", "info")
        if not isinstance(s.get("sponsorblock_categories"), list): s["sponsorblock_categories"], changed = [], True
        for k in ("download_path", "filename_pattern"):
            if not str(s.get(k) or "").strip(): s[k], changed = self.DEFAULT_SETTINGS[k], True
        return s, changed

    def _load(self) -> Tuple[Dict[str, Any], bool]:
        try:
            if os.path.exists(self.settings_file):
                loaded = json.loads(Path(self.settings_file).read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    return self._normalize(loaded)
        except Exception as e: LoggerSetup.log(f"Error loading settings: {e}", "error")
        return self._normalize(copy.deepcopy(self.DEFAULT_SETTINGS))

    def normalize_and_save(self):
        """Thread-safe normalize + persist + runtime re-apply (used by Settings UI)."""
        with self._lock:
            self.settings, _ = self._normalize(self.settings)
        self.save(); self._ensure_paths(); self.apply_runtime_globals()

    def save(self):
        try:
            with self._lock: payload = copy.deepcopy(self.settings)
            p = Path(self.settings_file); p.parent.mkdir(parents=True, exist_ok=True)
            # Unique tmp name: concurrent save() calls must not race on one .tmp path.
            tmp = p.with_suffix(p.suffix + f".{threading.get_ident()}.tmp")
            tmp.write_text(json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, p)
        except Exception as e: LoggerSetup.log(f"Error saving settings: {e}", "error")


class AntiBotManager:
    CLIENT_PROFILES: Dict[str, Optional[List[str]]] = {
        "auto": None, "default_no_ios": ["default", "-ios_downgraded"], "tv_embedded_combo": ["tv", "web_embedded"],
        "web_safari": ["web_safari"], "web": ["web"], "android": ["android"], "ios": ["ios"], "mweb": ["mweb", "web"], "tv": ["tv"],
    }

    def __init__(self, settings: SettingsManager):
        self.settings = settings

    def get_proxy_url(self, override_mode: Optional[str] = None) -> Optional[str]:
        mode = (override_mode or self.settings.get("proxy_mode") or "system").lower()
        if mode == "none": return ""
        if mode == "custom":
            addr = str(self.settings.get("proxy_address") or "").strip()
            if addr:
                pt, port = str(self.settings.get("proxy_type") or "http").strip(), str(self.settings.get("proxy_port") or "").strip()
                return f"{pt}://{addr}:{port}" if port else f"{pt}://{addr}"
        return None

    def apply_common_options(self, opts: Dict[str, Any], url: str = "", active_count: int = 1):
        r = safe_int(self.settings.get("max_retries"), 5, 0, 20)
        opts.update({
            "logger": YtdlLoggerAdapter(), "color": "no_color", "continuedl": True, "overwrites": False,
            "ignoreerrors": False, "windowsfilenames": sys.platform == "win32", "trim_file_name": 180,
            "retries": r, "fragment_retries": r, "extractor_retries": max(3, r),
            "concurrent_fragment_downloads": safe_int(self.settings.get("concurrent_fragments"), 8, 1, 32), "socket_timeout": 30,
        })
        l_kbps = safe_int(self.settings.get("global_speed_limit_kbps"), 0, 0, 1048576)
        if l_kbps > 0: opts["ratelimit"] = max(10240, int((l_kbps * 1024) / max(1, active_count)))
        ff = resolve_ffmpeg_location(self.settings.get("ffmpeg_path"))
        if ff: opts["ffmpeg_location"] = ff
        js = detect_js_runtimes()
        if js:
            opts["js_runtimes"] = js
            if self.settings.get("ytdlp_remote_ejs"): opts["remote_components"] = {"ejs:github"}
        pv = self.get_proxy_url(opts.pop("_override_proxy_mode", None))
        if pv is not None: opts["proxy"] = pv
        if self.settings.get("force_ipv4"): opts["source_address"] = "0.0.0.0"
        if str(self.settings.get("allow_insecure_tls") or "").lower() in ("true", "1", "yes"):
            opts["nocheckcertificate"] = True
            LoggerSetup.log("TLS certificate verification DISABLED (explicit user setting 'allow_insecure_tls'). Only use behind a trusted MITM proxy.", "warning")

        c_src = str(opts.pop("_override_cookie_source", None) or self.settings.get("cookie_source", "auto") or "auto").lower()
        browser_name = BrowserCookieExtractor.resolve_browser(str(self.settings.get("cookie_browser", "auto") or "auto"))
        explicit_cf = opts.get("cookiefile")
        LoggerSetup.log(f"Cookie mode for this request: source='{c_src}', browser='{browser_name}', explicit_file={explicit_cf}", "debug")
        if c_src == "none":
            opts.pop("cookiefile", None); opts.pop("cookiesfrombrowser", None)
        elif c_src == "browser":
            # Prefer live bridge cookies: the browser DB is exclusively locked while
            # it runs, so yt-dlp's cookiesfrombrowser would fail on the first attempt
            # and waste a retry. The bridge IS real browser cookies, already decrypted.
            snap = self._bridge_snapshot()
            if snap:
                opts["cookiefile"] = snap; opts.pop("cookiesfrombrowser", None)
                LoggerSetup.log("Browser source: using live bridge cookies (avoids locked-DB first-attempt failure).", "debug")
            else:
                opts["cookiesfrombrowser"] = (browser_name, None, None, None)
                opts.pop("cookiefile", None)
        elif explicit_cf and os.path.exists(str(explicit_cf)) and looks_like_netscape_cookie_file(explicit_cf):
            opts.pop("cookiesfrombrowser", None)  # honor per-task cookie file (e.g. auto-retry refresh)
        elif c_src == "file":
            cf = self.settings.get("cookies_file_path")
            if cf and os.path.exists(cf) and looks_like_netscape_cookie_file(cf):
                opts["cookiefile"] = cf; opts.pop("cookiesfrombrowser", None)
            else:
                if cf and os.path.exists(cf):
                    LoggerSetup.log(f"Configured cookie file is NOT a valid Netscape cookies.txt: {cf}. Falling back to auto browser extraction. Re-export it via Cookie Helper.", "warning")
                auto_cf = self.ensure_auto_cookies()
                if auto_cf:
                    opts["cookiefile"] = auto_cf; opts.pop("cookiesfrombrowser", None)
                else:
                    opts["cookiesfrombrowser"] = (browser_name, None, None, None); opts.pop("cookiefile", None)
        else:  # auto: user file -> live browser extraction -> yt-dlp browser engine
            cf = self.settings.get("cookies_file_path")
            if cf and os.path.exists(cf) and looks_like_netscape_cookie_file(cf):
                opts["cookiefile"] = cf; opts.pop("cookiesfrombrowser", None)
            else:
                if cf and os.path.exists(cf) and os.path.getsize(cf) > 0:
                    LoggerSetup.log(f"Ignoring invalid Netscape cookie file: {cf} (using auto extraction).", "warning")
                auto_cf = self.ensure_auto_cookies()
                if auto_cf:
                    opts["cookiefile"] = auto_cf; opts.pop("cookiesfrombrowser", None)
                else:
                    opts["cookiesfrombrowser"] = (browser_name, None, None, None); opts.pop("cookiefile", None)

        low = (url or "").lower()
        _h = _url_host(url)
        if not low or _host_is(_h, "youtube.com") or _host_is(_h, "youtu.be"):
            smin = safe_float(self.settings.get("request_sleep_min"), 0.75, 0.0, 30.0)
            smax = safe_float(self.settings.get("request_sleep_max"), 2.25, smin, 60.0)
            if smax > 0: opts["sleep_interval_requests"], opts["sleep_interval"], opts["max_sleep_interval"] = smin, smin, smax
            clients = self.CLIENT_PROFILES.get(str(self.settings.get("youtube_client_profile", "auto") or "auto").lower())
            tok = str(self.settings.get("po_token") or "").strip() if str(self.settings.get("po_token_mode", "off")).lower() == "manual" else ""
            if clients or tok:
                yt_a = opts.setdefault("extractor_args", {}).setdefault("youtube", {})
                if clients: yt_a.setdefault("player_client", list(clients))
                if tok: yt_a["po_token"] = [tok]

    _cookie_extract_lock = threading.Lock()

    def _bridge_snapshot(self) -> Optional[str]:
        """Return a snapshot COPY of fresh live bridge cookies, or None. yt-dlp
        gets a copy so its jar write-back on close can't clobber the bridge file
        that the extension keeps refreshing."""
        try:
            if os.path.exists(BRIDGE_COOKIE_FILE) and os.path.getsize(BRIDGE_COOKIE_FILE) > 100 \
                    and (time.time() - os.path.getmtime(BRIDGE_COOKIE_FILE)) < 1800 \
                    and looks_like_netscape_cookie_file(BRIDGE_COOKIE_FILE):
                dest = AUTO_COOKIE_FILE
                tmp = Path(dest).with_suffix(f".{threading.get_ident()}.tmp")
                shutil.copyfile(BRIDGE_COOKIE_FILE, tmp)
                os.replace(tmp, dest)
                return dest
        except OSError:
            pass
        return None

    def ensure_auto_cookies(self, force: bool = False) -> Optional[str]:
        """Extract fresh cookies from the configured browser (cached for 30 min).

        Serialized: concurrent workers hitting auth errors must not interleave
        writes to the same cookies.txt / SQLite temp copy (corrupt-file race).
        """
        dest = AUTO_COOKIE_FILE
        with self._cookie_extract_lock:
            # 0) Live bridge cookies are the best source: real, decrypted, refreshed
            # continuously while the browser is open - no DB lock, no CDP, no restart.
            snap = self._bridge_snapshot()
            if snap:
                LoggerSetup.log("Using live cookies from the SINA Cookie Bridge extension (snapshot).", "debug")
                return snap
            try:
                if not force and os.path.exists(dest) and os.path.getsize(dest) > 100 and (time.time() - os.path.getmtime(dest)) < 1800:
                    LoggerSetup.log(f"Using cached auto-extracted cookies ({dest}).", "debug")
                    return dest
            except OSError:
                pass
            LoggerSetup.log(f"Auto cookie extraction starting (force={force})...", "debug")
            browser = str(self.settings.get("cookie_browser") or "auto")
            ok, msg = BrowserCookieExtractor.extract(browser, dest)
            if ok:
                LoggerSetup.log(msg, "info")
                return dest
            LoggerSetup.log(msg, "warning")
            # Direct DB copy fails while the browser is RUNNING (exclusive lock).
            # If a CDP endpoint is already open (after Cookie Helper > "Extract from
            # OPEN browser (CDP)"), harvest REAL decrypted cookies from it - this is
            # non-disruptive (the browser stays open) and yields logged-in cookies
            # that actually bypass YouTube bot detection, unlike anonymous warm-up.
            port = CdpCookieExtractor.find_debug_port()
            if port:
                LoggerSetup.log(f"Direct extraction failed; harvesting real cookies via open CDP port {port}...", "debug")
                ok2, msg2 = CdpCookieExtractor.harvest(port, dest)
                LoggerSetup.log(msg2, "info" if ok2 else "warning")
                if ok2:
                    return dest
            return None

    def refresh_cookies(self) -> Optional[str]:
        """Best-effort cookie refresh used by the auto-retry engine on auth errors.

        Returns REAL browser cookies (AUTO_COOKIE_FILE) when possible; only falls
        back to anonymous warm-up cookies (ANON_COOKIE_FILE) as a last resort.
        Anonymous cookies cannot bypass 'sign in to confirm you're not a bot'.
        """
        p = self.ensure_auto_cookies(force=True)
        if p: return p
        if sync_playwright or reload_playwright():
            try:
                ok, _ = CookieGenerator(ANON_COOKIE_FILE).generate()
                if ok: return ANON_COOKIE_FILE
            except Exception as e:
                LoggerSetup.log(f"Playwright cookie warm-up failed: {e}", "warning")
        return None


class DownloadManager:
    def __init__(self, app_callback: "SinaEnterpriseApp"):
        self.app, self.settings = app_callback, app_callback.settings_manager
        self.tasks: Dict[str, DownloadTask] = {}; self.download_queue: List[str] = []
        self.active_threads: Dict[str, threading.Thread] = {}; self._active_runs: Dict[str, Tuple[int, threading.Event]] = {}
        self._run_counter, self.state_lock = 0, threading.RLock()
        self._watchdog_restarts: Dict[str, int] = {}
        self.is_shutting_down = self.queue_paused_globally = self._completion_notified = False
        self.scheduled_start_ts: Optional[float] = None; self.session_bytes_downloaded = 0
        self.fingerprint, self.antibot = DigitalFingerprint(), AntiBotManager(self.settings)
        self.taskbar = TaskbarManager() if HAS_TASKBAR else None
        if self.settings.get("auto_cleanup"): threading.Thread(target=self._cleanup_temp_files, name="Cleanup", daemon=True).start()

    def start_processing(self):
        threading.Thread(target=self._process_queue_loop, name="QueueDispatch", daemon=True).start()
        threading.Thread(target=self._watchdog_loop, name="Watchdog", daemon=True).start()

    def get_task(self, tid: str) -> Optional[DownloadTask]:
        with self.state_lock: return self.tasks.get(tid)

    def _is_current_run(self, tid: str, rid: int) -> bool:
        with self.state_lock: p = self._active_runs.get(tid); return bool(p and p[0] == rid)

    def _signal_cancel(self, tid: str):
        with self.state_lock:
            p = self._active_runs.get(tid)
            if p: p[1].set()

    def add_task(self, task: DownloadTask, from_restore: bool = False):
        if not from_restore:
            ok, msg = DiskAnalyzer.check_space(self.settings.get("download_path"), 500)
            if not ok and threading.current_thread() is threading.main_thread(): messagebox.showwarning("Disk Space Warning", msg, parent=self.app)
            with self.state_lock:
                dup = any(t.status == DownloadStatus.COMPLETED and t.url == task.url for t in self.tasks.values())
                live_dup = any(t.url == task.url and t.status in {DownloadStatus.QUEUED, DownloadStatus.STARTING, DownloadStatus.DOWNLOADING, DownloadStatus.PROCESSING, DownloadStatus.PAUSED} for t in self.tasks.values())
            if live_dup and not (task.is_playlist_item or task.category == "Playlist"):
                LoggerSetup.log(f"Skipped duplicate URL (already queued/active): {task.url}", "info"); return
            if dup:
                if task.is_playlist_item or task.category == "Playlist": return
                if threading.current_thread() is threading.main_thread() and not messagebox.askyesno("Duplicate", f"'{task.title}' already downloaded.\nDownload again?", parent=self.app): return
        with self.state_lock:
            self.tasks[task.task_id] = task
            if task.status == DownloadStatus.QUEUED and task.task_id not in self.download_queue:
                self.download_queue.append(task.task_id); self._completion_notified = False
        self.app.run_on_gui_thread(self.app.add_task_to_ui, task)
        self.app.run_on_gui_thread(self.app._update_global_progress)

    def promote_task(self, tid: str):
        with self.state_lock:
            if tid in self.download_queue:
                self.download_queue.remove(tid); self.download_queue.insert(0, tid)
                if tid in self.tasks: self.tasks[tid].stage_label = "Priority (Next)"
        self.app.run_on_gui_thread(self.app.update_task_ui, tid)

    def pause_task(self, tid: str):
        with self.state_lock:
            t = self.tasks.get(tid)
            if not t or t.status not in {DownloadStatus.DOWNLOADING, DownloadStatus.STARTING, DownloadStatus.QUEUED}: return
            t.is_terminating, t.status, t.stage_label, t.speed_float = True, DownloadStatus.PAUSED, "Paused", 0.0
            if tid in self.download_queue: self.download_queue.remove(tid)
            self._signal_cancel(tid)
        self.app.run_on_gui_thread(self.app.update_task_ui, tid)

    def resume_task(self, tid: str):
        with self.state_lock:
            t = self.tasks.get(tid)
            if not t or t.status != DownloadStatus.PAUSED: return
            t.status, t.stage_label, t.is_terminating, t.last_activity_time = DownloadStatus.QUEUED, "Queued", False, time.time()
            if tid not in self.download_queue: self.download_queue.insert(0, tid)
            self._completion_notified = False
        self.app.run_on_gui_thread(self.app.update_task_ui, tid)

    def retry_task(self, tid: str, override_opts: Optional[Dict[str, Any]] = None, _watchdog: bool = False):
        do_clean = False
        with self.state_lock:
            t = self.tasks.get(tid)
            if not t: return
            if _watchdog:
                # Never resurrect a task the user cancelled/paused or that already
                # completed in the race window between watchdog scan and retry.
                if t.status not in {DownloadStatus.STARTING, DownloadStatus.DOWNLOADING, DownloadStatus.ERROR}: return
                n = self._watchdog_restarts.get(tid, 0) + 1
                self._watchdog_restarts[tid] = n
                if n > 3:
                    t.status, t.stage_label, t.speed_float = DownloadStatus.ERROR, "Failed (repeatedly stalled)", 0.0
                    t.error_message = "Task stalled repeatedly; watchdog stopped after 3 automatic restarts. Retry manually or check the URL/network."
                    t.error_category = ErrorCategory.NETWORK_PROXY.value
                    t.error_remediation = ErrorClassifier.remediation(ErrorCategory.NETWORK_PROXY)
                    self.app.run_on_gui_thread(self.app.update_task_ui, tid)
                    return
            if override_opts:
                ov = dict(override_opts)
                do_clean = ov.pop("_clean_resume", False)
                if do_clean: t.progress_float, t.progress_str = 0.0, "0%"
                t.ydl_opts.update(ov)
            # Invalidate any still-active run so the old worker aborts and cannot
            # overwrite the re-queued state (retry-vs-active-worker race).
            if tid in self._active_runs:
                self._signal_cancel(tid)
                self._run_counter += 1
                self._active_runs[tid] = (self._run_counter, threading.Event())
            t.status, t.stage_label, t.is_terminating = DownloadStatus.QUEUED, "Queued", False
            t.error_message = None; t.error_category = t.error_remediation = ""
            t.last_activity_time = time.time()
            if not _watchdog:
                t.retry_count = 0; self._watchdog_restarts.pop(tid, None)
            if tid not in self.download_queue: self.download_queue.insert(0, tid)
            self._completion_notified = False
        # Run the (recursive) partial-file cleanup OUTSIDE state_lock so a large
        # download-tree scan never freezes the dispatcher/watchdog/progress hooks.
        if do_clean: self._cleanup_resume_files(t)
        self.app.run_on_gui_thread(self.app.update_task_ui, tid)

    def cancel_task(self, tid: str):
        with self.state_lock:
            t = self.tasks.get(tid)
            if not t: return
            t.is_terminating, t.status, t.stage_label, t.speed_float = True, DownloadStatus.CANCELLED, "Cancelled", 0.0
            if tid in self.download_queue: self.download_queue.remove(tid)
            self._signal_cancel(tid)
        self.app.run_on_gui_thread(self.app.update_task_ui, tid)

    def remove_task_from_ui(self, tid: str):
        with self.state_lock:
            if tid in self.tasks: self.tasks[tid].is_terminating = True
            self._signal_cancel(tid); self.tasks.pop(tid, None)
            if tid in self.download_queue: self.download_queue.remove(tid)
        self.app.run_on_gui_thread(self.app.remove_task_widget, tid)

    def set_schedule_delay(self, minutes: float):
        with self.state_lock:
            if minutes <= 0:
                self.scheduled_start_ts, self.queue_paused_globally = None, False; LoggerSetup.log("Queue schedule cleared.", "info")
            else:
                self.scheduled_start_ts, self.queue_paused_globally = time.time() + minutes * 60.0, True
                LoggerSetup.log(f"Queue scheduled for {datetime.fromtimestamp(self.scheduled_start_ts).strftime('%H:%M:%S')}.", "info")

    def _cleanup_temp_files(self):
        try:
            root = Path(self.settings.get("download_path"))
            if not root.exists(): return
            now, cnt = time.time(), 0
            for f in root.rglob("*"):
                if f.is_file() and (f.suffix in {".part", ".temp", ".ytdl"} or ".part-Frag" in f.name) and now - f.stat().st_mtime > 86400:
                    try: f.unlink(); cnt += 1
                    except OSError: pass
            if cnt: LoggerSetup.log(f"Cleaned {cnt} old temp file(s).", "info")
        except Exception: pass

    def _cleanup_resume_files(self, task: DownloadTask) -> int:
        roots = {Path(os.path.abspath(self.settings.get("download_path")))}
        stems: Set[str] = set()
        if task.filepath: p = Path(task.filepath); roots.add(Path(os.path.abspath(p.parent))); stems.update({p.name, p.stem})
        if task.info_dict:
            stems.add(sanitize_filename_part(task.info_dict.get("title"), limit=80))
            if task.info_dict.get("id"): stems.add(str(task.info_dict["id"]))
        if task.title and not task.is_placeholder_title: stems.add(sanitize_filename_part(task.title, limit=80))
        stems = {s for s in stems if s and len(s) >= 3}
        # SAFETY: with no known stems we cannot attribute partial files to this
        # task - NEVER bulk-delete every .part in the download root.
        if not stems: return 0
        # Protect OTHER tasks' partials by their UNIQUE video id (the old 'claimed'
        # final-name set never matched .part names). Similar titles must not cause
        # task A's 416 cleanup to delete task B's actively-downloading partial.
        with self.state_lock:
            other_ids = {str(t.info_dict["id"]).lower() for t in self.tasks.values()
                         if t.task_id != task.task_id and t.info_dict and t.info_dict.get("id")}
        removed = 0
        for root in roots:
            if not root.exists(): continue
            try:
                # RECURSIVE: playlist tasks download into a subfolder, and at 416
                # time task.filepath may still be unset - a top-level iterdir()
                # would miss the stale .part and loop on 416 forever.
                for path in root.rglob("*"):
                    if path.is_file() and (path.name.endswith((".part", ".ytdl", ".temp")) or ".part-" in path.name):
                        nl = path.name.lower()
                        if any(oid and oid in nl for oid in other_ids): continue
                        if any(s.lower() in nl for s in stems):
                            try: path.unlink(); removed += 1
                            except OSError: pass
            except OSError: pass
        LoggerSetup.log(f"416 cleanup: removed {removed} stale partial file(s) for '{task.title or task.task_id}'.", "debug")
        return removed

    def _set_task_error(self, task: DownloadTask, msg: Any):
        cm = clean_ansi_codes(msg); cat = ErrorClassifier.classify(cm); rem = ErrorClassifier.remediation(cat)
        task.status, task.error_message, task.error_category, task.error_remediation, task.stage_label, task.speed_float = DownloadStatus.ERROR, cm, cat.value, rem, cat.value, 0.0
        if cat == ErrorCategory.RESUME_MISMATCH: self._cleanup_resume_files(task)
        LoggerSetup.log(f"{cat.value}: {rem}", "warning")

    def _watchdog_loop(self):
        while not self.is_shutting_down:
            time.sleep(15)
            if not self.settings.get("watchdog_enabled"): continue
            now, stalled = time.time(), []
            # Scale the metadata-phase budget with configured request sleeps so
            # legitimately slow extraction (proxies, retries) is not killed.
            start_limit = 600 + int(safe_float(self.settings.get("request_sleep_max"), 2.25, 0.0, 60.0) * 20)
            with self.state_lock:
                for tid, th in list(self.active_threads.items()):
                    if not th.is_alive():
                        self.active_threads.pop(tid, None); self._active_runs.pop(tid, None); continue
                    t = self.tasks.get(tid)
                    if not t: continue
                    limit = 300 if t.status == DownloadStatus.DOWNLOADING else (start_limit if t.status == DownloadStatus.STARTING else None)
                    if limit is not None and now - t.last_activity_time > limit:
                        stalled.append(tid); t.is_terminating = True; self._signal_cancel(tid)
            for tid in stalled:
                LoggerSetup.log(f"Watchdog restarting stalled task {tid}...", "warning"); self.retry_task(tid, _watchdog=True)

    def _process_queue_loop(self):
        while not self.is_shutting_down:
            with self.state_lock:
                if self.scheduled_start_ts is not None and time.time() >= self.scheduled_start_ts:
                    self.scheduled_start_ts, self.queue_paused_globally = None, False; LoggerSetup.log("Scheduled queue started!", "info")
                if not self.queue_paused_globally:
                    max_c, idx = safe_int(self.settings.get("max_concurrent_downloads"), 2, 1, 8), 0
                    while len(self.active_threads) < max_c and idx < len(self.download_queue):
                        tid = self.download_queue[idx]
                        if tid in self.active_threads:
                            # Reclaim slots whose worker died without finalizing.
                            if not self.active_threads[tid].is_alive():
                                self.active_threads.pop(tid, None); self._active_runs.pop(tid, None)
                            else:
                                idx += 1; continue
                        self.download_queue.pop(idx); task = self.tasks.get(tid)
                        if task and not task.is_terminating and task.status == DownloadStatus.QUEUED:
                            self._run_counter += 1; rid = self._run_counter; ev = threading.Event()
                            self._active_runs[tid] = (rid, ev); task.status, task.stage_label, task.last_activity_time = DownloadStatus.STARTING, "Initializing", time.time()
                            th = threading.Thread(target=self._execute_smart_download, args=(task, rid, ev), name=f"DL-{rid}", daemon=True)
                            self.active_threads[tid] = th; self.app.run_on_gui_thread(self.app.update_task_ui, tid); th.start()
                        elif task:
                            LoggerSetup.log(f"Dispatcher skipped task {tid} (status={task.status.value}, terminating={task.is_terminating}).", "debug")
            time.sleep(0.35)

    def _execute_smart_download(self, task: DownloadTask, run_id: int, cancel_event: threading.Event):
        success, max_r = False, safe_int(self.settings.get("max_retries"), 5, 0, 20)
        try:
            while task.retry_count <= max_r and not success:
                if cancel_event.is_set() or task.is_terminating or self.is_shutting_down or not self._is_current_run(task.task_id, run_id): break
                try:
                    if task.service_type == ServiceType.INSTAGRAM:
                        success = self._strategy_ytdlp(task, run_id, cancel_event)
                        if not success and not cancel_event.is_set() and instaloader is not None: success = self._strategy_instaloader(task, run_id, cancel_event)
                    else:
                        success = self._strategy_ytdlp(task, run_id, cancel_event)

                    if not success and not cancel_event.is_set() and not task.is_terminating and self._is_current_run(task.task_id, run_id):
                        self._set_task_error(task, task.error_message or "Download failed.")
                        with self.state_lock: task.retry_count += 1
                        # Permanent errors won't fix themselves on retry - stop now
                        # instead of wasting max_retries x retry_delay on each.
                        if task.error_category in {ErrorCategory.UNAVAILABLE.value, ErrorCategory.DRM_PROTECTED.value,
                                                   ErrorCategory.GEO_BLOCKED.value, ErrorCategory.FORMAT_UNAVAILABLE.value}:
                            LoggerSetup.log(f"Permanent error ({task.error_category}); not retrying.", "info")
                            break
                        if task.retry_count <= max_r:
                            if task.error_category in {ErrorCategory.NEEDS_COOKIES.value, ErrorCategory.COOKIE_DB_LOCKED.value} and self.settings.get("auto_cookie_gen"):
                                new_cf = self.antibot.refresh_cookies()
                                if new_cf and new_cf != ANON_COOKIE_FILE:
                                    with self.state_lock:
                                        task.ydl_opts["cookiefile"] = new_cf
                                        task.ydl_opts.pop("cookiesfrombrowser", None)
                                    LoggerSetup.log(f"Auto-retry with refreshed REAL cookies: {new_cf}", "info")
                                else:
                                    # Only anonymous (or no) cookies are available - these cannot
                                    # bypass YouTube bot/login checks. Stop the futile retry loop and
                                    # surface the one action that actually obtains real cookies.
                                    task.error_remediation = ("Real browser cookies are needed. Open Settings > Cookie Helper > "
                                                              "'Extract from OPEN browser (CDP)' once (it keeps your browser open), then Retry.")
                                    LoggerSetup.log("No real browser cookies available (anonymous cookies cannot bypass bot/login checks); stopping retries. Use Cookie Helper > CDP.", "warning")
                                    break
                            delay = safe_int(self.settings.get("retry_delay"), 10, 1, 600)
                            task.stage_label = f"Retry {task.retry_count}/{max_r} in {delay}s"
                            self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)
                            for _ in range(delay * 10):
                                if cancel_event.is_set() or task.is_terminating or self.is_shutting_down: break
                                time.sleep(0.1)
                        else: break
                    else: break
                except Exception as e:
                    LoggerSetup.log(f"Worker Error: {e}", "error", exc_info=True)
                    if not cancel_event.is_set() and not task.is_terminating: self._set_task_error(task, str(e))
                    break
        finally:
            self._finalize_task(task, run_id, cancel_event)

    def _verify_integrity(self, task: DownloadTask):
        if not self.settings.get("verify_hash"):
            LoggerSetup.log(f"Post-download hash check skipped (disabled) for '{task.title}'.", "debug")
            return
        if not task.filepath or not os.path.isfile(task.filepath): return
        algo = str(self.settings.get("hash_algo") or "md5").lower()
        task.status, task.hash_algo, task.stage_label = DownloadStatus.VERIFYING, algo, f"Hashing ({algo.upper()})"
        self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)
        try:
            task.file_hash = compute_file_hash(task.filepath, algo)
            task.status, task.stage_label = DownloadStatus.COMPLETED, "Completed"
            LoggerSetup.log(f"Verified ({algo.upper()}): {task.file_hash}", "info")
        except Exception as e:
            LoggerSetup.log(f"Hash failed: {e}", "error")
            task.status, task.stage_label, task.error_message = DownloadStatus.ERROR, "Verify Failed", f"Integrity verification failed: {e}"

    def _categorize_download(self, task: DownloadTask):
        if not self.settings.get("auto_categorize") or not task.filepath or not os.path.isfile(task.filepath): return
        if task.is_playlist_item and self.settings.get("playlist_subfolder"): task.category = "Playlist"; return
        ext = Path(task.filepath).suffix.lower()
        cat = next((c for c, ex in {"Music": {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus"}, "Video": {".mp4", ".mkv", ".webm", ".avi", ".mov", ".flv"}, "Images": {".jpg", ".jpeg", ".png", ".webp", ".gif"}}.items() if ext in ex), "Other")
        task.category = cat; tdir = Path(self.settings.get("download_path")) / cat; tdir.mkdir(parents=True, exist_ok=True)
        src, dst = Path(task.filepath), tdir / Path(task.filepath).name
        if src.resolve() == dst.resolve(): return
        i = 1
        while dst.exists(): dst = tdir / f"{src.stem} ({i}){src.suffix}"; i += 1
        for attempt in range(5):
            try: shutil.move(str(src), str(dst)); task.filepath = str(dst); break
            except (PermissionError, OSError): time.sleep(min(8, 2 ** attempt))
            except Exception: break

    def _resolve_downloaded_file(self, task: DownloadTask, ydl: yt_dlp.YoutubeDL, info: Dict[str, Any], started_at: float, extra: Optional[List[Any]] = None) -> Optional[str]:
        m_exts = {".mp4", ".mkv", ".webm", ".mov", ".avi", ".flv", ".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus"}
        i_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
        cands: List[Path] = []

        def add_c(v):
            if not v: return
            p = Path(str(v))
            if p not in cands: cands.append(p)

        add_c(task.filepath)
        for x in extra or []: add_c(x)
        if info:
            for k in ("filepath", "_filename", "filename"): add_c(info.get(k))
            for r in info.get("requested_downloads") or []: add_c(r.get("filepath") or r.get("filename"))
            for ent in info.get("entries") or []:
                if isinstance(ent, dict):
                    for k in ("filepath", "_filename", "filename"): add_c(ent.get(k))
            try: add_c(ydl.prepare_filename(info))
            except Exception: pass
        exp = list(cands) + [c.with_suffix(e) for c in cands if c.suffix for e in m_exts]
        for pp in task.ydl_opts.get("postprocessors", []) or []:
            if pp.get("key") == "FFmpegExtractAudio":
                codec = str(pp.get("preferredcodec") or self.settings.get("audio_format") or "mp3").lower()
                exp.extend(c.with_suffix(f".{codec}") for c in cands)
        if task.ydl_opts.get("merge_output_format"):
            exp.extend(c.with_suffix(f".{task.ydl_opts['merge_output_format']}") for c in cands)
        for exts in (m_exts, i_exts):
            for p in exp:
                try:
                    if p.exists() and p.is_file() and p.suffix.lower() in exts: return str(p)
                except OSError: pass
        roots = {Path(self.settings.get("download_path"))} | {c.parent for c in cands if c.parent} | {Path(self.settings.get("download_path")) / s for s in ("Video", "Music", "Images", "Other")}
        stems = {c.stem for c in cands if c.stem}
        if info:
            stems.add(sanitize_filename_part(info.get("title"), limit=80))
            if info.get("id"): stems.add(str(info["id"]))
        # Never attribute a file that another live task already claimed (chapter
        # splits share title/id stems and run concurrently).
        with self.state_lock:
            claimed = {str(Path(t.filepath).resolve()) for t in self.tasks.values() if t.filepath and t.task_id != task.task_id}
        img_expected = any(c.suffix.lower() in i_exts for c in cands)
        matches = []
        for rt in roots:
            if rt.exists():
                try:
                    for p in rt.iterdir():
                        if p.is_file() and p.suffix.lower() in (m_exts | i_exts) and p.stat().st_mtime >= started_at - 10:
                            if str(p.resolve()) in claimed: continue
                            if p.suffix.lower() in i_exts and not img_expected: continue  # a thumbnail is not the media file
                            if not stems or any(s and s.lower() in p.stem.lower() for s in stems): matches.append(p)
                except OSError: pass
        if matches:
            matches.sort(key=lambda p: (p.suffix.lower() in m_exts, p.stat().st_mtime, p.stat().st_size), reverse=True)
            return str(matches[0])
        return None

    def _burn_hardsubs_ffmpeg(self, task: DownloadTask, vp_str: str, cancel_event: Optional[threading.Event] = None) -> str:
        ff, vp = resolve_ffmpeg_location(self.settings.get("ffmpeg_path")), Path(vp_str)
        if not ff or not vp.exists() or vp.suffix.lower() not in {".mp4", ".mkv", ".webm", ".mov", ".avi"}: return vp_str
        cands = [c for ext in (".srt", ".ass", ".ssa", ".vtt") for c in sorted(vp.parent.glob(f"*{ext}")) if c.name.lower().startswith(vp.stem.lower())]
        if not cands: return vp_str
        # Prefer the user's selected subtitle languages over alphabetical order.
        langs = [str(l).lower() for l in (task.ydl_opts.get("subtitleslangs") or []) if l and l != "all"]
        sub = next((c for l in langs for c in cands if f".{l}." in c.name.lower()), cands[0])
        task.status, task.stage_label = DownloadStatus.PROCESSING, "Burning Subtitles (Hardsub)"
        self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)
        # Copy subtitles to a guaranteed-safe filename: avoids all ffmpeg filter
        # escaping pitfalls (colons, quotes, brackets, commas, spaces, RTL names).
        # Per-task name: concurrent hardsub tasks must not share one temp file.
        tmp_sub = vp.parent / f".sina_hardsub_{os.getpid()}_{task.task_id[:12]}{sub.suffix.lower()}"
        out = vp.with_name(f"{vp.stem}.hardsub.mp4")
        err_log = vp.parent / f".sina_hardsub_{os.getpid()}_{task.task_id[:12]}.log"
        proc = None
        burn_ok = False
        try:
            shutil.copyfile(sub, tmp_sub)
            # stderr -> FILE, not a pipe: a full stderr pipe blocks ffmpeg forever
            # while wait() loops, deadlocking the burn for up to 2h on noisy errors.
            with open(err_log, "w+", encoding="utf-8", errors="replace") as ef:
                proc = subprocess.Popen(
                    [ff, "-y", "-loglevel", "error", "-i", vp.name, "-vf", f"subtitles={tmp_sub.name}",
                     "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-c:a", "aac", "-b:a", "192k", out.name],
                    cwd=str(vp.parent), stdout=subprocess.DEVNULL, stderr=ef)
                deadline = time.time() + 7200
                while True:
                    try:
                        proc.wait(timeout=0.5); break
                    except subprocess.TimeoutExpired:
                        if (cancel_event is not None and cancel_event.is_set()) or task.is_terminating or self.is_shutting_down:
                            proc.terminate()
                            try: proc.wait(timeout=5)
                            except subprocess.TimeoutExpired: proc.kill()
                            LoggerSetup.log("Hardsub burn cancelled.", "info"); return str(vp)
                        if time.time() > deadline:
                            proc.kill(); raise RuntimeError("Hardsub burn timed out (2h).")
                        task.last_activity_time = time.time()
            err = ""
            try: err = err_log.read_text(encoding="utf-8", errors="replace")
            except OSError: pass
            if proc.returncode == 0 and out.exists() and out.stat().st_size > 0:
                burn_ok = True
                if (cancel_event is not None and cancel_event.is_set()) or task.is_terminating: return str(vp)
                if vp.suffix.lower() == ".mp4":
                    os.replace(out, vp); return str(vp)
                LoggerSetup.log(f"Hardsub created: {out.name} (original kept)", "info")
                return str(out)
            LoggerSetup.log(f"Hardsub failed (rc={proc.returncode}): {err.strip()[-400:]}", "warning")
        except Exception as e:
            LoggerSetup.log(f"Hardsub error: {e}", "warning")
        finally:
            if proc is not None and proc.poll() is None:
                try: proc.kill()
                except OSError: pass
            try: tmp_sub.unlink(missing_ok=True)
            except OSError: pass
            try: err_log.unlink(missing_ok=True)
            except OSError: pass
            try:
                # A killed/failed burn can leave a multi-GB partial output - remove it
                # unless the burn actually succeeded.
                if not burn_ok and out.exists(): out.unlink(missing_ok=True)
            except OSError: pass
        return str(vp)

    def _strategy_ytdlp(self, task: DownloadTask, run_id: int, cancel_event: threading.Event) -> bool:
        opts = copy.deepcopy(task.ydl_opts) if isinstance(task.ydl_opts, dict) else {}
        fp, ex_h = self.fingerprint.get_yt_dlp_options(task.url), opts.get("http_headers") or {}
        for k, v in fp.items():
            if k != "http_headers": opts.setdefault(k, v)
        if fp.get("http_headers") or ex_h: opts["http_headers"] = {**(fp.get("http_headers") or {}), **ex_h}
        with self.state_lock: active_n = max(1, len(self.active_threads))
        self.antibot.apply_common_options(opts, url=task.url, active_count=active_n)
        if opts.get("download_ranges_spec"):
            opts["download_ranges"] = yt_dlp.utils.download_range_func(None, [(float(s), None if e is None else float(e)) for s, e in opts.pop("download_ranges_spec")])
            opts["force_keyframes_at_cuts"] = True

        burn_subs, sb_cats = bool(opts.pop("_burn_subtitles", False)), opts.pop("_sponsorblock_categories", None)
        base_pps, ordered_pps = list(opts.get("postprocessors") or []), []
        if sb_cats:
            cats = [str(c) for c in sb_cats if c]
            if cats: ordered_pps.append({"key": "SponsorBlock", "categories": set(cats), "api": "https://sponsor.ajay.app", "when": "after_filter"})
        if burn_subs and (opts.get("writesubtitles") or opts.get("writeautomaticsub")):
            opts["embedsubtitles"], opts["subtitlesformat"] = False, "srt/best"
            ordered_pps.append({"key": "FFmpegSubtitlesConvertor", "format": "srt", "when": "before_dl"})
        if opts.get("writethumbnail"): ordered_pps.append({"key": "FFmpegThumbnailsConvertor", "format": "jpg", "when": "before_dl"})
        ordered_pps.extend(p for p in base_pps if p.get("key") == "FFmpegExtractAudio")
        ordered_pps.extend(p for p in base_pps if p.get("key") not in {"FFmpegExtractAudio", "FFmpegMetadata", "EmbedThumbnail", "FFmpegEmbedSubtitle", "SponsorBlock", "ModifyChapters"})
        if opts.get("embedsubtitles") and not burn_subs: ordered_pps.append({"key": "FFmpegEmbedSubtitle"})
        if sb_cats:
            cats = [str(c) for c in sb_cats if c]
            if cats: ordered_pps.append({"key": "ModifyChapters", "remove_sponsor_segments": set(cats)})
        for tk in ("FFmpegMetadata", "EmbedThumbnail"):
            for p in base_pps:
                if p.get("key") == tk: ordered_pps.append(p); break
        if ordered_pps: opts["postprocessors"] = ordered_pps

        if self.settings.get("use_aria2"):
            a2 = detect_aria2(self.settings.get("aria2_path"))
            if a2: opts["external_downloader"], opts["external_downloader_args"] = a2, {"default": ["-j", "16", "-x", "16", "-s", "16", "-k", "1M"]}
        arch_on = bool(self.settings.get("playlist_sync") and (task.is_playlist_item or task.category == "Playlist"))
        if arch_on: opts["download_archive"] = str(Path(self.settings.get("download_path")) / ARCHIVE_FILE)

        last_dl, last_ui, pp_cands = {"b": None}, {"ts": 0.0}, []

        def sync_meta(inf: Dict[str, Any]):
            if not inf: return
            if inf.get("title") and (task.is_placeholder_title or task.title in {"Fetching Title...", "Restored Download", ""}):
                task.title, task.is_placeholder_title = str(inf["title"]), False
            if not task.uploader and (inf.get("uploader") or inf.get("channel")): task.uploader = str(inf.get("uploader") or inf.get("channel"))
            if not task.duration_sec and inf.get("duration"): task.duration_sec = inf["duration"]
            if not task.thumbnail_url and inf.get("thumbnail"): task.thumbnail_url = inf["thumbnail"]

        def progress_hook(d: Dict[str, Any]):
            if cancel_event.is_set() or task.is_terminating or not self._is_current_run(task.task_id, run_id):
                raise yt_dlp.utils.DownloadError("Download aborted by user.")
            now = time.time(); task.last_activity_time = now; inf = d.get("info_dict") or {}; sync_meta(inf)
            vc, ac = inf.get("vcodec"), inf.get("acodec")
            s_lbl = "Video Stream" if (vc and vc != "none" and (not ac or ac == "none")) else ("Audio Stream" if (ac and ac != "none" and (not vc or vc == "none")) else "Media")
            if d.get("status") == "downloading":
                task.status, task.stage_label = DownloadStatus.DOWNLOADING, s_lbl
                dl_b = safe_int(d.get("downloaded_bytes"), 0, 0)
                # First hook of a (possibly resumed) stream: downloaded_bytes
                # already includes the pre-existing .part prefix - don't
                # double-count it into the session telemetry.
                prev = last_dl["b"]
                with self.state_lock: self.session_bytes_downloaded += (0 if prev is None else max(0, dl_b - prev))
                last_dl["b"], task.downloaded_bytes = dl_b, dl_b
                tot_b = d.get("total_bytes") or d.get("total_bytes_estimate")
                if tot_b:
                    task.total_bytes = int(tot_b); task.progress_float = min(1.0, max(0.0, dl_b / float(tot_b)))
                    task.progress_str, task.total_bytes_str = f"{task.progress_float:.1%}", format_bytes(tot_b, True)
                else: task.total_bytes_str = format_bytes(dl_b, True)
                spd = d.get("speed")
                if spd and spd > 0:
                    task.speed_float, task.peak_speed, task.speed_str = float(spd), max(task.peak_speed, float(spd)), f"{format_bytes(spd, False)}/s"
                    task.speed_history.append(float(spd))
                    if len(task.speed_history) > 50: task.speed_history.pop(0)
                eta = d.get("eta")
                task.eta_str = format_duration(eta) if eta is not None else (clean_ansi_codes(d.get("_eta_str", "N/A")).strip() or "N/A")
                if now - last_ui["ts"] >= 0.15: last_ui["ts"] = now; self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)
            elif d.get("status") == "finished":
                last_dl["b"] = None; task.status, task.stage_label, task.progress_float, task.speed_float = DownloadStatus.PROCESSING, f"Finished {s_lbl}", 1.0, 0.0
                fn = d.get("filename")
                if fn and not fn.endswith((".part", ".ytdl", ".temp")) and not re.search(r"\.f\d+\.[^.]+$", fn): task.filepath = fn
                self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)

        def pp_hook(d: Dict[str, Any]):
            if cancel_event.is_set() or task.is_terminating or not self._is_current_run(task.task_id, run_id):
                raise yt_dlp.utils.DownloadError("Post-processing aborted by user.")
            task.last_activity_time = time.time(); inf = d.get("info_dict") or {}
            for k in ("filepath", "_filename", "filename"):
                if d.get(k): pp_cands.append(d[k])
                if inf.get(k): pp_cands.append(inf[k])
            if d.get("status") == "started": task.status, task.stage_label = DownloadStatus.PROCESSING, d.get("postprocessor") or "Post-Processing"
            elif d.get("status") == "finished":
                for k in ("filepath", "filename"):
                    if d.get(k): task.filepath = d[k]
            self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)

        try:
            opts["progress_hooks"], opts["postprocessor_hooks"], t0 = [progress_hook], [pp_hook], time.time()
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(task.url, download=True)
                if cancel_event.is_set() or task.is_terminating or not self._is_current_run(task.task_id, run_id): return False
                if not info:
                    if arch_on: task.status, task.progress_float, task.progress_str, task.stage_label = DownloadStatus.SKIPPED, 1.0, "Skipped", "Already in archive"; return True
                    raise yt_dlp.utils.DownloadError("No media information returned.")
                try: task.filepath = ydl.prepare_filename(info)
                except Exception: pass
                sync_meta(info); resolved = self._resolve_downloaded_file(task, ydl, info, t0, pp_cands)
                mcap = re.search(r"height<=(\d+)", str(task.ydl_opts.get("format") or ""))
                if mcap:
                    got_h = safe_int(info.get("height"), 0, 0)
                    if 0 < got_h < int(mcap.group(1)):
                        LoggerSetup.log(f"Quality notice: requested <={mcap.group(1)}p but best available was {got_h}p (separate streams may be unavailable for this video/client).", "warning")

            if cancel_event.is_set() or task.is_terminating: return False
            if resolved:
                if burn_subs: resolved = self._burn_hardsubs_ffmpeg(task, resolved, cancel_event)
                if cancel_event.is_set() or task.is_terminating or not self._is_current_run(task.task_id, run_id): return False
                task.filepath = resolved
                try: task.total_bytes = Path(resolved).stat().st_size; task.total_bytes_str = format_bytes(task.total_bytes, True)
                except OSError: pass
                task.status, task.stage_label, task.progress_float, task.progress_str, task.speed_float, task.completed_at = DownloadStatus.COMPLETED, "Completed", 1.0, "100%", 0.0, time.time()
                LoggerSetup.log(f"Download completed: {task.filepath}", "info"); return True
            if arch_on: task.status, task.progress_float, task.progress_str, task.stage_label = DownloadStatus.SKIPPED, 1.0, "Skipped", "Already in archive"; return True
            task.status, task.error_message = DownloadStatus.ERROR, "Download finished but no output media file was found."; return False
        except Exception as e:
            if not cancel_event.is_set() and not task.is_terminating and self._is_current_run(task.task_id, run_id):
                task.status, task.error_message = DownloadStatus.ERROR, clean_ansi_codes(str(e))
            return False

    def _strategy_instaloader(self, task: DownloadTask, run_id: int, cancel_event: threading.Event) -> bool:
        if not instaloader: return False
        L = None
        try:
            task.status, task.stage_label, task.last_activity_time = DownloadStatus.DOWNLOADING, "Instagram Engine", time.time()
            self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)
            m = re.search(r"(?:p|reel|reels|tv)/([^/?#&]+)", task.url)
            if not m: raise ValueError("Invalid Instagram URL.")
            sc = m.group(1)
            if not re.fullmatch(r"[A-Za-z0-9_-]+", sc): raise ValueError("Invalid Instagram shortcode.")
            tdir = Path(self.settings.get("download_path")) / f"ig_{sc}"; tdir.mkdir(parents=True, exist_ok=True)
            L = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False, quiet=True, dirname_pattern=str(tdir), request_timeout=30)
            u, p = self.settings.get("instagram_user"), self.settings.get("instagram_pass")
            if u and p:
                try: L.login(u, p)
                except Exception: pass
            if cancel_event.is_set() or task.is_terminating: return False
            post = instaloader.Post.from_shortcode(L.context, sc)
            if post.caption and (task.is_placeholder_title or task.title in {"Fetching Title...", "Instagram"}):
                task.title, task.is_placeholder_title = sanitize_filename_part(post.caption.splitlines()[0], default=f"Instagram {sc}", limit=100), False
            # download_post has no cancel/progress hooks: run it in a sub-thread
            # and poll cancellation + heartbeat here, with an overall hard cap so
            # a hung transfer can never leak a concurrency slot forever.
            done_ev, err_box = threading.Event(), []

            def _dl():
                try: L.download_post(post, target=str(tdir))
                except Exception as e: err_box.append(e)
                finally: done_ev.set()

            th = threading.Thread(target=_dl, name=f"IG-{sc}", daemon=True); th.start()
            hard_deadline = time.time() + 1800
            while not done_ev.wait(0.5):
                if cancel_event.is_set() or task.is_terminating or not self._is_current_run(task.task_id, run_id): return False
                if time.time() > hard_deadline: raise RuntimeError("Instagram download timed out (30 min).")
                task.last_activity_time = time.time()
            if err_box: raise err_box[0]
            if cancel_event.is_set() or task.is_terminating or not self._is_current_run(task.task_id, run_id): return False
            files = sorted([f for f in tdir.iterdir() if f.is_file() and f.suffix.lower() in {".mp4", ".jpg", ".jpeg", ".png", ".webp"}], key=lambda f: (f.suffix.lower() == ".mp4", f.stat().st_size), reverse=True)
            if not files: raise RuntimeError("No media file created by Instaloader.")
            task.filepath = str(files[0]); task.total_bytes = files[0].stat().st_size; task.total_bytes_str = format_bytes(task.total_bytes, True)
            task.status, task.stage_label, task.progress_float, task.progress_str, task.completed_at = DownloadStatus.COMPLETED, "Completed", 1.0, "100%", time.time()
            return True
        except Exception as e:
            if not cancel_event.is_set() and not task.is_terminating: task.status, task.error_message = DownloadStatus.ERROR, clean_ansi_codes(str(e))
            return False
        finally:
            if L is not None:
                try: L.close()
                except Exception: pass

    def _finalize_task(self, task: DownloadTask, run_id: int, cancel_event: threading.Event):
        is_cur = self._is_current_run(task.task_id, run_id)
        if is_cur and not cancel_event.is_set() and task.status == DownloadStatus.COMPLETED:
            self._verify_integrity(task)
            # Cancel may arrive during (slow) hashing/categorization - never
            # overwrite CANCELLED back to COMPLETED or move the file anyway.
            if not cancel_event.is_set() and not task.is_terminating and task.status == DownloadStatus.COMPLETED:
                self._categorize_download(task)
            if not cancel_event.is_set() and not task.is_terminating and task.status == DownloadStatus.COMPLETED:
                task.stage_label = "Completed"
        check_done = False
        with self.state_lock:
            # Always reclaim our own slot, even if a newer run superseded us
            # (otherwise a dead worker would block the dispatcher forever).
            if self.active_threads.get(task.task_id) is threading.current_thread():
                self.active_threads.pop(task.task_id, None)
            if is_cur:
                self._active_runs.pop(task.task_id, None)
                if not cancel_event.is_set() and task.status not in {DownloadStatus.QUEUED, DownloadStatus.COMPLETED, DownloadStatus.SKIPPED, DownloadStatus.ERROR, DownloadStatus.CANCELLED, DownloadStatus.PAUSED, DownloadStatus.VERIFYING}:
                    task.status = DownloadStatus.INVALID
                task.speed_float = 0.0
                if not self.active_threads and not self.download_queue and not self._completion_notified:
                    has_comp = any(t.status == DownloadStatus.COMPLETED for t in self.tasks.values())
                    if has_comp: check_done = self._completion_notified = True
        self.app.run_on_gui_thread(self.app.update_task_ui, task.task_id)
        if notification and is_cur and not cancel_event.is_set() and task.status == DownloadStatus.COMPLETED:
            try: notification.notify(title=APP_NAME, message=f"Completed: {(task.title or 'Media')[:60]}", app_name=APP_NAME, timeout=6)
            except Exception: pass
        self.app.run_on_gui_thread(self.app.update_status_bar)
        if check_done and not self.is_shutting_down: self.app.run_on_gui_thread(self.app._handle_all_downloads_finished)

    def shutdown(self):
        self.is_shutting_down = True
        with self.state_lock:
            for tid, t in self.tasks.items():
                if t.status in {DownloadStatus.DOWNLOADING, DownloadStatus.STARTING, DownloadStatus.PROCESSING, DownloadStatus.VERIFYING, DownloadStatus.QUEUED}:
                    t.is_terminating, t.status, t.stage_label = True, DownloadStatus.CANCELLED, "Cancelled (Exit)"
                self._signal_cancel(tid)
            threads = list(self.active_threads.values())
        # Bounded join so workers can abort cleanly (and their ffmpeg/aria2
        # children see the cancel) instead of being orphaned mid-write.
        deadline = time.time() + 8.0
        for th in threads:
            try: th.join(timeout=max(0.05, deadline - time.time()))
            except RuntimeError: pass

    def export_queue(self, dest: str) -> int:
        with self.state_lock: data = [t.to_dict() for t in self.tasks.values()]
        p = Path(dest); tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, p)
        return len(data)

    def import_queue(self, src: str) -> int:
        data = json.loads(Path(src).read_text(encoding="utf-8"))
        if not isinstance(data, list): raise ValueError("Invalid queue JSON.")
        cnt = skipped = 0
        for entry in data:
            try:
                t = DownloadTask.from_dict(entry)
            except Exception:
                skipped += 1; continue
            with self.state_lock:
                if t.task_id in self.tasks: t.task_id = f"imp_{time.time_ns()}_{random.randint(100, 999)}"
            self.add_task(t, from_restore=True); cnt += 1
        if skipped: LoggerSetup.log(f"Import skipped {skipped} invalid queue entry(s).", "warning")
        return cnt


# --- Dialogs & UI (pure tkinter / ttk, no CustomTkinter) ---

UI_FONT = "Segoe UI" if sys.platform == "win32" else "Arial"


def safe_grab_set(win):
    """grab_set that tolerates X11 'window not viewable' (grab before the window
    is mapped). Retries once the window becomes visible instead of raising."""
    try:
        win.grab_set()
    except tkinter.TclError:
        try:
            win.wait_visibility()
            win.grab_set()
        except Exception:
            pass
    except Exception:
        pass


def restore_parent_grab(win, parent):
    """When a nested modal child closes, re-grab the still-open parent so it
    stays modal (Tk drops the grab entirely when the grabbing window dies)."""
    def _on_destroy(event):
        if event.widget is not win: return
        try:
            # Only re-grab a modal parent dialog (Toplevel), never the root window.
            if parent is not None and isinstance(parent, tkinter.Toplevel) and parent.winfo_exists():
                parent.grab_set()
        except Exception:
            pass
    try:
        win.bind("<Destroy>", _on_destroy, add="+")
    except Exception:
        pass


def setup_styles(root, font: Optional[str] = None):
    """Flat dark/light theme for all ttk widgets (re-runnable on theme change)."""
    f = font or UI_FONT
    p = ThemeColors.palette()
    accent = ColorPalette.ACCENT_COLOR.value
    accent_h = ColorPalette.ACCENT_HOVER.value
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    root.configure(bg=p["BG"])
    style.configure(".", background=p["BG"], foreground=p["TEXT_PRIMARY"], fieldbackground=p["INPUT"],
                    bordercolor=p["BORDER"], lightcolor=p["CARD"], darkcolor=p["CARD"],
                    troughcolor=p["CARD_ALT"], focuscolor=accent, font=(f, 11))
    style.configure("TFrame", background=p["BG"])
    style.configure("Card.TFrame", background=p["CARD"])
    style.configure("Alt.TFrame", background=p["CARD_ALT"])
    style.configure("Sidebar.TFrame", background=p["SIDEBAR"])
    style.configure("TLabel", background=p["BG"], foreground=p["TEXT_PRIMARY"], font=(f, 12))
    style.configure("Card.TLabel", background=p["CARD"], foreground=p["TEXT_PRIMARY"], font=(f, 12))
    style.configure("Muted.TLabel", background=p["BG"], foreground=p["TEXT_MUTED"], font=(f, 11))
    style.configure("CardMuted.TLabel", background=p["CARD"], foreground=p["TEXT_MUTED"], font=(f, 11))
    style.configure("Title.TLabel", background=p["BG"], foreground=p["TEXT_PRIMARY"], font=(f, 20, "bold"))
    style.configure("H2.TLabel", background=p["BG"], foreground=p["TEXT_PRIMARY"], font=(f, 15, "bold"))
    style.configure("Accent.TLabel", background=p["BG"], foreground=accent, font=(f, 12, "bold"))
    style.configure("Badge.TLabel", background=p["BADGE_BG"], foreground=p["BADGE_TEXT"], font=(f, 10, "bold"), padding=(8, 3))
    style.configure("TButton", background=p["CARD_ALT"], foreground=p["TEXT_PRIMARY"], font=(f, 11), padding=(10, 6), borderwidth=0, focusthickness=0)
    style.map("TButton", background=[("active", p["BORDER"]), ("disabled", p["CARD_ALT"])], foreground=[("disabled", p["TEXT_MUTED"])])
    style.configure("Accent.TButton", background=accent, foreground="#FFFFFF", font=(f, 11, "bold"), padding=(12, 7))
    style.map("Accent.TButton", background=[("active", accent_h), ("disabled", p["BORDER"])], foreground=[("disabled", p["TEXT_MUTED"])])
    style.configure("Danger.TButton", background=ColorPalette.BUTTON_CANCEL_FG.value, foreground="#FFFFFF", padding=(10, 6))
    style.map("Danger.TButton", background=[("active", ColorPalette.BUTTON_CANCEL_HOVER.value), ("disabled", p["BORDER"])])
    style.configure("Success.TButton", background=ColorPalette.BUTTON_ACTION_FG.value, foreground="#FFFFFF", padding=(10, 6))
    style.map("Success.TButton", background=[("active", ColorPalette.BUTTON_ACTION_HOVER.value), ("disabled", p["BORDER"])])
    style.configure("Warning.TButton", background="#D97706", foreground="#FFFFFF", padding=(10, 6))
    style.map("Warning.TButton", background=[("active", "#B45309"), ("disabled", p["BORDER"])])
    style.configure("Teal.TButton", background="#0F766E", foreground="#FFFFFF", padding=(10, 6))
    style.map("Teal.TButton", background=[("active", "#115E59"), ("disabled", p["BORDER"])])
    style.configure("Icon.TButton", background=p["CARD_ALT"], foreground=p["TEXT_PRIMARY"], padding=(5, 5))
    style.map("Icon.TButton", background=[("active", p["BORDER"]), ("disabled", p["CARD_ALT"])])
    style.configure("Ghost.TButton", background=p["SIDEBAR"], foreground=p["TEXT_PRIMARY"], anchor="w", padding=(12, 10), font=(f, 12, "bold"))
    style.map("Ghost.TButton", background=[("active", p["NAV_ACTIVE"])])
    style.configure("GhostActive.TButton", background=p["NAV_ACTIVE"], foreground=p["TEXT_PRIMARY"], anchor="w", padding=(12, 10), font=(f, 12, "bold"))
    style.map("GhostActive.TButton", background=[("active", p["BORDER"])])
    style.configure("TEntry", fieldbackground=p["INPUT"], foreground=p["TEXT_PRIMARY"], insertcolor=p["TEXT_PRIMARY"],
                    bordercolor=p["BORDER"], lightcolor=p["BORDER"], darkcolor=p["BORDER"], padding=6)
    style.map("TEntry", fieldbackground=[("disabled", p["CARD_ALT"])], bordercolor=[("focus", accent)])
    style.configure("TCombobox", fieldbackground=p["INPUT"], background=p["CARD_ALT"], foreground=p["TEXT_PRIMARY"],
                    arrowcolor=p["TEXT_PRIMARY"], bordercolor=p["BORDER"], padding=4)
    style.map("TCombobox", fieldbackground=[("readonly", p["INPUT"]), ("disabled", p["CARD_ALT"])],
              foreground=[("readonly", p["TEXT_PRIMARY"])], arrowcolor=[("disabled", p["TEXT_MUTED"])])
    root.option_add("*TCombobox*Listbox.background", p["INPUT"])
    root.option_add("*TCombobox*Listbox.foreground", p["TEXT_PRIMARY"])
    root.option_add("*TCombobox*Listbox.selectBackground", accent)
    root.option_add("*TCombobox*Listbox.selectForeground", "#FFFFFF")
    root.option_add("*TCombobox*Listbox.font", (f, 11))
    style.configure("TCheckbutton", background=p["BG"], foreground=p["TEXT_PRIMARY"], font=(f, 11), focusthickness=0)
    style.map("TCheckbutton", background=[("active", p["BG"])], foreground=[("disabled", p["TEXT_MUTED"])])
    style.configure("Card.TCheckbutton", background=p["CARD"], foreground=p["TEXT_PRIMARY"], font=(f, 11))
    style.map("Card.TCheckbutton", background=[("active", p["CARD"])])
    style.configure("Alt.TCheckbutton", background=p["CARD_ALT"], foreground=p["TEXT_PRIMARY"], font=(f, 11))
    style.map("Alt.TCheckbutton", background=[("active", p["CARD_ALT"])])
    style.configure("TNotebook", background=p["BG"], borderwidth=0, tabmargins=(4, 4, 4, 0))
    style.configure("TNotebook.Tab", background=p["CARD_ALT"], foreground=p["TEXT_MUTED"], padding=(14, 8), font=(f, 11, "bold"), borderwidth=0)
    style.map("TNotebook.Tab", background=[("selected", accent)], foreground=[("selected", "#FFFFFF")], expand=[("selected", (0, 0, 0, 2))])
    style.configure("Horizontal.TProgressbar", background=accent, troughcolor=p["CARD_ALT"], bordercolor=p["CARD_ALT"],
                    lightcolor=accent, darkcolor=accent, thickness=8)
    style.configure("Treeview", background=p["CARD"], fieldbackground=p["CARD"], foreground=p["TEXT_PRIMARY"],
                    borderwidth=0, rowheight=27, font=(f, 11))
    style.configure("Treeview.Heading", background=p["CARD_ALT"], foreground=p["TEXT_PRIMARY"], font=(f, 10, "bold"), padding=(6, 6))
    style.map("Treeview", background=[("selected", accent)], foreground=[("selected", "#FFFFFF")])
    style.map("Treeview.Heading", background=[("active", p["BORDER"])])
    style.configure("TScrollbar", background=p["CARD_ALT"], troughcolor=p["BG"], bordercolor=p["BG"],
                    arrowcolor=p["TEXT_MUTED"], lightcolor=p["CARD_ALT"], darkcolor=p["CARD_ALT"])
    style.map("TScrollbar", background=[("active", p["BORDER"])])
    style.configure("TSeparator", background=p["BORDER"])


def _install_wheel_router(root):
    """Route mouse wheel to the scrollable canvas under the pointer (nested-safe)."""
    def find_canvas(event):
        try:
            w = root.winfo_containing(event.x_root, event.y_root)
        except Exception:
            return None
        while w is not None:
            if isinstance(w, tk.Canvas) and getattr(w, "_scrollable", False):
                return w
            w = getattr(w, "master", None)
        return None

    def on_wheel(event):
        c = find_canvas(event)
        if c is not None:
            c.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_btn(event, direction):
        c = find_canvas(event)
        if c is not None:
            c.yview_scroll(direction, "units")

    root.bind_all("<MouseWheel>", on_wheel)
    root.bind_all("<Button-4>", lambda e: on_btn(e, -3))
    root.bind_all("<Button-5>", lambda e: on_btn(e, 3))


class ScrollFrame(ttk.Frame):
    """Vertically scrollable frame (canvas + inner frame + scrollbar)."""

    def __init__(self, parent, style: str = "TFrame", canvas_bg: Optional[str] = None):
        super().__init__(parent, style=style)
        p = ThemeColors.palette()
        self.canvas = tk.Canvas(self, bg=canvas_bg or p["BG"], highlightthickness=0, bd=0)
        self.canvas._scrollable = True
        self.sb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas, style=style)
        self._win = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.sb.pack(side="right", fill="y")
        self.inner.bind("<Configure>", lambda _e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self._win, width=e.width))


def ask_string(parent, title: str, prompt: str, initial: str = "") -> Optional[str]:
    dlg = tk.Toplevel(parent)
    dlg.title(title); dlg.configure(bg=ThemeColors.BG)
    safe_grab_set(dlg); dlg.transient(parent); dlg.resizable(False, False); restore_parent_grab(dlg, parent)
    ttk.Label(dlg, text=prompt, wraplength=400, justify="left").pack(padx=16, pady=(16, 8))
    var = tk.StringVar(master=dlg, value=initial)
    ent = ttk.Entry(dlg, textvariable=var, width=56)
    ent.pack(padx=16, pady=4); ent.focus_set()
    result: Dict[str, Optional[str]] = {"v": None}

    def ok():
        result["v"] = var.get(); dlg.destroy()

    bf = ttk.Frame(dlg); bf.pack(pady=12)
    ttk.Button(bf, text="OK", style="Accent.TButton", command=ok).pack(side="left", padx=4)
    ttk.Button(bf, text="Cancel", command=dlg.destroy).pack(side="left", padx=4)
    dlg.bind("<Return>", lambda _e: ok())
    dlg.protocol("WM_DELETE_WINDOW", dlg.destroy)
    dlg.wait_window()
    return result["v"]


class SettingsWindow(tk.Toplevel):
    def __init__(self, parent: "SinaEnterpriseApp", sm: SettingsManager, apply_cb: Callable[[], None]):
        super().__init__(parent)
        self.sm, self.apply_cb = sm, apply_cb
        self.title("System Settings & Enterprise Controls")
        self.geometry("960x780"); self.minsize(800, 600)
        self.configure(bg=ThemeColors.BG); safe_grab_set(self); self.transient(parent); restore_parent_grab(self, parent)
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=12, pady=(12, 4))
        self.frames: Dict[str, ttk.Frame] = {}
        for name in ("General & Storage", "Security & Anti-Bot", "Network & Engines", "Processing & Automation"):
            sf = ScrollFrame(self.nb)
            self.nb.add(sf, text=name)
            sf.inner.grid_columnconfigure(1, weight=1)
            self.frames[name] = sf.inner
        self._vars: Dict[str, tk.Variable] = {}
        self._build_tabs()
        # Snapshot values at open so Save only writes fields the user actually
        # changed (avoids clobbering concurrent edits made elsewhere, e.g. the
        # dashboard speed cap or the FFmpeg auto-installer, while this was open).
        self._snapshot: Dict[str, Any] = {k: v.get() for k, v in self._vars.items()}
        bf = ttk.Frame(self); bf.pack(fill="x", padx=16, pady=12)
        ttk.Button(bf, text="Save & Apply", style="Accent.TButton", command=self._save).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(bf, text="Cancel", command=self.destroy).pack(side="right", fill="x", expand=True, padx=4)

    def _sec(self, p, r: int, txt: str) -> int:
        ttk.Label(p, text=txt, style="Accent.TLabel", font=(UI_FONT, 13, "bold"), anchor="w").grid(row=r, column=0, columnspan=2, sticky="w", padx=12, pady=(14, 6))
        return r + 1

    def _row(self, p, r: int, lbl: str, w) -> int:
        ttk.Label(p, text=lbl, anchor="w").grid(row=r, column=0, sticky="w", padx=12, pady=5)
        w.grid(row=r, column=1, sticky="ew", padx=(0, 12), pady=5)
        return r + 1

    def _ent(self, p, r: int, lbl: str, key: str, show: str = "") -> int:
        v = tk.StringVar(master=self, value=str(self.sm.get(key) or "")); self._vars[key] = v
        return self._row(p, r, lbl, ttk.Entry(p, textvariable=v, show=show))

    def _opt(self, p, r: int, lbl: str, key: str, vals: List[str]) -> int:
        v = tk.StringVar(master=self, value=str(self.sm.get(key))); self._vars[key] = v
        cb = ttk.Combobox(p, textvariable=v, values=vals, state="readonly")
        return self._row(p, r, lbl, cb)

    def _chk(self, p, r: int, txt: str, key: str) -> int:
        v = tk.BooleanVar(master=self, value=bool(self.sm.get(key))); self._vars[key] = v
        ttk.Checkbutton(p, text=txt, variable=v).grid(row=r, column=0, columnspan=2, sticky="w", padx=12, pady=4)
        return r + 1

    def _path_row(self, p, r: int, lbl: str, key: str, is_dir: bool = False, extra_btn: Optional[Tuple[str, Callable]] = None) -> int:
        box = ttk.Frame(p); box.grid_columnconfigure(0, weight=1)
        v = tk.StringVar(master=self, value=str(self.sm.get(key) or "")); self._vars[key] = v
        ttk.Entry(box, textvariable=v).grid(row=0, column=0, sticky="ew")

        def pick():
            res = filedialog.askdirectory(parent=self) if is_dir else filedialog.askopenfilename(parent=self)
            if res: v.set(res)

        ttk.Button(box, text="...", width=4, command=pick).grid(row=0, column=1, padx=(6, 0))
        if extra_btn:
            ttk.Button(box, text=extra_btn[0], style="Teal.TButton", command=extra_btn[1]).grid(row=0, column=2, padx=(6, 0))
        return self._row(p, r, lbl, box)

    def _build_tabs(self):
        # Tab 1: General
        p, r = self.frames["General & Storage"], 0
        r = self._sec(p, r, "Storage & Naming")
        r = self._path_row(p, r, "Download Folder:", "download_path", is_dir=True)
        r = self._ent(p, r, "Filename Pattern:", "filename_pattern")
        r = self._sec(p, r, "Queue, Speed & Appearance")
        r = self._opt(p, r, "UI Theme:", "theme", ["Dark", "Light", "System"])
        r = self._opt(p, r, "Default Mode:", "default_download_type", ["Video", "Audio"])
        r = self._ent(p, r, "Max Concurrent (1-8):", "max_concurrent_downloads")
        r = self._ent(p, r, "Max Retries (0-20):", "max_retries")
        r = self._ent(p, r, "Retry Delay (s):", "retry_delay")
        r = self._ent(p, r, "Speed Cap (KB/s, 0=Max):", "global_speed_limit_kbps")
        r = self._chk(p, r, "Minimize to System Tray on Close", "close_to_tray")
        r = self._chk(p, r, "Smart Clipboard URL Monitor", "clipboard_monitor")
        self._chk(p, r, "Enable Verbose Debug Logging", "debug_mode")

        # Tab 2: Security & Anti-Bot
        p, r = self.frames["Security & Anti-Bot"], 0
        r = self._sec(p, r, "Cookie Engine (correct extraction)")
        r = self._chk(p, r, "Auto-Fix Cookies on Auth Error (extract from browser / warm-up)", "auto_cookie_gen")
        r = self._opt(p, r, "Cookie Source:", "cookie_source", ["auto", "file", "browser", "none"])
        r = self._opt(p, r, "Browser Profile:", "cookie_browser", ["auto", "chrome", "edge", "firefox", "brave", "opera", "vivaldi", "chromium"])
        r = self._path_row(p, r, "Cookies File Path:", "cookies_file_path", extra_btn=("Extract Now", self._extract_cookies))
        wb = ttk.Frame(p); wb.grid(row=r, column=1, sticky="ew", padx=(0, 12), pady=4); r += 1
        ttk.Button(wb, text="Cookie Helper...", style="Accent.TButton", command=lambda: CookieHelperDialog(self, self.sm, self.master)).pack(side="left")
        ttk.Button(wb, text="Anonymous Warm-up (Playwright)", style="Teal.TButton", command=self._gen_cookies).pack(side="left", padx=(8, 0))
        ttk.Label(wb, text="auto = your file -> live browser extraction -> yt-dlp engine", style="Muted.TLabel").pack(side="left", padx=10)
        r = self._sec(p, r, "YouTube Client, EJS & Rate Limits")
        r = self._opt(p, r, "Player Client Profile:", "youtube_client_profile", list(AntiBotManager.CLIENT_PROFILES.keys()))
        r = self._chk(p, r, "Enable yt-dlp Remote EJS Solver (when Deno/Node installed)", "ytdlp_remote_ejs")
        r = self._ent(p, r, "Request Sleep Min (s):", "request_sleep_min")
        r = self._ent(p, r, "Request Sleep Max (s):", "request_sleep_max")
        r = self._opt(p, r, "PO Token Mode:", "po_token_mode", ["off", "manual"])
        r = self._ent(p, r, "PO Token Value:", "po_token")
        r = self._sec(p, r, "Instagram Credentials (AES-256-GCM)")
        r = self._ent(p, r, "Instagram Username:", "instagram_user")
        self._ent(p, r, "Instagram Password:", "instagram_pass", show="*")

        # Tab 3: Network & Engines
        p, r = self.frames["Network & Engines"], 0
        r = self._sec(p, r, "Proxy, IPv4 & DNS-over-HTTPS (DoH)")
        r = self._opt(p, r, "Proxy Mode:", "proxy_mode", ["system", "custom", "none"])
        r = self._opt(p, r, "Custom Proxy Type:", "proxy_type", ["http", "https", "socks4", "socks5", "socks5h"])
        r = self._ent(p, r, "Custom Proxy Host:", "proxy_address")
        r = self._ent(p, r, "Custom Proxy Port:", "proxy_port")
        r = self._chk(p, r, "Force IPv4 Connections (0.0.0.0)", "force_ipv4")
        r = self._chk(p, r, "Enable Real DNS-over-HTTPS (DoH) Resolver", "doh_enabled")
        r = self._ent(p, r, "DoH Endpoint URL:", "doh_url")
        tb = ttk.Frame(p); tb.grid(row=r, column=1, sticky="ew", padx=(0, 12), pady=4); r += 1
        self.btn_test = ttk.Button(tb, text="Test Net / DoH", style="Teal.TButton", command=self._test_network); self.btn_test.pack(side="left")
        self.net_lbl = ttk.Label(tb, text="", style="Muted.TLabel"); self.net_lbl.pack(side="left", padx=10)
        r = self._sec(p, r, "Downloader Engines & FFmpeg")
        r = self._path_row(p, r, "FFmpeg Binary:", "ffmpeg_path", extra_btn=("Auto-Detect", self._detect_ffmpeg))
        fb = ttk.Frame(p); fb.grid(row=r, column=1, sticky="ew", padx=(0, 12), pady=4); r += 1
        ttk.Button(fb, text="Download / Update FFmpeg (one click)", style="Success.TButton", command=lambda: start_ffmpeg_install(self, self.sm, self._vars.get("ffmpeg_path"))).pack(side="left")
        ttk.Label(fb, text="~30 MB static build, progress + cancel, auto-configured", style="Muted.TLabel").pack(side="left", padx=10)
        r = self._ent(p, r, "Concurrent Fragments (1-32):", "concurrent_fragments")
        r = self._chk(p, r, "Use Aria2c Multi-Threaded Downloader", "use_aria2")
        r = self._path_row(p, r, "Aria2c Path:", "aria2_path")
        self._ent(p, r, "Search Results (5-30):", "search_results_count")

        # Tab 4: Processing & Automation
        p, r = self.frames["Processing & Automation"], 0
        r = self._sec(p, r, "Audio, Subtitles & Metadata")
        r = self._opt(p, r, "Default Audio Codec:", "audio_format", ["mp3", "m4a", "flac", "wav", "opus", "aac"])
        r = self._ent(p, r, "Default Subtitle Langs:", "default_subtitle_langs")
        for txt, key in (("Embed Soft Subtitles", "embed_subtitles"), ("Burn Hardsub (FFmpeg - slower)", "burn_subtitles"), ("Embed Cover Thumbnail", "embed_thumbnail"), ("Embed Metadata & Chapters", "embed_metadata")):
            r = self._chk(p, r, txt, key)
        r = self._sec(p, r, "SponsorBlock Default Segment Removal")
        sbf = ttk.Frame(p); sbf.grid(row=r, column=0, columnspan=2, sticky="ew", padx=12, pady=4); r += 1
        saved_sb = set(self.sm.get("sponsorblock_categories") or [])
        self.sb_vars: Dict[str, tk.BooleanVar] = {}
        for i, (ck, cl) in enumerate(SPONSORBLOCK_CATEGORIES.items()):
            v = tk.BooleanVar(master=self, value=(ck in saved_sb)); self.sb_vars[ck] = v
            ttk.Checkbutton(sbf, text=cl, variable=v).grid(row=i // 3, column=i % 3, sticky="w", padx=8, pady=3)
        r = self._sec(p, r, "Queue Automation & Integrity")
        for txt, key in (("Sync Playlists (Skip Duplicates via Archive)", "playlist_sync"), ("Organize Playlist Items in Subfolders", "playlist_subfolder"), ("Auto-Categorize Files (Video/Music/Images)", "auto_categorize"), ("Verify File Integrity Hash", "verify_hash")):
            r = self._chk(p, r, txt, key)
        r = self._opt(p, r, "Hash Algorithm:", "hash_algo", ["md5", "sha256"])
        r = self._chk(p, r, "Auto-Cleanup Old Temp Files (.part)", "auto_cleanup")
        r = self._chk(p, r, "Enable Stalled Download Watchdog", "watchdog_enabled")
        r = self._opt(p, r, "When Queue Completes:", "on_queue_complete", ["notify", "open_folder", "none", "sleep", "shutdown"])
        ub = ttk.Frame(p); ub.grid(row=r, column=0, columnspan=2, sticky="ew", padx=12, pady=(10, 6))
        self.btn_upd = ttk.Button(ub, text="Update yt-dlp & Core Libraries", style="Teal.TButton", command=self.update_libs); self.btn_upd.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ttk.Button(ub, text="System Diagnostics", command=lambda: DiagnosticsDialog(self, self.sm)).pack(side="right")

    def _detect_ffmpeg(self):
        f = detect_bundled_ffmpeg()
        if f: self._vars["ffmpeg_path"].set(f)
        else: messagebox.showwarning("FFmpeg", "Not found.", parent=self)

    def _extract_cookies(self):
        path = self._vars["cookies_file_path"].get().strip() or self.sm.get("cookies_file_path")
        browser = self._vars["cookie_browser"].get()

        def run():
            ok, msg = BrowserCookieExtractor.extract(browser, path)
            try:
                self.after(0, lambda: (messagebox.showinfo("Cookies", msg, parent=self) if ok else messagebox.showerror("Cookies", msg, parent=self)) if self.winfo_exists() else None)
            except (RuntimeError, tkinter.TclError):
                pass  # dialog/app already destroyed

        threading.Thread(target=run, daemon=True).start()

    def _gen_cookies(self):
        path = self._vars["cookies_file_path"].get().strip() or self.sm.get("cookies_file_path")
        # Never overwrite an existing user cookie file with anonymous warm-up
        # cookies - write a separate *_warmup file instead.
        if path and os.path.exists(path) and os.path.getsize(path) > 0:
            pp = Path(path); path = str(pp.with_name(pp.stem + "_warmup" + pp.suffix))
        path = path or str(AUTO_COOKIE_FILE)

        def run():
            ok, msg = CookieGenerator(path).generate()
            try:
                self.after(0, lambda: (messagebox.showinfo("Cookies", msg, parent=self) if ok else messagebox.showerror("Cookies", msg, parent=self)) if self.winfo_exists() else None)
            except (RuntimeError, tkinter.TclError):
                pass

        threading.Thread(target=run, daemon=True).start()

    def _test_network(self):
        self.btn_test.configure(state="disabled", text="Testing..."); self.net_lbl.configure(text="Testing...")
        px = None
        if self._vars["proxy_mode"].get() == "custom" and self._vars["proxy_address"].get().strip():
            h, pt, prt = self._vars["proxy_address"].get().strip(), self._vars["proxy_type"].get().strip() or "http", self._vars["proxy_port"].get().strip()
            px = f"{pt}://{h}:{prt}" if prt else f"{pt}://{h}"
        doh = self._vars["doh_url"].get().strip() or DOH_PROVIDERS["Cloudflare"]

        def run():
            ok_d, msg_d = DoHResolver.test_connection(doh, proxy_url=px)
            try:
                t0 = time.perf_counter(); r = requests.get("https://www.youtube.com/generate_204", timeout=6, proxies={"http": px, "https": px} if px else None)
                yt = f"YT HTTP {r.status_code} ({int((time.perf_counter() - t0) * 1000)}ms)"
            except Exception as e:
                yt = f"YT err: {e}"
            try:
                self.after(0, lambda: [self.btn_test.configure(state="normal", text="Test Net / DoH"),
                                       self.net_lbl.configure(text=f"{yt} | {msg_d}")] if self.winfo_exists() else None)
            except (RuntimeError, tkinter.TclError):
                pass

        threading.Thread(target=run, daemon=True).start()

    def update_libs(self):
        if getattr(sys, "frozen", False):
            messagebox.showinfo("Packaged App", "Update via release package.", parent=self); return
        self.btn_upd.configure(state="disabled", text="Updating...")

        def run():
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp", "instaloader", "Pillow", "requests", "humanize", "psutil", "pycryptodome", "mutagen"],
                               capture_output=True, text=True, timeout=900, check=True)
                res = (True, "Updated! Restart app.")
            except Exception as e:
                res = (False, f"Failed: {e}")
            try:
                self.after(0, lambda: [self.btn_upd.configure(state="normal", text="Update yt-dlp & Core Libraries"),
                                       messagebox.showinfo("Update", res[1], parent=self) if res[0] else messagebox.showerror("Error", res[1], parent=self)] if self.winfo_exists() else None)
            except (RuntimeError, tkinter.TclError):
                pass

        threading.Thread(target=run, daemon=True).start()

    def _save(self):
        try:
            for k, v in self._vars.items():
                val = v.get()
                if isinstance(val, str) and k not in {"instagram_pass"}: val = val.strip()
                orig = self._snapshot.get(k)
                if isinstance(orig, str) and k not in {"instagram_pass"}: orig = orig.strip()
                if val == orig: continue  # unchanged: don't overwrite concurrent edits
                self.sm.set(k, val)
            self.sm.set("sponsorblock_categories", [k for k, v in self.sb_vars.items() if v.get()])
            self.sm.normalize_and_save()
            parent = self.master
            self.destroy()  # close first: apply_cb may rebuild the main UI
            self.apply_cb()
            messagebox.showinfo("Saved", "Settings applied successfully.", parent=parent)
        except Exception as e:
            LoggerSetup.log(f"Settings save error: {e}", "error", exc_info=True)
            try:
                messagebox.showerror("Save Error", str(e), parent=self if self.winfo_exists() else None)
            except Exception:
                pass


class NewTaskDialog(tk.Toplevel):
    """Media Studio: format table, playlist/chapters/trim, subtitles, audio & SponsorBlock."""

    def __init__(self, parent: "SinaEnterpriseApp", info: Dict[str, Any], callback: Callable[..., None]):
        super().__init__(parent)
        self.settings, self.info, self.callback = parent.settings_manager, info or {}, callback
        self.selected_format_id = "bestvideo+bestaudio/best"
        ts = str(self.info.get("title") or self.info.get("id") or "Unknown Media")
        self.title(f"Media Studio: {ts[:55]}")
        self.geometry("1000x820"); self.minsize(840, 620)
        self.configure(bg=ThemeColors.BG); safe_grab_set(self); self.transient(parent); restore_parent_grab(self, parent)
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)

        hf = tk.Frame(self, bg=ThemeColors.CARD); hf.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6)); hf.grid_columnconfigure(1, weight=1)
        th = tk.Label(hf, text="No Preview", width=22, height=5, bg=ThemeColors.CANVAS, fg=ThemeColors.TEXT_MUTED)
        th.grid(row=0, column=0, rowspan=2, padx=12, pady=10)
        if self.info.get("thumbnail"): parent._load_img_async(self.info["thumbnail"], th, size=(160, 90))
        tk.Label(hf, text=ts, font=(UI_FONT, 15, "bold"), bg=ThemeColors.CARD, fg=ThemeColors.TEXT_PRIMARY, anchor="w", justify="left", wraplength=720).grid(row=0, column=1, sticky="sw", padx=(0, 12), pady=(10, 2))
        meta = [f"Channel: {self.info.get('uploader') or self.info.get('channel')}"] if (self.info.get("uploader") or self.info.get("channel")) else []
        if self.info.get("duration"): meta.append(f"Duration: {format_duration(self.info['duration'])}")
        if self.info.get("view_count"): meta.append(f"Views: {format_count(self.info['view_count'])}")
        if self.info.get("entries"): meta.append(f"Items: {len(self.info['entries'])}")
        tk.Label(hf, text="  |  ".join(meta) or "Media Ready", bg=ThemeColors.CARD, fg=ThemeColors.TEXT_MUTED, font=(UI_FONT, 11), anchor="w").grid(row=1, column=1, sticky="nw", padx=(0, 12), pady=(0, 10))

        self.nb = ttk.Notebook(self); self.nb.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        self.t_fmt = ttk.Frame(self.nb); self.t_chp = ttk.Frame(self.nb); self.t_sub = ttk.Frame(self.nb); self.t_aud = ttk.Frame(self.nb)
        self.nb.add(self.t_fmt, text="Format & Quality"); self.nb.add(self.t_chp, text="Playlist / Chapters / Trim")
        self.nb.add(self.t_sub, text="Subtitles"); self.nb.add(self.t_aud, text="Audio & SponsorBlock")
        self._build_fmt(); self._build_pl(); self._build_sub(); self._build_aud()

        af = tk.Frame(self, bg=ThemeColors.CARD); af.grid(row=2, column=0, sticky="ew", padx=12, pady=(6, 12))
        self.v_merge = tk.BooleanVar(master=self, value=True)
        self.v_thumb = tk.BooleanVar(master=self, value=bool(self.settings.get("embed_thumbnail")))
        self.v_meta = tk.BooleanVar(master=self, value=bool(self.settings.get("embed_metadata")))
        for txt, v in (("Merge Best Audio", self.v_merge), ("Embed Cover", self.v_thumb), ("Embed Metadata", self.v_meta)):
            ttk.Checkbutton(af, text=txt, variable=v, style="Card.TCheckbutton").pack(side="left", padx=10, pady=10)
        ttk.Button(af, text="Cancel", command=self.destroy).pack(side="right", padx=(4, 12), pady=10)
        ttk.Button(af, text="Add to Queue", style="Accent.TButton", command=self._finish).pack(side="right", padx=6, pady=10)

    def _build_fmt(self):
        fb = ttk.Frame(self.t_fmt); fb.pack(fill="x", padx=6, pady=(6, 4))
        self.flt_v = tk.StringVar(master=self, value="All")
        ttk.Label(fb, text="Filter:").pack(side="left", padx=(0, 6))
        flt = ttk.Combobox(fb, textvariable=self.flt_v, values=["All", "Video+Audio", "Video Only", "Audio Only"], state="readonly", width=14)
        flt.pack(side="left"); flt.bind("<<ComboboxSelected>>", lambda _e: self._populate_formats())
        ttk.Label(fb, text="Container:").pack(side="left", padx=(16, 6))
        self.cont_v = tk.StringVar(master=self, value="mp4")
        ttk.Combobox(fb, textvariable=self.cont_v, values=["mp4", "mkv", "webm"], state="readonly", width=8).pack(side="left")
        cols = ("fid", "kind", "res", "fps", "ext", "size", "tbr", "codecs")
        self.fmt_tree = ttk.Treeview(self.t_fmt, columns=cols, show="headings", selectmode="browse")
        for c, t, w, stretch in (("fid", "", 0, False), ("kind", "Type", 100, False), ("res", "Resolution", 170, True), ("fps", "FPS", 55, False), ("ext", "Ext", 60, False), ("size", "Est. Size", 100, False), ("tbr", "Bitrate", 75, False), ("codecs", "Codecs (Video / Audio)", 230, True)):
            self.fmt_tree.heading(c, text=t)
            self.fmt_tree.column(c, width=w, stretch=stretch, anchor="w")
        vsb = ttk.Scrollbar(self.t_fmt, orient="vertical", command=self.fmt_tree.yview)
        self.fmt_tree.configure(yscrollcommand=vsb.set)
        self.fmt_tree.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=4)
        vsb.pack(side="right", fill="y", padx=(0, 6), pady=4)
        self.fmt_tree.bind("<<TreeviewSelect>>", self._on_fmt_select)
        self.fmt_tree.bind("<Double-1>", lambda _e: self._finish())
        self._populate_formats()

    def _on_fmt_select(self, _e=None):
        sel = self.fmt_tree.selection()
        if sel:
            self.selected_format_id = str(self.fmt_tree.item(sel[0], "values")[0])

    def _populate_formats(self):
        self.fmt_tree.delete(*self.fmt_tree.get_children())
        flt = self.flt_v.get()
        is_pl = "entries" in self.info or self.info.get("_type") == "playlist"
        rows: List[Tuple[str, str, str, str, str, str, str, str]] = []
        if flt in {"All", "Video+Audio"}:
            rows.extend([
                ("bestvideo+bestaudio/best", "Preset", "★ Best Quality (Auto)", "Auto", "mp4/mkv", "Auto", "-", "Best Video / Best Audio"),
                ("bestvideo[height<=2160]+bestaudio/best[height<=2160]", "Preset", "★ 2160p 4K UHD", "60/30", "mp4/mkv", "Auto", "-", "Up to 2160p"),
                ("bestvideo[height<=1440]+bestaudio/best[height<=1440]", "Preset", "★ 1440p QHD", "60/30", "mp4/mkv", "Auto", "-", "Up to 1440p"),
                ("bestvideo[height<=1080]+bestaudio/best[height<=1080]", "Preset", "★ 1080p Full HD", "60/30", "mp4/mkv", "Auto", "-", "Up to 1080p"),
                ("bestvideo[height<=720]+bestaudio/best[height<=720]", "Preset", "★ 720p HD", "60/30", "mp4/mkv", "Auto", "-", "Up to 720p"),
                ("bestvideo[height<=480]+bestaudio/best[height<=480]", "Preset", "★ 480p SD", "30", "mp4/mkv", "Auto", "-", "Up to 480p"),
            ])
        if not is_pl:
            fmts = sorted(list(self.info.get("formats") or []), key=lambda x: ((x.get("height") or 0), (x.get("tbr") or 0), (x.get("abr") or 0)), reverse=True)
            seen = set()
            for f in fmts:
                fid = str(f.get("format_id") or "")
                if not fid or fid in seen: continue
                seen.add(fid); vc, ac = str(f.get("vcodec") or "none"), str(f.get("acodec") or "none")
                kind = "Video+Audio" if (vc != "none" and ac != "none") else ("Video Only" if vc != "none" else ("Audio Only" if ac != "none" else "Other"))
                if flt != "All" and kind != flt: continue
                sz, h, w, tbr = f.get("filesize") or f.get("filesize_approx") or 0, f.get("height"), f.get("width"), f.get("tbr") or f.get("abr")
                res = f"{w}x{h}" if (h and w) else (f"{h}p" if h else "Audio Stream")
                rows.append((fid, kind, res, str(f.get("fps") or "-"), str(f.get("ext") or "-"), format_bytes(sz, True) if sz else "N/A", f"{int(tbr)}k" if tbr else "-", f"{vc[:14]} / {ac[:14]}"))
        for i, row in enumerate(rows):
            self.fmt_tree.insert("", "end", iid=f"fmt{i}", values=row)
        kids = self.fmt_tree.get_children()
        if kids:
            self.fmt_tree.selection_set(kids[0]); self.fmt_tree.focus(kids[0])
            self.selected_format_id = str(self.fmt_tree.item(kids[0], "values")[0])

    def _build_pl(self):
        self.chp_vars: List[Tuple[tk.BooleanVar, Dict[str, Any]]] = []
        self.pl_vars: List[Tuple[tk.BooleanVar, int, str, ttk.Checkbutton]] = []
        self.split_chp_v = tk.BooleanVar(master=self, value=False)
        self.pl_sub_v = tk.BooleanVar(master=self, value=bool(self.settings.get("playlist_subfolder")))
        tb = ttk.Frame(self.t_chp, style="Alt.TFrame"); tb.pack(fill="x", padx=8, pady=(8, 4))
        self.trim_v = tk.BooleanVar(master=self, value=False)
        ttk.Checkbutton(tb, text="Clip / Trim Custom Time Range", variable=self.trim_v, style="Alt.TCheckbutton").pack(side="left", padx=10, pady=8)
        ttk.Label(tb, text="Start:", style="Alt.TCheckbutton").pack(side="left", padx=(8, 4))
        self.t_start_e = ttk.Entry(tb, width=11); self.t_start_e.pack(side="left", padx=4); self.t_start_e.insert(0, "00:00:00")
        ttk.Label(tb, text="End:", style="Alt.TCheckbutton").pack(side="left", padx=(8, 4))
        self.t_end_e = ttk.Entry(tb, width=11); self.t_end_e.pack(side="left", padx=4); self.t_end_e.insert(0, "00:02:30")
        self.chp_scroll = ScrollFrame(self.t_chp)
        self.chp_scroll.pack(fill="both", expand=True, padx=8, pady=(4, 8))
        chapters, entries = self.info.get("chapters") or [], self.info.get("entries") or []
        if chapters:
            cc = ttk.Frame(self.chp_scroll.inner); cc.pack(fill="x", pady=4)
            ttk.Checkbutton(cc, text="Split into Selected Chapters", variable=self.split_chp_v).pack(side="left")
            ttk.Button(cc, text="None", width=6, command=lambda: [v.set(False) for v, _ in self.chp_vars]).pack(side="right", padx=2)
            ttk.Button(cc, text="All", width=6, style="Accent.TButton", command=lambda: [v.set(True) for v, _ in self.chp_vars]).pack(side="right", padx=2)
            for ch in chapters:
                v = tk.BooleanVar(master=self, value=False)
                ttk.Checkbutton(self.chp_scroll.inner, text=f"{ch.get('title', 'Chapter')} ({format_duration(ch.get('start_time', 0))} - {format_duration(ch.get('end_time', 0))})", variable=v).pack(anchor="w", pady=2, padx=6)
                self.chp_vars.append((v, ch))
        if entries:
            pc = ttk.Frame(self.chp_scroll.inner); pc.pack(fill="x", pady=(8, 4))
            ttk.Checkbutton(pc, text="Save into Playlist Subfolder", variable=self.pl_sub_v).pack(side="left")
            ttk.Button(pc, text="Invert", width=7, command=lambda: [v.set(not v.get()) for v, _, _, _ in self.pl_vars]).pack(side="right", padx=2)
            ttk.Button(pc, text="None", width=6, command=lambda: [v.set(False) for v, _, _, _ in self.pl_vars]).pack(side="right", padx=2)
            ttk.Button(pc, text="All", width=6, style="Accent.TButton", command=lambda: [v.set(True) for v, _, _, _ in self.pl_vars]).pack(side="right", padx=2)
            rb = ttk.Frame(self.chp_scroll.inner); rb.pack(fill="x", pady=4)
            self.pl_rng_e = ttk.Entry(rb, width=20); self.pl_rng_e.pack(side="left", padx=(0, 6))
            ToolTip(self.pl_rng_e, "Range e.g. 1-5, 8")
            ttk.Button(rb, text="Apply", width=7, style="Teal.TButton", command=lambda: self._apply_pl_rng(len(entries))).pack(side="left", padx=(0, 10))
            self.pl_flt_e = ttk.Entry(rb); self.pl_flt_e.pack(side="left", fill="x", expand=True)
            ToolTip(self.pl_flt_e, "Filter titles...")
            self.pl_flt_e.bind("<KeyRelease>", lambda _e: [chk.pack(anchor="w", pady=2, padx=6) if (not self.pl_flt_e.get().strip().lower() or self.pl_flt_e.get().strip().lower() in tl) else chk.pack_forget() for _v, _ix, tl, chk in self.pl_vars])
            for idx, ent in enumerate(entries):
                if not ent: continue
                v, et = tk.BooleanVar(master=self, value=True), str(ent.get("title") or f"Video {idx + 1}")
                chk = ttk.Checkbutton(self.chp_scroll.inner, text=f"{idx + 1}. {et}" + (f" [{format_duration(ent.get('duration'))}]" if ent.get("duration") else ""), variable=v)
                chk.pack(anchor="w", pady=2, padx=6); self.pl_vars.append((v, idx + 1, et.lower(), chk))
        if not chapters and not entries:
            ttk.Label(self.chp_scroll.inner, text="No playlist items or chapters found. Use Custom Time Range above if needed.", style="Muted.TLabel").pack(pady=24)

    def _apply_pl_rng(self, total: int):
        try:
            chosen = set(parse_index_selection(self.pl_rng_e.get(), total))
            for v, ix, _, _ in self.pl_vars: v.set(ix in chosen)
        except Exception as ex:
            messagebox.showerror("Invalid Range", str(ex), parent=self)

    def _build_sub(self):
        ctrl = ttk.Frame(self.t_sub); ctrl.pack(fill="x", padx=8, pady=(8, 4))
        def_m = "Burn Hardsub" if self.settings.get("burn_subtitles") else ("Embed Softsub" if self.settings.get("embed_subtitles") else "External File")
        self.sub_m_v = tk.StringVar(master=self, value=def_m)
        ttk.Label(ctrl, text="Mode:").pack(side="left", padx=(0, 6))
        ttk.Combobox(ctrl, textvariable=self.sub_m_v, values=["External File", "Embed Softsub", "Burn Hardsub"], state="readonly", width=16).pack(side="left")
        self.sub_vars: Dict[str, Tuple[tk.BooleanVar, bool]] = {}
        ttk.Button(ctrl, text="Clear", width=6, command=lambda: [v.set(False) for v, _ in self.sub_vars.values()]).pack(side="right", padx=2)
        ttk.Button(ctrl, text="All", width=6, style="Accent.TButton", command=lambda: [v.set(True) for v, _ in self.sub_vars.values()]).pack(side="right", padx=2)
        self.sub_scroll = ScrollFrame(self.t_sub)
        self.sub_scroll.pack(fill="both", expand=True, padx=8, pady=6)
        man, auto = self.info.get("subtitles") or {}, self.info.get("automatic_captions") or {}
        comb = {k: True for k in auto if k != "live_chat"}
        for k in man:
            if k != "live_chat": comb[k] = False
        defs = {x.strip().lower() for x in str(self.settings.get("default_subtitle_langs") or "en,fa").split(",") if x.strip()}
        if comb:
            for l in sorted(comb, key=lambda k: (comb[k], k)):
                ia = comb[l]; v = tk.BooleanVar(master=self, value=(l.lower() in defs and (not ia or l not in man)))
                ttk.Checkbutton(self.sub_scroll.inner, text=f"{SUBTITLE_LANGUAGES.get(l, l)} ({l}) {'[Auto]' if ia else '[Manual]'}", variable=v).pack(anchor="w", pady=2, padx=6)
                self.sub_vars[l] = (v, ia)
        else:
            ttk.Label(self.sub_scroll.inner, text="No subtitles available.", style="Muted.TLabel").pack(pady=24)

    def _build_aud(self):
        sc = ScrollFrame(self.t_aud); sc.pack(fill="both", expand=True, padx=8, pady=8)
        p = sc.inner
        ttk.Label(p, text="Audio Extraction & Conversion", style="H2.TLabel").pack(anchor="w", padx=12, pady=(8, 6))
        self.aud_only_v = tk.BooleanVar(master=self, value=str(self.settings.get("default_download_type") or "Video").lower() == "audio")
        ttk.Checkbutton(p, text="Enable Audio-Only Extraction Mode", variable=self.aud_only_v).pack(anchor="w", padx=12, pady=6)
        ra = ttk.Frame(p); ra.pack(fill="x", padx=12, pady=6)
        self.afmt_v = tk.StringVar(master=self, value=str(self.settings.get("audio_format") or "mp3")); self.aq_v = tk.StringVar(master=self, value="320")
        ttk.Label(ra, text="Format:").pack(side="left", padx=(0, 6))
        ttk.Combobox(ra, textvariable=self.afmt_v, values=["mp3", "m4a", "flac", "wav", "opus", "aac"], state="readonly", width=8).pack(side="left", padx=(0, 18))
        ttk.Label(ra, text="Bitrate:").pack(side="left", padx=(0, 6))
        ttk.Combobox(ra, textvariable=self.aq_v, values=["128", "192", "256", "320", "0"], state="readonly", width=6).pack(side="left")
        ttk.Label(p, text="SponsorBlock Segment Removal (YouTube)", style="H2.TLabel").pack(anchor="w", padx=12, pady=(18, 6))
        saved_sb = set(self.settings.get("sponsorblock_categories") or []); self.sb_vars: Dict[str, tk.BooleanVar] = {}
        sg = ttk.Frame(p); sg.pack(fill="x", padx=12, pady=4)
        for i, (ck, cl) in enumerate(SPONSORBLOCK_CATEGORIES.items()):
            v = tk.BooleanVar(master=self, value=(ck in saved_sb)); self.sb_vars[ck] = v
            ttk.Checkbutton(sg, text=cl, variable=v).grid(row=i // 2, column=i % 2, sticky="w", padx=10, pady=4)

    def _finish(self):
        if self.pl_vars and not any(v.get() for v, _ix, _tl, _chk in self.pl_vars):
            messagebox.showwarning("No Items Selected", "All playlist items are unchecked.\nSelect at least one item (or press 'All'), then add to queue.", parent=self)
            return
        aud_only = self.aud_only_v.get()
        fid = self.selected_format_id or ("bestaudio/best" if aud_only else "bestvideo+bestaudio/best")
        cr = None
        if self.trim_v.get():
            try:
                s_sec, e_sec = parse_timestamp_to_seconds(self.t_start_e.get()) or 0.0, parse_timestamp_to_seconds(self.t_end_e.get())
                if e_sec is not None and e_sec <= s_sec: raise ValueError("End time must exceed Start time.")
                cr = (s_sec, e_sec)
            except Exception as ex:
                messagebox.showerror("Invalid Trim Range", str(ex), parent=self); return
        self.callback(self.info, {
            "format_id": fid, "container": self.cont_v.get(), "subs": [k for k, (v, _) in self.sub_vars.items() if v.get()],
            "has_auto_subs": any(v.get() and ia for v, ia in self.sub_vars.values()), "sub_mode": self.sub_m_v.get(),
            "chapters": [ch for v, ch in self.chp_vars if v.get()] if self.split_chp_v.get() else [], "custom_range": cr,
            "merge": self.v_merge.get(), "embed_thumbnail": self.v_thumb.get(), "embed_metadata": self.v_meta.get(),
            "playlist_indices": [ix for v, ix, _, _ in self.pl_vars if v.get()], "playlist_subfolder": self.pl_sub_v.get(),
            "audio_opts": {"format": self.afmt_v.get(), "quality": self.aq_v.get()} if aud_only else None,
            "sponsorblock_cats": [k for k, v in self.sb_vars.items() if v.get()],
        })
        self.destroy()


class TaskInspectorDialog(tk.Toplevel):
    def __init__(self, parent: "SinaEnterpriseApp", task: DownloadTask):
        super().__init__(parent)
        self.title(f"Task Inspector: {(task.title or '')[:45]}")
        self.geometry("780x620"); self.configure(bg=ThemeColors.BG); safe_grab_set(self); self.transient(parent); restore_parent_grab(self, parent)
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        head = tk.Frame(self, bg=ThemeColors.CARD); head.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        tk.Label(head, text=task.title or "Untitled", font=(UI_FONT, 15, "bold"), bg=ThemeColors.CARD, fg=ThemeColors.TEXT_PRIMARY, wraplength=700, anchor="w", justify="left").pack(anchor="w", padx=12, pady=(10, 2))
        tk.Label(head, text=f"ID: {task.task_id}  |  Platform: {detect_platform_label(task.url)}  |  Profile: {task.quality_profile}", bg=ThemeColors.CARD, fg=ThemeColors.TEXT_MUTED, font=(UI_FONT, 10)).pack(anchor="w", padx=12, pady=(0, 10))

        body = ScrollFrame(self); body.grid(row=1, column=0, sticky="nsew", padx=12, pady=6)
        body.inner.grid_columnconfigure(1, weight=1)
        rows = [
            ("Status / Stage", f"{task.status.value} ({task.stage_label or '-'})"), ("Source URL", task.url),
            ("Progress", f"{task.progress_str} ({format_bytes(task.downloaded_bytes)} / {task.total_bytes_str})"),
            ("Peak Speed", f"{format_bytes(task.peak_speed, False)}/s" if task.peak_speed else "N/A"),
            ("Category", task.category), ("Output File", task.filepath or "Not created yet"),
            (f"Hash ({task.hash_algo.upper()})", task.file_hash or "Not computed"),
            ("Error Category", task.error_category or "None"), ("Remediation Hint", task.error_remediation or "None"),
        ]
        for idx, (k, v) in enumerate(rows):
            ttk.Label(body.inner, text=f"{k}", font=(UI_FONT, 11, "bold"), anchor="nw").grid(row=idx, column=0, sticky="nw", padx=10, pady=4)
            ent = ttk.Entry(body.inner); ent.insert(0, str(v)); ent.configure(state="readonly"); ent.grid(row=idx, column=1, sticky="ew", padx=10, pady=4)
        if task.error_message:
            ttk.Label(body.inner, text="Error Trace:", font=(UI_FONT, 11, "bold"), foreground=ColorPalette.TEXT_ERROR.value).grid(row=len(rows), column=0, sticky="nw", padx=10, pady=(8, 2))
            eb = tk.Text(body.inner, height=7, bg=ThemeColors.CANVAS, fg=ColorPalette.TEXT_ERROR.value, font=("Consolas", 10), relief="flat", wrap="word")
            eb.insert("1.0", task.error_message); eb.configure(state="disabled"); eb.grid(row=len(rows) + 1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)

        bb = ttk.Frame(self); bb.grid(row=2, column=0, sticky="ew", padx=12, pady=12)
        if task.status in {DownloadStatus.ERROR, DownloadStatus.INVALID, DownloadStatus.CANCELLED}:
            rec = ErrorClassifier.recommended_action(ErrorClassifier.classify(task.error_message))
            if rec:
                ak, al = rec
                ov_map = {"browser_cookies": {"_override_cookie_source": "browser"}, "file_cookies": {"_override_cookie_source": "file"}, "direct_no_proxy": {"_override_proxy_mode": "none"}, "clean_resume": {"_clean_resume": True}, "best_fallback": {"format": "bestvideo+bestaudio/best"}}
                ttk.Button(bb, text=al, style="Warning.TButton", command=lambda k=ak: [parent.dl_manager.retry_task(task.task_id, ov_map[k]), self.destroy()]).pack(side="left", padx=4)
            ttk.Button(bb, text="Retry Now", style="Accent.TButton", command=lambda: [parent.dl_manager.retry_task(task.task_id), self.destroy()]).pack(side="left", padx=4)
            if ErrorClassifier.classify(task.error_message) in {ErrorCategory.NEEDS_COOKIES, ErrorCategory.COOKIE_DB_LOCKED}:
                ttk.Button(bb, text="Fix Cookies", style="Teal.TButton", command=lambda: CookieHelperDialog(self, parent.settings_manager, parent)).pack(side="left", padx=4)
        if task.filepath and os.path.exists(task.filepath):
            ttk.Button(bb, text="Open Folder", style="Accent.TButton", command=lambda: open_file_location(task.filepath)).pack(side="left", padx=4)

        def copy_details():
            self.clipboard_clear()
            self.clipboard_append(f"Title: {task.title}\nURL: {task.url}\nError: {task.error_message}\nFile: {task.filepath}\nHash: {task.file_hash}")
            messagebox.showinfo("Copied", "Copied.", parent=self)

        ttk.Button(bb, text="Copy Details", command=copy_details).pack(side="left", padx=4)
        ttk.Button(bb, text="Close", command=self.destroy).pack(side="right", padx=4)


class DiagnosticsDialog(tk.Toplevel):
    def __init__(self, parent, sm: SettingsManager):
        super().__init__(parent)
        self.title("System Environment Diagnostics")
        self.geometry("780x540"); self.configure(bg=ThemeColors.BG); safe_grab_set(self); self.transient(parent); restore_parent_grab(self, parent)
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        ttk.Label(self, text="SINA Fusion Environment & Dependency Health", style="Title.TLabel", foreground=ColorPalette.ACCENT_COLOR.value).grid(row=0, column=0, pady=(14, 6), padx=14, sticky="w")
        box = ScrollFrame(self); box.grid(row=1, column=0, sticky="nsew", padx=14, pady=6)
        box.inner.grid_columnconfigure(1, weight=1)
        rep = EnvironmentDiagnostics.collect(sm)
        for i, (k, v) in enumerate(rep.items()):
            ttk.Label(box.inner, text=f"{k}:", font=(UI_FONT, 11, "bold"), anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(box.inner, text=v, anchor="w", wraplength=520, justify="left").grid(row=i, column=1, sticky="w", padx=10, pady=5)
        rt = "\n".join(f"{k}: {v}" for k, v in rep.items())
        btns = ttk.Frame(self); btns.grid(row=2, column=0, sticky="ew", padx=14, pady=12)

        def copy_report():
            self.clipboard_clear(); self.clipboard_append(rt)
            messagebox.showinfo("Copied", "Copied.", parent=self)

        ttk.Button(btns, text="Copy Report", style="Accent.TButton", command=copy_report).pack(side="left", padx=4)
        ttk.Button(btns, text="Download FFmpeg", style="Success.TButton", command=lambda: start_ffmpeg_install(self, sm)).pack(side="left", padx=4)
        ttk.Button(btns, text="Cookie Helper", style="Teal.TButton", command=lambda: CookieHelperDialog(self, sm, parent if isinstance(parent, SinaEnterpriseApp) else None)).pack(side="left", padx=4)
        ttk.Button(btns, text="Close", command=self.destroy).pack(side="right", padx=4)


class SchedulerDialog(tk.Toplevel):
    def __init__(self, parent: "SinaEnterpriseApp"):
        super().__init__(parent)
        self.title("Queue Scheduler & Power Automation")
        self.geometry("460x340"); self.configure(bg=ThemeColors.BG); safe_grab_set(self); self.transient(parent); restore_parent_grab(self, parent); self.resizable(False, False)
        ttk.Label(self, text="Download Queue Scheduler", style="H2.TLabel", foreground=ColorPalette.ACCENT_COLOR.value).pack(pady=(16, 8))
        ttk.Label(self, text="Delay queue start (minutes, 0 = start now):").pack(pady=(6, 4))
        de = ttk.Entry(self, width=18, justify="center"); de.insert(0, "0"); de.pack(pady=4)
        qr = ttk.Frame(self); qr.pack(pady=6)
        for lbl, m in (("Now", 0), ("15m", 15), ("30m", 30), ("1h", 60), ("2h", 120)):
            ttk.Button(qr, text=lbl, width=6, command=lambda v=m: [de.delete(0, "end"), de.insert(0, str(v))]).pack(side="left", padx=3)
        ttk.Label(self, text="When Queue Completes:").pack(pady=(12, 4))
        odv = tk.StringVar(master=self, value=str(parent.settings_manager.get("on_queue_complete")))
        ttk.Combobox(self, textvariable=odv, values=["notify", "open_folder", "none", "sleep", "shutdown"], state="readonly", width=22).pack(pady=4)
        br = ttk.Frame(self); br.pack(pady=16)

        def apply_s():
            parent.settings_manager.set("on_queue_complete", odv.get()); parent.settings_manager.save()
            parent.dl_manager.set_schedule_delay(safe_float(de.get(), 0.0, 0.0, 1440.0)); parent.update_status_bar(); self.destroy()

        ttk.Button(br, text="Apply", style="Accent.TButton", command=apply_s).pack(side="left", padx=6)
        ttk.Button(br, text="Cancel", command=self.destroy).pack(side="left", padx=6)


# --- Main Application ---

class ProgressDialog(tk.Toplevel):
    """Modal progress window with live status, determinate/indeterminate bar and cancel."""

    def __init__(self, parent, title: str):
        super().__init__(parent)
        self.title(title); self.geometry("540x170")
        self.configure(bg=ThemeColors.BG); self.transient(parent); safe_grab_set(self); restore_parent_grab(self, parent); self.resizable(False, False)
        self.cancelled = threading.Event()
        self.lbl = ttk.Label(self, text="Starting...", wraplength=500, justify="left")
        self.lbl.pack(padx=16, pady=(16, 8), fill="x")
        self.pb = ttk.Progressbar(self, mode="determinate", maximum=1.0)
        self.pb.pack(padx=16, fill="x")
        self.btn = ttk.Button(self, text="Cancel", style="Danger.TButton", command=self._cancel)
        self.btn.pack(pady=12)
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _cancel(self):
        self.cancelled.set()
        try:
            self.lbl.configure(text="Cancelling..."); self.btn.configure(state="disabled")
        except Exception:
            pass

    def set_progress(self, frac: float, text: str):
        if not self.winfo_exists(): return
        try:
            self.lbl.configure(text=text)
            if frac < 0:
                if str(self.pb["mode"]) != "indeterminate":
                    self.pb.configure(mode="indeterminate"); self.pb.start(12)
            else:
                if str(self.pb["mode"]) != "determinate":
                    self.pb.stop(); self.pb.configure(mode="determinate")
                self.pb.configure(value=max(0.0, min(1.0, frac)))
        except Exception:
            pass

    def close(self):
        try: self.pb.stop()
        except Exception: pass
        try: self.destroy()
        except Exception: pass


def start_ffmpeg_install(parent, sm: SettingsManager, entry_var=None):
    """One-click FFmpeg download/update worker shared by Settings and Diagnostics."""
    dlg = ProgressDialog(parent, "FFmpeg Auto-Installer")

    def report(f, t):
        try:
            parent.after(0, lambda: dlg.set_progress(f, t) if dlg.winfo_exists() else None)
        except Exception:
            pass

    def run():
        ok, msg, path = FFmpegInstaller.install(report, dlg.cancelled)
        LoggerSetup.log(msg, "info" if ok else "warning")

        def done():
            if dlg.winfo_exists(): dlg.close()
            if ok and path:
                sm.set("ffmpeg_path", path); sm.save()
                if entry_var is not None:
                    try: entry_var.set(path)
                    except Exception: pass
                messagebox.showinfo("FFmpeg", msg, parent=parent if parent.winfo_exists() else None)
            elif not dlg.cancelled.is_set():
                messagebox.showerror("FFmpeg", msg, parent=parent if parent.winfo_exists() else None)

        try:
            parent.after(0, done)
        except Exception:
            pass

    threading.Thread(target=run, name="FFmpegInstall", daemon=True).start()


class CookieHelperDialog(tk.Toplevel):
    """Central place to obtain working cookies: extract, auto-fix, import, Playwright."""

    def __init__(self, parent, sm: SettingsManager, app: Optional["SinaEnterpriseApp"] = None):
        super().__init__(parent)
        self.sm, self.app = sm, app
        self.title("Cookie Helper"); self.geometry("640x640")
        self.configure(bg=ThemeColors.BG); self.transient(parent); safe_grab_set(self); restore_parent_grab(self, parent)
        ttk.Label(self, text="Cookie Helper", style="Title.TLabel", foreground=ColorPalette.ACCENT_COLOR.value).pack(anchor="w", padx=16, pady=(14, 4))
        ttk.Label(self, text="Get working cookies for age-restricted / bot-checked / members-only media.", style="Muted.TLabel").pack(anchor="w", padx=16)

        sf = tk.Frame(self, bg=ThemeColors.CARD); sf.pack(fill="x", padx=16, pady=10)
        self.status_lbl = tk.Label(sf, text="", bg=ThemeColors.CARD, fg=ThemeColors.TEXT_PRIMARY, font=(UI_FONT, 10), justify="left", anchor="w")
        self.status_lbl.pack(fill="x", padx=12, pady=10)

        bf = ttk.Frame(self); bf.pack(fill="x", padx=16)
        ttk.Button(bf, text="★ Install SINA Cookie Extension (automatic - recommended)", style="Accent.TButton", command=self._install_bridge).pack(fill="x", pady=3)
        ttk.Button(bf, text="1) Extract Now (browser closed)", style="Teal.TButton", command=self._extract).pack(fill="x", pady=3)
        ttk.Button(bf, text="2) Extract from OPEN browser (CDP - like an extension)", style="Accent.TButton", command=self._autofix_cdp).pack(fill="x", pady=3)
        ttk.Button(bf, text="3) Auto-Fix: Close Browser > Extract DB > Reopen", command=self._autofix).pack(fill="x", pady=3)
        ttk.Button(bf, text="4) Import cookies.txt (from browser extension)...", command=self._import).pack(fill="x", pady=3)
        ttk.Button(bf, text="5) Install Playwright Engine (anonymous warm-up)", command=self._install_playwright).pack(fill="x", pady=3)
        if app is not None:
            ttk.Button(bf, text="6) Retry tasks failed on cookies", style="Warning.TButton", command=self._retry_failed).pack(fill="x", pady=3)

        ttk.Label(self, text="Result:", style="Muted.TLabel").pack(anchor="w", padx=16, pady=(10, 2))
        self.result_txt = tk.Text(self, height=8, bg=ThemeColors.CANVAS, fg=ThemeColors.TEXT_PRIMARY, font=("Consolas", 10), relief="flat", wrap="word", state="disabled")
        self.result_txt.pack(fill="both", expand=True, padx=16, pady=(0, 8))
        ttk.Button(self, text="Close", command=self.destroy).pack(pady=(0, 12))
        self._refresh_status()

    def _refresh_status(self):
        browser = BrowserCookieExtractor.resolve_browser(str(self.sm.get("cookie_browser") or "auto"))
        src = str(self.sm.get("cookie_source") or "auto")
        cf = str(self.sm.get("cookies_file_path") or "")
        cf_ok = bool(cf and os.path.exists(cf) and os.path.getsize(cf) > 0)
        auto_ok = os.path.exists(AUTO_COOKIE_FILE) and os.path.getsize(AUTO_COOKIE_FILE) > 0
        bridge_line = "Cookie Bridge extension: n/a"
        if self.app is not None and hasattr(self.app, "cookie_bridge"):
            st = self.app.cookie_bridge.status()
            if st["received"] > 0:
                bridge_line = f"Cookie Bridge extension: CONNECTED ({st['last_count']} cookies auto-received)"
            elif st["running"]:
                bridge_line = "Cookie Bridge extension: waiting - install it with the ★ button below"
            else:
                bridge_line = "Cookie Bridge extension: server not running"

        def render(running: bool):
            try:
                if not self.winfo_exists(): return
                self.status_lbl.configure(text=(
                    f"Cookie source: {src}   |   Browser: {browser} ({'RUNNING - DB locked' if running else 'not running'})\n"
                    f"Your cookies file: {'OK' if cf_ok else 'missing/empty'} ({cf})\n"
                    f"Auto-extracted file: {'OK' if auto_ok else 'not created yet'}\n"
                    f"{bridge_line}"))
            except Exception:
                pass

        # tasklist can block up to 15 s on a loaded system - never run it on the
        # GUI thread (it would freeze the whole window). Probe in the background.
        pname = BrowserCookieFixer.PROC.get(browser.lower(), "")
        if sys.platform == "win32" and pname:
            render(False)  # immediate paint; refined when the probe returns

            def probe():
                running = BrowserCookieFixer._running(pname)
                try: self.after(0, lambda: render(running))
                except Exception: pass

            threading.Thread(target=probe, daemon=True).start()
        else:
            render(False)

    def _log_result(self, text: str):
        try:
            self.result_txt.configure(state="normal")
            self.result_txt.delete("1.0", "end")
            self.result_txt.insert("1.0", text)
            self.result_txt.configure(state="disabled")
        except Exception:
            pass

    def _run_bg(self, fn):
        def wrap():
            try:
                ok, msg = fn()
            except Exception as e:
                ok, msg = False, str(e)
            def show():
                if not self.winfo_exists(): return
                self._log_result(("SUCCESS: " if ok else "FAILED: ") + msg)
                self._refresh_status()
            try: self.after(0, show)
            except Exception: pass
        threading.Thread(target=wrap, daemon=True).start()

    def _install_bridge(self):
        """Materialize the custom extension, open the browser's extensions page
        and the extension folder, and guide the one-time 'Load unpacked' step."""
        try:
            d = materialize_cookie_bridge_extension()
        except Exception as e:
            messagebox.showerror("Cookie Bridge", f"Could not write the extension folder:\n{e}", parent=self)
            return
        browser = BrowserCookieExtractor.resolve_browser(str(self.sm.get("cookie_browser") or "auto"))
        page = {"brave": "brave://extensions", "chrome": "chrome://extensions", "edge": "edge://extensions",
                "vivaldi": "vivaldi://extensions", "opera": "opera://extensions"}.get(browser, "chrome://extensions")
        exe = BrowserCookieFixer._exe_path(BrowserCookieFixer.PROC.get(browser, ""))
        try:
            if exe:
                subprocess.Popen([exe, page], close_fds=True)
            else:
                webbrowser.open(page)
        except Exception as e:
            LoggerSetup.log(f"Could not open extensions page automatically: {e}", "debug")
        try:
            open_file_location(str(d))
        except Exception:
            pass
        messagebox.showinfo(
            "Install SINA Cookie Bridge",
            "The extension folder is open in Explorer and the extensions page in your browser.\n\n"
            "1) In the extensions page, enable 'Developer mode' (top-right).\n"
            "2) Click 'Load unpacked' and select this folder:\n"
            f"    {d}\n"
            "3) Done! While the browser is open, cookies now flow to this app AUTOMATICALLY\n"
            "    (no restart, no CDP). The extension badge shows the cookie count.\n\n"
            "Keep this app running so it can receive the cookies.",
            parent=self)
        self._log_result(f"Extension ready at:\n{d}\nLoad it unpacked into {browser}, then cookies auto-push to the app.")
        self._refresh_status()

    def _extract(self):
        browser = str(self.sm.get("cookie_browser") or "chrome")
        dest = str(self.sm.get("cookies_file_path") or AUTO_COOKIE_FILE)
        self._log_result("Extracting...")
        self._run_bg(lambda: BrowserCookieExtractor.extract(browser, dest))

    def _autofix(self):
        browser = BrowserCookieExtractor.resolve_browser(str(self.sm.get("cookie_browser") or "auto"))
        if not messagebox.askyesno("Auto-Fix Cookies", f"{browser} will be closed NORMALLY (your session/tabs are saved),\ncookies will be extracted, then {browser} reopens with your previous session.\n\nContinue?", parent=self):
            return
        dest = str(self.sm.get("cookies_file_path") or AUTO_COOKIE_FILE)
        self._log_result("Auto-fix running...")
        self._run_bg(lambda: BrowserCookieFixer.auto_fix(browser, dest, progress=lambda t: self.after(0, lambda: self._log_result(t) if self.winfo_exists() else None)))

    def _autofix_cdp(self):
        browser = BrowserCookieExtractor.resolve_browser(str(self.sm.get("cookie_browser") or "auto"))
        if not messagebox.askyesno(
                "Extract from open browser (CDP)",
                f"This works like a cookie extension and reads DECRYPTED cookies even while {browser} is open.\n\n"
                f"{browser} will be closed normally (tabs saved), reopened with a LOCAL cookie-access port,\n"
                f"cookies harvested, and {browser} LEFT OPEN with your session restored.\n\nContinue?", parent=self):
            return
        dest = str(self.sm.get("cookies_file_path") or AUTO_COOKIE_FILE)
        self._log_result("CDP cookie harvest running...")

        def run():
            ok, msg = BrowserCookieFixer.auto_fix_cdp(browser, dest, progress=lambda t: self.after(0, lambda: self._log_result(t) if self.winfo_exists() else None))
            if ok:
                # Persist the REAL cookies to the auto engine's file too, so the
                # download auto-retry picks them up immediately (the open CDP port
                # is also remembered for future non-disruptive re-harvests).
                try:
                    if os.path.abspath(dest) != os.path.abspath(AUTO_COOKIE_FILE):
                        shutil.copyfile(dest, AUTO_COOKIE_FILE)
                    LoggerSetup.log(f"Real CDP cookies persisted to auto file: {AUTO_COOKIE_FILE}", "debug")
                except Exception as e:
                    LoggerSetup.log(f"Could not persist CDP cookies to auto file: {e}", "warning")
            return ok, msg

        self._run_bg(run)

    def _import(self):
        src = filedialog.askopenfilename(parent=self, title="Import cookies.txt", filetypes=[("Cookie files", "*.txt"), ("All files", "*.*")])
        if not src: return
        dest = str(self.sm.get("cookies_file_path") or AUTO_COOKIE_FILE)
        try:
            Path(dest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
            n = sum(1 for l in Path(dest).read_text(encoding="utf-8", errors="replace").splitlines() if l and not l.startswith("#"))
            self._log_result(f"SUCCESS: Imported {n} cookie line(s) to {dest}")
        except Exception as e:
            self._log_result(f"FAILED: {e}")
        self._refresh_status()

    def _install_playwright(self):
        self._log_result("Installing Playwright + Chromium... this can take several minutes on a slow connection.")

        def stream(cmd: List[str], timeout: int, label: str, env: Optional[Dict[str, str]] = None) -> Tuple[bool, str]:
            LoggerSetup.log(f"[PW-INSTALL] {label}: {' '.join(cmd)}", "debug")
            run_env = {**os.environ, **(env or {})}
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace", env=run_env)
            except Exception as e:
                return False, f"{label}: could not start ({e})"
            tail: collections.deque = collections.deque(maxlen=40)
            start = time.time()
            try:
                for line in proc.stdout:
                    line = line.rstrip()
                    if line:
                        tail.append(line)
                        LoggerSetup.log(f"[PW-INSTALL] {line}", "debug")
                    if time.time() - start > timeout:
                        proc.kill()
                        return False, f"{label}: timed out after {timeout}s"
                proc.wait(timeout=30)
            except Exception as e:
                try: proc.kill()
                except Exception: pass
                return False, f"{label}: {e}"
            if proc.returncode != 0:
                return False, f"{label} failed (exit {proc.returncode}):\n" + "\n".join(tail)[-600:]
            return True, "\n".join(tail)[-300:]

        def run():
            ok1, out1 = stream([sys.executable, "-m", "pip", "install", "--disable-pip-version-check", "-U", "playwright"], 900, "pip install playwright")
            if not ok1:
                return False, out1
            if not reload_playwright():
                return False, "Playwright installed but could not be loaded. Restart the app and retry."
            # If the FULL Chromium binary is already present the engine is ready:
            # the warm-up uses it directly, so no separate headless-shell download
            # is required (that download is geo-blocked in some regions).
            ready, detail = playwright_browser_ready()
            if ready:
                LoggerSetup.log(f"Playwright engine already ready (no download needed): {detail}", "info")
                return True, f"Playwright is installed and the Chromium binary is present - ready to use (no restart needed).\nBinary: {detail}"
            # Browser missing -> download it. cdn.playwright.dev returns 403
            # "not available in your location" in some regions (Google Cloud
            # sanctions). The npmmirror REGISTRY mirror serves the real builds
            # (verified HTTP 206); the cdn.npmmirror.com path 404s, so use the
            # registry host. Fall back to the default host only if the mirror fails.
            mirror = "https://registry.npmmirror.com/-/binary/playwright"
            ok2, out2 = stream([sys.executable, "-m", "playwright", "install", "chromium"], 1800,
                               "playwright install chromium (mirror)", env={"PLAYWRIGHT_DOWNLOAD_HOST": mirror})
            if not ok2:
                LoggerSetup.log("Mirror install failed; retrying default host.", "debug")
                ok2, out2 = stream([sys.executable, "-m", "playwright", "install", "chromium"], 1800, "playwright install chromium (default)")
            if not ok2:
                return False, out2 + "\nTip: the browser download may be blocked in your region. You can still use 'Extract from OPEN browser (CDP)', which needs no Playwright browser download."
            ready, detail = playwright_browser_ready()
            if not ready:
                return False, f"Chromium download finished but binary check failed: {detail}"
            LoggerSetup.log(f"Playwright + Chromium ready: {detail}", "info")
            return True, f"Playwright + Chromium installed and loaded (no restart needed).\nBinary: {detail}"

        self._run_bg(run)

    def _retry_failed(self):
        if self.app is None: return
        cats = {ErrorCategory.NEEDS_COOKIES.value, ErrorCategory.COOKIE_DB_LOCKED.value}
        with self.app.dl_manager.state_lock:
            ids = [tid for tid, t in self.app.dl_manager.tasks.items() if t.error_category in cats and t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID}]
        for tid in ids: self.app.dl_manager.retry_task(tid)
        self._log_result(f"Retrying {len(ids)} cookie-failed task(s).")


class SinaEnterpriseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager(SETTINGS_FILE)
        ThemeColors.set_mode(self.settings_manager.get("theme"))
        global UI_FONT
        UI_FONT = self.settings_manager.get("font_family") or ("Segoe UI" if sys.platform == "win32" else "Arial")
        setup_styles(self, UI_FONT)
        self.title(f"{APP_NAME} v{APP_VERSION}"); self.geometry("1360x880"); self.minsize(1040, 660)

        self.gui_queue: queue.Queue = queue.Queue()
        self.ui_render_queue: queue.Queue = queue.Queue()
        self.thumbnail_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="Thumb")
        self._thumb_cache: collections.OrderedDict = collections.OrderedDict()
        self._thumb_lock = threading.Lock()
        self._thumb_pending: Set[Tuple[str, Tuple[int, int]]] = set()
        self._thumb_failed: Dict[Tuple[str, Tuple[int, int]], float] = {}
        self.cards: Dict[str, Dict[str, Any]] = {}; self.card_order: List[str] = []
        self._last_visible_ids: Optional[List[str]] = None
        self._tray_icon = None; self._last_clip = self._dismissed_clip = ""
        self._last_log_seq = 0; self._log_dirty = True; self._global_speed_history: List[float] = []
        self._current_page = "add"

        _install_wheel_router(self)
        self._build_sidebar(); self._build_pages()

        self.dl_manager = DownloadManager(self)
        self.dl_manager.start_processing()

        # SINA Cookie Bridge: receive auto-pushed cookies from the browser extension
        # and make sure the loadable extension folder exists for the user.
        self.cookie_bridge = CookieBridgeServer()
        self.cookie_bridge.start()
        try:
            materialize_cookie_bridge_extension()
        except Exception as e:
            LoggerSetup.log(f"Could not materialize cookie-bridge extension: {e}", "debug")

        self._show_page("add"); self._poll_gui_queue(); self._process_ui_render_queue(); self._ui_heartbeat()
        self.after(250, lambda: self._attach_taskbar())
        threading.Thread(target=self._clipboard_monitor_loop, name="ClipboardMon", daemon=True).start()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.report_callback_exception = self._tk_exception

        for k, pg in (("1", "add"), ("2", "search"), ("3", "dashboard"), ("4", "logs")):
            self.bind(f"<Control-Key-{k}>", lambda _e, p=pg: self._show_page(p))
        self.bind("<Control-comma>", lambda _e: self._open_settings())
        self.bind("<Control-d>", lambda _e: self._open_diagnostics())
        self.bind("<Control-l>", lambda _e: [self._show_page("add"), self.url_ent.focus_set()])

        LoggerSetup.set_gui_callback(lambda: setattr(self, "_log_dirty", True))
        LoggerSetup.log(f"{APP_NAME} v{APP_VERSION} (pure tkinter) initialized cleanly.", "info")
        if not resolve_ffmpeg_location(self.settings_manager.get("ffmpeg_path")):
            LoggerSetup.log("FFmpeg NOT found - merging/audio extraction will fail. Fix: Settings > Network & Engines > 'Download / Update FFmpeg' (one click).", "warning")

        # Verbose startup diagnostics (background thread so the window paints fast).
        def _startup_dump():
            try:
                diag = EnvironmentDiagnostics.collect(self.settings_manager)
                LoggerSetup.log("Startup environment diagnostics:", "debug", debug_data=diag)
                cb = str(self.settings_manager.get("cookie_browser") or "auto")
                LoggerSetup.log(f"Cookie config: source={self.settings_manager.get('cookie_source')}, browser='{cb}' -> resolved '{BrowserCookieExtractor.resolve_browser(cb)}', debug_mode={self.settings_manager.get('debug_mode')}, verify_hash={self.settings_manager.get('verify_hash')}", "debug")
            except Exception as e:
                LoggerSetup.log(f"Startup diagnostics failed: {e}", "debug")
        threading.Thread(target=_startup_dump, name="StartupDiag", daemon=True).start()

    # -- threading / lifecycle helpers --

    def run_on_gui_thread(self, callback: Callable, *args, **kwargs):
        self.gui_queue.put((callback, args, kwargs))

    def _attach_taskbar(self, tries: int = 0):
        tb = getattr(self.dl_manager, "taskbar", None)
        if not tb: return
        tb.attach_window(self)
        if not tb.hwnd and tries < 6:
            self.after(700, lambda: self._attach_taskbar(tries + 1))

    def _tk_exception(self, exc_type, exc_value, exc_tb):
        try:
            LoggerSetup.log("".join(traceback.format_exception(exc_type, exc_value, exc_tb)), "error")
        except Exception:
            pass
        try:
            if self.winfo_exists():
                messagebox.showerror("Unexpected Error", f"{exc_type.__name__}: {exc_value}\n\nDetails were written to System Logs. The app will keep running.", parent=self)
        except Exception:
            pass

    def _poll_gui_queue(self):
        if getattr(self, "dl_manager", None) and self.dl_manager.is_shutting_down: return
        try:
            for _ in range(120):
                if getattr(self, "dl_manager", None) and self.dl_manager.is_shutting_down: break
                cb, args, kwargs = self.gui_queue.get_nowait()
                try: cb(*args, **kwargs)
                except Exception as e: sys.stderr.write(f"GUI callback error: {e}\n")
                finally: self.gui_queue.task_done()
        except queue.Empty: pass
        try:
            if self.winfo_exists(): self.after(40, self._poll_gui_queue)
        except Exception: pass

    def _process_ui_render_queue(self):
        if getattr(self, "dl_manager", None) and self.dl_manager.is_shutting_down: return
        rendered = False
        try:
            for _ in range(8):
                try:
                    t = self.ui_render_queue.get_nowait()
                except queue.Empty:
                    break
                try:
                    self._render_task_card(t); rendered = True
                except Exception as e:
                    # One bad card must never kill the whole render loop.
                    LoggerSetup.log(f"Card render error: {e}", "error")
                finally:
                    self.ui_render_queue.task_done()
            if rendered: self._last_visible_ids = None; self._apply_queue_filters()
        except Exception as e:
            LoggerSetup.log(f"Render queue error: {e}", "error")
        finally:
            try:
                if self.winfo_exists(): self.after(35, self._process_ui_render_queue)
            except Exception: pass

    def _ui_heartbeat(self):
        if getattr(self, "dl_manager", None) and self.dl_manager.is_shutting_down: return
        try:
            if self._log_dirty: self._log_dirty = False; self._flush_logs_to_ui()
            self.update_status_bar(); self._update_global_progress()
        except Exception as e:
            LoggerSetup.log(f"UI heartbeat error: {e}", "error")
        finally:
            try:
                if self.winfo_exists(): self.after(800, self._ui_heartbeat)
            except Exception: pass

    # -- layout --

    def _build_sidebar(self):
        p = ThemeColors.palette()
        self.sidebar = tk.Frame(self, bg=p["SIDEBAR"], width=232)
        self.sidebar.pack(side="left", fill="y"); self.sidebar.pack_propagate(False)
        bb = tk.Frame(self.sidebar, bg=p["SIDEBAR"]); bb.pack(fill="x", padx=14, pady=(22, 16))
        tk.Label(bb, text="SINA FUSION", font=("Impact", 26), bg=p["SIDEBAR"], fg=ColorPalette.ACCENT_COLOR.value).pack(anchor="w")
        tk.Label(bb, text=f"Pro Engine v{APP_VERSION} - pure tkinter", font=(UI_FONT, 9), bg=p["SIDEBAR"], fg=p["TEXT_MUTED"]).pack(anchor="w")

        self.nav_buttons: Dict[str, ttk.Button] = {}
        for key, txt, icon, cmd in (("add", "Add & Batch", "add", lambda: self._show_page("add")), ("search", "YouTube Search", "search", lambda: self._show_page("search")), ("dashboard", "Active Queue", "queue", lambda: self._show_page("dashboard")), ("logs", "System Logs", "logs", lambda: self._show_page("logs"))):
            b = ttk.Button(self.sidebar, text=f"  {txt}", image=IconFactory.get(icon, 18, p["TEXT_PRIMARY"]), compound="left", style="Ghost.TButton", command=cmd)
            b.pack(fill="x", padx=12, pady=3); self.nav_buttons[key] = b
        ob = ttk.Button(self.sidebar, text="  Open Downloads", image=IconFactory.get("folder", 18, p["TEXT_PRIMARY"]), compound="left", style="Ghost.TButton", command=lambda: open_file_location(self.settings_manager.get("download_path")))
        ob.pack(fill="x", padx=12, pady=(10, 3))
        tk.Frame(self.sidebar, height=1, bg=p["BORDER"]).pack(fill="x", padx=14, pady=12)
        for key, txt, icon, cmd, sty in (("settings_btn", "Settings", "settings", self._open_settings, "Ghost.TButton"), ("diag_btn", "Diagnostics", "shield", self._open_diagnostics, "Ghost.TButton"), ("exit_btn", "Exit App", "exit", self._on_close, "Danger.TButton")):
            b = ttk.Button(self.sidebar, text=f"  {txt}", image=IconFactory.get(icon, 18, p["TEXT_PRIMARY"]), compound="left", style=sty, command=cmd)
            b.pack(fill="x", padx=12, pady=3); self.nav_buttons[key] = b

        tel = tk.Frame(self.sidebar, bg=p["CARD"]); tel.pack(side="bottom", fill="x", padx=12, pady=14)
        tk.Label(tel, text="LIVE TELEMETRY", font=(UI_FONT, 9, "bold"), bg=p["CARD"], fg=ColorPalette.ACCENT_COLOR.value).pack(anchor="w", padx=10, pady=(8, 2))
        self.side_stats = tk.Label(tel, text="System Ready", bg=p["CARD"], fg=p["TEXT_MUTED"], font=(UI_FONT, 10), justify="left")
        self.side_stats.pack(anchor="w", padx=10, pady=(0, 8))

    def _build_pages(self):
        p = ThemeColors.palette()
        self.content = ttk.Frame(self)
        self.content.pack(side="left", fill="both", expand=True)
        self.content.grid_rowconfigure(0, weight=1); self.content.grid_columnconfigure(0, weight=1)
        self.pages: Dict[str, ttk.Frame] = {}

        # Page 1: Add & Batch
        add = ttk.Frame(self.content); self.pages["add"] = add; add.grid_columnconfigure(0, weight=1); add.grid_rowconfigure(1, weight=1)
        self.clip_banner = tk.Frame(add, bg=p["BADGE_BG"])
        self.clip_banner_lbl = tk.Label(self.clip_banner, text="", font=(UI_FONT, 11, "bold"), bg=p["BADGE_BG"], fg=p["BADGE_TEXT"], anchor="w")
        self.clip_banner_lbl.pack(side="left", fill="x", expand=True, padx=12, pady=8)
        ttk.Button(self.clip_banner, text="Paste & Analyze", style="Accent.TButton", command=self._clip_analyze).pack(side="left", padx=4, pady=6)
        ttk.Button(self.clip_banner, text="Quick DL", style="Success.TButton", command=self._clip_quick_dl).pack(side="left", padx=4, pady=6)
        ttk.Button(self.clip_banner, text="X", width=3, command=self._clip_dismiss).pack(side="left", padx=(4, 10), pady=6)

        c = tk.Frame(add, bg=p["CARD"]); c.grid(row=1, column=0, sticky="nsew", padx=32, pady=24)
        tk.Label(c, text="Media Analyzer, Quick Presets & Batch Importer", font=(UI_FONT, 20, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"]).pack(pady=(20, 4))
        tk.Label(c, text="YouTube, Playlists, Shorts, Instagram, TikTok, X, SoundCloud, Vimeo & Direct Streams", font=(UI_FONT, 11), bg=p["CARD"], fg=p["TEXT_MUTED"]).pack(pady=(0, 14))
        slr = tk.Frame(c, bg=p["CARD"]); slr.pack(fill="x", padx=30, pady=(4, 2))
        tk.Label(slr, text="Single Media / Playlist URL:", font=(UI_FONT, 12, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"]).pack(side="left")
        self.platform_badge = tk.Label(slr, text="Ready", font=(UI_FONT, 10, "bold"), bg=p["BADGE_BG"], fg=p["BADGE_TEXT"], padx=8, pady=2)
        self.platform_badge.pack(side="right")

        ur = tk.Frame(c, bg=p["CARD"]); ur.pack(fill="x", padx=30, pady=4)
        self.url_ent = ttk.Entry(ur, font=(UI_FONT, 13))
        self.url_ent.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=6)
        ToolTip(self.url_ent, "https://www.youtube.com/watch?v=... or playlist / reel URL")
        self.url_ent.bind("<KeyRelease>", lambda _e: self._update_platform_badge()); self.url_ent.bind("<Return>", lambda _e: self._analyze())
        bp = ttk.Button(ur, image=IconFactory.get("paste", 20), style="Icon.TButton", command=self._paste_single_url); bp.pack(side="left", padx=(0, 6)); ToolTip(bp, "Paste URL")
        self.btn_anlz = ttk.Button(ur, text="Analyze Link", image=IconFactory.get("analyze", 18), compound="left", style="Accent.TButton", command=self._analyze)
        self.btn_anlz.pack(side="left")

        pr = tk.Frame(c, bg=p["CARD_ALT"]); pr.pack(fill="x", padx=30, pady=(12, 10))
        tk.Label(pr, text="Quick Download Preset:", font=(UI_FONT, 12, "bold"), bg=p["CARD_ALT"], fg=p["TEXT_PRIMARY"]).pack(side="left", padx=12, pady=10)
        self.quick_preset_var = tk.StringVar(master=self, value="Best Video (MP4)")
        ttk.Combobox(pr, textvariable=self.quick_preset_var, values=list(QUICK_PRESETS.keys()), state="readonly", width=24).pack(side="left", padx=6, pady=10)
        ttk.Button(pr, text="Quick Download URL", image=IconFactory.get("download", 16), compound="left", style="Success.TButton", command=self._quick_download_single).pack(side="right", padx=12, pady=10)

        bh = tk.Frame(c, bg=p["CARD"]); bh.pack(fill="x", padx=30, pady=(10, 4))
        tk.Label(bh, text="Batch Multi-URL Importer:", font=(UI_FONT, 12, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"]).pack(side="left")
        ttk.Button(bh, text="Clear", width=7, command=lambda: [self.batch_txt.delete("1.0", "end"), self._update_batch_count()]).pack(side="right", padx=3)
        ttk.Button(bh, text="Deduplicate", width=11, command=self._dedup_batch).pack(side="right", padx=3)
        ttk.Button(bh, text="Import .txt", width=11, command=self._import_batch_txt).pack(side="right", padx=3)
        bt_frame = tk.Frame(c, bg=p["CARD"]); bt_frame.pack(fill="both", expand=True, padx=30, pady=(0, 8))
        self.batch_txt = tk.Text(bt_frame, height=8, bg=p["INPUT"], fg=p["TEXT_PRIMARY"], insertbackground=p["TEXT_PRIMARY"], font=("Consolas", 11), relief="flat", bd=0, highlightthickness=1, highlightbackground=p["BORDER"], highlightcolor=ColorPalette.ACCENT_COLOR.value, wrap="none")
        bt_sb = ttk.Scrollbar(bt_frame, orient="vertical", command=self.batch_txt.yview)
        self.batch_txt.configure(yscrollcommand=bt_sb.set)
        self.batch_txt.pack(side="left", fill="both", expand=True); bt_sb.pack(side="right", fill="y")
        self.batch_txt.bind("<KeyRelease>", lambda _e: self._update_batch_count())
        ba = tk.Frame(c, bg=p["CARD"]); ba.pack(fill="x", padx=30, pady=(0, 18))
        self.batch_status_lbl = tk.Label(ba, text="0 valid URL(s) detected", font=(UI_FONT, 11), bg=p["CARD"], fg=p["TEXT_MUTED"])
        self.batch_status_lbl.pack(side="left")
        ttk.Button(ba, text="Queue All Batch Links", image=IconFactory.get("queue", 16), compound="left", style="Accent.TButton", command=self._add_batch_urls).pack(side="right")

        # Page 2: YouTube Search
        sp = ttk.Frame(self.content); self.pages["search"] = sp
        st = tk.Frame(sp, bg=p["CARD"]); st.pack(fill="x", padx=20, pady=(16, 10))
        tk.Label(st, text="YouTube Search & Quick Explorer", font=(UI_FONT, 17, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"]).pack(anchor="w", padx=16, pady=(12, 4))
        sb = tk.Frame(st, bg=p["CARD"]); sb.pack(fill="x", padx=16, pady=(4, 14))
        self.search_ent = ttk.Entry(sb, font=(UI_FONT, 12))
        self.search_ent.pack(side="left", fill="x", expand=True, padx=(0, 8), ipady=5)
        ToolTip(self.search_ent, "Search videos, lectures, music on YouTube...")
        self.search_ent.bind("<Return>", lambda _e: self._perform_search())
        self.search_count_var = tk.StringVar(master=self, value=str(self.settings_manager.get("search_results_count")))
        ttk.Combobox(sb, textvariable=self.search_count_var, values=["10", "15", "20", "30"], state="readonly", width=5).pack(side="left", padx=(0, 8))
        self.btn_search = ttk.Button(sb, text="Search", image=IconFactory.get("search", 16), compound="left", style="Accent.TButton", command=self._perform_search)
        self.btn_search.pack(side="right")
        self.search_scroll = ScrollFrame(sp); self.search_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        ttk.Label(self.search_scroll.inner, text="Enter keywords above to search YouTube directly.", style="Muted.TLabel").pack(pady=40)

        # Page 3: Queue Dashboard
        dash = ttk.Frame(self.content); self.pages["dashboard"] = dash
        tc = tk.Frame(dash, bg=p["CARD"]); tc.pack(fill="x", padx=20, pady=(16, 8))
        tr = tk.Frame(tc, bg=p["CARD"]); tr.pack(fill="x", padx=14, pady=(10, 4))
        tk.Label(tr, text="Download Queue & Telemetry", font=(UI_FONT, 17, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"]).pack(side="left")
        self.global_speed_canvas = tk.Canvas(tr, width=180, height=34, bg=p["CANVAS"], highlightthickness=0)
        self.global_speed_canvas.pack(side="right", padx=(10, 0))
        ttk.Button(tr, text="Scheduler", image=IconFactory.get("clock", 15), compound="left", command=lambda: SchedulerDialog(self)).pack(side="right", padx=6)
        cur_lim = safe_int(self.settings_manager.get("global_speed_limit_kbps"), 0, 0, 1048576)
        self.speed_limit_var = tk.StringVar(master=self, value=next((k for k, v in SPEED_LIMIT_CHOICES.items() if v == cur_lim), "Unlimited"))
        ttk.Combobox(tr, textvariable=self.speed_limit_var, values=list(SPEED_LIMIT_CHOICES.keys()), state="readonly", width=12).pack(side="right", padx=6)
        self.speed_limit_var.trace_add("write", lambda *_a: self._on_quick_speed_limit(self.speed_limit_var.get()))
        tk.Label(tr, text="Speed Cap:", font=(UI_FONT, 10), bg=p["CARD"], fg=p["TEXT_MUTED"]).pack(side="right", padx=(8, 2))
        self.dash_summary_lbl = tk.Label(tc, text="Active: 0 | Queued: 0 | Completed: 0 | Speed: 0 B/s", font=(UI_FONT, 11, "bold"), bg=p["CARD"], fg=ColorPalette.ACCENT_COLOR.value, anchor="w")
        self.dash_summary_lbl.pack(fill="x", padx=14, pady=(0, 8))

        cr = ttk.Frame(dash); cr.pack(fill="x", padx=20, pady=(2, 8))
        bl = ttk.Frame(cr); bl.pack(side="left")
        for txt, sty, cmd in (("Resume All", "Success.TButton", self._bulk_resume), ("Pause All", "Warning.TButton", self._bulk_pause), ("Retry Failed", "Warning.TButton", self._bulk_retry_failed), ("Cancel Active", "Danger.TButton", self._bulk_cancel), ("Clear Done", "TButton", self._bulk_clear), ("Export", "TButton", self._export_queue_dialog), ("Import", "TButton", self._import_queue_dialog)):
            ttk.Button(bl, text=txt, style=sty, command=cmd).pack(side="left", padx=2)
        fr = ttk.Frame(cr); fr.pack(side="right")
        self.queue_filter_var = tk.StringVar(master=self, value="All")
        fc = ttk.Combobox(fr, textvariable=self.queue_filter_var, values=["All", "Active", "Queued", "Paused", "Completed", "Errors"], state="readonly", width=11)
        fc.pack(side="left", padx=(0, 8)); fc.bind("<<ComboboxSelected>>", lambda _e: self._apply_queue_filters())
        self.queue_search_ent = ttk.Entry(fr, width=20); self.queue_search_ent.pack(side="left")
        ToolTip(self.queue_search_ent, "Filter queue...")
        self.queue_search_ent.bind("<KeyRelease>", lambda _e: self._apply_queue_filters())
        self.queue_scroll = ScrollFrame(dash); self.queue_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 18))

        # Page 4: Logs
        logs = ttk.Frame(self.content); self.pages["logs"] = logs
        hd = tk.Frame(logs, bg=p["CARD"]); hd.pack(fill="x", padx=20, pady=(16, 8))
        tk.Label(hd, text="System Logs & Diagnostics Console", font=(UI_FONT, 15, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"]).pack(side="left", padx=14, pady=10)
        ct = tk.Frame(hd, bg=p["CARD"]); ct.pack(side="right", padx=12, pady=8)
        self.log_level_var = tk.StringVar(master=self, value="ALL")
        lc = ttk.Combobox(ct, textvariable=self.log_level_var, values=["ALL", "INFO", "WARNING", "ERROR", "DEBUG"], state="readonly", width=9)
        lc.pack(side="left", padx=6); lc.bind("<<ComboboxSelected>>", lambda _e: self._refresh_logs_full())
        self.log_search_ent = ttk.Entry(ct, width=18); self.log_search_ent.pack(side="left", padx=4)
        ToolTip(self.log_search_ent, "Search logs...")
        self.log_search_ent.bind("<KeyRelease>", lambda _e: self._refresh_logs_full())
        self.log_autoscroll_var = tk.BooleanVar(master=self, value=True)
        ttk.Checkbutton(ct, text="Auto-Scroll", variable=self.log_autoscroll_var, style="Card.TCheckbutton").pack(side="left", padx=6)
        ttk.Button(ct, text="Export", width=7, command=self._export_logs).pack(side="left", padx=3)
        self._copy_logs_btn = ttk.Button(ct, text="Copy Logs", width=10, command=self._copy_logs)
        self._copy_logs_btn.pack(side="left", padx=3)
        ToolTip(self._copy_logs_btn, "Copy the shown log entries (current filter/search) to the clipboard.")
        ttk.Button(ct, text="Logs Folder", width=10, command=lambda: open_file_location(str(LoggerSetup.log_dir() / "sina_fusion.log"))).pack(side="left", padx=3)
        ttk.Button(ct, text="Clear", width=6, command=self._clear_logs).pack(side="left", padx=3)
        lt_frame = ttk.Frame(logs); lt_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))
        self.log_txt = tk.Text(lt_frame, bg=p["CANVAS"], fg=p["TEXT_PRIMARY"], insertbackground=p["TEXT_PRIMARY"], font=("Consolas", 11), relief="flat", wrap="none", state="disabled")
        lt_sb = ttk.Scrollbar(lt_frame, orient="vertical", command=self.log_txt.yview)
        self.log_txt.configure(yscrollcommand=lt_sb.set)
        self.log_txt.pack(side="left", fill="both", expand=True); lt_sb.pack(side="right", fill="y")
        for tg, col in (("INFO", "#E2E8F0"), ("WARNING", "#FBBF24"), ("ERROR", "#FB7185"), ("DEBUG", "#94A3B8")):
            self.log_txt.tag_config(tg, foreground=col)

    def _show_page(self, name: str):
        self._current_page = name
        for pg in self.pages.values(): pg.grid_forget()
        if name in self.pages: self.pages[name].grid(row=0, column=0, sticky="nsew")
        for key in ("add", "search", "dashboard", "logs"):
            if key in self.nav_buttons:
                self.nav_buttons[key].configure(style="GhostActive.TButton" if key == name else "Ghost.TButton")

    def _rebuild_ui(self):
        """Rebuild main layout (used after a theme change). Toplevel dialogs are preserved."""
        # Snapshot user-entered state so a theme switch does not discard it.
        batch_txt = url_txt = ""
        try: batch_txt = self.batch_txt.get("1.0", "end")
        except Exception: pass
        try: url_txt = self.url_ent.get()
        except Exception: pass
        for w in (getattr(self, "sidebar", None), getattr(self, "content", None)):
            if w is not None:
                try: w.destroy()
                except Exception: pass
        self.cards.clear(); self.card_order.clear(); self._last_visible_ids = None
        setup_styles(self, UI_FONT)
        self._build_sidebar(); self._build_pages()
        try:
            if batch_txt.strip(): self.batch_txt.insert("1.0", batch_txt)
            self._update_batch_count()
        except Exception: pass
        try:
            if url_txt: self.url_ent.insert(0, url_txt); self._update_platform_badge()
        except Exception: pass
        self._last_log_seq = 0; self._log_dirty = True  # re-render existing logs into the new widget
        self._show_page(self._current_page if self._current_page in self.pages else "add")
        with self.dl_manager.state_lock:
            tasks = list(self.dl_manager.tasks.values())
        for t in tasks: self.add_task_to_ui(t)
        self.update_status_bar(); self._update_global_progress()    # -- add / batch / clipboard --

    def _update_platform_badge(self):
        u = self.url_ent.get().strip()
        self.platform_badge.configure(text=detect_platform_label(u) if u else "Ready")

    def _update_batch_count(self):
        self.batch_status_lbl.configure(text=f"{len(extract_urls_from_text(self.batch_txt.get('1.0', 'end')))} valid URL(s) detected")

    def _dedup_batch(self):
        urls = extract_urls_from_text(self.batch_txt.get("1.0", "end"))
        self.batch_txt.delete("1.0", "end")
        if urls: self.batch_txt.insert("1.0", "\n".join(urls) + "\n")
        self._update_batch_count()

    def _paste_single_url(self):
        try: txt = self.clipboard_get().strip()
        except Exception: txt = ""
        if txt:
            urls = extract_urls_from_text(txt)
            self.url_ent.delete(0, "end"); self.url_ent.insert(0, urls[0] if urls else txt); self._update_platform_badge()

    def _clip_analyze(self):
        if self._last_clip:
            self.url_ent.delete(0, "end"); self.url_ent.insert(0, self._last_clip); self._update_platform_badge(); self._clip_dismiss(); self._analyze()

    def _clip_quick_dl(self):
        if self._last_clip:
            self.url_ent.delete(0, "end"); self.url_ent.insert(0, self._last_clip); self._update_platform_badge(); self._clip_dismiss(); self._quick_download_single()

    def _clip_dismiss(self):
        self._dismissed_clip = self._last_clip
        try: self.clip_banner.grid_forget()
        except Exception: pass

    def _clipboard_monitor_loop(self):
        while not getattr(self, "dl_manager", None) or not self.dl_manager.is_shutting_down:
            if self.settings_manager.get("clipboard_monitor"): self.run_on_gui_thread(self._check_clipboard)
            time.sleep(2.0)

    def _check_clipboard(self):
        if not self.settings_manager.get("clipboard_monitor"): return
        try: raw = self.clipboard_get().strip()
        except Exception: return
        urls = extract_urls_from_text(raw)
        if not urls: return
        cand = urls[0]
        if cand in {self._last_clip, self._dismissed_clip} or not is_likely_media_url(cand): return
        self._last_clip = cand
        self.clip_banner_lbl.configure(text=f"Clipboard {detect_platform_label(cand)} link: {cand[:75]}{'...' if len(cand) > 75 else ''}")
        self.clip_banner.grid(row=0, column=0, sticky="ew", padx=32, pady=(16, 0))

    def _import_batch_txt(self):
        fp = filedialog.askopenfilename(parent=self, filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not fp: return
        try:
            urls = extract_urls_from_text(Path(fp).read_text(encoding="utf-8", errors="replace"))
            if urls:
                cur = self.batch_txt.get("1.0", "end").strip()
                self.batch_txt.insert("end", ("\n" if cur else "") + "\n".join(urls) + "\n"); self._update_batch_count()
            else:
                messagebox.showinfo("No Links", "No valid URLs found.", parent=self)
        except Exception as e:
            messagebox.showerror("Import Error", str(e), parent=self)

    # -- task creation --

    def _build_preset_ydl_opts(self, pname: str, is_pl: bool = False) -> Tuple[Dict[str, Any], str, str]:
        p = QUICK_PRESETS.get(pname, QUICK_PRESETS["Best Video (MP4)"])
        dl_dir, pat = Path(self.settings_manager.get("download_path")), self.settings_manager.get("filename_pattern")
        opts: Dict[str, Any] = {"outtmpl": str(dl_dir / f"{pat}.%(ext)s"), "quiet": True, "ignoreerrors": False, "overwrites": False, "continuedl": True, "windowsfilenames": sys.platform == "win32", "noplaylist": not is_pl}
        pps: List[Dict[str, Any]] = []
        if p["type"] == "audio":
            dl_type = "Audio"; opts["format"] = "bestaudio/best"
            pps.append({"key": "FFmpegExtractAudio", "preferredcodec": p["codec"], "preferredquality": p["quality"]}); allow_th = p["codec"] != "wav"
        else:
            dl_type = "Video"; opts["format"] = p["format"]; opts["merge_output_format"] = p.get("ext", "mp4"); allow_th = True
        if self.settings_manager.get("embed_metadata"): pps.append({"key": "FFmpegMetadata", "add_metadata": True, "add_chapters": True})
        if self.settings_manager.get("embed_thumbnail") and allow_th: opts["writethumbnail"] = True; pps.append({"key": "EmbedThumbnail", "already_have_thumbnail": False})
        sb = self.settings_manager.get("sponsorblock_categories") or []
        if sb: opts["_sponsorblock_categories"] = list(sb)
        if pps: opts["postprocessors"] = pps
        return opts, dl_type, pname

    def _quick_download_single(self):
        urls = extract_urls_from_text(self.url_ent.get().strip())
        if not urls: messagebox.showwarning("Invalid URL", "Enter a valid http/https URL first.", parent=self); return
        u, pname = urls[0], self.quick_preset_var.get()
        is_pl = "list=" in u.lower() and not any(k in u.lower() for k in ("watch?v=", "youtu.be/", "/shorts/", "/live/"))
        opts, dt, prof = self._build_preset_ydl_opts(pname, is_pl)
        self.dl_manager.add_task(DownloadTask(task_id=f"t_{time.time_ns()}_{random.randint(100, 999)}", url=u, ydl_opts=opts, download_type=dt, service_type=detect_service_type(u), title=f"{detect_platform_label(u)} ({u[:45]}...)" if len(u) > 45 else u, is_placeholder_title=True, quality_profile=prof))
        self._show_page("dashboard")

    def _add_batch_urls(self):
        urls = extract_urls_from_text(self.batch_txt.get("1.0", "end"))
        if not urls: messagebox.showwarning("Empty Batch", "No valid URLs found.", parent=self); return
        pname = self.quick_preset_var.get()
        for i, u in enumerate(urls):
            is_pl = "list=" in u.lower() and not any(k in u.lower() for k in ("watch?v=", "youtu.be/", "/shorts/", "/live/"))
            opts, dt, prof = self._build_preset_ydl_opts(pname, is_pl)
            self.dl_manager.add_task(DownloadTask(task_id=f"b_{time.time_ns()}_{i}_{random.randint(100, 999)}", url=u, ydl_opts=opts, download_type=dt, service_type=detect_service_type(u), title=f"[{i + 1}/{len(urls)}] {detect_platform_label(u)} - {u[:44]}", is_placeholder_title=True, quality_profile=prof))
        self.batch_txt.delete("1.0", "end"); self._update_batch_count(); self._show_page("dashboard")

    def _analyze(self):
        urls = extract_urls_from_text(self.url_ent.get().strip())
        if not urls: messagebox.showwarning("URL Required", "Please paste a valid media URL.", parent=self); return
        u, apl, cu = urls[0], False, urls[0]
        low = u.lower()
        if "list=" in low:
            if any(k in low for k in ("watch?v=", "youtu.be/", "/shorts/", "/live/")):
                res = messagebox.askyesnocancel("Playlist Detected", "URL contains both a video and a playlist.\n\nYes: Load entire playlist\nNo: Single video only\nCancel: Abort", parent=self)
                if res is None: return
                apl = bool(res)
                if not apl: cu = strip_playlist_query_params(u)
            else: apl = True
        self.btn_anlz.configure(state="disabled", text="Analyzing...")
        threading.Thread(target=self._analyze_thread, args=(cu, apl), name="Analyze", daemon=True).start()

    def _analyze_thread(self, url: str, apl: bool):
        try:
            opts = self.dl_manager.fingerprint.get_yt_dlp_options(url)
            opts.update({"quiet": True, "no_warnings": True, "noplaylist": not apl})
            if apl: opts["extract_flat"] = "in_playlist"
            self.dl_manager.antibot.apply_common_options(opts, url=url)
            with yt_dlp.YoutubeDL(opts) as ydl: info = ydl.extract_info(url, download=False)
            if not info: raise RuntimeError("No metadata returned.")
            if "entries" in info and info["entries"] is not None: info["entries"] = list(info["entries"])
            self.run_on_gui_thread(lambda i=info: NewTaskDialog(self, i, self._add_final_task))
        except Exception as e:
            err = clean_ansi_codes(str(e)); LoggerSetup.log(f"Analysis failed: {err}", "error")
            self.run_on_gui_thread(lambda m=err: messagebox.showerror("Analysis Error", m, parent=self))
        finally:
            self.run_on_gui_thread(lambda: self.btn_anlz.configure(state="normal", text="Analyze Link") if self.winfo_exists() else None)

    def _add_final_task(self, info: Dict[str, Any], options: Dict[str, Any]):
        url = str(info.get("webpage_url") or info.get("original_url") or info.get("url") or "")
        if not url: messagebox.showerror("Error", "Missing source URL.", parent=self); return
        dl_dir, pat = Path(self.settings_manager.get("download_path")), self.settings_manager.get("filename_pattern")
        fid, cont, subs, has_a, smode = str(options.get("format_id") or "bestvideo+bestaudio/best"), str(options.get("container") or "mp4"), list(options.get("subs") or []), bool(options.get("has_auto_subs")), str(options.get("sub_mode") or "External File")
        chps, cr, merge, aopts, sb = list(options.get("chapters") or []), options.get("custom_range"), bool(options.get("merge", True)), options.get("audio_opts"), list(options.get("sponsorblock_cats") or [])
        pl_idx, pl_sub = list(options.get("playlist_indices") or []), bool(options.get("playlist_subfolder", True))
        base: Dict[str, Any] = {"outtmpl": str(dl_dir / f"{pat}.%(ext)s"), "quiet": True, "writethumbnail": False, "ignoreerrors": False, "overwrites": False, "continuedl": True, "windowsfilenames": sys.platform == "win32"}
        pps: List[Dict[str, Any]] = []
        if aopts:
            dt, cc, q = "Audio", str(aopts.get("format") or "mp3"), str(aopts.get("quality") or "320")
            base["format"] = "bestaudio/best"; pps.append({"key": "FFmpegExtractAudio", "preferredcodec": cc, "preferredquality": q})
            qp, can_th = f"Audio {cc.upper()} {q}k", (cc != "wav")
        else:
            dt = "Video"
            if merge: base["format"] = fid if (fid == "best" or "+" in fid or "bestvideo" in fid) else f"{fid}+bestaudio/best"; base["merge_output_format"] = cont
            else: base["format"] = fid
            qp, can_th = ("Auto Best" if "bestvideo" in fid else f"Fmt {fid} ({cont})"), (cont != "webm")
        if subs:
            base["writesubtitles"], base["subtitleslangs"] = True, subs
            if has_a: base["writeautomaticsub"] = True
            if smode == "Burn Hardsub" and not aopts: base["_burn_subtitles"] = True
            elif smode == "Embed Softsub" and not aopts: base["embedsubtitles"] = True; pps.append({"key": "FFmpegEmbedSubtitle"})
        if options.get("embed_metadata"): pps.append({"key": "FFmpegMetadata", "add_metadata": True, "add_chapters": True})
        if options.get("embed_thumbnail") and can_th: base["writethumbnail"] = True; pps.append({"key": "EmbedThumbnail", "already_have_thumbnail": False})
        if sb: base["_sponsorblock_categories"] = sb
        if pps: base["postprocessors"] = pps

        entries = info.get("entries") or []
        if entries and pl_idx:
            pt = str(info.get("title") or info.get("playlist_title") or "Playlist")
            tr = (dl_dir / sanitize_filename_part(pt, "Playlist", 80)) if pl_sub else dl_dir; tr.mkdir(parents=True, exist_ok=True)
            ek = str(info.get("extractor_key") or info.get("extractor") or url).lower()
            for ix in pl_idx:
                try:
                    ent = entries[ix - 1]
                    if not ent: continue
                    eu = ent.get("webpage_url") or ent.get("url")
                    if eu and not str(eu).startswith("http"): eu = f"https://www.youtube.com/watch?v={eu}" if "youtube" in ek else None
                    if not eu and ent.get("id") and "youtube" in ek: eu = f"https://www.youtube.com/watch?v={ent['id']}"
                    if not eu: continue
                    eo = copy.deepcopy(base); eo["noplaylist"] = True; et = str(ent.get("title") or f"Video {ix}")
                    eo["outtmpl"] = str(tr / f"{ix:03d} - {escape_ytdlp_template_literal(sanitize_filename_part(et, f'Video_{ix}'))} [%(id)s].%(ext)s")
                    self.dl_manager.add_task(DownloadTask(task_id=f"pl_{time.time_ns()}_{ix}_{random.randint(100, 999)}", url=str(eu), ydl_opts=eo, download_type=dt, service_type=detect_service_type(str(eu)), title=et, uploader=str(ent.get("uploader") or info.get("uploader") or ""), duration_sec=ent.get("duration"), quality_profile=qp, thumbnail_url=ent.get("thumbnail") or info.get("thumbnail"), category="Playlist", is_playlist_item=True, playlist_title=pt))
                except Exception as ex: LoggerSetup.log(f"Playlist item #{ix} err: {ex}", "error")
            self._show_page("dashboard"); return

        if chps:
            bt = str(info.get("title") or "Video")
            for ci, ch in enumerate(chps, 1):
                co = copy.deepcopy(base); s0, e0 = float(ch.get("start_time") or 0.0), ch.get("end_time")
                co["download_ranges_spec"], co["force_keyframes_at_cuts"] = [(s0, None if e0 is None else float(e0))], True
                cht = str(ch.get("title") or f"Chapter {ci}")
                co["outtmpl"] = str(dl_dir / f"%(title)s - {ci:02d} {escape_ytdlp_template_literal(sanitize_filename_part(cht, f'ch_{ci}'))}.%(ext)s")
                self.dl_manager.add_task(DownloadTask(task_id=f"ch_{time.time_ns()}_{ci}_{random.randint(100, 999)}", url=url, ydl_opts=co, download_type=dt, service_type=detect_service_type(url), title=f"{bt} - {cht}", uploader=str(info.get("uploader") or info.get("channel") or ""), duration_sec=(float(e0) - s0) if e0 is not None else None, quality_profile=f"{qp} [Ch]", thumbnail_url=info.get("thumbnail"), info_dict=info))
            self._show_page("dashboard"); return

        ctag = ""
        if cr:
            s_sec, e_sec = cr; base["download_ranges_spec"], base["force_keyframes_at_cuts"] = [(float(s_sec), None if e_sec is None else float(e_sec))], True
            base["outtmpl"] = str(dl_dir / f"{pat} [clip {format_duration(s_sec).replace(':', '-')}_to_{format_duration(e_sec).replace(':', '-') if e_sec is not None else 'end'}].%(ext)s")
            ctag = f" [Clip {format_duration(s_sec)}-{format_duration(e_sec) if e_sec is not None else 'End'}]"
        self.dl_manager.add_task(DownloadTask(task_id=f"t_{time.time_ns()}_{random.randint(100, 999)}", url=url, ydl_opts=base, download_type=dt, service_type=detect_service_type(url), title=str(info.get("title") or info.get("id") or "Untitled Media") + ctag, uploader=str(info.get("uploader") or info.get("channel") or ""), duration_sec=info.get("duration"), quality_profile=qp, thumbnail_url=info.get("thumbnail"), info_dict=info))
        self._show_page("dashboard")

    # -- search --

    def _perform_search(self):
        q = self.search_ent.get().strip()
        if not q: return
        cnt = safe_int(self.search_count_var.get(), 15, 5, 30)
        for w in self.search_scroll.inner.winfo_children(): w.destroy()
        lbl = ttk.Label(self.search_scroll.inner, text=f"Searching YouTube for '{q}'...", style="Muted.TLabel"); lbl.pack(pady=30)
        self.btn_search.configure(state="disabled", text="Searching...")
        threading.Thread(target=self._search_thread, args=(q, cnt, lbl), name="YTSearch", daemon=True).start()

    def _search_thread(self, query: str, count: int, loading_lbl):
        try:
            opts = self.dl_manager.fingerprint.get_yt_dlp_options()
            opts.update({"extract_flat": True, "quiet": True, "no_warnings": True})
            self.dl_manager.antibot.apply_common_options(opts)
            with yt_dlp.YoutubeDL(opts) as ydl: res = ydl.extract_info(f"ytsearch{count}:{query}", download=False)
            self.run_on_gui_thread(self._render_search_results, res or {}, loading_lbl)
        except Exception as e:
            err = clean_ansi_codes(str(e)); LoggerSetup.log(f"Search failed: {err}", "error")
            self.run_on_gui_thread(lambda: [loading_lbl.configure(text=f"Search failed: {err}") if loading_lbl.winfo_exists() else None, self.btn_search.configure(state="normal", text="Search")])

    def _render_search_results(self, results: Dict[str, Any], loading_lbl):
        self.btn_search.configure(state="normal", text="Search")
        if loading_lbl.winfo_exists(): loading_lbl.destroy()
        p = ThemeColors.palette()
        entries = [e for e in (results.get("entries") or []) if e]
        if not entries:
            ttk.Label(self.search_scroll.inner, text="No matching results found.", style="Muted.TLabel").pack(pady=30); return
        for ent in entries:
            card = tk.Frame(self.search_scroll.inner, bg=p["CARD"]); card.pack(fill="x", pady=5); card.grid_columnconfigure(1, weight=1)
            th = tk.Label(card, text="...", width=16, height=4, bg=p["CANVAS"], fg=p["TEXT_MUTED"])
            th.grid(row=0, column=0, rowspan=2, padx=10, pady=10)
            tu = ent.get("thumbnail") or ((ent.get("thumbnails") or [{}])[-1].get("url"))
            if tu: self._load_img_async(tu, th, size=(120, 68))
            t_txt = str(ent.get("title") or "Unknown Title")
            tk.Label(card, text=t_txt, font=(UI_FONT, 12, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"], anchor="w", justify="left", wraplength=540).grid(row=0, column=1, sticky="sw", padx=8, pady=(10, 2))
            meta = [str(ent.get("uploader") or ent.get("channel") or "Unknown")]
            if ent.get("duration"): meta.append(format_duration(ent["duration"]))
            if ent.get("view_count"): meta.append(f"{format_count(ent['view_count'])} views")
            tk.Label(card, text="  |  ".join(meta), bg=p["CARD"], fg=p["TEXT_MUTED"], font=(UI_FONT, 10), anchor="w").grid(row=1, column=1, sticky="nw", padx=8, pady=(0, 10))
            u = ent.get("webpage_url") or ent.get("url")
            if u and not str(u).startswith("http"): u = f"https://www.youtube.com/watch?v={u}"
            elif not u and ent.get("id"): u = f"https://www.youtube.com/watch?v={ent['id']}"
            if u:
                btns = tk.Frame(card, bg=p["CARD"]); btns.grid(row=0, column=2, rowspan=2, padx=12, pady=10)
                ttk.Button(btns, text="Analyze", style="Accent.TButton", command=lambda x=u: [self.url_ent.delete(0, "end"), self.url_ent.insert(0, x), self._update_platform_badge(), self._show_page("add"), self._analyze()]).pack(side="left", padx=3)
                ttk.Button(btns, text="Best MP4", style="Success.TButton", command=lambda x=u, tt=t_txt, t_u=tu, e=ent: self._direct_search_dl(x, tt, t_u, e, "Best Video (MP4)")).pack(side="left", padx=3)
                ttk.Button(btns, text="MP3", command=lambda x=u, tt=t_txt, t_u=tu, e=ent: self._direct_search_dl(x, tt, t_u, e, "Audio MP3 (320k)")).pack(side="left", padx=3)
                bw = ttk.Button(btns, image=IconFactory.get("open", 15), style="Icon.TButton", command=lambda x=u: webbrowser.open(x)); bw.pack(side="left", padx=3); ToolTip(bw, "Open in Browser")

    def _direct_search_dl(self, url: str, title: str, tu: Optional[str], ent: Dict[str, Any], pname: str):
        opts, dt, prof = self._build_preset_ydl_opts(pname)
        self.dl_manager.add_task(DownloadTask(task_id=f"s_{time.time_ns()}_{random.randint(100, 999)}", url=url, ydl_opts=opts, download_type=dt, service_type=ServiceType.YOUTUBE, title=title, uploader=str(ent.get("uploader") or ent.get("channel") or ""), duration_sec=ent.get("duration"), quality_profile=prof, thumbnail_url=tu))
        self._show_page("dashboard")

    # -- queue operations --

    def _on_quick_speed_limit(self, label: str):
        kbps = SPEED_LIMIT_CHOICES.get(label, 0)
        if safe_int(self.settings_manager.get("global_speed_limit_kbps"), 0, 0, 1048576) == kbps: return
        self.settings_manager.set("global_speed_limit_kbps", kbps); self.settings_manager.save()
        LoggerSetup.log(f"Speed cap set to {label} (applies to new/retried tasks).", "info")

    def _bulk_resume(self):
        self.dl_manager.set_schedule_delay(0)
        with self.dl_manager.state_lock: ids = [tid for tid, t in self.dl_manager.tasks.items() if t.status == DownloadStatus.PAUSED]
        for tid in ids: self.dl_manager.resume_task(tid)

    def _bulk_pause(self):
        with self.dl_manager.state_lock: ids = [tid for tid, t in self.dl_manager.tasks.items() if t.status in {DownloadStatus.DOWNLOADING, DownloadStatus.STARTING, DownloadStatus.QUEUED}]
        for tid in ids: self.dl_manager.pause_task(tid)

    def _bulk_retry_failed(self):
        with self.dl_manager.state_lock: ids = [tid for tid, t in self.dl_manager.tasks.items() if t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID, DownloadStatus.CANCELLED}]
        for tid in ids: self.dl_manager.retry_task(tid)

    def _bulk_cancel(self):
        with self.dl_manager.state_lock: ids = [tid for tid, t in self.dl_manager.tasks.items() if t.status in {DownloadStatus.QUEUED, DownloadStatus.STARTING, DownloadStatus.DOWNLOADING, DownloadStatus.PAUSED}]
        for tid in ids: self.dl_manager.cancel_task(tid)

    def _bulk_clear(self):
        with self.dl_manager.state_lock: ids = [tid for tid, t in self.dl_manager.tasks.items() if t.status in {DownloadStatus.COMPLETED, DownloadStatus.SKIPPED, DownloadStatus.CANCELLED, DownloadStatus.INVALID}]
        for tid in ids: self.dl_manager.remove_task_from_ui(tid)

    def _export_queue_dialog(self):
        d = filedialog.asksaveasfilename(parent=self, defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile="sina_queue_backup.json")
        if d:
            try: messagebox.showinfo("Exported", f"Exported {self.dl_manager.export_queue(d)} task(s).", parent=self)
            except Exception as e: messagebox.showerror("Error", str(e), parent=self)

    def _import_queue_dialog(self):
        s = filedialog.askopenfilename(parent=self, filetypes=[("JSON", "*.json")])
        if s:
            try: messagebox.showinfo("Imported", f"Imported {self.dl_manager.import_queue(s)} task(s).", parent=self)
            except Exception as e: messagebox.showerror("Error", str(e), parent=self)

    def _apply_queue_filters(self):
        flt, q = self.queue_filter_var.get(), self.queue_search_ent.get().strip().lower()
        vis = []
        for tid in self.card_order:
            ui, t = self.cards.get(tid), self.dl_manager.get_task(tid)
            if not ui or not t or not ui["card"].winfo_exists(): continue
            ok_s = (flt == "All" or (flt == "Active" and t.status in {DownloadStatus.DOWNLOADING, DownloadStatus.STARTING, DownloadStatus.PROCESSING, DownloadStatus.VERIFYING}) or (flt == "Queued" and t.status == DownloadStatus.QUEUED) or (flt == "Paused" and t.status == DownloadStatus.PAUSED) or (flt == "Completed" and t.status in {DownloadStatus.COMPLETED, DownloadStatus.SKIPPED}) or (flt == "Errors" and t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID, DownloadStatus.CANCELLED}))
            if ok_s and ((not q) or (q in f"{t.title} {t.url} {t.uploader} {t.category}".lower())): vis.append(tid)
        if self._last_visible_ids != vis:
            self._last_visible_ids = vis
            for tid in self.card_order:
                ui = self.cards.get(tid)
                if ui and ui["card"].winfo_exists() and ui["card"].winfo_manager(): ui["card"].pack_forget()
            for tid in vis:
                ui = self.cards.get(tid)
                if ui and ui["card"].winfo_exists(): ui["card"].pack(fill="x", pady=5, padx=2)

    # -- task cards --

    def add_task_to_ui(self, task: DownloadTask):
        self.ui_render_queue.put(task)

    def _render_task_card(self, task: DownloadTask):
        if task.task_id in self.cards: self.update_task_ui(task.task_id); return
        p = ThemeColors.palette()
        card = tk.Frame(self.queue_scroll.inner, bg=p["CARD"]); card.pack(fill="x", pady=5, padx=2); card.grid_columnconfigure(1, weight=1)
        thumb = tk.Label(card, text=detect_platform_label(task.url)[:10], width=13, height=3, bg=p["CANVAS"], fg=p["TEXT_MUTED"], font=(UI_FONT, 9))
        thumb.grid(row=0, column=0, rowspan=3, padx=10, pady=10)
        if task.thumbnail_url: self._load_img_async(task.thumbnail_url, thumb, size=(96, 54))
        tlbl = tk.Label(card, text=task.title or "Untitled Media", font=(UI_FONT, 12, "bold"), bg=p["CARD"], fg=p["TEXT_PRIMARY"], anchor="w", justify="left", wraplength=560)
        tlbl.grid(row=0, column=1, sticky="ew", padx=(4, 8), pady=(8, 0))
        mlbl = tk.Label(card, text=f"{detect_platform_label(task.url)}  |  {task.quality_profile}", bg=p["CARD"], fg=p["TEXT_MUTED"], font=(UI_FONT, 10), anchor="w")
        mlbl.grid(row=0, column=2, sticky="e", padx=8, pady=(8, 0))
        slbl = tk.Label(card, text=task.status.value, bg=p["CARD"], fg=ColorPalette.TEXT_GRAY.value, anchor="w", font=(UI_FONT, 11))
        slbl.grid(row=1, column=1, sticky="ew", padx=(4, 8))
        graph = tk.Canvas(card, width=140, height=28, bg=p["CANVAS"], highlightthickness=0); graph.grid(row=1, column=2, padx=8, pady=2)
        prog = ttk.Progressbar(card, style="Horizontal.TProgressbar", mode="determinate", maximum=1.0)
        prog.grid(row=2, column=1, columnspan=2, sticky="ew", padx=(4, 8), pady=(4, 10)); prog.configure(value=task.progress_float)
        btns = tk.Frame(card, bg=p["CARD"]); btns.grid(row=0, column=3, rowspan=3, padx=10, pady=8)
        b_act = ttk.Button(btns, style="Icon.TButton", command=lambda tid=task.task_id: self._card_action(tid)); b_act.grid(row=0, column=0, padx=2); t_act = ToolTip(b_act, "Action")
        b_info = ttk.Button(btns, image=IconFactory.get("info", 16), style="Icon.TButton", command=lambda tid=task.task_id: [t := self.dl_manager.get_task(tid), t and TaskInspectorDialog(self, t)]); b_info.grid(row=0, column=1, padx=2); ToolTip(b_info, "Inspect")
        b_extra = ttk.Button(btns, image=IconFactory.get("play", 16), style="Icon.TButton"); b_extra.grid(row=0, column=2, padx=2); t_extra = ToolTip(b_extra, "Preview / Repair / Priority")
        b_folder = ttk.Button(btns, image=IconFactory.get("folder", 16), style="Icon.TButton", command=lambda tid=task.task_id: [t := self.dl_manager.get_task(tid), t and open_file_location(t.filepath or self.settings_manager.get("download_path"))]); b_folder.grid(row=0, column=3, padx=2); ToolTip(b_folder, "Open Folder")
        b_clear = ttk.Button(btns, image=IconFactory.get("clear", 16), style="Icon.TButton", command=lambda tid=task.task_id: self.dl_manager.remove_task_from_ui(tid)); b_clear.grid(row=0, column=4, padx=2); ToolTip(b_clear, "Remove")
        self.cards[task.task_id] = {"card": card, "thumb": thumb, "title": tlbl, "meta": mlbl, "status": slbl, "prog": prog, "act": b_act, "act_tip": t_act, "extra": b_extra, "extra_tip": t_extra, "folder": b_folder, "graph": graph, "_indeterminate": False}
        self.card_order.append(task.task_id); self.update_task_ui(task.task_id)

    def _card_action(self, tid: str):
        t = self.dl_manager.get_task(tid)
        if not t: return
        if t.status == DownloadStatus.DOWNLOADING: self.dl_manager.pause_task(tid)
        elif t.status == DownloadStatus.PAUSED: self.dl_manager.resume_task(tid)
        elif t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID, DownloadStatus.CANCELLED}: self.dl_manager.retry_task(tid)
        else: self.dl_manager.cancel_task(tid)

    def _draw_sparkline(self, canvas, history: List[float], color: str = ColorPalette.GRAPH_LINE.value):
        if not canvas or not canvas.winfo_exists(): return
        canvas.delete("all")
        if not history or len(history) < 2: return
        try:
            w, h, mx, pts = max(60, int(canvas["width"])), max(20, int(canvas["height"])), max(history) or 1.0, []
            step = w / (len(history) - 1)
            for i, val in enumerate(history): pts.extend([i * step, h - ((val / mx) * (h - 6)) - 3])
            if len(pts) >= 4: canvas.create_line(pts, fill=color, width=1.8, smooth=True)
        except Exception: pass

    def _repair_task_url(self, tid: str):
        t = self.dl_manager.get_task(tid)
        if not t: return
        nu = ask_string(self, "Repair Source URL", f"Enter refreshed URL for:\n{(t.title or '')[:60]}")
        if nu and nu.strip():
            with self.dl_manager.state_lock:
                t.url = t.original_url = nu.strip()
            self.dl_manager.retry_task(tid)

    def _play_media_preview(self, tid: str):
        t = self.dl_manager.get_task(tid)
        if not t or not t.filepath or not os.path.exists(t.filepath): messagebox.showerror("File Not Found", "Output file not found.", parent=self); return
        try:
            if sys.platform == "win32": os.startfile(t.filepath)
            elif sys.platform == "darwin": subprocess.Popen(["open", t.filepath])
            else: subprocess.Popen(["xdg-open", t.filepath])
        except Exception as e: messagebox.showerror("Player Error", str(e), parent=self)

    def update_task_ui(self, tid: str):
        t, ui = self.dl_manager.get_task(tid), self.cards.get(tid)
        if not t or not ui or not ui["card"].winfo_exists(): return
        ui["title"].configure(text=t.title or "Untitled Media")
        ui["meta"].configure(text=f"{detect_platform_label(t.url)}  |  {t.quality_profile}")
        ind = t.status in {DownloadStatus.PROCESSING, DownloadStatus.VERIFYING}
        if ind and not ui["_indeterminate"]:
            ui["_indeterminate"] = True; ui["prog"].configure(mode="indeterminate"); ui["prog"].start(14)
        elif not ind:
            if ui["_indeterminate"]: ui["_indeterminate"] = False; ui["prog"].stop(); ui["prog"].configure(mode="determinate")
            ui["prog"].configure(value=t.progress_float)
        if t.status == DownloadStatus.DOWNLOADING:
            txt = f"{t.stage_label or 'Downloading'} | {t.progress_str} ({format_bytes(t.downloaded_bytes)} / {t.total_bytes_str}) | {t.speed_str} | ETA {t.eta_str}"
            self._draw_sparkline(ui["graph"], t.speed_history)
        elif t.status == DownloadStatus.PROCESSING: txt = f"Processing: {t.stage_label or 'Muxing...'}"
        elif t.status == DownloadStatus.VERIFYING: txt = f"Verifying: {t.stage_label}"
        elif t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID}: txt = f"{t.error_category or 'Error'}: {(t.error_message or 'Failed')[:58]}"
        elif t.status == DownloadStatus.COMPLETED: txt = f"Completed | {t.total_bytes_str} | {t.category}"
        elif t.status == DownloadStatus.SKIPPED: txt = "Skipped | Already in archive"
        else: txt = f"{t.status.value}{(' | ' + t.stage_label) if t.stage_label else ''}"
        cols = {DownloadStatus.DOWNLOADING: ColorPalette.STATUS_DOWNLOADING.value, DownloadStatus.COMPLETED: ColorPalette.STATUS_COMPLETED.value, DownloadStatus.ERROR: ColorPalette.STATUS_ERROR.value, DownloadStatus.INVALID: ColorPalette.STATUS_ERROR.value, DownloadStatus.PAUSED: ColorPalette.STATUS_PAUSED.value, DownloadStatus.CANCELLED: ColorPalette.STATUS_CANCELLED.value, DownloadStatus.PROCESSING: ColorPalette.STATUS_PROCESSING.value, DownloadStatus.VERIFYING: ColorPalette.STATUS_VERIFYING.value, DownloadStatus.SKIPPED: ColorPalette.STATUS_SKIPPED.value}
        ui["status"].configure(text=txt, fg=cols.get(t.status, ThemeColors.TEXT_MUTED))

        b = ui["act"]
        if t.status == DownloadStatus.DOWNLOADING: b.configure(image=IconFactory.get("pause", 16), style="Warning.TButton", state="normal"); ui["act_tip"].set_text("Pause")
        elif t.status == DownloadStatus.PAUSED: b.configure(image=IconFactory.get("play", 16), style="Success.TButton", state="normal"); ui["act_tip"].set_text("Resume")
        elif t.status == DownloadStatus.COMPLETED: b.configure(image=IconFactory.get("done", 16), style="Success.TButton", state="disabled"); ui["act_tip"].set_text("Completed")
        elif t.status == DownloadStatus.SKIPPED: b.configure(image=IconFactory.get("done", 16), style="TButton", state="disabled"); ui["act_tip"].set_text("Skipped")
        elif t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID, DownloadStatus.CANCELLED}: b.configure(image=IconFactory.get("retry", 16), style="Warning.TButton", state="normal"); ui["act_tip"].set_text("Retry")
        else: b.configure(image=IconFactory.get("cancel", 16), style="Danger.TButton", state="normal"); ui["act_tip"].set_text("Cancel")

        bx = ui["extra"]
        if t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID, DownloadStatus.CANCELLED}:
            bx.configure(image=IconFactory.get("repair", 16), command=lambda tid=t.task_id: self._repair_task_url(tid), style="Warning.TButton", state="normal"); ui["extra_tip"].set_text("Repair URL")
        elif t.status == DownloadStatus.COMPLETED and t.filepath and os.path.exists(t.filepath):
            bx.configure(image=IconFactory.get("play", 16), command=lambda tid=t.task_id: self._play_media_preview(tid), style="Success.TButton", state="normal"); ui["extra_tip"].set_text("Play Media")
        elif t.status == DownloadStatus.QUEUED:
            bx.configure(image=IconFactory.get("up", 16), command=lambda tid=t.task_id: self.dl_manager.promote_task(tid), style="Teal.TButton", state="normal"); ui["extra_tip"].set_text("Move to Top of Queue")
        else:
            bx.configure(image=IconFactory.get("play", 16), style="Icon.TButton", state="disabled"); ui["extra_tip"].set_text("Unavailable")

        ui["folder"].configure(state="normal" if (t.filepath and os.path.exists(t.filepath)) else "disabled")
        if t.thumbnail_url and getattr(ui["thumb"], "_loaded_url", None) != t.thumbnail_url: self._load_img_async(t.thumbnail_url, ui["thumb"], size=(96, 54))

    def remove_task_widget(self, tid: str):
        ui = self.cards.pop(tid, None)
        if tid in self.card_order: self.card_order.remove(tid)
        self._last_visible_ids = None
        if ui and ui["card"].winfo_exists(): ui["card"].destroy()
        self.update_status_bar(); self._update_global_progress()

    # -- telemetry / status --

    def update_status_bar(self):
        if not hasattr(self, "dl_manager"): return
        with self.dl_manager.state_lock:
            tasks, active, queued = list(self.dl_manager.tasks.values()), len(self.dl_manager.active_threads), len(self.dl_manager.download_queue)
            sess_b, sched_ts = self.dl_manager.session_bytes_downloaded, self.dl_manager.scheduled_start_ts
        done = sum(1 for t in tasks if t.status == DownloadStatus.COMPLETED)
        errs = sum(1 for t in tasks if t.status in {DownloadStatus.ERROR, DownloadStatus.INVALID})
        spd = sum(t.speed_float for t in tasks if t.status == DownloadStatus.DOWNLOADING)
        spd_s = f"{format_bytes(spd, False)}/s" if spd > 0 else "0 B/s"
        self._global_speed_history.append(spd)
        if len(self._global_speed_history) > 45: self._global_speed_history.pop(0)
        self._draw_sparkline(self.global_speed_canvas, self._global_speed_history)
        sched_s = f"  |  Starts in {format_duration(max(0, int(sched_ts - time.time())))}" if sched_ts is not None else ""
        self.dash_summary_lbl.configure(text=f"Active: {active}  |  Queued: {queued}  |  Completed: {done}  |  Errors: {errs}  |  Speed: {spd_s}  |  Session: {format_bytes(sess_b)}{sched_s}")
        if "dashboard" in self.nav_buttons:
            self.nav_buttons["dashboard"].configure(text=f"  Active Queue ({active + queued})" if (active + queued) else "  Active Queue")
        # Cache disk free-space for 8s: check_space() is a disk syscall that would
        # otherwise run on the GUI thread every heartbeat (stalls on network drives).
        now = time.time()
        if now - getattr(self, "_disk_cache_ts", 0.0) > 8:
            self._disk_cache_ts = now
            self._disk_cache_val = DiskAnalyzer.check_space(self.settings_manager.get("download_path"))[1]
        disk = getattr(self, "_disk_cache_val", "")
        self.side_stats.configure(text=f"Active: {active}  |  Queued: {queued}\nDone: {done}  |  Errors: {errs}\nSpeed: {spd_s}\nSession: {format_bytes(sess_b)}\nDisk: {disk}")

    def _update_global_progress(self):
        if not hasattr(self, "dl_manager"): return
        try:
            with self.dl_manager.state_lock:
                dl = [t for t in self.dl_manager.tasks.values() if t.status == DownloadStatus.DOWNLOADING]
                pr = [t for t in self.dl_manager.tasks.values() if t.status in {DownloadStatus.PROCESSING, DownloadStatus.VERIFYING, DownloadStatus.STARTING}]
            if dl:
                avg = sum(t.progress_float for t in dl) / len(dl); self.title(f"{APP_NAME} v{APP_VERSION} - Downloading ({avg:.1%})")
                if self.dl_manager.taskbar: self.dl_manager.taskbar.set_progress(int(avg * 100), 100, "normal")
            elif pr:
                self.title(f"{APP_NAME} v{APP_VERSION} - Processing...")
                if self.dl_manager.taskbar: self.dl_manager.taskbar.set_progress(0, 100, "indeterminate")
            else:
                self.title(f"{APP_NAME} v{APP_VERSION}")
                if self.dl_manager.taskbar: self.dl_manager.taskbar.set_progress(0, 100, "none")
        except Exception: pass

    def _handle_all_downloads_finished(self):
        act = str(self.settings_manager.get("on_queue_complete") or "notify").lower()
        LoggerSetup.log(f"All queued downloads finished. Action: {act}", "info")
        if act == "open_folder": open_file_location(self.settings_manager.get("download_path"))
        elif act == "notify" and notification:
            try: notification.notify(title=APP_NAME, message="All queued downloads finished!", app_name=APP_NAME, timeout=8)
            except Exception: pass
        elif act in {"sleep", "shutdown"}: self._confirm_power_action(act)

    def _confirm_power_action(self, action: str):
        dlg = tk.Toplevel(self); dlg.title("Scheduled Power Action"); dlg.geometry("400x180")
        dlg.configure(bg=ThemeColors.BG); safe_grab_set(dlg); dlg.transient(self); dlg.resizable(False, False)
        rem, cancelled = {"s": 20}, {"f": False}
        lbl = ttk.Label(dlg, text=f"Queue complete. System will {action} in 20s...", font=(UI_FONT, 13, "bold")); lbl.pack(pady=24)
        ttk.Button(dlg, text="Cancel Power Action", style="Danger.TButton", command=lambda: [cancelled.__setitem__("f", True), dlg.destroy()]).pack(pady=6)

        def tick():
            if cancelled["f"] or not dlg.winfo_exists(): return
            rem["s"] -= 1
            if rem["s"] <= 0:
                dlg.destroy()
                try:
                    if sys.platform == "win32": subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"] if action == "sleep" else ["shutdown", "/s", "/t", "5"])
                    elif sys.platform == "darwin": subprocess.Popen(["pmset", "sleepnow"] if action == "sleep" else ["osascript", "-e", 'tell app "System Events" to shut down'])
                    else: subprocess.Popen(["systemctl", "suspend" if action == "sleep" else "poweroff"])
                except Exception as e: LoggerSetup.log(f"Power action failed: {e}", "error")
                return
            lbl.configure(text=f"Queue complete. System will {action} in {rem['s']}s..."); dlg.after(1000, tick)

        dlg.after(1000, tick)

    # -- thumbnails --

    def _load_img_async(self, url: str, lbl, size: Tuple[int, int] = (96, 54)):
        if not url: return
        with self._thumb_lock:
            cached = self._thumb_cache.get((url, size))
            if cached is not None: self._thumb_cache.move_to_end((url, size))
            # In-flight / failed dedup: progress ticks re-call this ~6x/second;
            # without this, a dead thumbnail URL floods the executor queue and
            # hammers the network for the whole download.
            if cached is None:
                if (url, size) in self._thumb_pending: return
                ft = self._thumb_failed.get((url, size))
                if ft is not None and (time.time() - ft) < 60: return  # negative cache: retry dead URLs at most once/min
                self._thumb_pending.add((url, size))
        if cached is not None: self.run_on_gui_thread(self._apply_pil_to_label, lbl, cached, url); return
        try:
            self.thumbnail_executor.submit(self._fetch_thumb_worker, url, lbl, size)
        except RuntimeError:
            with self._thumb_lock: self._thumb_pending.discard((url, size))

    def _fetch_thumb_worker(self, url: str, lbl, size: Tuple[int, int]):
        try:
            px = self.dl_manager.antibot.get_proxy_url() if hasattr(self, "dl_manager") else None
            proxies = {"http": None, "https": None} if px == "" else ({"http": px, "https": px} if px else None)
            # 'with' releases the urllib3 connection - reading r.raw directly leaks
            # the socket until GC, accumulating FDs across hundreds of cards.
            with requests.get(url, timeout=8, proxies=proxies, stream=True) as r:
                r.raise_for_status()
                data = r.raw.read(10 * 1024 * 1024 + 1, decode_content=True)  # 10 MB cap
            if len(data) > 10 * 1024 * 1024: raise ValueError("Thumbnail too large")
            resample = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.BICUBIC)
            pil_img = Image.open(BytesIO(data)).convert("RGBA"); pil_img.thumbnail(size, resample)
            with self._thumb_lock:
                self._thumb_cache[(url, size)] = pil_img; self._thumb_cache.move_to_end((url, size))
                while len(self._thumb_cache) > 80: self._thumb_cache.popitem(last=False)
            self.run_on_gui_thread(self._apply_pil_to_label, lbl, pil_img, url)
        except Exception:
            with self._thumb_lock:
                self._thumb_failed[(url, size)] = time.time()
                # Evict the oldest ~100 instead of wiping all 500 (a full clear
                # re-enables a burst of re-fetches of known-dead URLs).
                if len(self._thumb_failed) > 500:
                    for k in sorted(self._thumb_failed, key=self._thumb_failed.get)[:100]:
                        self._thumb_failed.pop(k, None)
        finally:
            with self._thumb_lock: self._thumb_pending.discard((url, size))

    def _apply_pil_to_label(self, lbl, pil_img, url: str):
        try:
            if not lbl or not lbl.winfo_exists(): return
            photo = ImageTk.PhotoImage(pil_img)
            lbl._photo = photo; lbl._loaded_url = url
            lbl.configure(image=photo, text="", width=pil_img.width, height=pil_img.height)
        except Exception: pass

    # -- logs --

    def _flush_logs_to_ui(self):
        items, latest = LoggerSetup.get_records(after_seq=self._last_log_seq, level_filter=self.log_level_var.get(), search=self.log_search_ent.get().strip())
        self._last_log_seq = latest
        if not items: return
        try:
            self.log_txt.configure(state="normal")
            for rec in items: self.log_txt.insert("end", rec["formatted"] + "\n", rec["level"])
            lc = int(self.log_txt.index("end-1c").split(".")[0])
            if lc > 2500: self.log_txt.delete("1.0", f"{lc - 2000}.0")
            if self.log_autoscroll_var.get(): self.log_txt.see("end")
            self.log_txt.configure(state="disabled")
        except Exception: pass

    def _refresh_logs_full(self):
        self._last_log_seq = 0
        try: self.log_txt.configure(state="normal"); self.log_txt.delete("1.0", "end"); self.log_txt.configure(state="disabled")
        except Exception: pass
        self._flush_logs_to_ui()

    def _clear_logs(self):
        LoggerSetup.clear(); self._refresh_logs_full()

    def _export_logs(self):
        dest = filedialog.asksaveasfilename(parent=self, defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialfile="sina_fusion_logs.txt")
        if dest:
            try:
                recs, _ = LoggerSetup.get_records(after_seq=0, level_filter="ALL", search="")
                Path(dest).write_text("\n".join(r["formatted"] for r in recs) + "\n", encoding="utf-8")
                messagebox.showinfo("Exported", f"Exported {len(recs)} log entries.", parent=self)
            except Exception as e: messagebox.showerror("Export Error", str(e), parent=self)

    def _copy_logs(self):
        """Copy the currently-shown log entries (honoring level filter + search)
        to the system clipboard so they can be pasted into a chat/issue report."""
        try:
            lvl = self.log_level_var.get() if hasattr(self, "log_level_var") else "ALL"
            q = self.log_search_ent.get() if hasattr(self, "log_search_ent") else ""
            recs, _ = LoggerSetup.get_records(after_seq=0, level_filter=lvl, search=q)
            text = "\n".join(r["formatted"] for r in recs)
            if not text:
                text = "(no log entries match the current filter)"
            self.clipboard_clear(); self.clipboard_append(text)
            # Non-blocking feedback: flash the button label, then restore it.
            btn = getattr(self, "_copy_logs_btn", None)
            if btn is not None:
                btn.configure(text=f"Copied {len(recs)}")
                self.after(1600, lambda: btn.configure(text="Copy Logs") if btn.winfo_exists() else None)
            LoggerSetup.log(f"Copied {len(recs)} log entries to clipboard (filter={lvl}, search='{q}').", "debug")
        except Exception as e:
            messagebox.showerror("Copy Error", str(e), parent=self)

    # -- settings / close --

    def _open_settings(self):
        # Single instance: two Settings windows would hold stale snapshots and
        # last-save-wins would silently discard the other's edits.
        existing = getattr(self, "_settings_win", None)
        if existing is not None and existing.winfo_exists():
            existing.lift(); existing.focus_set(); return
        self._settings_win = SettingsWindow(self, self.settings_manager, self._on_settings_applied)

    def _open_diagnostics(self):
        existing = getattr(self, "_diag_win", None)
        if existing is not None and existing.winfo_exists():
            existing.lift(); existing.focus_set(); return
        self._diag_win = DiagnosticsDialog(self, self.settings_manager)

    def _on_settings_applied(self):
        global UI_FONT
        prev_theme, prev_font = ThemeColors.mode, UI_FONT
        ThemeColors.set_mode(self.settings_manager.get("theme"))
        UI_FONT = self.settings_manager.get("font_family") or ("Segoe UI" if sys.platform == "win32" else "Arial")
        cur_lim = safe_int(self.settings_manager.get("global_speed_limit_kbps"), 0, 0, 1048576)
        # Only rebuild the layout when the theme/font actually changed. Rebuilding
        # on every save would wipe the user's batch list / URL box / log view.
        if ThemeColors.mode != prev_theme or UI_FONT != prev_font:
            self._rebuild_ui()
        self.speed_limit_var.set(next((k for k, v in SPEED_LIMIT_CHOICES.items() if v == cur_lim), "Unlimited"))
        self.update_status_bar(); LoggerSetup.log("Runtime settings synchronized.", "info")

    def _on_close(self):
        if self.settings_manager.get("close_to_tray") and Icon is not None:
            if self._tray_icon is not None:
                self.withdraw(); return
            img = Image.new("RGB", (64, 64), (14, 165, 233)); ImageDraw.Draw(img).text((16, 20), "SF", fill="white")

            def show_app(icon, _item=None):
                try: icon.stop()
                except Exception: pass
                self._tray_icon = None; self.run_on_gui_thread(lambda: [self.deiconify(), self.lift()])

            def exit_app(icon, _item=None):
                try: icon.stop()
                except Exception: pass
                self._tray_icon = None; self.run_on_gui_thread(self.quit_app)

            # Build/start the tray icon FIRST; only hide the window once it exists.
            # If the tray backend fails, exit normally instead of leaving an
            # unreachable hidden window (the single-instance mutex blocks relaunch).
            try:
                icon = Icon("SF", image=img, title=APP_NAME, menu=(item("Show Window", show_app, default=True), item("Exit", exit_app)))
                threading.Thread(target=icon.run, name="TrayIcon", daemon=True).start()
                self._tray_icon = icon
                self.withdraw()
            except Exception as e:
                LoggerSetup.log(f"Tray icon unavailable ({e}); exiting normally.", "warning")
                self._tray_icon = None
                self.quit_app()
        else:
            with self.dl_manager.state_lock:
                busy = any(t.status in {DownloadStatus.QUEUED, DownloadStatus.STARTING, DownloadStatus.DOWNLOADING, DownloadStatus.PROCESSING, DownloadStatus.VERIFYING} for t in self.dl_manager.tasks.values())
            if busy and not messagebox.askyesno("Exit Confirmation", "Downloads are still active or queued.\nExit anyway? Active downloads will be stopped.", parent=self):
                return
            self.quit_app()

    def quit_app(self):
        for fn in (
            lambda: self._tray_icon.stop() if self._tray_icon is not None else None,
            lambda: DoHResolver.configure(False, ""),
            lambda: self.settings_manager.save(),
            lambda: self.dl_manager.shutdown() if hasattr(self, "dl_manager") else None,
            lambda: self.cookie_bridge.stop() if hasattr(self, "cookie_bridge") else None,
            lambda: self.thumbnail_executor.shutdown(wait=False, cancel_futures=True),
            self.quit,
            self.destroy,
        ):
            try: fn()
            except Exception: pass


# --- Self-test, single-instance guard & hardened entry point ---

def assert_(cond: bool):
    if not cond:
        raise AssertionError("assertion failed")


def _check_task_roundtrip():
    t = DownloadTask(task_id="t1", url="https://youtu.be/x", ydl_opts={"format": "best", "logger": object()}, download_type="Video", title="Test")
    t.status = DownloadStatus.PAUSED; t.progress_float = 0.4; t.downloaded_bytes = 1000
    d = json.loads(json.dumps(t.to_dict()))
    assert_("logger" not in d["ydl_opts"])
    t2 = DownloadTask.from_dict(d)
    assert_(t2.url == t.url and t2.status == DownloadStatus.PAUSED and t2.title == "Test")
    assert_(abs(t2.progress_float - 0.4) < 1e-9 and t2.downloaded_bytes == 1000)


def _check_compact_info():
    info = {"id": "x", "title": "T", "formats": [{"url": "u"}], "bad": object()}
    c = DownloadTask.compact_info_dict(info)
    assert_(c.get("id") == "x" and "formats" not in c and "bad" not in c)
    json.dumps(c)


def _check_cookie_crypto():
    assert_(BrowserCookieExtractor._decrypt_value(b"plain", None) == "plain")
    assert_(BrowserCookieExtractor._decrypt_value(b"v20xxxx", None) is None)
    if HAS_CRYPTO:
        key = get_random_bytes(32); nonce = get_random_bytes(12)
        c = AES.new(key, AES.MODE_GCM, nonce=nonce)
        ct, tag = c.encrypt_and_digest(b"hello-cookie")
        ev = b"v10" + nonce + ct + tag
        assert_(BrowserCookieExtractor._decrypt_value(ev, key) == "hello-cookie")
        assert_(BrowserCookieExtractor._decrypt_value(ev, None) is None)


def _run_selftest() -> int:
    """Headless deterministic checks of core logic (no GUI, no network)."""
    import tempfile
    failures: List[str] = []

    def check(name: str, fn: Callable[[], None]):
        try:
            fn(); print(f"[PASS] {name}")
        except Exception as e:
            failures.append(name); print(f"[FAIL] {name}: {e}")

    def expect_raises(exc, fn):
        try:
            fn()
        except exc:
            return
        raise AssertionError(f"expected {exc.__name__} to be raised")

    check("format_bytes", lambda: (
        assert_(format_bytes(0) in ("0 B", "0 Bytes")), assert_(format_bytes(None) == "N/A"),
        assert_("KiB" in format_bytes(1536)), assert_("MiB" in format_bytes(5 * 1024 * 1024))))
    check("format_duration", lambda: (
        assert_(format_duration(3661) == "01:01:01"), assert_(format_duration(65) == "01:05"),
        assert_(format_duration(None) == "N/A")))
    check("format_count robust", lambda: (
        assert_(format_count("1234567") == "1,234,567"), assert_(format_count(42) == "42"),
        assert_(format_count(None) == "0")))
    check("timestamp parsing", lambda: (
        assert_(parse_timestamp_to_seconds("90") == 90.0),
        assert_(parse_timestamp_to_seconds("01:30") == 90.0),
        assert_(parse_timestamp_to_seconds("01:01:01") == 3661.0),
        assert_(parse_timestamp_to_seconds("") is None)))
    check("timestamp validation", lambda: (
        expect_raises(ValueError, lambda: parse_timestamp_to_seconds("01:75")),
        expect_raises(ValueError, lambda: parse_timestamp_to_seconds("01:61:00")),
        expect_raises(ValueError, lambda: parse_timestamp_to_seconds("abc")),
        expect_raises(ValueError, lambda: parse_timestamp_to_seconds("-5"))))
    check("index selection", lambda: (
        assert_(parse_index_selection("1-3, 5", 10) == [1, 2, 3, 5]),
        assert_(parse_index_selection("2-1", 10) == []),
        expect_raises(ValueError, lambda: parse_index_selection("x", 10))))
    check("url extraction", lambda: assert_(
        extract_urls_from_text("see https://a.com/x, and https://b.com/y.") == ["https://a.com/x", "https://b.com/y"]))
    check("playlist param strip", lambda: assert_(
        strip_playlist_query_params("https://www.youtube.com/watch?v=abc&list=PL1&index=2") == "https://www.youtube.com/watch?v=abc"))
    check("filename sanitize", lambda: assert_(
        not re.search(r'[<>:"/\\|?*]', sanitize_filename_part('a<b>c:d"e/f\\g|h?i*j'))))
    check("template escape", lambda: assert_(escape_ytdlp_template_literal("100%") == "100%%"))
    check("platform detection", lambda: (
        assert_(detect_platform_label("https://www.youtube.com/playlist?list=PL1") == "YouTube Playlist"),
        assert_(detect_platform_label("https://www.youtube.com/shorts/xyz") == "YouTube Shorts"),
        assert_(detect_platform_label("https://music.youtube.com/watch?v=x") == "YouTube Music"),
        assert_(detect_platform_label("https://www.instagram.com/reel/abc/") == "Instagram")))
    check("media url heuristic", lambda: (
        assert_(is_likely_media_url("https://youtu.be/abc")),
        assert_(not is_likely_media_url("https://example.com/page"))))
    check("error classifier", lambda: (
        assert_(ErrorClassifier.classify("HTTP Error 429: Too Many Requests") == ErrorCategory.RATE_LIMITED),
        assert_(ErrorClassifier.classify("Sign in to confirm you're not a bot") == ErrorCategory.NEEDS_COOKIES),
        assert_(ErrorClassifier.classify("Requested range not satisfiable") == ErrorCategory.RESUME_MISMATCH),
        assert_(ErrorClassifier.classify("ffmpeg not found") == ErrorCategory.FFMPEG),
        assert_(ErrorClassifier.classify("Download aborted by user") == ErrorCategory.CANCELLED)))
    check("task serialization roundtrip", _check_task_roundtrip)
    check("compact info dict", _check_compact_info)
    check("cookie value decryption (DPAPI/AES-GCM logic)", _check_cookie_crypto)

    def _check_crypto():
        with tempfile.TemporaryDirectory() as td:
            sm = SecurityManager(str(Path(td) / "test.key"))
            secret = "p@ssw0rd-یونیکد-123"
            enc = sm.encrypt(secret)
            if HAS_CRYPTO:
                assert_(enc.startswith("enc:v2:"))
            assert_(sm.decrypt(enc) == secret)

    def _check_settings():
        with tempfile.TemporaryDirectory() as td:
            sf = str(Path(td) / "settings.json")
            sm = SettingsManager(sf)
            assert_(sm.get("max_concurrent_downloads") == 2)
            sm.set("max_concurrent_downloads", "999")
            sm.normalize_and_save()
            assert_(sm.get("max_concurrent_downloads") == 8)
            sm2 = SettingsManager(sf)
            assert_(sm2.get("max_concurrent_downloads") == 8)

    check("crypto roundtrip (AES-GCM)", _check_crypto)
    check("settings normalize + persistence", _check_settings)

    print("-" * 50)
    if failures:
        print(f"SELFTEST FAILED: {len(failures)} check(s): {', '.join(failures)}")
        return 1
    print("SELFTEST OK: all checks passed.")
    return 0


_INSTANCE_MUTEX = None
_APP_REF: Optional["SinaEnterpriseApp"] = None


def _single_instance_state() -> str:
    """Windows named-mutex guard: prevents two instances running at once."""
    global _INSTANCE_MUTEX
    if sys.platform != "win32":
        return "ok"
    try:
        import ctypes
        # use_last_error=True + get_last_error() captures the thread last-error
        # atomically at call time; plain windll.GetLastError() can be clobbered
        # by intervening ctypes/Win32 calls and miss ERROR_ALREADY_EXISTS.
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        _INSTANCE_MUTEX = k32.CreateMutexW(None, False, "Local\\SinaFusionDownloader_SingleInstance")
        if ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
            return "exists"
    except Exception:
        pass
    return "ok"


def _global_excepthook(exc_type, exc_value, exc_tb):
    try:
        LoggerSetup.log("UNHANDLED EXCEPTION:\n" + "".join(traceback.format_exception(exc_type, exc_value, exc_tb)), "error")
    except Exception:
        pass
    try:
        parent = _APP_REF if (_APP_REF is not None and _APP_REF.winfo_exists()) else None
        if parent is None:
            # Reuse the existing default root if one is alive instead of spawning
            # a second Tk() (which would orphan the first interpreter).
            r = tkinter._default_root if getattr(tkinter, "_default_root", None) is not None else tkinter.Tk()
            r.withdraw()
            messagebox.showerror("Unexpected Error", f"{exc_type.__name__}: {exc_value}\n\nDetails were written to the log file.")
            if getattr(tkinter, "_default_root", None) is None:
                r.destroy()
        else:
            messagebox.showerror("Unexpected Error", f"{exc_type.__name__}: {exc_value}\n\nDetails were written to System Logs.", parent=parent)
    except Exception:
        pass


def _thread_excepthook(args):
    # Worker-thread exceptions go to threading.excepthook, NOT sys.excepthook.
    # Log them so background failures are not lost to stderr only.
    try:
        LoggerSetup.log("UNHANDLED THREAD EXCEPTION:\n" + "".join(traceback.format_exception(args.exc_type, args.exc_value, args.exc_traceback)), "error")
    except Exception:
        pass


def main() -> int:
    global _APP_REF
    if "--version" in sys.argv:
        print(f"{APP_NAME} v{APP_VERSION}"); return 0
    if "--selftest" in sys.argv:
        return _run_selftest()
    if sys.platform == "win32":
        try:
            from ctypes import windll
            try: windll.shcore.SetProcessDpiAwareness(2)
            except Exception: windll.shcore.SetProcessDpiAwareness(1)
        except Exception: pass
        if _single_instance_state() == "exists":
            try:
                r = tkinter.Tk(); r.withdraw()
                messagebox.showinfo(APP_NAME, "SINA Fusion Downloader is already running.\nCheck the taskbar or system tray.")
                r.destroy()
            except Exception: pass
            return 0
    sys.excepthook = _global_excepthook
    threading.excepthook = _thread_excepthook
    try:
        app = SinaEnterpriseApp(); _APP_REF = app
        app.mainloop()
    except Exception as e:
        try: LoggerSetup.log(f"Fatal startup error: {e}", "error", exc_info=True)
        except Exception: pass
        try:
            r = tkinter._default_root if getattr(tkinter, "_default_root", None) is not None else tkinter.Tk()
            r.withdraw()
            messagebox.showerror("Startup Failed", f"{e}\n\nSee logs folder for details.")
            if getattr(tkinter, "_default_root", None) is None:
                r.destroy()
        except Exception: pass
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())