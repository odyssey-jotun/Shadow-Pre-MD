#!/usr/bin/env python3
"""Builds guide.html, the print source for the Shadow Pre-MD guide.

Twelve fixed Letter pages. Each page is a flex column that shares its spare
height between blocks, so no page ends with a hole at the foot.

Run: python3 guide.py && node render.mjs
"""
from html import escape

N = 43
TITLE = "The High School Student's Guide to Shadowing a Doctor"

CSS = r"""
@font-face{ font-family:'Newsreader'; font-weight:600 700; src:url(../fonts/newsreader-normal.woff2) format('woff2'); }
@font-face{ font-family:'DM Sans'; font-weight:400 700; src:url(../fonts/dm-sans-normal.woff2) format('woff2'); }
@page{ size: 8.5in 11in; margin: 0; }
:root{
  --paper:#F6F3EC; --card:#FFFFFF; --ink:#14232B; --soft:#465A65; --primary:#0F4C5C; --dark:#0A2B35;
  --rust:#C2571F; --teal:#008A9E; --gold:#D9A441; --peach:#F2A77E; --track:#DDE5E8; --line:rgba(20,35,43,.16);
}
*{ box-sizing:border-box; }
html,body{ margin:0; padding:0; }
body{ font-family:'DM Sans',sans-serif; font-size:10.4pt; line-height:1.5; color:var(--ink); -webkit-print-color-adjust:exact; print-color-adjust:exact; }
h1,h2,h3{ font-family:'Newsreader',Georgia,serif; font-weight:600; margin:0; letter-spacing:-0.012em; line-height:1.1; }
p{ margin:0; }
ul,ol{ margin:0; padding:0; list-style:none; }

.page{ width:8.5in; height:11in; position:relative; overflow:hidden; background:var(--paper);
  padding:.62in .7in .78in; display:flex; flex-direction:column; page-break-after:always; break-after:page; }
.page:last-child{ page-break-after:auto; break-after:auto; }
.body{ flex:1; display:flex; flex-direction:column; justify-content:space-between; min-height:0; }
.foot{ position:absolute; left:.7in; right:.7in; bottom:.4in; display:flex; justify-content:space-between;
  font-size:7.6pt; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--soft); }
.foot b{ color:var(--ink); }

/* section head: number, title and kicker are one unit */
.head{ display:grid; grid-template-columns:auto 1fr; column-gap:.2in; align-items:baseline;
  padding-bottom:.13in; border-bottom:1px solid var(--line); margin-bottom:.2in; }
.head .num{ font-weight:700; font-size:10pt; letter-spacing:.06em; color:var(--rust); }
.head h2{ font-size:27pt; color:var(--primary); }
.head .kicker{ grid-column:2; margin-top:.05in; font-size:7.8pt; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--soft); }
.lead{ font-size:11pt; line-height:1.5; }

.tag{ display:inline-block; font-size:7.4pt; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
  padding:.055in .16in; border-radius:99px; background:var(--gold); color:var(--dark); margin-bottom:.075in; }
.tag.teal{ background:#BFE3E8; } .tag.rust{ background:#F3C9B3; } .tag.dark{ background:var(--primary); color:#fff; }

.stats{ display:grid; grid-template-columns:repeat(3,1fr); gap:.16in; }
.stat{ background:var(--card); border:1px solid var(--line); border-bottom:5px solid var(--rust); border-radius:10px; padding:.15in .17in .14in; }
.stat:nth-child(2){ border-bottom-color:var(--teal); } .stat:nth-child(3){ border-bottom-color:var(--gold); }
.stat .n{ display:block; font-family:'Newsreader',serif; font-weight:700; font-size:24pt; line-height:1; color:var(--primary); margin-bottom:.06in; }
.stat .t{ display:block; font-size:8.8pt; font-weight:600; line-height:1.35; color:var(--soft); }

.panel{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:.19in .22in; }
.panel h3{ font-size:13pt; margin-bottom:.03in; }
.panel .sub{ font-size:8.4pt; color:var(--soft); margin-bottom:.12in; }
.bars li{ margin-top:.085in; } .bars li:first-child{ margin-top:0; }
.bars .lab{ display:flex; justify-content:space-between; align-items:baseline; font-size:8.9pt; font-weight:600; margin-bottom:.03in; }
.bars .v{ font-weight:400; color:var(--soft); font-size:8pt; white-space:nowrap; }
.bars .v b{ font-family:'Newsreader',serif; font-size:10.6pt; color:var(--ink); margin-left:.07in; }
.bars .track{ height:.085in; border-radius:3px; background:var(--track); overflow:hidden; }
.bars .fill{ display:block; height:100%; background:var(--teal); border-radius:0 3px 3px 0; }
.bars li.hl .fill{ background:var(--rust); } .bars li.mu .fill{ background:#8FA3AD; }

.cols{ display:grid; grid-template-columns:1fr 1fr; gap:.26in; }
.cols.wide-l{ grid-template-columns:1.25fr 1fr; } .cols.wide-r{ grid-template-columns:1fr 1.3fr; }
.dots li{ position:relative; padding-left:.2in; margin-top:.07in; }
.dots li:first-child{ margin-top:0; }
.dots li:before{ content:""; position:absolute; left:0; top:.075in; width:.075in; height:.075in; border-radius:50%; background:var(--gold); }
.dots.teal li:before{ background:var(--teal); } .dots.rust li:before{ background:var(--rust); }
.dots b{ font-weight:inherit; }

.checks{ display:grid; grid-template-columns:1fr 1fr; gap:.1in .3in; }
.checks li{ position:relative; padding-left:.27in; font-weight:600; font-size:9.8pt; }
.checks li:before{ content:""; position:absolute; left:0; top:.025in; width:.14in; height:.14in; border:1.6px solid var(--primary); border-radius:3px; }

.moves{ display:grid; grid-template-columns:repeat(3,1fr); gap:.16in; }
.move{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:.15in .16in; }
.move .k{ display:block; font-size:7.2pt; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--rust); margin-bottom:.03in; }
.move h3{ font-size:11.6pt; margin-bottom:.04in; }
.move p{ font-size:8.9pt; color:var(--soft); line-height:1.42; }
.moves.six{ grid-template-columns:repeat(3,1fr); }
.moves.two{ grid-template-columns:1fr 1fr; }

.quote{ position:relative; background:var(--dark); color:#fff; border-radius:12px; padding:.2in .3in .2in .62in; }
.quote:before{ content:"\201C"; position:absolute; left:.22in; top:.06in; font-family:'Newsreader',serif; font-size:40pt; line-height:1; color:var(--peach); }
.quote p{ font-family:'Newsreader',serif; font-style:italic; font-size:12.4pt; line-height:1.36; }
.quote cite{ display:block; margin-top:.06in; font-style:normal; font-size:7.4pt; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--peach); }

.letter{ background:var(--card); border:1px solid var(--line); border-left:5px solid var(--teal); border-radius:10px; padding:.18in .24in; font-size:9.5pt; line-height:1.5; }
.letter p + p{ margin-top:.07in; }
.letter .subj{ font-weight:700; color:var(--primary); }
.blank{ display:inline-block; min-width:.9in; border-bottom:1.2px solid #8FA3AD; height:.13in; vertical-align:baseline; }

.photo{ border-radius:12px; overflow:hidden; background:var(--track); }
.photo img{ display:block; width:100%; height:100%; object-fit:cover; }

table.log{ width:100%; border-collapse:collapse; font-size:8.2pt; background:var(--card); border-radius:10px; overflow:hidden; }
table.log th{ text-align:left; font-size:7pt; letter-spacing:.08em; text-transform:uppercase; color:#fff; background:var(--primary); padding:.07in .1in; }
table.log td{ border-bottom:1px solid var(--line); border-right:1px solid var(--line); height:.3in; }
table.log td:last-child{ border-right:0; }

.write{ display:grid; gap:.13in; }
.write .q{ font-weight:700; font-size:9.6pt; }
.write .ln{ border-bottom:1.1px solid #9FB2BB; height:.25in; }

.tip{ background:#FBF1EC; border:1px solid #EBCDBD; border-radius:10px; padding:.14in .2in; font-size:9.3pt; }
.tip b{ color:var(--rust); letter-spacing:.06em; text-transform:uppercase; font-size:7.6pt; display:block; margin-bottom:.02in; }

/* cover */
.cover{ padding:0; background:var(--dark); color:#fff; }
.cover .top{ padding:.75in .8in 0; flex:1; display:flex; flex-direction:column; }
.cover .badge{ align-self:flex-start; font-size:7.6pt; font-weight:700; letter-spacing:.12em; text-transform:uppercase; background:var(--peach); color:var(--dark); padding:.06in .17in; border-radius:99px; }
.cover h1{ font-size:45pt; line-height:1.02; margin-top:.36in; color:#fff; max-width:6.4in; }
.cover h1 span{ color:var(--peach); }
.cover .deck{ font-size:13pt; color:#BFD0D7; margin-top:.22in; max-width:5.6in; line-height:1.4; }
.cover .by{ margin-top:auto; padding-bottom:.3in; font-size:8.6pt; letter-spacing:.1em; text-transform:uppercase; font-weight:700; }
.cover .by span{ display:block; font-weight:400; letter-spacing:0; text-transform:none; color:#BFD0D7; font-size:9.4pt; margin-top:.03in; }
.cover .img{ height:5.2in; }
.cover .img img{ display:block; width:100%; height:100%; object-fit:cover; }

/* intro */
.me{ display:grid; grid-template-columns:2.35in 1fr; gap:.3in; align-items:start; }
.me .photo{ height:2.95in; }
.me p + p{ margin-top:.09in; }
.steps3{ display:grid; grid-template-columns:repeat(3,1fr); gap:.16in; }
.steps3 li{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:.15in .16in; }
.steps3 .c{ display:flex; align-items:center; justify-content:center; width:.34in; height:.34in; border-radius:50%; background:var(--primary); color:#fff; font-family:'Newsreader',serif; font-weight:700; font-size:12pt; margin-bottom:.08in; }
.steps3 h3{ font-size:11.6pt; margin-bottom:.03in; } .steps3 p{ font-size:8.9pt; color:var(--soft); line-height:1.42; }
.toc{ display:grid; grid-template-columns:1fr 1fr; gap:.05in .4in; font-size:9.4pt; }
.toc li{ display:flex; justify-content:space-between; border-bottom:1px dotted #9FB2BB; padding-bottom:.02in; }
.toc b{ color:var(--rust); margin-right:.1in; font-size:8pt; letter-spacing:.06em; }

/* back */
.back{ background:var(--dark); color:#fff; }
.back .head{ border-bottom-color:rgba(255,255,255,.2); } .back .head h2{ color:#fff; } .back .head .kicker{ color:#BFD0D7; } .back .head .num{ color:var(--peach); }
.back .lead{ color:#DCE7EB; }
.back .checks li{ color:#fff; } .back .checks li:before{ border-color:var(--peach); }
.glance{ display:grid; grid-template-columns:1fr 1fr; gap:.14in; }
.glance li{ background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.15); border-radius:10px; padding:.14in .18in; }
.glance .n{ display:block; font-family:'Newsreader',serif; font-weight:700; font-size:22pt; line-height:1; color:var(--peach); margin-bottom:.04in; }
.glance .t{ font-size:9pt; font-weight:600; color:#EEF4F6; }
.src{ font-size:7.5pt; line-height:1.42; color:#BFD0D7; } .src li + li{ margin-top:.035in; }
.back .foot{ color:#BFD0D7; } .back .foot b{ color:var(--peach); }
.sign{ font-size:8.6pt; color:#BFD0D7; } .sign b{ color:#fff; letter-spacing:.1em; text-transform:uppercase; font-size:8pt; display:block; }
"""


