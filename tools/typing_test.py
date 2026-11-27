"""Typing speed test (/tools/typing-test/): WPM and accuracy, made in the browser. Nothing is sent anywhere."""

WORDS = ('the be to of and a in that have it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about '
 'who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after '
 'use two how our work first well way even new want because any these give day most us is was are been has had were said did made find long down side been called water oil sit '
 'part place sound number little very after thing name great help through much before line right too mean old same tell boy follow came want show also around form three small set put '
 'end does another well large must big even such turn here why ask went men read need land different home move try kind hand picture again change off play spell air away animal house '
 'point page letter mother answer found study still learn should world high every near add food between own below country plant last school father keep tree never start city earth eye '
 'light thought head under story saw left few while along might close something seem next hard open example begin life always those both paper together got group often run important '
 'until children feet car mile night walk white sea began grow took river four carry state once book hear stop without second later miss idea enough eat face watch far really almost let').split()

PASSAGES = [
 'The library was quiet except for the soft turning of pages. Near the window, a girl traced the map of a faraway island with one finger, already planning the trip she would take one day.',
 'Bees visit hundreds of flowers on a single trip. As they collect nectar, they carry pollen from one blossom to the next, helping fruits and vegetables grow in gardens and on farms.',
 'Our class planted beans in paper cups and set them by the window. Every morning we measured the stems, and by Friday the tallest one had grown taller than a pencil.',
 'A good habit is small enough to start today. Read for ten minutes, drink a glass of water, or write one kind note. Little steps, repeated often, add up to big changes.',
 'The ocean covers more than two thirds of our planet. Deep below the waves, there are mountains, valleys and creatures that glow in the dark, many of them still waiting to be discovered.',
 'When the power went out, the family gathered around a single candle. Grandpa told stories about the village where he grew up, and no one noticed when the lights came back on.',
 'Practice does not have to be perfect to be useful. Every mistake shows you what to try next, and every try makes the next one a little easier.',
 'The train left the station just after sunrise. Fields of rice slid past the windows, and farmers in wide hats waved as the long carriages rolled toward the city.',
 'Clouds form when warm air rises and cools. Tiny drops of water gather around specks of dust, and when enough drops join together, they fall back to the ground as rain.',
 'Before a big test, a good night of sleep can help more than one more hour of studying. A rested brain remembers facts better and solves problems faster.',
 'The market opened early on Saturdays. There were baskets of mangoes, stacks of fresh bread, and a man who sold kites in every color you could imagine.',
 'Writing is thinking on paper. A first draft only needs to exist; you can make it clear, short and strong later, one sentence at a time.',
 'Owls can turn their heads much farther than people can. Their large eyes cannot move in their sockets, so they look around by turning their whole head instead.',
 'The team lost the first game, but nobody gave up. They practiced passing every afternoon, and by the end of the season they were cheering for a trophy of their own.',
 'Saving money is easier with a plan. Decide what you want, write down how much it costs, and put aside a small amount each week until you reach your goal.',
]

