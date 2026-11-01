#!/usr/bin/env python3
"""Builds DraftTrail's information pages into public/. The apps are public/write/ and public/review/.
Run: python3 tools/build.py   (standard library only)"""
import json, os, html
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
CFG = json.load(open(os.path.join(ROOT, 'site.config.json')))
E = lambda s: html.escape(str(s), quote=True)
URL = CFG['site_url'].rstrip('/'); NAME = CFG['site_name']; ST = CFG['studio']; MAIL = CFG['contact_email']
LOGO = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true"><rect x="4" y="3" width="20" height="26" rx="3" fill="#1F3F7A"/><path d="M9 10h10M9 15h10M9 20h6" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
        '<circle cx="24" cy="23" r="6" fill="#C3303A"/><path d="M21.5 23l1.8 1.8 3.2-3.4" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


import hashlib as _h
CSSV = _h.md5(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'assets', 'site.css'), 'rb').read()).hexdigest()[:8]

# ---------------------------------------------------------------- Telar Labs family links
FAMILY = [f for f in CFG.get('family', []) if f['name'] != CFG['site_name']]
HUB = CFG.get('studio_url', '')

def slug_app(n): return ''.join(ch for ch in n.lower() if ch.isalnum())

def family_row():
    if not FAMILY: return ''
    head = f'<a href="{E(HUB)}">More from {E(CFG["studio"])}</a>' if HUB else f'More from {E(CFG["studio"])}'
    links = ''.join(f'<a class="app-{slug_app(f["name"])}" href="{E(f["url"])}" title="{E(f["blurb"])}">{E(f["name"])}</a>' for f in FAMILY)
    return f'<div class="wrap family"><span class="family-h">{head}:</span>{links}</div>'

def family_promo(title):
    if not FAMILY: return ''
    links = ''.join(f'<a class="app-{slug_app(f["name"])}" href="{E(f["url"])}"><b>{E(f["name"])}</b><span>{E(f["blurb"])}</span></a>' for f in FAMILY)
    return f'<section class="wrap section family-promo"><h2>{title}</h2><div class="family-links">{links}</div></section>'

def ad(key):
    slot = CFG['ad_slots'].get(key, '')
    if not (CFG['adsense_client'] and slot): return ''
    return (f'<div class="ad"><span class="ad-label">Advertisement</span><ins class="adsbygoogle" style="display:block" data-ad-client="{E(CFG["adsense_client"])}" '
            f'data-ad-slot="{E(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></div>')

def page(path, title, desc, body):
    full = title if NAME in title else f'{title} | {NAME}'
    ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={E(CFG["adsense_client"])}" crossorigin="anonymous"></script>'
           if CFG['adsense_client'] else '')
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(full)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(URL + path)}">
<meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(URL + path)}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><meta name="theme-color" content="#1F3F7A">
<link rel="preload" href="/assets/fonts/public-sans-400.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/site.css?v={CSSV}">
{ads}
</head>
<body>
<header class="top"><div class="wrap top-in">
  <a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a>
  <nav class="nav"><a href="/how-it-works/">How it works</a><a href="/for-teachers/">For teachers</a><a href="/faq/">FAQ</a></nav>
  <a class="btn btn-ghost btn-sm" href="/write/">Start writing</a><a class="btn btn-sm" href="/review/">Review files</a>
</div></header>
<main>
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <div><a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a><p class="muted">Free writing-process recorder for students and teachers. Part of the {E(ST)} teacher tools.</p></div>
  <div class="foot-cols">
    <div><h4>Use it</h4><a href="/write/">Start writing</a><a href="/review/">Review .drafttrail files</a><a href="/how-it-works/">How it works</a><a href="/for-teachers/">For teachers</a><a href="/faq/">FAQ</a></div>
    <div><h4>{E(ST)}</h4><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="/contact/">Contact</a></div>
  </div>
</div>{family_row()}<div class="wrap fine">&copy; {date.today().year} {E(ST)}.</div></footer>
</body>
</html>'''
    out = os.path.join(PUB, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(PUB, path.strip('/'))
    os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'w').write(doc)

def prose(path, title, desc, inner): page(path, title, desc, f'<article class="wrap prose">{inner}</article>')

FEATS = [('Records how the writing happened', 'Every keystroke, pause, deletion and paste inside the DraftTrail editor, with timestamps. Not the screen, not other apps.'),
         ('Replay like a video', 'Teachers watch the essay being written from the first word, with pasted text highlighted in yellow.'),
         ('Clear signals, not accusations', 'Flags for big pastes, very few corrections, unusual speed or lots of time away, each explained in plain words.'),
         ('Nothing is uploaded', 'The recording stays on the student\'s device until they download the .drafttrail file and hand it in.'),
         ('Works with Google Classroom', 'Students attach the .drafttrail file like any other file. Teachers open many files at once.'),
         ('Free, no accounts', 'No sign-up for students or teachers, and it works on phones, tablets and computers.')]

def home():
    f = ''.join(f'<div class="feat"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in FEATS)
    body = f'''