def pct(n):
    return round(100 * n / N)


def bars(rows, hl=(), mu=()):
    out = ['<ul class="bars">']
    for label, n in rows:
        cls = ' class="hl"' if label in hl else (' class="mu"' if label in mu else "")
        out.append(f'<li{cls}><div class="lab"><span>{escape(label)}</span><span class="v">{n} of {N}<b>{pct(n)}%</b></span></div>'
                   f'<div class="track"><span class="fill" style="width:{pct(n)}%"></span></div></li>')
    return "\n".join(out) + "</ul>"


def stats(items):
    return '<div class="stats">' + "".join(
        f'<div class="stat"><span class="n">{n}</span><span class="t">{t}</span></div>' for n, t in items) + "</div>"


def head(num, title, kicker):
    return (f'<div class="head"><span class="num">{num}</span><h2>{title}</h2>'
            f'<p class="kicker">{kicker}</p></div>')


def dots(items, tone=""):
    return f'<ul class="dots {tone}">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def checks(items):
    return '<ul class="checks">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def moves(items, cls=""):
    return f'<div class="moves {cls}">' + "".join(
        f'<div class="move"><span class="k">{k}</span><h3>{h}</h3><p>{p}</p></div>' for k, h, p in items) + "</div>"


def quote(text, who=""):
    c = f"<cite>{who}</cite>" if who else ""
    return f'<blockquote class="quote" style="margin:0"><p>{text}</p>{c}</blockquote>'


