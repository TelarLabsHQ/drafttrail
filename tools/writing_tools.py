"""DraftTrail writing tools (/tools/...): word counter and readability checker.
Both run entirely in the browser; the text is never sent anywhere."""

CSS = '''<style>
.wt{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;margin:8px 0 34px;box-shadow:0 10px 30px rgba(20,27,43,.07)}
.wt textarea{width:100%;min-height:230px;border:1px solid var(--line);border-radius:12px;padding:14px;font:17px/1.6 var(--body);color:var(--fg);background:var(--bg);resize:vertical}
.wt .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-top:14px}
.wt .stat{border:1px solid var(--line);border-radius:12px;padding:10px 12px;background:#fff}.wt .stat b{display:block;font-size:26px;font-family:var(--head);color:var(--brand);line-height:1.2}
.wt .stat span{font-size:13px;color:var(--muted)}
.wt .row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px}
.wt button{font:inherit;font-weight:700;font-size:15px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--fg);padding:8px 14px;cursor:pointer}
.wt .pri{background:var(--brand);color:#fff;border-color:var(--brand)}
.wt .lvl{margin-top:14px;padding:14px;border-radius:12px;background:var(--info-bg)}
.wt .lvl b{font-size:20px}
.wt .hl{margin-top:12px;border:1px solid var(--line);border-radius:12px;padding:14px;background:#fff;line-height:1.8;white-space:pre-wrap}
.wt .hl mark{background:var(--warn-bg);border-bottom:2px solid var(--warn);color:inherit;padding:1px 0}.wt .hl mark.vl{background:var(--bad-bg);border-color:var(--bad)}
.wt .key{font-size:14px;color:var(--muted);margin-top:8px}.wt .key i{display:inline-block;width:14px;height:10px;border-radius:3px;vertical-align:middle;margin:0 4px 0 10px}
</style>'''

# shared text analysis: words, sentences, syllables (English estimate)
ENGINE = r'''
const TA={
 words:t=>(t.match(/[\p{L}\p{N}][\p{L}\p{N}'’\-]*/gu)||[]),
 sentences:t=>t.replace(/\s+/g,' ').trim().split(/(?<=[.!?…])\s+(?=[\p{Lu}\p{N}"“‘(\[])/u).map(s=>s.trim()).filter(s=>TA.words(s).length),
 paragraphs:t=>t.split(/\n\s*\n/).filter(p=>p.trim()).length,
 syl:w=>{w=w.toLowerCase().replace(/[^a-z]/g,'');if(!w)return 0;if(w.length<=3)return 1;
  w=w.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'');const m=w.match(/[aeiouy]{1,2}/g);return Math.max(1,m?m.length:1)},
 fk:t=>{const W=TA.words(t),S=Math.max(1,TA.sentences(t).length),sy=W.reduce((a,w)=>a+TA.syl(w),0);if(!W.length)return null;
  return {grade:0.39*W.length/S+11.8*sy/W.length-15.59,ease:206.835-1.015*W.length/S-84.6*sy/W.length,wps:W.length/S}},
 time:(n,wpm)=>{const m=n/wpm;return m<1?Math.max(1,Math.round(m*60))+' sec':Math.floor(m)+' min '+(Math.round(m%1*60)?Math.round(m%1*60)+' sec':'')}
};
const store={get:(k,d)=>{try{const v=localStorage.getItem(k);return v===null?d:v}catch(e){return d}},set:(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}}};
'''

WC = '''<div class="wt" id="wc">
 <textarea id="wcT" placeholder="Type or paste your text here…" aria-label="Your text"></textarea>
 <div class="stats">
  <div class="stat"><b id="wcW">0</b><span>words</span></div><div class="stat"><b id="wcC">0</b><span>characters</span></div>
  <div class="stat"><b id="wcCn">0</b><span>characters without spaces</span></div><div class="stat"><b id="wcS">0</b><span>sentences</span></div>
  <div class="stat"><b id="wcP">0</b><span>paragraphs</span></div><div class="stat"><b id="wcR">0 sec</b><span>reading time</span></div>
  <div class="stat"><b id="wcSp">0 sec</b><span>speaking time</span></div><div class="stat"><b id="wcA">0</b><span>average words per sentence</span></div>
 </div>
 <div class="row"><label>Word goal <input type="number" id="wcG" min="0" step="50" style="width:90px;font:inherit;padding:6px;border:1px solid var(--line);border-radius:8px"></label><span id="wcGl" class="muted"></span>
  <span style="flex:1"></span><button type="button" id="wcClr">Clear</button><a class="pri" href="/write/" style="text-decoration:none;font-weight:700;border-radius:999px;padding:8px 14px;background:var(--brand);color:#fff">Write with DraftTrail →</a></div>
 <p class="key">Your text stays in this browser. Nothing is uploaded.</p>
</div>
<script>(()=>{''' + ENGINE + '''
const $=i=>document.getElementById(i);$('wcT').value=store.get('dt-wc','');$('wcG').value=store.get('dt-wc-goal','');
function upd(){const t=$('wcT').value,W=TA.words(t),S=TA.sentences(t);store.set('dt-wc',t);
 $('wcW').textContent=W.length.toLocaleString();$('wcC').textContent=t.length.toLocaleString();$('wcCn').textContent=t.replace(/\\s/g,'').length.toLocaleString();
 $('wcS').textContent=S.length;$('wcP').textContent=TA.paragraphs(t);$('wcR').textContent=W.length?TA.time(W.length,238):'0 sec';$('wcSp').textContent=W.length?TA.time(W.length,140):'0 sec';
 $('wcA').textContent=S.length?(W.length/S.length).toFixed(1):0;
 const g=+$('wcG').value;store.set('dt-wc-goal',$('wcG').value);$('wcGl').textContent=g?(W.length>=g?'✓ Goal reached ('+(W.length-g)+' over)':(g-W.length)+' words to go'):''}
$('wcT').oninput=upd;$('wcG').oninput=upd;$('wcClr').onclick=()=>{$('wcT').value='';upd()};upd()})();</script>'''