TT = r'''
<div class="tt" id="tt">
 <p class="tt-ch" id="ttCh" hidden></p>
 <div class="tt-opts" id="ttOpts">
  <div class="tt-seg" id="ttTime"><button type="button" data-v="15">15 s</button><button type="button" data-v="30">30 s</button><button type="button" data-v="60">1 min</button><button type="button" data-v="120">2 min</button></div>
  <div class="tt-seg" id="ttMode"><button type="button" data-v="words">Common words</button><button type="button" data-v="text">Sentences</button><button type="button" data-v="custom">My own text</button></div>
 </div>
 <textarea id="ttCustom" class="tt-custom" rows="4" placeholder="Paste or type the text to practice: a vocabulary list, a speech, a passage from class…" hidden></textarea>
 <div class="tt-live"><span><b id="ttLeft">60</b> s left</span><span><b id="ttWpm">0</b> WPM</span><span><b id="ttAcc">100</b>% accuracy</span></div>
 <div class="tt-box" id="ttBox" tabindex="0" aria-label="Typing area. Start typing to begin."><div class="tt-text" id="ttText"></div><div class="tt-hint" id="ttHint">Tap here and start typing. The timer starts with your first key.</div></div>
 <textarea id="ttIn" class="tt-in" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" aria-label="Type here"></textarea>
 <div class="tt-row"><button type="button" class="pri" id="ttNew">↻ New test</button><span class="muted small tt-kb">Tab + Enter also starts a new test</span></div>
 <div class="tt-res" id="ttRes" hidden>
  <div class="tt-big"><div><b id="rWpm">0</b><span>words per minute</span></div><div><b id="rAcc">0%</b><span>accuracy</span></div></div>
  <div class="tt-stats"><div><b id="rRaw">0</b><span>raw WPM</span></div><div><b id="rOk">0</b><span>correct characters</span></div><div><b id="rBad">0</b><span>mistakes</span></div><div><b id="rBest">0</b><span>your best (WPM)</span></div></div>
  <p class="tt-lvl" id="rLvl"></p>
  <div class="tt-hist" id="rHist"></div>
  <div class="tt-row"><button type="button" class="pri" id="ttAgain">↻ Try again</button><button type="button" id="ttSame">Same text again</button><button type="button" id="ttChal">🎯 Challenge a friend</button></div>
  <p class="muted small" id="ttChalMsg" hidden></p>
 </div>
</div>
<style>
.tt{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px;margin:8px 0 34px;box-shadow:0 10px 30px rgba(20,27,43,.07)}
.tt [hidden]{display:none!important}
.tt-ch{background:var(--ok-bg);color:var(--ok);border-radius:10px;padding:9px 12px;margin:0 0 12px;font-weight:600}
.tt-opts{display:flex;flex-wrap:wrap;gap:10px;justify-content:space-between;margin-bottom:12px}
.tt-seg{display:flex;gap:4px;background:var(--bg);border:1px solid var(--line);border-radius:999px;padding:3px;flex-wrap:wrap}
.tt-seg button{border:0;background:none;border-radius:999px;padding:7px 12px;font:inherit;font-weight:700;font-size:14px;color:var(--muted);cursor:pointer}.tt-seg button.on{background:var(--brand);color:#fff}
.tt-custom{width:100%;border:1px solid var(--line);border-radius:12px;padding:10px 12px;font:16px/1.5 var(--body);margin-bottom:12px;background:var(--bg);box-sizing:border-box}
.tt-live{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:15px;margin-bottom:8px}.tt-live b{color:var(--brand);font-size:22px;font-family:var(--head)}
.tt-box{position:relative;border:2px solid var(--line);border-radius:14px;background:#fff;padding:14px 16px;height:calc(3 * 1.75em + 28px);overflow:hidden;font:clamp(19px,2.6vw,24px)/1.75 ui-monospace,"SF Mono",Menlo,Consolas,monospace;cursor:text}
.tt-box:focus-within,.tt-box.on{border-color:var(--brand);box-shadow:0 0 0 3px rgba(31,63,122,.12)}
.tt-text{color:#9aa3b2;white-space:pre-wrap;word-break:normal;overflow-wrap:break-word}.tt-text .ok{color:var(--fg)}.tt-text .no{color:var(--bad);background:var(--bad-bg);border-radius:3px}
.tt-text .cur{border-left:2px solid var(--brand);margin-left:-2px;animation:ttb 1s steps(1) infinite}@keyframes ttb{50%{border-color:transparent}}
.tt-hint{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;text-align:center;background:rgba(255,255,255,.86);font:600 17px/1.4 var(--body);color:var(--brand);padding:10px}
.tt-in{position:absolute;opacity:0;pointer-events:none;width:1px;height:1px;left:-9999px}
.tt-row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:12px}
.tt button.pri,.tt-row button{font:inherit;font-weight:700;font-size:15px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--fg);padding:9px 16px;cursor:pointer}.tt .pri{background:var(--brand)!important;color:#fff!important;border-color:var(--brand)!important}
.tt-res{margin-top:16px;border-top:1px solid var(--line);padding-top:16px}
.tt-big{display:grid;grid-template-columns:1fr 1fr;gap:12px}.tt-big div{background:var(--info-bg);border-radius:14px;padding:14px;text-align:center}.tt-big b{display:block;font:800 clamp(44px,9vw,64px)/1 var(--head);color:var(--brand)}.tt-big span{color:var(--muted);font-size:14px}
.tt-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-top:10px}.tt-stats div{border:1px solid var(--line);border-radius:12px;padding:10px 12px}.tt-stats b{display:block;font:700 22px var(--head);color:var(--fg)}.tt-stats span{font-size:13px;color:var(--muted)}
.tt-lvl{background:var(--bg);border-radius:12px;padding:12px 14px;margin:12px 0 0}
@media(hover:none),(max-width:600px){.tt-kb{display:none}}
.tt-box .tt-text{-webkit-mask-image:linear-gradient(#000 70%,transparent 100%);mask-image:linear-gradient(#000 70%,transparent 100%)}
.tt-hist{margin-top:10px}.tt-hist svg{width:100%;height:70px;display:block}.tt-hist p{margin:4px 0 0;font-size:13px;color:var(--muted)}
</style>
<script>(function(){
var WORDS=__WORDS__,PAS=__PAS__;
var $=function(i){return document.getElementById(i)};
function keep(k,v){try{if(v===undefined)return JSON.parse(localStorage.getItem(k)||'null');localStorage.setItem(k,JSON.stringify(v))}catch(e){return null}}
function rng(seed){return function(){seed|=0;seed=seed+0x6D2B79F5|0;var t=Math.imul(seed^seed>>>15,1|seed);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
var P=keep('dt-typing')||{t:60,mode:'words',custom:'',hist:[],best:0};P.hist=P.hist||[];
var q=new URLSearchParams(location.search),chal=null;
if(q.get('seed')){chal={seed:+q.get('seed')||1,t:+q.get('t')||60,mode:q.get('m')==='text'?'text':'words',wpm:+q.get('wpm')||0};P.t=chal.t;P.mode=chal.mode;$('ttCh').hidden=false;
 $('ttCh').textContent=chal.wpm?'🎯 A friend typed '+chal.wpm+' WPM on this test. Can you beat them? Same text, same time.':'🎯 You got a typing challenge: same text, same time.';history.replaceState(null,'',location.pathname)}
var T='',seed=chal?chal.seed:Math.floor(Math.random()*1e9),typed='',start=0,timer=0,done=false,keys=0,keyOk=0,spans=[];
function save(){keep('dt-typing',P)}
function gen(){var r=rng(seed);if(P.mode==='custom'){var c=P.custom.replace(/\s+/g,' ').trim();return c||'Type your own text in the box above, then start typing.'}
 if(P.mode==='text'){var idx=PAS.map(function(_,i){return i});for(var i=idx.length-1;i>0;i--){var j=Math.floor(r()*(i+1)),t=idx[i];idx[i]=idx[j];idx[j]=t}return idx.map(function(i){return PAS[i]}).join(' ')}
 var out=[];for(var k=0;k<(P.t<=30?120:P.t*3);k++)out.push(WORDS[Math.floor(r()*WORDS.length)]);return out.join(' ')}
function setUI(){[].forEach.call($('ttTime').children,function(b){b.classList.toggle('on',+b.dataset.v===P.t)});[].forEach.call($('ttMode').children,function(b){b.classList.toggle('on',b.dataset.v===P.mode)});
 $('ttCustom').hidden=P.mode!=='custom';$('ttCustom').value=P.custom}
function reset(sameText){clearInterval(timer);if(!sameText&&!chal)seed=Math.floor(Math.random()*1e9);T=gen();typed='';start=0;done=false;keys=0;keyOk=0;$('ttIn').value='';$('ttIn').disabled=false;
 $('ttText').innerHTML=T.split('').map(function(c){return '<span>'+(c==='<'?'&lt;':c==='&'?'&amp;':c)+'</span>'}).join('');spans=$('ttText').children;
 $('ttLeft').textContent=P.t;$('ttWpm').textContent=0;$('ttAcc').textContent=100;$('ttRes').hidden=true;$('ttHint').hidden=false;$('ttBox').scrollTop=0;$('ttText').style.transform='';paint();}
function paint(){for(var i=0;i<spans.length;i++){var s=spans[i];s.className=i<typed.length?(typed[i]===T[i]?'ok':'no'):(i===typed.length?'cur':'')}
 var cur=spans[Math.min(typed.length,spans.length-1)];if(cur){var lh=parseFloat(getComputedStyle($('ttBox')).lineHeight)||40,top=cur.offsetTop;$('ttText').style.transform='translateY('+(-Math.max(0,top-lh))+'px)'}}
function stats(){var el=start?Math.max(.5,(Date.now()-start)/1000):0,ok=0;for(var i=0;i<typed.length;i++)if(typed[i]===T[i])ok++;var m=el/60;
 return {el:el,ok:ok,bad:typed.length-ok,wpm:m?Math.max(0,Math.round(ok/5/m)):0,raw:m?Math.round(typed.length/5/m):0,acc:keys?Math.round(keyOk/keys*100):100}}
function tick(){var s=stats(),left=Math.max(0,P.t-s.el);$('ttLeft').textContent=Math.ceil(left);$('ttWpm').textContent=s.wpm;$('ttAcc').textContent=s.acc;if(left<=0)finish()}
function finish(){if(done)return;done=true;clearInterval(timer);$('ttIn').disabled=true;$('ttIn').blur();var s=stats();if(s.el>P.t)s.el=P.t;
 var m=Math.min(s.el,P.t)/60;s.wpm=Math.round(s.ok/5/m);s.raw=Math.round(typed.length/5/m);
 $('rWpm').textContent=s.wpm;$('rAcc').textContent=s.acc+'%';$('rRaw').textContent=s.raw;$('rOk').textContent=s.ok;$('rBad').textContent=keys-keyOk;
 var nb=s.wpm>P.best&&s.acc>=80;if(nb)P.best=s.wpm;$('rBest').textContent=P.best+(nb?' 🎉':'');
 P.hist.push({w:s.wpm,a:s.acc,t:P.t,d:Date.now()});P.hist=P.hist.slice(-20);save();
 var lv=s.wpm<20?'Getting started. Keep your eyes on the screen and your fingers on the home row (A S D F, J K L ;). Speed comes with practice.':s.wpm<35?'A steady pace. Many students type 25 to 40 WPM. Aim for 95% accuracy first, then speed.':s.wpm<50?'Good speed, around the average for adults (about 40 WPM). Keep accuracy high as you push faster.':s.wpm<70?'Fast! You type well above average. Try the 2-minute test to build endurance.':'Excellent! That’s professional-level typing speed.';
 $('rLvl').innerHTML=(chal&&chal.wpm?(s.wpm>chal.wpm?'<b>🏆 You beat your friend’s '+chal.wpm+' WPM!</b> ':s.wpm===chal.wpm?'<b>🤝 A tie with your friend at '+chal.wpm+' WPM!</b> ':'<b>Your friend got '+chal.wpm+' WPM. Try again?</b> '):'')+(s.acc<90?'<b>Slow down a little:</b> accuracy under 90% costs more time than it saves. ':'')+lv;
 var H=P.hist.slice(-12),mx=Math.max(10,...H.map(function(x){return x.w})),W=300,pts=H.map(function(x,i){return [(H.length<2?W/2:i*W/(H.length-1)),62-x.w/mx*54]});
 $('rHist').innerHTML=H.length>1?'<svg viewBox="-6 0 312 70" preserveAspectRatio="none"><polyline fill="none" stroke="#1F3F7A" stroke-width="2.5" vector-effect="non-scaling-stroke" points="'+pts.map(function(p){return p.join(',')}).join(' ')+'"/>'+pts.map(function(p){return '<circle cx="'+p[0]+'" cy="'+p[1]+'" r="3.5" fill="#1F3F7A"/>'}).join('')+'</svg><p>Your last '+H.length+' tests on this device: '+H.map(function(x){return x.w}).join(', ')+' WPM</p>':'';
 $('ttRes').hidden=false;$('ttRes').scrollIntoView({behavior:'smooth',block:'nearest'});window.__ttLast=s}
$('ttIn').addEventListener('input',function(){if(done)return;var v=this.value.replace(/\n/g,' ');if(v.length>T.length)v=v.slice(0,T.length);
 if(!start&&v.length){start=Date.now();timer=setInterval(tick,200);$('ttHint').hidden=true}
 if(v.length>typed.length){for(var i=typed.length;i<v.length;i++){keys++;if(v[i]===T[i])keyOk++}}
 typed=v;if(this.value!==v)this.value=v;paint();if(typed.length>=T.length)finish()});
$('ttIn').addEventListener('keydown',function(e){if(e.key==='Tab'){e.preventDefault();$('ttNew').focus()}});
var focusIn=function(){if(!done){$('ttIn').focus({preventScroll:true});$('ttBox').classList.add('on')}};
$('ttBox').addEventListener('click',focusIn);$('ttBox').addEventListener('keydown',function(e){if(e.key.length===1||e.key==='Enter'){focusIn()}});
$('ttIn').addEventListener('blur',function(){$('ttBox').classList.remove('on')});
$('ttNew').onclick=function(){chal=null;$('ttCh').hidden=true;reset(false);focusIn()};$('ttAgain').onclick=function(){chal=null;$('ttCh').hidden=true;reset(false);focusIn()};$('ttSame').onclick=function(){reset(true);focusIn()};
[].forEach.call($('ttTime').children,function(b){b.onclick=function(){P.t=+b.dataset.v;save();setUI();reset(false)}});
[].forEach.call($('ttMode').children,function(b){b.onclick=function(){P.mode=b.dataset.v;chal=null;$('ttCh').hidden=true;save();setUI();reset(false);if(P.mode==='custom')$('ttCustom').focus()}});
$('ttCustom').oninput=function(){P.custom=this.value;save();reset(true)};
$('ttChal').onclick=function(){var s=window.__ttLast||{wpm:0},u=location.origin+location.pathname+'?seed='+seed+'&t='+P.t+'&m='+(P.mode==='text'?'text':'words')+(s.wpm?'&wpm='+s.wpm:''),b=this,msg=$('ttChalMsg');
 var txt='I typed '+s.wpm+' words per minute on this typing test. Can you beat me? Same text, same time: '+u;
 function ok(){b.textContent='✓ Link copied';msg.hidden=false;msg.textContent='Send it to a friend or your class group. They get the same text and time.';setTimeout(function(){b.textContent='🎯 Challenge a friend'},2200)}
 if(P.mode==='custom'){msg.hidden=false;msg.textContent='Challenges work with Common words or Sentences, so your friend gets the same text.';return}
 if(navigator.share&&/Android|iPhone|iPad/i.test(navigator.userAgent))navigator.share({text:txt}).catch(function(){});else if(navigator.clipboard)navigator.clipboard.writeText(txt).then(ok,function(){window.prompt('Copy this:',txt)});else window.prompt('Copy this:',txt)};
setUI();reset(true);
})();</script>'''

