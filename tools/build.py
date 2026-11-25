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
  <span class="tl-wrap"><a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a><a class="tl-by" href="https://telarlabs.net" title="Telar Labs home"><span>by </span>Telar Labs</a><style>.tl-wrap{{display:flex;align-items:center;min-width:0}}.tl-by{{margin-left:10px;font-size:13px;font-weight:500;line-height:1;color:inherit;opacity:.65;text-decoration:none;white-space:nowrap;flex:none}}.tl-by:hover{{opacity:1;text-decoration:underline}}@media(max-width:560px){{.tl-wrap{{flex-direction:column;align-items:flex-start}}.tl-by{{margin:3px 0 0;font-size:11.5px}}}}</style></span>
  <nav class="nav"><a href="/how-it-works/">How it works</a><a href="/set-up/">Set up a task</a><a href="/for-teachers/">For teachers</a><a href="/prompts/">Prompts</a><a href="/guides/">Guides</a><a href="/faq/">FAQ</a></nav>
  <a class="btn btn-ghost btn-sm" href="/write/">Start writing</a><a class="btn btn-sm" href="/review/">Review files</a>
</div></header>
<main>
{body}
</main>
<footer class="foot"><div class="wrap foot-in">
  <div><a class="logo" href="/">{LOGO}<span>{E(NAME)}</span></a><p class="muted">Free writing-process recorder for students and teachers. Part of the {E(ST)} teacher tools.</p></div>
  <div class="foot-cols">
    <div><h4>Use it</h4><a href="/write/">Start writing</a><a href="/review/">Review .drafttrail files</a><a href="/how-it-works/">How it works</a><a href="/for-teachers/">For teachers</a><a href="/guides/">Guides</a><a href="/prompts/">Writing prompts</a><a href="/tools/word-counter/">Word counter</a><a href="/tools/readability-checker/">Readability checker</a><a href="/practice/word-choice/">Word Choice Check</a><a href="/faq/">FAQ</a></div>
    <div><h4><a href="https://telarlabs.net" style="color:inherit;margin:0">{E(ST)}</a></h4><a href="https://telarlabs.net">Telar Labs home</a><a href="https://telarlabs.net/guides/">Telar Labs guides</a><a href="/about/">About</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="/contact/">Contact</a></div>
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
         ('Nothing is uploaded', 'The recording stays on the student\'s device until they download the .drafttrail file and hand it in. Only the optional live in-class mode (with QuizPolice) saves essays on our server, for up to 30 days.'),
         ('Works with Google Classroom', 'Students attach the .drafttrail file like any other file. Teachers open many files at once.'),
         ('Free, no accounts', 'No sign-up for students or teachers, and it works on phones, tablets and computers.')]

