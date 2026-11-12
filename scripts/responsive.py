#!/usr/bin/env python3
"""
Rebuild scalpture-ink/index.html from the bundled source with a mobile-first
responsive layer injected into the template.

Usage:
    python3 scripts/responsive.py            # patch in place
    python3 scripts/responsive.py --check    # report only
"""
import json, re, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'scalpture-ink.html')      # pristine bundled export
OUT = os.path.join(ROOT, 'index.html')


CLASSES = [
    ('<div style="font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:rgba(242,240,238,0.4); font-weight:400;">Johannesburg</div>', '{{REMOVE_JHB}}'),
    ('<p style="margin:26px 0 0; max-width:54ch;', '<p class="si-hero-lede" style="margin:26px 0 0; max-width:54ch;'),
    ('<div style="font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:rgba(242,240,238,0.4); font-weight:400;">Johannesburg</div>',
     '<div class="si-hdr-loc" style="font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:rgba(242,240,238,0.4); font-weight:400;">Johannesburg</div>'),
    ('<div style="display:flex; align-items:center; gap:26px;">\n    <a href="Portfolio.dc.html"',
     '<div class="si-hdr-actions" style="display:flex; align-items:center; gap:26px;">\n    <a class="si-hdr-portfolio" href="Portfolio.dc.html"'),
    ('<a href="#book" style="border:1px solid rgba(242,240,238,0.35); border-radius:999px; padding:13px 26px;',
     '<a class="si-hdr-cta" href="#book" style="border:1px solid rgba(242,240,238,0.35); border-radius:999px; padding:13px 26px;'),
    ('<div style="position:relative; z-index:10; display:grid; grid-template-columns:minmax(0,1fr) auto;',
     '<div class="si-hero-main" style="position:relative; z-index:10; display:grid; grid-template-columns:minmax(0,1fr) auto;'),
    ('<div style="display:flex; flex-direction:column; gap:7px; padding-bottom:22px; min-width:210px;">',
     '<div class="si-hero-tags" style="display:flex; flex-direction:column; gap:7px; padding-bottom:22px; min-width:210px;">'),
    ('<div style="position:relative; z-index:10; display:flex; align-items:flex-end; gap:14px; padding:0 34px 92px;',
     '<div class="si-hero-scroll" style="position:relative; z-index:10; display:flex; align-items:flex-end; gap:14px; padding:0 34px 92px;'),
    ('<div style="display:flex; gap:clamp(26px,3.5vw,60px); border-top:1px solid rgba(242,240,238,0.2);',
     '<div class="si-stats" style="display:flex; gap:clamp(26px,3.5vw,60px); border-top:1px solid rgba(242,240,238,0.2);'),
    ('<div style="display:flex; flex-direction:column; gap:26px; border-left:1px solid rgba(192,131,71,0.55);',
     '<div class="si-bio-col" style="display:flex; flex-direction:column; gap:26px; border-left:1px solid rgba(192,131,71,0.55);'),
    ('<div style="display:grid; grid-template-columns:minmax(0,1fr) minmax(300px, 470px); align-items:end;',
     '<div class="si-bio-grid" style="display:grid; grid-template-columns:minmax(0,1fr) minmax(300px, 470px); align-items:end;'),
    ('<div style="display:grid; grid-template-columns:minmax(0,0.95fr) minmax(0,1.05fr); align-items:center;',
     '<div class="si-tier-grid" style="display:grid; grid-template-columns:minmax(0,0.95fr) minmax(0,1.05fr); align-items:center;'),
    ('<div id="book" style="display:grid;',
     '<div id="book" class="si-book" style="display:grid;'),
    ('<form sc-camel-on-submit="{{ onSubmit }}" style=',
     '<form class="si-book-form" sc-camel-on-submit="{{ onSubmit }}" style='),
    ('<div data-reveal="" style="transition:opacity .8s ease-out, transform .8s ease-out; position:absolute; top:130px; left:34px;',
     '<div class="si-eyebrow-ab" data-reveal="" style="transition:opacity .8s ease-out, transform .8s ease-out; position:absolute; top:130px; left:34px;'),
    ('<div style="position:absolute; top:130px; right:34px; z-index:2; font-family:\'Courier New\', monospace; font-size:10px; letter-spacing:0.24em; text-transform:uppercase; color:rgba(242,240,238,0.5); writing-mode:vertical-rl;">',
     '<div class="si-vertical-credit" style="position:absolute; top:130px; right:34px; z-index:2; font-family:\'Courier New\', monospace; font-size:10px; letter-spacing:0.24em; text-transform:uppercase; color:rgba(242,240,238,0.5); writing-mode:vertical-rl;">'),
    ('<div style="display:flex; gap:2px; height:min(66vh, 620px);">',
     '<div class="si-card-row" style="display:flex; gap:2px; height:min(66vh, 620px);">'),
    ('<div style="display:flex; flex-direction:column; gap:30px; padding:80px 34px 0; max-width:1100px;',
     '<div class="si-quote-wrap" style="display:flex; flex-direction:column; gap:30px; padding:80px 34px 0; max-width:1100px;'),
    ('<div style="display:flex; align-items:baseline; justify-content:space-between; gap:40px; margin-bottom:90px;">',
     '<div class="si-proof-head" style="display:flex; align-items:baseline; justify-content:space-between; gap:40px; margin-bottom:90px;">'),
    ('<div style="display:flex; align-items:center; gap:16px; border-top:1px solid rgba(242,240,238,0.14); padding-top:22px;">',
     '<div class="si-pay-note" style="display:flex; align-items:center; gap:16px; border-top:1px solid rgba(242,240,238,0.14); padding-top:22px;">'),
    ('<nav style="position:fixed; left:0; right:0; bottom:0; z-index:40; display:grid;',
     '<nav class="si-nav" style="position:fixed; left:0; right:0; bottom:0; z-index:40; display:grid;'),
]