def page(n, inner, cls=""):
    foot = f'<div class="foot"><span>{TITLE}</span><b>{n}</b></div>'
    return f'<section class="page {cls}">{inner}{foot}</section>'


def block(tag, body, tone=""):
    return f'<div><span class="tag {tone}">{tag}</span>{body}</div>'


B = "<span class=\"blank\"></span>"

BARRIERS = [("Lack of physician time", 34), ("No formal shadowing structure", 24), ("Patient privacy and confidentiality", 22),
            ("Hospital or institutional policies", 22), ("Liability or administrative concerns", 19),
            ("Difficulty coordinating schedules", 18), ("Student preparedness and professionalism", 15),
            ("Uncertainty about what students may do", 12)]
FACTORS = [("Direct observation of patient care", 30), ("Ability to ask questions", 22), ("Interaction with physicians", 19),
           ("Career guidance", 17), ("Understanding clinical reasoning", 15), ("Exposure to medical procedures", 8)]
RESOURCES = [("Student orientation handbook", 28), ("Clear rules on what students may observe", 26),
             ("Suggested questions or discussion topics", 19), ("Pre-shadowing educational materials", 17),
             ("Professionalism expectations", 16)]

pages = []

# ------------------------------------------------------------------ 1 cover
pages.append(f"""<section class="page cover">
  <div class="top">
    <span class="badge">Physician survey edition</span>
    <h1>The High School Student's Guide to <span>Shadowing a Doctor</span></h1>
    <p class="deck">How to find a physician, ask the right way, show up prepared, and learn something real from every day in the clinic.</p>
    <p class="by">By Zoha Waheed<span>Built from a survey of 43 practicing physicians. 2026.</span></p>
  </div>
  <div class="img"><img src="img/cover.jpg" alt=""></div>
</section>""")