<section class="hero"><div class="wrap hero-in">
  <div><p class="eyebrow">Free · No accounts · Nothing uploaded</p>
  <h1>See how the writing was made</h1>
  <p class="hero-sub">In the age of AI, the finished essay isn't enough. DraftTrail records the writing process: typing, pauses, revisions and pastes, so teachers can replay it and students can prove their work is their own.</p>
  <div class="cta"><a class="btn btn-big" href="/write/">Start writing</a><a class="btn btn-ghost btn-big" href="/review/">Review files</a></div></div>
  <div class="mock"><div class="mrow"><b>Maria Santos</b><span class="pill p-lock">2 to review</span></div>
   <div class="mlist"><div><span>Pasted 76 words at 2:41</span></div><div><span>58% of the essay was pasted</span></div></div>
   <div class="mchips"><span class="c-info">212<br><small>Words</small></span><span class="c-bad">58%<br><small>Pasted</small></span><span class="c-warn">4:10<br><small>Active</small></span><span class="c-ok">1<br><small>Session</small></span></div></div>
</div></section>
<section class="wrap section"><h2>What DraftTrail does</h2><div class="feats">{f}</div></section>
{ad("home")}
<section class="wrap section"><h2>How it works</h2>
<ol class="steps"><li><h3>Student writes in DraftTrail</h3><p>Open <a href="/write/">the writing page</a>, type the assignment and name, and write. It saves on the device as you go.</p></li>
<li><h3>Hand in the file</h3><p>Tap <b>Download DraftTrail file</b> and attach it with the writing, for example in Google Classroom.</p></li>
<li><h3>Teacher replays it</h3><p>Open the files on <a href="/review/">the review page</a> to see flags, a timeline and a replay of each essay.</p></li></ol></section>
<section class="wrap section"><div class="callout"><h2>DraftTrail is a conversation starter</h2><p>A big paste or very fast writing doesn't prove cheating. Students may paste their own notes or quotes. DraftTrail shows what happened so teachers can ask good questions, and gives honest students a simple way to show their effort.</p><a class="btn" href="/how-it-works/">Read how it works</a></div></section>'''
    body += family_promo('More free tools for teachers')
    page('/', f'{NAME} – Free Writing Process Recorder for Students and Teachers',
         'DraftTrail records how an essay was written: typing, pauses, revisions and pasted text. Teachers replay it to check originality. Free, no accounts, nothing uploaded.', body)

