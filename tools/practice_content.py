"""Word Choice Check (/practice/word-choice/): commonly confused words game + guide. Rendered by build.py."""

GAME_CSS = '''<style>
.game{max-width:620px;margin:8px auto 34px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;box-shadow:0 10px 30px rgba(20,27,43,.08)}
.game h2{margin:0 0 4px;font-size:22px}.game .gsub{margin:0 0 14px;color:var(--muted);font-size:15px}
.gchips{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 14px}
.gchips button{border:2px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:15px;font-weight:700;color:var(--fg);cursor:pointer}
.gchips button.on{border-color:var(--brand);background:var(--brand);color:#fff}
.glabel{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:4px 0 0}
.gbtn{display:block;width:100%;background:var(--brand);color:#fff;border:0;border-radius:12px;padding:14px;font:inherit;font-size:18px;font-weight:800;cursor:pointer}
.gbtn.ghost{background:transparent;color:var(--brand);border:2px solid var(--brand)}
.gbar{height:8px;background:#E6EAF2;border-radius:99px;overflow:hidden;margin-bottom:12px}.gbar i{display:block;height:100%;background:var(--badge);width:100%}
.gtop{display:flex;justify-content:space-between;font-weight:700;color:var(--muted);font-size:15px;margin-bottom:6px}
.gq{font-family:var(--head);font-weight:800;font-size:44px;text-align:center;margin:6px 0 4px;color:var(--fg)}
.gin{font-family:var(--head);font-weight:800;font-size:36px;text-align:center;min-height:54px;border:2px solid var(--line);border-radius:12px;margin:0 auto 12px;max-width:220px;background:var(--bg)}
.gin.ok{border-color:#2e9e5b;background:#e5f6ec}.gin.bad{border-color:#d64545;background:#fdeaea}
.pad{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;max-width:320px;margin:0 auto}
.pad button{font:inherit;font-size:24px;font-weight:800;padding:12px 0;border-radius:12px;border:1px solid var(--line);background:#fff;color:var(--fg);cursor:pointer;touch-action:manipulation}
.pad button:active{background:#E6EAF2}.pad .go{background:var(--brand);color:#fff;border-color:var(--brand)}
.gopts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0}
.gopts button{font:inherit;font-size:17px;font-weight:700;padding:14px 10px;border-radius:12px;border:2px solid var(--line);background:#fff;color:var(--fg);cursor:pointer;min-height:62px;touch-action:manipulation}
.gopts button.ok{border-color:#2e9e5b;background:#e5f6ec}.gopts button.bad{border-color:#d64545;background:#fdeaea}
.gopts button:disabled{cursor:default;opacity:1}
.gq2{font-family:var(--head);font-weight:800;font-size:24px;text-align:center;margin:8px 0 0;line-height:1.3}
.gres{text-align:center}.gbig{font-family:var(--head);font-weight:800;font-size:56px;color:var(--brand);line-height:1.1;margin:6px 0}
.gmiss{text-align:left;margin:14px 0;padding:0;list-style:none;border-top:1px solid var(--line)}
.gmiss li{padding:8px 4px;border-bottom:1px solid var(--line);font-size:16px}
.grow{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px}
.gfb{text-align:center;min-height:26px;font-weight:700;margin-top:2px}
.ptiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:18px 0}
.ptiles a{display:block;border:1px solid var(--line);border-radius:14px;padding:18px;background:var(--card);text-decoration:none;color:var(--fg)}
.ptiles b{display:block;font-size:20px;color:var(--brand);margin-bottom:4px}
@media(max-width:480px){.game{padding:16px 14px}.gq{font-size:38px}.gopts{grid-template-columns:1fr}}
</style>'''