WC_TEXT = '''<h2>What the word counter shows</h2>
<ul><li><b>Words:</b> any run of letters or numbers, including words with apostrophes or hyphens (<i>don’t</i> and <i>well-known</i> count as one word each).</li>
<li><b>Characters:</b> every letter, number, space and punctuation mark. Many forms and social posts limit characters, not words.</li>
<li><b>Sentences and paragraphs:</b> sentences end with a period, question mark or exclamation mark; paragraphs are separated by a blank line.</li>
<li><b>Reading time:</b> based on an average silent reading speed of about 238 words per minute.</li>
<li><b>Speaking time:</b> based on about 140 words per minute, a comfortable pace for a speech or presentation.</li></ul>
<p>Set a <b>word goal</b> and the counter tells you how many words are left. The text and the goal are remembered on this device, so you can come back later.</p>

<h2>How long is…?</h2>
<table class="ptable"><thead><tr><th>Piece of writing</th><th>Typical length</th></tr></thead><tbody>
<tr><td>A paragraph</td><td>100 to 200 words, 4 to 8 sentences</td></tr>
<tr><td>A short answer on a test</td><td>50 to 150 words</td></tr>
<tr><td>A five-paragraph essay</td><td>500 to 800 words</td></tr>
<tr><td>A college application essay</td><td>often 250 to 650 words (check the exact limit)</td></tr>
<tr><td>A one-page, double-spaced essay</td><td>about 250 to 300 words</td></tr>
<tr><td>A 5-minute speech</td><td>about 650 to 750 words</td></tr>
<tr><td>A blog post</td><td>usually 600 to 1,500 words</td></tr></tbody></table>

<h2>Tips for hitting a word count</h2>
<ul><li><b>Too short?</b> Add an example, a quotation or a counter-argument, rather than repeating yourself. Explain <i>why</i> a point matters.</li>
<li><b>Too long?</b> Cut words like <i>very</i>, <i>really</i> and <i>in order to</i>. Remove sentences that only restate the one before.</li>
<li><b>Check the rules.</b> Some teachers count titles and references, others don’t. When in doubt, ask.</li>
<li><b>Read it aloud.</b> The speaking time helps you practice a presentation and stay within your slot.</li></ul>

<h2>Writing for a class?</h2>
<p>When you write in <a href="/write/">DraftTrail</a>, your teacher can see how your writing was built, step by step, which shows the work is your own. To check how easy your text is to read, try the <a href="/tools/readability-checker/">readability checker</a>.</p>
<h2>Questions</h2>
<p><b>Is my text private?</b> Yes. Counting happens in your browser; your text is never uploaded.</p>
<p><b>Why might my word processor show a slightly different number?</b> Programs treat dashes, numbers and links slightly differently. Differences of a word or two are normal.</p>'''

