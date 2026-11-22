"""DraftTrail help guides: practical articles for teachers (rendered by build.py under /guides/)."""

LEAD = 'Practical guides for checking student writing fairly in the age of AI, and for running writing tasks in class.'

GUIDES = [
dict(slug='check-student-writing-without-ai-detector', updated='2026-11-23',
     title='How to Check if a Student Used AI, Without an AI Detector',
     short='Check for AI use without a detector',
     desc='AI detectors guess, and sometimes accuse honest students. Here are fairer ways to check student writing: process evidence, conversation, sources and assignment design.',
     body='''<p class="lead">An AI detector looks at a finished essay and guesses. A fairer check looks at how the essay was made, and at whether the student understands it.</p>

<h2>Why detectors are a weak basis for a decision</h2>
<p>AI detectors give a score, not evidence. They can mark honest writing as AI-generated, especially short texts, very formal writing, and writing by students who are still learning English and use simple, predictable sentences. They can also miss AI text that was lightly edited. A score can’t be shown to a student or parent as proof of anything, and an unfair accusation can damage a student’s trust for years.</p>
<p>That doesn’t mean you should ignore your doubts. It means you need better evidence. Here are four kinds.</p>

<h2>1. Look at the writing process</h2>
<p>Real writing has a history: a slow start, sentences rewritten, paragraphs moved, pauses to think. Text pasted from a chatbot usually arrives in large blocks, with few corrections.</p>
<ul><li><b>Google Docs version history</b> shows how a document changed over time. See our guide to <a href="/guides/google-docs-version-history-student-writing/">checking student writing with version history</a>.</li>
<li><b><a href="/">DraftTrail</a></b> records every edit in its writing box, separates typed text from pasted text, and lets you replay the essay from the first word. It flags large pastes, very few corrections, unusually fast typing and long essays written in very little time. Each flag is a simple rule, listed on <a href="/how-it-works/">How it works</a>.</li>
<li><b>Drafts and outlines</b>: asking for a plan and a first draft before the final version is the oldest process check, and it still works.</li></ul>
<p>Process evidence protects honest students most. A student who wrote for three hours can show it.</p>

<h2>2. Talk with the student</h2>
<p>A five-minute conversation tells you more than any score. Keep it calm and curious, not accusing:</p>
<ul><li>“Walk me through how you wrote this. Where did you start?”</li>
<li>“This paragraph makes an interesting point. Can you explain it in your own words?”</li>
<li>“What does this word mean here?” for an unusual word in the essay.</li>
<li>“Which source gave you this idea? Can you show me where?”</li></ul>
<p>Students who wrote their own work can usually talk about it easily, even if they are nervous. Students who didn’t often can’t explain their own key sentences.</p>

<h2>3. Check the sources</h2>
<p>Chatbots sometimes invent sources: real-sounding books, articles or quotes that don’t exist, or real authors with made-up titles. Pick two or three references and look them up. Check that quoted passages appear in the source. A reference that can’t be found is a fair question to ask the student about.</p>
<p>In DraftTrail, students add sources and cite them as they write, and pasted passages they mark as quotes are listed separately, which makes this check quick.</p>

<h2>4. Compare with writing done in class</h2>
<p>A short piece written in class, on paper or in a monitored writing task, shows what a student can do on their own. If a take-home essay is very different in vocabulary, structure and accuracy, that’s worth a conversation. Our guide to <a href="/guides/in-class-writing-on-phones/">running an in-class writing task on phones</a> shows one way to do this with the devices students already have.</p>

<h2>Design assignments that are hard to outsource</h2>
<ul><li><b>Make it personal or local.</b> Ask students to connect the topic to their own experience, family, town or a class discussion.</li>
<li><b>Use your own materials.</b> A graph from your lesson, a case you wrote, or a reading only your class has is hard for a chatbot to use well.</li>
<li><b>Grade the process.</b> Give points for the outline, the draft and the reflection, not only the final text.</li>
<li><b>Ask for a short reflection</b>: what was hardest, what changed between drafts, which source was most useful.</li></ul>

<h2>When you have real doubts</h2>
<ol><li>Collect the evidence: process records, sources you checked, in-class work.</li>
<li>Talk with the student privately, and listen.</li>
<li>Follow your school’s academic honesty policy. If the evidence isn’t clear, give the student a chance to show their understanding, for example by rewriting a section in class.</li></ol>
<p>Be clear with students from the start about what AI use is allowed in your class. Many teachers allow it for brainstorming or checking grammar, but not for writing the text. Clear rules make honest choices easier.</p>
<p>Further reading: <a href="https://telarlabs.net/guides/writing-process-age-of-ai/">seeing the writing process in the age of AI</a>.</p>'''),

dict(slug='google-docs-version-history-student-writing', updated='2026-11-23',
     title='How to Use Google Docs Version History to Check Student Writing',
     short='Google Docs version history for student writing',
     desc='Step by step: open version history on a student’s Google Doc, read what it shows, spot pasted blocks, and understand its limits compared with a writing-process recorder.',
     body='''<p class="lead">Every Google Doc keeps a history of how it changed. For teachers, it’s a free, built-in way to see how a piece of writing was made.</p>

<h2>What you need</h2>
<p>You need <b>edit access</b> to the document. Version history isn’t available with view or comment access. In Google Classroom, if you create the assignment with <b>Make a copy for each student</b>, you have edit access to each student’s copy automatically. Otherwise, ask students to share the doc with you as an <b>Editor</b>.</p>

<h2>Open version history</h2>
<ol><li>Open the student’s document.</li>
<li>Choose <b>File → Version history → See version history</b>. The keyboard shortcut is <b>Ctrl + Alt + Shift + H</b> on Windows and ChromeOS, or <b>⌘ + Option + Shift + H</b> on a Mac.</li>
<li>A panel opens on the right with a list of versions, newest first, each with a date and time.</li>
<li>Click a version to see the document as it was at that moment.</li>
<li>Turn on <b>Show changes</b> at the bottom of the panel to highlight what was added at each step. Each person who edited gets a color.</li>
<li>Some versions are grouped. Click the small arrow next to a version to expand it into more detailed versions.</li></ol>

<h2>What to look for</h2>
<table class="tbl"><thead><tr><th>Pattern</th><th>What it may mean</th></tr></thead><tbody>
<tr><td>Many versions over several days, with text growing and changing</td><td>A normal writing process.</td></tr>
<tr><td>Whole paragraphs appearing in a single version, with no smaller steps before</td><td>Text that may have been pasted in. Worth asking where it came from: notes, another doc, or another source.</td></tr>
<tr><td>The first version already contains most of the essay</td><td>The text was written somewhere else and brought into this doc. Ask to see the original document.</td></tr>
<tr><td>Very few versions for a long essay, all within a few minutes</td><td>Fast work, or copied text. Look at the timestamps and talk with the student.</td></tr>
<tr><td>Edits made by another person’s color</td><td>Someone else edited the document. That may be fine (a peer review) or not, depending on your rules.</td></tr></tbody></table>

<h2>Limits of version history</h2>
<ul><li><b>It groups edits.</b> Versions are snapshots, not every keystroke. A paragraph typed in two minutes and a paragraph pasted in one second can look the same.</li>
<li><b>It doesn’t say “pasted”.</b> You can see that text appeared, not how it got there.</li>
<li><b>Writing somewhere else breaks it.</b> If a student writes in another app and copies the result in, the history starts with the finished text. That is a signal in itself, but it’s also how some honest students work, for example writing offline on a phone first.</li>
<li><b>It’s tied to the doc.</b> A student who makes a fresh copy of the document starts a new history.</li></ul>
<p>Use what you see as a reason to talk with the student, not as proof. Many honest students paste from their own notes or from a draft written on another device.</p>

<h2>When you need more detail: DraftTrail</h2>
<p><a href="/">DraftTrail</a> is a free writing page that records every edit inside its writing box, with the time. Compared with version history, it:</p>
<ul><li>separates <b>typed</b> text from <b>pasted</b> text, and shows exactly what was pasted and when;</li>
<li>counts active writing time, sessions, thinking pauses and corrections;</li>
<li>lets you <b>replay</b> the essay from the first word, faster than real time, with pasted text highlighted;</li>
<li>lets students cite sources and mark quotes, so honest quotations aren’t mistaken for copying.</li></ul>
<p>Students hand in a small .drafttrail file with their work, and you open many files at once on the <a href="/review/">review page</a>. Nothing is uploaded unless you use the live in-class mode. Set up a task on the <a href="/set-up/">set-up page</a>.</p>

<h2>Tell students in advance</h2>
<p>Let students know that you may look at how their work was written, and why: it helps you see their effort and protects them if anyone doubts their work. Students who know their process matters tend to keep drafts and notes, which is a good writing habit anyway.</p>
<p>Next: <a href="/guides/check-student-writing-without-ai-detector/">how to check if a student used AI, without an AI detector</a>.</p>'''),

dict(slug='in-class-writing-on-phones', updated='2026-11-23',
     title='How to Run an In-Class Writing Task on Students’ Phones',
     short='In-class writing on students’ phones',
     desc='A step-by-step plan for short answers and essays written in class on phones: setting up a live DraftTrail task, prompts that suit phones, timing, and reviewing the essays.',
     body='''<p class="lead">Writing done in class shows what students can do on their own. With a live DraftTrail task, students can write on the phones they already have while you see, live, who leaves the writing page.</p>

<h2>When to use it</h2>
<ul><li><b>Short answers and reflections</b> at the end of a lesson.</li>
<li><b>Timed essays</b> and exam questions that need a written answer.</li>
<li><b>A baseline sample</b> early in the term, to compare with later take-home work.</li>
<li><b>Exit tickets</b>: two or three sentences on what students learned today.</li></ul>

<h2>Set up the task</h2>
<ol><li>Open the <a href="/set-up/">set-up page</a> and type the assignment, for example “Explain how the water cycle affects our town during the rainy season.”</li>
<li>Choose <b>Live in class, with QuizPolice</b>. It opens QuizPolice with a DraftTrail writing task.</li>
<li>Choose how many exits are allowed before a student is locked, and add a timer if you want one.</li>
<li>Show the code or QR on the board. Students join, type their name and section, and write.</li></ol>
<p>On your dashboard you see, live, who is writing, who left the page and for how long, large pastes and word counts. When the time runs out, essays are handed in automatically. Essays are saved for up to 30 days and only you can see them.</p>

<h2>Write prompts that suit phones</h2>
<ul><li><b>Keep the length realistic.</b> Typing on a phone is slower than on a keyboard. 100 to 300 words in 20 to 30 minutes is a fair target for most students.</li>
<li><b>Show any reading on the board or on paper</b>, so students don’t need to switch apps to see it. Switching away counts as leaving the page.</li>
<li><b>Ask for thinking, not recall.</b> “Explain”, “compare”, “give an example from your own life” work better than “define”.</li>
<li><b>One task per session.</b> Several short questions in one box are fine; number them in the prompt.</li></ul>

<h2>Prepare the class</h2>
<ul><li>Ask students to charge their phones and close other apps.</li>
<li>Tell them clearly what is recorded: leaving the writing page, large pastes and word counts. Not their screen, camera or other apps.</li>
<li>Explain your rules on voice typing and spelling suggestions before you start, so everyone follows the same rules.</li>
<li>Have a plan for students without phones: a school device, or paper.</li></ul>

<h2>During the task</h2>
<ul><li>Keep the dashboard open and walk around.</li>
<li>If a student is locked after a notification or a call, ask what happened and unlock them if you’re satisfied.</li>
<li>Give one student extra time from the dashboard if their phone had a problem.</li></ul>

<h2>After the task</h2>
<ol><li>On the dashboard, choose <b>Download all essays</b>. You get one file with every student’s essay and its recording.</li>
<li>Open the <a href="/review/">DraftTrail review page</a> and drag the file in. Click a name to see the essay, the numbers and the replay.</li>
<li>Look at flags as reasons to ask, not proof. On phones, predictive text and autocorrect can make typing look a little faster than on a keyboard.</li></ol>

<h2>Use it as a writing sample</h2>
<p>Keep each student’s in-class piece. When a take-home essay later looks very different, you have a fair comparison, written in front of you, to talk about with the student. Read more in <a href="/guides/check-student-writing-without-ai-detector/">how to check if a student used AI, without an AI detector</a>.</p>

<h2>No reliable internet?</h2>
<p>The live mode needs a connection to send updates to your dashboard. Without one, use the <b>on their own</b> mode: students write on the DraftTrail page, which works offline once opened, and hand in the .drafttrail file afterwards. You won’t see exits live, but every exit is still recorded in the file.</p>'''),
]