# sentence with ___, choices, correct, why
WC = [
 ('Lack of sleep can ___ your memory.', ['affect','effect'], 'affect', '<b>Affect</b> is usually the verb (to influence). <b>Effect</b> is usually the noun (the result).'),
 ('The new schedule had a big ___ on attendance.', ['affect','effect'], 'effect', 'Here you need the noun, the result: an <b>effect</b>.'),
 ('This essay is longer ___ the last one.', ['then','than'], 'than', '<b>Than</b> compares. <b>Then</b> is about time: first this, then that.'),
 ('Finish your outline, and ___ start the first draft.', ['then','than'], 'then', '<b>Then</b> shows order in time.'),
 ('There were ___ students in the lab this week.', ['fewer','less'], 'fewer', 'Use <b>fewer</b> with things you can count (students), <b>less</b> with amounts (time, water).'),
 ('I have ___ time to study than I hoped.', ['fewer','less'], 'less', 'Time is an amount, not a count, so it’s <b>less</b> time.'),
 ('The university updated ___ admission policy.', ['its','it’s'], 'its', '<b>Its</b> shows ownership. <b>It’s</b> always means “it is” or “it has”.'),
 ('___ important to back up your files.', ['Its','It’s'], 'It’s', 'You can say “It is important”, so the answer is <b>It’s</b>.'),
 ('The students handed in ___ reports on Friday.', ['their','there','they’re'], 'their', '<b>Their</b> = belonging to them. <b>There</b> = a place. <b>They’re</b> = they are.'),
 ('___ planning to present the project together.', ['Their','There','They’re'], 'They’re', '“They are planning…” so it’s <b>They’re</b>.'),
 ('Put the printed copies over ___.', ['their','there','they’re'], 'there', '<b>There</b> refers to a place.'),
 ('Let me know when ___ ready to start.', ['your','you’re'], 'you’re', '“When you are ready” so it’s <b>you’re</b>.'),
 ('Don’t forget to cite ___ sources.', ['your','you’re'], 'your', '<b>Your</b> shows ownership: the sources belong to you.'),
 ('If you ___ your ID card, report it to the front desk.', ['lose','loose'], 'lose', '<b>Lose</b> means to misplace. <b>Loose</b> means not tight.'),
 ('The screw on my laptop hinge is ___.', ['lose','loose'], 'loose', '<b>Loose</b> means not tight.'),
 ('The ___ approved the new library hours.', ['principal','principle'], 'principal', 'A <b>principal</b> is the head of a school (or “main”). A <b>principle</b> is a rule or belief.'),
 ('Honesty is a core ___ of academic work.', ['principal','principle'], 'principle', 'A <b>principle</b> is a basic rule or value.'),
 ('She paid me a ___ on my presentation.', ['complement','compliment'], 'compliment', 'A <b>compliment</b> is praise. A <b>complement</b> completes or goes well with something.'),
 ('The charts ___ the written report nicely.', ['complement','compliment'], 'complement', 'The charts complete the report, so they <b>complement</b> it.'),
 ('Bring something to write with, ___ a pen or pencil.', ['i.e.','e.g.'], 'e.g.', '<b>e.g.</b> means “for example”. <b>i.e.</b> means “that is”, to say exactly which.'),
 ('Submit it by the deadline, ___ 11:59 p.m. on Friday.', ['i.e.','e.g.'], 'i.e.', 'This names the exact deadline, so it’s <b>i.e.</b> (“that is”).'),
 ('Everyone passed ___ the two who missed the exam.', ['accept','except'], 'except', '<b>Except</b> means “not including”. <b>Accept</b> means to receive or agree.'),
 ('The journal will ___ papers until March.', ['accept','except'], 'accept', '<b>Accept</b> means to receive.'),
 ('My advisor gave me good ___ about my thesis.', ['advice','advise'], 'advice', '<b>Advice</b> is the noun. <b>Advise</b> is the verb.'),
 ('I would ___ you to start early.', ['advice','advise'], 'advise', 'Here you need the verb: to <b>advise</b>.'),
 ('The course ___ five modules.', ['comprises','comprises of'], 'comprises', '<b>Comprises</b> already means “consists of”, so never add “of” after it.'),
 ('Last year, she ___ the research team.', ['lead','led'], 'led', 'The past tense of the verb “lead” is <b>led</b>.'),
 ('To ___ should I address the letter?', ['who','whom'], 'whom', 'After a preposition (to, for, with), use <b>whom</b>. Tip: if “him” fits, use whom.'),
 ('___ is presenting first?', ['Who','Whom'], 'Who', '“He is presenting”, not “him”, so it’s <b>Who</b>.'),
 ('The author ___ that the data was incomplete, without saying it directly.', ['implied','inferred'], 'implied', 'The writer <b>implies</b> (suggests). The reader <b>infers</b> (works it out).'),
 ('From the results, we ___ that the method worked.', ['implied','inferred'], 'inferred', 'The reader draws the conclusion, so it’s <b>inferred</b>.'),
 ('The prize was divided ___ the two finalists.', ['between','among'], 'between', 'Use <b>between</b> for two people or things.'),
 ('The snacks were shared ___ the whole class.', ['between','among'], 'among', 'Use <b>among</b> for a group of three or more.'),
 ('The library is ___ from the dorms than the gym.', ['farther','further'], 'farther', '<b>Farther</b> is for physical distance. <b>Further</b> means more, or to a greater degree.'),
 ('We need ___ research before we decide.', ['farther','further'], 'further', '“More research” is <b>further</b> research.'),
 ('Please ___ that all sources are listed.', ['ensure','insure'], 'ensure', '<b>Ensure</b> means make sure. <b>Insure</b> is about insurance.'),
 ('I ___ finished earlier if the Wi-Fi had worked.', ['could have','could of'], 'could have', 'It’s always <b>could have</b> (or could’ve). “Could of” is a mishearing.'),
 ('The topic really ___ my interest.', ['peaked','piqued'], 'piqued', 'To <b>pique</b> interest is to stir it up. A <b>peak</b> is a top point.'),
 ('I’m not sure ___ the class is online today.', ['weather','whether'], 'whether', '<b>Whether</b> introduces a choice or doubt. <b>Weather</b> is rain and sun.'),
 ('The survey was designed to ___ honest answers.', ['elicit','illicit'], 'elicit', '<b>Elicit</b> means to draw out. <b>Illicit</b> means illegal.'),
 ('Always ___ the original study, not just a summary of it.', ['cite','site','sight'], 'cite', 'To <b>cite</b> is to quote or reference. A <b>site</b> is a place. <b>Sight</b> is seeing.'),
 ('Please keep this information ___; it’s confidential.', ['discreet','discrete'], 'discreet', '<b>Discreet</b> means careful and private. <b>Discrete</b> means separate.'),
 ('The data was grouped into five ___ categories.', ['discreet','discrete'], 'discrete', '<b>Discrete</b> means separate and distinct.'),
 ('I bought ___ for the event: envelopes, paper and cards.', ['stationary','stationery'], 'stationery', '<b>Stationery</b> is paper and envelopes (e for envelope). <b>Stationary</b> means not moving.'),
]