def tool():
    import json
    return TT.replace('__WORDS__', json.dumps(WORDS)).replace('__PAS__', json.dumps(PASSAGES))

TEXT = '''
<h2>How the typing test works</h2>
<ol><li>Choose a time: 15 seconds, 30 seconds, 1 minute or 2 minutes.</li>
<li>Choose the text: <b>Common words</b> (the most-used English words), <b>Sentences</b> (short paragraphs with capitals and punctuation), or <b>My own text</b> to practice a vocabulary list, a speech or a passage from class.</li>
<li>Start typing. The timer starts with your first key. Correct letters turn dark, mistakes turn red, and you can fix them with Backspace.</li>
<li>When time is up, you see your words per minute (WPM), accuracy and mistakes, your best score and your last tests on this device.</li></ol>
<h2>How WPM is calculated</h2>
<p>A “word” in typing tests is any 5 characters, including spaces, so long and short words count fairly. <b>WPM</b> counts only the characters you typed correctly: correct characters ÷ 5 ÷ minutes. <b>Raw WPM</b> counts everything you typed, mistakes included. <b>Accuracy</b> is the share of keys you pressed correctly the first time, so fixed mistakes still count against it.</p>
<p>Example: in 1 minute you type 230 characters, and 220 of them are correct. Your WPM is 220 ÷ 5 = <b>44 WPM</b>, and your raw WPM is 46.</p>
<h2>What is a good typing speed?</h2>
<ul><li><b>Getting started:</b> under 20 WPM. Everyone starts here.</li><li><b>Students:</b> many type around 25 to 40 WPM.</li><li><b>Average adult:</b> about 40 WPM.</li><li><b>Fast:</b> 60 WPM and up. Professional typists often reach 70 to 90 WPM.</li></ul>
<p>Accuracy matters more than speed. Aim for <b>95% or higher</b>; then let speed grow.</p>
<h2>Tips to type faster</h2>
<ul><li><b>Use the home row.</b> Rest your left fingers on A S D F and your right on J K L ;. The bumps on F and J help you find them without looking.</li>
<li><b>Don’t look at the keyboard.</b> It feels slower at first, but it’s the fastest way to improve.</li>
<li><b>Keep a steady rhythm</b> instead of rushing and stopping.</li>
<li><b>Practice a little every day.</b> Five minutes daily beats an hour once a week.</li>
<li><b>Sit up straight</b>, with your wrists relaxed and the screen at eye level.</li></ul>
<h2>For teachers</h2>
<ul><li><b>Class challenge:</b> run a 1-minute test, then tap <b>Challenge a friend</b> and share the link. Everyone gets the same text, so scores are fair to compare.</li>
<li><b>Warm-up before writing:</b> a 30-second test gets fingers ready for an in-class essay in <a href="/write/">DraftTrail</a>.</li>
<li><b>Vocabulary practice:</b> paste this week’s words into <b>My own text</b>.</li></ul>
<h2>Questions</h2>
<h3>Can I take the test on a phone?</h3><p>Yes. Tap the text and type with your phone’s keyboard. Scores are usually lower than on a real keyboard, so compare phone scores with phone scores.</p>
<h3>Are my results saved?</h3><p>Only in this browser on this device: your best score and your last 20 tests. Nothing is sent to us.</p>'''

TOOL = ('/tools/typing-test/', 'Typing Speed Test: Free WPM and Accuracy Test (1 Minute)', 'Typing speed test',
        'Take a free typing speed test: 15 seconds to 2 minutes, common words, sentences or your own text. See your WPM, accuracy and best score, and challenge a friend. No sign-up.', tool(), TEXT)
