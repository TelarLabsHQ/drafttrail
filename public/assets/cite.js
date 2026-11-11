// DraftTrail citations: format sources (Chicago notes-bibliography, Chicago author-date, APA 7, MLA 9),
// render a paper from plain text with [@key, page] citations, and build a Word (.docx) file with real footnotes.
// Italic text inside formatted strings is wrapped in \u0001 ... \u0002.
const Cite = (() => {
  const I = s => s ? `\u0001${s}\u0002` : '';
  const STYLES = {
    'cmos-nb': { name: 'Chicago (notes and bibliography)', list: 'Bibliography', notes: true },
    'cmos-ad': { name: 'Chicago (author-date)', list: 'References' },
    'apa': { name: 'APA 7th edition', list: 'References' },
    'mla': { name: 'MLA 9th edition', list: 'Works Cited' },
  };
  const TYPES = { book: 'Book', chapter: 'Chapter in an edited book', journal: 'Journal article', news: 'Newspaper or magazine article', web: 'Web page', other: 'Other (report, interview, video…)' };
  const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  const MLAM = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.'];

  /* ---------- small helpers ---------- */
  const t = s => String(s || '').trim();
  const dash = s => t(s).replace(/(\d)\s*[-–—]\s*(\d)/g, '$1–$2');
  const end = s => /[.?!]$/.test(s.replace(/[\u0001\u0002”’"]+$/, '')) ? s : s + '.';   // add a period unless one is there
  function people(str) {   // "Smith, Jane; Lee, Ann B." -> [{last, first}]; a name without a comma is an organization
    return t(str).split(/\s*;\s*/).filter(Boolean).map(n => { const i = n.indexOf(','); return i < 0 ? { last: n, first: '', org: true } : { last: t(n.slice(0, i)), first: t(n.slice(i + 1)) }; });
  }
  const fl = a => a.first ? `${a.first} ${a.last}` : a.last;           // Jane Smith
  const lf = a => a.first ? `${a.last}, ${a.first}` : a.last;          // Smith, Jane
  const initials = f => f.split(/[\s.]+/).filter(Boolean).map(w => w.includes('-') ? w.split('-').map(x => x[0] + '.').join('-') : w[0] + '.').join(' ');
  const apaName = a => a.first ? `${a.last}, ${initials(a.first)}` : a.last;
  function parseDate(s) { const m = t(s).match(/^(\d{4})(?:-(\d{1,2})(?:-(\d{1,2}))?)?$/); return m ? { y: m[1], m: m[2] ? +m[2] : 0, d: m[3] ? +m[3] : 0 } : null; }
  const longDate = d => !d ? '' : d.m ? `${MONTHS[d.m - 1]}${d.d ? ' ' + d.d : ''}, ${d.y}` : d.y;          // March 3, 2024
  const mdOnly = d => !d || !d.m ? '' : `${MONTHS[d.m - 1]}${d.d ? ' ' + d.d : ''}`;                     // March 3
  const mlaDate = d => !d ? '' : d.m ? `${d.d ? d.d + ' ' : ''}${MLAM[d.m - 1]} ${d.y}` : d.y;              // 3 Mar. 2024
  const year = s => t(s.year) || (parseDate(s.date) || {}).y || '';
  function shortTitle(title) {
    let w = t(title).split(':')[0].trim().split(/\s+/);
    if (w.length > 4 && /^(a|an|the)$/i.test(w[0])) w = w.slice(1);
    return w.slice(0, 4).join(' ').replace(/[,;]$/, '');
  }
  const isItalicType = s => ['book', 'other'].includes(s.type);
  const titleQ = (s, punct) => isItalicType(s) ? I(s.title) + punct : `“${t(s.title)}${punct}”`;   // punctuation goes inside quotation marks
  const link = s => t(s.url).replace(/^doi:\s*/i, 'https://doi.org/');

  /* ---------- author strings ---------- */
  function auNote(s) { const a = people(s.authors); if (!a.length) return ''; if (a.length === 1) return fl(a[0]); if (a.length === 2) return `${fl(a[0])} and ${fl(a[1])}`; return `${fl(a[0])} et al.`; }
  function auShort(s) { const a = people(s.authors); if (!a.length) return ''; if (a.length === 1) return a[0].last; if (a.length === 2) return `${a[0].last} and ${a[1].last}`; return `${a[0].last} et al.`; }
  function auBib(s) {
    const a = people(s.authors); if (!a.length) return '';
    const list = a.length > 6 ? a.slice(0, 3) : a;
    const out = list.map((p, i) => i ? fl(p) : lf(p));
    if (a.length > 6) return out.join(', ') + ', et al.';
    if (out.length === 1) return out[0];
    if (out.length === 2) return `${out[0]}, and ${out[1]}`;
    return out.slice(0, -1).join(', ') + ', and ' + out[out.length - 1];
  }
  function auAPA(s) {
    const a = people(s.authors).map(apaName); if (!a.length) return '';
    if (a.length === 1) return a[0]; if (a.length <= 20) return a.slice(0, -1).join(', ') + ', & ' + a[a.length - 1];
    return a.slice(0, 19).join(', ') + ', . . . ' + a[a.length - 1];
  }
  function auMLA(s) { const a = people(s.authors); if (!a.length) return ''; if (a.length === 1) return lf(a[0]); if (a.length === 2) return `${lf(a[0])}, and ${fl(a[1])}`; return `${lf(a[0])}, et al.`; }
  const pubInfo = s => [t(s.place) && t(s.publisher) ? `${t(s.place)}: ${t(s.publisher)}` : t(s.publisher) || t(s.place), year(s)].filter(Boolean).join(', ');

  /* ---------- Chicago notes ---------- */
  function noteFull(s, pg) {
    const au = auNote(s), P = pg ? dash(pg) : '', d = parseDate(s.date), yr = year(s), pre = au ? au + ', ' : '';
    switch (s.type) {
      case 'book': return `${pre}${I(s.title)}${pubInfo(s) ? ` (${pubInfo(s)})` : ''}${P ? ', ' + P : ''}.`;
      case 'chapter': return `${pre}“${t(s.title)},” in ${I(s.container)}${t(s.editors) ? ', ed. ' + t(s.editors) : ''}${pubInfo(s) ? ` (${pubInfo(s)})` : ''}${P ? ', ' + P : ''}.`;
      case 'journal': return `${pre}“${t(s.title)},” ${I(s.container)}${t(s.volume) ? ' ' + t(s.volume) : ''}${t(s.issue) ? ', no. ' + t(s.issue) : ''}${yr ? ` (${d && d.m ? (MONTHS[d.m - 1] + ' ') : ''}${yr})` : ''}${P ? ': ' + P : ''}${link(s) ? ', ' + link(s) : ''}.`;
      case 'news': return `${pre}“${t(s.title)},” ${I(s.container)}, ${longDate(d) || yr}${link(s) ? ', ' + link(s) : ''}.`;
      case 'web': return `${pre}“${t(s.title)},” ${t(s.container)}${d ? ', ' + longDate(d) : ''}${!d && t(s.accessed) ? ', accessed ' + longDate(parseDate(s.accessed)) : ''}${link(s) ? ', ' + link(s) : ''}.`;
      default: return `${pre}${I(s.title)}${t(s.container) ? ', ' + t(s.container) : ''}${yr ? ' (' + yr + ')' : ''}${P ? ', ' + P : ''}${link(s) ? ', ' + link(s) : ''}.`;
    }
  }
  function noteShort(s, pg) {
    const au = auShort(s), st = shortTitle(s.title), P = pg ? dash(pg) : '';
    const tt = isItalicType(s) ? I(st) + (P ? ', ' + P : '') + '.' : (P ? `“${st},” ${P}.` : `“${st}.”`);
    return au ? `${au}, ${tt}` : tt;
  }
  /* ---------- reference list entries ---------- */
  function bibNB(s) {
    const au = auBib(s), d = parseDate(s.date), yr = year(s), pre = au ? end(au) + ' ' : '';
    switch (s.type) {
      case 'book': return `${pre}${end(I(s.title))}${pubInfo(s) ? ' ' + pubInfo(s) + '.' : ''}`;
      case 'chapter': return `${pre}“${t(s.title)}.” In ${I(s.container)}${t(s.editors) ? ', edited by ' + t(s.editors) : ''}${t(s.pages) ? ', ' + dash(s.pages) : ''}.${pubInfo(s) ? ' ' + pubInfo(s) + '.' : ''}`;
      case 'journal': return `${pre}“${t(s.title)}.” ${I(s.container)}${t(s.volume) ? ' ' + t(s.volume) : ''}${t(s.issue) ? ', no. ' + t(s.issue) : ''}${yr ? ` (${d && d.m ? MONTHS[d.m - 1] + ' ' : ''}${yr})` : ''}${t(s.pages) ? ': ' + dash(s.pages) : ''}.${link(s) ? ' ' + link(s) + '.' : ''}`;
      case 'news': return `${pre}“${t(s.title)}.” ${I(s.container)}, ${longDate(d) || yr}.${link(s) ? ' ' + link(s) + '.' : ''}`;
      case 'web': return `${pre}“${t(s.title)}.” ${t(s.container)}${d ? ', ' + longDate(d) : ''}.${!d && t(s.accessed) ? ' Accessed ' + longDate(parseDate(s.accessed)) + '.' : ''}${link(s) ? ' ' + link(s) + '.' : ''}`;
      default: return `${pre}${end(I(s.title))}${t(s.container) ? ' ' + end(t(s.container)) : ''}${yr ? ' ' + yr + '.' : ''}${link(s) ? ' ' + link(s) + '.' : ''}`;
    }
  }
  function bibAD(s) {
    const au = auBib(s), d = parseDate(s.date), yr = year(s) || 'n.d.';
    const head = au ? `${end(au)} ${yr}.` : `${end(isItalicType(s) ? I(s.title) : '“' + t(s.title) + '.”')} ${yr}.`;
    const ttl = au ? ' ' + (isItalicType(s) ? end(I(s.title)) : `“${t(s.title)}.”`) : '';
    switch (s.type) {
      case 'book': return `${head}${ttl}${[t(s.place) && t(s.publisher) ? t(s.place) + ': ' + t(s.publisher) : t(s.publisher)].filter(Boolean).map(x => ' ' + x + '.').join('')}`;
      case 'chapter': return `${head}${ttl} In ${I(s.container)}${t(s.editors) ? ', edited by ' + t(s.editors) : ''}${t(s.pages) ? ', ' + dash(s.pages) : ''}.${t(s.publisher) ? ' ' + (t(s.place) ? t(s.place) + ': ' : '') + t(s.publisher) + '.' : ''}`;
      case 'journal': return `${head}${ttl} ${I(s.container)}${t(s.volume) ? ' ' + t(s.volume) : ''}${t(s.issue) ? ` (${t(s.issue)})` : ''}${t(s.pages) ? ': ' + dash(s.pages) : ''}.${link(s) ? ' ' + link(s) + '.' : ''}`;
      case 'news': return `${head}${ttl} ${I(s.container)}, ${mdOnly(d) || ''}.`.replace(', .', '.') + (link(s) ? ' ' + link(s) + '.' : '');
      case 'web': return `${head}${ttl} ${t(s.container)}${mdOnly(d) ? ', ' + mdOnly(d) : ''}.${!d && t(s.accessed) ? ' Accessed ' + longDate(parseDate(s.accessed)) + '.' : ''}${link(s) ? ' ' + link(s) + '.' : ''}`;
      default: return `${head}${ttl}${t(s.container) ? ' ' + end(t(s.container)) : ''}${link(s) ? ' ' + link(s) + '.' : ''}`;
    }
  }
  function bibAPA(s) {
    const au = auAPA(s), d = parseDate(s.date), yr = year(s) || 'n.d.', U = link(s) ? ' ' + link(s) : '';
    const when = (s.type === 'news' || s.type === 'web') && d && d.m ? `${d.y}, ${mdOnly(d)}` : yr;
    const ttlI = end(I(s.title)), ttlP = end(t(s.title));
    const lead = au ? `${end(au)} (${when}). ` : '';
    const T = x => au ? x : '';
    const noAu = x => au ? '' : `${x} (${when}). `;
    switch (s.type) {
      case 'book': return `${lead}${noAu(ttlI.replace(/\.$/, '')) || ''}${T(ttlI + ' ')}${t(s.publisher) ? end(t(s.publisher)) : ''}${U}`.replace(/\s+$/, '');
      case 'chapter': return `${lead}${noAu(ttlP.replace(/\.$/, ''))}${T(ttlP + ' ')}In ${t(s.editors) ? t(s.editors) + (/,| and |&/.test(t(s.editors)) ? ' (Eds.), ' : ' (Ed.), ') : ''}${I(s.container)}${t(s.pages) ? ` (pp. ${dash(s.pages)})` : ''}.${t(s.publisher) ? ' ' + end(t(s.publisher)) : ''}${U}`;
      case 'journal': return `${lead}${noAu(ttlP.replace(/\.$/, ''))}${T(ttlP + ' ')}${I(t(s.container) + (t(s.volume) ? ', ' + t(s.volume) : ''))}${t(s.issue) ? `(${t(s.issue)})` : ''}${t(s.pages) ? ', ' + dash(s.pages) : ''}.${U}`;
      case 'news': return `${lead}${noAu(ttlP.replace(/\.$/, ''))}${T(ttlP + ' ')}${end(I(s.container))}${U}`;
      case 'web': return `${lead}${noAu(ttlI.replace(/\.$/, ''))}${T(ttlI + ' ')}${t(s.container) ? end(t(s.container)) : ''}${U}`.replace(/\s+$/, '');
      default: return `${lead}${noAu(ttlI.replace(/\.$/, ''))}${T(ttlI + ' ')}${t(s.container) ? end(t(s.container)) : ''}${U}`.replace(/\s+$/, '');
    }
  }
  function bibMLA(s) {
    const au = auMLA(s), d = parseDate(s.date), yr = year(s), U = link(s).replace(/^https?:\/\//, '');
    const pre = au ? end(au) + ' ' : '';
    const ttl = isItalicType(s) ? end(I(s.title)) : `“${end(t(s.title))}”`;
    const parts = [];
    switch (s.type) {
      case 'book': parts.push(t(s.publisher), yr); break;
      case 'chapter': parts.push(I(s.container), t(s.editors) ? 'edited by ' + t(s.editors) : '', t(s.publisher), yr, t(s.pages) ? 'pp. ' + dash(s.pages) : ''); break;
      case 'journal': parts.push(I(s.container), t(s.volume) ? 'vol. ' + t(s.volume) : '', t(s.issue) ? 'no. ' + t(s.issue) : '', d && d.m ? mlaDate({ y: d.y, m: d.m }) : yr, t(s.pages) ? 'pp. ' + dash(s.pages) : '', U); break;
      case 'news': parts.push(I(s.container), mlaDate(d) || yr, U); break;
      case 'web': parts.push(I(s.container), mlaDate(d) || yr, U); break;
      default: parts.push(t(s.container), yr, U);
    }
    const tail = parts.filter(Boolean).join(', ');
    let out = `${pre}${ttl}${tail ? ' ' + tail + '.' : ''}`;
    if (!d && t(s.accessed) && (s.type === 'web')) out += ` Accessed ${mlaDate(parseDate(s.accessed))}.`;
    return out;
  }
  function entry(style, s) { return style === 'cmos-ad' ? bibAD(s) : style === 'apa' ? bibAPA(s) : style === 'mla' ? bibMLA(s) : bibNB(s); }
  const sortKey = s => (people(s.authors)[0] || { last: '' }).last.toLowerCase() || t(s.title).replace(/^(a|an|the)\s+/i, '').toLowerCase();

  /* ---------- in-text citations ---------- */
  function locator(style, pg) {
    pg = dash(pg); if (!pg) return '';
    if (style !== 'apa' || /[a-z]/i.test(pg)) return pg;
    return (/–|,/.test(pg) ? 'pp. ' : 'p. ') + pg;
  }
  function paren(style, s, pg) {
    const P = locator(style, pg), yr = year(s) || 'n.d.';
    const au = auShort(s) || (isItalicType(s) ? I(shortTitle(s.title)) : `“${shortTitle(s.title)}”`);
    if (style === 'apa') return `(${au.replace(' and ', ' & ')}, ${yr}${P ? ', ' + P : ''})`;
    if (style === 'mla') return `(${au}${P ? ' ' + P : ''})`;
    return `(${au} ${yr}${P ? ', ' + P : ''})`;
  }

  /* ---------- keys ---------- */
  function makeKey(s, sources) {
    const a = people(s.authors)[0];
    let base = ((a ? a.last : shortTitle(s.title).split(' ')[0]) || 'source').normalize('NFD').replace(/[^\p{L}\p{N}]/gu, '').toLowerCase().slice(0, 14) || 'source';
    base += year(s) || 'nd';
    let k = base, n = 0; const taken = new Set(sources.filter(x => x !== s && x.id !== s.id).map(x => x.key));
    while (taken.has(k)) k = base + 'abcdefghijklmnopqrstuvwxyz'[n++];
    return k;
  }
  const TOKEN = /\[@([\p{L}\p{N}]+)(?:\s*,\s*([^\]]*))?\]/gu;

  /* ---------- paper model ---------- */
  // Splits the plain text into blocks and resolves citations. Returns {blocks, notes, used, missing}.
  // A block is {kind:'h'|'p'|'q', parts:[{text}|{note:n}|{cite:'(Smith 2019, 4)'}]}; text may contain *italic* stars.
  function model(text, sources, style) {
    const S = STYLES[style] ? style : 'cmos-nb', byKey = new Map(sources.map(s => [s.key, s]));
    const blocks = [], notes = [], used = [], missing = new Set(); let lastNoteKey = null;
    for (let line of String(text).split(/\n/)) {
      if (!line.trim()) continue;
      let kind = 'p';
      const h = line.match(/^\s*#{1,3}\s+(.*)$/); if (h) { kind = 'h'; line = h[1]; }
      else { const q = line.match(/^\s*>\s?(.*)$/); if (q) { kind = 'q'; line = q[1]; } }
      const parts = []; let last = 0, m; TOKEN.lastIndex = 0;
      while ((m = TOKEN.exec(line))) {
        let before = line.slice(last, m.index); const key = m[1].toLowerCase(), pg = t(m[2]); last = TOKEN.lastIndex;
        const s = byKey.get(key);
        if (!s) { missing.add(m[1]); parts.push({ text: before }, { bad: m[0] }); continue; }
        if (!used.includes(s)) used.push(s);
        if (STYLES[S].notes) {
          before = before.replace(/\s+$/, '');
          // a note number goes after the punctuation that follows it
          const after = line.slice(last).match(/^[”’"]?[.,;:?!]+[”’"]?|^[”’"]/);
          if (after) { let a = after[0]; last += a.length; TOKEN.lastIndex = last;
            // American style: a period or comma goes inside the closing quotation mark
            const q = before.match(/[”"]$/); if (q && /^[.,]/.test(a)) { before = before.slice(0, -1) + a[0] + q[0]; a = a.slice(1); }
            before += a; }
          const first = !notes.some(n => n.key === key || (n.keys || []).includes(key));
          const nt = first ? noteFull(s, pg) : noteShort(s, pg);
          const prevPart = parts[parts.length - 1];
          if (prevPart && prevPart.note && !before.trim()) {   // two citations side by side share one note
            const n = notes[prevPart.note - 1]; n.text = n.text.replace(/\.$/, '') + '; ' + nt; (n.keys = n.keys || [n.key]).push(key);
            parts.push({ text: before.replace(/\s+/g, '') });
          } else { notes.push({ key, text: nt }); parts.push({ text: before }, { note: notes.length }); }
          lastNoteKey = key;
        } else {
          if (before && !/[\s(]$/.test(before)) before += ' ';
          parts.push({ text: before }, { cite: paren(S, s, pg) });
        }
      }
      parts.push({ text: line.slice(last) });
      blocks.push({ kind, parts: parts.filter(p => p.text !== '') });
    }
    const list = sources.filter(s => used.includes(s) || s.keep !== false).slice().sort((a, b) => sortKey(a).localeCompare(sortKey(b)) || year(a).localeCompare(year(b)));
    return { style: S, blocks, notes, used, missing: [...missing], list: list.map(s => entry(S, s)), listTitle: STYLES[S].list };
  }

  /* ---------- HTML ---------- */
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const fmtHTML = s => esc(s).replace(/\u0001/g, '<i>').replace(/\u0002/g, '</i>');
  const starsHTML = s => esc(s).replace(/\*([^*\n]+)\*/g, '<i>$1</i>');
  function html(m, title, name) {
    let h = `<div class="paper">${title ? `<h1 class="p-title">${starsHTML(title)}</h1>` : ''}${name ? `<p class="p-name">${esc(name)}</p>` : ''}`;
    for (const b of m.blocks) {
      const inner = b.parts.map(p => p.note ? `<sup>${p.note}</sup>` : p.cite ? fmtHTML(p.cite) : p.bad ? `<span class="p-bad" title="No source with this key">${esc(p.bad)}</span>` : starsHTML(p.text)).join('');
      h += b.kind === 'h' ? `<h2>${inner}</h2>` : b.kind === 'q' ? `<blockquote>${inner}</blockquote>` : `<p>${inner}</p>`;
    }
    if (m.notes.length) h += `<h2 class="p-sec">Notes</h2><ol class="p-notes">${m.notes.map(n => `<li>${fmtHTML(n.text)}</li>`).join('')}</ol>`;
    if (m.list.length) h += `<h2 class="p-sec">${m.listTitle}</h2>${m.list.map(e => `<p class="p-bib">${fmtHTML(e)}</p>`).join('')}`;
    return h + '</div>';
  }
  function plain(m, title, name) {
    const st = s => s.replace(/[\u0001\u0002]/g, '');
    let out = (title ? title + '\n' : '') + (name ? name + '\n' : '') + '\n';
    for (const b of m.blocks) out += (b.kind === 'h' ? '\n' : b.kind === 'q' ? '    ' : '') + b.parts.map(p => p.note ? toSup(p.note) : p.cite ? st(p.cite) : p.bad || p.text).join('') + '\n\n';
    if (m.notes.length) out += 'Notes\n\n' + m.notes.map((n, i) => `${i + 1}. ${st(n.text)}`).join('\n') + '\n\n';
    if (m.list.length) out += m.listTitle + '\n\n' + m.list.map(st).join('\n\n') + '\n';
    return out;
  }
  const toSup = n => String(n).replace(/\d/g, d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]);

  /* ---------- DOCX ---------- */
  const X = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  function runs(s, starItalic) {      // text -> <w:r> runs with italics
    let src = String(s);
    if (starItalic) src = src.replace(/\*([^*\n]+)\*/g, '\u0001$1\u0002');
    let out = '', it = false;
    for (const piece of src.split(/([\u0001\u0002])/)) {
      if (piece === '\u0001') { it = true; continue; } if (piece === '\u0002') { it = false; continue; } if (!piece) continue;
      out += `<w:r>${it ? '<w:rPr><w:i/></w:rPr>' : ''}<w:t xml:space="preserve">${X(piece)}</w:t></w:r>`;
    }
    return out;
  }
  const P = (style, body, extra = '') => `<w:p><w:pPr>${style ? `<w:pStyle w:val="${style}"/>` : ''}${extra}</w:pPr>${body}</w:p>`;
  function docx(m, title, name) {
    let body = '';
    if (title) body += P('Title', runs(title, true));
    if (name) body += P('Byline', runs(name));
    const fns = [];
    for (const b of m.blocks) {
      const inner = b.parts.map(p => {
        if (p.note) { fns.push(m.notes[p.note - 1].text); return `<w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteReference w:id="${p.note}"/></w:r>`; }
        if (p.cite) return runs(p.cite); if (p.bad) return runs(p.bad); return runs(p.text, true);
      }).join('');
      body += b.kind === 'h' ? P('Heading1', inner) : b.kind === 'q' ? P('BlockQuote', inner) : P('', inner);
    }
    if (m.list.length) { body += `<w:p><w:r><w:br w:type="page"/></w:r></w:p>` + P('ListTitle', runs(m.listTitle)) + m.list.map(e => P('Bib', runs(e))).join(''); }
    body += '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>';
    const NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"';
    const document = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document ${NS}><w:body>${body}</w:body></w:document>`;
    const footnotes = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:footnotes ${NS}>
<w:footnote w:type="separator" w:id="-1"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:separator/></w:r></w:p></w:footnote>
<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r><w:continuationSeparator/></w:r></w:p></w:footnote>
${m.notes.map((n, i) => `<w:footnote w:id="${i + 1}"><w:p><w:pPr><w:pStyle w:val="FootnoteText"/></w:pPr><w:r><w:rPr><w:rStyle w:val="FootnoteReference"/></w:rPr><w:footnoteRef/></w:r><w:r><w:t xml:space="preserve"> </w:t></w:r>${runs(n.text)}</w:p></w:footnote>`).join('')}</w:footnotes>`;
    const font = '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman" w:eastAsia="Times New Roman"/>';
    const styles = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles ${NS}>
<w:docDefaults><w:rPrDefault><w:rPr>${font}<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="480" w:lineRule="auto"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:ind w:firstLine="720"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Byline"><w:name w:val="Byline"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0"/><w:spacing w:after="240"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:ind w:firstLine="0"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="BlockQuote"><w:name w:val="Block Quote"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:firstLine="0"/><w:spacing w:before="120" w:after="240" w:line="240" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="ListTitle"><w:name w:val="List Title"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0"/><w:spacing w:after="240"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Bib"><w:name w:val="Bibliography"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:left="720" w:hanging="720"/><w:spacing w:after="240" w:line="240" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="FootnoteText"><w:name w:val="footnote text"/><w:basedOn w:val="Normal"/><w:pPr><w:ind w:firstLine="360"/><w:spacing w:after="120" w:line="240" w:lineRule="auto"/></w:pPr><w:rPr><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr></w:style>
<w:style w:type="character" w:styleId="FootnoteReference"><w:name w:val="footnote reference"/><w:rPr><w:vertAlign w:val="superscript"/></w:rPr></w:style>
</w:styles>`;
    const settings = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:settings ${NS}><w:footnotePr><w:footnote w:id="-1"/><w:footnote w:id="0"/></w:footnotePr><w:compat><w:compatSetting w:name="compatibilityMode" w:uri="http://schemas.microsoft.com/office/word" w:val="15"/></w:compat></w:settings>`;
    const files = {
      '[Content_Types].xml': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/><Override PartName="/word/footnotes.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/></Types>`,
      '_rels/.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>`,
      'word/_rels/document.xml.rels': `<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footnotes" Target="footnotes.xml"/></Relationships>`,
      'word/document.xml': document, 'word/styles.xml': styles, 'word/settings.xml': settings, 'word/footnotes.xml': footnotes,
    };
    return zip(files);
  }
  // minimal ZIP writer (stored, no compression)
  const CRC = (() => { const tb = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; tb[n] = c >>> 0; } return b => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = tb[(c ^ b[i]) & 0xFF] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }; })();
  function zip(files) {
    const enc = new TextEncoder(), chunks = [], central = []; let off = 0;
    for (const [name, text] of Object.entries(files)) {
      const nb = enc.encode(name), data = enc.encode(text), crc = CRC(data);
      const h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint16(6, 0x0800, true); h.setUint16(8, 0, true);
      h.setUint16(10, 0, true); h.setUint16(12, 0x5A21, true); h.setUint32(14, crc, true); h.setUint32(18, data.length, true); h.setUint32(22, data.length, true);
      h.setUint16(26, nb.length, true); h.setUint16(28, 0, true);
      chunks.push(new Uint8Array(h.buffer), nb, data);
      const c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true); c.setUint16(10, 0, true);
      c.setUint16(12, 0, true); c.setUint16(14, 0x5A21, true); c.setUint32(16, crc, true); c.setUint32(20, data.length, true); c.setUint32(24, data.length, true);
      c.setUint16(28, nb.length, true); c.setUint32(42, off, true);
      central.push(new Uint8Array(c.buffer), nb);
      off += 30 + nb.length + data.length;
    }
    const csize = central.reduce((n, a) => n + a.length, 0), e = new DataView(new ArrayBuffer(22)), count = Object.keys(files).length;
    e.setUint32(0, 0x06054b50, true); e.setUint16(8, count, true); e.setUint16(10, count, true); e.setUint32(12, csize, true); e.setUint32(16, off, true);
    return new Blob([...chunks, ...central, new Uint8Array(e.buffer)], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
  }

  return { STYLES, TYPES, model, html, plain, docx, entry, makeKey, people, TOKEN, year, fmtHTML };
})();
if (typeof module !== 'undefined') module.exports = Cite;