# ------------------------------------------------------------------ 2 start here
pages.append(page(2, f"""
{head("00", "Start Here", "Why I wrote this guide and how to use it")}
<div class="body">
  <div class="me">
    <div class="photo"><img src="img/zoha.jpg" alt=""></div>
    <div>
      <p class="lead">I'm Zoha Waheed. I walked into my first endocrinology clinic knowing little more than what Google had told me the week before.</p>
      <p>Since then I have shadowed seven physicians across four specialties. Even once I had those days, I found it difficult to get the most out of them.</p>
      <p>So I surveyed 43 practicing physicians about what stops them from hosting high schoolers and what makes a shadowing day worth it. I also read five peer-reviewed studies on how students learn in the clinic.</p>
      <p>This guide turns what they told me into steps you can follow.</p>
    </div>
  </div>
  {block("How to use this guide", '''<ol class="steps3">
    <li><span class="c">1</span><h3>Get the day</h3><p>Sections 1 to 3 show you why doctors say no, where to look, and how to ask.</p></li>
    <li><span class="c">2</span><h3>Show up ready</h3><p>Sections 4 to 6 cover paperwork, what to wear, and the privacy rules.</p></li>
    <li><span class="c">3</span><h3>Learn from it</h3><p>Sections 7 to 9 cover what to watch, what to ask, and what to write down.</p></li>
  </ol>''')}
  {block("What physicians told me", stats([("72%", "would likely host a student if the right resources were in place."),
                                          ("65%", "asked for students to arrive with an orientation handbook."),
                                          ("51%", "said the chance to ask questions makes shadowing meaningful.")]), "teal")}
  {block("Inside", '''<ul class="toc">
    <li><span><b>01</b>Why doctors say no</span><span>3</span></li><li><span><b>06</b>Privacy and professionalism</span><span>8</span></li>
    <li><span><b>02</b>Find a doctor to shadow</span><span>4</span></li><li><span><b>07</b>What to watch for</span><span>9</span></li>
    <li><span><b>03</b>How to ask</span><span>5</span></li><li><span><b>08</b>Questions to ask a doctor</span><span>10</span></li>
    <li><span><b>04</b>Before your first day</span><span>6</span></li><li><span><b>09</b>After each day</span><span>11</span></li>
    <li><span><b>05</b>What to wear and bring</span><span>7</span></li><li><span><b>10</b>Ready to shadow</span><span>12</span></li>
  </ul>''', "dark")}
</div>"""))

