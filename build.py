#!/usr/bin/env python3
"""Build index.html — pre-render all MD to inline HTML, zero JS deps, guaranteed to work."""
from pathlib import Path
from html import escape
import json, re

ROOT = Path(__file__).resolve().parent
PAGES_DIR = ROOT / "pages"

# ---- Minimal Markdown to HTML ----
def md_to_html(text):
    """Pure Python MD→HTML with callout/highlight/table support."""
    lines = text.split('\n')
    out = []
    i = 0
    in_code, code_lang, code_buf = False, '', []
    in_table, table_rows = False, []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows: return
        h = '<div class="table-wrap"><table>\n<thead><tr>'
        for c in table_rows[0]: h += f'<th>{_inline(c)}</th>'
        h += '</tr></thead>\n<tbody>'
        for row in table_rows[1:]:
            h += '<tr>'
            for c in row: h += f'<td>{_inline(c)}</td>'
            h += '</tr>'
        h += '</tbody></table></div>'
        out.append(h); table_rows = []; in_table = False

    def flush_list():
        nonlocal in_list, list_data
        if not list_data: return
        out.append(f'<{in_list}>\n' + '\n'.join(f'<li>{x}</li>' for x in list_data) + f'\n</{in_list}>')
        list_data = []; in_list = None

    in_list, list_data = None, []

    while i < len(lines):
        line = lines[i]

        if line.strip().startswith('```'):
            if not in_code:
                flush_list(); flush_table()
                in_code = True; code_lang = line.strip()[3:].strip(); code_buf = []
            else:
                in_code = False
                lang_attr = f' class="language-{escape(code_lang)}"' if code_lang else ''
                out.append(f'<pre><code{lang_attr}>{escape("\n".join(code_buf))}</code></pre>')
                code_buf = []
            i += 1; continue

        if in_code:
            code_buf.append(line); i += 1; continue

        if '|' in line and line.strip().startswith('|'):
            flush_list()
            if re.match(r'^\|[\s\-:|]+\|$', line.strip()): i += 1; continue
            cells = [c.strip() for c in line.strip().split('|')[1:-1]]
            if not in_table: in_table = True; table_rows = []
            table_rows.append(cells); i += 1; continue
        elif in_table:
            flush_table()

        if not line.strip():
            flush_list(); i += 1; continue

        if re.match(r'^[-*_]{3,}\s*$', line.strip()):
            flush_list(); out.append('<hr>'); i += 1; continue

        h_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h_match:
            flush_list()
            level = len(h_match.group(1)); text = h_match.group(2).strip()
            id_match = re.search(r'\{#([\w\-]+)\}\s*$', text)
            if id_match: text = text[:id_match.start()].strip(); aid = id_match.group(1)
            else: aid = re.sub(r'[^\w\s\u0600-\u06ff-]','',text).strip().replace(' ','-').lower() or 's'
            out.append(f'<h{level} id="{aid}">{_inline(text)}</h{level}>'); i += 1; continue

        if line.startswith('> '):
            flush_list()
            bq = []
            while i < len(lines) and lines[i].startswith('> '):
                bq.append(lines[i][2:]); i += 1
            out.append(f'<blockquote>{_inline(" ".join(bq))}</blockquote>'); continue

        ul = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if ul:
            if in_list != 'ul': flush_list(); in_list = 'ul'
            list_data.append(_inline(ul.group(2))); i += 1; continue

        ol = re.match(r'^(\s*)\d+[.)]\s+(.+)$', line)
        if ol:
            if in_list != 'ol': flush_list(); in_list = 'ol'
            list_data.append(_inline(ol.group(2))); i += 1; continue

        # Callout
        cm = re.match(r'^:::(info|warn|danger|success|decision)\s*(.*)$', line)
        if cm:
            flush_list(); flush_table();
            ct = cm.group(1); ctitle = cm.group(2).strip()
            cbody = []; i += 1
            while i < len(lines) and not lines[i].strip().startswith(':::'):
                cbody.append(lines[i]); i += 1
            i += 1
            icons = {'info':'i-info','warn':'i-warn','danger':'i-danger','success':'i-success','decision':'i-warn'}
            defaults = {'info':'معلومة','warn':'تنبيه','danger':'خطر','success':'تم بنجاح','decision':'قرار'}
            title = ctitle or defaults.get(ct, '')
            inner = md_to_html('\n'.join(cbody))
            out.append(f'<aside class="callout callout-{ct}"><svg class="callout-icon" viewBox="0 0 24 24"><use href="#{icons.get(ct,"i-info")}"/></svg><div class="callout-body"><p class="callout-title">{title}</p>{inner}</div></aside>')
            continue

        # Highlight
        hm = re.match(r'^!!!\s+(.+)$', line)
        if hm:
            flush_list(); flush_table()
            label = hm.group(1); hl = []; i += 1
            while i < len(lines) and lines[i].strip():
                hl.append(lines[i]); i += 1
            out.append(f'<div class="highlight"><span class="highlight-label">{label}</span>{md_to_html("\n".join(hl))}</div>')
            continue

        # Collapsible
        dm = re.match(r'^\?\?\?\s+(.+)$', line)
        if dm:
            flush_list(); flush_table()
            summary = dm.group(1); db = []; i += 1
            while i < len(lines) and lines[i].strip():
                db.append(lines[i]); i += 1
            out.append(f'<details class="collapsible"><summary>{summary}</summary><div class="collapsible-body">{md_to_html("\n".join(db))}</div></details>')
            continue

        flush_list(); flush_table()
        out.append(f'<p>{_inline(line)}</p>'); i += 1

    flush_list(); flush_table()
    return '\n'.join(out)