def wc_game():
    import json
    Q = json.dumps(WC, ensure_ascii=False)
    return '''<div class="game" id="wc">
 <div id="wcSetup">
  <h2>Word Choice Check</h2><p class="gsub">Pick the right word for each sentence. 10 sentences a round.</p>
  <p style="margin:4px 0 14px;font-size:16px">Affect or effect? Fewer or less? Its or it’s? After each answer you’ll see a quick rule to remember.</p>
  <button class="gbtn" id="wcStart">Start</button>
 </div>
 <div id="wcPlay" hidden>
  <div class="gtop"><span id="wcNum"></span><span>Score: <b id="wcScore">0</b></span></div>
  <div class="gbar"><i id="wcBar"></i></div>
  <div class="wsent" id="wcQ"></div>
  <div class="gopts" id="wcOpts"></div>
  <div class="gfb fexp" id="wcFb"></div>
  <button class="gbtn" id="wcNext" hidden>Next</button>
 </div>
 <div id="wcEnd" class="gres" hidden>
  <p class="glabel">Round complete</p><div class="gbig" id="wcFinal"></div><p id="wcNote" class="muted"></p>
  <ul class="gmiss" id="wcMiss"></ul>
  <div class="grow"><button class="gbtn" id="wcAgain">Play again</button><a class="gbtn ghost" href="#guide" style="text-align:center;text-decoration:none">Read the guide</a></div>
 </div>
</div>
<style>.wsent{font-size:21px;line-height:1.5;text-align:center;margin:14px 0 4px;font-weight:600}.wsent u{display:inline-block;min-width:70px;text-decoration:none;border-bottom:3px solid var(--badge);padding:0 4px}
.fexp{text-align:left;font-weight:400;font-size:16px;line-height:1.5;margin:4px 0 12px}.fexp>b:first-child{display:block}
#wcOpts{grid-template-columns:repeat(auto-fit,minmax(120px,1fr))}</style>
<script>
(()=>{const Q=''' + Q + ''';
const $=i=>document.getElementById(i),sh=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const esc=t=>t.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
const get=k=>{try{return +localStorage.getItem(k)||0}catch(e){return 0}},put=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
let qs=[],n=0,score=0,miss=[],locked=false;
function start(){qs=sh(Q).slice(0,10);n=0;score=0;miss=[];$('wcScore').textContent=0;$('wcSetup').hidden=true;$('wcEnd').hidden=true;$('wcPlay').hidden=false;ask();$('wc').scrollIntoView({block:'nearest'})}
function fill(q,w){return esc(q[0]).replace('___','<u>'+(w?esc(w):'&nbsp;')+'</u>')}
function ask(){const q=qs[n];locked=false;$('wcNum').textContent='Sentence '+(n+1)+' of '+qs.length;$('wcBar').style.width=(n/qs.length*100)+'%';
 $('wcQ').innerHTML=fill(q);$('wcOpts').innerHTML='';$('wcFb').innerHTML='';$('wcNext').hidden=true;
 q[1].forEach(o=>{const b=document.createElement('button');b.textContent=o;b.onclick=()=>choose(b,o);$('wcOpts').appendChild(b)})}
function choose(b,o){if(locked)return;locked=true;const q=qs[n],ok=o===q[2];
 document.querySelectorAll('#wcOpts button').forEach(x=>{x.disabled=true;if(x.textContent===q[2])x.classList.add('ok')});
 if(ok){score++;$('wcScore').textContent=score}else{b.classList.add('bad');miss.push(q)}
 $('wcQ').innerHTML=fill(q,q[2]);
 $('wcFb').innerHTML='<b style="color:'+(ok?'#2e9e5b':'#b23a3a')+'">'+(ok?'Correct!':'Not quite.')+'</b>'+q[3];
 $('wcNext').textContent=n+1<qs.length?'Next':'See my score';$('wcNext').hidden=false}
$('wcNext').onclick=()=>{n++;if(n<qs.length)ask();else end()};
document.addEventListener('keydown',e=>{if($('wcPlay').hidden)return;const bs=document.querySelectorAll('#wcOpts button');
 if(!locked&&/^[1-3]$/.test(e.key)&&bs[+e.key-1]){bs[+e.key-1].click();e.preventDefault()}else if(locked&&e.key==='Enter'){$('wcNext').click();e.preventDefault()}});
function end(){$('wcBar').style.width='100%';$('wcPlay').hidden=true;$('wcEnd').hidden=false;const best=get('dt-wc');
 $('wcFinal').textContent=score+' / '+qs.length;$('wcNote').textContent=score===10?'Perfect round!':score>best?'New best score!':'Your best: '+best+' / 10';if(score>best)put('dt-wc',score);
 $('wcMiss').innerHTML=miss.length?'<li><b>Review these:</b></li>'+miss.map(q=>'<li>'+fill(q,q[2])+'</li>').join(''):'<li>No mistakes. Play again for new sentences.</li>'}
$('wcStart').onclick=start;$('wcAgain').onclick=start;})();
</script>'''