RC = '''<div class="wt" id="rc">
 <textarea id="rcT" placeholder="Paste a paragraph or more of English text…" aria-label="Your text"></textarea>
 <div class="lvl" id="rcL">Paste some text to see its reading level.</div>
 <div class="stats">
  <div class="stat"><b id="rcG">–</b><span>Flesch–Kincaid grade</span></div><div class="stat"><b id="rcE">–</b><span>reading ease (0–100)</span></div>
  <div class="stat"><b id="rcA">–</b><span>average words per sentence</span></div><div class="stat"><b id="rcLong">0</b><span>long sentences (over 25 words)</span></div>
 </div>
 <div class="hl" id="rcH" hidden></div>
 <p class="key"><i style="background:var(--warn-bg);border-bottom:2px solid var(--warn)"></i>long sentence (25–34 words) <i style="background:var(--bad-bg);border-bottom:2px solid var(--bad)"></i>very long sentence (35+ words)</p>
 <p class="key">Works best with at least 100 words of English. Your text stays in this browser.</p>
</div>
<script>(()=>{''' + ENGINE + '''
const $=i=>document.getElementById(i),esc=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));$('rcT').value=store.get('dt-rc','');
const band=e=>e>=90?['very easy','about age 10 to 11']:e>=80?['easy','about age 11 to 12']:e>=70?['fairly easy','about age 12 to 13']:e>=60?['plain English','about age 13 to 15']:e>=50?['fairly difficult','high school']:e>=30?['difficult','college']:['very difficult','university graduate'];
function upd(){const t=$('rcT').value;store.set('dt-rc',t);const r=TA.fk(t),S=TA.sentences(t);
 if(!r||TA.words(t).length<10){$('rcL').textContent='Paste some text to see its reading level.';['rcG','rcE','rcA'].forEach(i=>$(i).textContent='–');$('rcLong').textContent=0;$('rcH').hidden=true;return}
 const g=Math.max(0,r.grade),e=Math.min(100,Math.max(0,r.ease)),[d,who]=band(e);
 $('rcG').textContent=g.toFixed(1);$('rcE').textContent=Math.round(e);$('rcA').textContent=r.wps.toFixed(1);
 $('rcL').innerHTML='<b>'+d[0].toUpperCase()+d.slice(1)+'</b> to read: about US grade '+Math.round(g)+' ('+who+').';
 let n=0;$('rcH').innerHTML=S.map(s=>{const k=TA.words(s).length;if(k>=25)n++;return k>=35?'<mark class="vl" title="'+k+' words">'+esc(s)+'</mark>':k>=25?'<mark title="'+k+' words">'+esc(s)+'</mark>':esc(s)}).join(' ');
 $('rcLong').textContent=n;$('rcH').hidden=false}
$('rcT').oninput=upd;upd()})();</script>'''

RC_TEXT = '''<h2>What the readability scores mean</h2>
<p>The checker uses two well-known formulas based on the length of your sentences and the number of syllables in your words. Longer sentences and longer words make text harder to read.</p>
<ul><li><b>Flesch–Kincaid grade level</b> estimates the US school grade needed to understand the text. A score of 8 means an average 8th-grade student (about age 13 to 14) should follow it.</li>
<li><b>Flesch reading ease</b> runs from 0 to 100. Higher is easier: 60 to 70 is plain English, 30 or below is very hard.</li></ul>
<table class="ptable"><thead><tr><th>Reading ease</th><th>How it reads</th><th>Good for</th></tr></thead><tbody>
<tr><td>80–100</td><td>Easy</td><td>Children’s stories, instructions for young students</td></tr>
<tr><td>60–80</td><td>Plain English</td><td>Most school writing, websites, emails, news</td></tr>
<tr><td>40–60</td><td>Fairly difficult</td><td>High school essays, reports</td></tr>
<tr><td>0–40</td><td>Difficult</td><td>Academic papers, legal and technical writing</td></tr></tbody></table>

<h2>Find the long sentences</h2>
<p>Below the scores, the checker shows your text with long sentences highlighted: yellow for 25 to 34 words and red for 35 or more. Long sentences aren’t wrong, but too many in a row make writing tiring to read. Try splitting one into two, or turning a list inside a sentence into bullet points.</p>

<h2>How to make writing easier to read</h2>
<ul><li><b>One idea per sentence.</b> If a sentence has three commas and an “and”, it may be two sentences.</li>
<li><b>Prefer short, common words.</b> <i>Use</i> instead of <i>utilize</i>, <i>help</i> instead of <i>facilitate</i>.</li>
<li><b>Mix sentence lengths.</b> A short sentence after two long ones gives the reader a rest. Like this.</li>
<li><b>Use active voice.</b> “The class planted the trees” is clearer than “The trees were planted by the class”.</li>
<li><b>Know your reader.</b> A science report for your teacher can be harder than a newsletter for parents.</li></ul>

<h2>For teachers</h2>
<p>Use the checker to match reading passages and instructions to your students’ level, or have students compare the reading level of two drafts. Readability formulas only measure sentence and word length; they don’t judge ideas, accuracy or style, so use them as one guide among many.</p>
<p>Want to see how a piece of writing was built, not just how it reads? Try <a href="/write/">writing in DraftTrail</a>, and count your words with the <a href="/tools/word-counter/">word counter</a>.</p>
<h2>Questions</h2>
<p><b>Does it work for other languages?</b> The formulas are designed for English. Scores for other languages won’t be accurate.</p>
<p><b>Is my text private?</b> Yes. Everything runs in your browser; nothing is uploaded.</p>'''

TOOLS = [
 ('/tools/word-counter/', 'Word Counter: Count Words, Characters and Reading Time', 'Word counter',
  'A free word counter: words, characters, sentences, paragraphs, reading and speaking time, plus a word goal. Private: your text never leaves your browser.', WC, WC_TEXT),
 ('/tools/readability-checker/', 'Readability Checker: Grade Level and Long Sentences', 'Readability checker',
  'Check the reading level of your writing with Flesch–Kincaid grade level and reading ease, and see long sentences highlighted. Free and private.', RC, RC_TEXT),
]