def _inline(text):
    # Escape HTML first, then apply markdown on safe text
    text = escape(text)
    # Now unescape the markdown syntax we want to convert
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    return text

# ---- Template ----
TPL = '''<!DOCTYPE html>
<html lang="ar" dir="rtl" data-theme="light">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>موسوعة هيرميس</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#FAFAF7;--surface:#FFF;--surface-2:#F5F5F0;--text:#1A1A1A;--text-muted:#4A4A45;--text-subtle:#6B6B66;--accent:#D97757;--accent-soft:#FBEEE6;--accent-border:#F0D5C4;--accent-strong:#A85533;--border:#E5E4DC;--border-strong:#CDCDC4;--code-bg:#F5F2EC;--code-text:#2A2A2A;--info:#2563EB;--info-soft:#EFF6FF;--info-border:#BFDBFE;--warn:#B45309;--warn-soft:#FFFBEB;--warn-border:#FDE68A;--danger:#B91C1C;--danger-soft:#FEF2F2;--danger-border:#FECACA;--success:#047857;--success-soft:#ECFDF5;--success-border:#A7F3D0;--radius:12px;--radius-sm:8px;--shadow-sm:0 1px 2px rgba(0,0,0,.04);--shadow-lg:0 8px 24px rgba(0,0,0,.1);--font-sans:'Noto Sans Arabic','Inter',sans-serif;--font-mono:'JetBrains Mono',monospace}
[data-theme="dark"]{--bg:#1A1714;--surface:#221E1A;--surface-2:#2A2520;--text:#F5F0E8;--text-muted:#C8C0B6;--text-subtle:#9A938A;--accent:#E89572;--accent-soft:#3A2A22;--accent-border:#5A3D2E;--accent-strong:#F5B493;--border:#2E2924;--border-strong:#463F38;--code-bg:#1E1B17;--code-text:#E8E2D8;--info:#93C5FD;--info-soft:#1E2A3D;--info-border:#2A4365;--warn:#FBBF24;--warn-soft:#332817;--warn-border:#5C4520;--danger:#FCA5A5;--danger-soft:#3A1F1F;--danger-border:#5C2A2A;--success:#6EE7B7;--success-soft:#1A3329;--success-border:#1F5C45}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:70px}
body{margin:0;font-family:var(--font-sans);background:var(--bg);color:var(--text);line-height:1.75;font-size:16px;-webkit-font-smoothing:antialiased}
::selection{background:var(--accent-soft);color:var(--accent-strong)}
.icon{display:inline-block;flex-shrink:0;vertical-align:middle;stroke:currentColor;fill:none}
.topbar{position:sticky;top:0;z-index:100;background:rgba(250,250,247,.85);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--border)}
[data-theme="dark"] .topbar{background:rgba(26,23,20,.85)}
.topbar-inner{max-width:1280px;margin:0 auto;padding:10px 20px;display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:10px;font-weight:600;font-size:14px}
.brand-dot{width:10px;height:10px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px var(--accent-soft);animation:pulse 2.8s infinite}
.brand-logo{height:28px;width:auto;vertical-align:middle;margin-inline-start:4px}
@keyframes pulse{0%,100%{box-shadow:0 0 0 4px var(--accent-soft)}50%{box-shadow:0 0 0 7px transparent}}
.topbar-actions{display:flex;gap:6px}
.btn{width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--border);background:var(--surface);color:var(--text-muted);border-radius:var(--radius-sm);cursor:pointer;padding:0}
.btn .icon{width:18px;height:18px;stroke-width:2}
.layout{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:260px 1fr;gap:48px;padding:32px 24px 96px}
.content{min-width:0}
.sidebar{position:sticky;top:80px;align-self:start;max-height:calc(100vh-100px);overflow-y:auto;padding-inline-end:8px}
.sidebar-title{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:var(--text-subtle);margin:0 0 4px;padding:0 14px}
.sidebar-section{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:var(--text-subtle);padding:16px 14px 6px;margin:0}
.sidebar-nav{display:flex;flex-direction:column;gap:2px}
.sidebar-nav a{display:flex;align-items:center;min-height:36px;padding:8px 14px;color:var(--text-muted);text-decoration:none;font-size:13.5px;border-inline-start:2px solid transparent;border-radius:0 var(--radius-sm) var(--radius-sm) 0;transition:color .15s,background .15s,border-color .15s;cursor:pointer}
.sidebar-nav a.active{color:var(--accent);border-inline-start-color:var(--accent);background:var(--accent-soft);font-weight:500}
.page{display:none}
.page.active{display:block}
.doc-header{margin-bottom:40px;padding-bottom:24px;border-bottom:1px solid var(--border)}
.doc-eyebrow{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;background:var(--accent-soft);color:var(--accent-strong);border:1px solid var(--accent-border);border-radius:999px;font-size:12px;font-weight:500;margin-bottom:16px}
.doc-title{font-size:clamp(28px,4vw,40px);font-weight:700;line-height:1.15;margin:0 0 12px}
.doc-subtitle{font-size:clamp(15px,1.5vw,18px);color:var(--text-muted);margin:0 0 20px;max-width:75ch}
.doc-meta{display:flex;flex-wrap:wrap;gap:16px;font-size:13px;color:var(--text-subtle)}
.doc-meta .icon{width:14px;height:14px;stroke-width:2}
.content h2{font-size:26px;font-weight:600;margin:56px 0 16px;padding-top:8px;scroll-margin-top:80px}
.content h3{font-size:19px;font-weight:600;margin:36px 0 12px;scroll-margin-top:80px}
.content h1{font-size:32px;font-weight:700;margin:40px 0 16px;scroll-margin-top:80px}
.content p,.content li,.content blockquote{max-width:75ch;overflow-wrap:anywhere}
.content p{margin:0 0 16px}
.content a{color:var(--accent);text-decoration:none;border-bottom:1px solid var(--accent-border)}
.content ul,.content ol{padding-inline-start:24px;margin:0 0 16px}
.content li{margin:4px 0}
.content strong{color:var(--text);font-weight:600}
.content hr{border:none;border-top:1px solid var(--border);margin:40px 0}
.content code{font-family:var(--font-mono);background:var(--code-bg);padding:2px 6px;border-radius:4px;font-size:.88em;color:var(--code-text);border:1px solid var(--border);direction:ltr;unicode-bidi:embed;max-width:100%;overflow-wrap:anywhere;word-break:break-all}
.content pre{background:var(--code-bg);border:1px solid var(--border);border-radius:var(--radius);padding:16px 20px;overflow-x:auto;font-size:13.5px;line-height:1.6;margin:16px 0;direction:ltr;text-align:left;max-width:100%}
.content pre code{background:none;padding:0;border:none;color:var(--code-text);font-size:inherit}
.callout{display:flex;gap:14px;padding:14px 18px;border-radius:var(--radius);border:1px solid;margin:20px 0;font-size:14.5px;line-height:1.6;max-width:75ch}
.callout-icon{width:20px;height:20px;margin-top:2px;flex-shrink:0}
.callout-body{flex:1}.callout-title{font-weight:600;margin:0 0 4px;font-size:14px}.callout-body p:last-child{margin-bottom:0}
.callout-info{background:var(--info-soft);border-color:var(--info-border)}.callout-info .callout-title,.callout-info .callout-icon{color:var(--info)}
.callout-warn{background:var(--warn-soft);border-color:var(--warn-border)}.callout-warn .callout-title,.callout-warn .callout-icon{color:var(--warn)}
.callout-danger{background:var(--danger-soft);border-color:var(--danger-border)}.callout-danger .callout-title,.callout-danger .callout-icon{color:var(--danger)}
.callout-success{background:var(--success-soft);border-color:var(--success-border)}.callout-success .callout-title,.callout-success .callout-icon{color:var(--success)}
.highlight{background:linear-gradient(135deg,var(--accent-soft),var(--surface-2));border-inline-start:4px solid var(--accent);padding:18px 22px;border-radius:0 var(--radius) var(--radius) 0;margin:24px 0;font-size:16px;max-width:75ch}
.highlight-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--accent-strong);margin-bottom:6px}
details.collapsible{border:1px solid var(--border);border-radius:var(--radius);margin:16px 0;background:var(--surface)}
details.collapsible>summary{cursor:pointer;padding:14px 18px;font-weight:500;list-style:none;display:flex;justify-content:space-between;align-items:center}
details.collapsible>summary::-webkit-details-marker{display:none}
details.collapsible>summary::after{content:"‹";font-size:20px;font-weight:700;color:var(--accent);transition:transform .18s}
details.collapsible[open]>summary::after{transform:rotate(-90deg)}
.collapsible-body{padding:4px 18px 18px;border-top:1px solid var(--border)}
.table-wrap{overflow-x:auto;margin:20px 0;border-radius:var(--radius);border:1px solid var(--border)}
.content table{width:100%;border-collapse:collapse;font-size:14px;background:var(--surface)}
.content th{background:var(--surface-2);font-weight:600;text-align:start;padding:12px 14px;border-bottom:1px solid var(--border);font-size:13px}
.content td{padding:12px 14px;border-bottom:1px solid var(--border);color:var(--text-muted)}
.content tr:last-child td{border-bottom:none}
.content blockquote{margin:20px 0;padding:4px 20px;border-inline-start:3px solid var(--accent-border);color:var(--text-muted);font-style:italic}
.copy-btn{position:absolute;top:8px;right:8px;width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-sm);cursor:pointer;color:var(--text-subtle);opacity:0;transition:opacity .15s;padding:0;z-index:1}
.copy-btn .icon{width:14px;height:14px;stroke-width:2}
.copy-btn.copied{color:var(--success);border-color:var(--success-border);opacity:1}
.content pre{position:relative}
.content pre:hover .copy-btn,.copy-btn:focus-visible{opacity:1}
.doc-footer{margin-top:80px;padding-top:24px;border-top:1px solid var(--border);font-size:13px;color:var(--text-subtle);display:flex;justify-content:space-between;flex-wrap:wrap}
.mobile-menu{display:none!important}
@media(hover:hover){.btn:hover{color:var(--accent);border-color:var(--accent-border);background:var(--accent-soft)}.sidebar-nav a:hover{color:var(--accent);background:var(--accent-soft)}}
@media(max-width:900px){
  .layout{grid-template-columns:1fr;gap:12px;padding:8px 8px 60px}
  .topbar-inner{padding:8px 10px}
  .sidebar{display:none;position:fixed;top:0;right:0;width:min(280px,85vw);height:100dvh;height:100svh;background:var(--surface);z-index:300;padding:16px;box-shadow:var(--shadow-lg);overflow-y:auto;overscroll-behavior:contain}
  .sidebar.open{display:block}
  .mobile-menu{display:inline-flex!important}
  .mobile-close{display:inline-flex!important;width:36px;height:36px;align-items:center;justify-content:center;background:transparent;border:1px solid transparent;border-radius:var(--radius-sm);color:var(--text-muted);cursor:pointer;padding:0;margin-bottom:12px}
  .backdrop{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:250}
  .backdrop.open{display:block}
  body{font-size:15px;overflow-x:hidden}
  .doc-header{margin-bottom:20px;padding-bottom:14px}
  .doc-title{font-size:22px;word-break:break-word}
  .doc-subtitle{font-size:13px;word-break:break-word}
  .doc-eyebrow{font-size:11px;padding:3px 8px;margin-bottom:10px}
  .doc-meta{font-size:11px;gap:8px;flex-wrap:wrap}
  .content h1{font-size:22px;margin:28px 0 10px;word-break:break-word}
  .content h2{font-size:18px;margin:28px 0 10px;padding-top:4px;word-break:break-word}
  .content h3{font-size:15px;margin:20px 0 8px;word-break:break-word}
  .content p,.content li,.content blockquote{max-width:100%;overflow-wrap:anywhere;word-break:break-word;hyphens:auto}
  .content p{margin-bottom:12px}
  .content ul,.content ol{padding-inline-start:20px;margin-bottom:12px}
  .content pre{font-size:11px;padding:10px 12px;margin:10px 0;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--radius-sm)}
  .content pre code{font-size:11px}
  .content code{font-size:.8em;word-break:break-all;max-width:100%;display:inline-block;overflow-wrap:anywhere}
  .table-wrap{margin:12px 0;max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;border-radius:var(--radius-sm)}
  .content table{font-size:11px;min-width:100%}
  .content th,.content td{padding:6px 8px;white-space:nowrap}
  .content th{font-size:11px}
  .content td{font-size:11px}
  .callout{padding:10px 12px;font-size:13px;margin:12px 0;flex-direction:column;gap:8px}
  .callout-icon{width:18px;height:18px}
  .callout-title{font-size:13px}
  .highlight{padding:10px 14px;font-size:13px;margin:12px 0}
  .highlight-label{font-size:10px;margin-bottom:4px}
  .doc-footer{margin-top:32px;padding-top:12px;font-size:11px;flex-direction:column;gap:4px}
  .content blockquote{padding:4px 12px;margin:12px 0;font-size:13px}
  details.collapsible>summary{padding:10px 12px;font-size:13px;min-height:38px}
  details.collapsible>summary::after{font-size:16px}
  .collapsible-body{padding:4px 12px 12px}
  .content img{max-width:100%;height:auto}
  .brand{font-size:13px}
  .brand-dot{width:8px;height:8px}
  .sidebar-section{font-size:10px;padding:12px 14px 4px}
  .sidebar-nav a{font-size:13px;min-height:40px;padding:10px 14px}
  .copy-btn{width:28px;height:28px;opacity:.6;top:6px;right:6px}
  .copy-btn .icon{width:12px;height:12px}
}
@media(min-width:901px){.mobile-menu{display:none!important}.sidebar{display:block!important}}
@media print{.topbar,.sidebar,.backdrop,.mobile-menu{display:none!important}.layout{grid-template-columns:1fr;padding:0}body{background:#fff;color:#000}}
</style>
</head>
<body>
<svg style="position:absolute;width:0;height:0" aria-hidden="true">
<symbol id="i-info" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></symbol>
<symbol id="i-warn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></symbol>
<symbol id="i-danger" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></symbol>
<symbol id="i-success" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></symbol>
<symbol id="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></symbol>
<symbol id="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="18" y2="18"/></symbol>
<symbol id="i-x" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></symbol>
<symbol id="i-file" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></symbol>
<symbol id="i-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></symbol>
</svg>

<header class="topbar"><div class="topbar-inner">
<div class="brand">
<button class="btn mobile-menu" onclick="openSidebar()" aria-label="القائمة"><svg class="icon" viewBox="0 0 24 24"><use href="#i-menu"/></svg></button>
<span class="brand-dot"></span><span>موسوعة هيرميس</span>
</div>
<div class="topbar-actions">
<button class="btn" onclick="toggleTheme()" aria-label="المظهر"><svg class="icon" viewBox="0 0 24 24"><use id="ti" href="#i-moon"/></svg></button>
</div>
</div></header>

<div class="backdrop" id="backdrop" onclick="closeSidebar()"></div>

<div class="layout">
<aside class="sidebar" id="sidebar">
<button class="mobile-close" onclick="closeSidebar()"><svg class="icon" viewBox="0 0 24 24"><use href="#i-x"/></svg></button>
<nav class="sidebar-nav" id="sidebar-nav">
__SIDEBAR__
</nav>
</aside>
<main class="content" id="main">
__PAGES__
</main>
</div>

<script>
function showPage(slug){
  document.querySelectorAll('.page').forEach(function(p){p.classList.remove('active')});
  document.querySelectorAll('.sidebar-nav a').forEach(function(a){a.classList.remove('active')});
  var page=document.getElementById('page-'+slug);
  if(page)page.classList.add('active');
  var link=document.querySelector('.sidebar-nav a[data-slug=\"'+slug+'\"]');
  if(link)link.classList.add('active');
  if(window.matchMedia('(max-width:900px)').matches)closeSidebar();
  window.scrollTo(0,0);
  location.hash=slug;
}
function openSidebar(){document.getElementById('sidebar').classList.add('open');document.getElementById('backdrop').classList.add('open')}
function closeSidebar(){document.getElementById('sidebar').classList.remove('open');document.getElementById('backdrop').classList.remove('open')}
var tk='hw-theme';
function toggleTheme(){var n=(document.documentElement.dataset.theme||'light')==='light'?'dark':'light';document.documentElement.dataset.theme=n;localStorage.setItem(tk,n);document.getElementById('ti').setAttribute('href',n==='dark'?'#i-sun':'#i-moon')}
(function(){
var s=localStorage.getItem(tk);if(s)document.documentElement.dataset.theme=s;
document.getElementById('ti').setAttribute('href',(document.documentElement.dataset.theme||'light')==='dark'?'#i-sun':'#i-moon');
var slug='index';
if(location.hash){var h=location.hash.substring(1);if(document.getElementById('page-'+h))slug=h}
showPage(slug);
window.addEventListener('hashchange',function(){var h=location.hash.substring(1)||'index';showPage(h)});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeSidebar()});
})();
// Copy buttons
function injectCopyButtons(){
  document.querySelectorAll('.content pre').forEach(function(pre){
    if(pre.querySelector('.copy-btn'))return;
    var btn=document.createElement('button');btn.className='copy-btn';btn.setAttribute('aria-label','نسخ الكود');
    btn.innerHTML='<svg class="icon" viewBox="0 0 24 24"><use href="#i-copy"/></svg>';
    btn.onclick=function(){copyCode(this)};
    pre.appendChild(btn);
  });
}
function copyCode(btn){
  var code=(btn.parentNode.querySelector('code')||btn.parentNode).textContent||'';
  navigator.clipboard.writeText(code).then(function(){
    btn.classList.add('copied');
    btn.innerHTML='<svg class="icon" viewBox="0 0 24 24"><use href="#i-check"/></svg>';
    setTimeout(function(){btn.classList.remove('copied');btn.innerHTML='<svg class="icon" viewBox="0 0 24 24"><use href="#i-copy"/></svg>'},1500);
  });
}
injectCopyButtons();
</script>
</body>
</html>'''