PAIRS = [
 ('Affect / effect', '<b>Affect</b> is usually a verb: stress can affect sleep. <b>Effect</b> is usually a noun: the effect of stress. Memory trick: <i>A</i> for action (affect), <i>E</i> for end result (effect).'),
 ('Then / than', '<b>Than</b> compares (bigger than). <b>Then</b> is about time or order (first this, then that).'),
 ('Fewer / less', '<b>Fewer</b> for things you can count (fewer pages). <b>Less</b> for amounts (less time, less money).'),
 ('Its / it’s', '<b>It’s</b> = it is or it has. <b>Its</b> = belonging to it. If you can’t say “it is”, write its.'),
 ('Their / there / they’re', '<b>Their</b> = belonging to them. <b>There</b> = a place. <b>They’re</b> = they are.'),
 ('Your / you’re', '<b>You’re</b> = you are. <b>Your</b> = belonging to you.'),
 ('Lose / loose', '<b>Lose</b> = to misplace or not win. <b>Loose</b> = not tight.'),
 ('Principal / principle', '<b>Principal</b> = head of a school, or main. <b>Principle</b> = a rule or value.'),
 ('Complement / compliment', '<b>Complement</b> = completes or goes well with. <b>Compliment</b> = praise. Trick: a compl<i>e</i>ment compl<i>e</i>tes.'),
 ('i.e. / e.g.', '<b>e.g.</b> = for example (one of several). <b>i.e.</b> = that is (exactly this). Trick: e.g. = “example given”.'),
 ('Accept / except', '<b>Accept</b> = receive or agree. <b>Except</b> = not including.'),
 ('Advice / advise', '<b>Advice</b> is the noun (good advice). <b>Advise</b> is the verb (I advise you).'),
 ('Comprise / consist of', '<b>Comprise</b> already includes “of”: the course comprises five modules, or consists of five modules. Avoid “comprises of”.'),
 ('Lead / led', 'The past tense of the verb <b>lead</b> is <b>led</b>. (Lead, pronounced “led”, is also a metal, which causes the confusion.)'),
 ('Who / whom', '<b>Who</b> does the action (who wrote this?). <b>Whom</b> receives it (to whom it may concern). If “him” fits, use whom.'),
 ('Imply / infer', 'The speaker or writer <b>implies</b>. The listener or reader <b>infers</b>.'),
 ('Between / among', '<b>Between</b> for two. <b>Among</b> for three or more in a group.'),
 ('Farther / further', '<b>Farther</b> for physical distance. <b>Further</b> for more or additional (further study).'),
 ('Ensure / insure', '<b>Ensure</b> = make sure. <b>Insure</b> = protect with insurance.'),
 ('Could have / could of', 'Always <b>could have</b>, should have, would have. “Could of” comes from how “could’ve” sounds.'),
 ('Peak / peek / pique', '<b>Peak</b> = top. <b>Peek</b> = quick look. <b>Pique</b> = stir up (it piqued my interest).'),
 ('Weather / whether', '<b>Weather</b> = rain and sun. <b>Whether</b> = if, or a choice between options.'),
 ('Elicit / illicit', '<b>Elicit</b> = draw out (a response). <b>Illicit</b> = illegal or not allowed.'),
 ('Cite / site / sight', '<b>Cite</b> = reference a source. <b>Site</b> = a place or website. <b>Sight</b> = vision.'),
 ('Discreet / discrete', '<b>Discreet</b> = careful and private. <b>Discrete</b> = separate and distinct.'),
 ('Stationary / stationery', '<b>Stationary</b> = not moving. <b>Stationery</b> = paper and envelopes (e for envelope).'),
]

