// Bakas core: rebuild text from recorded edits, analyze the writing process, draw the chart.
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const words=s=>(s.trim().match(/\S+/g)||[]).length;
const mmss=ms=>{const s=Math.round(ms/1000);return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`};
/* ---------- reconstruct + analyze ---------- */
function apply(arr,op){ arr.splice(op.p,op.d,...[...op.i].map(ch=>({ch,o:op.k==='type'?'t':'p'}))) }
function build(ops,n){const a=[]; for(let i=0;i<n;i++) apply(a,ops[i]); return a}
function analyze(ops){
  const fin=build(ops,ops.length), text=fin.map(c=>c.ch).join('');
  let typed=0,pasted=0,deleted=0,active=0,sessions=ops.length?1:0,pauses=0,longest=0; const pastes=[];
  ops.forEach((o,i)=>{ if(o.k==='type') typed+=o.i.length; else {pasted+=o.i.length; pastes.push(o)} deleted+=o.d;
    if(i){const g=o.t-ops[i-1].t; active+=Math.min(g,30000); if(g>5000) pauses++; if(g>300000) sessions++; longest=Math.max(longest,g)} });
  const keptPaste=fin.filter(c=>c.o==='p').length, pastePct=text.length?Math.round(keptPaste/text.length*100):0;
  const wpm=active?Math.round((typed/5)/(active/60000)):0, w=words(text), rev=typed?Math.round(deleted/typed*100):0;
  const flags=[];
  pastes.forEach(p=>{const pw=words(p.i); if(pw>=15) flags.push(`Pasted ${pw} words at ${mmss(p.t)} into the session`)});
  if(pastePct>=30) flags.push(`${pastePct}% of the final essay was pasted, not typed`);
  if(w>=120&&rev<2) flags.push(`Very few corrections (${rev}% of typed text deleted)`);
  if(wpm>90) flags.push(`Unusually fast typing (${wpm} words per minute)`);
  if(w>=150&&active<5*60000) flags.push(`${w} words written in only ${mmss(active)} of active time`);
  return {text,fin,w,typed,pasted,deleted,active,total:ops.length?ops[ops.length-1].t:0,sessions,pauses,longest,pastePct,wpm,rev,flags,pastes};
}

function chart(ops){
  if(!ops.length) return '<p class="note">No writing recorded.</p>';
  const Wd=640,Hd=200,L=44,R=12,T=12,B=30, total=Math.max(ops[ops.length-1].t,60000);
  let len=0; const pts=[[0,0]]; const pm=[];
  ops.forEach(o=>{len+=o.i.length-o.d; pts.push([o.t,len]); if(o.k==='paste') pm.push([o.t,len])});
  const maxL=Math.max(...pts.map(p=>p[1]),50); const yMax=Math.ceil(maxL/250)*250||250;
  const X=t=>L+(t/total)*(Wd-L-R), Y=v=>T+(1-v/yMax)*(Hd-T-B);
  const minStep=[1,2,5,10,15,20,30].find(m=>total/60000/m<=6)||60;
  let g='';
  for(let m=0;m*60000<=total;m+=minStep){const x=X(m*60000); g+=`<line x1="${x}" y1="${T}" x2="${x}" y2="${Hd-B}" stroke="var(--grid)"/><text x="${x}" y="${Hd-10}" font-size="11" text-anchor="middle" fill="var(--muted)">${m} min</text>`}
  for(let v=0;v<=yMax;v+=yMax/2){const y=Y(v); g+=`<line x1="${L}" y1="${y}" x2="${Wd-R}" y2="${y}" stroke="var(--grid)"/><text x="${L-6}" y="${y+4}" font-size="11" text-anchor="end" fill="var(--muted)">${v}</text>`}
  const d=pts.map((p,i)=>`${i?'L':'M'}${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join('');
  const area=d+`L${X(pts[pts.length-1][0]).toFixed(1)},${Y(0)}L${X(0)},${Y(0)}Z`;
  const dots=pm.map(p=>`<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="5" fill="var(--pen)" stroke="var(--panel)" stroke-width="2"/>`).join('');
  return `<div style="overflow-x:auto"><svg viewBox="0 0 ${Wd} ${Hd}" role="img" aria-label="Essay length over time">${g}
    <path d="${area}" fill="var(--chart)" fill-opacity=".12"/><path d="${d}" fill="none" stroke="var(--chart)" stroke-width="2" stroke-linejoin="round"/>${dots}</svg></div>`;
}