REPEATED = [
    ('<div style="flex:1; position:relative; overflow:hidden; background-color:#0e0e0e;',
     '<div class="si-card" style="flex:1; position:relative; overflow:hidden; background-color:#0e0e0e;'),
    ('<div style="position:relative; display:flex; flex-direction:column; gap:10px;">\n          <div style="font-family:Anton',
     '<div class="si-card-title" style="position:relative; display:flex; flex-direction:column; gap:10px;">\n          <div style="font-family:Anton'),
    ('<div data-tier="', '<div class="si-tier-row" data-tier="'),
    ('<span style="font-family:Anton, sans-serif; font-weight:400; font-size:clamp(19px,1.8vw,30px); line-height:1.05;',
     '<span class="si-tier-name" style="font-family:Anton, sans-serif; font-weight:400; font-size:clamp(19px,1.8vw,30px); line-height:1.05;'),
    ('<div style="scroll-snap-align:start; position:sticky; top:0; height:100vh; display:grid;',
     '<div class="si-step" style="scroll-snap-align:start; position:sticky; top:0; height:100vh; display:grid;'),
    ('<div style="font-family:Archivo, sans-serif; font-weight:100; font-size:clamp(96px, min(18vw, 29vh), 300px);',
     '<div class="si-step-num" style="font-family:Archivo, sans-serif; font-weight:100; font-size:clamp(96px, min(18vw, 29vh), 300px);'),
    ('<div style="display:grid; grid-template-columns:minmax(0,0.95fr) minmax(0,1.05fr); gap:clamp(30px,6vw,90px); border-top:1px solid rgba(10,10,10,0.2);',
     '<div class="si-faq-row" style="display:grid; grid-template-columns:minmax(0,0.95fr) minmax(0,1.05fr); gap:clamp(30px,6vw,90px); border-top:1px solid rgba(10,10,10,0.2);'),
    ('<h3 style="margin:0; font-family:Anton, sans-serif; font-weight:400; font-size:clamp(24px,2.4vw,40px);',
     '<h3 class="si-faq-q" style="margin:0; font-family:Anton, sans-serif; font-weight:400; font-size:clamp(24px,2.4vw,40px);'),
]

def find_script(s, typ):
    """Return (payload_start, payload_end) by decoding the JSON payload properly.

    The bundled page escapes markup inside the payload (so a naive
    s.find('</script>') lands inside the data), therefore we decode with
    json.JSONDecoder and use the byte length it consumed.
    """
    m = re.search(r'<script type="%s">' % re.escape(typ), s)
    if not m:
        raise SystemExit('missing script block: ' + typ)
    start = m.end()
    while s[start].isspace():
        start += 1
    _, consumed = json.JSONDecoder().raw_decode(s, start)
    return start, consumed