# ------------------------------------------------------------------ 3 why doctors say no
pages.append(page(3, f"""
{head("01", "Why Doctors Say No", "Know the barriers before you ask")}
<div class="body">
  <p class="lead">A doctor who turns you down is rarely saying no to you. When I asked 43 physicians what gets in the way of hosting a high school student, their answers were about time, missing structure, and hospital rules. Once you know the obstacle, you can write a request that removes it.</p>
  {stats([("79%", "named lack of time, the most common barrier."),
          ("56%", "said no formal shadowing structure exists for them to follow."),
          ("51%", "named hospital policies, and the same share named patient privacy.")])}
  <div class="panel"><h3>Every barrier physicians named</h3><p class="sub">Share of 43 physicians selecting each</p>
    {bars(BARRIERS, hl=("Lack of physician time",))}</div>
  {block("Turn each barrier into your next move", moves([
      ("If the barrier is time", "Ask for less", "Request one half day. Offer three dates and let the office choose."),
      ("If the barrier is structure", "Bring the plan", "Say what you hope to observe and that you will follow their lead."),
      ("If the barrier is policy", "Ask the office first", "Call the front desk and ask who approves student observers.")]), "rust")}
</div>"""))

# ------------------------------------------------------------------ 4 find a doctor
pages.append(page(4, f"""
{head("02", "Find a Doctor to Shadow", "Start with people who already know you")}
<div class="body">
  <p class="lead">Most shadowing days start with a personal connection. A physician is far more likely to answer a student they have some tie to than a stranger. Work outward from the people closest to you, and keep track of everyone you contact.</p>
  {moves([
      ("Closest", "Your own doctors", "Your pediatrician, family doctor, or dentist already knows you. Ask at your next visit."),
      ("Close", "Family and friends", "Ask parents, relatives, neighbors, and friends' parents who they know in medicine."),
      ("At school", "Counselors and teachers", "School counselors and science teachers often know alumni and local physicians."),
      ("In town", "Private practices", "Small clinics have fewer layers of approval than large hospitals. Call the office manager."),
      ("Hospitals", "Volunteer offices", "Many hospitals route student observers through a volunteer or education office."),
      ("Programs", "Health career clubs", "Groups such as HOSA and local health career programs can connect students with hosts.")], "six")}
  {stats([("63%", "of the physicians I surveyed had already hosted a high school student."),
          ("27", "physicians had hosted before. Ask a doctor who has and you skip the first-time worries."),
          ("16", "had never hosted one. A short, prepared request matters most with them.")])}
  {block("Outreach tracker", '''<table class="log"><thead><tr><th style="width:24%">Physician or office</th><th style="width:17%">Specialty</th><th style="width:21%">How I know them</th><th style="width:13%">Date asked</th><th style="width:13%">Follow-up</th><th>Answer</th></tr></thead><tbody>'''
         + ("<tr>" + "<td></td>" * 6 + "</tr>") * 5 + "</tbody></table>", "teal")}
  {quote("High school students shouldn't have to endlessly email physicians with no hope of finding any shadowing opportunities.", "Zoha Waheed")}
</div>"""))

# ------------------------------------------------------------------ 5 how to ask
pages.append(page(5, f"""
{head("03", "How to Ask a Doctor to Shadow", "A short, specific request is easier to say yes to")}
<div class="body">
  <p class="lead">Physicians read email between patients. Keep your request under 150 words, say exactly what you are asking for, and answer their worries before they have to raise them.</p>
  <div class="cols wide-r">
    {block("What a good request includes", dots([
        "<b>Who you are:</b> name, school, and grade.",
        "<b>Your connection:</b> how you found them.",
        "<b>Why them:</b> one sentence on why their specialty interests you.",
        "<b>A small ask:</b> one half day, with flexible dates.",
        "<b>Proof you are ready:</b> you know the privacy rules and will complete any forms.",
        "<b>An easy out:</b> thank them either way."]))}
    <div class="letter">
      <p class="subj">Subject: High school student asking to shadow for a half day</p>
      <p>Dear Dr. {B},</p>
      <p>My name is {B} and I am a {B} at {B} High School. {B} suggested I contact you. I am considering a career in medicine and would like to learn what a day in {B} looks like.</p>
      <p>Would you allow me to observe for one half day? I am free on {B}, {B}, or {B}, and I can work around your schedule. I understand patient confidentiality and will complete any forms your office requires.</p>
      <p>Thank you for considering it.</p>
      <p>Sincerely, {B}<br>Phone: {B}</p>
    </div>
  </div>
  {moves([
      ("After one week", "Follow up once", "Reply to your own email with two sentences. Then call the office and ask for the manager."),
      ("After two weeks", "Move on politely", "No answer usually means no time. Thank them and contact the next name on your list."),
      ("When they say yes", "Confirm in writing", "Repeat the date, time, address, dress code, and who to ask for when you arrive.")])}
  {block("Before you press send", checks(["The doctor's name is spelled correctly", "The email is under 150 words",
                                           "My phone number is included", "A parent or teacher has read it"]), "rust")}
  {block("If you call the office instead", f'''<div class="letter"><p>"Hello, my name is {B}. I am a high school student interested in medicine. Could you tell me who handles requests to observe a physician, and the best way to reach them?"</p></div>''', "teal")}
</div>"""))