def pages():
    prose('/how-it-works/', 'How DraftTrail Works', 'What DraftTrail records, what the flags mean, and what it cannot see.', f'''
<h1>How {E(NAME)} works</h1>
<p class="lead">Every piece of writing leaves a trail: first words, pauses, rewrites, and sometimes pasted text. DraftTrail records that trail so it can be replayed.</p>
<h2>What is recorded</h2><ul><li>Each change in the DraftTrail writing box: what was typed or deleted, where, and when.</li><li>Whether text was typed or pasted (or dropped in).</li><li>How many times the student left the page while writing, and for how long.</li></ul>
<h2>What is not recorded</h2><ul><li>Anything outside the DraftTrail writing box: other apps, websites, the screen or the camera.</li><li>Nothing is sent to a server. The recording is saved on the student's device and in the .drafttrail file they download.</li></ul>
<h2>What the teacher sees</h2><ul><li><b>Flags</b> to look at: large pastes, a high share of pasted text, very few corrections, unusually fast typing, a long essay in very little time, leaving the page often, or a file whose text doesn't match its own recording.</li>
<li><b>Numbers:</b> words, % pasted, active writing time, sessions, revisions, thinking pauses.</li><li><b>A chart</b> of the essay's length over time with paste markers, and a <b>replay</b> with pasted text highlighted.</li></ul>
<h2>Limits to know</h2><ul><li>A student could type out text from another source by hand. Replay often shows this as steady typing with no pauses or corrections.</li>
<li>Tech-savvy students could try to edit a .drafttrail file. DraftTrail checks that the final text matches its recording and flags it if not.</li>
<li>Flags are reasons to talk with the student, not proof.</li></ul>''')
    prose('/for-teachers/', 'Using DraftTrail with Your Class', 'Step-by-step guide for teachers: assigning writing with DraftTrail and reviewing the files in Google Classroom.', f'''
<h1>Using {E(NAME)} with your class</h1>
<h2>1. Give students the writing link</h2><p>Share <b>{E(URL)}/write/</b>. To fill in the assignment name for them, add it to the link, for example:<br><code>{E(URL)}/write/?task=Essay%3A%20My%20Dream</code></p>
<h2>2. Ask for two things</h2><p>The writing itself (copied into a doc or the assignment box) <b>and</b> the .drafttrail file from <b>Download DraftTrail file</b>. In Google Classroom, students attach the file with <b>Add or create → File</b>.</p>
<h2>3. Review</h2><p>Download the students' .drafttrail files from Classroom (you can select several), then open <a href="/review/">the review page</a> and drag them in. Click a name to see the report and replay.</p>
<h2>Tips</h2><ul><li>Tell students why: DraftTrail protects honest work and helps you understand their writing process.</li><li>Allow pasting of their own notes, and talk about it, rather than banning it.</li><li>Try <b>"Try with two sample essays"</b> on the review page to see what flags look like.</li></ul>''')
    faq = [('Is DraftTrail free?', 'Yes, for students and teachers, with no accounts.'),
           ('Where is my writing saved?', 'In your browser on your device while you write, and in the .drafttrail file when you download it. Nothing is uploaded to us.'),
           ('Can I continue later?', 'Yes, in the same browser on the same device. Your draft and its recording are kept until you choose Start over.'),
           ('Can I write in Filipino or other languages?', 'Yes. DraftTrail works with any language your keyboard can type, including accents and emoji.'),
           ('What if I paste my own notes?', "That's fine. It shows as pasted text, and your teacher can see it was your notes. Talk with your teacher about what's allowed."),
           ('Does DraftTrail detect AI writing?', 'Not directly. It shows how the text arrived: typed with pauses and corrections, or pasted in large blocks. That is often more useful than an AI detector, which can be wrong.'),
           ('Do teachers need to upload student files?', 'No. Files open in the teacher\'s browser and are not uploaded.')]
    prose('/faq/', 'Frequently Asked Questions', f'Answers to common questions about {NAME}.', '<h1>Frequently asked questions</h1>' + ''.join(f'<h2>{E(q)}</h2><p>{E(a)}</p>' for q, a in faq))
    prose('/about/', 'About', f'About {NAME} by {ST}.', f'''
<h1>About {E(NAME)}</h1><p class="lead">{E(NAME)} is a free writing-process recorder made by {E(ST)}, a small independent studio.</p>
<p>AI tools can produce a finished essay in seconds, and AI detectors often get it wrong, sometimes accusing honest students. {E(NAME)} takes a different approach: instead of guessing from the final text, it keeps a record of how the text was written, which students can share to show their effort.</p>
<h2>Our promises</h2><ul><li>Free, no accounts.</li><li>Recordings stay on the student's device and in the file they choose to hand in.</li><li>No ads on the writing page or the review page.</li></ul>
<h2>Other {E(ST)} tools</h2><p><a href="https://quizpolice.telarlabs.net">QuizPolice</a> for monitored online quizzes, <a href="https://pizarrapad.telarlabs.net">PizarraPad</a>, a free whiteboard, and <a href="https://clips.telarlabs.net">Telar Clips</a>, free motion backgrounds.</p>''')
    prose('/privacy/', 'Privacy Policy', f'Privacy policy for {NAME}.', f'''
<h1>Privacy policy</h1><p class="lead">{E(NAME)} is run by {E(ST)}. Your writing and its recording never leave your device unless you share the file yourself.</p>
<h2>What DraftTrail stores</h2><p>While you write, your text, your name, the assignment name and the recording of your edits are saved in your browser's storage on your device. When you tap Download, the same information is saved into a .drafttrail file on your device. We don't receive any of it.</p>
<h2>Teachers</h2><p>.drafttrail files opened on the review page are read inside the teacher's browser and are not uploaded.</p>
<h2>Advertising</h2><p>The information pages may show ads from Google AdSense, which uses cookies; you can manage personalized ads in <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>. <b>The writing page and the review page never show ads.</b></p>
<h2>Children</h2><p>Students of all ages may use DraftTrail. We don't collect personal information from them.</p>
<h2>Contact</h2><p><a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG["launch_date"])}.</p>''')
    prose('/terms/', 'Terms of Use', f'Terms of use for {NAME}.', f'''
<h1>Terms of use</h1><ul><li>{E(NAME)} is free to use for school and personal writing.</li><li>Your writing belongs to you.</li><li>Flags are signals for a conversation, not proof of misconduct; teachers should use them fairly.</li>
<li>The service is provided as it is, without warranty. Keep your own copies of important work.</li></ul><p>Questions: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG["launch_date"])}.</p>''')
    prose('/contact/', 'Contact', f'Contact {NAME}.', f'<h1>Contact us</h1><p class="lead">Questions or ideas?</p><p>Email: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p>')

def extras():
    open(os.path.join(PUB, 'favicon.svg'), 'w').write(LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" '))
    urls = ['/', '/how-it-works/', '/for-teachers/', '/faq/', '/about/', '/privacy/', '/terms/', '/contact/']
    open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{URL}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(PUB, 'robots.txt'), 'w').write(f'User-agent: *\nDisallow: /write/\nDisallow: /review/\nSitemap: {URL}/sitemap.xml\n')
    if CFG['adsense_client']:
        open(os.path.join(PUB, 'ads.txt'), 'w').write(f'google.com, {CFG["adsense_client"].replace("ca-", "")}, DIRECT, f08c47fec0942fa0\n')
    page('/404.html', 'Page not found', 'Page not found.', '<section class="wrap prose"><h1>Page not found</h1><p><a class="btn" href="/">Go home</a></p></section>')

if __name__ == '__main__':
    home(); pages(); extras(); print('Built DraftTrail pages')