def wc_text():
    rows = ''.join(f'<h3>{a}</h3><p>{b}</p>' for a, b in PAIRS)
    return f'''<h2 id="guide">Why these words get mixed up</h2>
<p>Most confused words sound alike, look alike, or both. Spell checkers don’t catch them, because each word is spelled correctly. It’s just the wrong word. That’s why they slip into essays, emails and even published papers, and why readers notice them.</p>
<p>The good news: there are only a few dozen common pairs, and each one has a simple rule. Learn the rule, practice it a few times, and the mistake usually disappears for good.</p>

<h2>Commonly confused words: a quick guide</h2>
{rows}

<h2>How to catch them in your own writing</h2>
<ul><li><b>Read your draft out loud.</b> Swap in the long form: if “it is” or “you are” fits, use the apostrophe.</li>
<li><b>Search for your problem words.</b> If you often mix up affect and effect, use Find (Ctrl+F or ⌘F) and check each one.</li>
<li><b>Keep a personal list.</b> Write down the pairs you miss in this game and check for them before you submit.</li>
<li><b>Proofread after a break.</b> Fresh eyes catch more than a fifth re-read right after writing.</li></ul>

<h2>For teachers</h2>
<p>Word Choice Check works as a quick warm-up before a writing task, as homework, or as a mini-lesson on one pair at a time. It’s free, there’s no sign-up, and scores stay on the student’s device. When students write in class, <a href="/">DraftTrail</a> shows how each piece of writing was built, from the first word to the final draft.</p>
<p>More practice for students: try <a href="https://quizpolice.telarlabs.net/practice/spot-the-fallacy/">Spot the Fallacy</a> to sharpen your arguments, or the other <a href="https://quizpolice.telarlabs.net/practice/">practice games on QuizPolice</a>.</p>

<h2>Questions</h2>
<p><b>Is “effect” ever a verb?</b> Yes, in “to effect change”, meaning to bring it about. And “affect” can be a noun in psychology. Those uses are rarer, so the everyday rule is a good start.</p>
<p><b>Is it free?</b> Yes, completely.</p>'''