# ------------------------------------------------------------------ 6 before your first day
pages.append(page(6, f"""
{head("04", "Before Your First Day", "Arrive ready and you remove a doctor's biggest doubt")}
<div class="body">
  <p class="lead">Student preparedness worried 56% of the physicians who had never hosted a student, against 22% of those who had. The doctors asked for the fix themselves: students who arrive already oriented.</p>
  <div class="panel"><h3>What physicians asked for</h3><p class="sub">Share of 43 physicians requesting each resource</p>
    {bars(RESOURCES, hl=("Student orientation handbook",))}</div>
  <div class="cols">
    {block("Ask the office about paperwork", dots([
        "<b>Age minimum:</b> many hospitals set one, often 16.",
        "<b>Confidentiality form:</b> most require a signed agreement.",
        "<b>Parent permission:</b> expect a signature if you are under 18.",
        "<b>Health records:</b> some ask for immunizations or a TB test.",
        "<b>Badge and parking:</b> where to check in and where to park."], "teal"), "teal")}
    {block("Learn the basics first", dots([
        "<b>The specialty:</b> what it treats and who its patients are.",
        "<b>Five common conditions:</b> read a plain-language summary of each.",
        "<b>Ten key terms:</b> write them in the front of your notebook.",
        "<b>The physician:</b> read their practice's website.",
        "<b>The route:</b> plan to arrive 15 minutes early."]))}
  </div>
  {block("The night before", checks(["Forms signed and printed", "Clothes laid out", "Notebook and two pens packed", "Questions written down",
                                      "Address and contact name saved", "Alarm set, breakfast planned"]), "rust")}
</div>"""))

# ------------------------------------------------------------------ 7 wear and bring
pages.append(page(7, f"""
{head("05", "What to Wear to Shadow a Doctor", "Dress like you work there")}
<div class="body">
  <p class="lead">Patients will assume you are part of the team, so dress the part. Unless the office tells you otherwise, wear business casual. Save the scrubs for when someone hands them to you.</p>
  <div class="cols">
    <div style="display:flex;flex-direction:column;justify-content:space-between;gap:.2in">
    {block("Wear", dots([
        "Business casual: slacks or a knee-length skirt with a collared shirt or blouse.",
        "Closed-toe shoes you can stand in for hours.",
        "Hair tied back if it is long.",
        "Scrubs only if the office asks for them."]))}
    {block("Leave at home", dots([
        "Perfume or cologne. Patients may be sensitive to scent.",
        "Dangling jewelry and long necklaces.",
        "Jeans, shorts, and open-toe shoes.",
        "Anything with large logos or slogans."], "rust"), "rust")}
    </div>
    <div class="photo" style="height:3.2in"><img src="img/students.jpg" alt=""></div>
  </div>
  {moves([
      ("Scrubs", "Change when you get there", "Some surgical settings hand observers scrubs on arrival. Arrive in business casual and change on site."),
      ("White coats", "Leave them to the staff", "A white coat tells patients you are a clinician. Observers should not wear one."),
      ("Badges", "Keep yours visible", "If the office gives you a visitor or observer badge, wear it where people can read it.")])}
  {block("Bring", checks(["Small notebook that fits a pocket", "Two pens", "Photo ID", "Signed forms",
                          "Water bottle and a snack", "Phone on silent, kept in your bag"]), "teal")}
  <div class="tip"><b>If you feel faint</b>Feeling lightheaded during a first procedure is common and nothing to be embarrassed about. Eat breakfast, keep your knees unlocked, and if the room starts to tilt, sit down and tell someone right away.</div>
</div>"""))