def main():
    check = '--check' in sys.argv
    body = open(SRC, encoding='utf-8').read()

    # --- template ---
    tstart, tend = find_script(body, '__bundler/template')
    tpl = json.loads(body[tstart:tend])

    tpl = tpl.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
        '<meta name="theme-color" content="#050505">',
        1)

    tpl = tpl.replace(
        'scroll-snap-type:y proximity;',
        'scroll-snap-type:y proximity; overflow-x:hidden;', 1)

    # Appended inside the last <style> so it wins the cascade.
    MOBILE = r'''

/* Short CTA label only appears on phones */
.si-cta-short { display:none; }

/* ============================================================
   Responsive layer — tablet (<=900px), phone (<=640px), small (<=390px)
   Everything below is additive; desktop styles are untouched.
   ============================================================ */
@media (max-width: 900px) {
  [style*="padding:230px 34px 280px"] { padding:150px 24px 160px !important; }
  [style*="padding:230px 0 280px"]     { padding:150px 0 160px !important; }
  [style*="padding:200px 34px 240px"]  { padding:130px 24px 150px !important; }
  [style*="padding:230px 34px 0"]      { padding:150px 24px 0 !important; }
  [style*="padding:230px 34px 110px"]  { padding:150px 24px 80px !important; }
  [style*="padding:170px 34px 150px"]  { padding:130px 24px 110px !important; }
  [style*="130px 34px 120px"]          { padding:90px 24px 90px !important; }
  .si-card-row {
    display:grid !important; grid-template-columns:repeat(2,minmax(0,1fr)) !important;
    height:auto !important; gap:2px !important;
  }
  .si-card-row > .si-card { min-height:220px; flex:none !important; }
  footer[style*="repeat(4"] { grid-template-columns:repeat(2,minmax(0,1fr)) !important; }
}

@media (max-width: 640px) {
  /* --- base --- */
  html { -webkit-text-size-adjust:100%; }
  body { overflow-x:hidden; }

  /* --- fixed chrome --- */
  .si-hdr {
    padding:14px 18px !important; gap:10px !important;
    background:linear-gradient(180deg, rgba(5,5,5,0.92) 0%, rgba(5,5,5,0) 100%) !important;
  }
  .si-hdr-brand { gap:11px !important; }
  .si-hdr-mark { width:36px !important; height:36px !important; font-size:14px !important; }
  .si-hdr-name { font-size:10px !important; letter-spacing:0.18em !important; }
  .si-hdr-actions { gap:10px !important; }
  .si-hdr-portfolio { display:none !important; }
  .si-cta-full { display:none !important; }
  .si-cta-short { display:inline !important; }
  .si-hdr-cta {
    padding:11px 20px !important; font-size:10px !important;
    letter-spacing:0.18em !important; white-space:nowrap !important;
  }

  /* --- loader --- */
  [data-loader-body] { padding:20px !important; }
  [data-loader-count] { font-size:clamp(38px,13vw,64px) !important; }
  [data-loader-body] > div:nth-child(2) { gap:24px !important; flex-direction:column !important; align-items:flex-start !important; }

  /* --- section rhythm --- */
  section { padding-left:0 !important; padding-right:0 !important; }
  section > * { --gutter:18px; }
  [style*="padding:230px 34px 280px"],
  [style*="padding:230px 0 280px"],
  [style*="padding:200px 34px 240px"],
  [style*="padding:230px 34px 0"],
  [style*="padding:230px 34px 110px"],
  [style*="padding:170px 34px 150px"] {
    padding-top:96px !important; padding-bottom:96px !important;
    padding-left:18px !important; padding-right:18px !important;
  }
  [style*="130px 34px 120px"] { padding:70px 18px !important; }

  /* --- hero --- */
  section[data-screen-label="Hero"] { min-height:100svh !important; }
  .si-hero-main {
    display:flex !important; flex-direction:column !important; align-items:flex-start !important;
    gap:22px !important; padding:84px 18px 20px !important;
  }
  .si-hero-tags {
    display:grid !important; grid-template-columns:1fr 1fr !important;
    gap:6px 14px !important; padding-bottom:0 !important;
    min-width:0 !important; max-width:100% !important;
  }
  .si-hero-tags > div { white-space:normal !important; }
  .si-hero-scroll { padding:0 18px 84px !important; }
  h1[data-drift], h2[data-drift], h3[data-drift] {
    font-size:clamp(34px, 11vw, 56px) !important;
    line-height:1.02 !important;
    max-width:100% !important; overflow-wrap:break-word !important;
  }
  h2[data-drift] { margin-bottom:44px !important; }
  h3[data-drift] { margin-bottom:36px !important; }

  /* --- grids collapse to single column --- */
  [style*="grid-template-columns:minmax(0,1fr) minmax(300px, 470px)"],
  [style*="grid-template-columns:minmax(0,1fr) minmax(0,1fr)"],
  [style*="grid-template-columns:minmax(0,0.95fr) minmax(0,1.05fr)"],
  [style*="grid-template-columns:minmax(0,0.85fr) minmax(0,1.15fr)"],
  [style*="grid-template-columns:repeat(4"],
  [style*="grid-template-columns:repeat(5"] {
    grid-template-columns:minmax(0,1fr) !important;
  }

  /* --- Chapter I: the artist -------------------------------------- */
  /* Real layout change: the section stops being a full-height photo plate
     with absolutely-positioned furniture and becomes a readable editorial
     stack. Everything shares one 18px gutter. */
  #chapter-1 {
    min-height:auto !important;
    padding:120px 18px 96px !important;
    justify-content:flex-start !important;
  }
  #chapter-1 > div[style*="linear-gradient(180deg"] {
    background:linear-gradient(180deg, rgba(5,5,5,0.78) 0%, rgba(5,5,5,0.45) 30%, rgba(5,5,5,0.9) 78%, #050505 100%) !important;
  }

  /* eyebrow: flow into the stack instead of floating over the headline */
  .si-eyebrow-ab {
    position:static !important;
    margin:0 0 26px !important;
    gap:8px !important;
    align-items:flex-start !important;
    max-width:100% !important;
  }
  .si-eyebrow-ab > span:last-child {
    font-size:9.5px !important; letter-spacing:0.16em !important;
    line-height:1.5 !important; white-space:normal !important;
  }

  /* vertical credit is unreadable on a phone — turn it into a byline */
  .si-vertical-credit {
    position:static !important;
    writing-mode:horizontal-tb !important;
    font-size:9px !important; letter-spacing:0.16em !important;
    color:rgba(242,240,238,0.82) !important;
    margin:0 0 14px !important;
    padding-bottom:14px !important;
    border-bottom:1px solid rgba(242,240,238,0.14) !important;
    max-width:100% !important;
  }

  /* legibility scrim behind the text column */
  #chapter-1 > div[style*="position:relative; z-index:2; display:flex; flex-direction:column"]::before {
    content:''; position:absolute; inset:-40px -20px -40px -20px; z-index:-1;
    background:linear-gradient(180deg, rgba(5,5,5,0.72) 0%, rgba(5,5,5,0.86) 40%, rgba(5,5,5,0.94) 100%);
    pointer-events:none;
  }

  /* the section becomes a flex column we control */
  #chapter-1 > div[style*="position:relative; z-index:2; display:flex; flex-direction:column"] {
    gap:30px !important;
  }
  #chapter-1 h2[data-drift] {
    font-size:clamp(38px, 12.5vw, 62px) !important;
    line-height:0.98 !important;
    letter-spacing:0.005em !important;
    margin:0 !important;
    max-width:100% !important;
  }
  #chapter-1 h2[data-drift] span[style*="padding-left:0.12em"] { padding-left:0 !important; }

  /* stats: 3 cells that actually fit, numerals over captions */
  .si-stats {
    display:grid !important;
    grid-template-columns:repeat(3,minmax(0,1fr)) !important;
    gap:0 !important;
    border-top:1px solid rgba(242,240,238,0.2) !important;
    border-bottom:1px solid rgba(242,240,238,0.12) !important;
    padding:20px 0 22px !important;
  }
  .si-stats > div {
    display:flex !important; flex-direction:column !important; gap:8px !important;
    padding:0 10px 0 0 !important;
    border-right:1px solid rgba(242,240,238,0.1) !important;
    min-width:0 !important;
  }
  .si-stats > div:last-child { border-right:0 !important; padding-right:0 !important; }
  .si-stats > div:nth-child(2) { padding-left:12px !important; }
  .si-stats > div:nth-child(3) { padding-left:12px !important; }
  .si-stats > div > div:first-child {
    font-size:clamp(24px,7.5vw,34px) !important; line-height:1 !important;
  }
  .si-stats > div > div:last-child {
    font-size:8px !important; letter-spacing:0.08em !important;
    line-height:1.5 !important; text-transform:uppercase !important;
    white-space:normal !important; overflow-wrap:break-word !important;
    hyphens:auto !important; color:rgba(242,240,238,0.6) !important;
  }
  /* keep the designed line breaks but let them breathe */
  .si-stats br { display:inline !important; }
  .si-stats > div > div:last-child { padding-right:0 !important; }
  .si-stats > div:last-child > div:last-child { padding-right:0 !important; }
  #chapter-1 { padding-right:22px !important; }

  /* bio: accent rule becomes a top rule so nothing hangs off the gutter */
  .si-bio-grid { gap:26px !important; }
  .si-bio-col {
    border-left:0 !important;
    border-top:1px solid rgba(192,131,71,0.55) !important;
    padding:20px 0 0 !important;
    gap:20px !important;
  }
  .si-bio-col > p {
    font-size:14px !important; line-height:1.65 !important;
    color:rgba(242,240,238,0.9) !important;
  }
  .si-bio-col > a {
    align-self:flex-start !important;
    font-size:10px !important; letter-spacing:0.18em !important;
    padding-bottom:7px !important;
  }

  /* --- chapter 1 stats (legacy) --- */
  .si-bio-col > p, .si-bio-col > a { max-width:100% !important; }
  [style*="writing-mode:vertical-rl"] { display:none !important; }

  /* --- treatments --- */
  .si-card-row { grid-template-columns:minmax(0,1fr) !important; }
  .si-card-row > .si-card { min-height:190px !important; }
  .si-card-row > .si-card > .si-card-title { font-size:15px !important; }

  /* --- pricing --- */
  .si-tier-row { gap:12px !important; padding:22px 0 !important; }
  .si-tier-row .si-tier-name { font-size:17px !important; }
  svg[sc-camel-view-box] { max-width:100% !important; }

  /* --- showcase --- */
  [data-showcase] { height:70svh !important; }
  [data-showcase] button { width:48px !important; height:48px !important; }
  [data-showcase] > div[style*="left:34px"] { left:18px !important; }
  [data-showcase] > div[style*="right:34px"] { right:18px !important; }
  [data-showcase] > div[style*="left:34px; right:34px"] { left:18px !important; right:18px !important; }
  .si-quote-wrap { padding:44px 18px 0 !important; }
  p[style*="Instrument Serif"] { font-size:clamp(22px,6.5vw,30px) !important; }

  /* --- proof strip --- */
  [style*="repeat(4"] { gap:18px 14px !important; }
  [style*="repeat(4"] > div > div:first-child { font-size:clamp(34px,10vw,52px) !important; }
  .si-proof-head {
    flex-direction:column !important; align-items:flex-start !important;
    gap:14px !important; margin-bottom:44px !important;
  }

  /* --- process steps --- */
  .si-step {
    height:auto !important; min-height:66svh !important; position:relative !important;
    padding:90px 18px 60px !important; align-items:flex-start !important;
    gap:10px !important;
  }
  .si-step > .si-step-num {
    font-size:clamp(64px,22vw,120px) !important; line-height:1 !important;
  }

  /* --- faq --- */
  .si-faq-row { padding:30px 0 !important; }
  .si-faq-q { font-size:20px !important; }

  /* --- Chapter V: contact & booking ------------------------------- */
  #chapter-5 { padding-left:18px !important; padding-right:18px !important; }
  #chapter-5 h2[data-drift] {
    font-size:clamp(34px, 10.5vw, 52px) !important;
    line-height:1.02 !important; margin-bottom:44px !important;
  }
  #chapter-5 h2[data-drift] span[style*="padding-left"] { padding-left:0 !important; }

  /* the two-column book grid becomes a single readable column */
  .si-book {
    grid-template-columns:minmax(0,1fr) !important;
    gap:34px !important; padding-top:28px !important;
  }
  .si-book > div { min-width:0 !important; max-width:100% !important; }
  .si-book > div > p {
    font-size:14px !important; line-height:1.65 !important; max-width:100% !important;
  }

  /* WhatsApp CTA: full-width, comfortable target */
  .si-book a[href^="https://wa.me"] {
    width:100% !important; max-width:100% !important;
    padding:20px 22px !important; font-size:10.5px !important;
    letter-spacing:0.16em !important; min-height:56px !important;
  }
  .si-book a[href^="https://wa.me"] span { font-size:16px !important; }

  /* phone + email: never break mid-token */
  .si-book a[href^="tel:"] { font-size:19px !important; letter-spacing:0.01em !important; }
  .si-book a[href^="mailto:"] {
    font-size:15px !important; letter-spacing:0 !important;
    word-break:break-all !important; overflow-wrap:anywhere !important;
    max-width:100% !important;
  }

  /* consultation pills: readable, equal, tappable */
  .si-book-form > div:first-child > div:last-child {
    display:flex !important; flex-wrap:wrap !important; gap:8px !important;
  }
  .si-book-form > div:first-child > div:last-child > button {
    flex:1 1 calc(50% - 4px) !important; min-height:52px !important;
    padding:14px 14px !important; font-size:9.5px !important;
    letter-spacing:0.12em !important; line-height:1.35 !important;
    white-space:normal !important; text-align:center !important;
  }
  .si-book-form > div:first-child { padding:20px 0 24px !important; gap:12px !important; }

  /* form rows */
  .si-book-form { border-top:0 !important; }
  .si-book-form input, .si-book-form textarea {
    font-size:16px !important; padding:18px 2px !important; width:100% !important;
  }
  .si-book-form textarea { min-height:88px !important; }
  .si-book-form button[type="submit"] {
    width:100% !important; max-width:100% !important;
    margin-top:24px !important; padding:20px 24px !important;
    font-size:10.5px !important; letter-spacing:0.18em !important;
    min-height:58px !important; text-align:center !important;
  }

  /* footer: two up, everything inside the gutter */
  #chapter-5 footer {
    grid-template-columns:minmax(0,1fr) minmax(0,1fr) !important;
    gap:26px 18px !important;
    margin-top:64px !important;
    padding:30px 0 calc(120px + env(safe-area-inset-bottom)) !important;
    border-top:1px solid rgba(242,240,238,0.14) !important;
  }
  #chapter-5 footer > div { min-width:0 !important; }
  #chapter-5 footer a, #chapter-5 footer div {
    max-width:100% !important; overflow-wrap:break-word !important;
  }
  /* footer headings carry wide tracking that orphans letters in a 2-col grid */
  #chapter-5 footer > div > div:first-child {
    font-size:9px !important; letter-spacing:0.1em !important;
    white-space:nowrap !important;
  }
  #chapter-5 footer > div > div:nth-child(2),
  #chapter-5 footer > div:last-child > div:last-child {
    font-size:12px !important; line-height:1.55 !important;
  }
  #chapter-5 footer > div:last-child { grid-column:1 / -1 !important; }

  /* --- contact (legacy) --- */
  input, textarea, button { font-size:16px !important; }
  form input, form textarea { padding:18px 2px !important; }
  .si-pay-note {
    flex-direction:column !important; align-items:flex-start !important; gap:12px !important;
  }

  /* --- footer --- */


  /* --- chapter nav dock: becomes a compact segmented control --- */
  .si-nav {
    gap:5px !important;
    padding:10px 10px calc(10px + env(safe-area-inset-bottom)) !important;
    background:linear-gradient(180deg, rgba(5,5,5,0) 0%, rgba(5,5,5,0.94) 40%) !important;
  }
  .si-nav > div { gap:5px !important; min-width:0 !important; }
  .si-nav > div > div:first-child {
    font-size:0 !important; letter-spacing:0 !important;
    justify-content:center !important; gap:4px !important;
  }
  .si-nav > div > div:first-child > span:first-child {
    font-size:9px !important; letter-spacing:0.01em !important;
    white-space:nowrap !important; overflow:hidden !important; text-overflow:clip !important;
  }
  .si-nav > div > div:first-child > span:last-child {
    width:3px !important; height:3px !important; flex:none !important;
  }

  /* --- misc --- */
  [data-marker] { display:none !important; }
  [style*="height:100vh; overflow-y:auto"] { scroll-snap-type:none !important; }
  img, video, svg { max-width:100%; }
}


/* ---------- hard guards: no horizontal overflow on phones ---------- */
@media (max-width: 640px) {
  .si-hdr { padding:12px 14px !important; gap:8px !important; }
  .si-hdr > div { gap:10px !important; min-width:0 !important; }
  .si-hdr-actions { flex:none !important; }
  .si-hdr-cta {
    padding:9px 12px !important; font-size:8.5px !important;
    letter-spacing:0.08em !important; white-space:nowrap !important;
  }
  .si-hero-main {
    padding:76px 14px 18px !important;
    display:flex !important; flex-direction:column !important;
    align-items:stretch !important; width:100% !important; max-width:100% !important;
  }
  .si-hero-main > div { min-width:0 !important; max-width:100% !important; }
  .si-hero-lede {
    font-size:13.5px !important; line-height:1.6 !important;
    max-width:100% !important; width:100% !important; margin-top:18px !important;
    overflow-wrap:break-word !important; word-break:normal !important;
    text-wrap:wrap !important; hyphens:auto !important;
  }
  .si-hero-tags {
    grid-template-columns:minmax(0,1fr) !important;
    width:100% !important; max-width:100% !important;
  }
  .si-hero-tags > div {
    white-space:normal !important; word-break:break-word !important;
    font-size:10px !important; letter-spacing:0.14em !important;
  }
  .si-hero-scroll { padding:0 14px 78px !important; }
  .si-hero-scroll > div > div { font-size:10px !important; letter-spacing:0.12em !important; }
  .si-stats { gap:10px !important; }
  .si-stats > div > div:last-child { font-size:8.5px !important; letter-spacing:0.1em !important; }
  .si-stats > div > div:first-child { font-size:clamp(26px,8vw,38px) !important; }
  .si-quote-wrap { padding:36px 14px 0 !important; }
  .si-card-row > .si-card { min-height:170px !important; padding:16px !important; }
  .si-card-title { font-size:13px !important; letter-spacing:0.02em !important; }
  .si-tier-row { grid-template-columns:auto minmax(0,1fr) !important; gap:10px !important; }
  .si-tier-row > span:last-child {
    grid-column:2 !important; font-size:20px !important;
    text-align:left !important; margin-top:4px !important;
  }
  .si-tier-name { font-size:15px !important; }
  .si-proof-head { margin-bottom:34px !important; }
  .si-faq-row { gap:12px !important; padding:26px 0 !important; }
  .si-faq-q { font-size:18px !important; }
  .si-step { padding:70px 14px 50px !important; }
  .si-step-num { font-size:clamp(52px,18vw,92px) !important; }
  .si-pay-note > div:first-child {
    white-space:normal !important; text-align:left !important;
  }
  footer { padding-left:14px !important; padding-right:14px !important; }
  section > div[style*="padding:0 34px"], section > div[style*="padding:230px 34px"] {
    padding-left:14px !important; padding-right:14px !important;
  }

  /* nav dock: keep 5 equal cells, never let labels bleed */
  .si-nav { gap:4px !important; padding:9px 8px calc(9px + env(safe-area-inset-bottom)) !important; }
  .si-nav > div { gap:4px !important; min-width:0 !important; overflow:hidden !important; }
  .si-nav > div > div:first-child {
    font-size:0 !important; letter-spacing:0 !important;
    justify-content:center !important; gap:3px !important; overflow:hidden !important;
  }
  .si-nav > div > div:first-child > span:first-child {
    font-size:8px !important; letter-spacing:0 !important;
    display:block !important; max-width:100% !important;
    overflow:hidden !important; white-space:nowrap !important; text-align:center !important;
  }
  .si-nav > div > div:first-child > span:last-child { display:none !important; }
  /* keep only the meaningful word: "Chapter I — About" -> "About" */
  .si-nav > div > div:first-child > span:first-child { font-size:0 !important; }
  .si-nav > div > div:first-child > span:first-child::after {
    font-size:9px !important; letter-spacing:0.02em !important;
  }
  .si-nav > div:nth-child(1) > div:first-child > span:first-child::after { content:'About'; }
  .si-nav > div:nth-child(2) > div:first-child > span:first-child::after { content:'Treat'; }
  .si-nav > div:nth-child(3) > div:first-child > span:first-child::after { content:'Proof'; }
  .si-nav > div:nth-child(4) > div:first-child > span:first-child::after { content:'Steps'; }
  .si-nav > div:nth-child(5) > div:first-child > span:first-child::after { content:'Book'; }
  /* keep the last cell away from the right bezel */
  .si-nav { padding-right:14px !important; padding-left:14px !important; }

  /* flex/grid children must be allowed to shrink below content width */
  [style*="display:flex"] > *, [style*="display:grid"] > * { min-width:0 !important; }
  [style*="display:flex"] { flex-wrap:wrap; }

  /* chapter-1 bio grid: its 470px fixed column never collapses in-place */
  .si-bio-grid { grid-template-columns: minmax(0,1fr) !important; }
  .si-bio-grid > .si-bio-col { width:100% !important; }

  /* pricing-tier grid: drop the third (price) column, let it sit under the name */
  .si-tier-grid { grid-template-columns: minmax(0,1fr) !important; }
  .si-tier-grid > div { width:100% !important; }
  .si-tier-grid svg { width:100% !important; max-width:100% !important; }

  /* absolute safety net */
  body, html { max-width:100vw !important; overflow-x:hidden !important; }
  * { max-width:100%; }
  img, video, svg { max-width:100% !important; }
}

@media (max-width: 390px) {
  .si-hdr-name { display:none !important; }
  .si-hdr-cta { padding:10px 16px !important; font-size:9px !important; letter-spacing:0.14em !important; }
  h1[data-drift], h2[data-drift], h3[data-drift] { font-size:clamp(30px, 12vw, 46px) !important; }
  footer[style*="repeat(4"] { grid-template-columns:minmax(0,1fr) !important; }
  nav[style*="grid-template-columns:repeat(5"] > div > div:first-child > span:first-child {
    font-size:8.5px !important;
  }
}

/* Reduced motion respect */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration:0.01ms !important; animation-iteration-count:1 !important;
    transition-duration:0.01ms !important; scroll-behavior:auto !important; }
}
'''

    # Rebuild the fixed header as a compact, overflow-proof bar.
    hs = tpl.find('<header ')
    he = tpl.find('</header>', hs)
    if hs != -1 and he != -1:
        NEW_HEADER = '''<header class="si-hdr" style="position:fixed; top:0; left:0; right:0; z-index:40; display:flex; align-items:center; justify-content:space-between; gap:12px; padding:22px 34px; mix-blend-mode:normal;">
    <a class="si-hdr-brand" href="#top" style="display:flex; align-items:center; gap:14px; min-width:0; overflow:hidden;">
      <span class="si-hdr-mark" style="flex:none; width:44px; height:44px; border-radius:50%; background:#f2f0ee; color:#050505; display:flex; align-items:center; justify-content:center; font-family:Anton, sans-serif; font-weight:400; font-size:17px; letter-spacing:0.02em;">SI</span>
      <span class="si-hdr-name" style="font-size:11px; letter-spacing:0.26em; text-transform:uppercase; font-weight:500; white-space:nowrap;">Scalpture Ink</span>
    </a>
    <div class="si-hdr-actions" style="display:flex; align-items:center; gap:26px; flex:none;">
      <a class="si-hdr-portfolio" href="Portfolio.dc.html" style="font-size:11px; letter-spacing:0.22em; text-transform:uppercase; font-weight:500; color:rgba(242,240,238,0.75);">Portfolio</a>
      <a class="si-hdr-cta" href="#book" aria-label="Book Consultation" style="border:1px solid rgba(242,240,238,0.35); border-radius:999px; padding:13px 26px; font-size:11px; letter-spacing:0.22em; text-transform:uppercase; font-weight:500; white-space:nowrap;"><span class="si-cta-full">Book Consultation</span><span class="si-cta-short">Book</span></a>
    </div>
  </header>'''
        tpl = tpl[:hs] + NEW_HEADER + tpl[he + len('</header>'):]

    # Tag the structural nodes the mobile layer needs to target. Inline styles
    # are inline styles; classes make the media queries precise instead of
    # guessing with attribute selectors.
    tpl = tpl.replace('{{REMOVE_JHB}}', '')
    for a, b in CLASSES:
        if a in tpl:
            tpl = tpl.replace(a, b, 1)
    for a, b in REPEATED:
        tpl = tpl.replace(a, b)

    idx = tpl.rfind('</style>')
    assert idx != -1, 'no </style> in template'
    tpl_new = tpl[:idx] + MOBILE + tpl[idx:]

    if check:
        print('template len', len(tpl), '->', len(tpl_new))
        print('mobile bytes added', len(tpl_new) - len(tpl))
        return

    tstart, tend = find_script(body, '__bundler/template')
    # Escape closing tags the same way the exporter did (<\u002Fscript> etc.)
    # so an inline JSON island can never terminate early.
    payload = json.dumps(tpl_new, ensure_ascii=False).replace('</', '<\\u002F')
    out = body[:tstart] + payload + body[tend:]
    open(OUT, 'w', encoding='utf-8').write(out)
    print('wrote', OUT, len(out), 'bytes (was', len(body), ')')

if __name__ == '__main__':
    main()