# ---- Build ----
def build():
    pages_list = []
    pages_html = []
    sidebar = ''

    # Collect pages
    files = []
    for md_file in sorted(PAGES_DIR.glob("*.md")):
        slug = md_file.stem
        # Read frontmatter
        content = md_file.read_text(encoding='utf-8')
        title = slug; desc = ''; cat = 'عام'; body = content
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                for line in content[3:end].strip().split('\n'):
                    if ':' in line:
                        k, v = line.split(':', 1); k = k.strip(); v = v.strip()
                        if k == 'title': title = v
                        elif k == 'description': desc = v
                        elif k == 'category': cat = v
                body = content[end+3:].strip()
        files.append({'slug':slug,'title':title,'desc':desc,'cat':cat,'body':body})

    # Sort by category then order
    cat_order = {'عام':0,'البدء':1,'متقدم':2,'دعم':3}
    files.sort(key=lambda f: (cat_order.get(f['cat'],99), f['slug']))

    # Build sidebar
    cats = {}
    for f in files:
        c = f['cat']
        if c not in cats: cats[c] = []
        cats[c].append(f)
    for c in sorted(cats, key=lambda x: cat_order.get(x,99)):
        sidebar += f'<p class="sidebar-section">📂 {c}</p>\n'
        for f in cats[c]:
            sidebar += f'<a data-slug="{f["slug"]}" onclick="showPage(\'{f["slug"]}\')">{f["title"]}</a>\n'

    # Build pages HTML
    for f in files:
        html_body = md_to_html(f['body'])
        pages_html.append(f'''
<div class="page" id="page-{f["slug"]}">
<header class="doc-header">
<span class="doc-eyebrow">{f["cat"]}</span>
<h1 class="doc-title">{f["title"]}</h1>
<div class="doc-meta"><span class="doc-meta-item"><svg class="icon" viewBox="0 0 24 24"><use href="#i-file"/></svg> {f["slug"]}.md</span></div>
</header>
{html_body}
<footer class="doc-footer"><span>موسوعة هيرميس</span><span>{f["slug"]}.md</span></footer>
</div>''')

    html = TPL.replace('__SIDEBAR__', sidebar).replace('__PAGES__', '\n'.join(pages_html))
    out = ROOT / 'index.html'
    out.write_text(html, encoding='utf-8')
    print(f'✓ index.html ({len(files)} pages, zero JS deps)')

if __name__ == '__main__':
    build()