# ------------------------------------------------------------------ 8 privacy
pages.append(page(8, f"""
{head("06", "Patient Privacy and Professionalism", "The rules that keep you welcome")}
<div class="body">
  <p class="lead">Every patient you see is trusting the room with private information. In the United States that trust is protected by a federal law called HIPAA. Half of the physicians I surveyed named privacy as a barrier to hosting students, so show them you take it seriously.</p>
  {stats([("51%", "of physicians named patient privacy as a barrier to hosting."),
          ("33%", "asked for HIPAA and confidentiality training for students."),
          ("37%", "asked for clear professionalism expectations.")])}
  <div class="cols">
    {block("Always", dots([
        "<b>Introduce yourself</b> and let the patient decide if you stay.",
        "<b>Step out</b> the moment anyone asks you to.",
        "<b>Stand where you are told</b> and keep out of the way.",
        "<b>Keep your notes free of names,</b> birth dates, and room numbers.",
        "<b>Wash or sanitize your hands</b> going in and coming out."], "teal"), "teal")}
    {block("Never", dots([
        "<b>Take photos or video,</b> even of an empty room.",
        "<b>Post about a patient,</b> even without a name.",
        "<b>Discuss a case</b> in hallways, elevators, or at home.",
        "<b>Touch a patient or equipment</b> unless the physician asks.",
        "<b>Offer medical opinions</b> to a patient or family."], "rust"), "rust")}
  </div>
  {block("Three terms to know", moves([
      ("The law", "HIPAA", "The federal law that protects the privacy of a patient's health information."),
      ("The information", "PHI", "Protected health information: anything that could identify a patient, from a name to a photo."),
      ("The habit", "Need to know", "Only the people caring for a patient should hear the details. That rule applies to you too.")]))}
  {block("What to say when you meet a patient", f'''<div class="letter"><p>"Hello, my name is {B}. I am a high school student observing Dr. {B} today. Is it all right with you if I stay in the room?"</p><p>If the patient says no, smile, thank them, and wait outside. It is their right, and physicians notice students who handle it well.</p></div>''')}
</div>"""))

# ------------------------------------------------------------------ 9 what to watch
pages.append(page(9, f"""
{head("07", "What to Do When Shadowing a Doctor", "Watch how a physician thinks")}
<div class="body">
  <p class="lead">Students often hope for a dramatic procedure. Physicians told me the value lies elsewhere: in watching patient care up close and understanding the reasoning behind it. Procedures ranked near the bottom.</p>
  <div class="photo" style="height:2.8in"><img src="img/notes.jpg" alt=""></div>
  <div class="cols wide-l">
    <div class="panel"><h3>What makes shadowing meaningful</h3><p class="sub">Share of 43 physicians selecting each factor</p>
      {bars(FACTORS, hl=("Ability to ask questions",), mu=("Exposure to medical procedures",))}</div>
    {block("Watch for these six things", dots([
        "<b>The opening:</b> how the physician greets the patient and starts the visit.",
        "<b>The history:</b> which questions get asked, and in what order.",
        "<b>The exam:</b> what the physician checks and what gets skipped.",
        "<b>The reasoning:</b> what changed their mind along the way.",
        "<b>The explanation:</b> how a diagnosis is put in plain words.",
        "<b>The team:</b> who else helps, and what each person does."]))}
  </div>
  <div class="tip"><b>Shadow more than one specialty</b>A day in endocrinology looks nothing like a day in rheumatology. Seeing several specialties shows you different kinds of patients, problems, and pace, and it helps you picture where you fit.</div>
</div>"""))

# ------------------------------------------------------------------ 10 questions
pages.append(page(10, f"""
{head("08", "Questions to Ask a Doctor You Shadow", "Ask between patients")}
<div class="body">
  <p class="lead">More than half of the physicians I surveyed said the ability to ask questions is what makes shadowing meaningful. Write yours down before you arrive. Hold them until the patient has left, then ask while the visit is fresh.</p>
  <div class="cols wide-l">
    <div>
      {block("About the patient you just saw", dots([
          "What information mattered most in making that decision?",
          "What possibilities were you considering?",
          "How did you decide which tests were necessary?",
          "What made this case difficult?"]))}
    </div>
    <div class="photo" style="height:2.35in"><img src="img/pair.jpg" alt=""></div>
  </div>
  <div class="cols">
    {block("About the work", dots([
        "What does a typical week look like for you?",
        "Which parts of your job differ most from what students expect?",
        "What do you wish you had more time for?",
        "What is the hardest part of this specialty?"], "teal"), "teal")}
    {block("About the path", dots([
        "When did you know you wanted this specialty?",
        "What would you do differently in high school or college?",
        "What should I be doing now to prepare?",
        "Who else would you suggest I talk to or shadow?"], "rust"), "rust")}
  </div>
  {moves([
      ("Timing", "Between patients", "Save questions for the hallway or the end of the day, never in front of a patient."),
      ("Depth", "Ask why", "Questions about reasoning teach you more than questions about facts you can look up."),
      ("Limits", "Read the room", "On a packed day, pick your best two questions and write the others down for later.")])}
  <div class="tip"><b>Questions to skip</b>Leave out anything about salary, anything that names or identifies a patient, and anything a quick search could answer. Use your time with a physician for what only a physician can tell you.</div>
</div>"""))