def home():
    f = ''.join(f'<div class="feat"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in FEATS)
    body = f'''
<section class="hero"><div class="wrap hero-in">
  <div><p class="eyebrow">Free · No accounts · Nothing uploaded</p>
  <h1>See how the writing was made</h1>
  <p class="hero-sub">In the age of AI, the finished essay isn't enough. DraftTrail records the writing process: typing, pauses, revisions and pastes, so teachers can replay it and students can prove their work is their own.</p>
  <div class="cta"><a class="btn btn-big" href="/write/">Start writing</a><a class="btn btn-ghost btn-big" href="/set-up/">Teachers: set up a task</a><a class="btn btn-ghost btn-big" href="/review/">Review files</a></div></div>
  <div class="mock"><div class="mrow"><b>Emma Johnson</b><span class="pill p-lock">2 to review</span></div>
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
    body += ('<section class="wrap section"><h2>Guides for teachers</h2><ul class="glist" style="list-style:none;padding:0;display:grid;gap:12px">' + ''.join(f'<li style="border:1px solid var(--line);border-radius:12px;padding:14px 16px"><a href="/guides/{g["slug"]}/" style="font-weight:700">{E(g["title"])}</a></li>' for g in GUIDES) + '</ul><p><a href="/guides/">All guides →</a></p></section>')
    body += family_promo('More free tools for teachers')
    page('/', f'{NAME} – Free Writing Process Recorder for Students and Teachers',
         'DraftTrail records how an essay was written: typing, pauses, revisions and pasted text. Teachers replay it to check originality. Free, no accounts, nothing uploaded.', body)

SETUP = r'''
<h1>Set up a writing task</h1>
<p class="lead">Choose how your students will write. Both are free, and students don't need accounts.</p>
<style>#su [hidden]{display:none!important}#su .field{display:flex;flex-direction:column;gap:6px;font-weight:600}#su input#suTask,#su input#suLink{width:100%;min-height:46px;border-radius:10px;border:1px solid #c9cfdb;padding:0 12px;font:inherit;font-weight:400;box-sizing:border-box}#su fieldset{min-width:0}#su select,#su textarea{width:100%;box-sizing:border-box;max-width:100%}#su{background:#fff;border:1px solid #e2e6ee;border-radius:14px;padding:18px}</style>
<form id="su" class="panel pad" style="display:flex;flex-direction:column;gap:14px;max-width:720px">
  <label class="field"><span>Assignment</span><input id="suTask" maxlength="140" placeholder="e.g. Short answer: Why do leaves change color?" required></label>
  <fieldset style="border:1px solid var(--line);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:10px;margin:0">
    <legend><b>How will students write?</b></legend>
    <label style="display:flex;gap:10px;align-items:flex-start"><input type="radio" name="mode" value="own" checked style="margin-top:5px"><span><b>On their own: homework, or class without live monitoring</b><br><span class="note">Students get a link, write, and hand in a .drafttrail file. Nothing is uploaded. You review the files afterwards.</span></span></label>
    <label style="display:flex;gap:10px;align-items:flex-start"><input type="radio" name="mode" value="live" style="margin-top:5px"><span><b>Live in class, with QuizPolice</b><br><span class="note">Students join with a code. You see live who leaves the writing page, big pastes and word counts. You can lock after too many exits, set a timer, and download every essay at the end. Essays are saved on our server for up to 30 days.</span></span></label>
  </fieldset>
  <fieldset id="suPaper" style="border:1px solid var(--line);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:12px;margin:0">
    <legend><b>For papers and longer writing (optional)</b></legend>
    <label class="field"><span>Citation style</span><select id="suStyle" style="min-height:44px;border-radius:10px;border:1px solid #c9cfdb;padding:0 10px;font:inherit"><option value="">Let students choose (or no citations)</option><option value="cmos-nb">Chicago, notes and bibliography (footnotes)</option><option value="cmos-ad">Chicago, author-date</option><option value="apa">APA 7th edition</option><option value="mla">MLA 9th edition</option></select></label>
    <label class="field"><span>Word goal</span><input id="suWords" type="number" min="0" step="100" placeholder="e.g. 3000" style="min-height:44px;border-radius:10px;border:1px solid #c9cfdb;padding:0 12px;font:inherit;max-width:220px"></label>
    <label class="field"><span>Sections</span><select id="suSecT" style="min-height:44px;border-radius:10px;border:1px solid #c9cfdb;padding:0 10px;font:inherit"><option value="">None</option><option value="Introduction|Background|Analysis|Conclusion">Research paper: Introduction, Background, Analysis, Conclusion</option><option value="Background|Problem|Analysis|Options|Recommendation|Conclusion">Case study: Background, Problem, Analysis, Options, Recommendation, Conclusion</option><option value="Introduction|Literature Review|Method|Results|Discussion|Conclusion">Research report: Introduction, Literature Review, Method, Results, Discussion, Conclusion</option><option value="custom">My own sections…</option></select></label>
    <label class="field" id="suSecRow" hidden><span>Your sections, one per line</span><textarea id="suSec" rows="5" style="border-radius:10px;border:1px solid #c9cfdb;padding:10px 12px;font:inherit"></textarea></label>
    <span class="note">Students add their sources once, press “Cite” where a citation belongs, and get the footnotes or in-text citations and the bibliography made for them. They can download the paper as a Word file with real footnotes, and hand in the .drafttrail file with it.</span>
  </fieldset>
  <label id="suRulesRow" style="display:flex;gap:10px;align-items:center"><input type="checkbox" id="suRules" checked> <span><b>Warn students when they leave the page</b> <span class="note">(every exit is recorded in the file either way)</span></span></label>
  <button class="btn btn-big" id="suGo">Create the student link</button>
  <div id="suOut" hidden style="display:flex;flex-direction:column;gap:8px">
    <b>Share this link with your students:</b>
    <input id="suLink" readonly style="min-height:44px;border-radius:10px;border:1px solid var(--line);padding:0 12px;font:inherit">
    <div style="display:flex;gap:8px;flex-wrap:wrap"><button type="button" class="btn" id="suCopy">Copy link</button><a class="btn btn-ghost" href="/review/">Open the review page</a></div>
    <span class="note">Ask students to hand in the .drafttrail file with their work, for example in Google Classroom.</span>
  </div>
</form>
<h2>Which should I choose?</h2>
<ul><li><b>On their own</b> suits homework, take-home essays and schools with no reliable internet. It works offline, and nothing leaves the student's device until they hand in the file.</li>
<li><b>Live in class</b> suits short answers and essays written during the lesson, when the rule is "no searching, no other pages". You watch the class live and collect all essays at once.</li></ul>
<p class="note">Neither mode can see a second phone or a book on the desk. It records when a student leaves the writing page on that device. For "no other gadgets", keep an eye on the room too.</p>
<script>
(()=>{const $=s=>document.querySelector(s);
const mode=()=>document.querySelector('input[name=mode]:checked').value;
$('#suSecT').onchange=()=>{$('#suSecRow').hidden=$('#suSecT').value!=='custom'};
document.querySelectorAll('input[name=mode]').forEach(r=>r.onchange=()=>{const live=mode()==='live';$('#suRulesRow').hidden=live;$('#suPaper').hidden=live;$('#suGo').textContent=live?'Continue in QuizPolice':'Create the student link';$('#suOut').hidden=true;});
$('#su').onsubmit=e=>{e.preventDefault();const t=$('#suTask').value.trim();if(!t){$('#suTask').focus();return}
 if(mode()==='live'){location.href='https://quizpolice.telarlabs.net/teacher/?writing='+encodeURIComponent(t)+'#new';return}
 const q=new URLSearchParams({task:t}); if($('#suRules').checked) q.set('rules','1');
 if($('#suStyle').value) q.set('style',$('#suStyle').value); if(parseInt($('#suWords').value)>0) q.set('words',parseInt($('#suWords').value));
 const sec=$('#suSecT').value==='custom'?$('#suSec').value.split('\n').map(x=>x.trim()).filter(Boolean).join('|'):$('#suSecT').value; if(sec) q.set('sections',sec);
 const u=location.origin+'/write/?'+q.toString();$('#suLink').value=u;$('#suOut').hidden=false;$('#suLink').select();};
$('#suCopy').onclick=async()=>{try{await navigator.clipboard.writeText($('#suLink').value);$('#suCopy').textContent='Copied ✓'}catch(e){$('#suLink').select()}setTimeout(()=>$('#suCopy').textContent='Copy link',2000)};
})();
</script>'''

def pages():
    prose('/how-it-works/', 'How DraftTrail Works', 'What DraftTrail records, what the flags mean, and what it cannot see.', f'''
<h1>How {E(NAME)} works</h1>
<p class="lead">Every piece of writing leaves a trail: first words, pauses, rewrites, and sometimes pasted text. DraftTrail records that trail so it can be replayed.</p>
<h2>What is recorded</h2><ul><li>Each change in the DraftTrail writing box: what was typed or deleted, where, and when.</li><li>Whether text was typed or pasted (or dropped in), and which pasted passages the student marked as quotes from a source.</li><li>The sources the student added and where they cited them.</li><li>How many times the student left the page while writing, and for how long.</li></ul>
<h2>What is not recorded</h2><ul><li>Anything outside the DraftTrail writing box: other apps, websites, the screen or the camera.</li><li>Nothing is sent to a server. The recording is saved on the student's device and in the .drafttrail file they download.</li></ul>
<h2>What the teacher sees</h2><ul><li><b>Flags</b> to look at: large pastes, a high share of pasted text, very few corrections, unusually fast typing, a long essay in very little time, leaving the page often, or a file whose text doesn't match its own recording.</li>
<li><b>Numbers:</b> words, % pasted, active writing time, sessions, revisions, thinking pauses.</li><li><b>A chart</b> of the essay's length over time with paste markers, and a <b>replay</b> with pasted text highlighted.</li></ul>
<h2>What each number means</h2>
<ul><li><b>Active writing time</b> adds up the time between edits, but counts any gap as at most 30 seconds. A student who leaves the essay open overnight doesn’t look like they wrote for 12 hours.</li>
<li><b>Sessions</b>: a new session starts after a break of more than 5 minutes. Real essays are often written in two or three sittings.</li>
<li><b>Thinking pauses</b>: gaps of more than 5 seconds between edits. Writers pause to plan, reread and choose words, so a long essay with almost no pauses is unusual.</li>
<li><b>Revisions</b>: how much of the typed text was later deleted. Most people delete and rewrite as they go.</li>
<li><b>% pasted</b>: how much of the final essay arrived by pasting or dropping text in, rather than typing. Pasted text the student marked as a quote is counted separately.</li></ul>

<h2>When a flag appears</h2>
<table class="tbl"><thead><tr><th>Flag</th><th>Shown when</th></tr></thead><tbody>
<tr><td>Large paste</td><td>A single paste of 15 words or more that the student didn’t mark as a quote.</td></tr>
<tr><td>High share of pasted text</td><td>30% or more of the final text was pasted.</td></tr>
<tr><td>Lots of quoted text</td><td>25% or more of the final text is quoted from sources. Quoting is allowed, but an essay that is mostly quotes may need a conversation.</td></tr>
<tr><td>Very few corrections</td><td>An essay of 120 words or more where less than 2% of the typed text was deleted.</td></tr>
<tr><td>Unusually fast typing</td><td>More than 90 words per minute of active time.</td></tr>
<tr><td>Long essay, little time</td><td>150 words or more written in less than 5 minutes of active time.</td></tr></tbody></table>
<p>Flags are deliberately simple so you can explain them to a student or a parent in one sentence. None of them decides anything on its own.</p>

<h2>Quotes and sources</h2>
<p>Students can add sources (books, articles, web pages and more) and cite them while they write. DraftTrail formats the citations in APA 7, MLA 9 or Chicago, and builds the reference list. When a student pastes a passage and marks it as a quote from a source, it’s shown as a quote, not as an unexplained paste. This teaches the habit you want: copy only what you cite, and say where it came from.</p>

<h2>Reading a replay</h2>
<p>The replay shows the essay being written from the first word, faster than real time, with pasted text highlighted. Look for the shape of the work rather than single moments:</p>
<ul><li><b>Usual:</b> an outline or a rough start, then sentences that grow, move and get rewritten, with pauses in between.</li>
<li><b>Worth asking about:</b> a whole paragraph arriving at once, or steady typing from start to finish with no pauses or corrections, which can mean the text was copied by hand from somewhere else.</li></ul>

<h2>Limits to know</h2><ul><li>A student could type out text from another source by hand. Replay often shows this as steady typing with no pauses or corrections.</li>
<li>Tech-savvy students could try to edit a .drafttrail file. DraftTrail checks that the final text matches its recording and flags it if not.</li>
<li>Flags are reasons to talk with the student, not proof.</li></ul>
<p>Ready to try it? <a href="/set-up/">Set up a writing task</a>, or read <a href="https://telarlabs.net/guides/writing-process-age-of-ai/">how to see the writing process in the age of AI</a>.</p>''')
    prose('/set-up/', 'Set Up a Writing Task', 'Create a DraftTrail writing link for homework, or a live in-class writing task with exit monitoring through QuizPolice.', SETUP)
    prose('/for-teachers/', 'Using DraftTrail with Your Class', 'Step-by-step guide for teachers: assigning writing with DraftTrail and reviewing the files in Google Classroom.', f'''
<h1>Using {E(NAME)} with your class</h1>
<p class="lead"><a class="btn" href="/set-up/">Set up a writing task</a> &nbsp;Choose homework mode, or live in class with exit monitoring.</p>
<h2>1. Give students the writing link</h2><p>Use <a href="/set-up/">Set up a writing task</a> to make the link, or share <b>{E(URL)}/write/</b>. To fill in the assignment name for them, add it to the link, for example:<br><code>{E(URL)}/write/?task=Essay%3A%20My%20Dream</code>. Add <code>&amp;rules=1</code> to warn students each time they leave the page.</p>
<h2>Term papers, case studies and citations</h2><p>On the <a href="/set-up/">set-up page</a>, choose a citation style (Chicago notes and bibliography, Chicago author-date, APA 7 or MLA 9), a word goal and sections. Students cite with one button and download their paper as a Word file with real footnotes. On the review page you see every writing session with its date, the sources, which ones were cited, and each pasted passage the student marked as a quote, so you can check it against the source. Students can move between computers by continuing from their .drafttrail file.</p><h2>Writing in class with live monitoring</h2><p>For short answers or essays written during the lesson, choose <b>Live in class</b> on the <a href="/set-up/">set-up page</a>. It opens QuizPolice, where students join with a code and write in DraftTrail. You see live who leaves the page, big pastes and word counts, can lock students after too many exits, set a timer, and download all essays as one file to open on the review page. When the time runs out, essays are handed in automatically.</p>
<h2>2. Ask for two things</h2><p>The writing itself (copied into a doc or the assignment box) <b>and</b> the .drafttrail file from <b>Download DraftTrail file</b>. In Google Classroom, students attach the file with <b>Add or create → File</b>.</p>
<h2>3. Review</h2><p>Download the students' .drafttrail files from Classroom (you can select several), then open <a href="/review/">the review page</a> and drag them in. Click a name to see the report and replay.</p>
<h2>Tips</h2><ul><li>Tell students why: DraftTrail protects honest work and helps you understand their writing process.</li><li>Allow pasting of their own notes, and talk about it, rather than banning it.</li><li>Try <b>"Try with three samples"</b> on the review page to see what flags look like.</li></ul>''')
    faq = [('Is DraftTrail free?', 'Yes, for students and teachers, with no accounts.'),
           ('Where is my writing saved?', 'In your browser on your device while you write, and in the .drafttrail file when you download it. Nothing is uploaded to us, unless your teacher uses the live in-class mode with QuizPolice: then your essay is saved with the quiz and deleted after 30 days.'),
           ('Can I continue later?', 'Yes. In the same browser, your draft and its recording are kept until you choose Start over. To switch computers, download your DraftTrail file, then on the other computer open "Continue on another computer" on the writing page and choose the file. The recording continues from where you stopped.'),
           ('Can I use DraftTrail for term papers and case studies?', 'Yes. There is no word limit, you can write over many days, and your teacher can set a word goal and sections (for example Background, Problem, Analysis, Recommendation). The review shows each writing session with its date.'),
           ('How do citations work?', 'Add each source once (book, chapter, journal article, newspaper, web page). Put the cursor where the citation belongs and press "Cite a source". DraftTrail writes a short code like [@smith2019, 45] and turns it into footnotes or in-text citations, with the bibliography, in Chicago (notes and bibliography or author-date), APA 7 or MLA 9. "Download Word (.docx)" gives you the paper with real footnotes. Always check the list against your teacher\'s guide: DraftTrail formats sources but can\'t check that they are real.'),
           ('What if I paste a quote from a source?', 'DraftTrail asks whether the pasted text is a quote. If you choose the source, it adds quotation marks (or makes a block quote for long passages) and the citation, and your teacher sees it as a cited quote instead of copied text.'),
           ('Can I write in Spanish, Filipino or other languages?', 'Yes. DraftTrail works with any language your keyboard can type, including accents and emoji.'),
           ('What if I paste my own notes?', "That's fine. It shows as pasted text, and your teacher can see it was your notes. Talk with your teacher about what's allowed."),
           ('Does DraftTrail detect AI writing?', 'Not directly. It shows how the text arrived: typed with pauses and corrections, or pasted in large blocks. That is often more useful than an AI detector, which can be wrong.'),
           ('Do teachers need to upload student files?', 'No. Files open in the teacher\'s browser and are not uploaded.')]
    prose('/faq/', 'Frequently Asked Questions', f'Answers to common questions about {NAME}.', '<h1>Frequently asked questions</h1>' + ''.join(f'<h2>{E(q)}</h2><p>{E(a)}</p>' for q, a in faq))
    prose('/about/', 'About', f'About {NAME}, the free writing-process recorder, by {ST}.', f"""
<h1>About {E(NAME)}</h1><p class="lead">{E(NAME)} is a free writing-process recorder made by {E(ST)}, a small independent studio.</p>
<p>AI tools can produce a finished essay in seconds, and AI detectors often get it wrong, sometimes accusing honest students. {E(NAME)} takes a different approach: instead of guessing from the final text, it keeps a record of how the text was written, which students can share to show their effort.</p>

<h2>Why a record of the process</h2>
<p>A finished essay can’t tell you how it was made. A history of the writing can: when it started, how it grew, what was rewritten, and what was pasted in. Teachers have always asked for drafts and outlines for this reason. DraftTrail does the same thing automatically, for every essay, without extra work for the student.</p>
<p>It helps honest students most. A student who is wrongly suspected can hand in the recording and show hours of real work, instead of trying to prove a negative.</p>

<h2>Who it’s for</h2>
<ul><li><b>Teachers</b> who assign essays, reflections or short answers and want a fair way to check the work.</li>
<li><b>Students</b> who want proof that their writing is their own.</li>
<li><b>Schools</b> that use Google Classroom or another learning system: the .drafttrail file is handed in like any other file.</li>
<li><b>Writing tutors</b> who want to see where a student gets stuck, by watching how the draft develops.</li></ul>

<h2>How it’s built</h2>
<ul><li><b>Private by default.</b> The writing and its recording are saved on the student’s device. Nothing is uploaded unless the teacher uses the live in-class mode with <a href="https://quizpolice.telarlabs.net">QuizPolice</a>.</li>
<li><b>Checks that can be explained.</b> Every flag is a simple rule in plain words, listed on <a href="/how-it-works/">How it works</a>.</li>
<li><b>Useful for writing, too.</b> Students get word counts, section headings, citations in APA, MLA and Chicago, and a reference list.</li>
<li><b>Works on any device</b> with a modern browser, including phones, with no app to install.</li></ul>

<h2>Our promises</h2><ul><li>Free, no accounts.</li><li>Recordings stay on the student's device and in the file they choose to hand in.</li><li>No ads on the writing page or the review page.</li></ul>

<h2>Get started</h2>
<ul><li>Students: <a href="/write/">start writing</a>.</li><li>Teachers: <a href="/set-up/">set up a task</a>, read <a href="/for-teachers/">using DraftTrail with your class</a>, or <a href="/review/">review files</a>.</li></ul>

<h2>Other {E(ST)} tools</h2><p><a href="https://quizpolice.telarlabs.net">QuizPolice</a> for monitored online quizzes, <a href="https://pizarrapad.telarlabs.net">PizarraPad</a>, a free whiteboard, <a href="https://clips.telarlabs.net">Telar Clips</a>, free motion backgrounds, and <a href="https://tixward.telarlabs.net">Tixward</a>, event tickets and bookings.</p>
<p>Questions or ideas? <a href="/contact/">Contact us</a>.</p>""")
    prose('/privacy/', 'Privacy Policy', f'Privacy policy for {NAME}.', f'''
<h1>Privacy policy</h1><p class="lead">{E(NAME)} is run by {E(ST)}. Your writing and its recording never leave your device unless you share the file yourself, or your teacher uses the live in-class mode described below.</p>
<h2>What DraftTrail stores</h2><p>While you write, your text, your name, the assignment name and the recording of your edits are saved in your browser's storage on your device. When you tap Download, the same information is saved into a .drafttrail file on your device. We don't receive any of it.</p>
<h2>Live in-class mode (with QuizPolice)</h2><p>If your teacher sets up a live writing task, you write in DraftTrail inside QuizPolice. Your name, your essay, its recording, word counts, large pastes and times you left the page are then sent to QuizPolice so your teacher can see them during class and download them afterwards. This data is visible only to that teacher and is deleted automatically 30 days after the task was created. See the <a href="https://quizpolice.telarlabs.net/privacy/">QuizPolice privacy policy</a>.</p>
<h2>Teachers</h2><p>.drafttrail files opened on the review page are read inside the teacher's browser and are not uploaded.</p>
<h2>Advertising</h2><p>The information pages may show ads from Google AdSense, which uses cookies; you can manage personalized ads in <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>. <b>The writing page and the review page never show ads.</b></p>
<h2>Analytics</h2><p>We use Cloudflare Web Analytics to count page visits. It does not use cookies and does not track you across websites.</p>
<h2>Children</h2><p>Students of all ages may use DraftTrail. In the normal mode we don't collect personal information from them. In the live in-class mode we collect only what the teacher needs, as described above.</p>
<h2>Contact</h2><p><a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated 2026-11-07.</p>''')
    prose('/terms/', 'Terms of Use', f'Terms of use for {NAME}.', f'''
<h1>Terms of use</h1><ul><li>{E(NAME)} is free to use for school and personal writing.</li><li>Your writing belongs to you.</li><li>Flags are signals for a conversation, not proof of misconduct; teachers should use them fairly.</li>
<li>The service is provided as it is, without warranty. Keep your own copies of important work.</li></ul><p>Questions: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p><p class="muted">Last updated {E(CFG["launch_date"])}.</p>''')
    prose('/contact/', 'Contact', f'Contact {NAME}.', f'<h1>Contact us</h1><p class="lead">Questions or ideas?</p><p>Email: <a href="mailto:{E(MAIL)}">{E(MAIL)}</a></p>')

def extras():
    open(os.path.join(PUB, 'favicon.svg'), 'w').write(LOGO.replace('class="logo-mark" ', 'xmlns="http://www.w3.org/2000/svg" '))
    urls = ['/', '/how-it-works/', '/set-up/', '/for-teachers/', '/faq/', '/guides/'] + [f'/guides/{g["slug"]}/' for g in GUIDES] + ['/practice/word-choice/', '/tools/word-counter/', '/tools/readability-checker/', '/prompts/'] + [f'/prompts/{t["slug"]}/' for t in PTYPES] + ['/about/', '/privacy/', '/terms/', '/contact/']
    open(os.path.join(PUB, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{URL}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    open(os.path.join(PUB, 'robots.txt'), 'w').write(f'User-agent: *\nDisallow: /write/\nDisallow: /review/\nDisallow: /cdn-cgi/\n\nUser-agent: Mediapartners-Google\nAllow: /\n\nSitemap: {URL}/sitemap.xml\n')
    if CFG['adsense_client']:
        open(os.path.join(PUB, 'ads.txt'), 'w').write(f'google.com, {CFG["adsense_client"].replace("ca-", "")}, DIRECT, f08c47fec0942fa0\n')
    page('/404.html', 'Page not found', 'Page not found.', '<section class="wrap prose"><h1>Page not found</h1><p><a class="btn" href="/">Go home</a></p></section>')


# ---------------------------------------------------------------- help guides (content pages)
import sys as _sys; _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides_content import GUIDES, LEAD as GUIDES_LEAD
GUIDE_STYLE = ('<style>.glist{list-style:none;padding:0;display:flex;flex-direction:column;gap:14px}.glist li{border:1px solid var(--line);border-radius:12px;padding:14px 16px}'
               '.glist a{font-weight:700}.glist p{margin:6px 0 0}.gmeta{font-size:14px;margin:0 0 6px}</style>')
def guides():
    items = ''.join(f'<li><a href="/guides/{g["slug"]}/">{E(g["title"])}</a><p class="muted">{E(g["desc"])}</p></li>' for g in GUIDES)
    prose('/guides/', f'{NAME} Guides for Teachers', f'{GUIDES_LEAD}', f'{GUIDE_STYLE}<h1>Guides</h1><p class="lead">{E(GUIDES_LEAD)}</p><ul class="glist">{items}</ul>'
          f'<p><b>For students:</b> practice commonly confused words with our free <a href="/practice/word-choice/">Word Choice Check</a> game.</p><p>More guides for teachers and organizers: <a href="https://telarlabs.net/guides/">Telar Labs guides</a>.</p>')
    for g in GUIDES:
        more = ''.join(f'<li><a href="/guides/{o["slug"]}/">{E(o["title"])}</a></li>' for o in GUIDES if o is not g)
        prose(f'/guides/{g["slug"]}/', g['title'], g['desc'],
              f'{GUIDE_STYLE}<p class="gmeta muted"><a href="/guides/">Guides</a> · Updated {E(g["updated"])}</p><h1>{E(g["title"])}</h1>{g["body"]}'
              f'<h2>More guides</h2><ul>{more}<li><a href="https://telarlabs.net/guides/">Telar Labs guides for teachers and organizers</a></li></ul>')

# ---------------------------------------------------------------- Word Choice Check (practice game)
from practice_content import GAME_CSS, wc_game, wc_text
def practice():
    prose('/practice/word-choice/', 'Word Choice Check: Commonly Confused Words Quiz Game',
          'A free game for students: affect or effect, fewer or less, its or it’s and more. Practice commonly confused words, with a quick guide to each pair.',
          f'{GAME_CSS}<p class="gmeta muted" style="font-size:14px;margin:0 0 6px">Practice for students</p><h1>Word Choice Check</h1>{wc_game()}{wc_text()}')

# ---------------------------------------------------------------- writing tools and prompts
import urllib.parse as _up
from writing_tools import TOOLS as WTOOLS, CSS as WCSS
from prompts_content import TYPES as PTYPES, HUB_INTRO, HUB_TEXT
PT_CSS = ('<style>.ptable{width:100%;border-collapse:collapse;font-size:15px;margin:10px 0 18px}.ptable th,.ptable td{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left;vertical-align:top}'
          '.ptable th{font-size:13px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}'
          '.plist{list-style:none;padding:0;display:flex;flex-direction:column;gap:10px}.plist li{border:1px solid var(--line);border-radius:12px;padding:12px 14px;background:var(--card);display:flex;gap:12px;align-items:center;justify-content:space-between}'
          '.plist a{flex:none;font-weight:700;white-space:nowrap}.ptiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin:16px 0}'
          '.ptiles a{display:block;border:1px solid var(--line);border-radius:14px;padding:16px;background:var(--card);text-decoration:none;color:var(--fg)}.ptiles b{display:block;font-size:19px;color:var(--brand);margin-bottom:4px}'
          '@media(max-width:560px){.plist li{flex-direction:column;align-items:flex-start}}</style>')
def wtools():
    for path, title, short, desc, tool, text in WTOOLS:
        other = ''.join(f'<li><a href="{p}">{E(s)}</a></li>' for p, _, s, _, _, _ in WTOOLS if p != path)
        prose(path, title, desc, f'{WCSS}{PT_CSS}<p class="muted" style="font-size:14px;margin:0 0 6px">Free writing tools</p><h1>{E(short)}</h1>{tool}{text}'
              f'<h2>More free tools</h2><ul>{other}<li><a href="/prompts/">Writing prompts for every grade</a></li><li><a href="/practice/word-choice/">Word Choice Check</a></li></ul>')
    tiles = ''.join(f'<a href="/prompts/{t["slug"]}/"><b>{E(t["name"])}</b>{E(t["intro"])}</a>' for t in PTYPES)
    prose('/prompts/', 'Writing Prompts for Students: 100+ Free Prompts by Grade', 'Over 100 free writing prompts for elementary, middle and high school: narrative, persuasive, opinion, informative, descriptive and journal. Start writing in one tap.',
          f'{PT_CSS}<h1>Writing prompts</h1>{HUB_INTRO}<div class="ptiles">{tiles}</div>{HUB_TEXT}')
    for t in PTYPES:
        bands = ''.join(f'<h2>{E(b)}</h2><ul class="plist">' + ''.join(f'<li><span>{E(q)}</span><a href="/write/?task={_up.quote(q)}">Write this →</a></li>' for q in ps) + '</ul>' for b, ps in t['P'].items())
        tips = ''.join(f'<li>{E(x)}</li>' for x in t['tips'])
        others = ''.join(f'<li><a href="/prompts/{o["slug"]}/">{E(o["name"])} writing prompts</a></li>' for o in PTYPES if o is not t)
        prose(f'/prompts/{t["slug"]}/', t['title'], t['desc'],
              f'{PT_CSS}<p class="muted" style="font-size:14px;margin:0 0 6px"><a href="/prompts/">Writing prompts</a></p><h1>{E(t["name"])} writing prompts</h1>'
              f'<p class="lead">{E(t["intro"])} Tap <b>Write this</b> to open a prompt in DraftTrail and start writing.</p>'
              f'<h2>Tips for {E(t["name"].lower())} writing</h2><ul>{tips}</ul>{bands}'
              f'<h2>For teachers</h2><p>Share a prompt’s <b>Write this</b> link with your class, or use <a href="/set-up/">Set up a task</a> to add a time limit. Students hand in a file you can replay to see how the writing was built.</p>'
              f'<h2>More prompts</h2><ul>{others}</ul>')

if __name__ == '__main__':
    home(); pages(); guides(); practice(); wtools(); extras(); print('Built DraftTrail pages')

    # AdSense: no ad code on error, contact and legal pages (no publisher content)
    import re as _re
    for _p in ('404.html', 'contact/index.html', 'privacy/index.html', 'terms/index.html'):
        _f = os.path.join(PUB, _p)
        if os.path.exists(_f):
            _s = open(_f).read()
            _s = _re.sub(r'<script async src="https://pagead2\.googlesyndication\.com[^>]*></script>', '', _s)
            _s = _re.sub(r'<div class="ad">.*?</ins>(<script>.*?</script>)?</div>', '', _s, flags=_re.S)
            open(_f, 'w').write(_s)