# ------------------------------------------------------------------ 11 after each day
pages.append(page(11, f"""
{head("09", "After Each Day of Shadowing", "Write it down while it is fresh")}
<div class="body">
  <p class="lead">The studies I read agreed on one habit: reflection. Students who put their clinical experiences into writing analyze what they saw more carefully and notice what they still need to learn. Give yourself fifteen minutes the same evening.</p>
  {block("Shadowing journal", f'''<div class="panel write">
      <div><p class="q">Date, physician, and specialty</p><div class="ln"></div></div>
      <div><p class="q">What did I observe today? (no patient names)</p><div class="ln"></div><div class="ln"></div></div>
      <div><p class="q">What surprised me?</p><div class="ln"></div><div class="ln"></div></div>
      <div><p class="q">What did I learn about how this physician makes decisions?</p><div class="ln"></div><div class="ln"></div></div>
      <div><p class="q">What questions do I still have?</p><div class="ln"></div><div class="ln"></div></div>
      <div><p class="q">Could I see myself doing this work? Why or why not?</p><div class="ln"></div><div class="ln"></div></div>
    </div>''', "teal")}
  {block("Send a thank-you note within two days", f'''<div class="letter">
      <p>Dear Dr. {B},</p>
      <p>Thank you for letting me shadow you on {B}. Watching you {B} taught me {B}. I especially appreciated the time you took to explain {B}.</p>
      <p>The day made me more certain that {B}. Thank you again for your generosity.</p>
      <p>Sincerely, {B}</p></div>''')}
</div>"""))

# ------------------------------------------------------------------ 12 back
pages.append(page(12, f"""
{head("10", "Ready to Shadow?", "Your checklist, your log, and the research behind this guide")}
<div class="body">
  <p class="lead">Physicians want to teach. Arrive prepared, ask good questions, and write down what you saw, and you will leave with a clearer answer about medicine than you came in with.</p>
  {block("Final checklist", checks(["I know who approves observers at this office", "My forms are signed", "I know the dress code",
                                    "I can explain the privacy rules", "My questions are written down", "My journal page is ready"]))}
  {block("Shadowing log", '''<table class="log"><thead><tr><th style="width:15%">Date</th><th style="width:27%">Physician</th><th style="width:22%">Specialty</th><th style="width:12%">Hours</th><th>One thing I learned</th></tr></thead><tbody>'''
         + ("<tr>" + "<td></td>" * 5 + "</tr>") * 3 + "</tbody></table>", "teal")}
  {block("The survey in one glance", '''<ul class="glance">
      <li><span class="n">79%</span><span class="t">named lack of time as a barrier</span></li>
      <li><span class="n">72%</span><span class="t">would likely host with the right resources</span></li>
      <li><span class="n">65%</span><span class="t">asked for a student orientation handbook</span></li>
      <li><span class="n">51%</span><span class="t">said asking questions makes shadowing meaningful</span></li></ul>''', "rust")}
  <div>
    <span class="tag dark">Sources</span>
    <ol class="src">
      <li>Waheed, Z. S. (2026). Physician perspectives on high school shadowing: Barriers, educational value, and opportunities for standardization. Survey of 43 practicing physicians. Abstract submitted to the 2027 Medical Education Innovation Conference.</li>
      <li>Mann, K., Gordon, J., &amp; MacLeod, A. (2009). Reflection and reflective practice in health professions education: A systematic review. Advances in Health Sciences Education, 14(4), 595-621.</li>
      <li>Mafinejad, M. K., et al. (2022). Reflection on near-peer shadowing program. BMC Medical Education, 22.</li>
      <li>Estes, M., et al. (2026). From fly on the wall to future colleagues: Best practice recommendations for medical student shadowing programs. AEM Education and Training, 10(3).</li>
    </ol>
  </div>
  <p class="sign"><b>Developed by Zoha Waheed</b>Shadow Pre-MD. Free for any student to use and share. Hospital rules vary, so always follow the instructions of the office hosting you.</p>
</div>""", "back"))

import re
SCALE = 1.05
CSS = re.sub(r"font-size:([\d.]+)pt", lambda m: f"font-size:{float(m.group(1)) * SCALE:.2f}pt", CSS)

html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{TITLE}</title>
<meta name="author" content="Zoha Waheed"><style>{CSS}</style></head><body>
{''.join(pages)}
</body></html>"""
open("guide.html", "w").write(html)
print("wrote guide.html,", len(pages), "pages")
